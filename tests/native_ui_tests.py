"""Exercise the real dashboard builder and numeric input; export layout previews."""
from native_harness import *
import json
exec((work/"ui_support.py").read_text(encoding="utf-8"),globals())
L.execute("""
local W=require("scripts/managers/ui/ui_widget")
W.init=function(name,definition) return table.clone_instance(definition) end
mods.SoloPlay.has_local_gameplay_authority=function() return host end
new_test_mod("HavocEnemyDirector")
""")
D=L.globals().mods.HavocEnemyDirector
D.localization=load_mod("HavocEnemyDirector/scripts/mods/HavocEnemyDirector/HavocEnemyDirector_localization")
load_mod("HavocEnemyDirector/scripts/mods/HavocEnemyDirector/HavocEnemyDirector")
B.condition_catalog=load_mod("HavocConditionManager/scripts/mods/HavocConditionManager/native_condition_catalog")
templates=cache["scripts/settings/circumstance/circumstance_templates"]
ids=sorted(templates.keys())
settings=tbl({"order":{"havoc_circumstances":list(circ.keys()),"circumstances":ids},
    "lookup":{"havoc_circumstances":{id:True for id in circ.keys()}},
    "loc":{"havoc_circumstances":{id:id for id in ids},"circumstances":{id:id for id in ids}}})
