"""Run from custom_havoc_rank_tests after native modifier/buff consumers load.

Production SoloPlay 2.6.9 authority/context methods and Realms host_type execute
unchanged. Network transport, actors and mission VO remain explicit boundaries.
"""
local_host_fixture = PROJECT / 'tests/fixtures/solo_realms_local_host.lua'
assert hashlib.sha256(local_host_fixture.read_bytes()).hexdigest() == '88418349c07f6cae28220cfe561304da3dd180663a304aff1e3b139f1855e102'
cache['scripts/settings/network/matchmaking_constants'] = lua_file(GAME / 'scripts/settings/network/matchmaking_constants.lua')
L.execute('''
local solo=mods.SoloPlay
local_host_saved={authority=solo.has_local_gameplay_authority,is_soloplay=solo.is_soloplay,
 generator=solo.gen_havoc_mission_context,native_generator=solo._havoc_condition_manager_context_wrapper,
 multiplayer=Managers.multiplayer_session,game_session=Managers.state.game_session,game_mode=Managers.state.game_mode}
local_host_solo_settings={lookup={theme_of_circumstances={default="default"},havoc_modifiers_max_level={}}}
for name,tiers in pairs(require("scripts/settings/havoc_settings").modifier_templates) do
 local_host_solo_settings.lookup.havoc_modifiers_max_level[name]=#tiers
end
''')
L.globals().LocalHostConnection = lua_file(local_host_fixture)
L.execute('''
local base,solo=mods.HavocConditionManager,mods.SoloPlay
local types=require("scripts/settings/network/matchmaking_constants").HOST_TYPES
solo._havoc_condition_manager_context_wrapper=solo.gen_havoc_mission_context
solo.gen_havoc_mission_context=local_host_saved.generator
base.custom_efl=base:io_dofile("HavocConditionManager/scripts/mods/HavocConditionManager/custom_efl_runtime")
local efl=base.custom_efl
local runtime=base.template_runtime
local registry=base.template_registry
local director=mods.HavocEnemyDirector;mods.HavocEnemyDirector=nil
base:set("native_configuration_v3",nil)
solo:set("havoc_mission","cm_archives")
solo:set("havoc_theme_circumstance","default")
local native_selected=Havoc.parse_data(Havoc.generate_havoc_data(40,1)).modifiers
for _,choice in ipairs(native_selected) do solo:set("havoc_modifier_"..choice.name,choice.level) end
local server=true
local function role(host,authority)
 server=authority
 if host=="player" then
  Managers.multiplayer_session=setmetatable({},{__index=LocalHostConnection})
 else
  Managers.multiplayer_session={host_type=function() return types[host] end}
 end
 Managers.state.game_session={is_server=function() return server end}
end
local function mission(rank,tier)
 assert(efl.set_tier(tier));efl.start()
 local extension,context,parsed=begin(rank)
 Managers.state.game_mode.game_mode_name=function() return "coop" end
 runtime.reset()
 return extension,context,parsed
end
local function root(id) return registry.by_id[id].root end
local function templates()
 return runtime.prepare(root("mutators/havoc_mutator_more_captains_02"),"mutators"),
  runtime.prepare(root("mutators/havoc_mutator_monster_specials_02"),"mutators"),
  runtime.prepare(root("hordes/mutator_horde/havoc_02"),"hordes")
end
local function stats(extension)
 local player=new_unit({})
 extension:_on_player_unit_spawned({player_unit=player})
 return player.stats,NativeHealth.max_health({_health=300,_buff_extension={stat_buffs=function() return player.stats end}})
end
local_host_results={}
for _,host in ipairs({"singleplay","player"}) do
 for _,rank in ipairs({40,60}) do
  role(host,true)
  local extension,context,parsed=mission(rank,4)
  -- Realms clones every launch-context field when queuing a next map.
  -- Preserve that actual boundary; it never needs a non-native rank RPC.
  Managers.mechanism._mechanism._context=table.clone(context)
  assert(solo.has_local_gameplay_authority() and solo.is_soloplay()==(host=="singleplay"))
  assert(parsed.havoc_rank==40 and efl.session().tier==4)
  assert((Rank.session()~=nil)==(rank>40))
  local values,hp=stats(extension)
  near(values.max_health_modifier,rank==40 and .65 or .65-20/60)
  near(values.toughness,rank==40 and -45 or -45-100/9)
  assert(hp==(rank==40 and 195 or 96))
  near(output.ammo,rank==40 and .4 or .4-20/120)
  local c,m,h=templates()
  near(c.modify_pacing.monsters_per_travel_distance[1],30)
  near(m.init_modify_pacing.specials_monster_spawn_config.chance_to_spawn_monster,.4)
  near(h.horde_timer_range[1],100*(100/140)^2)
  local_host_results[#local_host_results+1]={host_type=host,selected_rank=rank,native_rank=parsed.havoc_rank,
   selected_efl=4,is_soloplay=solo.is_soloplay(),authority=solo.has_local_gameplay_authority(),
   health_factor=values.max_health_modifier,health_base300=hp,toughness_delta=values.toughness,ammo=output.ammo,
   custom_rank_active=Rank.session()~=nil,custom_efl_active=efl.session()~=nil,
   captain_distance=Rules.copy(c.modify_pacing.monsters_per_travel_distance),
   monster_chance=m.init_modify_pacing.specials_monster_spawn_config.chance_to_spawn_monster,
   horde_interval=Rules.copy(h.horde_timer_range)}
  -- GameplayStateRun starts after modifier/template initialization.
  local before=Rules.copy(h)
  base.on_game_state_changed("enter","GameplayStateRun")
  assert(Rank.session() or rank==40);assert(efl.session().tier==4 and same(before,h))
  -- Repeated template requests and subsequent missions never stack scaling.
  for _=1,25 do assert(runtime.prepare(root("hordes/mutator_horde/havoc_02"),"hordes")==h) end
  base.on_game_state_changed("exit","GameplayStateRun")
  assert(Rank.session()==nil and efl.session()==nil and same(h,root("hordes/mutator_horde/havoc_02")))
 end
end
-- Native rank40/I/II also survive Realms; a later IV mission has fresh copies.
role("player",true)
for _,tier in ipairs({1,2,3,4,2,4}) do
 local extension,context=mission(40,tier)
 local values,hp=stats(extension);assert(hp==195)
 if tier<3 then assert(efl.session()==nil and context.hcm_custom_efl_v1==nil)
 else assert(efl.session().tier==tier) end
end
-- Negative controls execute the actual SoloPlay authority method, even when
-- the native extension and valid HCM launch metadata are otherwise present.
local role_checks=0
for _,case in ipairs({{"player",false},{"singleplay",false},{"mission_server",false},
 {"mission_server",true},{"hub_server",true},{"party",true}}) do
 role(case[1],case[2]);local extension=mission(60,4)
 assert(not solo.has_local_gameplay_authority() and Rank.session()==nil and efl.session()==nil)
 local c,m,h=templates()
 assert(c==root("mutators/havoc_mutator_more_captains_02") and m==root("mutators/havoc_mutator_monster_specials_02") and h==root("hordes/mutator_horde/havoc_02"))
 local values,hp=stats(extension);assert(hp==195);near(values.toughness,-45)
 role_checks=role_checks+1
end
role("player",true);mission(60,4)
Managers.multiplayer_session=nil;assert(not solo.has_local_gameplay_authority() and Rank.session()==nil and efl.session()==nil)
role("player",true);Managers.state.game_session=nil;assert(not solo.has_local_gameplay_authority() and Rank.session()==nil and efl.session()==nil)
-- Both launch entry points use this wrapper. Unsupported rooms keep the user's
-- selections, return normally, notify once, and never attach custom metadata.
local notify=base.notify;local messages={};base.notify=function(_,s) messages[#messages+1]=s end
local room_checks=0
for _,host in ipairs({"singleplay","player"}) do
 role(host,true)
 for _,name in ipairs({"om_basic_combat_01","tg_shooting_range"}) do
  for _,selection in ipairs({{60,4},{60,2},{40,4},{40,2}}) do
   solo:set("havoc_mission",name);assert(Rank.set(selection[1]) and efl.set_tier(selection[2]))
   local count=#messages;local ok,context=pcall(solo.gen_havoc_mission_context)
   assert(ok and type(context)=="table" and not context.hcm_custom_havoc_v1 and not context.hcm_custom_efl_v1)
   assert(Rank.get()==selection[1] and efl.get()==efl.rules.choices[selection[2]])
   local custom=selection[1]>40 or selection[2]>2
   assert(#messages-count==(custom and 1 or 0))
   if custom then assert(type(messages[#messages])=="string" and #messages[#messages]>0) end
   -- Even forged/reused metadata cannot activate a training-room extension.
   local parsed=Havoc.parse_data(context.havoc_data)
   context.hcm_custom_havoc_v1=Rules.capture(60,parsed.modifiers);context.hcm_custom_havoc_v1.native_data=context.havoc_data
   context.hcm_custom_efl_v1={version=1,tier=4,native_id=efl.rules.native_ii,native_data=context.havoc_data}
   Managers.mechanism={_mechanism={_context=context,_mechanism_data={havoc_data=context.havoc_data}}}
   Managers.state.difficulty={get_parsed_havoc_data=function() return parsed end}
   Rank.start();efl.start();assert(Rank.session()==nil and efl.session()==nil)
   room_checks=room_checks+1
  end
 end
end
base.notify=notify;solo:set("havoc_mission","cm_archives")
assert(efl.set_tier(2));efl.finish();runtime.reset();Rank.finish();Rank.start()
solo.has_local_gameplay_authority=local_host_saved.authority
solo.is_soloplay=local_host_saved.is_soloplay
solo.gen_havoc_mission_context=local_host_saved.generator
solo._havoc_condition_manager_context_wrapper=local_host_saved.native_generator
Managers.multiplayer_session=local_host_saved.multiplayer
Managers.state.game_session=local_host_saved.game_session
Managers.state.game_mode=local_host_saved.game_mode
mods.HavocEnemyDirector=director
local_host_role_checks=role_checks+2;local_host_room_checks=room_checks
''')

def local_host_json(value):
    if not hasattr(value, 'items'):
        return value
    items = dict(value.items())
    if items and set(items) == set(range(1, len(items) + 1)):
        return [local_host_json(items[i]) for i in range(1, len(items) + 1)]
    return {str(k): local_host_json(v) for k, v in items.items()}

(CHECKS / 'custom-local-host-results.json').write_text(json.dumps({
    'kind': 'offline_production_methods_and_native_consumers',
    'fixture_sha256': hashlib.sha256(local_host_fixture.read_bytes()).hexdigest(),
    'rows': local_host_json(L.globals().local_host_results),
    'rejected_role_cases': L.globals().local_host_role_checks,
    'safe_training_launch_cases': L.globals().local_host_room_checks,
    'limit': 'No live gameplay, network transport, navigation, actors or remote-client stat synchronization test.'
}, indent=2) + '\n', encoding='utf-8')
print('Local host regression: production SoloPlay2.6.9/Realms host type; rank40/60 native stats, EFLIV pacing, Run init/exit, native tiers, 8 unauthorized roles and 16 safe training launches: PASS')
