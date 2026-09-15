from pathlib import Path
import sys,re,json
work=Path(__file__).resolve().parent

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
Vector3Box=function(...) return {...} end
CLASS={HudElementBossHealth={}}
Application={user_setting=function() return {} end}
Log={info=function() end,warning=function() end}
mods={}; hooks={}; classes={}; warnings={}
function get_mod(name) return mods[name] end
function new_test_mod(name)
    local m={_settings={},values={},localization={}}
    function m:get(k) return self.values[k] end
    function m:set(k,v) self.values[k]=table.clone_instance(v) end
    function m:persistent_table(k) self._persistent=self._persistent or {};self._persistent[k]=self._persistent[k] or {};return self._persistent[k] end
    function m:is_enabled() return self._enabled~=false end
    function m:enable_all_hooks() self._hooks_enabled=true end
    function m:disable_all_hooks() self._hooks_enabled=false end
    -- DMF always formats translated text, including calls without arguments.
    function m:localize(k,...) local v=self.localization[k]; local s=v and (v[test_language or "zh-cn"] or v.en) or k; return string.format(s,...) end
    function m:io_dofile(p) return load_mod_file(p) end
    function m:io_read_content(p,extension) return read_mod_file(p,extension) end
    function m:add_global_localize_strings(t) self.global_localization=self.global_localization or {}; for k,v in pairs(t) do self.global_localization[k]=v end end
    local function register(target,name,fn,safe)
        for _,h in ipairs(hooks) do
            assert(h.owner~=m or h.target~=target or h.name~=name,"DMF rejects duplicate hooks on the same owner/target/method: "..name)
        end
        hooks[#hooks+1]={target=target,name=name,fn=fn,owner=m,safe=safe}
    end
    function m:hook(target,name,fn) register(target,name,fn,false) end
    function m:hook_safe(target,name,fn) register(target,name,fn,true) end
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
def load_mod(p):
    source=stage if p.startswith("HavocConditionManager/") else PROJECT.parent/"HavocEnemyDirector/src"
    return lua_file(source/(p+".lua"))
L.globals().load_mod_file=load_mod
L.globals().read_mod_file=lambda p,ext: (stage/(p+'.'+ext)).read_text(encoding='utf-8-sig')
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
cache['scripts/managers/main_path/utilities/spawn_point_queries']=tbl({})
cache['scripts/managers/horde/horde_templates']=tbl({n:{'name':n} for n in ('trickle_horde','ambush_horde','far_vector_horde','flood_horde','far_distance_horde')})
cache['scripts/utilities/attack/player_unit_status']=tbl({})
cache['scripts/utilities/breed_queries']=L.eval('{minion_breeds_by_name=function() return require("scripts/settings/breed/breeds") end}')
# Small native helpers are executed as written; only their engine boundaries
# (route projection, vectors and physics) are supplied by individual cases.
cache['scripts/utilities/main_path_queries']=lua_file(game/'scripts/utilities/main_path_queries.lua')
cache['scripts/extension_systems/blackboard/utilities/blackboard']=L.eval('{write_component=function(board,name) return board[name] end}')
for path, owner, name in (
    ('scripts/utilities/minion_patrols','MinionPatrols','get_follow_index'),
    ('scripts/managers/horde/utilities/horde_utilities','HordeUtilities','position_has_line_of_sight_to_any_enemy_player'),
):
    source=(game/(path+'.lua')).read_text(encoding='utf-8-sig')
    start=source.index(owner+'.'+name+' = function')
    cache[path]=L.execute('local '+owner+'={};'+source[start:source.index('\nend',start)+4]+';return '+owner)
cache['scripts/settings/perception/perception_settings']=tbl({'aggro_states':{'aggroed':'aggroed','passive':'passive'}})
cache['scripts/managers/mutator/mutators/mutator_spawner/mutator_spawner_node']=tbl({'SINGLE_PLACEMENT':1,'CIRCLE_PLACEMENT':2})
cache['scripts/managers/mutator/mutators/mutator_spawner/mutator_spawner_location_sources']=L.eval('{prebaked_mission_locations=function() return {} end, mission_provided_gizmo=function() return {} end}')
cache['scripts/settings/components/enemy_event_spawner_settings']=tbl({'nurgle_totem':{}})
cache['scripts/network_lookup/network_lookup']=tbl({'buff_templates':{},'circumstance_templates':{}})
cache['scripts/settings/buff/buff_templates']=tbl({'NON_PREDICTED':{},'mutator_minion_nurgle_blessing_tougher':{'name':'mutator_minion_nurgle_blessing_tougher'}})
cache['scripts/utilities/loaded_dice']=L.eval('{create=function() return {},{} end}')
cache['scripts/utilities/nav_queries']=tbl({})
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
    'scripts/settings/havoc_settings','scripts/settings/circumstance/templates/havoc_circumstance_template','scripts/settings/monster/monster_settings'}
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
        'scripts/extension_systems/minion_spawner/minion_spawner_extension',
        'scripts/extension_systems/minion_spawner/minion_spawner_system',
        'scripts/extension_systems/trigger/trigger_actions/trigger_action_base',
        'scripts/extension_systems/health/health_extension',
        'scripts/extension_systems/perception/minion_perception_extension',
        'scripts/extension_systems/hazard_prop/hazard_prop_system']:
        value=tbl({});cache[path]=value;class_paths[path]=value;return value
    raise RuntimeError('Missing harness dependency: '+path)
