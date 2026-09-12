"""Fresh HCM + SoloPlay harness: never loads the advanced director."""
from pathlib import Path

work = Path(__file__).resolve().parent
source = (work / 'harness.py').read_text(encoding='utf-8')
bootstrap = source.split("L.execute('''\nmods.HavocConditionManager.condition_catalog=test_catalog", 1)[0]
exec(compile(bootstrap, 'standalone_bootstrap', 'exec'), globals())
loaded_modules = []
original_load_mod = load_mod

def standalone_load_mod(path):
    assert not path.startswith('HavocEnemyDirector/'), path
    loaded_modules.append(path)
    return original_load_mod(path)

load_mod = standalone_load_mod
L.globals().load_mod_file = standalone_load_mod
cache['scripts/settings/ui/ui_sound_events'] = tbl({})
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
base:set("havoc_circumstances_serialized", "mutator_havoc_rotten_armor:hcm_auric_hounds:more_havoc_elite_army")
local context=solo.gen_havoc_mission_context()
for _,id in ipairs({"mutator_havoc_rotten_armor","hcm_auric_hounds","more_havoc_elite_army","darkness_01","mutator_highest_difficulty"}) do
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
for _,hook in ipairs(hooks) do
    assert(not (hook.owner==base and hook.target==MS and hook.name=="spawn_minion"),"HCM native mode must not duplicate low-level spawns")
end
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
    assert(ui.page_count==3 and view._hcm_page==math.min(page,3))
    for _,item in ipairs(ui.items) do assert(item.key~="tab_4") end
end
assert(get_mod("HavocEnemyDirector")==nil)
''')
print('Standalone UI: three pages; no advanced page or advanced module imports: PASS')

L.execute("""
local RP=game_classes["scripts/managers/pacing/roamer_pacing/roamer_pacing"]
local update
for _,h in ipairs(hooks) do if h.target==RP and h.name=="update" then update=h.fn end end
mods.HavocConditionManager:set("faction_switch_guaranteed",false)
local old_unpack=unpack
unpack=function() error("Unnecessary per-frame result table") end
local a,b,c=update(function() return 17,nil,23 end,{},0.016,1,1,2)
assert(a==17 and b==nil and c==23)
unpack=old_unpack
""")
print('Inactive guaranteed-faction update: native returns including nil preserved, no result-table allocation: PASS')

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
local saved=B:get("havoc_circumstances_serialized")
B.get_primary_havoc_conditions()
local setter=B.set;local writes=0
B.set=function(...) writes=writes+1;return setter(...) end
for i=1,100 do B.get_selected_conditions() end
assert(writes==0,"Read-only selection queries must not mark settings dirty")
setter(B,"havoc_circumstances_serialized","invalid-condition")
assert(#B.get_primary_havoc_conditions()==0 and writes==1,"Invalid legacy values are still repaired once")
B.set=setter;B:set("havoc_circumstances_serialized",saved)
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
local ui={items={},help_widget={content={}}}
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
