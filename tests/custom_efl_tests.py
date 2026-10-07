"""Custom EFL tiers against native templates, consumers, UI and installed HED."""
from pathlib import Path
import json, hashlib, platform
exec(Path(__file__).with_name('custom_havoc_rank_tests.py').read_text(encoding='utf-8'), globals())

L.execute('''
local base,solo=mods.HavocConditionManager,mods.SoloPlay
base.custom_efl=base:io_dofile("HavocConditionManager/scripts/mods/HavocConditionManager/custom_efl_runtime")
EFL=base.custom_efl;EF=EFL.rules;E=base.template_runtime;A=base.template_registry
assert(EFL.set("default"));base:set("native_configuration_v3",nil)
efl_director=mods.HavocEnemyDirector;mods.HavocEnemyDirector=nil
native_efl_before={}
for _,id in ipairs({"mutators/havoc_mutator_more_captains_01","mutators/havoc_mutator_more_captains_02",
 "mutators/havoc_mutator_monster_specials_01","mutators/havoc_mutator_monster_specials_02",
 "hordes/mutator_horde/havoc_01","hordes/mutator_horde/havoc_02"}) do native_efl_before[id]=Rules.copy(A.by_id[id].root) end
function efl_begin(rank,tier)
 EFL.start();assert(EFL.set_tier(tier));local extension,context,parsed=begin(rank)
 E.reset();return extension,context,parsed
end
function efl_root(id) return A.by_id[id].root end
function efl_templates()
 return E.prepare(efl_root("mutators/havoc_mutator_more_captains_02"),"mutators"),
 E.prepare(efl_root("mutators/havoc_mutator_monster_specials_02"),"mutators"),
 E.prepare(efl_root("hordes/mutator_horde/havoc_02"),"hordes")
end
local saved=Rules.copy(solo.values)
for _,bad in ipairs({0,5,1.5,math.huge,-math.huge,"3",false}) do assert(not EFL.set_tier(bad));assert(same(saved,solo.values)) end
assert(not EFL.set_tier(0/0) and not EFL.set("unknown"))
for _,bad in ipairs({{},true,{version=1,tier=5,native_id=EF.native_ii},{version=1,tier=3,native_id=EF.native_i},
 {version=1,tier=3,native_id=EF.native_ii,extra=true},setmetatable(EF.record(3),{})}) do assert(not EF.validate_record(bad)) end
for rank=1,60 do
 for tier=1,4 do
  local _,context,parsed=efl_begin(rank,tier)
  assert(Rank.get()==rank and solo:get("havoc_difficulty")==math.min(rank,40))
  local expected=tier==1 and EF.native_i or EF.native_ii
  local n=0;for _,id in ipairs(parsed.circumstances) do if id==expected then n=n+1 end;assert(id~=EF.choices[3] and id~=EF.choices[4]) end
  assert(n==1 and solo:get("havoc_difficulty_circumstance")==expected)
  assert(EFL.get()==EF.choices[tier])
  if tier<=2 then
   assert(context.hcm_custom_efl_v1==nil and EFL.session()==nil)
   for id in pairs(native_efl_before) do assert(E.prepare(efl_root(id),A.by_id[id].family)==efl_root(id)) end
  else
   assert(context.hcm_custom_efl_v1.tier==tier and EFL.session().tier==tier)
   assert(not E.config().changed,"Custom EFL must work with default coarse/fine settings")
   local captain,monster,horde=efl_templates()
   local c0=efl_root("mutators/havoc_mutator_more_captains_02")
   local m0=efl_root("mutators/havoc_mutator_monster_specials_02")
   local h0=efl_root("hordes/mutator_horde/havoc_02")
   local c=captain.modify_pacing.monsters_per_travel_distance
   local m=monster.init_modify_pacing.specials_monster_spawn_config
   local h=horde.horde_timer_range
   for i=1,2 do
    near(c[i],c0.modify_pacing.monsters_per_travel_distance[i]*(c0.modify_pacing.monsters_per_travel_distance[i]/efl_root("mutators/havoc_mutator_more_captains_01").modify_pacing.monsters_per_travel_distance[i])^(tier-2))
    near(m.max_monster_duration[i],m0.init_modify_pacing.specials_monster_spawn_config.max_monster_duration[i]*(m0.init_modify_pacing.specials_monster_spawn_config.max_monster_duration[i]/efl_root("mutators/havoc_mutator_monster_specials_01").init_modify_pacing.specials_monster_spawn_config.max_monster_duration[i])^(tier-2))
    near(h[i],h0.horde_timer_range[i]*(h0.horde_timer_range[i]/efl_root("hordes/mutator_horde/havoc_01").horde_timer_range[i])^(tier-2))
   end
   near(m.chance_to_spawn_monster,.1*2^(tier-2))
   for _,r in ipairs({c,m.max_monster_duration,h}) do assert(r[1]>0 and r[1]<=r[2] and r[2]<math.huge) end
   assert(m.max_monsters==1 and m.health_modifiers.chaos_spawn==.4 and #m.breeds==3)
   assert(horde.max_active_minions==110 and horde.time_between_waves==7)
   local cc,mc,hc=Rules.copy(captain),Rules.copy(monster),Rules.copy(horde)
   cc.modify_pacing.monsters_per_travel_distance=Rules.copy(c0.modify_pacing.monsters_per_travel_distance)
   mc.init_modify_pacing.specials_monster_spawn_config.chance_to_spawn_monster=.1
   mc.init_modify_pacing.specials_monster_spawn_config.max_monster_duration=Rules.copy(m0.init_modify_pacing.specials_monster_spawn_config.max_monster_duration)
   hc.horde_timer_range=Rules.copy(h0.horde_timer_range)
   assert(same(cc,c0) and same(mc,m0) and same(hc,h0),"Only four pacing paths may change")
   for _=1,20 do assert(E.prepare(c0,"mutators")==captain and E.prepare(captain,"mutators")==captain and E.prepare(m,"mutators")==m and E.prepare(h0,"hordes")==horde) end
   assert(EFL.set_tier(tier==3 and 4 or 3));assert(EFL.session().tier==tier,"Active mission must retain its launch tier")
   EFL.finish();assert(EFL.session()==nil)
   assert(same(captain,c0) and same(monster,m0) and same(horde,h0))
  end
 end
end
for id,before in pairs(native_efl_before) do assert(same(before,efl_root(id)),id) end
-- Context provenance, multiplayer/client gates and unsupported mission refusal.
local _,context,parsed=efl_begin(40,3)
singleplay=false;assert(EFL.session()==nil);singleplay=true
local authority=base.has_local_gameplay_authority;base.has_local_gameplay_authority=function() return false end
assert(EFL.session()==nil);base.has_local_gameplay_authority=authority
EFL.start();context.hcm_custom_efl_v1.tier=5;assert(EFL.session()==nil)
_,context,parsed=efl_begin(60,4);EFL.start();Managers.mechanism._mechanism._mechanism_data.havoc_data="different";assert(EFL.session()==nil)
_,context,parsed=efl_begin(40,3);EFL.start();parsed.mission="another_mission";assert(EFL.session()==nil)
assert(not EF.native_ii_only({circumstances={EF.native_i,EF.native_ii}}))
assert(not EF.native_ii_only({circumstances={EF.native_ii,EF.native_ii}}))
assert(not EF.native_ii_only({circumstances={EF.choices[3]}}))
solo:set("havoc_mission","tg_shooting_range");assert(EFL.set_tier(3));assert(not pcall(solo.gen_havoc_mission_context))
solo:set("havoc_mission","cm_archives")
assert(EFL.set_tier(3));solo:set("havoc_difficulty_circumstance",EF.native_ii)
assert(EFL.get()==EF.native_ii and base:get(EF.storage_key)==nil)
-- Existing coarse/fine values are the private baseline, never scaled twice.
efl_begin(40,3);base:set("native_configuration_v3",{horde_frequency=2});E.reset()
local raw=efl_root("hordes/mutator_horde/havoc_02")
local baseline=base.template_schema.apply(raw,"hordes",E.config().coarse,nil,A.breeds,A.by_table)
local prepared=E.prepare(raw,"hordes")
near(prepared.horde_timer_range[1],baseline.horde_timer_range[1]*(100/140))
near(prepared.time_between_waves,baseline.time_between_waves)
EFL.finish();assert(same(prepared,baseline));base:set("native_configuration_v3",nil)
local root=efl_root("mutators/havoc_mutator_monster_specials_02")
local edited=Rules.copy(root);local config=edited.init_modify_pacing.specials_monster_spawn_config
config.chance_to_spawn_monster=.8;config.max_monster_duration={30,60}
local custom,restore=EF.prepare(root,edited,A.by_id["mutators/havoc_mutator_monster_specials_02"],A,4)
assert(custom.init_modify_pacing.specials_monster_spawn_config.chance_to_spawn_monster==1)
restore();assert(same(custom,edited) and config.chance_to_spawn_monster==.8)
-- EFL-only preparation skips the coarse compiler and touches just three roots.
efl_begin(40,3)
local prepare,apply=EF.prepare,base.template_schema.apply
local builds,coarse_calls=0,0
EF.prepare=function(...) builds=builds+1;return prepare(...) end
base.template_schema.apply=function(...) coarse_calls=coarse_calls+1;return apply(...) end
local c,m,h=efl_templates()
for _=1,10000 do local cc,mm,hh=efl_templates();assert(cc==c and mm==m and hh==h) end
for id in pairs(native_efl_before) do if not EF.targets[id] then assert(E.prepare(efl_root(id),A.by_id[id].family)==efl_root(id)) end end
assert(builds==3 and coarse_calls==0)
efl_compile_counts={fresh_roots=3,repeated_root_calls=30000,custom_clone_builds=builds,coarse_compiler_calls=coarse_calls}
EF.prepare=prepare;base.template_schema.apply=apply;EFL.finish()
-- Root condition gates follow the final EFL clone and survive its retirement.
efl_begin(40,3)
mods.HavocEnemyDirector={is_gameplay_enabled=function() return true end,get_config=function()
 return {version=2,patches={},rules={["hordes/mutator_horde/havoc_02"]={encounter={mode="append",match="all",clauses={{condition="load_max",value=20}}}}}}
end}
E.reset();local context=E.context;E.context=function() return {load=30} end
local gated=E.prepare(efl_root("hordes/mutator_horde/havoc_02"),"hordes")
assert(E.has_gate(gated) and not E.allowed(gated))
EFL.finish();assert(E.has_gate(gated) and not E.allowed(gated))
E.context=context;mods.HavocEnemyDirector=nil;E.reset()
print("Custom EFL: all ranks1-60 x tiersI-IV, four exact curves, native I/II identity, unchanged II remainder, no cumulative scaling/shared mutation, invalid metadata and launch/authority gates: PASS")
''')

