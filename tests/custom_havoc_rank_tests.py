"""Rank50 adapter against native generation, initialization and stat consumers."""
from pathlib import Path
import hashlib, json, math, os, re
exec(Path(__file__).with_name('native_integration_tests.py').read_text(encoding='utf-8'),globals())

settings_native=require('scripts/settings/havoc_settings')
buffs=cache['scripts/settings/buff/buff_templates']
buff_source=(GAME/'scripts/settings/buff/havoc_buff_templates.lua').read_text(encoding='utf-8-sig')
ordinary_buff_names=set()
for choices in settings_native.modifier_templates.values():
    for choice in choices.values():
        for value in choice.values():
            if isinstance(value,str): ordinary_buff_names.add(value)
L.globals().native_buff_stat_keys=require('scripts/settings/buff/buff_settings').stat_buffs
for name in sorted(ordinary_buff_names):
    match=re.search(r'(?m)^templates\.'+re.escape(name)+r' = \{(.*?)^\}',buff_source,re.S)
    assert match,name
    definition=L.execute('local buff_stat_buffs=native_buff_stat_keys;return {'+match.group(1)+'}')
    definition.name=name
    assert definition.class_name=='buff'
    buffs[name]=definition

L.execute('''
function math.next_random(seed,a,b) return seed,a end
NetworkLookup={havoc_modifiers={}}
local names=table.keys(require("scripts/settings/havoc_settings").modifier_templates)
table.sort(names)
for i,name in ipairs(names) do NetworkLookup.havoc_modifiers[name]=i;NetworkLookup.havoc_modifiers[i]=name end
mods.SoloPlay.is_soloplay=function() return singleplay~=false end
''')
cache['scripts/utilities/havoc']=lua_file(GAME/'scripts/utilities/havoc.lua')
cache['scripts/settings/mission/mission_templates']=tbl({'cm_archives':{'game_mode_name':'coop'},
    'om_basic_combat_01':{'game_mode_name':'training_grounds'},'tg_shooting_range':{'game_mode_name':'shooting_range'}})
L.globals().Havoc=cache['scripts/utilities/havoc']
L.globals().hcm_context_wrapper=L.globals().mods.SoloPlay.gen_havoc_mission_context
solo_source=Path(os.environ.get('DARKTIDE_SOLO_SOURCE',PROJECT.parent/'dev-support/installed-mod-fixtures/SoloPlay-2.6.5'))
solo_text=(solo_source/'SoloPlay.lua').read_text(encoding='utf-8-sig')
assert hashlib.sha256((solo_source/'SoloPlay.lua').read_bytes()).hexdigest()=='c99f4507258779dff1ac29a06deb54b18e805aa1cb1a74573d60d8dc38899807'
assert hashlib.sha256((solo_source/'havoc.lua').read_bytes()).hexdigest()=='434c7c74daca7eff1a4a82b2c50e0c775c0ce0a7961d34e7a2e5e401f032cd6c'
lua_file(solo_source/'havoc.lua')
def method(text,owner,name):
    start=text.index(owner+'.'+name+' = function')
    return text[start:text.index('\nend',start)+4]
