"""Recreate mission-linked dropdowns and click with the native hotspot pass."""
from native_harness import *
import hashlib, json
exec((work/'ui_support.py').read_text(encoding='utf-8'),globals())

widget_text=(GAME/'scripts/managers/ui/ui_widget.lua').read_text(encoding='utf-8-sig')
passes_text=(GAME/'scripts/managers/ui/ui_passes.lua').read_text(encoding='utf-8-sig')
hotspot_text=passes_text[passes_text.index('UIPasses.hotspot = {'):passes_text.index('\nUIPasses.debug_cursor = {')]
L.execute('''
bit=require("bit")
function table.set(t) local r={} for _,v in ipairs(t) do r[v]=true end return r end
InputDevice={gamepad_active=false};GameParameters={};NilCursor={-10000,-10000,0}
Script.type_name=function() return "Vector3" end
function math.point_is_inside_2d_box(p,pos,size)
 return p[1]>=pos[1] and p[1]<=pos[1]+size[1] and p[2]>=pos[2] and p[2]<=pos[2]+size[2]
end
local UIPasses={};local double_click_threshold=.3;local cursor_value_type_name="Vector3"
local UIResolution=require("scripts/managers/ui/ui_resolution")
'''+hotspot_text+'\nNativeHotspot=UIPasses.hotspot')
cache['scripts/managers/ui/ui_passes']=L.eval('setmetatable({hotspot=NativeHotspot},{__index=function() return {init=function() end} end})')
cache['scripts/managers/ui/ui_scenegraph']=tbl({})
cache['scripts/managers/ui/ui_animation']=tbl({})
cache['scripts/managers/input/input_device']=L.globals().InputDevice
cache['scripts/ui/default_pass_values']=lua_file(GAME/'scripts/ui/default_pass_values.lua')
cache['scripts/ui/default_pass_styles']=lua_file(GAME/'scripts/ui/default_pass_styles.lua')
cache['scripts/managers/ui/ui_widget']=L.execute(widget_text)

# Dropdown decorations/animation are a rendering boundary. The actual widget
# factory, instance isolation, hotspot hit testing and view callbacks execute.
cache['scripts/ui/pass_templates/dropdown_pass_templates']=L.eval('''{
 settings_dropdown=function(w,h)
  return {{pass_type="hotspot",content_id="hotspot",style_id="hotspot",style={size={w,h}}}}
 end}''')
L.execute('''
function callback(owner,name,...)
 local args={...};return function() return owner[name](owner,unpack(args)) end
end
Managers.time={time=function() return 1 end}
mods.HavocConditionManager.refresh_condition_generators=function() end
mods.HavocConditionManager.custom_efl={
 get=function() return mods.SoloPlay:get("havoc_difficulty_circumstance") end,
 set=function(value) mods.SoloPlay:set("havoc_difficulty_circumstance",value) end}
''')
view_text=(SOURCES/'HavocConditionManager/scripts/mods/HavocConditionManager/condition_manager_view/condition_manager_view.lua').read_text(encoding='utf-8-sig')
def method(name):
 start=view_text.index('HavocConditionManagerView.'+name+' = function')
 return view_text[start:view_text.index('\nend',start)+4]
