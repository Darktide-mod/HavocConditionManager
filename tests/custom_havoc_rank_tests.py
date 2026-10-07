"""Rank60 adapter against native generation, initialization and stat consumers."""
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
solo_source=Path(os.environ.get('DARKTIDE_SOLO_SOURCE',PROJECT/'.assistant-support/dev-support/installed-mod-fixtures/SoloPlay-2.6.5'))
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
for _,bad in ipairs({0,61,40.5,math.huge,-math.huge,"60",false}) do
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
assert(Rank.set(60) and solo:get("havoc_difficulty")==40 and Rank.get()==60)
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
L.execute('NativeHealth={};NativeToughness={};local PlayerUnitHealthExtension=NativeHealth;local PlayerUnitToughnessExtension=NativeToughness;'+method(health,'PlayerUnitHealthExtension','max_health')+'\n'+method(health,'PlayerUnitHealthExtension','max_wounds')+'\n'+method(tough,'PlayerUnitToughnessExtension','max_toughness'))
archetypes={}
toughness_source=(GAME/'scripts/settings/toughness/archetype_toughness_templates.lua').read_text(encoding='utf-8-sig')
for path in (GAME/'scripts/settings/archetype/archetypes').glob('*_archetype.lua'):
    name=path.stem.removesuffix('_archetype')
    source=path.read_text(encoding='utf-8-sig')
    hp=re.search(r'\n\thealth = (\d+)',source)
    toughness=re.search(r'archetype_toughness_templates\.'+re.escape(name)+r' = \{\s*max = (\d+)',toughness_source)
    if hp and toughness: archetypes[name]={'health':int(hp.group(1)),'toughness':int(toughness.group(1))}
