"""Full HCM entry point without HED; SoloPlay catalog contract and view lifecycle."""
from native_harness import *
templates=cache["scripts/settings/circumstance/circumstance_templates"]
# Representative SoloPlay selection rows include valid, missing, environmental,
# duplicate and difficulty entries. Native template tables stay unmodified.
for id,extra in {
    "high_flash_mission_test":{},"native_event_test":{"ui":{"description":"loc_event_test"}},
    "native_general_test":{},"darkness_01":{"theme_tag":"darkness"},
    "missing_mutator_test":{},"mutator_highest_difficulty":{}}.items():
    templates[id]=tbl({"mutators":["missing" if id=="missing_mutator_test" else "mutator_rotten_armor"],**extra})
ids=list(templates.keys())
settings=tbl({"order":{"havoc_circumstances":list(circ.keys()),"circumstances":ids+["unavailable_test"]},
    "lookup":{"havoc_circumstances":{id:True for id in circ.keys()},
    "theme_circumstances_of_havoc_missions":{"cm_habs":{"darkness_01":True}},
    "havoc_modifiers_max_level":{}},
    "loc":{"havoc_circumstances":{id:id for id in circ.keys()},"circumstances":{id:id for id in ids}}})
L.globals().test_settings=settings
L.globals().native_conditions=templates
L.globals().native_mutators=mutators
L.execute('before_conditions=table.clone_instance(native_conditions); before_mutators=table.clone_instance(native_mutators)')
loaded_modules = []
original_load_mod = load_mod

def standalone_load_mod(path):
    assert not path.startswith('HavocEnemyDirector/'), path
    loaded_modules.append(path)
    if '--failed-diy' in sys.argv and path.endswith('/diy_conditions'):
        return False
    return original_load_mod(path)

load_mod = standalone_load_mod
L.globals().load_mod_file = standalone_load_mod
cache['scripts/settings/ui/ui_sound_events'] = tbl({})
# This test executes entrypoint/catalog wiring with DIY disabled. Dedicated DIY
# boundary tests execute the real native utility and extension methods.
for path in ('scripts/extension_systems/buff/buff_extension_base','scripts/extension_systems/buff/player_unit_buff_extension',
    'scripts/extension_systems/buff/minion_buff_extension','scripts/utilities/attack/attack',
    'scripts/utilities/attack/damage_calculation','scripts/settings/damage/damage_profile_templates',
    'scripts/utilities/ammo','scripts/utilities/attack/stamina','scripts/utilities/warp_charge',
    'scripts/utilities/overheat','scripts/utilities/fixed_frame','scripts/managers/attack_report/attack_report_manager',
    'scripts/managers/difficulty/difficulty_manager'):
    cache[path]=tbl({})
cache['scripts/settings/wwise_game_sync/wwise_game_sync_settings'] = tbl({'state_groups': {'options': {'ingame_menu': 'menu'}}})
for path in ('scripts/ui/hud/elements/tactical_overlay/hud_element_tactical_overlay', 'scripts/ui/views/lobby_view/lobby_view'):
    cache[path] = tbl({})
L.execute('''
hooks={}
function string.split(s, delimiter)
    local result,first={},1
    while true do
        local last=s:find(delimiter,first,true)
        result[#result+1]=s:sub(first,last and last-1 or #s)
        if not last then return result end
        first=last+#delimiter
    end
end
mods.SoloPlay.io_dofile=function() return test_settings end
mods.SoloPlay.has_local_gameplay_authority=function() return true end
mods.SoloPlay.gen_havoc_mission_context=function() return {havoc_data="a;;rank;faction;old;modifiers;seed;tail"} end
mods.SoloPlay.open_solo_view=function() return "native view" end
''')
load_mod('HavocConditionManager/scripts/mods/HavocConditionManager/HavocConditionManager')
if '--failed-diy' in sys.argv:
    L.execute('''
    local m=mods.HavocConditionManager
    assert(m.update_diy_conditions==nil and m.finish_diy_conditions==nil)
    for i=1,1000 do m.update(.016) end
    m.on_game_state_changed("exit","GameplayStateRun")
    m.on_disabled(false);m.on_enabled(false)
    ''')
    print('Failed HCM DIY initialization: 1,000 updates, mission exit and enable/disable without repeated errors: PASS')
    sys.exit(0)