B.condition_catalog.extend(settings)
L.globals().test_settings=settings
L.execute("""
view={_widgets_by_name=table.clone_instance(full_definitions.widget_definitions),_hcm_page=3,
    _options={havoc_theme_circumstance={{id="default",display_name="Default"}}},
    _dropdown_widgets={},_current={havoc_circumstances={}},_positions={},_hcm_offsets={}}
function view:_set_exclusive_focus_on_setting() end
function view:_persist_havoc_circumstances() mods.SoloPlay:set("hcm_condition_selection_v3",table.concat(self._current.havoc_circumstances,":")) end
function view:_condition_display_name(id) return test_settings.loc.havoc_circumstances[id] or id end
function view:_set_scenegraph_position(id,x,y,z) self._positions[id]={x,y,z} end
function view:_set_scenegraph_size(id,w,h) self._positions[id]=self._positions[id] or {}; self._positions[id].w=w; self._positions[id].h=h end
function refresh() Paging.refresh(view,test_settings) end
function find(key)
    for i,item in ipairs(view._hcm_ui.items) do if item.key==key then return item,view._widgets_by_name["hcm_control_"..i] end end
    error("Missing control: "..key)
end
function click(key)
    local item,widget=find(key); assert(item.action and not widget.content.hotspot.disabled,"Unavailable control: "..key)
    widget.content.hotspot.pressed_callback(); refresh()
end
function edit(key,text)
    click(key)
    view._widgets_by_name.hcm_number_input.content.input_text=text
    assert(Paging.numeric.commit(view)); refresh()
end
refresh()
assert(find("native_advanced_toggle") and #view._hcm_ui.sliders==1 and #view._hcm_ui.help_targets==1 and #view._hcm_ui.hover_targets<=1)
for _,item in ipairs(view._hcm_ui.items) do assert(item.key~="native_roamer_population_value") end
click("native_advanced_toggle")
-- Collapsing active controls releases the native slider's cursor capture.
local old_windows,old_window=IS_WINDOWS,Window
local released=0;IS_WINDOWS=true;Window={set_clip_cursor=function(value) assert(value==false);released=released+1 end}
local hidden_slider=view._widgets_by_name.hcm_slider_2.content
hidden_slider.drag_active=true;hidden_slider.hcm_dragging=true;hidden_slider.input_offset=12
click("native_advanced_toggle")
assert(#view._hcm_ui.sliders==1 and not hidden_slider.drag_active and not hidden_slider.hcm_dragging and not hidden_slider.input_offset and released==1)
IS_WINDOWS=old_windows;Window=old_window
click("native_advanced_toggle")
edit("native_roamer_population_value","1.25")
assert(mods.HavocConditionManager:get("native_configuration_v3").roamer_population==1.25)
edit("native_roamer_population_value","2.5")
assert(mods.HavocConditionManager:get("native_configuration_v3").roamer_population==2.5)
edit("native_roamer_population_value","1")
assert(mods.HavocConditionManager:get("native_configuration_v3").roamer_population==1)
click("native_group_specials"); edit("native_special_slots_value","1.75")
assert(mods.HavocConditionManager:get("native_configuration_v3").special_slots==1.75)
click("tab_4")
view._hed_family="specials"; view._hed_entry="specials/default_specials/1"; view._hed_path={}; view._hed_item="max_alive_specials"; refresh()
local before=mods.HavocEnemyDirector.get_config()
edit("hed_value_value","8")
assert(mods.HavocEnemyDirector.peek_config().patches["specials/default_specials/1"].max_alive_specials==8)
click("hed_reset_field")
assert(not mods.HavocEnemyDirector.peek_config().patches["specials/default_specials/1"])
click("hed_native_field")
assert(mods.HavocEnemyDirector.peek_config().patches["specials/default_specials/1"].max_alive_specials==A.by_id["specials/default_specials/1"].root.max_alive_specials)
-- A false boolean override remains visible, including when the baseline is true.
local entry=A.by_id["specials/default_specials/1"]; local flag
for _,item in ipairs(entry.items) do if item.kind=="boolean" and item.value==true then flag=item; break end end
if flag then
    view._hed_item=flag.id; refresh(); click("hed_value")
    assert(mods.HavocEnemyDirector.peek_config().patches[entry.id][flag.id]==false)
    local shown=find("hed_value"); assert(shown.selected==false)
end
click("hed_tab_composition")
view._hed_path={"breeds"}; view._hed_item="breeds/all"; refresh()
local size=#entry.fields["breeds/all"].value
click("hed_add")
assert(#mods.HavocEnemyDirector.peek_config().patches[entry.id]["breeds/all"]==size+1)
-- The pool remains non-empty and native faction aliases are valid choices.
local original=entry.fields["breeds/all"].value
assert(S.validate_value(entry.fields["breeds/all"],original,A.breeds))
click("hed_tab_rules"); click("hed_rule_add")
click("hed_condition_1"); click("choice_hed_condition_1_load_max")
edit("hed_condition_value_1_value","55")
assert(mods.HavocEnemyDirector.peek_config().rules[entry.id].encounter.clauses[1].value==55)
click("hed_rule_match"); click("choice_hed_rule_match_any")
assert(mods.HavocEnemyDirector.peek_config().rules[entry.id].encounter.match=="any")
click("hed_rule_reset")
assert(not mods.HavocEnemyDirector.peek_config().rules[entry.id] or not next(mods.HavocEnemyDirector.peek_config().rules[entry.id]))
-- Invalid numeric edits keep the previous setting.
view._hed_tab="parameters"; view._hed_item="max_alive_specials"; view._hed_path={}; refresh()
click("hed_value_value"); view._widgets_by_name.hcm_number_input.content.input_text="0"
assert(not Paging.numeric.commit(view)); Paging.numeric.cancel(view); refresh()
-- Templates remain available when the separate HED mod is disabled/enabled.
mods.HavocEnemyDirector._enabled=false; refresh(); assert(view._hcm_ui.page_count==3)
mods.HavocEnemyDirector._enabled=true; view._hcm_page=4; refresh(); assert(view._hcm_ui.page_count==4)
""")
print("Live widget callbacks: coarse values, typed input, fine overrides, false booleans, composition edits, rule editing and DMF visibility: PASS")

def plain_items(ui):
    keys=("key","x","y","w","h","text","font","fill","panel","selected","center","danger","color","checkbox","choice","expanded","upwards","overlay","blocked","text_right_padding","vertical_alignment")
    result=[]
    for _,item in ui["items"].items():
        record={key:item[key] for key in keys if item[key] is not None}
        if item.slider is not None:
            record['slider']={key:item.slider[key] for key in ('value','min','max','mixed') if item.slider[key] is not None}
        result.append(record)
    return result