assert set(archetypes)=={'adamant','broker','cryptic','ogryn','psyker','veteran','zealot'}
L.globals().rank60_archetypes=tbl(archetypes)
skin=re.search(r'local function _get_damage_reduction_value\(\)(.*?)\nend',buff_source,re.S).group(1)
L.globals().skin_value=L.execute('return function()'+skin+'\nend')
spillway=(GAME/'scripts/managers/pacing/bosses/spillway_wizard.lua').read_text(encoding='utf-8-sig')
helper=spillway[spillway.index('function _is_havoc()'):spillway.index('\nfunction _try_spawn_havoc_twin()')]
phase=spillway.index('abilities_component.current_ability = "force_push"')
start=spillway.rfind('init = function',0,phase)
init=spillway[start:spillway.index('\n\t\tend,',phase)+len('\n\t\tend')].replace('init = function','local init = function',1)
chance=re.search(r'local HAVOC_TWIN_CHANCE = ([^\n]+)',spillway).group(1)
L.execute('''
local BLACKBOARDS={}
local GameSession={set_game_object_field=function() end}
local ShockwaveStageHazard={init=function() end}
local function _set_toughness_shield_state() end
local function _index_against_challenge(v) return v end
local function _try_start_retreat_burst() end
local twins=0
local function _try_spawn_havoc_twin() twins=twins+1 end
local HAVOC_TWIN_CHANCE='''+chance+'\n'+helper+'\n'+init+'''
function check_twin_eligibility(expected)
 local unit={};BLACKBOARDS[unit]={spawn={}}
 local scratch={boss_unit=unit,positions={center={unbox=function() return {} end}},abilities_component={ability_position={store=function() end}}}
 local old=math.random;local before=twins
 math.random=function() return .5 end
 init(scratch,{inital_state="force_push",exhaust_escape_step={},burst_events={}}, {},1)
 assert(twins-before==(expected and 1 or 0))
 before=twins;math.random=function() return 1 end
 init(scratch,{inital_state="force_push",exhaust_escape_step={},burst_events={}}, {},1)
 assert(twins==before,"Native twin chance must still gate the custom rank path")
 math.random=old
end
''')
L.execute('''
results={}
for rank=40,60 do
 local extension,context=begin(rank)
 assert(extension:get_current_rank()==40 and Havoc.parse_data(context.havoc_data).havoc_rank==40)
 near(skin_value(),.5)
 check_twin_eligibility(true)
 local player=new_unit({});NativeHavocExtension._on_player_unit_spawned(extension,{player_unit=player})
 local health=NativeHealth.max_health({_health=200,_buff_extension={stat_buffs=function() return player.stats end}})
 local toughness=NativeToughness.max_toughness({_max_toughness=75,_buff_extension={stat_buffs=function() return player.stats end}})
 local d=rank-40
 near(player.stats.max_health_modifier,.65-d/60)
 near(player.stats.toughness,-45-5*d/9)
 near(player.stats.toughness_regen_rate_modifier,.5-d/90)
 near(player.stats.vent_warp_charge_speed,1.85+d/60)
 near(output.ammo,.4-d/120)
 near(extension._modifiers.modify_elite_health,.5+d/40)
 near(extension._modifiers.modify_special_health,.5+d/48)
 near(extension._modifiers.modify_monster_health,.7+.03*d)
 near(extension._modifiers.modify_horde_health,.3+.005*d)
 near(extension._modifiers.modify_horde_hit_mass,1.7+.02*d)
 near(extension._modifiers.add_more_elites,1+.125*d)
 near(extension._modifiers.add_more_ogryns,.8+.05*d)
 near(extension:get_power_level_modifier(),1.5+d/40)
 near(output.horde,2.4+.04*d);near(output.terror,.85+d/32)
 near(extension._modifiers.add_max_alive_specials,6+d/10)
 assert(extension._modifiers.add_num_monsters==3)
 local minion=new_unit({tags={horde=true,melee=true,far=true}})
 extension:_on_minion_unit_spawned(minion)
 near(minion.hit_mass,2.7+.02*d)
 near(minion.stats.melee_attack_speed,2+.05*d)
 near(minion.stats.ranged_attack_speed,1.3+.01*d)
 near(minion.stats.minion_num_shots_modifier,2.25+.05*d)
 near(minion.stats.permanent_damage_ratio,.3+d/160)
 assert(health>0 and toughness>0)
 local independent=new_unit({});independent.buff_system:add_internally_controlled_buff("havoc_health_modifier_5",1)
 near(independent.stats.max_health_modifier,.65)
 local snapshot=Rank.session()
 if rank>40 then
  assert(snapshot.record.requested_rank==rank)
  local old_ammo=output.ammo;Rank.set(41);assert(Rank.session()==snapshot and output.ammo==old_ammo)
 end
 results[#results+1]={rank=rank,health_factor=player.stats.max_health_modifier,max_health_base200=health,toughness_base75=toughness,regen=player.stats.toughness_regen_rate_modifier,ammo=output.ammo,special_bonus=extension._modifiers.add_max_alive_specials,slots_on_base5=math.ceil(5+extension._modifiers.add_max_alive_specials),native_rank=extension:get_current_rank(),skin=skin_value(),twin_eligibility=true,modifier_fields=Rules.copy(extension._modifiers),vent=player.stats.vent_warp_charge_speed,minion_hit_mass=minion.hit_mass,minion_stats={melee_attack_speed=minion.stats.melee_attack_speed,ranged_attack_speed=minion.stats.ranged_attack_speed,minion_num_shots_modifier=minion.stats.minion_num_shots_modifier,permanent_damage_ratio=minion.stats.permanent_damage_ratio}}
end
rank60_tier_checks=0;rank60_players={}
for rank=51,60 do
 for _,name in ipairs({"reduce_health_and_wounds","reduce_toughness","reduce_toughness_regen","ammo_pickup_modifier"}) do
  for tier=1,#require("scripts/settings/havoc_settings").modifier_templates[name] do
   local extension=begin(rank,{{name=name,level=tier}})
   local player=new_unit({});extension:_on_player_unit_spawned({player_unit=player})
   local stats=player.stats;local buff={stat_buffs=function() return stats end}
   assert(stats.max_health_modifier>0 and stats.toughness_regen_rate_modifier>0)
   for _,bases in pairs(rank60_archetypes) do
    assert(NativeHealth.max_health({_health=bases.health,_buff_extension=buff})>0)
    assert(NativeToughness.max_toughness({_max_toughness=bases.toughness,_buff_extension=buff})>0)
   end
   if output.ammo then assert(output.ammo>0) end
   rank60_tier_checks=rank60_tier_checks+1
  end
 end
end
assert(rank60_tier_checks==200)
local extension=begin(60);local player=new_unit({});extension:_on_player_unit_spawned({player_unit=player})
local buff={stat_buffs=function() return player.stats end}
for name,bases in pairs(rank60_archetypes) do
 rank60_players[name]={base_health=bases.health,base_toughness=bases.toughness,
  health=NativeHealth.max_health({_health=bases.health,_buff_extension=buff}),
  toughness=NativeToughness.max_toughness({_max_toughness=bases.toughness,_buff_extension=buff}),
  wounds_on_base2=NativeHealth.max_wounds({_base_max_wounds=2,_buff_extension=buff})}
 assert(rank60_players[name].wounds_on_base2==2)
end
assert(NativeHealth.max_wounds({_base_max_wounds=0,_buff_extension=buff})==1)
local selected={{name="buff_elites",level=2},{name="reduce_health_and_wounds",level=1}}
local extension=begin(60,selected)
near(extension._modifiers.modify_elite_health,.65)
assert(extension._modifiers.add_max_alive_specials==nil and extension._modifiers.ammo_pickup_modifier==nil)
local player=new_unit({});extension:_on_player_unit_spawned({player_unit=player})
near(player.stats.max_health_modifier,.85-1/3)
assert(player.added.havoc_toughness_modifier_5==nil)
for _,hook in ipairs(hooks) do if hook.target==NativeHavocExtension and hook.name=="_on_player_unit_spawned" then
 assert(not pcall(hook.fn,function() error("native event failure") end,extension,{player_unit=player}))
 local independent=new_unit({});independent.buff_system:add_internally_controlled_buff("havoc_health_modifier_1",1)
 near(independent.stats.max_health_modifier,.85)
end end
for _,mission in ipairs({"om_basic_combat_01","tg_shooting_range"}) do
 mods.SoloPlay:set("havoc_mission",mission)
 local ok,context=pcall(mods.SoloPlay.gen_havoc_mission_context)
 assert(ok and context.hcm_custom_havoc_v1==nil and Rank.get()==60)
end
mods.SoloPlay:set("havoc_mission","cm_archives")
singleplay=false;Rank.start();assert(Rank.session(),"A local player host must retain the custom rank")
local authority=mods.SoloPlay.has_local_gameplay_authority
mods.SoloPlay.has_local_gameplay_authority=function() return false end
assert(Rank.session()==nil);mods.SoloPlay.has_local_gameplay_authority=authority;singleplay=true
Rank.start();assert(Rank.session());Rank.finish();assert(Rank.session()==nil)
Rank.start();Managers.mechanism._mechanism._mechanism_data.havoc_data="different mission";assert(Rank.session()==nil)
assert(same(native_settings_before,require("scripts/settings/havoc_settings")))
assert(same(native_buffs_before,require("scripts/settings/buff/buff_templates")))
''')
plain=lambda t:{k:(plain(v) if hasattr(v,'items') else v) for k,v in t.items()}
record=[plain(v) for v in L.globals().results.values()]
(CHECKS/'custom-havoc-rank-results.json').write_text(json.dumps({'scope':'offline native Lua plus explicit engine/VO boundaries; no game launch','ranks':record,'rank60_selected_tier_checks':L.globals().rank60_tier_checks,'rank60_archetypes':plain(L.globals().rank60_players)},indent=2)+'\n',encoding='utf-8')
print('Custom rank60: native1-40 generation equivalence, all41-60 exact selected curves, real modifier/buff initialization and stat consumers, source immutability, DIY separation, mission snapshots and singleplay boundaries: PASS')
exec(Path(__file__).with_name('custom_local_host_regressions.py').read_text(encoding='utf-8'), globals())

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
assert(entry.max_value==60)
for _,rank in ipairs({40,41,45,50,55,60}) do
 entry.on_activated(rank,entry);assert(view._current_havoc_difficulty==rank and Rank.get()==rank and badge_rank==rank)
 for _,choice in ipairs(Havoc.parse_data(Havoc.generate_havoc_data(math.min(rank,40),1)).modifiers) do assert(view._current_modifier[choice.name]==choice.level) end