# Execute native callback bodies. Physics/rendering, asset loading and navigation
# stay explicit boundaries; scheduling and eligibility bodies execute unchanged.
sources = {
 'pacing': GAME/'scripts/managers/pacing/pacing_manager.lua',
 'special': GAME/'scripts/managers/pacing/specials_pacing/specials_pacing.lua',
 'monster': GAME/'scripts/managers/pacing/monster_pacing/monster_pacing.lua',
 'horde': GAME/'scripts/managers/pacing/horde_pacing/horde_pacing.lua',
 'modify': GAME/'scripts/managers/mutator/mutators/mutator_modify_pacing.lua',
 'override': GAME/'scripts/managers/mutator/mutators/mutator_horde_pacing_overrides.lua',
}
L.execute('''
NP={};NS={};NM={};NH={};NModify={};NOverride={}
function efl_hook(target,name,fn,self,...)
 for _,hook in ipairs(hooks) do if hook.owner==mods.HavocConditionManager and hook.target==target and hook.name==name then return hook.fn(fn,self,...) end end
 error("Missing native hook "..name)
end
local function base_init(self,is_server,delegate,template) self._is_server=is_server;self._template=template end
local function init(self,...) return efl_hook(require("scripts/managers/mutator/mutators/mutator_base"),"init",base_init,self,...) end
NModify.super={init=init};NOverride.super={init=init}
''')
L.execute('local PacingManager=NP;'+ '\n'.join(method(sources['pacing'].read_text(encoding='utf-8-sig'),'PacingManager',n) for n in ('add_pacing_modifiers','override_horde_pacing','get_horde_pacing_override_tempate')))
L.execute('local Breeds=require("scripts/settings/breed/breeds");local SpecialsPacing=NS;'+ '\n'.join(method(sources['special'].read_text(encoding='utf-8-sig'),'SpecialsPacing',n) for n in ('set_monster_spawn_config','_start_monster_cooldown','_check_monster_override')))
L.execute('local MonsterPacing=NM;'+method(sources['monster'].read_text(encoding='utf-8-sig'),'MonsterPacing','fill_spawns_by_travel_distance'))
L.execute('local HordeTemplates=require("scripts/managers/horde/horde_templates");local HordePacing=NH;'+ '\n'.join(method(sources['horde'].read_text(encoding='utf-8-sig'),'HordePacing',n) for n in ('on_gameplay_post_init','_setup_next_horde','add_trickle_horde')))
L.execute('local MutatorModifyPacing=NModify;'+ '\n'.join(method(sources['modify'].read_text(encoding='utf-8-sig'),'MutatorModifyPacing',n) for n in ('init','on_gameplay_post_init')))
L.execute('local HordePacingTemplates=require("scripts/managers/pacing/horde_pacing/horde_pacing_templates");local MutatorHordePacingOverride=NOverride;'+method(sources['override'].read_text(encoding='utf-8-sig'),'MutatorHordePacingOverride','init'))
L.execute('''
function table.clear(t) for k in pairs(t) do t[k]=nil end end
local draw=.15;local random=math.random;math.random=function(a,b) if a then return a end;return draw end
efl_workload={}
for tier=1,4 do
 efl_begin(40,tier)
 local suffix=tier==1 and "01" or "02"
 local monster=setmetatable({_monsters={},_spawn_type_point_sections={captains={}}},{__index=NM})
 local section={};for i=1,180 do section[i]={spawn_travel_distance=i*20,position={i}} end
 monster._spawn_type_point_sections.captains[1]=section
 local special=setmetatable({_specials_slots={{}},_get_special_slot_breed_name=function() end},{__index=NS})
 special.set_monster_spawn_config=function(self,config) return efl_hook(require("scripts/managers/pacing/specials_pacing/specials_pacing"),"set_monster_spawn_config",NS.set_monster_spawn_config,self,config) end
 local pacing=setmetatable({_monster_pacing=monster,_specials_pacing=special},{__index=NP})
 pacing.get_horde_pacing_override_tempate=function(self) return efl_hook(require("scripts/managers/pacing/pacing_manager"),"get_horde_pacing_override_tempate",NP.get_horde_pacing_override_tempate,self) end
 Managers.state.pacing=pacing;Managers.state.mutator=nil
 local captain=setmetatable({},{__index=NModify})
 NModify.init(captain,true,nil,efl_root("mutators/havoc_mutator_more_captains_"..suffix))
 NModify.on_gameplay_post_init(captain)
 local replacement=setmetatable({},{__index=NModify})
 NModify.init(replacement,true,nil,efl_root("mutators/havoc_mutator_monster_specials_"..suffix))
 local override=setmetatable({},{__index=NOverride})
 NOverride.init(override,true,nil,efl_root("mutators/mutator_havoc_override_horde_pacing_"..suffix))
 assert(special._monster_spawn_config==replacement._template.init_modify_pacing.specials_monster_spawn_config)
 Managers.state.mutator={mutator=function() end};Managers.state.minion_spawn={num_spawned_minions=function() return 0 end}
 local horde=setmetatable({_timer_modifier=1,_init_coordinated_horde_strikes=function() end},{__index=NH})
 efl_hook(require("scripts/managers/pacing/horde_pacing/horde_pacing"),"on_gameplay_post_init",NH.on_gameplay_post_init,horde,nil,efl_root("hordes/mutator_horde/havoc_"..suffix))
 local before_config=Rules.copy(special._monster_spawn_config);local before_horde=Rules.copy(horde._template)
 mods.HavocConditionManager.on_game_state_changed("enter","GameplayStateRun")
 assert(same(before_config,special._monster_spawn_config) and same(before_horde,horde._template),"Run enter must preserve Init-owned EFL templates")
 local interval=horde._next_horde_at;local hordes=0;local time=0
 while time+interval<=3600 do time=time+interval;hordes=hordes+1;NH._setup_next_horde(horde,horde._template);interval=horde._next_horde_at end
 local attempts,successes=0,0;Managers.state.terror_event={num_active_events=function() return 0 end}
 for t=0,3599 do
  Managers.time={time=function() return t end};attempts=attempts+1
  local breed,hp=NS._check_monster_override(special,{})
  if breed then successes=successes+1;assert(hp==.4) end
 end
 -- The native slot cap and cooldown still refuse a reserved monster.
 special._max_monster_duration=nil;special._get_special_slot_breed_name=function() return "chaos_spawn" end
 draw=.01;assert(NS._check_monster_override(special,{})==nil and special._max_monster_duration>3599);draw=.15
 local config=special._monster_spawn_config;local deadline=special._max_monster_duration
 local plan=#monster._monsters;local horde_deadline=horde._next_horde_at
 efl_workload[tier]={tier=tier,route_meters=3600,captain_plan_points=plan,slot_checks=attempts,monster_replacements=successes,horde_schedules_within_horizon=hordes,horde_timer_draws=hordes+1,horde_midpoint_seconds=interval}
 EFL.finish()
 assert(#monster._monsters==plan and special._max_monster_duration==deadline and horde._next_horde_at==horde_deadline)
 assert(same(config,efl_root("mutators/havoc_mutator_monster_specials_"..suffix).init_modify_pacing.specials_monster_spawn_config))
 assert(same(horde._template,efl_root("hordes/mutator_horde/havoc_"..suffix)))
end
math.random=random
assert(efl_workload[3].captain_plan_points>efl_workload[2].captain_plan_points and efl_workload[4].captain_plan_points>efl_workload[3].captain_plan_points)
assert(efl_workload[4].horde_timer_draws>efl_workload[3].horde_timer_draws and efl_workload[3].horde_timer_draws>efl_workload[2].horde_timer_draws)
print("Native consumers: mutator init/post-init, captain plan, II horde override/first draw, monster eligibility/slot cap/cooldown and alias cleanup, including unpublished mutator manager: PASS")
''')

