"""Compare native multiplier hooks with the supplied SoloModifier reference.

Native slot setup and sub-zone iteration execute the game's actual Lua methods.
Rendering, navigation and spawning are boundaries, not a full game simulation.
"""
from pathlib import Path
import re
from project_env import SOURCES, GAME, FIXTURES
from lupa.luajit21 import LuaRuntime

def method(path, owner, name):
    text=(GAME/path).read_text(encoding='utf-8-sig')
    start=text.index(owner+'.'+name+' = function')
    end=text.index('\nend',start)+len('\nend')
    return text[start:end]

for stripped in (False,True):
    L=LuaRuntime(unpack_returned_tuples=True)
    def load(path):
        text=(SOURCES/(path+'.lua')).read_text(encoding='utf-8-sig')
        if stripped: text=re.sub(r'(?m)^\s*-- PERF_DEBUG_BEGIN\n.*?^\s*-- PERF_DEBUG_END\n?', '', text, flags=re.S)
        return L.execute(text,name='@'+path)
    L.globals().load_module=load
    L.execute('''
mods={};hooks={};classes={};host=true;advanced=false
Managers={state={game_session={is_server=function() return host end},
    difficulty={get_table_entry_by_challenge=function(_,v) return v[2] end}}}
Script={new_array=function() return {} end}
local names={pacing_manager="PacingManager",roamer_pacing="RoamerPacing",
    specials_pacing="SpecialsPacing",horde_pacing="HordePacing",mutator_modify_havoc="MutatorModifyHavoc"}
function require(path)
    local key=path:match("([^/]+)$");key=names[key] or key
    classes[key]=classes[key] or {name=key};return classes[key]
end
function new_mod(name)
    local m={values={}};mods[name]=m;hooks[name]={}
    function m:io_dofile(path) return load_module(path) end
    function m:get(key) return self.values[key] end
    function m.has_local_gameplay_authority() return host end
    function m:hook(target,name,fn)
        local key=(type(target)=="table" and target.name or target).."."..name
        assert(not hooks[self.name][key],key)
        hooks[self.name][key]={fn=fn}
    end
    function m:hook_safe(target,name,fn)
        self:hook(target,name,fn)
        hooks[self.name][target.name.."."..name].safe=true
    end
    m.name=name;return m
end
function get_mod(name) return mods[name] end
new_mod("HavocConditionManager");new_mod("SoloModifier")
mods.HavocEnemyDirector={is_active=function() return advanced end}
function pack(...) return {n=select("#",...),...} end
function invoke(owner,key,original,...)
    local hook=hooks[owner][key]
    if not hook then return original(...) end
    if hook.safe then local r=pack(original(...));hook.fn(...);return unpack(r,1,r.n) end
    return hook.fn(original,...)
end
B=mods.HavocConditionManager
''')
    load('HavocConditionManager/scripts/mods/HavocConditionManager/native_spawn')
    L.execute((FIXTURES/'solomodifier_native_spawn.lua').read_text(encoding='utf-8-sig'))
    L.globals().NativeScaling=load('HavocConditionManager/scripts/mods/HavocConditionManager/native_scaling')
    L.execute('SpecialsPacing={};RoamerPacing={}')
    for name in ('_setup','set_max_alive_specials_multiplier'):
        L.execute(method('scripts/managers/pacing/specials_pacing/specials_pacing.lua','SpecialsPacing',name))
    L.execute(method('scripts/managers/pacing/roamer_pacing/roamer_pacing.lua','RoamerPacing','_create_sub_zones'))
    L.execute('''
local keys={"challenge_rating_multiplier","alive_specials_multiplier","roamer_spawn_multiplier","ramp_horde_multiplier","coordinated_strike_multiplier"}
local function configure(n)
    B.reset_native_spawn_scaling()
    for _,name in ipairs({"HavocConditionManager","SoloModifier"}) do
        local m=mods[name]
        for _,key in ipairs(keys) do m.values[key]=key=="coordinated_strike_multiplier" and math.ceil(n) or n end
        m.values.high_density_type=false
    end
end
local function fixture(owner,n)
    local out={}
    local function call(key,fn,...) return invoke(owner,key,fn,...) end
    -- Execute actual native setup: multiplier scales the base, never the additive bonus.
    local sp=setmetatable({_template={max_alive_specials=6,first_spawn_timer_modifer=0.7},
        _max_alive_specials_bonus=2,_timer_modifier=1},{__index=SpecialsPacing})
    local draws=0
    sp._setup_specials_slot=function(self,slots,slot,template,timer)
        draws=draws+1;slot.breed_name=draws%2==0 and "netter" or "mutant"
        slot.spawn_timer=draws*timer;slot.index=#slots+1
    end
    call("SpecialsPacing.set_max_alive_specials_multiplier",SpecialsPacing.set_max_alive_specials_multiplier,sp,{1,2})
    assert(sp._max_alive_specials==math.ceil(6*2*n+2))
    assert(#sp._specials_slots==sp._max_alive_specials and draws==sp._max_alive_specials)
    for i,s in ipairs(sp._specials_slots) do assert(s.index==i and s.spawn_timer==i*0.7) end
    out.slots=#sp._specials_slots
    -- Native placement settings remain unmodified; both hooks expand the slot request.
    local original_settings={num_slots=4,position_offset=2,sentinel="keep"}
    local function placement(_,_,settings)
        local slots={}
        for i=1,settings.num_slots do slots[i]={index=i} end
        return slots,settings.num_slots
    end
    local placed,number=call("roamer_slot_placement_functions.circle_placement",placement,nil,nil,original_settings)
    assert(number==math.ceil(4*n) and #placed==number and original_settings.num_slots==4)
    out.placement=number
    -- Run the actual native sub-zone early-stop loop with the hooked placement.
    local rp=setmetatable({_random=function(_,a) return a end},{__index=RoamerPacing})
    rp._create_sub_zone_location=function(self,pos,density,group)
        return call("roamer_slot_placement_functions.circle_placement",placement,nil,pos,original_settings)
    end
    local sub,slots=call("RoamerPacing._create_sub_zones",RoamerPacing._create_sub_zones,rp,{{1},{2},{3}},
        {try_fill_one_sub_zone=true},10,4)
    assert(#sub==1 and slots==math.ceil(4*n),"Sub-zone target and slot expansion must agree")
    out.subzones=#sub;out.subslots=slots
    local zones=call("RoamerPacing._create_zones",function() return {{num_to_spawn=7},{num_to_spawn=2.5}} end,{},{})
    assert(zones[1].num_to_spawn==7*n and zones[2].num_to_spawn==2.5*n)
    out.zone=zones[1].num_to_spawn
    local pm={}
    call("PacingManager.on_gameplay_post_init",function(self)
        self._challenge_rating_thresholds={hordes=5,specials=7.5,monsters=0}
    end,pm)
    assert(pm._challenge_rating_thresholds.specials==math.ceil(7.5*n))
    out.threshold=pm._challenge_rating_thresholds.specials
    out.ramp=call("PacingManager.get_ramp_up_frequency_modifier",function() return 1.25 end,pm,"hordes")
    assert(out.ramp==math.ceil(1.25*n))
    assert(call("PacingManager.get_ramp_up_frequency_modifier",function() return 1.25 end,pm,"trickle_hordes")==out.ramp)
    assert(call("PacingManager.get_ramp_up_frequency_modifier",function() return 1.25 end,pm,"specials")==1.25)
    out.density=call("PacingManager.current_density_type",function() return "low" end,pm)
    local hp={}
    local template={coordinated_horde_strike_settings={a={total_num_allowed=2},unlimited={}}}
    call("HordePacing._init_coordinated_horde_strikes",function(self) self._coordinated_horde_strikes_total_num_allowed={a=3} end,hp,template)
    out.quota=hp._coordinated_horde_strikes_total_num_allowed.a
    assert(out.quota==3*math.ceil(n))
    for success_at=1,6 do
        local attempts=0
        local result=call("HordePacing._evaluate_coordinated_horde_strike",function(self,side)
            assert(side==1);attempts=attempts+1;return attempts==success_at
        end,hp,1)
        assert(attempts==math.min(success_at,math.ceil(n)))
        assert(result==(success_at<=math.ceil(n)))
    end
    return out
end
for _,n in ipairs({1,1.1,1.5,2,2.7,3,4,5}) do
    configure(n)
    local a,b=fixture("HavocConditionManager",n),fixture("SoloModifier",n)
    for k,v in pairs(a) do assert(v==b[k],k) end
end
-- Native mode cannot resurrect the legacy copy/timer hooks at any old setting.
for _,category in ipairs({"common","elite","special","boss"}) do
    B.values["spawn_multiplier_"..category]=5;B.values["spawn_mode_"..category]="mixed"
end
for key in pairs(hooks.HavocConditionManager) do
    assert(not key:find("spawn_minion",1,true) and not key:find("unregister_unit",1,true))
    assert(not key:find("_spawn_special",1,true) and not key:find("_update_timer",1,true))
    assert(not key:find("add_trickle_horde",1,true))
end
assert(B.scale_native_horde==nil and B.scale_native_special_slot==nil)
-- All pressure steps, including values beyond the other controls' upper bound.
for step=10,150 do
    B.reset_native_spawn_scaling();B.values.challenge_rating_multiplier=step/10
    local pm={_challenge_rating_thresholds={hordes=5}}
    invoke("HavocConditionManager","PacingManager.on_gameplay_post_init",function() end,pm)
    assert(pm._challenge_rating_thresholds.hordes==math.ceil(5*step/10))
end
-- A mission uses one snapshot, even when saved values change during the run.
configure(2);B.values.high_density_type=true
local function ramp() return invoke("HavocConditionManager","PacingManager.get_ramp_up_frequency_modifier",function() return 1.25 end,{},"hordes") end
assert(ramp()==3)
B.values.ramp_horde_multiplier=5;B.values.high_density_type=false
assert(ramp()==3)
assert(invoke("HavocConditionManager","PacingManager.current_density_type",function() return "low" end,{})=="high")
B.reset_native_spawn_scaling();assert(ramp()==7)
assert(invoke("HavocConditionManager","PacingManager.current_density_type",function() return "low" end,{})=="low")
B.values.ramp_horde_multiplier=2
Managers.state.game_session={is_server=function() return host end};assert(ramp()==3)
-- Only local authority gates HCM; an old HED does not own its new multipliers.
for _,gate in ipairs({"client"}) do
    configure(5);host=gate~="client";advanced=gate=="advanced"
    local saved=B.get;B.get=function() error("Inactive native mode read settings") end
    local input={1,2}
    assert(invoke("HavocConditionManager","SpecialsPacing.set_max_alive_specials_multiplier",function(_,v) return v end,{},input)==input)
    local zone=invoke("HavocConditionManager","RoamerPacing._create_zones",function() return {{num_to_spawn=7}} end,{},{})
    assert(zone[1].num_to_spawn==7 and ramp()==1.25)
    local count=0
    assert(not invoke("HavocConditionManager","HordePacing._evaluate_coordinated_horde_strike",function() count=count+1;return false end,{},1))
    assert(count==1);B.get=saved
end
host=true;advanced=true
configure(2);assert(ramp()==3,"HCM native configuration must not yield to legacy HED")
advanced=false
-- Every numerical input is finite, bounded and normalized to the advertised step.
for _,c in ipairs(NativeScaling.controls) do
    assert(NativeScaling.normalize(nil,c)==1 and NativeScaling.normalize(0/0,c)==1)
    assert(NativeScaling.normalize(-10,c)==1 and NativeScaling.normalize(math.huge,c)==c.max)
    assert(NativeScaling.normalize(1.56,c)==(c.step==1 and 2 or 1.6))
end
-- Template restoration is preserved independently of HED's spawn ownership.
advanced=true
local restored
Managers.state.game_mode={game_mode=function() return {extension=function()
    return {init_horde_buff=function(_,data) restored=data end}
end} end}
local data={probability=0.1}
invoke("HavocConditionManager","MutatorModifyHavoc.init",function() end,{_is_server=true,_template={init_modify_horde=data}})
assert(restored==data)
''')
    print(('Stripped' if stripped else 'Diagnostic')+' native migration: 8 SoloModifier equivalence cases, actual native slot/sub-zone setup, 141 pressure steps, ownership, lifecycle, retries, no copies/timer rewrites: PASS')