L.execute('''
assert(get_mod("HavocEnemyDirector")==nil)
local base,solo=mods.HavocConditionManager,mods.SoloPlay
local saved_open=base.open_condition_manager_view
base.open_condition_manager_view=function() return "expanded view" end
assert(solo.open_solo_view()=="expanded view")
base._enabled=false; base.on_disabled(false)
assert(solo.open_solo_view()=="native view")
assert(solo.gen_havoc_mission_context().havoc_data=="a;;rank;faction;old;modifiers;seed;tail")
base._enabled=true; base.on_enabled(false)
assert(solo.open_solo_view()=="expanded view")
base.open_condition_manager_view=saved_open
local previous_ui=Managers.ui
local opened,closing,close_count=false,false,0
Managers.ui={view_instance=function() return opened and {} or nil end,
    is_view_closing=function() return closing end,
    open_view=function() opened=true end,
    close_view=function() assert(not closing,"duplicate close during exit animation"); closing=true; close_count=close_count+1 end}
base.open_condition_manager_view(); assert(opened)
base._enabled=false; base.on_disabled(false)
base.close_condition_manager_view(); base.open_condition_manager_view()
assert(closing and close_count==1)
base._enabled=true; base.on_enabled(false); assert(close_count==1)
Managers.ui=previous_ui
solo:set("havoc_mission","cm_habs")
solo:set("havoc_theme_circumstance","darkness_01")
solo:set("havoc_difficulty_circumstance","mutator_highest_difficulty")
base:set("havoc_circumstances_serialized", "mutator_havoc_rotten_armor:high_flash_mission_test:native_event_test:missing_removed")
solo.values.hcm_condition_selection_v3=nil
local context=solo.gen_havoc_mission_context()
assert(not context.havoc_data:find("missing_removed",1,true))
assert(base:get("havoc_circumstances_serialized"):find("missing_removed",1,true))
assert(solo:get("hcm_condition_selection_v3"):find("native_event_test",1,true))
for _,id in ipairs({"mutator_havoc_rotten_armor","high_flash_mission_test","native_event_test","darkness_01","mutator_highest_difficulty"}) do
    assert(context.havoc_data:find(id,1,true),id)
end
assert(context.havoc_data:find(";modifiers;seed;tail",1,true))
solo:set("havoc_mission","cm_raid")
solo.gen_havoc_mission_context()
assert(solo:get("havoc_theme_circumstance")=="default")
base.refresh_condition_generators()
''')
print('Standalone entry point, all condition categories, environment fallback and optional callbacks: PASS')

L.globals().game_classes = tbl(class_paths)
L.execute('''
local base=mods.HavocConditionManager
local MS=game_classes["scripts/managers/minion/minion_spawn_manager"]
local receipts=0
for _,hook in ipairs(hooks) do
    if hook.owner==base and hook.target==MS and hook.name=="spawn_minion" then
        receipts=receipts+1
        local native_calls=0;local unit={};local params={source="retained"}
        local authority=base.has_local_gameplay_authority;base.has_local_gameplay_authority=function() return true end
        local result=hook.fn(function(self,breed,position,rotation,side,passed,extra)
            native_calls=native_calls+1;assert(passed==params and extra=="tail" and breed=="test");return unit
        end,{},"test",{}, {},2,params,"tail")
        base.has_local_gameplay_authority=authority
        assert(native_calls==1 and result==unit and not base.current_spawn_batch,"origin receipt duplicated or replaced native creation")
    end
end
assert(receipts==1)
assert(base.scale_native_horde==nil and base.scale_native_special_slot==nil)
''')
print('Standalone native migration: old spawn copies and per-category timer functions removed: PASS')

ui_setup = (work / 'ui_support.py').read_text(encoding='utf-8').split("L.execute('''\nlocal D=mods.HavocEnemyDirector", 1)[0]
exec(compile(ui_setup, 'standalone_ui_setup', 'exec'), globals())
L.execute('''
local view={_current={havoc_circumstances={}},_options={havoc_theme_circumstance={{id="default",display_name="default"}}}}
function view:_condition_display_name(id) return test_settings.loc.havoc_circumstances[id] or id end
for page=1,4 do
    view._hcm_page=page
    local ui=Paging.build(view,test_settings)
    assert(ui.page_count==4 and view._hcm_page==page)
    for _,item in ipairs(ui.items) do assert(not item.key:match("^hed_")) end
end
assert(get_mod("HavocEnemyDirector")==nil)
''')
print('Standalone UI: four pages including DIY; no HED page or HED module imports: PASS')

