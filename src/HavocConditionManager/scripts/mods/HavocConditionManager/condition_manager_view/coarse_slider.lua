local mod=get_mod("HavocConditionManager")
local Widget=require("scripts/managers/ui/ui_widget")
local Templates=require("scripts/ui/pass_templates/slider_pass_templates")
local Slider={count=1}
local group_counts={}
for _,control in ipairs(mod.template_schema.coarse) do
    group_counts[control.group]=(group_counts[control.group] or 0)+1
    Slider.count=math.max(Slider.count,group_counts[control.group]+1)
end
function Slider.definition(node,width)
    local passes=table.clone_instance(Templates.value_slider(width,46,0,true))
    for _,pass in ipairs(passes) do
        if pass.value_id=="value_text" or pass.value_id=="slider_action_gamepad" then pass.visibility_function=function() return false end end
        if pass.value and type(pass.value)=="string" and pass.value:find("slider_handle",1,true) then
            local previous=pass.visibility_function
            pass.visibility_function=function(c,s) return not c.hcm_mixed and (not previous or previous(c,s)) end
        end
        if pass.style_id=="slider_track_left" then pass.visibility_function=function(c) return not c.hcm_mixed end end
    end
    passes[#passes+1]={pass_type="rect",style_id="baseline",style={size={2,16},offset={0,15,4},color={160,221,194,122}},
        change_function=function(c,s) local d=c.hcm_spec; if d then s.offset[1]=23+(1-d.min)/(d.max-d.min)*(width-50) end end}
    return Widget.create_definition(passes,node,{slider_value=0,highlight_progress=0,area_length=width-50}, {width,46})
end
local function cancel_widget(w)
    if not w then return false end
    local c=w.content;local had=c.drag_active or c.hcm_dragging
    c.drag_active=nil;c.hcm_dragging=nil;c.input_offset=nil
    if c.hcm_spec then c.slider_value=(c.hcm_spec.value-c.hcm_spec.min)/(c.hcm_spec.max-c.hcm_spec.min) end
    return had
end
function Slider.cancel(view)
    local had=false
    for i=1,Slider.count do had=cancel_widget(view._widgets_by_name["hcm_slider_"..i]) or had end
    if had and IS_WINDOWS and Window then Window.set_clip_cursor(false) end
    return had
end
function Slider.refresh(view,ui,visible)
    local count=0; local cancelled=false; ui.sliders={}
    for _,item in ipairs(ui.items) do if item.slider then
        count=count+1; local name="hcm_slider_"..count; local widget=view._widgets_by_name[name]; local c=widget.content
        visible(widget,not item.blocked)
        view:_set_scenegraph_position(name,item.x,item.y,16)
        if c.hcm_key~=item.key then cancelled=cancel_widget(widget) or cancelled end
        c.hcm_key=item.key; c.hcm_spec=item.slider; c.hcm_value_key=item.value_key
        c.hcm_value_widget=ui.widgets_by_key[item.value_key]
        c.entry={disabled=item.blocked==true}; c.hotspot.disabled=item.blocked; c.track_hotspot.disabled=item.blocked
        c.hcm_mixed=item.slider.mixed and not c.drag_active
        c.step_size=item.slider.step/(item.slider.max-item.slider.min)
        if not c.drag_active and not c.hcm_dragging then c.slider_value=(item.slider.value-item.slider.min)/(item.slider.max-item.slider.min) end
        c.hcm_initial=c.slider_value
        c.slider_horizontal_offset=4+c.slider_value*(item.w-50)
        c.hcm_page=view._hcm_page
        ui.sliders[#ui.sliders+1]=widget
    end end
    for i=count+1,Slider.count do
        local widget=view._widgets_by_name["hcm_slider_"..i]
        cancelled=cancel_widget(widget) or cancelled;visible(widget,false)
    end
    if cancelled and IS_WINDOWS and Window then Window.set_clip_cursor(false) end
end
function Slider.update(view,input)
    local ui=view._hcm_ui
    if not ui or not ui.sliders then return end
    if ui.popup or view._input_disabled or input.is_null_service and input:is_null_service() then Slider.cancel(view); return end
    for _,widget in ipairs(ui.sliders) do
        local c=widget.content; local d=c.hcm_spec
        if c.hcm_page~=view._hcm_page then Slider.cancel(view); return end
        local value=math.max(d.min,math.min(d.max,d.min+c.slider_value*(d.max-d.min)))
        value=math.floor(value*10000+0.5)/10000
        if c.drag_active then
            c.hcm_dragging=true; c.hcm_mixed=false
            if c.hcm_value_widget then c.hcm_value_widget.content.text=d.format and d.format(value) or string.format("%.4g×",value) end
        elseif c.hcm_dragging or math.abs(c.slider_value-c.hcm_initial)>0.000001 then
            c.hcm_dragging=nil; c.hcm_initial=c.slider_value
            if value~=d.value or d.mixed then d.set(value); view._hcm_refresh=true end
        end
    end
end
return Slider
