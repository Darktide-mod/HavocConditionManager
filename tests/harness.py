from pathlib import Path
import sys,re,json
work=Path(__file__).resolve().parent
sys.excepthook=lambda typ,value,tb: print(typ.__name__+': '+str(value))
from project_env import PROJECT, GAME, FIXTURES, CHECKS, SOURCES
from isolated_diy_io import isolate
isolate()
from lupa.luajit21 import LuaRuntime
L=LuaRuntime(unpack_returned_tuples=True)
stage=SOURCES; game=GAME
L.execute('''
function settings(_,value) return value end
function table.clone(t) local r={} for k,v in pairs(t or {}) do r[k]=v end return r end
function table.clone_instance(t)
    if type(t)~="table" then return t end
    local r={} for k,v in pairs(t) do r[k]=table.clone_instance(v) end return r
end
function table.merge(a,b) for k,v in pairs(b) do a[k]=v end return a end
function table.merge_recursive(a,b)
    for k,v in pairs(b) do
        if type(v)=="table" and type(a[k])=="table" then table.merge_recursive(a[k],v) else a[k]=table.clone_instance(v) end
    end
    return a
end
function table.merge_recursive_advanced(a,b) return table.merge_recursive(a,b),{} end\nfunction table.enum(...) local r={} for _,s in ipairs({...}) do r[s]=s end return r end
function table.keys(t) local r={} for k in pairs(t) do r[#r+1]=k end return r end
table.enum_id=table.enum
function table.array_contains(t,v) for _,x in ipairs(t) do if x==v then return true end end return false end
function math.clamp(n,a,b) return math.max(a,math.min(n,b)) end
function math.lerp(a,b,t) return a+(b-a)*t end
function math.round(n) return math.floor(n+0.5) end
function math.random_range(a,b) return (a+b)/2 end
function Localize(s)
    local strings=mods and mods.HavocConditionManager and mods.HavocConditionManager.global_localization
    return strings and strings[s] and (strings[s][test_language or "zh-cn"] or strings[s].en) or s
end
Managers={state={}}
Script={new_map=function() return {} end,new_array=function() return {} end}
CLASS={HudElementBossHealth={}}
Application={user_setting=function() return {} end}
mods={}; hooks={}; classes={}; warnings={}
function get_mod(name) return mods[name] end
function new_test_mod(name)
    local m={_settings={},values={},localization={}}
    function m:get(k) return self.values[k] end
    function m:set(k,v) self.values[k]=table.clone_instance(v) end
    function m:is_enabled() return self._enabled~=false end
    function m:enable_all_hooks() self._hooks_enabled=true end
    function m:disable_all_hooks() self._hooks_enabled=false end
    -- DMF always formats translated text, including calls without arguments.
    function m:localize(k,...) local v=self.localization[k]; local s=v and (v[test_language or "zh-cn"] or v.en) or k; return string.format(s,...) end
    function m:io_dofile(p) return load_mod_file(p) end
    function m:add_global_localize_strings(t) self.global_localization=self.global_localization or {}; for k,v in pairs(t) do self.global_localization[k]=v end end
    function m:hook(target,name,fn) hooks[#hooks+1]={target=target,name=name,fn=fn,owner=self,safe=false} end
    function m:hook_safe(target,name,fn) hooks[#hooks+1]={target=target,name=name,fn=fn,owner=self,safe=true} end
    function m:hook_require(path,fn) hooks[#hooks+1]={path=path,fn=fn,owner=self,require_hook=true} end
    function m:info(...) end
    function m:warning(...) warnings[#warnings+1]={...} end
    function m:error(...) error(string.format(...)) end
    function m:add_require_path(...) end
    function m:register_view(...) end
    function m:notify(...) end
    mods[name]=m
    return m
end
''')
def lua_file(path): return L.execute(path.read_text(encoding='utf-8-sig'),name='@'+str(path))
def load_mod(p): return lua_file(stage/(p+'.lua'))
L.globals().load_mod_file=load_mod
cache={'bit':L.eval("require('bit')"),'ffi':L.eval("require('ffi')")}
def tbl(x):
    if isinstance(x,dict): return L.table_from({k:tbl(v) for k,v in x.items()})
    if isinstance(x,list): return L.table_from([tbl(v) for v in x])
    return x