# Load the actual view chunk. Native rendering/blueprint boundaries are stubbed;
# definitions, paging, settings/options and view initialization execute normally.
for path in (
    'scripts/foundation/utilities/promise','scripts/utilities/havoc',
    'scripts/managers/ui/ui_renderer','scripts/foundation/utilities/script_world',
    'scripts/ui/view_elements/view_element_input_legend/view_element_input_legend',
    'scripts/ui/view_elements/view_element_grid/view_element_grid',
    'scripts/ui/pass_templates/dropdown_pass_templates'):
    cache.setdefault(path,tbl({}))
previous_loader=L.globals().load_mod_file
def view_load(path):
    if path.endswith('/condition_manager_view_blueprints'): return tbl({})
    return previous_loader(path)
L.globals().load_mod_file=view_load
L.execute('''
view_classes=0;settings_loads=0
test_settings.lookup.havoc_modifiers_max_level={test_modifier=5}
local original_settings=mods.SoloPlay.io_dofile
mods.SoloPlay.io_dofile=function(...)
 settings_loads=settings_loads+1;return table.clone_instance(original_settings(...))
end
BaseView={init=function(self,definitions)
 self._definitions=definitions
 self._widgets_by_name=table.clone_instance(definitions.widget_definitions)
end}
function class(name,parent)
 assert(name=="HavocConditionManagerView" and parent=="BaseView")
 view_classes=view_classes+1;local c={super=BaseView};c.__index=c;return c
end
''')
view_path='HavocConditionManager/scripts/mods/HavocConditionManager/condition_manager_view/condition_manager_view'
L.globals().View=load_mod(view_path)
L.globals().reload_view=lambda: load_mod(view_path)
L.execute('''
local B=mods.HavocConditionManager
assert(settings_loads==1,"The options module must reuse the view's prepared SoloPlay catalog")
local first=setmetatable({},View);first:init({})
assert(first._definitions.widget_definitions.hcm_control_1.passes==first._definitions.widget_definitions.hcm_control_220.passes)
for i=1,40 do
 assert(reload_view()==View)
 local v=setmetatable({},View);v:init({})
 assert(v._definitions==first._definitions)
 v._widgets_by_name.hcm_control_1.style.background.color[1]=0
 assert(first._widgets_by_name.hcm_control_1.style.background.color[1]~=0)
end
assert(view_classes==1 and settings_loads==1)
-- Disabling closes the view through the existing lifecycle; a later opening
-- can reuse the class while loading the latest saved values.
B._enabled=false;B.on_disabled(false);B._enabled=true;B.on_enabled(false)
assert(reload_view()==View)
local owner=mods.SoloPlay
local saved=owner:get("hcm_condition_selection_v3")
B.get_primary_havoc_conditions()
local setter=owner.set;local writes=0
owner.set=function(...) writes=writes+1;return setter(...) end
for i=1,100 do B.get_selected_conditions() end
assert(writes==0,"Read-only selection queries must not mark settings dirty")
setter(owner,"hcm_condition_selection_v3","invalid-condition")
assert(#B.get_primary_havoc_conditions()==0 and writes==1,"Invalid legacy values are still repaired once")
owner.set=setter;owner:set("hcm_condition_selection_v3",saved)
-- Draw callbacks change values in their own color table without allocating a
-- replacement every frame or mutating another widget/template.
local definition=first._definitions.widget_definitions.hcm_control_1
local bg,check
for _,pass in ipairs(definition.passes) do
 if pass.style_id=="background" then bg=pass.change_function end
 if pass.style_id=="check" then check=pass.change_function end
end
local style={color={0,0,0,0},text_color={0,0,0,0}};local color,text=style.color,style.text_color
for i=1,120 do
 bg({selected=i%2==0,hotspot={},actionable=true},style)
 check({selected=i%2==0},style)
 assert(style.color==color and style.text_color==text)
end
assert(color[1]==245 and text[2]==221)
-- An unchanged screen size and idle help line do not recreate viewport data
-- or re-localize the same help on every frame.
local paging=B._condition_paging_cache.module
local viewport=paging.viewport;local fits,helps=0,0
paging.viewport=function(...) fits=fits+1;return viewport(...) end
local localize=B.localize
B.localize=function(self,key,...) if key=="ui_051" then helps=helps+1 end;return localize(self,key,...) end
local ui={items={},help_targets={},hover_targets={},help_widget={content={}}}
local v={_ui_scenegraph={},_widgets_by_name={hcm_popup_blocker={style={hotspot={}}}},_hcm_ui=ui}
v.set_render_scale=function(self,s) self._render_scale=s end
v._set_scenegraph_size=function() end;v.trigger_resolution_update=function() end
RESOLUTION_LOOKUP={width=1920,height=1080}
local input={get=function(_,key) return key=="scroll_axis" and {0,0} or false end}
for i=1,120 do paging.update(v,input) end
assert(fits==1 and helps==1)
paging.viewport=viewport;B.localize=localize;RESOLUTION_LOOKUP=nil
-- A language change refreshes localized definitions rather than freezing text.
B.localize=function(self,key,...) if key=="ui_034" then return "changed-language" end;return localize(self,key,...) end
assert(reload_view()~=View and settings_loads==2 and view_classes==2)
B.localize=localize
''')
L.globals().load_mod_file=previous_loader
print('Standalone editor: 40 warm opens reuse one class/catalog/template; widget colors remain isolated, language changes rebuild, disabled/re-enabled entry retained, 100 unchanged reads avoid setting writes: PASS')