end
local previous=Rank.get();entry.on_activated(61,entry);assert(Rank.get()==previous and badge_rank==60)
entry.on_activated(40.5,entry);entry.on_activated(0/0,entry);assert(Rank.get()==previous)
view._modifier_customizable=true;view._current_modifier.buff_elites=2;solo:set("havoc_modifier_buff_elites",2)
entry.on_activated(45,entry);assert(solo:get("havoc_modifier_buff_elites")==2 and view._current_modifier.buff_elites==2)
view:_regen_havoc();assert(view._current_modifier.buff_elites==5)
test_language="en";assert(entry.format_value_function(60)=="60 (custom)")
print("Actual HCM rank callbacks: first-open16,60 cap,40/41/45/50/55/60 refresh,bounds,custom label,locked/manual selections and native Randomize behavior: PASS")
''')


# Use the installed HED config, context, codec, preset and mode bodies. File I/O
# and Studio export transport are boundaries; no installed mod files are edited.
assert L.eval('not Rank.install_presets()')
load_mod=original_load_mod
L.globals().load_mod_file=load_mod
hed_root=Path(os.environ.get('DARKTIDE_HED_SOURCE',PROJECT/'.assistant-support/dev-support/installed-mod-fixtures'))/'HavocEnemyDirector/scripts/mods/HavocEnemyDirector'
director_text=(hed_root/'native_director.lua').read_text(encoding='utf-8-sig')
L.execute('new_test_mod("HavocEnemyDirector");Managers.state.game_mode={game_mode_name=function() return "hub" end};Rank.finish();Rank.start()')
L.execute(director_text[:director_text.index('mod:io_dofile("HavocEnemyDirector/scripts/mods/HavocEnemyDirector/native_relative")')])
load_mod('HavocEnemyDirector/scripts/mods/HavocEnemyDirector/studio_mode')
load_mod('HavocEnemyDirector/scripts/mods/HavocEnemyDirector/native_presets')
bridge=(hed_root/'studio_bridge.lua').read_text(encoding='utf-8-sig')
# Run capture with its real dependencies; transport/export callbacks aren't invoked.
L.execute(bridge[:bridge.index('function mod.studio_export_context')])
cache['scripts/settings/mission/mission_templates']['cm_archives'].level='cm_archives'
def json_value(t):
    if not hasattr(t,'items'): return t
    items=dict(t.items())
    if items and set(items)==set(range(1,len(items)+1)):
        return [json_value(items[i]) for i in range(1,len(items)+1)]
    return {str(k):json_value(v) for k,v in items.items()}
L.globals().cjson=tbl({})
L.globals().cjson.encode=lambda doc:json.dumps(json_value(doc),ensure_ascii=False)
L.globals().cjson.decode=lambda text:tbl(json.loads(text))
L.execute('''
local base,solo,director=mods.HavocConditionManager,mods.SoloPlay,mods.HavocEnemyDirector
director.finish_director=function() finishes=(finishes or 0)+1 end
local dirty=director.studio_dirty
director.studio_dirty=function(...) dirties=(dirties or 0)+1;return dirty(...) end
assert(base.diy_library,"Actual DIY library must be present")
assert(base.diy_library.set_options({enabled=false,selected={}}))
solo:set("hcm_condition_selection_v3","")
solo:set("havoc_theme_circumstance","default");solo:set("havoc_difficulty_circumstance","default")
base:io_dofile("HavocConditionManager/scripts/mods/HavocConditionManager/diy/diy_seed").new(base).set(123)
assert(Rank.install_presets())
assert(Rank.set(60))
solo:set("havoc_modifier_buff_elites",2);solo:set("havoc_modifier_buff_specials",0);solo:set("havoc_modifiers_customizable",true)
local cfg=director.get_saved_config()
cfg.studio={version=1,recycling=base:io_dofile("HavocConditionManager/scripts/mods/HavocConditionManager/recycling_config").validate(base:get("recycling_v1")),spatial={},policies={}}
cfg.studio.mission={id="cm_archives",level="cm_archives",rank=30}
assert(director.save_config(cfg))
custom_doc=assert(director.presets.capture("Rank60 roundtrip"))
assert(custom_doc.config.studio.mission.rank==40 and director.peek_config().studio.mission.rank==30)
assert(custom_doc.hcm_custom_havoc_v1.requested_rank==60 and custom_doc.hcm_custom_havoc_v1.modifiers.buff_elites==2 and custom_doc.hcm_custom_havoc_v1.modifiers.buff_specials==0)
assert(custom_doc.hcm_custom_havoc_v1.customizable)
local decoded=assert(director.presets.decode(cjson.encode(custom_doc)))
assert(same(decoded,custom_doc))
assert(Rank.set(16))
preset_view={_current={},_current_modifier={buff_elites=5,buff_specials=5},_modifier_customizable=false,_current_havoc_difficulty=16}
preset_view._setup_havoc_badge=function(self) shown_badge=self._current_havoc_difficulty end
assert(director.presets.apply(decoded,preset_view))
assert(Rank.get()==60 and solo:get("havoc_difficulty")==40 and shown_badge==60)
assert(solo:get("havoc_modifier_buff_elites")==2 and solo:get("havoc_modifier_buff_specials")==0)
assert(preset_view._current_modifier.buff_elites==2 and preset_view._modifier_customizable)
assert(director.studio_capture_context().document.hcm_custom_havoc_v1.requested_rank==60)
-- Previously saved custom50 metadata remains valid under the expanded cap.
local custom50_doc=Rules.copy(custom_doc);custom50_doc.hcm_custom_havoc_v1.requested_rank=50
assert(director.presets.codec.validate(custom50_doc))
assert(director.presets.apply(custom50_doc,preset_view) and Rank.get()==50 and shown_badge==50)
assert(director.presets.apply(custom_doc,preset_view) and Rank.get()==60 and shown_badge==60)
function complete_state()
 return {base=Rules.copy(base.values),solo=Rules.copy(solo.values),director=Rules.copy(director.values),config=director.get_saved_config(),diy=Rules.copy(base.diy_library.options)}