L.globals().require=require

# Additional native data families. Rendering, navigation and object creation are
# explicit boundaries; callbacks and managers are executed separately in tests.
real_roots += ("scripts/managers/pacing/auto_event/templates/","scripts/settings/terror_event/terror_event_templates/")
cache["scripts/managers/terror_event/utilities/terror_event_queries"]=tbl({})
cache["scripts/managers/terror_event/terror_event_manager"]=tbl({})
cache["scripts/managers/terror_event/terror_event_nodes"]=tbl({"spawn_by_points":{}})
cache["scripts/managers/pacing/auto_event/auto_event"]=tbl({})
cache["scripts/managers/mutator/mutators/mutator_base"]=tbl({})
L.execute("""
table.clone=table.clone_instance
function table.append(a,b) for _,v in ipairs(b) do a[#a+1]=v end return a end
function table.add_missing(a,b) for k,v in pairs(b) do if a[k]==nil then a[k]=v end end return a end
function table.reduce(a,fn,result) for _,v in ipairs(a) do result=fn(result,v) end return result end
""")
pacing=require("scripts/managers/pacing/pacing_templates")
# Materialize immutable boxed settings before individual tests install their
# lifetime-checking vector implementations for the engine calls under test.
require("scripts/settings/monster/monster_settings")
mutators=tbl({})
for path in ["mutator_havoc_templates","mutator_minion_nurgle_blessing_templates","mutator_extra_trickle_templates",
             "mutator_modify_pacing_templates","mutator_positive_templates"]:
    for key,value in require("scripts/settings/mutator/templates/"+path).items(): mutators[key]=value
cache["scripts/settings/mutator/mutator_templates"]=mutators
circ=require("scripts/settings/circumstance/templates/havoc_circumstance_template")
cache["scripts/settings/circumstance/circumstance_templates"]=L.eval("table.clone")(circ)
L.execute('new_test_mod("SoloPlay"); new_test_mod("HavocConditionManager"); host=true; mods.HavocConditionManager.has_local_gameplay_authority=function() return host end')
exec((work/"load_event_test_data.py").read_text(encoding="utf-8"),globals())
events=tbl({})
for path in sorted((game/"scripts/settings/terror_event/terror_event_templates").glob("*.lua")):
    events[path.stem]=require("scripts/settings/terror_event/terror_event_templates/"+path.stem)
cache["scripts/settings/terror_event/terror_event_templates"]=events
B=L.globals().mods.HavocConditionManager
B.localization=load_mod("HavocConditionManager/scripts/mods/HavocConditionManager/HavocConditionManager_localization")
B.template_schema=load_mod("HavocConditionManager/scripts/mods/HavocConditionManager/template_schema")
B.template_conditions=load_mod("HavocConditionManager/scripts/mods/HavocConditionManager/template_conditions")
B.template_registry=load_mod("HavocConditionManager/scripts/mods/HavocConditionManager/template_registry")
B.template_runtime=load_mod("HavocConditionManager/scripts/mods/HavocConditionManager/template_runtime")
L.execute("B=mods.HavocConditionManager; S=B.template_schema; R=B.template_conditions; A=B.template_registry; E=B.template_runtime")
