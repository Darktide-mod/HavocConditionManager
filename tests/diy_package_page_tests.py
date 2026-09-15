"""Automatic read-only built-ins, external packages and real isolated folder I/O."""
from native_ui_tests import *

for name, stem in [('Schema','diy_schema'),('Codec','diy_codec'),('Catalog','diy_catalog'),('Base','diy_library'),('Files','diy_files'),('Examples','diy_examples'),('Packages','diy_packages'),('Hash','diy_sha256'),('Library','diy_package_library'),('Details','diy_condition_details')]:
    L.globals()[name] = load_mod('HavocConditionManager/scripts/mods/HavocConditionManager/diy/' + stem)

L.execute(r'''
busy=false;template_loads=0
Bundled=B:io_dofile('HavocConditionManager/scripts/mods/HavocConditionManager/diy/diy_bundled')
B.diy_api={status=function()return {network='offline'}end}
B.diy_library=Library.new(B,'conditions',Catalog,Schema,Codec,Files,Base,Packages,Hash,{name='HavocConditionManager',busy=function()return busy end,bundled=function()
    template_loads=template_loads+1
    return {{name='HavocConditionManager',builtin=true,directory='mods/HavocConditionManager/diy/packages',files=assert(Bundled.read(B,'HavocConditionManager',Codec,Packages))}}
end})
assert(#B.diy_library.document.entries==1 and #B.diy_library.files==1 and template_loads==1,'No healing loads automatically')
assert(B.diy_library.package_builtin('starter-conditions-no_healing'))
assert(not B.diy_library.toggle_package('starter-conditions-no_healing'))
local fs=assert(Files.new(require('ffi'),'HavocConditionManager'))
assert(#assert(fs.list_packages(Packages.id))==0,'No built-in file may be extracted')
local pack=B.diy_library.packages['starter-conditions-no_healing']
local api=Packages.new(Schema,Codec,Hash)
assert(fs.write_package('external-medical',api.from_document(pack.document,'external-medical',true),Packages.id,Packages.path))
assert(B.diy_library.scan() and #B.diy_library.files==2)
view._hcm_page=5;refresh()
for _,item in ipairs(view._hcm_ui.items)do assert(item.key~='diy_extract_templates')end
assert(not B.diy_library.options.enabled and #B.diy_library.options.selected==0,'Loading does not choose gameplay effects')
for _,package in pairs(B.diy_library.packages)do assert(#package.document.entries==1 and package.manifest.version==2)end
function custom_key(suffix)
    for _,entry in ipairs(B.diy_library.document.entries)do if B.diy_library.entry_sources[entry.id].entry_id==suffix then return 'condition_'..entry.id,entry.id end end
    error(suffix)
end
assert(Details.clean('{#color(1,2,3)}正文{#reset()}\n `test`')=='正文\ntest')
''')

directory = Path(L.globals().B.diy_library.directory()[0])
target = directory / 'starter-conditions-no_healing'
source = PROJECT / 'src/HavocConditionManager/diy/packages/starter-conditions-no_healing'
import shutil
shutil.copytree(source,target)
original = (target / 'definitions.json').read_bytes()
changed = json.loads(original)
changed['entries'][0]['name']['zh-cn'] = '临时修改名称'
(target / 'definitions.json').write_text(json.dumps(changed, ensure_ascii=False), encoding='utf-8')
(target / 'old-file.txt').write_text('stale', encoding='utf-8')
L.execute("assert(B.diy_library.scan()); assert(#B.diy_library.files==2 and B.diy_library.shadowed_packages['starter-conditions-no_healing'])")
assert (target / 'definitions.json').read_bytes() != original
assert (target / 'old-file.txt').exists()
assert (source / 'definitions.json').read_bytes() == original