breeds={}
for p in (game/'scripts/settings/breed/breeds').rglob('*_breed.lua'):
    s=p.read_text(encoding='utf-8'); tags=re.search(r'\btags\s*=\s*\{(.*?)\}',s,re.S)
    if not tags: continue
    name=p.stem.removesuffix('_breed')
    kind=re.search(r'breed_type\s*=\s*breed_types\.(\w+)',s)
    breeds[name]={'name':name,'breed_type':kind.group(1) if kind else 'minion',
        'airbound':bool(re.search(r'airbound\s*=\s*true',s)),
        'can_patrol':bool(re.search(r'can_patrol\s*=\s*true',s)),
        'sub_faction_name':(re.search(r'sub_faction_name\s*=\s*"(\w+)"',s).group(1) if re.search(r'sub_faction_name\s*=\s*"(\w+)"',s) else None),
        'can_be_used_for_all_factions':bool(re.search(r'can_be_used_for_all_factions\s*=\s*true',s)),
        'tags':{k:True for k in re.findall(r'(\w+)\s*=\s*true',tags.group(1))},'display_name':name}
cache['scripts/settings/breed/breeds']=tbl(breeds)
cache['scripts/settings/roamer/roamer_slot_placement_functions']=tbl({})
cache['scripts/managers/horde/horde_templates']=tbl({n:{'name':n} for n in ('trickle_horde','ambush_horde','far_vector_horde','flood_horde','far_distance_horde')})
cache['scripts/utilities/attack/player_unit_status']=tbl({})
cache['scripts/utilities/breed_queries']=L.eval('{minion_breeds_by_name=function() return require("scripts/settings/breed/breeds") end}')
cache['scripts/settings/perception/perception_settings']=tbl({'aggro_states':{'aggroed':'aggroed','passive':'passive'}})
cache['scripts/managers/mutator/mutators/mutator_spawner/mutator_spawner_node']=tbl({'SINGLE_PLACEMENT':1,'CIRCLE_PLACEMENT':2})
cache['scripts/managers/mutator/mutators/mutator_spawner/mutator_spawner_location_sources']=L.eval('{prebaked_mission_locations=function() return {} end, mission_provided_gizmo=function() return {} end}')
cache['scripts/settings/components/enemy_event_spawner_settings']=tbl({'nurgle_totem':{}})
cache['scripts/network_lookup/network_lookup']=tbl({'buff_templates':{},'circumstance_templates':{}})
# Reproduce the engine's missing-key error instead of using permissive plain tables.
network_source=(game/'scripts/network_lookup/network_lookup.lua').read_text(encoding='utf-8-sig')
lookup_init=network_source.split('local function _init(name, lookup_table)',1)[1].split('\nend',1)[0]
L.execute('table.dump=function() end')
init_lookup=L.execute('return function(name,lookup_table)'+lookup_init+'\nend')
for lookup_name,lookup_table in cache['scripts/network_lookup/network_lookup'].items():
    init_lookup(lookup_name,lookup_table)

cache['scripts/settings/buff/buff_templates']=tbl({'NON_PREDICTED':{},'mutator_minion_nurgle_blessing_tougher':{'name':'mutator_minion_nurgle_blessing_tougher'}})
cache['scripts/utilities/loaded_dice']=L.eval('{create=function() return {},{} end}')
cache['scripts/managers/ui/ui_widget']=L.eval('''{create_definition=function(passes,node,content,size)
    local d={passes=passes,scenegraph_id=node,content=table.clone_instance(content or {}),style={},size=size}
    for _,p in ipairs(passes) do
        if p.style_id then d.style[p.style_id]=table.clone_instance(p.style or {}) end
        if p.value_id and p.value then d.content[p.value_id]=p.value end
        if p.content_id then d.content[p.content_id]={} end
    end
    return d
end}''')
real_roots=('scripts/managers/pacing/utilities/','scripts/managers/pacing/templates/','scripts/managers/pacing/roamer_pacing/templates/',
    'scripts/managers/pacing/specials_pacing/templates/','scripts/managers/pacing/monster_pacing/templates/',
    'scripts/managers/pacing/horde_pacing/templates/','scripts/managers/pacing/horde_pacing/compositions/',
    'scripts/settings/roamer/','scripts/settings/mutator/templates/','scripts/settings/havoc/','scripts/settings/circumstance/')