# Actual dropdown reopen and native rank/Randomize callbacks, with rendering stubbed.
view_text=(SOURCES/'HavocConditionManager/scripts/mods/HavocConditionManager/condition_manager_view/condition_manager_view.lua').read_text(encoding='utf-8-sig')
getter=view_text[view_text.index('local addon_setting_keys'):view_text.index('HavocConditionManagerView = class')]
L.execute('''
EFLView=setmetatable({},{__index=RankView});local HavocConditionManagerView=EFLView
local mod,base_mod=mods.HavocConditionManager,mods.SoloPlay
local SoloPlaySettings=mod._condition_ui_settings
SoloPlaySettings.order.havoc_difficulty_circumstances={EFL.rules.native_i,EFL.rules.native_ii}
SoloPlaySettings.loc.havoc_circumstances[EFL.rules.native_i]="EFL I"
SoloPlaySettings.loc.havoc_circumstances[EFL.rules.native_ii]="EFL II"
local make_options=mod:io_dofile("HavocConditionManager/scripts/mods/HavocConditionManager/condition_manager_view/make_options")
local view_settings=mod:io_dofile("HavocConditionManager/scripts/mods/HavocConditionManager/condition_manager_view/condition_manager_view_settings")
'''+getter+'\n'+'\n'.join(method(view_text,'HavocConditionManagerView',n) for n in ('_recreate_dropdown','_load_dropdown_selection','_build_dropdown_definition')))
L.execute('''
local base,solo=mods.HavocConditionManager,mods.SoloPlay
local view=setmetatable({_current={},_current_modifier={},_modifier_customizable=false,_options={},_dropdown_widgets={}},{__index=EFLView})
view._create_widget=function(_,name,definition) return definition end
view._persist_havoc_circumstances=function() end;view._refresh_condition_dropdowns=function() end
view._setup_dropdown=function(_,definition) return definition end
local recreate=EFLView._recreate_dropdown
view._recreate_dropdown=function(self,id) if id=="havoc_difficulty_circumstance" then return recreate(self,id) end end
solo:set("havoc_difficulty_circumstance",nil);base:set(EF.storage_key,nil)
view:_recreate_dropdown("havoc_difficulty_circumstance");assert(EFL.get()==EF.native_i)
for tier=1,4 do
 local dropdown=view:_build_dropdown_definition("havoc_difficulty_circumstance")
 dropdown.on_activated(EF.choices[tier],dropdown);view:_recreate_dropdown("havoc_difficulty_circumstance")
 assert(view._current.havoc_difficulty_circumstance==EF.choices[tier] and #view._options.havoc_difficulty_circumstance==5)
 local seen={};for _,option in ipairs(view._options.havoc_difficulty_circumstance) do assert(not seen[option.value]);seen[option.value]=true end
end
view:_setup_havoc_difficulty();local entry=view._havoc_difficulty_slider_widget.content.entry
entry.on_activated(40,entry);assert(EFL.get()==EF.choices[4])
entry.on_activated(60,entry);assert(EFL.get()==EF.choices[4])
view:_regen_havoc();assert(EFL.get()==EF.native_ii and base:get(EF.storage_key)==nil)
for _,lang in ipairs({"en","zh-cn","zh-tw"}) do test_language=lang;assert(base:localize("hcm_efl_3")~="hcm_efl_3" and base:localize("hcm_efl_4")~="hcm_efl_4") end
test_language="en"
-- Repeated reopen does not accumulate tier metadata or apply both circumstances.
assert(EFL.set_tier(3));for _=1,25 do
 local fresh=setmetatable({},{__index=EFLView});View.init(fresh,{})
 fresh._setup_dropdown=view._setup_dropdown;fresh:_recreate_dropdown("havoc_difficulty_circumstance")
 assert(EFL.get()==EF.choices[3] and fresh._current.havoc_difficulty_circumstance==EF.choices[3])
end
efl_view=view
print("Actual EFL UI: None plus exclusive I-IV, first-open I, 25 reopens, rank40/60 preserves manual choice, Randomize returns native generated tier, English/Chinese labels: PASS")
''')

