"""Compare the released animation policy with the quiet path on identical crowds.

Owned Lua facades measure wrapper work and redundant extension reads, not FPS.
Native memory checks/detours are separately exercised by the native suite.
"""
from project_env import PROJECT, CHECKS
from lupa.luajit21 import LuaRuntime
import json

package=PROJECT/'custom-packages/template-library/starter-conditions-frenzied_assault'
manifest=json.loads((package/'package.json').read_text(encoding='utf-8'))
assert 'lua/profile.lua' not in manifest['files'] and not (package/'lua/profile.lua').exists()
L=LuaRuntime(unpack_returned_tuples=True)
L.globals().old_source=(PROJECT/'tests/fixtures/frenzied_animation_1_7_3.lua').read_text(encoding='utf-8')
L.globals().new_source=(package/'lua/animation.lua').read_text(encoding='utf-8')
L.execute(r'''
local ffi=require('ffi')
ffi.cdef[[int QueryPerformanceCounter(int64_t *); int QueryPerformanceFrequency(int64_t *);]]
local kernel=ffi.load('kernel32');local value,freq=ffi.new('int64_t[1]'),ffi.new('int64_t[1]')
assert(kernel.QueryPerformanceFrequency(freq)~=0)
local function now()kernel.QueryPerformanceCounter(value);return tonumber(value[0])/tonumber(freq[0])end
table.clear=function(t)for k in pairs(t)do t[k]=nil end end
ALIVE=setmetatable({},{__index=function(_,u)return u.alive~=false end})
World={get_data=function(w,k)return w[k]end}
Unit={has_animation_state_machine=function(u)return u.machine~=false end}
local reads,binds,observations,logs=0,0,0,0
local native={rates={},traced=false,active=false}
function native.available()native.traced=false;return true end
function native.begin()native.active=false;table.clear(native.rates)end
function native.bind(u,rate,record)binds=binds+1;native.rates[u]=rate;return record end
function native.commit()native.active=true end
function native.finish()native.active=false end
function native.observed()observations=observations+1;return true end
function native.complete_trace()native.traced=true end
function native.cleanup()native.active=false end
local env=setmetatable({require=function(name)
    if name=='./native_timestep.lua' then return native end
    assert(name=='./native_clock.lua');return {}
end},{__index=_G})
local old=setfenv(assert(loadstring(old_source)),env)()
local new=setfenv(assert(loadstring(new_source)),env)()
ScriptUnit={has_extension=function(u,name)
    if name=='unit_data_system' then reads=reads+1;return u.data end
    if name=='first_person_system' then return u.first_person end
end}
results={}
for _,count in ipairs({100,200,400})do
    local players,units={},{}
    for i=1,4 do
        local p={disabled={},fp={}}
        p.data={breed=function()return {breed_type='player'}end,read_component=function()return p.disabled end}
        p.first_person={first_person_unit=function()return p.fp end};players[i]=p
    end
    for i=1,count do units[i]={target=players[(i-1)%4+1]}end
    for i=1,4 do players[i].disabled.disabling_unit=units[i]end
    for _,spec in ipairs({{old,'1.7.3'},{new,'1.7.4'}})do
        local animation,label=spec[1],spec[2]
        local current={world={active=true},moves={},animation_rate=function()return 1.4 end,log=function()logs=logs+1 end}
        for _,u in ipairs(units)do
            current.moves[u]={brain={_breed={name='synthetic'},_running_leaf_node={tree_node={'BtMeleeAttackAction'}},
                _scratchpad={perception_component={target_unit=u.target}}}}
        end
        assert(animation.available());reads,binds,observations,logs=0,0,0,0
        local function pass()
            local prepared=animation.before(current,current.world,1/60)
            assert(prepared and native.active)
            animation.after(prepared,current);assert(not native.active)
        end
        pass()
        assert(reads==(label=='1.7.4' and 4 or count) and binds==count+8)
        if label=='1.7.4' then assert(logs==0 and observations==0 and native.traced and not current.animation_snapshots)end
        -- Ownership changes at the next frame cannot inherit the old cache.
        players[1].disabled.disabling_unit=nil;pass()
        assert(native.rates[players[1]]==nil and native.rates[players[1].fp]==nil)
        players[1].disabled.disabling_unit=units[5];pass()
        assert(native.rates[players[1]]==1.4 and native.rates[players[1].fp]==1.4)
        players[1].disabled.disabling_unit=units[1]
        for i=1,50 do pass()end
        collectgarbage('collect');reads,binds,observations,logs=0,0,0,0
        local frames=500;local start=now()
        for i=1,frames do pass()end
        local ms=(now()-start)*1000/frames
        assert(reads==frames*(label=='1.7.4' and 4 or count))
        assert(binds==frames*(count+8) and logs==0 and observations==0)
        results[#results+1]={version=label,units=count,player_state_reads_per_frame=reads/frames,owner_binds_per_frame=binds/frames,wrapper_ms_per_frame=ms}
        animation.cleanup()
    end
end
''')
rows=[dict(row.items()) for _,row in L.globals().results.items()]
(CHECKS/'frenzied-quiet-performance.json').write_text(json.dumps({
    'scope':'Identical synthetic Lua crowds and four targets; animation policy only, not native guard/engine time or game FPS.',
    'results':rows},indent=2)+'\n',encoding='utf-8')
for index in range(0,len(rows),2):
    old,new=rows[index:index+2]
    print(f"PASS quiet animation: {new['units']} units, target reads {old['player_state_reads_per_frame']} -> {new['player_state_reads_per_frame']}; "
          f"wrapper {old['wrapper_ms_per_frame']:.3f} -> {new['wrapper_ms_per_frame']:.3f} ms/pass (synthetic); identical bindings, fresh ownership, zero normal logs/trace reads.")