layouts={}
for lang in ("en","zh-cn","zh-tw"):
    L.globals().test_language=lang
    B.condition_catalog=load_mod("HavocConditionManager/scripts/mods/HavocConditionManager/native_condition_catalog")
    B.condition_catalog.extend(settings)
    L.globals().Paging=load_mod("HavocConditionManager/scripts/mods/HavocConditionManager/condition_manager_view/paging")
    for level in (1,5,10):
        L.execute('view._hcm_page=3; view._hcm_coarse_advanced=false; view._hcm_choice=nil; refresh()')
        L.execute('edit("native_global_value","'+str(level)+'")')
        assert len(L.globals().view._hcm_ui.sliders)==1
        layouts[lang+"_intensity-"+str(level)]=plain_items(L.globals().view._hcm_ui)
    L.execute('click("native_advanced_toggle")')
    for group in ("map","hordes","trickle","specials","encounters","pacing"):
        L.execute('view._hcm_page=3; view._hcm_choice=nil; view._hcm_offsets={}')
        L.globals().view._hcm_coarse_group=group
        L.globals().refresh()
        layouts[lang+"_coarse-"+group]=plain_items(L.globals().view._hcm_ui)
    for name,setup in {
        "parameters":'view._hed_family="specials"; view._hed_entry="specials/default_specials/1"; view._hed_path={}; view._hed_item="max_alive_specials"; view._hed_tab="parameters"',
        "composition":'view._hed_family="hordes"; view._hed_entry="hordes/default_horde/5"; view._hed_path={}; view._hed_tab="composition"; view._hed_item=nil',
        "rules":'view._hed_family="specials"; view._hed_entry="specials/default_specials/1"; view._hed_path={}; view._hed_tab="rules"; view._hed_item=nil',
        "presets":'view._hed_tab="presets"',
    }.items():
        L.execute('view._hcm_page=4; view._hcm_choice=nil; view._hcm_offsets={};'+setup)
        if name=="composition":
            L.execute('for _,e in ipairs(A.entries) do if e.family=="hordes" then for _,i in ipairs(e.items) do if i.kind=="composition" then view._hed_entry=e.id; view._hed_item=i.id; view._hed_path={unpack(i.path,1,#i.path-1)}; break end end if view._hed_item then break end end end')
        if name=="rules":
            L.execute('mods.HavocEnemyDirector.set_rule("specials/default_specials/1","encounter",{mode="append",match="all",clauses={{condition="load_max",value=55},{condition="monster_idle"},{condition="stage",value="build_up_tension"}}})')
        if name=="presets":
            # Filesystem boundary only. Preset data is captured by the actual codec.
            L.execute('mods.HavocEnemyDirector.presets.list=function() return {{file="Example.json",name="Example",document=mods.HavocEnemyDirector.presets.capture("Example")}} end')
        L.globals().refresh()
        layouts[lang+"_"+name]=plain_items(L.globals().view._hcm_ui)
    L.execute('view._hed_tab="parameters"; mods.HavocEnemyDirector.cleanup_template_ui()')
# Additional native identifiers, roamer seed and opened choice menus.
for lang in ("en","zh-cn","zh-tw"):
    L.globals().test_language=lang
    L.globals().Paging=load_mod("HavocConditionManager/scripts/mods/HavocConditionManager/condition_manager_view/paging")
    for name,setup in {
        "map-seed":'view._hed_family="roamers"; view._hed_entry=nil; view._hed_path={}; view._hed_tab="parameters"; view._hed_item=nil',
        "mission-node":'view._hed_family="mission_events"; view._hed_entry=nil; view._hed_path={}; view._hed_tab="parameters"; view._hed_item=nil',
        "long-template":'local longest; for _,e in ipairs(A.entries) do if #e.items>0 and (not longest or #e.id>#longest.id) then longest=e end end; view._hed_family=longest.family; view._hed_entry=longest.id; view._hed_path={}; view._hed_tab="parameters"; view._hed_item=nil',
    }.items():
        L.execute('view._hcm_page=4; view._hcm_choice=nil; view._hcm_offsets={};'+setup)
        L.globals().refresh(); layouts[lang+"_"+name]=plain_items(L.globals().view._hcm_ui)
        if name=="long-template":
            L.execute('click("hed_master")'); layouts[lang+"_template-menu"]=plain_items(L.globals().view._hcm_ui)
    L.execute('view._hcm_choice=nil; refresh(); click("hed_tab_presets"); click("hed_reset_all"); assert(view._hed_library.reset_pending); click("hed_reset_all"); assert(not next(mods.HavocEnemyDirector.peek_config().patches) and not next(mods.HavocEnemyDirector.peek_config().rules)); click("template_back")')