L.execute('''
local base,solo=mods.HavocConditionManager,mods.SoloPlay
mods.HavocEnemyDirector=efl_director;local D=efl_director
Managers.state.game_mode={game_mode_name=function() return "hub" end};EFL.start();Rank.finish();Rank.start()
assert(Rank.install_presets())
for _,rank in ipairs({16,40,50,60}) do for tier=3,4 do
 assert(Rank.set(rank) and EFL.set_tier(tier))
 local doc=assert(D.presets.capture("EFL roundtrip"))
 assert(doc.hcm_custom_efl_v1.tier==tier and doc.hcm.difficulty==EF.native_ii)
 assert((rank>40)==(doc.hcm_custom_havoc_v1~=nil))
 local decoded=assert(D.presets.decode(cjson.encode(doc)));assert(same(doc,decoded))
 assert(EFL.set_tier(1));assert(D.presets.apply(decoded,efl_view))
 assert(EFL.get()==EF.choices[tier] and efl_view._current.havoc_difficulty_circumstance==EF.choices[tier])
 assert(D.studio_capture_context().document.hcm_custom_efl_v1.tier==tier)
 local previous=complete_state()
 for _,mutate in ipairs({function(v) v.hcm_custom_efl_v1.tier=5 end,function(v) v.hcm_custom_efl_v1.tier=0/0 end,
  function(v) v.hcm_custom_efl_v1.extra=true end,function(v) v.hcm.difficulty=EF.native_i end}) do
  local bad=Rules.copy(doc);mutate(bad);assert(not D.presets.apply(bad,efl_view));assert(same(previous,complete_state()))
 end
 local legacy=Rules.copy(doc);legacy.hcm_custom_efl_v1=nil
 assert(D.presets.codec.validate(legacy) and EFL.get()==EF.choices[tier])
 assert(D.presets.apply(legacy,efl_view) and EFL.get()==EF.native_ii and base:get(EF.storage_key)==nil)
end end
assert(D.set_studio_mode("hcm"));assert(Rank.set(16) and EFL.set_tier(3))
assert(D.set_studio_mode("hed"));assert(EFL.set_tier(4))
assert(D.set_studio_mode("hcm") and EFL.get()==EF.choices[3])
assert(D.set_studio_mode("hed") and EFL.get()==EF.choices[4])
local modes=base:get(EF.mode_key);base:set(EF.mode_key,{hed={version=1,tier=5,native_id=EF.native_ii}})
local previous=complete_state();assert(not D.set_studio_mode("hcm"));assert(same(previous,complete_state()));base:set(EF.mode_key,modes)
-- Fault after native apply and after mode writes: restore owned keys and display.
assert(Rank.set(60) and EFL.set_tier(3));local doc=assert(D.presets.capture("rollback"))
assert(EFL.set_tier(4));efl_view:_recreate_dropdown("havoc_difficulty_circumstance")
local old_set=base.set;local fail=true
base.set=function(self,key,value,...)
 if key==EF.storage_key and value and value.tier==3 and fail then fail=false;error("EFL owned write fault") end
 return old_set(self,key,value,...)
end
previous=complete_state();local ui=Rules.copy(efl_view._current)
assert(not pcall(D.presets.apply,doc,efl_view));assert(same(previous,complete_state()) and same(ui,efl_view._current))
base.set=old_set
local current=D.studio_mode();local target=current=="hed" and "hcm" or "hed"
fail=true;base.set=function(self,key,value,...)
 if key==EF.mode_key and fail then fail=false;error("EFL mode write fault") end
 return old_set(self,key,value,...)
end
previous=complete_state();assert(not pcall(D.set_studio_mode,target));assert(same(previous,complete_state()));base.set=old_set
-- Optional API appearance uses the existing identity-aware bridge for EFL too.
Rank.uninstall_presets();local capture=D.studio_capture_context;D.studio_capture_context=nil
assert(Rank.install_presets());D.studio_capture_context=capture;assert(Rank.install_presets())
assert(D.studio_capture_context().document.hcm_custom_efl_v1.tier==4)
local current_capture=D.studio_capture_context;assert(Rank.install_presets() and current_capture==D.studio_capture_context)
local held_capture=D.presets.capture;local held_studio=D.studio_capture_context
base._enabled=false;base.on_disabled(false)
assert(held_capture("disabled").hcm_custom_efl_v1==nil and held_studio().document.hcm_custom_efl_v1==nil)
base._enabled=true;base.on_enabled(false)
assert(D.presets.capture("enabled").hcm_custom_efl_v1.tier==4)
held_capture=D.presets.capture;held_studio=D.studio_capture_context
base.on_unload(false)
assert(held_capture("unloaded").hcm_custom_efl_v1==nil and held_studio().document.hcm_custom_efl_v1==nil)
base.custom_efl=base:io_dofile("HavocConditionManager/scripts/mods/HavocConditionManager/custom_efl_runtime");EFL=base.custom_efl
print("Actual installed HED: EFL III/IV JSON/capture/apply at ranks16/40/50/60, legacy records, native II identity, malformed context, independent mode slots, post-write rollback/UI and late API idempotency: PASS")
''')