end
local before=complete_state()
for _,mutate in ipairs({
 function(v) v.hcm_custom_havoc_v1.requested_rank=61 end,
 function(v) v.hcm_custom_havoc_v1.requested_rank=0/0 end,
 function(v) v.hcm_custom_havoc_v1.modifiers.buff_elites=nil end,
 function(v) v.hcm_custom_havoc_v1.modifiers.buff_elites=6 end,
 function(v) v.hcm_custom_havoc_v1.extra=true end,
 function(v) setmetatable(v.hcm_custom_havoc_v1,{}) end,
 function(v) v.config.studio.mission.rank=30 end,
 function(v) v.unknown=true end,
}) do
 local bad=Rules.copy(custom_doc);mutate(bad)
 assert(not director.presets.codec.validate(bad));assert(not director.presets.apply(bad,preset_view))
 assert(same(before,complete_state()))
end
-- Older documents remain readable without changing current state; explicit old
-- native-rank40 apply and same-value native writes invalidate custom metadata.
legacy_doc=Rules.copy(custom_doc);legacy_doc.hcm_custom_havoc_v1=nil
assert(director.presets.codec.validate(legacy_doc) and Rank.get()==60)
assert(director.presets.apply(legacy_doc,preset_view) and Rank.get()==40)
assert(Rank.set(60));local old_dirty=dirties
solo:set("havoc_difficulty",40);assert(Rank.get()==40 and dirties>old_dirty)
assert(Rank.set(60))
assert(director.set_studio_mode("hcm") and Rank.get()==40)
assert(Rank.set(45));solo:set("havoc_modifier_buff_elites",1)
assert(director.set_studio_mode("hed") and Rank.get()==60 and solo:get("havoc_modifier_buff_elites")==2)
assert(director.set_studio_mode("hcm") and Rank.get()==45 and solo:get("havoc_modifier_buff_elites")==1)
-- Invalid persisted mode records reject before any native writes.
for _,bad in ipairs({true,"bad",{other=custom_doc.hcm_custom_havoc_v1},{hed={version=1}},setmetatable({},{})}) do
 base.values.hcm_custom_havoc_modes_v1=bad;local saved=complete_state()
 assert(not director.set_studio_mode("hed"));assert(same(saved,complete_state()))