real_files={'scripts/managers/pacing/pacing_templates','scripts/managers/pacing/horde_pacing/horde_compositions',
    'scripts/managers/pacing/monster_pacing/boss_patrols','scripts/settings/horde/horde_settings','scripts/settings/buff/buff_settings',
    'scripts/settings/havoc_settings','scripts/settings/circumstance/templates/havoc_circumstance_template'}
class_paths={}
def require(path):
    if path in cache: return cache[path]
    f=game/(path+'.lua')
    if (path in real_files or path.startswith(real_roots) or path.endswith('_pacing_templates')) and f.exists():
        value=lua_file(f); cache[path]=value; return value
    if path in ['scripts/managers/pacing/pacing_manager','scripts/managers/pacing/roamer_pacing/roamer_pacing',
        'scripts/managers/pacing/horde_pacing/horde_pacing','scripts/managers/pacing/specials_pacing/specials_pacing','scripts/managers/pacing/heat_pacing/heat_pacing',
        'scripts/managers/pacing/monster_pacing/monster_pacing','scripts/managers/minion/minion_spawn_manager',
        'scripts/managers/mutator/mutators/mutator_spawner','scripts/managers/mutator/mutators/mutator_nurgle_warp',
        'scripts/managers/horde/horde_manager','scripts/managers/mutator/mutators/mutator_modify_havoc',
        'scripts/managers/mutator/mutator_manager','scripts/managers/game_mode/game_mode_extensions/game_mode_extension_havoc',
        'scripts/managers/circumstance/circumstance_manager','scripts/extension_systems/health_station/health_station_system',
        'scripts/extension_systems/hazard_prop/hazard_prop_system']:
        value=tbl({});cache[path]=value;class_paths[path]=value;return value
    raise RuntimeError('Missing harness dependency: '+path)
L.globals().require=require
# Load authoritative data, then register all ten reference words with their actual source code.
pacing=require('scripts/managers/pacing/pacing_templates')
circ=require('scripts/settings/circumstance/templates/havoc_circumstance_template')
cache['scripts/settings/circumstance/circumstance_templates']=L.eval('table.clone')(circ)
mutators=tbl({})
for path in ['scripts/settings/mutator/templates/mutator_havoc_templates','scripts/settings/mutator/templates/mutator_minion_nurgle_blessing_templates',
             'scripts/settings/mutator/templates/mutator_extra_trickle_templates',
             'scripts/settings/mutator/templates/mutator_modify_pacing_templates','scripts/settings/mutator/templates/mutator_positive_templates']:
    for key,value in require(path).items(): mutators[key]=value
cache['scripts/settings/mutator/mutator_templates']=mutators
L.execute('new_test_mod("SoloPlay"); new_test_mod("HavocConditionManager"); mods.HavocConditionManager.has_local_gameplay_authority=function() return true end')
loc=load_mod('HavocConditionManager/scripts/mods/HavocConditionManager/HavocConditionManager_localization')
L.globals().mods.HavocConditionManager.localization=loc
load_mod('HavocConditionManager/scripts/mods/HavocConditionManager/reference_conditions')
load_mod('HavocConditionManager/scripts/mods/HavocConditionManager/native_spawn')
exec((work/'load_event_test_data.py').read_text(encoding='utf-8'),globals())
catalog=load_mod('HavocConditionManager/scripts/mods/HavocConditionManager/condition_catalog')
settings=tbl({'order':{'havoc_circumstances':[]},'lookup':{'havoc_circumstances':{}},'loc':{'havoc_circumstances':{},'circumstances':{}}})
# Stale SoloPlay difficulty rows must be removed from both order and lookup.
settings.lookup.havoc_circumstances.mutator_increased_difficulty=True
settings.lookup.havoc_circumstances.mutator_highest_difficulty=True
catalog.extend(settings)
assert not settings.lookup.havoc_circumstances.mutator_highest_difficulty
assert not catalog.category('mutator_increased_difficulty')
assert catalog.category('mutator_havoc_rotten_armor')=='havoc'
assert catalog.category('more_old_rotten_armor')=='havoc'
assert catalog.category('more_havoc_monster_specials')=='maelstrom'
assert catalog.category('more_havoc_nurgle_blessing')=='maelstrom'
assert catalog.category('more_havoc_assault_force')=='maelstrom'
assert catalog.category('more_havoc_abhuman')=='event'
assert catalog.category('more_havoc_elite_army')=='event'
assert catalog.category('more_havoc_endless_hordes')=='event'
assert catalog.category('more_havoc_barrel_grounds')=='event'
assert catalog.category('more_faction_combined')=='faction'
assert not catalog.category('unknown_havoc_event')
auric=L.globals().mods.HavocConditionManager.auric_conditions
assert len(list(auric.entries.keys()))==20
assert sum(catalog.category(id)=='maelstrom' for id in settings.order.havoc_circumstances.values())==23
native_flash=require('scripts/settings/circumstance/templates/flash_mission_circumstance_template')
native_mutators={m for template in native_flash.values() for m in template.mutators.values()}
native_lookup=cache['scripts/network_lookup/network_lookup'].circumstance_templates
templates=cache['scripts/settings/circumstance/circumstance_templates']
for id,entry in auric.entries.items():
    template=templates[id]
    assert native_lookup[native_lookup[id]]==id
    assert template.theme_tag=='default'
    assert catalog.category(id)=='maelstrom'
    assert id in settings.lookup.havoc_circumstances
    assert not settings.loc.havoc_circumstances[id].startswith('hcm_auric_')
    for m in template.mutators.values():
        assert m in native_mutators and mutators[m] is not None,(id,m)