L.execute('''
local base,solo=mods.HavocConditionManager,mods.SoloPlay
mods.HavocEnemyDirector=nil;efl_begin(60,4);local captain,monster,horde=efl_templates()
base._enabled=false;base.on_disabled(false)
assert(EFL.session()==nil and same(horde,efl_root("hordes/mutator_horde/havoc_02")))
base._enabled=true;base.on_enabled(false);assert(EFL.session()==nil)
efl_begin(40,3);captain,monster,horde=efl_templates();assert(EFL.set_tier(2))
assert(EFL.session()==nil and same(horde,efl_root("hordes/mutator_horde/havoc_02")))
efl_begin(60,4);captain,monster,horde=efl_templates();base.on_game_state_changed("exit","GameplayStateRun")
assert(EFL.session()==nil and same(horde,efl_root("hordes/mutator_horde/havoc_02")))
efl_begin(60,3);captain,monster,horde=efl_templates()
local old=EFL;local wrapped=solo.set;local calls=0
local foreign=function(...) calls=calls+1;return wrapped(...) end;solo.set=foreign
base.on_unload(false);assert(solo.set==foreign and old.session()==nil)
base.custom_efl=base:io_dofile("HavocConditionManager/scripts/mods/HavocConditionManager/custom_efl_runtime")
EFL=base.custom_efl;assert(EFL.set_tier(4));local before=calls
solo:set("havoc_difficulty_circumstance",EF.native_ii)
assert(calls==before+1 and EFL.get()==EF.native_ii and base:get(EF.storage_key)==nil)
efl_begin(40,4);captain,monster,horde=efl_templates();EFL.unload()
assert(EFL.session()==nil and same(horde,efl_root("hordes/mutator_horde/havoc_02")))
for id,before in pairs(native_efl_before) do assert(same(before,efl_root(id))) end
print("EFL lifecycle: tierII, disable/re-enable, mission exit, reload/unload, foreign setter ownership, no stale observer or shared mutations: PASS")
''')

report = dict(kind='offline_native_callback_workload', game_source='7e662fcda16219d775b84af50322be2e9cd9d62e',
 python=platform.python_version(), lua=L.eval('_VERSION'),
 workload='One 3600m route with 180 evenly spaced captain points; 3600 one-second special-slot checks; 3600s horde horizon. Midpoint range draws, first-index choices, probability draw .15, no terror events, no occupied monster slots except final cap assertion with draw .01.',
 rows=json_value(L.globals().efl_workload),compiler_calls=json_value(L.globals().efl_compile_counts), native_consumer_sha256={k:hashlib.sha256(p.read_bytes()).hexdigest() for k,p in sources.items()},
 limitation='Synthetic Lua callbacks, no navigation/physics/actors/frame timings. Counts are scheduling candidates, not guaranteed spawns or FPS. Unchanged native slot cap and cooldown checks execute. Already scheduled deadlines/captain plans remain native-owned on cleanup.')
(CHECKS/'custom-efl-workload.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report['rows'],indent=2))