end
base:set("hcm_custom_havoc_modes_v1",nil)
-- Ordinary mission-time refusal must not clean up active owners or settings.
Managers.state.game_mode.game_mode_name=function() return "coop" end
before=complete_state();local old_finishes=finishes;local old_reset=base.template_runtime.reset
local resets=0;base.template_runtime.reset=function() resets=resets+1 end
assert(not director.presets.apply(custom_doc,preset_view))
assert(not director.set_studio_mode("hed"));assert(director.set_studio_mode("hcm"))
assert(not director.set_studio_mode("invalid"))
assert(same(before,complete_state()) and finishes==old_finishes and resets==0)
base.template_runtime.reset=old_reset;Managers.state.game_mode.game_mode_name=function() return "hub" end
-- A failure after native apply succeeds must restore all storage, cached native
-- config, DIY options, mode, selections and the already refreshed UI.
assert(Rank.set(45))
preset_view._current_havoc_difficulty=45;preset_view._current_modifier.buff_elites=1
local ui_before={rank=preset_view._current_havoc_difficulty,modifiers=Rules.copy(preset_view._current_modifier),lock=preset_view._modifier_customizable}
before=complete_state()
local setter=base.set;local fail=true
base.set=function(self,key,value)
 if fail and key==Rules.storage_key and value and value.requested_rank==60 then fail=false;error("owned write fault") end
 return setter(self,key,value)
