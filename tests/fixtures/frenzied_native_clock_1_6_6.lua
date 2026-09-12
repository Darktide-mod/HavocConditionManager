-- In-place AnimationInstance seek, verified against the 1.12.5 Windows image.
-- No patching, guessed crossfade handles, pending restore or layer rebuilding.
-- Build and pointer checks fail closed; an engine update needs a new audit.
local M={}
local signatures={
    {0x5a2460,"48895c24084889742410574883ec20488b41580f57c0448bc2488bf14a8b3cc04b8d1c8048c1e304480399e81200000f2fd00f86b80000008b13f30f5ad2f20f115308488b4940e884bd06008b13488b4e40e889c406004885c0740ac780d805000002000000f20f104b08448b43148b97a8000000660f5ac9f30f5e4b20443bc273330f1f4000660f1f840000000000418bc0488d0c40488b87b00000000f2f0c88721241ffc0448943148b97a8000000443bc272da8b4b183bca73330f1f008bc1488d1440488b87b0000000837c900804750ff30f104304f30f5c04900f2fc8720dffc1894b183b8fa800000072d0488b5c2430488b7424384883c4205fc3"},
    {0x5390f7,"488bc8c1e90281f9ffff0100741f8bc1c1e91125ffff010048c1e00448030546d1db00390875064c8b7008eb034d8bf7"},
    {0x53926b,"4d8b8e68020000498b4130448b7008"},
    {0x60e230,"40534883ec20488bd9e8020700004c8bc04885c0744c4533c94439482476439048"},
}
local function finite(n)return type(n)=="number" and n==n and math.abs(n)<1e9 end