context_function=method(solo_text,'mod','gen_havoc_mission_context')
L.execute('''local mod=mods.SoloPlay
local SoloPlaySettings={lookup={theme_of_circumstances={default="default"},havoc_modifiers_max_level={}}}
for name,tiers in pairs(require("scripts/settings/havoc_settings").modifier_templates) do SoloPlaySettings.lookup.havoc_modifiers_max_level[name]=#tiers end
local _mission_giver_vo_override=function() return "sergeant_a" end
mod.parse_mission_params=function(s) return s,"" end
'''+context_function)
# The real HCM wrapper remains in place; replace only its saved native delegate.
L.execute('mods.SoloPlay._havoc_condition_manager_context_wrapper=mods.SoloPlay.gen_havoc_mission_context;mods.SoloPlay.gen_havoc_mission_context=hcm_context_wrapper')
L.execute('''
local base=mods.HavocConditionManager
local solo=mods.SoloPlay
solo:set("havoc_mission","cm_archives");solo:set("havoc_faction","renegade")
for _,key in ipairs({"havoc_circumstance1","havoc_circumstance2","havoc_theme_circumstance","havoc_difficulty_circumstance"}) do solo:set(key,"default") end
Rank=base.custom_havoc_rank;Rules=Rank.rules
function near(a,b) assert(math.abs(a-b)<1e-10,tostring(a).." != "..tostring(b)) end
function same(a,b)
 if type(a)~=type(b) then return false end
 if type(a)~="table" then return a==b end
 for k,v in pairs(a) do if not same(v,b[k]) then return false end end
 for k in pairs(b) do if a[k]==nil then return false end end
 return true
end
native_settings_before=Rules.copy(require("scripts/settings/havoc_settings"))
native_buffs_before=Rules.copy(require("scripts/settings/buff/buff_templates"))
for _,bad in ipairs({0,51,40.5,math.huge,-math.huge,"50",false}) do
 local old=solo:get("havoc_difficulty");assert(not Rank.set(bad));assert(solo:get("havoc_difficulty")==old)
 assert(not pcall(Rank.generate,Havoc.generate_havoc_data,bad,1))
end
assert(not Rules.validate(0/0))
for rank=1,40 do
 assert(Rank.set(rank));assert(Rank.get()==rank and base:get(Rules.storage_key)==nil)
 assert(Rank.generate(Havoc.generate_havoc_data,rank,1)==Havoc.generate_havoc_data(rank,1))
 assert(same(Rank.generate(solo.gen_havoc_data,rank),solo.gen_havoc_data(rank)))
 assert(Rules.capture(rank,{})==nil)
end
assert(Rank.set(50) and solo:get("havoc_difficulty")==40 and Rank.get()==50)
local selected=Havoc.parse_data(Havoc.generate_havoc_data(40,1)).modifiers
for _,choice in ipairs(selected) do solo:set("havoc_modifier_"..choice.name,choice.level) end
''')

gme_text=(GAME/'scripts/managers/game_mode/game_mode_extensions/game_mode_extension_havoc.lua').read_text(encoding='utf-8-sig')
gme=class_paths['scripts/managers/game_mode/game_mode_extensions/game_mode_extension_havoc']
L.globals().NativeHavocExtension=gme
gme_names=('_initialize_modifiers','_initialize_server_modifiers','on_gameplay_init','get_modifier_value','get_current_rank',
           'get_minion_health_modifier','get_power_level_modifier','_on_player_unit_spawned','_on_minion_unit_spawned')