getter=view_text[view_text.index('local addon_setting_keys'):view_text.index('\nHavocConditionManagerView = class')]
L.execute('''
VisibilityView={};local HavocConditionManagerView=VisibilityView
local mod=mods.HavocConditionManager;local base_mod=mods.SoloPlay
local UIWidget=require("scripts/managers/ui/ui_widget")
local DropdownPassTemplates=require("scripts/ui/pass_templates/dropdown_pass_templates")
local Paging=mod:io_dofile("HavocConditionManager/scripts/mods/HavocConditionManager/condition_manager_view/paging")
local view_settings=mod:io_dofile("HavocConditionManager/scripts/mods/HavocConditionManager/condition_manager_view/condition_manager_view_settings")
local make_options={}
for _,id in ipairs(view_settings.dropdown_all_ids) do
 make_options[id]=function() return {{id="default",value="default",display_name="default"},{id="alternative",value="alternative",display_name="alternative"}} end
end
'''+getter+'\n'+'\n'.join(method(n) for n in ('_build_dropdown_definition','_recreate_dropdown','_load_dropdown_selection','_setup_dropdown','_set_exclusive_focus_on_setting','cb_on_dropdown_pressed'))+'''
function new_view(page)
 local view=setmetatable({_hcm_page=page,_current={},_options={},_dropdown_widgets={},_widgets_by_name={}}, {__index=VisibilityView})
 view._create_widget=function(self,name,definition)
  local widget=UIWidget.init(name,definition);self._widgets_by_name[name]=widget;return widget
 end
 view._modifier_grid={disable_input=function(_,value) view.grid_disabled=value end}
 local normal={hotspot_left={},hotspot_right={}}
 for i=1,5 do normal["hotspot_"..i]={} end
 view._widgets_by_name.normal_difficulty={content=normal}
 for _,id in ipairs({"havoc_modifier_lock","havoc_randomize","normal_start","havoc_start"}) do
  view._widgets_by_name[id]={content={hotspot={}}}
 end
 view._havoc_difficulty_slider_widget={content={hotspot={}}}
 for _,id in ipairs(view_settings.dropdown_all_ids) do view:_recreate_dropdown(id) end
 return view
end
function assert_hidden(view)
 for _,id in ipairs({"havoc_theme_circumstance","havoc_add_circumstance","havoc_remove_circumstance"}) do
  local widget=view._dropdown_widgets[id]
  assert(widget.visible==false and widget.content.hotspot.disabled and not widget.content.exclusive_focus,id.." leaked")
 end
end
function click_efl(view,scale,reverse)
 local ids={"havoc_difficulty_circumstance","havoc_theme_circumstance"}
 if reverse then ids={ids[2],ids[1]} end
 local input={get=function(_,key) if key=="cursor" then return {1550*scale,320*scale,0} elseif key=="left_pressed" then return true end end}
 local renderer={dt=.016,scale=scale,inverse_scale=1/scale,input_service=input}
 local hits={}
 for _,id in ipairs(ids) do
  local widget=view._dropdown_widgets[id]
  local hotspot=widget.content.hotspot;hotspot._input_pressed=false;hotspot.double_click_timer=0
  if widget.visible~=false then
   local callback=hotspot.pressed_callback
   hotspot.pressed_callback=function() hits[#hits+1]=id;callback() end
   NativeHotspot.draw({data={}},renderer,widget.style.hotspot,hotspot,{1295,294,0},{510,52})
   hotspot.pressed_callback=callback
  end
 end
 assert(#hits==1 and hits[1]=="havoc_difficulty_circumstance",table.concat(hits,","))
 assert(view._selected_setting==view._dropdown_widgets.havoc_difficulty_circumstance)
 assert_hidden(view)
end
for _,scale in ipairs({.8,1,2}) do for _,reverse in ipairs({false,true}) do
 local view=new_view(1);assert_hidden(view)
 -- Changing mission invokes its real callback and recreates linked controls.
 local mission=view._dropdown_widgets.havoc_mission
 mission.content.entry.on_activated("alternative",mission.content.entry)
 assert(view._current.havoc_mission=="alternative")
 assert_hidden(view);click_efl(view,scale,reverse)
 view:_set_exclusive_focus_on_setting(nil);assert_hidden(view)
 -- The conditions page still uses the hidden widget's persistence callback.
 local environment=view._dropdown_widgets.havoc_theme_circumstance
 environment.content.entry.on_activated("alternative",environment.content.entry)
 assert(mods.SoloPlay:get("havoc_theme_circumstance")=="alternative")
 view:_set_exclusive_focus_on_setting("havoc_theme_circumstance")
 assert(not view._selected_setting);assert_hidden(view)
 -- Randomize/preset refresh recreates every widget without a page refresh.
 for id in pairs(view._dropdown_widgets) do view:_recreate_dropdown(id) end
 click_efl(view,scale,reverse)
 -- Replacing the focused dropdown releases the old instance.
 view:_recreate_dropdown("havoc_difficulty_circumstance")
 assert(not view._selected_setting);assert_hidden(view)
end end
for page=2,4 do
 local view=new_view(page)
 for _,widget in pairs(view._dropdown_widgets) do assert(widget.visible==false and widget.content.hotspot.disabled) end
 view:_set_exclusive_focus_on_setting(nil)
 for id,widget in pairs(view._dropdown_widgets) do
  assert(widget.content.hotspot.disabled,id)
  view:_recreate_dropdown(id);assert(view._dropdown_widgets[id].visible==false)
 end
end
''')
report={'passed':True,'scope':'Native UIWidget factory/init, native hotspot hit testing and actual HCM callbacks; decorations and engine rendering are boundaries',
 'cases':['mission-linked recreation','EFL click at three scales in both draw orders','hidden focus rejection','environment callback persistence','randomize/preset-style recreation','focused instance replacement','recreation on pages 2-4'],
 'source_sha256':{str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in (GAME/'scripts/managers/ui/ui_widget.lua',GAME/'scripts/managers/ui/ui_passes.lua')}}
(CHECKS/'dropdown-visibility-results.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print('Dropdown visibility: mission changes, EFL clicks, hidden focus, environment persistence, repeated recreation, focused replacement and pages 2-4: PASS')
