"""Regressions from the 3.6.2 log, with actual target and buff callbacks."""
import subprocess
import native_recycling_harness as h
from native_harness import *

def source(path):
    dest=game/path
    if not dest.exists():
        dest.parent.mkdir(parents=True,exist_ok=True)
        dest.write_bytes(subprocess.check_output(['git','show','HEAD:'+path],cwd=game))
    return dest.read_text(encoding='utf-8-sig')

L.execute('''
selector_deps={}
selector_deps["scripts/utilities/breed"]={is_player=function() return false end}
selector_deps["scripts/utilities/minion_movement"]={target_speed_away=function() return 0 end}
selector_deps["scripts/utilities/minion_target_override"]={check_for_target_overrides=function(u,t) return t end}
selector_deps["scripts/settings/perception/perception_settings"]={aggro_states={aggroed="aggroed"}}
local weights={detection_radius=function() return 20 end,distance_weight=function() return 0,1 end,weight_multiplier=function() return 1 end}
for _,name in ipairs({"occupied_slots_weight","threat_weight","disabled_weight","targeted_by_monster_weight","stickiness_weight"}) do weights[name]=function() return 0 end end
selector_deps["scripts/utilities/minion_target_selection"]=weights
''')
selector=L.execute('local require=function(p) return selector_deps[p] end\n'+source('scripts/extension_systems/perception/target_selection_templates/melee_elite_target_selection_template.lua'))
L.globals().actual_selector=selector.melee_elite
L.execute('''
for _,distance in ipairs({100,200}) do
 for _,existing in ipairs({false,true}) do
  setup();local unit,record,ext=roaming("renegade_executor")
  for i,player in ipairs(players) do POSITION_LOOKUP[player]=vec(distance+i-1) end
  local player=players[1];player.extensions={unit_data_system={breed=function() return {} end}}
  local targets={player};targets[player]=true
  local buffs={owner_of_buff_with_id=function() return nil end}
  ext._perception_component.aggro_state="aggroed"
  ext._perception_component.target_unit=existing and player or nil
  function ext:_update_target_selection()
   return actual_selector(unit,enemy_side,self._perception_component,buffs,{target_selection_weights={}},targets,{},now,{},false)
  end
  tick(0);assert(ext._perception_component.target_unit==player and not ext._perception_component.has_line_of_sight)
  run(1,35);assert(#deleted==1,"real native distant target blocked retirement")
 end
end
for _,case in ipairs({"rotten_armor","havoc_gardens_embrace","stimmed","healed","injured","stim_record"}) do
 setup();local unit,record=roaming("renegade_executor")
 if case=="healed" then unit.damaged_by=players[1];unit.health=1
 elseif case=="injured" then unit.health=.6
 elseif case=="stim_record" then record.stim_buff_name="havoc_stimmed"
 else unit.keywords[case]=true end
 run(0,35);assert(#deleted==1,case)
end
for _,case in ipairs({"one_rotten","all_garden"}) do
 patrol_setup();local group=boss_patrol(12)
 for i,u in ipairs(group.members) do
  if case=="all_garden" then u.keywords.havoc_gardens_embrace=true
  elseif i==12 then u.keywords.rotten_armor=true end
 end
 run(0,110);assert(#deleted==12,case)
end
setup();roaming("renegade_executor");sensor._num_update_units=240
run(0,35);assert(#deleted==1,"unrelated perception population delayed the quiet interval")
for _,case in ipairs({"slow_position","slow_path"}) do
 setup();local unit=roaming("renegade_executor")
 if case=="slow_path" then
  unit.following=true
  unit.extensions.navigation_system.remaining_distance_from_progress_to_end_of_path=function() return 300-now*.2 end
 end
 for t=0,90 do
  POSITION_LOOKUP[unit]=case=="slow_position" and vec(t*.2) or vec(0,t*.2)
  tick(t)
 end
 assert(#deleted==1,"movement retained an out-of-contact unit forever: "..case)
end
print("Native melee-elite target selection at 100/200m; constant modifiers, old/healed injuries, 12-member modifier patrols and unrelated population 240: eligible entities actually retired: PASS")
''')

# Keep both the native death payload and template stop callback unchanged.
havoc=source('scripts/settings/buff/havoc_buff_templates.lua')
start=havoc.index('local function _on_rotten_armor_death(')
death=havoc[start:havoc.index('\nend',start)+4]
start=havoc.index('\tstop_func = function',havoc.index('templates.mutator_rotten_armor ='))
stop=havoc[start:havoc.index('\n\tend,',start)+7]
L.execute('''
Vector3.down=function() return vec(0,0,-1) end
setmetatable(Vector3,{__call=function(_,...) return vec(...) end})
Unit={local_rotation=function() return vec(0) end}
local rotten_armor_data={vfx_name="rotten",sfx_death_name="rotten"}
local _position=function(u) return POSITION_LOOKUP[u] end
LiquidAreaTemplates={rotten_armor={}}
LiquidArea={try_create=function() liquids=liquids+1 end}
'''+death+'\nrequire("scripts/settings/buff/buff_templates").mutator_rotten_armor={'+stop+'\n}')
load_mod('HavocConditionManager/scripts/mods/HavocConditionManager/retirement_effects')
buff=source('scripts/extension_systems/buff/buffs/buff.lua')
start=buff.index('Buff.destroy = function')
L.execute('NativeBuff={};local Buff=NativeBuff;'+buff[start:buff.index('\nend',start)+4])
L.execute('''
local template=require("scripts/settings/buff/buff_templates").mutator_rotten_armor
local native_stop=template.stop_func
for _,h in ipairs(hooks) do if h.target==template and h.name=="stop_func" then
 local wrapper=h.fn;template.stop_func=function(...) return wrapper(native_stop,...) end
end end
local function effects_setup()
 setup();liquids=0;vfx=0;sfx=0;other_cleanup=0
 local get_system=Managers.state.extension.system
 Managers.state.extension.system=function(self,name)
  if name=="fx_system" then return {trigger_vfx=function() vfx=vfx+1 end,trigger_wwise_event=function() sfx=sfx+1 end} end
  return get_system(self,name)
 end
end
local function destroy(unit,other)
 local data={nav_world="nav",cleanup=true}
 NativeBuff.destroy({_template=other or template,_template_context={unit=unit,is_server=true},_template_data=data},true)
 assert(next(data)==nil,"native buff data cleanup was skipped")
end
effects_setup();local unit=roaming("renegade_executor");unit.keywords.rotten_armor=true
run(0,35);assert(#deleted==1 and B.retiring_units[unit] and HEALTH_ALIVE[unit])
B.finish_straggler_recycling() -- deletion callback may arrive after session reset
destroy(unit);assert(liquids==0 and vfx==0 and sfx==0)
destroy(unit,{stop_func=function(data,context,destroyed) assert(destroyed and data.cleanup);other_cleanup=other_cleanup+1 end})
assert(other_cleanup==1)
effects_setup();unit=roaming("renegade_executor");HEALTH_ALIVE[unit]=false
destroy(unit);assert(liquids==1 and vfx==1 and sfx==1,"real death payload was suppressed")
effects_setup();unit=roaming("renegade_executor")
ms.despawn_minion=function() end
run(0,35);assert(#deleted==0 and not B.retiring_units[unit])
destroy(unit);assert(liquids==1 and vfx==1 and sfx==1,"failed removal leaked retirement scope")
print("Actual Buff.destroy + native rotten stop/death payload: deferred non-death removal has no liquid/VFX/SFX; native cleanup, genuine death and failed retirement retain callbacks: PASS")
''')