end
assert(not pcall(director.presets.apply,custom_doc,preset_view));base.set=setter
assert(same(before,complete_state()) and Rank.get()==45)
assert(preset_view._current_havoc_difficulty==ui_before.rank and shown_badge==45)
assert(same(preset_view._current_modifier,ui_before.modifiers) and preset_view._modifier_customizable==ui_before.lock)
-- Native apply failure and a late original exception also restore full state.
local save_config=director.save_config;fail=true
director.save_config=function(raw) if fail then fail=false;return false,"native config fault" end;return save_config(raw) end
before=complete_state();assert(not director.presets.apply(custom_doc,preset_view));director.save_config=save_config
assert(same(before,complete_state()))
Rank.uninstall_presets()
local apply=director.presets.apply
director.presets.apply=function(...)
 assert(apply(...));error("late native apply fault")
end
assert(Rank.install_presets());before=complete_state()
assert(not pcall(director.presets.apply,custom_doc,preset_view));assert(same(before,complete_state()))
Rank.uninstall_presets();director.presets.apply=apply;assert(Rank.install_presets())
-- Failure persisting mode-specific metadata is in the same transaction.
base:set("hcm_custom_havoc_modes_v1",nil);before=complete_state();fail=true
base.set=function(self,key,value)
 if fail and key=="hcm_custom_havoc_modes_v1" then fail=false;error("mode persistence fault") end
 return setter(self,key,value)