# Exercise slider passes at desktop and scaled resolutions, including a full drag.
L.execute("""
view._hcm_page=3; view._hcm_coarse_group="pacing"; refresh()
for _,d in ipairs(S.coarse) do assert(d.max==10) end
edit("native_global_value","5")
assert(B:get("native_configuration_v3").horde_size==1.1 and B:get("native_configuration_v3").patrols==3 and B:get("native_configuration_v3").special_slots==2)
edit("native_global_value","10")
assert(B:get("native_configuration_v3").horde_size==1.25 and B:get("native_configuration_v3").patrols==6 and B:get("native_configuration_v3").special_slots==3)
edit("native_recovery_duration_value","2")
assert(find("native_global_value").text==B:localize("native_mixed"))
-- Confirming 1 in a mixed setup must apply, even though 1 is the entry placeholder.
edit("native_global_value","1")
for _,value in pairs(B:get("native_configuration_v3")) do assert(value==1) end
local function drag(target,scale)
 local widget=view._widgets_by_name.hcm_slider_1;local content=widget.content;content.track_hotspot.parent=content
 local position={505,236};local ratio=(target-1)/9
 local input={get=function(_,key) if key=="left_hold" then return true elseif key=="cursor" then return {(position[1]+23+ratio*965)*scale,250*scale} end end}
 local renderer={input_service=input,inverse_scale=1/scale,dt=.016}
 local logic
 for _,p in ipairs(widget.passes) do if p.pass_type=="logic" and not p.style_id then logic=p.value;break end end
 assert(logic)
 content.track_hotspot.on_pressed=true;logic({},renderer,{},content,position,{1015,46})
 Paging.slider.update(view,input);content.track_hotspot.on_pressed=false
 input.get=function() return false end;logic({},renderer,{},content,position,{1015,46})
 Paging.slider.update(view,input);refresh()
 local profile=B:io_dofile("HavocConditionManager/scripts/mods/HavocConditionManager/intensity_profile");assert(profile.match(B:get("native_configuration_v3"))==target)
end
drag(5,1);drag(10,2);drag(1,.8)
edit("native_recovery_duration_value","10")
assert(B:get("native_configuration_v3").recovery_duration==10)
assert(find("native_global_value").text==B:localize("native_mixed"))
edit("native_global_value","5")
local input={get=function() return false end}
-- A numeric popup blocks the underlying sliders.
click("native_global_value");local before=B:get("native_configuration_v3").horde_size
Paging.slider.update(view,input);assert(B:get("native_configuration_v3").horde_size==before)
Paging.numeric.cancel(view);refresh()
for _,item in ipairs(view._hcm_ui.items) do assert(not item.key:find("native_reset",1,true)) end
""")
print("Coordinated 1–10 intensity profiles, individual 10x controls, custom state, actual slider drag at three scales and modal blocking: PASS")
for lang in ("en","zh-cn","zh-tw"):
    L.globals().test_language=lang
    L.globals().Paging=load_mod("HavocConditionManager/scripts/mods/HavocConditionManager/condition_manager_view/paging")
    sources=[("pacing","native_global_label")]+[(d.group,"native_"+d.id+"_label") for _,d in L.globals().S.coarse.items()]
    for group,key in sources:
        L.globals().view._hcm_coarse_group=group
        L.execute('view._hcm_page=3; refresh()')
        L.globals().hover_key=key
        L.execute('local item,w=find(hover_key); w.content.hotspot.is_hover=true; Paging.help.update(view); assert(view._hcm_hover_help and view._hcm_hover_help.key==hover_key)')
        tip=L.globals().view._hcm_hover_help; x,y,w,h=tip.x,tip.y,tip.w,tip.h
        assert y>=212 and y+h<=961 and x+w<=1810,(lang,key,x,y,w,h)
        records=plain_items(L.globals().view._hcm_ui)+[dict(key='tooltip_box',x=x,y=y,w=w,h=h,text='',tooltip=True,overlay=True),dict(key='tooltip_title',x=x+8,y=y+14,w=w-16,h=32,text=tip.title,font=24,color='gold',overlay=True),dict(key='tooltip_text',x=x+8,y=y+58,w=w-16,h=h-70,text=tip.text,font=20,overlay=True)]
        layouts[lang+'_tooltip-'+key]=records
        L.execute('local item,w=find(hover_key); w.content.hotspot.is_hover=false; Paging.help.update(view); assert(not view._hcm_hover_help)')
out=CHECKS/"native-ui-layouts.json"
out.write_text(json.dumps(layouts,ensure_ascii=False,indent=2),encoding="utf-8")
print("Exported",len(layouts),"localized layouts:",out)