# Only environmental setup supplies these mutually exclusive map states.
assert all(m not in {'mutator_darkness_los','mutator_ventilation_purge_los','mutator_toxic_gas_volumes'}
           for id in auric.entries.keys() for m in templates[id].mutators.values())
assert templates.hcm_auric_no_ammo.mission_overrides.pickup_settings.primary.ammo.small_clip[1]==-99
assert templates.hcm_auric_barrels.mission_overrides.hazard_prop_settings.none==0
before=len(list(native_lookup.keys()))
load_mod('HavocConditionManager/scripts/mods/HavocConditionManager/auric_conditions')
assert len(list(native_lookup.keys()))==before
# A reload with the module cache cleared must reuse every protected lookup ID.
registered={id:native_lookup[id] for id in auric.entries.keys()}
L.globals().mods.HavocConditionManager.auric_conditions=None
load_mod('HavocConditionManager/scripts/mods/HavocConditionManager/auric_conditions')
assert len(list(native_lookup.keys()))==before
assert all(native_lookup[id]==number and native_lookup[number]==id for id,number in registered.items())
print('Protected native NetworkLookup: first registration, cached reload and uncached reload: PASS')

environment_families={
    'darkness':['darkness_01','darkness_hunting_grounds_01'],
    'ventilation_purge':['ventilation_purge_01','ventilation_purge_with_snipers_01'],
    'toxic_gas':['toxic_gas_01','toxic_gas_cultist_grenadier'],
    'ember':['ember_01_havoc'],
}
for family in environment_families:
    for id,template in require('scripts/settings/circumstance/templates/'+family+'_circumstance_template').items():
        templates[id]=template
havoc_settings=require('scripts/settings/havoc_settings')
settings.order.havoc_theme_circumstances=tbl([id for ids in environment_families.values() for id in ids])
settings.lookup.theme_of_circumstances=tbl({'default':'default',**{id:family for family,ids in environment_families.items() for id in ids}})
allowed={}
for family,missions in havoc_settings.missions.items():
    for mission in missions.values():
        allowed.setdefault(mission,{})
        for id in environment_families.get(family,[]): allowed[mission][id]=True
settings.lookup.theme_circumstances_of_havoc_missions=tbl(allowed)
for ids in environment_families.values():
    for id in ids:
        settings.loc.havoc_circumstances[id]=id
# Each selectable environment must have a matching map theme and real loaded mutators.
for mission in allowed:
    for family,ids in environment_families.items():
        expected=family in havoc_settings.missions and mission in list(havoc_settings.missions[family].values())
        for id in ids:
            assert bool(catalog.environment_available(settings,mission,id))==expected,(mission,id)
assert not catalog.environment_available(settings,'unknown_map','darkness_01')
assert not catalog.environment_available(settings,'cm_habs','missing_template')
for mission in allowed:
    assert catalog.environment_available(settings,mission,'default')
print('Environment allowlists: 19 native maps; darkness 13, fog 9, gas 6; unknown maps and unsupported ember excluded: PASS')

print('20 native Auric mechanisms, 23 gold entries, network registration, localization, resource overrides and taxonomy: PASS')
L.globals().test_settings=settings
L.globals().test_catalog=catalog
L.globals().test_templates=pacing