L.execute('local HavocSettings=require("scripts/settings/havoc_settings");local GameModeExtensionHavoc=NativeHavocExtension;GameModeExtensionHavoc.super={on_gameplay_init=function() end};'+ '\n'.join(method(gme_text,'GameModeExtensionHavoc',n) for n in gme_names))
L.execute('''
local class=NativeHavocExtension
for _,hook in ipairs(hooks) do
 if hook.target==class and (hook.name=="_initialize_modifiers" or hook.name=="_on_player_unit_spawned" or hook.name=="_on_minion_unit_spawned") then
  local original,name,callback=class[hook.name],hook.name,hook.fn
  class[name]=function(self,...) return callback(original,self,...) end
 end
end
NativeBuff={}
''')
native_buff_text=(GAME/'scripts/extension_systems/buff/buffs/buff.lua').read_text(encoding='utf-8-sig')
L.execute('''local Buff=NativeBuff
local BuffArgs={add_args_to_context=function() end}
local FixedFrame={get_latest_fixed_frame=function() return 1 end}
local EMPTY_TABLE={}
local _default_conditional_keywords_func=function() return true end
local _default_stat_buff_multiplier=function() return 1 end
local _default_conditional_stat_buffs_func=function() return true end
local stat_buff_types=require("scripts/settings/buff/buff_settings").stat_buff_types
'''+method(native_buff_text,'Buff','init')+'\n'+method(native_buff_text,'Buff','_calculate_stat_buffs'))
L.execute('''
for _,hook in ipairs(hooks) do if hook.path=="scripts/extension_systems/buff/buffs/buff" then hook.fn(NativeBuff) end end
for _,hook in ipairs(hooks) do if hook.target==NativeBuff and hook.name=="init" then
 local fn,callback=NativeBuff.init,hook.fn
 NativeBuff.init=function(self,...) return callback(fn,self,...) end
end end
ScriptUnit={has_extension=function() end,extension=function(unit,name) return unit[name] end}
local buff_templates=require("scripts/settings/buff/buff_templates")
function new_unit(breed)
 local unit={added={},stats=Rules.copy(require("scripts/settings/buff/buff_settings").stat_buff_type_base_values)}
 unit.stats._modified_stats={}
 unit.unit_data_system={breed=function() return breed end}
 unit.health_system={hit_mass=function() return 1 end,set_hit_mass=function(_,value) unit.hit_mass=value end}
 unit.buff_system={add_internally_controlled_buff=function(_,name,t)
  local instance={_calculate_template_override_data=function() return {} end,duration=function() end,stat_buff_stacking_count=function() return 1 end}
  NativeBuff.init(instance,{unit=unit,is_server=true},buff_templates[name],t,1)
  NativeBuff._calculate_stat_buffs(instance,unit.stats,instance._template.stat_buffs,false)
  unit.added[name]=instance
 end}
 return unit
end
function begin(rank,selected)
 Rank.finish();Rank.start();assert(Rank.set(rank))
 local context=mods.SoloPlay.gen_havoc_mission_context()
 local parsed=Havoc.parse_data(context.havoc_data)
 if selected then parsed.modifiers=selected;context.hcm_custom_havoc_v1=Rules.capture(rank,selected);context.hcm_custom_havoc_v1.native_data=context.havoc_data end
 Managers.mechanism={_mechanism={_context=context,_mechanism_data={havoc_data=context.havoc_data}}}
 Managers.state.difficulty={get_parsed_havoc_data=function() return parsed end,set_ammo_modifier=function(_,v) output.ammo=v end}
 Managers.state.pacing={set_horde_rate_modifier=function(_,v) output.horde=v end,set_roamer_tag_limit_bonus=function(_,v) output.tags=v end}
 Managers.state.terror_event={set_terror_event_point_modifier=function(_,v) output.terror=v end}
 Managers.event={register=function() end}
 Managers.time={time=function() return 1 end}
 output={}
 local extension=setmetatable({_is_server=true},{__index=NativeHavocExtension})
 Managers.state.game_mode={game_mode=function() return {extension=function() return extension end} end}
 NativeHavocExtension.on_gameplay_init(extension)
 return extension,context,parsed
end
''')
health=(GAME/'scripts/extension_systems/health/player_unit_health_extension.lua').read_text(encoding='utf-8-sig')
tough=(GAME/'scripts/extension_systems/toughness/player_unit_toughness_extension.lua').read_text(encoding='utf-8-sig')
L.execute('NativeHealth={};NativeToughness={};local PlayerUnitHealthExtension=NativeHealth;local PlayerUnitToughnessExtension=NativeToughness;'+method(health,'PlayerUnitHealthExtension','max_health')+'\n'+method(tough,'PlayerUnitToughnessExtension','max_toughness'))
skin=re.search(r'local function _get_damage_reduction_value\(\)(.*?)\nend',buff_source,re.S).group(1)
L.globals().skin_value=L.execute('return function()'+skin+'\nend')
L.execute('''
results={}
for rank=40,50 do
 local extension,context=begin(rank)
 assert(extension:get_current_rank()==40 and Havoc.parse_data(context.havoc_data).havoc_rank==40)
 near(skin_value(),.5)
 local player=new_unit({});NativeHavocExtension._on_player_unit_spawned(extension,{player_unit=player})
 local health=NativeHealth.max_health({_health=200,_buff_extension={stat_buffs=function() return player.stats end}})
 local toughness=NativeToughness.max_toughness({_max_toughness=75,_buff_extension={stat_buffs=function() return player.stats end}})
 local d=rank-40
 near(player.stats.max_health_modifier,.65-d/60)
 near(player.stats.toughness_regen_rate_modifier,.5-d/90)
 near(output.ammo,.4-d/120)
 near(extension._modifiers.modify_elite_health,.5+d/40)
 near(extension._modifiers.add_max_alive_specials,6+d/10)
 assert(extension._modifiers.add_num_monsters==3)
 assert(health>0 and toughness>0)
 local independent=new_unit({});independent.buff_system:add_internally_controlled_buff("havoc_health_modifier_5",1)
 near(independent.stats.max_health_modifier,.65)
 local snapshot=Rank.session()
 if rank>40 then
  assert(snapshot.record.requested_rank==rank)
  local old_ammo=output.ammo;Rank.set(41);assert(Rank.session()==snapshot and output.ammo==old_ammo)
 end
 results[#results+1]={rank=rank,health_factor=player.stats.max_health_modifier,max_health_base200=health,toughness_base75=toughness,regen=player.stats.toughness_regen_rate_modifier,ammo=output.ammo,special_bonus=extension._modifiers.add_max_alive_specials,slots_on_base5=math.ceil(5+extension._modifiers.add_max_alive_specials),native_rank=extension:get_current_rank(),skin=skin_value()}
end
local selected={{name="buff_elites",level=2},{name="reduce_health_and_wounds",level=1}}
local extension=begin(50,selected)
near(extension._modifiers.modify_elite_health,.4)
assert(extension._modifiers.add_max_alive_specials==nil and extension._modifiers.ammo_pickup_modifier==nil)
local player=new_unit({});extension:_on_player_unit_spawned({player_unit=player})
near(player.stats.max_health_modifier,.85-1/6)
assert(player.added.havoc_toughness_modifier_5==nil)
for _,hook in ipairs(hooks) do if hook.target==NativeHavocExtension and hook.name=="_on_player_unit_spawned" then
 assert(not pcall(hook.fn,function() error("native event failure") end,extension,{player_unit=player}))
 local independent=new_unit({});independent.buff_system:add_internally_controlled_buff("havoc_health_modifier_1",1)
 near(independent.stats.max_health_modifier,.85)
end end
for _,mission in ipairs({"om_basic_combat_01","tg_shooting_range"}) do
 mods.SoloPlay:set("havoc_mission",mission)
 assert(not pcall(mods.SoloPlay.gen_havoc_mission_context))
end
mods.SoloPlay:set("havoc_mission","cm_archives")
singleplay=false;Rank.start();assert(Rank.session()==nil);singleplay=true
Rank.start();assert(Rank.session());Rank.finish();assert(Rank.session()==nil)
Rank.start();Managers.mechanism._mechanism._mechanism_data.havoc_data="different mission";assert(Rank.session()==nil)
assert(same(native_settings_before,require("scripts/settings/havoc_settings")))
assert(same(native_buffs_before,require("scripts/settings/buff/buff_templates")))
''')
plain=lambda t:{k:(plain(v) if hasattr(v,'items') else v) for k,v in t.items()}
record=[plain(v) for v in L.globals().results.values()]
(CHECKS/'custom-havoc-rank-results.json').write_text(json.dumps({'scope':'offline native Lua plus explicit engine/VO boundaries; no game launch','ranks':record},indent=2)+'\n',encoding='utf-8')
print('Custom rank50: native1-40 generation equivalence, all41-50 exact selected curves, real modifier/buff initialization and stat consumers, source immutability, DIY separation, mission snapshots and singleplay boundaries: PASS')