end
assert(not pcall(director.set_studio_mode,"hed"));base.set=setter
assert(same(before,complete_state()))
-- Disable detaches preset bridges, retaining only the native setter observer
-- needed for legacy rank resets. Re-enable restores the optional integration.
base._enabled=false;base.on_disabled(false)
assert(base._custom_havoc_preset_bridge==nil)
solo:set("havoc_difficulty",40);assert(base:get(Rules.storage_key)==nil)
base._enabled=true;base.on_enabled(false);assert(base._custom_havoc_preset_bridge)
print("Actual HED codec/presets/modes: rank60 JSON roundtrip, selected tiers/zeros/lock, old native presets, malformed data, mission no-op refusal, complete state/UI rollback and disable/re-enable: PASS")
''')
# Real reload callback body, with explicit DMF hook removal boundary.
L.execute('''
local base,solo,director=mods.HavocConditionManager,mods.SoloPlay,mods.HavocEnemyDirector
local first=Rank;local inner=solo.set;local third_calls=0
local third=function(...) third_calls=third_calls+1;return inner(...) end
solo.set=third
-- An externally captured preset wrapper must become a pass-through after unload.
local captured=director.presets.capture
local third_capture=function(...) return captured(...) end
director.presets.capture=third_capture
base.on_unload(false)
assert(solo.set==third and director.presets.capture==third_capture and base._custom_havoc_preset_bridge==nil)
local filtered={}
for _,h in ipairs(hooks) do
 if h.owner~=base or h.target~=NativeHavocExtension and not (h.require_hook and h.path=="scripts/extension_systems/buff/buffs/buff") then filtered[#filtered+1]=h end
end
hooks=filtered
Rank=base:io_dofile("HavocConditionManager/scripts/mods/HavocConditionManager/custom_havoc_rank_runtime")
base.custom_havoc_rank=Rank
base:io_dofile("HavocConditionManager/scripts/mods/HavocConditionManager/custom_havoc_rank_presets")(Rank,base,solo)
assert(Rank.install_presets());assert(Rank.set(60) and Rank.get()==60)
local expected_calls=third_calls
assert(Rank.set(45) and Rank.get()==45 and third_calls==expected_calls+1)
solo:set("havoc_difficulty",40);assert(Rank.get()==40)
-- Same director object with replaced exported tables must be wrapped anew.
Rank.uninstall_presets()
local replacement=director:io_dofile("HavocEnemyDirector/scripts/mods/HavocEnemyDirector/native_presets")
assert(Rank.install_presets());assert(Rank.set(60))
assert(replacement.capture("replacement").hcm_custom_havoc_v1.requested_rank==60)
local old_capture=replacement.capture
director.presets=nil
assert(not Rank.install_presets() and base._custom_havoc_preset_bridge==nil)
assert(old_capture("inactive").hcm_custom_havoc_v1==nil)
director.presets=replacement;assert(Rank.install_presets())
-- Both DMF reload and exit callbacks restore plain wrappers while preserving
-- third-party ownership. Disabled mods still receive on_unload.
base._enabled=false;base.on_unload(true)
assert(solo.set==third and base._custom_havoc_preset_bridge==nil)
assert(third_capture("unloaded").hcm_custom_havoc_v1==nil)
print("Actual DMF callback body: reload(false), exit(true), disabled unload, setter/preset wrappers behind third-party ownership, no stale depth guards, replaced optional API and absent HED: PASS")
''')

# Same owner/tables can publish individual optional functions after installation.
# Exercise the actual HED HCM-mode capture, which bypasses presets.capture.
L.execute('''
local base,solo,director=mods.HavocConditionManager,mods.SoloPlay,mods.HavocEnemyDirector
base._enabled=true;Rank.uninstall_presets()
assert(director.set_studio_mode("hcm"));assert(Rank.set(60))
local presets,codec=director.presets,director.presets.codec
local methods={
 {target=codec,key="validate"},
 {target=presets,key="capture"},{target=presets,key="apply"},
 {target=director,key="studio_capture_context"},
 {target=director,key="studio_refresh_view"},{target=director,key="set_studio_mode"},
}
local function identities()
 local values={}
 for i,entry in ipairs(methods) do values[i]={value=entry.target[entry.key]} end
 return values
end
local function stable(before)
 for i,entry in ipairs(methods) do assert(entry.target[entry.key]==before[i].value,"Repeated installation changed "..entry.key) end
end
local function captured_rank()
 local snapshot=assert(director.studio_capture_context())
 assert(snapshot.mode=="hcm" and snapshot.document.config.studio.mission.rank==40)
 assert(snapshot.document.hcm_custom_havoc_v1.requested_rank==60)
end
for _,missing in ipairs({{}, {value=false}}) do
 for i=2,#methods do
  local entry=methods[i];local original=entry.target[entry.key]
  entry.target[entry.key]=missing.value
  assert(Rank.install_presets())
  local before=identities()
  for _=1,5 do assert(Rank.install_presets());stable(before) end
  entry.target[entry.key]=original
  assert(Rank.install_presets() and entry.target[entry.key]~=original)
  before=identities()
  for _=1,5 do assert(Rank.install_presets());stable(before) end
  assert(director.presets==presets and director.presets.codec==codec)
  captured_rank()
  Rank.uninstall_presets();assert(entry.target[entry.key]==original)
 end
end
-- A slot HCM never wrapped can be published before uninstall: preserve it.
local capture=director.studio_capture_context
director.studio_capture_context=nil;assert(Rank.install_presets())
director.studio_capture_context=capture
Rank.uninstall_presets();assert(director.studio_capture_context==capture)
assert(Rank.install_presets());captured_rank();Rank.uninstall_presets()
-- Required codec readiness still refuses absent validation without overwriting
-- the method when its owner subsequently publishes it.
local validate=codec.validate
codec.validate=nil;assert(not Rank.install_presets())
codec.validate=validate;assert(Rank.install_presets());captured_rank();Rank.uninstall_presets()
-- Existing functions can be replaced in place on every supported slot.
for _,entry in ipairs(methods) do
 local original=entry.target[entry.key]
 assert(Rank.install_presets())
 local replacement=function(...) return original(...) end
 entry.target[entry.key]=replacement
 assert(Rank.install_presets() and entry.target[entry.key]~=replacement)
 local before=identities()
 for _=1,5 do assert(Rank.install_presets());stable(before) end
 captured_rank()
 Rank.uninstall_presets();assert(entry.target[entry.key]==replacement)
 entry.target[entry.key]=original
end
-- A third party retains its outer wrapper across reinstall/uninstall, while
-- its captured old HCM adapter becomes inactive. Metadata is injected once.
assert(Rank.install_presets())
local previous=director.studio_capture_context
local foreign_calls=0
local foreign=function(...) foreign_calls=foreign_calls+1;return previous(...) end
director.studio_capture_context=foreign
assert(Rank.install_presets())
local rules=Rank.rules;local preset=rules.preset;local owned_captures=0
rules.preset=function(...) owned_captures=owned_captures+1;return preset(...) end
captured_rank();assert(foreign_calls==1 and owned_captures==1)
local before=identities();assert(Rank.install_presets());stable(before)
captured_rank();assert(foreign_calls==2 and owned_captures==2)
Rank.uninstall_presets()
assert(director.studio_capture_context==foreign)
assert(director.studio_capture_context().document.hcm_custom_havoc_v1==nil)
assert(foreign_calls==3 and owned_captures==2)
Rank.uninstall_presets();assert(director.studio_capture_context==foreign)
rules.preset=preset
print("Optional HED APIs: same-owner/same-table nil/false-to-function appearance on all five optional methods, actual HCM capture native40/requested50, six function replacements, repeated installation idempotency, mandatory codec readiness and third-party uninstall ownership: PASS")
''')