L.execute("""
assert(S.equal(before_conditions,native_conditions) and S.equal(before_mutators,native_mutators))
local C=B.condition_catalog
assert(C.category("high_flash_mission_test")=="maelstrom" and C.category("native_event_test")=="event")
assert(C.category("native_general_test")=="general" and C.category("mutator_havoc_rotten_armor")=="havoc")
for _,id in ipairs({"darkness_01","missing_mutator_test","unavailable_test","mutator_highest_difficulty"}) do
 assert(not test_settings.lookup.havoc_circumstances[id],id)
end
-- Native condition extensions preserve deduplication and additive item semantics.
local function hook(path,name)
 local target=require(path)
 for _,h in ipairs(hooks) do if h.target==target and h.name==name then return h.fn end end
 error(name)
end
local mission={circumstances={"native_general_test","native_event_test"}}
Managers.state.difficulty={get_parsed_havoc_data=function() return mission end}
native_conditions.native_general_test.mission_overrides={health_station={charges=3},pickup_settings={ammo={small=2}},hazard_prop_settings={barrel="native_a"}}
native_conditions.native_event_test.mission_overrides={health_station={charges=2},pickup_settings={ammo={small=4}},hazard_prop_settings={barrel="native_b"}}
local calls=0
local manager={_is_server=false,load_mutator_from_name=function(self,name) calls=calls+1; return {_template={}} end}
hook("scripts/managers/mutator/mutator_manager","_load_mutators")(function() error("native duplicates") end,manager,"default")
assert(calls==1)
Managers.state.circumstance={circumstance_name=function() return "native_general_test" end}
local original={ammo={small=1}}
local pickups=hook("scripts/managers/game_mode/game_mode_extensions/game_mode_extension_havoc","get_havoc_pickup_overrides")(function() return original end,{})
assert(pickups.ammo.small==5 and original.ammo.small==1)
local hazard={}
hook("scripts/extension_systems/hazard_prop/hazard_prop_system","_populate_hazard_props")(function(self) assert(self._hazard_prop_settings.barrel=="native_b") end,hazard)
local overrides=hook("scripts/managers/circumstance/circumstance_manager","mission_overrides")(function() return {untouched=true} end,{})
assert(overrides.health_station.charges==2 and overrides.untouched)
Managers.state.difficulty=nil
""")
print("Catalog provenance, invalid-row filtering, old selection migration, mutator deduplication, pickup/health/hazard overrides: PASS")

# Every hook registered against a native class resolves to an actual source method.
checked=0
same=L.eval("function(a,b) return rawequal(a,b) end")
for _,hook in L.globals().hooks.items():
    if hook.target is None: continue
    for path,target in cache.items():
        if not same(hook.target,target): continue
        source=game/(path+".lua")
        if source.is_file() and hook.name:
            text=source.read_text(encoding="utf-8-sig")
            # The native class utility copies base methods into concrete buff
            # classes. Verify inheritance as well as methods declared here.
            if re.search(r'class\("(?:PlayerUnitBuffExtension|MinionBuffExtension)", "BuffExtensionBase"\)',text):
                text+='\n'+(game/'scripts/extension_systems/buff/buff_extension_base.lua').read_text(encoding='utf-8-sig')
            assert re.search(r"[.:]"+re.escape(hook.name)+r"\s*=\s*function",text),(path,hook.name)
            checked+=1
        break
assert checked>=15,checked
print("Registered native hook methods resolve in current game source:",checked,"PASS")
