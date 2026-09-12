local Widget=require("scripts/managers/ui/ui_widget")
local Renderer=require("scripts/managers/ui/ui_renderer")
local mod=get_mod("HavocConditionManager")
local Details=mod:io_dofile("HavocConditionManager/scripts/mods/HavocConditionManager/diy/diy_condition_details")
local Help={width=680,font=20,padding=20}
function Help.definition()
    return Widget.create_definition({
        {pass_type="rect",style_id="border",style={color={255,221,194,122},size={680,240}}},
        {pass_type="rect",style_id="body",style={color={255,4,7,5},size={676,236},offset={2,2,1}}},
        {pass_type="text",value_id="title",style_id="title",style={font_type="proxima_nova_bold",font_size=24,text_color={255,241,220,151},size={640,36},offset={20,14,2}}},
        {pass_type="text",value_id="description",style_id="description",style={font_type="proxima_nova_bold",font_size=20,text_color={255,226,232,220},size={640,170},offset={20,58,2}}},
    },"hcm_hover_help",{title="",description=""},{680,240})
end
function Help.hide(view)
    local w=view._widgets_by_name.hcm_hover_help
    if w then w.visible=false; w.alpha_multiplier=0 end
    view._hcm_hover_help=nil
end
function Help.show(view,item,page)
    local w=view._widgets_by_name.hcm_hover_help
    if not w then return end
    local current=view._hcm_hover_help
    if not page and current and current.key==item.key and current.raw==item.tooltip then return end
    local pages=Details.pages(item.tooltip,58,18)
    page=math.max(1,math.min(page or 1,#pages))
    local text=#pages==1 and item.tooltip or pages[page].."\n\n"..Details.word("more",mod,page,#pages).."  ·  "..Details.word("scroll_help",mod)
    local width=Help.width; local inner=width-40
    local renderer=view._ui_renderer
    local height=Renderer.text_height(renderer,text,"proxima_nova_bold",Help.font,{inner,1000})+110
    height=math.max(150,height)
    local x=math.max(110,math.min(item.x+item.w+12,1810-width))
    local y=math.max(212,math.min(item.y+item.h+8,961-height))
    view:_set_scenegraph_position("hcm_hover_help",x,y,65)
    view:_set_scenegraph_size("hcm_hover_help",width,height)
    w.content.title=item.tooltip_title or item.text; w.content.description=text
    w.style.border.size={width,height}; w.style.body.size={width-4,height-4}
    w.style.description.size={inner,height-78}
    w.visible=true; w.alpha_multiplier=1
    view._hcm_hover_help={key=item.key,x=x,y=y,w=width,h=height,title=w.content.title,text=text,raw=item.tooltip,item=item,page=page,pages=#pages}
end
function Help.scroll(view,direction)
    local current=view._hcm_hover_help
    if not current or current.pages<2 then return false end
    Help.show(view,current.item,current.page+direction)
    return true
end
function Help.update(view)
    local ui=view._hcm_ui; local hovered
    if ui and not ui.popup and not view._input_disabled then
        for _,w in ipairs(ui.sliders or {}) do if w.content.drag_active then Help.hide(view); return end end
        for _,target in ipairs(ui.help_targets) do
            local hotspot=target.hotspot
            if hotspot.is_hover and not hotspot.disabled then hovered=target.item; break end
        end
    end
    if hovered then Help.show(view,hovered) else Help.hide(view) end
end
return Help