result = {}
for lang in ('en', 'zh-cn', 'zh-tw'):
    L.globals().test_language = lang
    L.globals().Paging = load_mod('HavocConditionManager/scripts/mods/HavocConditionManager/condition_manager_view/paging')
    L.execute(r'''
    view._current.havoc_circumstances={};view._hcm_page=2;view._hcm_condition_filter='custom';view._hcm_offsets={};refresh()
    local expected={'filter_havoc','filter_maelstrom','filter_event','filter_custom','filter_all','filter_selected'}
    local actual={};for _,item in ipairs(view._hcm_ui.items)do if item.key:match('^filter_')then actual[#actual+1]=item.key end end
    assert(table.concat(expected,',')==table.concat(actual,','))
    assert(B.diy_library.set_options({enabled=false,selected={}}));refresh();click('select_all')
    assert(B.diy_library.options.enabled and #B.diy_library.options.selected==2)
    assert(#view._current.havoc_circumstances==0,'Custom IDs must not enter the native circumstance list')
    click('filter_selected')
    local count=0
    for _,item in ipairs(view._hcm_ui.items)do if item.key:match('^condition_')then
        count=count+1;assert(item.tooltip and #item.tooltip>40)
        assert(not item.tooltip:find('starter%-conditions') and not item.tooltip:find('power_level_modifier',1,true) and not item.tooltip:find('{#',1,true))
    end end
    assert(count==2,'One built-in and one external package are shown exactly once')
    click('filter_all');view._hcm_offsets.conditions=#test_settings.order.havoc_circumstances;refresh()
    local found=false;for _,item in ipairs(view._hcm_ui.items)do if item.key:match('^condition_') and B.diy_library.entry_sources[item.key:sub(11)] then found=true end end
    assert(found,'The all filter includes loaded DIY entries')
    click('filter_custom');refresh()
    ''')
    result[lang + '_main-diy'] = plain_items(L.globals().view._hcm_ui)
    L.execute(r'''
    local key,id=custom_key('no_healing')
    for i,entry in ipairs(B.diy_library.document.entries)do if entry.id==id then view._hcm_offsets.conditions=math.max(0,i-15);break end end
    refresh();local item,w=find(key);w.content.hotspot.is_hover=true;Paging.help.update(view)
    assert(view._hcm_hover_help and view._hcm_hover_help.y+view._hcm_hover_help.h<=961)
    ''')
    tip = L.globals().view._hcm_hover_help
    records = plain_items(L.globals().view._hcm_ui)
    records += [dict(key='tooltip_box',x=tip.x,y=tip.y,w=tip.w,h=tip.h,text='',tooltip=True,overlay=True),dict(key='tooltip_title',x=tip.x+8,y=tip.y+14,w=tip.w-16,h=32,text=tip.title,font=24,color='gold',overlay=True),dict(key='tooltip_text',x=tip.x+8,y=tip.y+58,w=tip.w-16,h=tip.h-70,text=tip.text,font=20,overlay=True)]
    result[lang+'_rage-hover'] = records
    L.execute(r'''
    local item={key='long',text='Long',x=120,y=820,w=500,h=48,tooltip=string.rep('完整说明 description. ',400)}
    Paging.help.show(view,item);assert(view._hcm_hover_help.pages>1 and view._hcm_hover_help.y+view._hcm_hover_help.h<=961)
    assert(Paging.help.scroll(view,1) and view._hcm_hover_help.page==2)
    view._hcm_page=5;view._hcm_offsets={};refresh()
    local before=#B.diy_library.options.selected;click('diy_package_1');assert(#B.diy_library.options.selected==before)
    for _,item in ipairs(view._hcm_ui.items)do assert(not item.checkbox,'The management page must not select gameplay conditions')end
    local _,rage_id=custom_key('no_healing')
    view._diy_inspect_file=B.diy_library.entry_sources[rage_id].package_id;refresh()
    ''')
    result[lang + '_manager'] = plain_items(L.globals().view._hcm_ui)
    L.execute(r'''
    busy=true;click('diy_scan');assert(not B.diy_library.last_error)
    view._hcm_page=2;view._hcm_condition_filter='custom';view._hcm_offsets={};refresh()
    for _,item in ipairs(view._hcm_ui.items)do if item.key:match('^condition_')then assert(not item.action and item.tooltip)end end
    busy=false
    ''')

out = CHECKS / 'diy-main-manager-layouts.json'
out.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print('HCM DIY filters, priority order, selection isolation, management inspection, bounded hover, direct built-ins and preserved external copies in three languages: PASS')
