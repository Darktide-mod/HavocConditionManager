"""Export only this project's actual UI definitions, without launching the game."""
from pathlib import Path
import argparse, json, re, runpy, sys
PROJECT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(PROJECT/'tests'))
from project_env import CHECKS
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--output',type=Path,default=CHECKS/'ui-layouts.json')
layout_output=parser.parse_args().output
globals().update(runpy.run_path(str(PROJECT/'tests/standalone_hcm_tests.py')))
result={}
L.execute('''
test_view={_widgets_by_name=table.clone_instance(full_definitions.widget_definitions),
    _options={havoc_theme_circumstance={{id="default",display_name="无特殊环境"},{id="darkness_01",display_name="停电"},
        {id="ventilation_purge_01",display_name="通风净化"},{id="toxic_gas_01",display_name="毒气"}}},
    _dropdown_widgets={},
    _spawn_multiplier_widgets={},_current={havoc_circumstances={}},_positions={}}
function test_view:_set_exclusive_focus_on_setting() end
function test_view:_persist_havoc_circumstances() mods.HavocConditionManager:set("havoc_circumstances_serialized",table.concat(self._current.havoc_circumstances,":")) end
function test_view:_condition_display_name(id) return test_settings.loc.havoc_circumstances[id] or id end
function test_view:_set_scenegraph_position(id,x,y,z) self._positions[id]={x,y,z} end
function test_view:_set_scenegraph_size(id,w,h) self._positions[id]=self._positions[id] or {}; self._positions[id].w=w; self._positions[id].h=h end
function find_control(key)
    for i,item in ipairs(test_view._hcm_ui.items) do if item.key==key then return item,test_view._widgets_by_name["hcm_control_"..i] end end
end
function click_control(key)
    local item,widget=find_control(key)
    assert(item and item.action and not widget.content.hotspot.disabled,"Unavailable control "..key)
    widget.content.hotspot.pressed_callback()
    Paging.refresh(test_view,test_settings)
end
test_view._current.havoc_theme_circumstance="default"
test_view._dropdown_widgets.havoc_theme_circumstance={content={hotspot={},entry={on_activated=function(value)
    test_view._current.havoc_theme_circumstance=value
    mods.SoloPlay:set("havoc_theme_circumstance",value)
end}}}
Paging.enter(test_view,test_settings)
''')
def plain_items(ui):
    fields=('key','x','y','w','h','text','font','fill','panel','selected','center','danger','color','checkbox','choice','expanded','upwards','overlay','blocked','text_right_padding')
    return [{key:item[key] for key in fields if item[key] is not None} for _,item in ui['items'].items()]
L.execute('''
-- Match the installed game's currently available event catalogue (latest console log).
require("scripts/settings/mutator/mutator_templates").mutator_gameplay_barren_odin=nil
test_view._current.havoc_circumstances={"hcm_auric_hounds","hcm_auric_monsters","hcm_auric_patrols"}
mods.HavocConditionManager:set("havoc_circumstances_serialized",table.concat(test_view._current.havoc_circumstances,":"))

test_view._hcm_condition_filter="maelstrom"
test_view._current.havoc_theme_circumstance="default"
test_view._hcm_offsets={}
''')
for lang in ('en','zh-cn','zh-tw'):
    L.globals().test_language=lang
    catalog=load_mod('HavocConditionManager/scripts/mods/HavocConditionManager/condition_catalog')
    L.globals().mods.HavocConditionManager.condition_catalog=catalog
    catalog.extend(settings)
    paging=load_mod('HavocConditionManager/scripts/mods/HavocConditionManager/condition_manager_view/paging')
    L.globals().Paging=paging
    labels={'en':['No special environment','Power supply interruption','Ventilation purge','Toxic gas'],
            'zh-cn':['无特殊环境','停电','通风净化','毒气'],
            'zh-tw':['無特殊環境','停電','通風淨化','毒氣']}[lang]
    L.globals().test_view._options.havoc_theme_circumstance=tbl([{'id':id,'display_name':name} for id,name in zip(['default','darkness_01','ventilation_purge_01','toxic_gas_01'],labels)])
    for page,name in [(2,'conditions'),(3,'multipliers')]:
        view=L.globals().test_view;view._hcm_page=page;view._hcm_choice=None;view._hcm_number=None;view._hcm_offsets=tbl({})
        paging.refresh(view,settings)
        result[lang+'_'+name]=plain_items(view._hcm_ui)
        if page==2:
            L.execute('click_control("environment")')
            result[lang+'_environment']=plain_items(view._hcm_ui)
            paging.close_choice(view)
assert result and all(not re.search(r'<ui_\d+>|%[dfs]',i['text']) for items in result.values() for i in items)
layout_output.parent.mkdir(parents=True,exist_ok=True)
layout_output.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print('Exported',len(result),'localized pages for',PROJECT.name)
