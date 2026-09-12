# Run within integration_tests.py using the existing real-template Lua harness.
L.execute('Color=setmetatable({}, {__index=function() return function() return {255,200,200,200} end end})')
cache['scripts/managers/ui/ui_font_settings']=tbl({f'header_{i}':{'font_size':24,'font_type':'proxima_nova_bold'} for i in range(1,6)})
cache['scripts/settings/difficulty/danger_settings']=tbl([{'color':[255,200,200,200]} for _ in range(5)])
cache['scripts/settings/ui/ui_sound_events']=tbl({})
cache['scripts/utilities/ui/colors']=tbl({})
cache['scripts/ui/pass_templates/button_pass_templates']=L.eval('{default_button={{pass_type="hotspot",content_id="hotspot"},size={347,76}},terminal_button={{pass_type="hotspot",content_id="hotspot"}}}')
cache['scripts/ui/views/mission_board_view/mission_board_view_styles']=tbl({'difficulty_stepper_style':{}})
exec((work/'numeric_ui_support.py').read_text(encoding='utf-8'),globals())
# The coarse controls execute the actual game slider pass template.
cache['scripts/managers/ui/ui_font_settings']['list_button']=tbl({'font_size':22,'font_type':'proxima_nova_bold'})
cache['scripts/managers/ui/ui_resolution']=L.eval('{inverse_scale_vector=function(v,scale) return {v[1]*scale,v[2]*scale} end}')
cache['scripts/ui/pass_templates/list_header_templates']=tbl({'highlight_size_addition':0,'default_hotspot_style':{'anim_focus_speed':16}})
cache['scripts/managers/input/input_utils']=tbl({})
cache['scripts/ui/pass_templates/slider_pass_templates']=lua_file(game/'scripts/ui/pass_templates/slider_pass_templates.lua')
from PIL import ImageFont
metric_fonts={}
def help_height(renderer,text,font_type,size,bounds):
    font=metric_fonts.setdefault(size,ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',size))
    lines=0
    for paragraph in text.split('\n'):
        line=''
        for character in paragraph:
            if line and font.getlength(line+character)>bounds[1]: lines+=1;line=character
            else: line+=character
        lines+=1
    return lines*round(size*1.3)
cache['scripts/managers/ui/ui_renderer']['text_height']=help_height
paging=load_mod('HavocConditionManager/scripts/mods/HavocConditionManager/condition_manager_view/paging')
definitions=load_mod('HavocConditionManager/scripts/mods/HavocConditionManager/condition_manager_view/condition_manager_view_definitions')
L.globals().Paging=paging
L.globals().full_definitions=definitions
