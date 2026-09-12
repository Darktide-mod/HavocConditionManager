-- Bounded diagnostics for the low-FPS investigation. Samples one frame in ten;
-- no native hook changes, playback changes, per-unit logs or recurring timers.
local P={}
local function system_clock()
    local ffi=Mods and Mods.lua and Mods.lua.ffi or require("ffi")
    if not pcall(ffi.typeof,"HCMFrenzyCounter171") then
        ffi.cdef[[typedef int64_t HCMFrenzyCounter171;
            int QueryPerformanceCounter(int64_t *);
            int QueryPerformanceFrequency(int64_t *);]]
    end
    local kernel=ffi.load("kernel32")
    local value,frequency=ffi.new("HCMFrenzyCounter171[1]"),ffi.new("HCMFrenzyCounter171[1]")
    assert(kernel.QueryPerformanceFrequency(frequency)~=0,"performance clock unavailable")
    local scale=1/tonumber(frequency[0])
    return function()kernel.QueryPerformanceCounter(value);return tonumber(value[0])*scale end
end
function P.new(log,world,clock)
    if not clock then
        local ok,value=pcall(system_clock)
        if not ok then log("[Frenzied perf] unavailable="..tostring(value));return end
        clock=value
    end
    local p={clock=clock,world=world,log=log,frames=0,sampling=false,stopped=false,histogram={}}
    function p:reset()
        self.intervals,self.frame_ms,self.frame_max=0,0,0
        self.samples,self.prepare,self.world_time,self.after,self.prepare_max,self.world_max=0,0,0,0,0,0
        self.ai_calls,self.ai_own,self.ai_native,self.node_swaps=0,0,0,0
        self.tracked,self.animated,self.tracked_max,self.animated_max=0,0,0,0
        table.clear(self.histogram)
    end
    function p:report(reason)
        if not self.started then return end
        local count,total,p95=0,math.ceil(self.intervals*.95),0
        if total>0 then
            for bucket=1,512 do count=count+(self.histogram[bucket] or 0);if count>=total then p95=bucket/2;break end end
        end
        local frames=math.max(self.intervals,1);local samples=math.max(self.samples,1)
        local mean=self.frame_ms/frames
        self.log(string.format("[Frenzied perf] version=1.7.1 reason=%s interval_frames=%d fps=%.1f frame_ms=%.2f p95_ms=%.2f max_ms=%.2f samples=%d tracked=%.1f/%d animated=%.1f/%d prepare_ms=%.3f prepare_max_ms=%.3f world_ms=%.3f world_max_ms=%.3f after_ms=%.3f ai_calls=%d ai_own_total_ms=%.3f ai_inner_total_ms=%.3f node_swaps=%d",
            reason,self.intervals,mean>0 and 1000/mean or 0,mean,p95,self.frame_max,self.samples,
            self.tracked/samples,self.tracked_max,self.animated/samples,self.animated_max,
            self.prepare*1000/samples,self.prepare_max*1000,self.world_time*1000/samples,self.world_max*1000,
            self.after*1000/samples,self.ai_calls,self.ai_own*1000,self.ai_native*1000,self.node_swaps))
    end
    function p:begin(world,dt)
        if self.stopped or world~=self.world then return end
        if dt<=0 or not World.get_data(world,"active") or World.get_data(world,"paused") then
            self.last_frame=nil;self.sampling=false;return
        end
        local now=self.clock()
        if not self.started then
            self.started,self.window=now,now
            self.log("[Frenzied perf] start duration_s=180 report_s=10 sample_every=10 world_includes_engine_and_callbacks=true")
        end
        if self.last_frame then
            local ms=math.max(0,(now-self.last_frame)*1000)
            self.intervals=self.intervals+1;self.frame_ms=self.frame_ms+ms;self.frame_max=math.max(self.frame_max,ms)
            local bucket=math.max(1,math.min(512,math.ceil(ms*2)))
            self.histogram[bucket]=(self.histogram[bucket] or 0)+1
        end
        self.last_frame=now
        if now-self.started>=180 then self:stop("completed");return end
        if now-self.window>=10 then self:report("window");self:reset();self.window=now end
        self.frames=self.frames+1;self.sampling=self.frames%10==1
        return self.sampling and self.clock() or nil
    end
    function p:ai(a,b,c,d,nodes)
        self.ai_calls=self.ai_calls+1
        self.ai_own=self.ai_own+(b-a)+(d-c);self.ai_native=self.ai_native+(c-b)
        self.node_swaps=self.node_swaps+nodes
    end
    function p:ended(a,b,c,d,tracked,animated)
        if not a then return end
        self.samples=self.samples+1;self.prepare=self.prepare+(b-a);self.world_time=self.world_time+(c-b);self.after=self.after+(d-c)
        self.prepare_max=math.max(self.prepare_max,b-a);self.world_max=math.max(self.world_max,c-b)
        self.tracked=self.tracked+tracked;self.animated=self.animated+animated
        self.tracked_max=math.max(self.tracked_max,tracked);self.animated_max=math.max(self.animated_max,animated)
    end
    function p:stop(reason)
        if self.stopped then return end
        if self.intervals>0 or self.samples>0 then self:report(reason or "cleanup")end
        self.stopped=true;self.sampling=false;self.last_frame=nil
    end
    p:reset();return p
end
return P