-- The constructor also accepts an isolated memory reader/call adapter for
-- regression tests. Production always supplies VirtualQuery and the image.
function M.create(ffi,base,readable,call,reset_reader)
    local byte=ffi.typeof("uint8_t *")
    local uint32,uint16=ffi.typeof("uint32_t *"),ffi.typeof("uint16_t *")
    local float,double=ffi.typeof("float *"),ffi.typeof("double *")
    local address=ffi.typeof("uintptr_t *")
    local carrier,low32=ffi.typeof("uintptr_t"),ffi.typeof("uint32_t")
    local scalar_float=ffi.typeof("float")
    local function ptr(p)return ffi.cast(byte,p)end
    base=ptr(base)
    local function u32(p,o)return tonumber(ffi.cast(uint32,p+o)[0])end
    local function f32(p,o)return tonumber(ffi.cast(float,p+o)[0])end
    local function f64(p,o)return tonumber(ffi.cast(double,p+o)[0])end
    local function pointer(p,o)return ptr(ffi.cast(address,p+o)[0])end
    local function encode(unit)return tonumber(ffi.cast(low32,ffi.cast(carrier,unit)))end
    if not readable(base,0x40) or u32(base,0)%0x10000~=0x5a4d then return nil,"invalid executable image" end
    local pe=u32(base,0x3c)
    if pe>0x1000 or not readable(base+pe,0x90) or u32(base,pe)~=0x4550
        or u32(base,pe+8)~=1786450566 or u32(base,pe+0x50)~=41992192
        or tonumber(ffi.cast(uint16,base+pe+0x18)[0])~=0x20b then
        return nil,"unsupported game executable; expected audited 1.12.5 build"
    end
    for _,spec in ipairs(signatures)do
        local expected=spec[2]:gsub("..",function(h)return string.char(tonumber(h,16))end)
        if not readable(base+spec[1],#expected) or ffi.string(base+spec[1],#expected)~=expected then
            return nil,string.format("engine signature mismatch at RVA %x",spec[1])
        end
    end
    if not readable(base+0x12f6260,8) then return nil,"unit registry unavailable" end
    local seek=call or ffi.cast("void (*)(void *, uint32_t, float)",base+0x5a2460)
    local clock={}
    local epoch,active=0,false
    function clock.begin_frame()
        epoch=epoch+1;active=true
        if reset_reader then reset_reader(true)end
    end
    function clock.end_frame()
        active=false;epoch=epoch+1
        if reset_reader then reset_reader(false)end
    end
    -- Prepared pointers only live inside the synchronous pre-world pass.
    -- Re-resolve the handle, generation and complete layout for every unit
    -- on every pass; no engine pointer is trusted across World.update.
    function clock.prepare(unit,count,context)
        if context then context.epoch=nil end
        if not active then return nil,"clock pass inactive" end
        if type(count)~="number" or count%1~=0 or count<1 or count>32 then return nil,"invalid clock request" end
        if type(unit)~="userdata" and type(unit)~="cdata" then return nil,"invalid unit reference" end
        -- Match the audited getter's `mov rcx,rax; shr ecx,2`: the handle
        -- is the LOW 32 bits, with two tag bits removed. Lua lightuserdata
        -- need not be a zero-tag, 32-bit address. Keep the full pointer as
        -- cdata until truncation so a high-word tag cannot lose precision.
        -- Unit's public getters have already validated this argument.
        local ok,encoded=pcall(encode,unit)
        if not ok then return nil,"unit reference conversion failed: "..tostring(encoded) end
        local ref=math.floor(encoded/4)
        local index=ref%0x20000
        if index==0x1ffff then return nil,"invalid unit index" end
        local registry=pointer(base,0x12f6260)
        local entry=registry+index*16
        if not readable(registry,16) or not readable(entry,16) or u32(entry,0)~=math.floor(ref/0x20000) then
            return nil,"expired unit generation"
        end
        local object=pointer(entry,8)
        if not readable(object,0x270) then return nil,"unit unavailable" end
        local instance=pointer(object,0x268)
        if not readable(instance,0x12f0) then return nil,"animation instance unavailable" end
        local resource=pointer(instance,0x30)
        local states,layers,blender=pointer(instance,0x58),pointer(instance,0x12e8),pointer(instance,0x40)
        if not readable(resource,12) or u32(resource,8)~=count or not readable(states,count*8)
            or not readable(layers,count*0x50) or not readable(blender,0x20) then return nil,"animation layout mismatch" end
        context=context or {}
        context.instance,context.resource,context.states,context.layers=instance,resource,states,layers
        context.count,context.epoch=count,epoch
        return context
    end
    function clock.advance_prepared(context,layer,before,target)
        if not active or context.epoch~=epoch then return nil,"expired clock pass" end
        local count=context.count
        if not finite(before) or not finite(target) or target<=before or target<=0
            or type(layer)~="number" or layer%1~=0 or layer<1 or layer>count then return nil,"invalid clock request" end
        local instance,resource,states,layers=context.instance,context.resource,context.states,context.layers
        local state=pointer(states,(layer-1)*8)
        local live=layers+(layer-1)*0x50
        -- Empty auxiliary layers are normal and may become active without
        -- changing the public clip id. Do not quarantine them as failures.
        if u32(live,0)==0xffffffff then return false,"inactive layer" end
        if not readable(state,0xb8) then return nil,"animation state unavailable" end
        local now=f64(live,8)
        if not finite(now) or math.abs(now-before)>.0001 then return nil,"live clock mismatch" end
        local divisor,duration=f32(live,0x20),f32(live,4)
        if not finite(divisor) or divisor<=0 or not finite(duration) or duration<=0 then return false,"inactive layer" end
        local events=u32(state,0xa8)
        local list=pointer(state,0xb0)
        if events>4096 or events>0 and not readable(list,events*12) then return nil,"event layout mismatch" end
        local first,last=u32(live,0x14),u32(live,0x18)
        if first>events or last>events then return nil,"event cursor mismatch" end
        -- Leave the next authored event and clip end for normal evaluation.
        -- Seeking past those cursors would silently omit animation events.
        local limit=duration*divisor
        if first<events then limit=math.min(limit,f32(list,first*12)*divisor)end
        for i=last,events-1 do
            if u32(list,i*12+8)==4 then
                limit=math.min(limit,(duration-f32(list,i*12))*divisor);break
            end
        end
        if not finite(limit) then return nil,"invalid event time" end
        target=tonumber(ffi.cast(scalar_float,math.min(target,limit-.0001)))
        if target<=before then return false,"native boundary" end
        -- Existing root blend and all of its child clips retain their handles,
        -- weights and outgoing transitions; the engine seeks those players.
        seek(instance,layer-1,target)
        if pointer(states,(layer-1)*8)~=state or u32(resource,8)~=count
            or math.abs(f64(live,8)-target)>.0001 then return nil,"seek readback mismatch" end
        return target
    end
    -- Standalone entry for contract tests; production prepares once per unit.
    function clock.advance(unit,layer,before,target,count)
        if not finite(before) or not finite(target) or target<=before or target<=0
            or type(count)~="number" or count%1~=0 or count<1 or count>32
            or type(layer)~="number" or layer%1~=0 or layer<1 or layer>count then return nil,"invalid clock request" end
        clock.begin_frame()
        local context,why=clock.prepare(unit,count)
        local value
        if context then value,why=clock.advance_prepared(context,layer,before,target)end
        clock.end_frame()
        return value,why
    end
    return clock
end

-- Cache OS memory-region permissions only during one synchronous seek pass.
-- Live values (generation, pointers, counts, clocks and event cursors) are
-- still read each time. Clear before returning to any native world update.
function M.memory_reader(ffi,query,info)
    local uintptr=ffi.typeof("uintptr_t")
    local ends={}
    local caching,last_start,last_end=false,0,0
    local function reset(enabled)
        for page in pairs(ends)do ends[page]=nil end
        caching=enabled;last_start,last_end=0,0
    end
    local function readable(address,size)
        local n=tonumber(ffi.cast(uintptr,address))
        if n<0x10000 or size<0 or n+size>=0x800000000000 then return false end
        local page=math.floor(n/4096)
        if caching then
            if n>=last_start and n+size<=last_end then return true end
            if ends[page] and n+size<=ends[page] then return true end
        end
        if query(address,info,48)~=48 then return false end
        local p=tonumber(info[0].protect)
        local access=p%0x100
        local start=tonumber(ffi.cast(uintptr,info[0].base))
        local finish=start+tonumber(info[0].size)
        local valid=info[0].state==0x1000 and p%0x200<0x100
            and (access==2 or access==4 or access==8 or access==0x20 or access==0x40 or access==0x80)
            and n>=start and n+size<=finish
        if valid and caching then
            last_start,last_end=start,finish
            if start<=page*4096 then ends[page]=finish end
        end
        return valid
    end
    return readable,reset
end

local instance,reason,attempted
function M.available()
    if attempted then return instance~=nil,reason end
    attempted=true
    local ok,result,why=pcall(function()
        local ffi=Mods and Mods.lua and Mods.lua.ffi or require("ffi")
        if not ffi or ffi.os~="Windows" or not ffi.abi("64bit") then return nil,"Windows x64 LuaJIT FFI required" end
        if not pcall(ffi.typeof,"HCMFrenzyMemoryInfo164") then
            ffi.cdef[[
                typedef struct { void *base; void *allocation; uint32_t allocation_protect;
                    uint16_t partition; uint16_t padding; size_t size; uint32_t state;
                    uint32_t protect; uint32_t type; uint32_t tail; } HCMFrenzyMemoryInfo164;
                void *GetModuleHandleA(const char *name);
                size_t VirtualQuery(const void *address, void *buffer, size_t length);
            ]]
        end
        local kernel=ffi.load("kernel32")
        local info=ffi.new("HCMFrenzyMemoryInfo164[1]")
        assert(ffi.sizeof(info)==48,"unexpected memory-info layout")
        local readable,reset=M.memory_reader(ffi,kernel.VirtualQuery,info)
        return M.create(ffi,kernel.GetModuleHandleA(nil),readable,nil,reset)
    end)
    if ok then instance,reason=result,why else reason=tostring(result)end
    return instance~=nil,reason
end
function M.advance(...)
    if not instance then return nil,reason or "native clock unavailable" end
    return instance.advance(...)
end
function M.begin_frame()if instance then instance.begin_frame()end end
function M.end_frame()if instance then instance.end_frame()end end
function M.prepare(...)
    if not instance then return nil,reason or "native clock unavailable" end
    return instance.prepare(...)
end
function M.advance_prepared(...)return instance.advance_prepared(...)end
return M
