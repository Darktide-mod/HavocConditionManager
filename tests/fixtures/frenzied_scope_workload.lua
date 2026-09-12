-- Identical synthetic crowds through the real released/current policy,
-- loader, native AI update and ScriptWorld entry. Native binding is a facade;
-- count avoided work here rather than claiming an in-game FPS measurement.
local ffi=real_ffi
if not pcall(ffi.typeof,'HCMFrenzyWorkloadCounter') then ffi.cdef[[
typedef int64_t HCMFrenzyWorkloadCounter;
int QueryPerformanceCounter(int64_t *); int QueryPerformanceFrequency(int64_t *);
]]end
local kernel=ffi.load('kernel32');local clock,frequency=ffi.new('int64_t[1]'),ffi.new('int64_t[1]')
assert(kernel.QueryPerformanceFrequency(frequency)~=0)
local function now()kernel.QueryPerformanceCounter(clock);return tonumber(clock[0])/tonumber(frequency[0])end
scope_workload_results={}
for _,scenario in ipairs({'mixed','native_only'})do
    for _,spec in ipairs({{previous_release_files,'1.7.4'},{shipped_package_files,'1.8.0'}})do
        engine=start(spec[1]);local current=mod._diy_frenzied_assault_hooks_v1.current
        animation_units={};local brains={};local count=400
        for i=1,count do
            local special=scenario=='mixed' and i>390
            local melee=scenario=='mixed' and i>360 and i<=390
            local firearm=i<=80
            local unit,breed=unit('minion',special)
            local name=firearm and 'BtShootAction' or melee and 'BtMeleeAttackAction' or 'BtMeleeFollowTargetAction'
            local data=melee and base_data or {aim_duration=1,attack_anim_duration=1}
            local node={identifier=name,tree_node={name,action_data=data},children=function()return {}end,leave=function()end}
            function node:enter(u,b,bb,pad)pad.behavior_component={move_state='moving'}end
            function node:run()return 'running',false end
            local ai=brain(unit,breed);ai._behavior_tree={root=function()return node end}
            ai:update(unit,1/60,0);brains[i]=ai
            unit.anim={times={0},states={1},ids={1},layers=1};animation_units[i]=unit
        end
        local world=modules['scripts/foundation/utilities/script_world']
        for i=1,15 do world.update(level_world,1/60)end
        native_dt.begin_calls=0;native_dt.bind_calls=0
        local swaps=0
        for _,ai in ipairs(brains)do swaps=swaps+#current.trees[ai._behavior_tree]end
        collectgarbage('collect');local start=now();local frames=100
        for frame=1,frames do
            for i,ai in ipairs(brains)do ai:update(animation_units[i],1/60,frame/60)end
            world.update(level_world,1/60)
        end
        local elapsed=(now()-start)*1000/frames
        local expected=spec[2]=='1.7.4' and 400 or scenario=='mixed' and 40 or 0
        assert(native_dt.bind_calls==frames*expected)
        assert(native_dt.begin_calls==(expected==0 and 0 or frames))
        if spec[2]=='1.8.0' then assert(swaps==(scenario=='mixed' and 30 or 0))end
        scope_workload_results[#scope_workload_results+1]={scenario=scenario,version=spec[2],units=count,
            binds_per_frame=native_dt.bind_calls/frames,preparations_per_frame=native_dt.begin_calls/frames,
            swapped_nodes_per_ai_pass=swaps,facade_frame_ms=elapsed}
        engine.finish();assert(not native_dt.enabled);animation_units={}
    end
end