# Execute the actual rank setup/refresh/randomize callbacks; rendering is a boundary.
view_text=(SOURCES/'HavocConditionManager/scripts/mods/HavocConditionManager/condition_manager_view/condition_manager_view.lua').read_text(encoding='utf-8-sig')
getter=view_text[view_text.index('local function get_setting'):view_text.index('\nHavocConditionManagerView = class')]
view_methods=('_setup_havoc_difficulty','_setup_havoc_badge','_refresh_modifiers','_apply_modifiers','_regen_havoc')
L.execute('''
RankView={}
local HavocConditionManagerView=RankView
local mod=mods.HavocConditionManager
local base_mod=mods.SoloPlay
local addon_setting_keys={}
local Havoc=require("scripts/utilities/havoc")
local HavocConditions=mod:io_dofile("HavocConditionManager/scripts/mods/HavocConditionManager/havoc_conditions")
local UIWidget=require("scripts/managers/ui/ui_widget")
local view_settings=mod:io_dofile("HavocConditionManager/scripts/mods/HavocConditionManager/condition_manager_view/condition_manager_view_settings")
local SoloPlaySettings={lookup={havoc_modifiers_max_level={},havoc_circumstances={}}}
for name,tiers in pairs(require("scripts/settings/havoc_settings").modifier_templates) do SoloPlaySettings.lookup.havoc_modifiers_max_level[name]=#tiers end
local blueprints={havoc_difficulty_slider={pass_template={},init=function(_,widget,entry) widget.content.entry=entry end},havoc_badge={pass_template_function=function(rank) badge_rank=rank;return {} end}}
'''+getter+'\n'+'\n'.join(method(view_text,'HavocConditionManagerView',n) for n in view_methods))
L.execute('''
local base,solo=mods.HavocConditionManager,mods.SoloPlay
Rank.finish();Rank.start();base:set(Rules.storage_key,nil);solo:set("havoc_difficulty",nil)
local view=setmetatable({_current={},_current_modifier={},_modifier_customizable=false},{__index=RankView})
view._create_widget=function(_,name,definition) return definition end
view._persist_havoc_circumstances=function() end
view._recreate_dropdown=function() end
view._refresh_condition_dropdowns=function() end
view:_setup_havoc_difficulty()
assert(view._current_havoc_difficulty==16 and solo:get("havoc_difficulty")==16)
local expected=Havoc.parse_data(Havoc.generate_havoc_data(16,1)).modifiers
for _,choice in ipairs(expected) do assert(view._current_modifier[choice.name]==choice.level) end
local entry=view._havoc_difficulty_slider_widget.content.entry
assert(entry.max_value==50)
for _,rank in ipairs({40,41,45,50}) do
 entry.on_activated(rank,entry);assert(view._current_havoc_difficulty==rank and Rank.get()==rank and badge_rank==rank)
 for _,choice in ipairs(Havoc.parse_data(Havoc.generate_havoc_data(math.min(rank,40),1)).modifiers) do assert(view._current_modifier[choice.name]==choice.level) end
end
local previous=Rank.get();entry.on_activated(51,entry);assert(Rank.get()==previous and badge_rank==50)
entry.on_activated(40.5,entry);entry.on_activated(0/0,entry);assert(Rank.get()==previous)
view._modifier_customizable=true;view._current_modifier.buff_elites=2;solo:set("havoc_modifier_buff_elites",2)
entry.on_activated(45,entry);assert(solo:get("havoc_modifier_buff_elites")==2 and view._current_modifier.buff_elites==2)
view:_regen_havoc();assert(view._current_modifier.buff_elites==5)
test_language="en";assert(entry.format_value_function(50)=="50 (custom)")
print("Actual HCM rank callbacks: first-open16,50 cap,40/41/45/50 refresh,bounds,custom label,locked/manual selections and native Randomize behavior: PASS")
''')
