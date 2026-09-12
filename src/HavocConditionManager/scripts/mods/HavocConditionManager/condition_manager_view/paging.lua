local mod = get_mod("HavocConditionManager")
local language = mod:localize("ui_034")
local cached_paging = mod._condition_paging_cache
if cached_paging and cached_paging.language == language then return cached_paging.module end
local UIWidget = require("scripts/managers/ui/ui_widget")
local UISoundEvents = require("scripts/settings/ui/ui_sound_events")
local Templates = require("scripts/settings/circumstance/circumstance_templates")
local H = mod:io_dofile("HavocConditionManager/scripts/mods/HavocConditionManager/havoc_conditions")
local CoarseEditor = mod:io_dofile("HavocConditionManager/scripts/mods/HavocConditionManager/coarse_editor")
local DIY=mod:io_dofile("HavocConditionManager/scripts/mods/HavocConditionManager/diy/diy_library_ui")
local DIYSchema=mod:io_dofile("HavocConditionManager/scripts/mods/HavocConditionManager/diy/diy_schema")
local DIYEngine=mod:io_dofile("HavocConditionManager/scripts/mods/HavocConditionManager/diy/diy_engine")
local DIYExamples=mod:io_dofile("HavocConditionManager/scripts/mods/HavocConditionManager/diy/diy_examples")
local Details=mod:io_dofile("HavocConditionManager/scripts/mods/HavocConditionManager/diy/diy_condition_details")
local DIYManager=mod:io_dofile("HavocConditionManager/scripts/mods/HavocConditionManager/diy/diy_condition_manager")
local Paging = {control_count=220}
local Numeric = mod:io_dofile("HavocConditionManager/scripts/mods/HavocConditionManager/condition_manager_view/numeric_input")
local Slider=mod:io_dofile("HavocConditionManager/scripts/mods/HavocConditionManager/condition_manager_view/coarse_slider")
local Help=mod:io_dofile("HavocConditionManager/scripts/mods/HavocConditionManager/condition_manager_view/hover_help")
Paging.numeric=Numeric; Paging.slider=Slider; Paging.help=Help
local labels={mod:localize("ui_034"),mod:localize("ui_035"),mod:localize("ui_036"),mod:localize("ui_037")}
local colors={text={255,222,229,214},muted={255,151,167,152},gold={255,221,194,122},
    selected={245,51,70,44},normal={225,25,35,27},hover={250,49,62,42},danger={255,220,133,117},panel={220,15,23,19}}
local function clone(t) local r={} for k,v in pairs(t) do r[k]=v end return r end
local function color_into(target, source)
    for i=1,4 do target[i]=source[i] end
    return target
end
local unchecked_color={255,65,76,65}
local disabled_arrow_color={80,151,167,152}
local function clean(text) return tostring(text or ""):gsub("{#[^}]*}","") end
local function short_hint(text)
    local result={}
    for character in clean(text):gsub("\n"," "):gmatch(".[\128-\191]*") do
        if #result==150 then result[#result+1]="…"; break end
        result[#result+1]=character
    end
    return table.concat(result)
end
local function localized(key)
    if not key then return "" end
    local ok,value=pcall(Localize,key)
    if not ok or not value or value==key or value:find("unlocalized",1,true) then return "" end
    return clean(value)
end
local function visible(widget,value)
    if not widget then return end
    widget.visible=value; widget.alpha_multiplier=value and 1 or 0; widget.content.page_visible=value
    if widget.content.hotspot then widget.content.hotspot.disabled=not value end
end
Paging.set_visible=visible
local function control_definition(node)
    return UIWidget.create_definition({
        {pass_type="hotspot",content_id="hotspot",style_id="hotspot",style={size={1,1}}},
        {pass_type="logic",value=function(pass,renderer,style,c)
            if c.hotspot.hcm_hold_callback then c.hotspot.hcm_hold_callback(c.hotspot,renderer.dt) end
        end},
        {pass_type="texture",value="content/ui/materials/backgrounds/default_square",style_id="background",style={color=clone(colors.normal),size={1,1}},
            visibility_function=function(c) return c.fill end,
            change_function=function(c,s)
                color_into(s.color,c.selected and colors.selected or c.hotspot.is_hover and c.actionable and colors.hover or c.panel and colors.panel or colors.normal)
            end},
        {pass_type="texture",value="content/ui/materials/buttons/background_selected",style_id="highlight",
            style={color={55,151,167,122},size={1,1},offset={0,0,1}},
            visibility_function=function(c) return c.fill and not c.panel and (c.selected or c.hotspot.is_hover and c.actionable) end},
        {pass_type="texture",value="content/ui/materials/frames/hover",style_id="frame",
            style={color={120,151,167,152},size={1,1},offset={0,0,1}},
            visibility_function=function(c) return c.fill and not c.panel and (c.choice or c.numeric or c.hotspot.is_hover and c.actionable) end},
        {pass_type="text",value="",style_id="check",style={font_type="proxima_nova_bold",font_size=26,
            text_color=clone(colors.gold),text_horizontal_alignment="center",text_vertical_alignment="center",size={32,44},offset={8,0,3}},
            visibility_function=function(c) return c.checkbox end,
            change_function=function(c,s) color_into(s.text_color,c.selected and colors.gold or unchecked_color) end},
        {pass_type="rotated_texture",value="content/ui/materials/buttons/arrow_01",style_id="choice_arrow",
            style={angle=math.pi/2,pivot={9,9},size={18,18},offset={0,0,3},color=clone(colors.gold)},
            visibility_function=function(c) return c.choice end},
        {pass_type="rect",style_id="accent",style={color=clone(colors.gold),size={3,1},offset={0,0,1}},visibility_function=function(c) return c.selected end},
        {pass_type="rect",style_id="edge",style={color={160,70,87,62},size={1,1},offset={0,0,1}},visibility_function=function(c) return c.fill and not c.panel end},
        {pass_type="text",style_id="text",value_id="text",value="",style={font_type="proxima_nova_bold",font_size=22,
            text_color=clone(colors.text),text_horizontal_alignment="left",text_vertical_alignment="center",size={1,1},offset={12,0,2}}},
    },node,{text=""},{1,1})
end
local function arrow_definition(node,flip)
    return UIWidget.create_definition({
        {pass_type="rotated_texture",style_id="arrow",value="content/ui/materials/buttons/arrow_01",style={
            size={64,64},offset={8,8,1},color=clone(colors.text),angle=flip and math.pi or 0,pivot={32,32}},
            change_function=function(c,s) color_into(s.color,c.hotspot.disabled and disabled_arrow_color or c.hotspot.is_hover and colors.gold or colors.text) end},
        {pass_type="hotspot",content_id="hotspot",style_id="hotspot",style={size={80,80}}},
    },node,nil,{80,80})
end
Paging.extend_definitions=function(definitions)
    local nodes,widgets=definitions.scenegraph_definition,definitions.widget_definitions
    nodes.hcm_number_input={parent="screen",horizontal_alignment="left",vertical_alignment="top",size={236,50},position={0,0,50}}
    widgets.hcm_number_input=Numeric.definition()
    -- One immutable pass/style template; UIWidget.init copies the mutable
    -- content and styles for each control, just like native button templates.
    for i=1,Slider.count do
        local id="hcm_slider_"..i; local width=i==1 and 1015 or 760
        nodes[id]={parent="screen",horizontal_alignment="left",vertical_alignment="top",size={width,46},position={0,0,16}}
        widgets[id]=Slider.definition(id,width)
    end
    nodes.hcm_hover_help={parent="screen",horizontal_alignment="left",vertical_alignment="top",size={680,240},position={0,0,65}}
    widgets.hcm_hover_help=Help.definition()
    local control_template=control_definition("hcm_control_1")
    for i=1,Paging.control_count do
        local id="hcm_control_"..i
        nodes[id]={parent="screen",horizontal_alignment="left",vertical_alignment="top",size={1,1},position={0,0,15}}
        widgets[id]=clone(control_template)
        widgets[id].scenegraph_id=id
    end
    for _,side in ipairs({"previous","next"}) do
        local id="hcm_"..side
        nodes[id]={parent="screen",horizontal_alignment="left",vertical_alignment="top",size={80,80},position={side=="previous" and 12 or 1828,500,20}}
        widgets[id]=arrow_definition(id,side=="previous")
    end
    nodes.hcm_popup_blocker={parent="screen",horizontal_alignment="left",vertical_alignment="top",size={1920,1080},position={0,0,35}}
    widgets.hcm_popup_blocker=UIWidget.create_definition({
        {pass_type="hotspot",content_id="hotspot",style_id="hotspot",style={size={1920,1080}}},
    },"hcm_popup_blocker",nil,{1920,1080})
    local function place(id,x,y,w,h)
        local n=nodes[id]
        n.parent="screen"; n.horizontal_alignment="left"; n.vertical_alignment="top"
        n.position={x,y,2}; n.size={w,h}
    end
    place("normal_section",105,220,550,690)
    place("havoc_section",690,220,1130,690)
    place("normal_start",207,917,347,76)
    place("havoc_randomize",887,917,347,76)
    place("havoc_start",1454,917,347,76)
    place("warn_info_box",1285,856,515,40)
    place("normal_difficulty",138,735,483,160)
    place("havoc_modifiers_grid",705,634,510,250)
    place("havoc_modifier_lock",1010,587,205,36)
    place("havoc_difficulty_badge",1295,390,160,128)
    place("havoc_difficulty",1455,432,350,64)
    local function text_style(id,key,offset,size,font)
        local s=widgets[id].style[key]
        s.offset=offset; s.size=size; s.font_size=font; s.text_color=clone(colors.text)
    end
    text_style("normal_title","normal_title",{15,0,0},{510,34},26)
    text_style("havoc_title","havoc_title",{15,0,0},{510,34},26)
    text_style("havoc_modifier_label","havoc_modifier_label",{15,365,0},{285,36},22)
    local fields={normal_mission={120,294},normal_side_mission={120,408},normal_circumstance={120,522},normal_mission_giver={120,636},
        havoc_mission={705,294},havoc_faction={705,408},havoc_mission_giver={705,522},havoc_theme_circumstance={1295,294},havoc_difficulty_circumstance={1295,294}}
    for id,p in pairs(fields) do
        place(id,p[1],p[2],510,52)
        local label=widgets[id.."_label"]
        local label_node=id.."_heading"
        nodes[label_node]={parent="screen",horizontal_alignment="left",vertical_alignment="top",position={p[1],p[2]-34,2},size={510,28}}
        label.scenegraph_id=label_node
        text_style(id.."_label",id.."_label",{0,0,0},{510,28},22)
    end
    -- The full-screen background stretches; the 1920 x 1080 control canvas does not.
    for _,node in pairs(nodes) do
        if node.parent=="screen" and node~=nodes.hcm_popup_blocker then node.parent="hcm_layout" end
    end
    nodes.hcm_layout={parent="screen",horizontal_alignment="center",vertical_alignment="center",size={1920,1080},position={0,0,0}}
    return definitions
end

Paging.viewport=function(width,height)
    local scale=math.min(width/1920,height/1080)
    return {scale=scale,width=width/scale,height=height/scale,x=(width/scale-1920)/2,y=(height/scale-1080)/2}
end
Paging.fit=function(view)
    if not RESOLUTION_LOOKUP or not view._ui_scenegraph then return end
    local width,height=RESOLUTION_LOOKUP.width,RESOLUTION_LOOKUP.height
    if view._hcm_width==width and view._hcm_height==height and view._render_scale==math.min(width/1920,height/1080) then return end
    local viewport=Paging.viewport(width,height)
    view._hcm_width=width; view._hcm_height=height
    view:set_render_scale(viewport.scale)
    view:_set_scenegraph_size("hcm_popup_blocker",viewport.width,viewport.height)
    view._widgets_by_name.hcm_popup_blocker.style.hotspot.size={viewport.width,viewport.height}
    -- BaseView propagates this same scale to native dropdowns, grid and input legend.
    view:trigger_resolution_update()
end

-- Geometry and callbacks are shared by the live controls and layout verification.
local function builder(view)
    local ui={items={},view=view,scrolls={},choices={}}
    function ui:add(key,x,y,w,h,text,options)
        local item=options or {}; item.key=key; item.x=x; item.y=y; item.w=w; item.h=h; item.text=clean(text)
        self.items[#self.items+1]=item
        return item
    end
    function ui:text(key,x,y,w,h,text,font,color) return self:add(key,x,y,w,h,text,{font=font or 22,color=color}) end
    function ui:panel(key,x,y,w,h) return self:add(key,x,y,w,h,"",{fill=true,panel=true}) end
    function ui:button(key,x,y,w,h,text,action,selected,hint,danger)
        return self:add(key,x,y,w,h,text,{fill=true,action=action,selected=selected,hint=hint,center=true,danger=danger,color=not action and "muted" or nil})
    end
    function ui:checkbox(key,x,y,w,h,text,action,checked,hint)
        local item=self:button(key,x,y,w,h,text,action,checked,hint)
        item.checkbox=true; item.center=false
        return item
    end
    function ui:choice(key,x,y,w,h,value,options,choose,hint)
        local label
        for _,option in ipairs(options) do if option[1]==value then label=option[2] end end
        local item=self:button(key,x,y,w,h,label or tostring(value),choose and function()
            view:_set_exclusive_focus_on_setting(nil)
            view._hcm_choice=view._hcm_choice~=key and key or nil
        end,false,hint)
        item.choice=choose~=nil; item.center=false; item.font=20
        if choose then self.choices[key]={anchor=item,value=value,options=options,choose=choose} end
        return item
    end
    function ui:repeat_button(key,x,y,w,h,text,action)
        local item=self:button(key,x,y,w,h,text,action)
        item.repeatable=action~=nil
        return item
    end
    function ui:number(key,x,y,w,h,text,spec,font)
        local item=self:button(key,x,y,w,h,text,nil,false,spec and mod:localize("ui_038") or nil)
        item.font=font or 20; item.color=spec and "gold" or "muted"
        if spec then item.number=spec; item.action=function() Numeric.open(view,item) end end
        return item
    end
    function ui:stepper(key,x,y,w,label,value,adjust,hint,spec)
        self:add(key.."_label",x,y,w-150,44,label,{fill=true,font=20,hint=hint})
        self:repeat_button(key.."_minus",x+w-148,y,34,44,"−",adjust and function() adjust(-1) end)
        self:number(key.."_value",x+w-112,y,76,44,value,spec)
        self:repeat_button(key.."_plus",x+w-34,y,34,44,"+",adjust and function() adjust(1) end)
    end
    function ui:window(key,total,capacity,step,x,y,w)
        view._hcm_offsets=view._hcm_offsets or {}
        local offset=math.max(0,math.min(view._hcm_offsets[key] or 0,math.max(0,total-capacity)))
        view._hcm_offsets[key]=offset
        local function scroll(direction)
            view._hcm_offsets[key]=math.max(0,math.min(offset+direction*step,math.max(0,total-capacity)))
            view._hcm_refresh=true
        end
        if total>capacity then
            self:button(key.."_up",x+w-96,y,44,32,"↑",offset>0 and function() scroll(-1) end)
            self:button(key.."_down",x+w-48,y,44,32,"↓",offset+capacity<total and function() scroll(1) end)
            self:text(key.."_range",x,y,w-100,32,string.format("%d–%d / %d",offset+1,math.min(offset+capacity,total),total),18,"muted")
        end
        self.scrolls[key]=scroll
        return offset
    end
    return ui
end
Paging.new_builder=builder
local function go(view,page)
    Numeric.cancel(view); Slider.cancel(view); Help.hide(view)
    view:_set_exclusive_focus_on_setting(nil)
    view._hcm_choice=nil
    view._hcm_page=page; view._hcm_refresh=true
end
local function active_custom_count()
    local library=mod.diy_library
    if not library or not library.options.enabled then return 0 end
    local selected={};for _,id in ipairs(library.options.selected)do selected[id]=true end
    local count=0;for _,entry in ipairs(library.document.entries)do
        if selected[entry.id] and entry.enabled and library.eligible(entry) then count=count+1 end
    end
    return count
end
local function conditions(view,settings,ui)
    local filter=view._hcm_condition_filter or "havoc"
    local all=settings.order.havoc_circumstances
    local ids,counts={},{}
    local library=mod.diy_library
    local custom=library and library.document.entries or {}
    local picked={};for _,id in ipairs(library and library.options.selected or {})do picked[id]=true end
    local custom_by_id={}
    for _,entry in ipairs(custom)do custom_by_id[entry.id]=entry end
    local selected_count=#view._current.havoc_circumstances+active_custom_count()
    for _,id in ipairs(all) do
        local category=mod.condition_catalog.category(id)
        counts[category or "other"]=(counts[category or "other"] or 0)+1
        if filter=="all" or filter==category or filter=="selected" and H.contains(view._current.havoc_circumstances,id) then ids[#ids+1]=id end
    end
    for _,entry in ipairs(custom)do
        if filter=="all" or filter=="custom" or filter=="selected" and library.options.enabled and picked[entry.id] and entry.enabled and library.eligible(entry) then ids[#ids+1]=entry.id end
    end
    counts.custom=#custom
    for i,f in ipairs({{"havoc",Details.word("havoc",mod)},{"maelstrom",Details.word("maelstrom",mod)},{"event",Details.word("event",mod)},{"custom",Details.word("diy",mod)},{"all",Details.word("all",mod)},{"selected",Details.word("active",mod)}}) do
        local count=f[1]=="all" and #all+#custom or f[1]=="selected" and selected_count or counts[f[1]] or 0
        local item=ui:button("filter_"..f[1],115+(i-1)*172,222,160,42,f[2].." "..count,function() view._hcm_condition_filter=f[1]; view._hcm_offsets.conditions=0 end,filter==f[1])
        item.font=19
    end
    ui:button("select_all",1334,222,218,42,filter=="all" and mod:localize("ui_041") or mod:localize("ui_042"),function()
        local selected=view._current.havoc_circumstances
        local diy_selected={};for id in pairs(picked)do diy_selected[#diy_selected+1]=id end
        local enable_custom=false
        for _,id in ipairs(ids) do
            local entry=custom_by_id[id]
            if entry then
                if entry.enabled and library.eligible(entry) then enable_custom=true end
                if not picked[id] and entry.enabled and library.eligible(entry) then diy_selected[#diy_selected+1]=id end
            else selected=H.add(selected,id,settings.lookup.havoc_circumstances) end
        end
        if library and library.can_edit() then library.set_options({selected=diy_selected,enabled=enable_custom or library.options.enabled}) end
        view._current.havoc_circumstances=selected; view:_persist_havoc_circumstances()
    end)
    ui:button("clear_all",1564,222,240,42,filter=="all" and mod:localize("ui_043") or mod:localize("ui_044"),function()
        local selected=view._current.havoc_circumstances
        local remove={};for _,id in ipairs(ids) do
            if custom_by_id[id] then remove[id]=true else selected=H.remove(selected,id,0) end
        end
        if library and library.can_edit() then
            local keep={};for _,id in ipairs(library.options.selected)do if not remove[id] then keep[#keep+1]=id end end
            library.set_options({selected=keep})
        end
        view._current.havoc_circumstances=selected; view:_persist_havoc_circumstances()
    end,false,nil,true)
    local environment_options={}
    for _,option in ipairs(view._options and view._options.havoc_theme_circumstance or {}) do
        environment_options[#environment_options+1]={option.id,option.display_name}
    end
    ui:text("environment_label",115,278,170,48,mod:localize("ui_045"),23)
    ui:choice("environment",295,276,510,52,view._current.havoc_theme_circumstance or "default",environment_options,
        function(value)
            local native=view._dropdown_widgets.havoc_theme_circumstance
            -- Reuse the original mission-compatible options and persistence callback.
            native.content.entry.on_activated(value,native.content.entry)
        end,mod:localize("ui_046"))
    ui:text("environment_help",835,276,958,52,mod:localize("ui_047"),20,"muted")
    if library then
        local toggle=ui:checkbox("diy_enabled",115,334,350,32,Details.word(library.options.enabled and "enabled" or "disabled",mod),
            library.can_edit() and function()library.set_options({enabled=not library.options.enabled})end,library.options.enabled)
        toggle.font=18;toggle.tooltip=Details.word("master_help",mod)
        ui:text("diy_selected_count",480,334,580,32,Details.word("selected",mod,#library.options.selected),18,"muted")
    end
    local offset=ui:window("conditions",#ids,27,3,1080,334,724)
    if #ids==0 then ui:text("empty",120,390,1500,90,filter=="custom" and Details.word("empty",mod) or mod:localize("ui_048"),23,"muted") end
    for i=1,math.min(27,#ids-offset) do
        local id=ids[offset+i]
        local custom_entry=custom_by_id[id]
        local template=Templates[id] or {}
        local description=custom_entry and Details.describe(custom_entry,library,DIYSchema,mod) or Details.clean(localized(template.ui and template.ui.description))
        local name=custom_entry and Details.name(custom_entry,DIYSchema,mod) or Details.clean(view:_condition_display_name(id))
        local is_selected=custom_entry and picked[id] or H.contains(view._current.havoc_circumstances,id)
        local category=custom_entry and Details.word("custom",mod) or mod.condition_catalog.labels[mod.condition_catalog.category(id)] or mod:localize("ui_049")
        local allowed=not custom_entry or library.can_edit() and (is_selected or custom_entry.enabled and library.eligible(custom_entry))
        local item=ui:checkbox("condition_"..id,115+(i-1)%3*568,376+math.floor((i-1)/3)*57,552,48,
            name,allowed and function()
                if custom_entry then
                    local keep={};for _,selected in ipairs(library.options.selected)do if selected~=id then keep[#keep+1]=selected end end
                    if not is_selected then keep[#keep+1]=id end
                    library.set_options({selected=keep,enabled=not is_selected or library.options.enabled});return
                end
                local selected=view._current.havoc_circumstances
                view._current.havoc_circumstances=H.contains(selected,id) and H.remove(selected,id,0) or H.add(selected,id,settings.lookup.havoc_circumstances)
                view:_persist_havoc_circumstances()
            end,is_selected,name.."  ·  "..category)
        item.center=false; item.scroll="conditions"; item.text_right_padding=112
        item.tooltip_title=name;item.tooltip=description~="" and description or category
        ui:text("category_tag_"..id,item.x+436,item.y,112,48,category,17,"muted")
    end
    ui:panel("help_panel",105,901,1710,62)
    ui.default_hint=Details.word("next_mission",mod)
    ui:text("help",120,903,1680,58,ui.default_hint,19,"muted")
end
Paging.build=function(view,settings)
    local ui=builder(view)
    view._hcm_offsets=view._hcm_offsets or {}
    local director=get_mod("HavocEnemyDirector")
    if director and not director:is_enabled() then director=nil end
    local total=director and director.build_dashboard and 4 or 3
    local diy_page=mod.diy_library and total+1
    if diy_page then total=diy_page end
    view._hcm_page=math.max(1,math.min(view._hcm_page or 1,total))
    ui.page_count=total
    local tab_step=total>4 and 258 or 306
    local selected_count=#view._current.havoc_circumstances+active_custom_count()
    for i=1,total do ui:button("tab_"..i,105+(i-1)*tab_step,141,tab_step-14,52,i==diy_page and Details.word("manager",mod) or labels[i],function() go(view,i) end,view._hcm_page==i) end
    ui:text("page_indicator",1430,145,375,44,mod:localize("ui_066",view._hcm_page,total,selected_count),20,"muted")
    if view._hcm_page==1 then
        ui:panel("normal_panel",105,212,550,688); ui:panel("havoc_panel",690,212,550,688); ui:panel("environment_panel",1275,212,540,688)
        ui:text("environment_heading",1295,220,495,34,mod:localize("ui_067"),26)
        ui:button("conditions_shortcut",1295,608,510,52,mod:localize("ui_068")..selected_count..mod:localize("ui_069"),function() go(view,2) end)
        ui:button("spawn_shortcut",1295,674,510,52,mod:localize("ui_070"),function() go(view,director and director.build_dashboard and 4 or 3) end)
        ui:text("configuration_help",1295,750,495,100,mod:localize("ui_071"),21,"muted")
    elseif view._hcm_page==2 then conditions(view,settings,ui)
    elseif view._hcm_page==3 then CoarseEditor(view,ui)
    elseif view._hcm_page==diy_page then DIYManager.build(ui,view,mod,mod.diy_library,DIYSchema,Details)
    else director.build_dashboard(view,ui) end
    if view._hcm_page~=1 then ui:text("saved_status",110,976,1600,30,mod:localize("ui_072"),18,"muted") end
    local choice=view._hcm_choice and ui.choices[view._hcm_choice]
    if choice then
        local a=choice.anchor; local row=44; local capacity=8; local visible_count=math.min(capacity,#choice.options)
        local height=visible_count*row+8+(#choice.options>capacity and 32 or 0)
        local upwards=a.y+a.h+height+6>964
        local top=upwards and a.y-height-6 or a.y+a.h+6
        ui.popup={key=a.key,x=a.x,y=top,w=a.w,h=height,upwards=upwards}
        for _,item in ipairs(ui.items) do item.blocked=item~=a end
        a.overlay=true; a.expanded=true; a.upwards=upwards
        a.action=function() Paging.close_choice(view) end
        ui:add("choice_panel",a.x,top,a.w,height,"",{fill=true,panel=true,overlay=true})
        local first=#ui.items+1
        local offset=ui:window("choice_list_"..a.key,#choice.options,capacity,1,a.x+4,top+4+visible_count*row,a.w-8)
        for i=1,visible_count do
            local option=choice.options[offset+i]
            local item=ui:checkbox("choice_"..a.key.."_"..tostring(option[1]),a.x+4,top+4+(i-1)*row,a.w-8,row,
                option[2],function() choice.choose(option[1]); view._hcm_choice=nil end,choice.value==option[1])
            item.overlay=true; item.font=20; item.scroll="choice_list_"..a.key
        end
        for i=first,#ui.items do ui.items[i].overlay=true end
    else view._hcm_choice=nil end
    Numeric.build(view,ui)
    assert(#ui.items<=Paging.control_count,"Dashboard control budget exceeded")
    return ui
end
Paging.refresh=function(view,settings)
    Help.hide(view)
    local ui=Paging.build(view,settings)
    ui.help_targets={};ui.hover_targets={};ui.widgets_by_key={}
    view._hcm_ui=ui
    local main=view._hcm_page==1
    for name,widget in pairs(view._widgets_by_name) do
        if not name:find("^hcm_") and name~="background" and name~="title_text" and name~="offline_tip_text" then visible(widget,main) end
    end
    for _,id in ipairs({"havoc_theme_circumstance_label","normal_tip_text","havoc_conditions_summary","havoc_add_circumstance_label","havoc_remove_circumstance_label"}) do visible(view._widgets_by_name[id],false) end
    for id,widget in pairs(view._dropdown_widgets) do visible(widget,main and id~="havoc_theme_circumstance" and id~="havoc_add_circumstance" and id~="havoc_remove_circumstance") end
    visible(view._havoc_difficulty_slider_widget,main); visible(view._havoc_difficulty_badge_widget,main)
    if view._modifier_grid then view._modifier_grid:set_visibility(main) end
    for i=1,Paging.control_count do
        local widget=view._widgets_by_name["hcm_control_"..i]
        local item=ui.items[i]
        visible(widget,item~=nil and not item.slider)
        if item then
            ui.widgets_by_key[item.key]=widget
            local id="hcm_control_"..i
            view:_set_scenegraph_position(id,item.x,item.y,item.overlay and 45 or item.panel and 1.5 or 15); view:_set_scenegraph_size(id,item.w,item.h)
            local c,s=widget.content,widget.style
            c.size={item.w,item.h}; c.text=item.text; c.fill=item.fill; c.panel=item.panel; c.selected=item.selected; c.actionable=item.action~=nil or item.on_hover~=nil
            c.choice=item.choice; c.checkbox=item.checkbox; c.numeric=item.number~=nil
            c.hotspot.on_hover_sound=UISoundEvents.default_mouse_hover
            c.hotspot.on_pressed_sound=UISoundEvents.default_click
            c.hotspot.disabled=item.blocked or not (item.action or item.on_hover or item.hint or item.scroll or item.tooltip)
            c.hotspot.pressed_callback=function() Numeric.activate(view,item) end
            c.hotspot.double_click_callback=c.hotspot.pressed_callback
            c.hotspot.hcm_hold_callback=function(hotspot,dt) Numeric.hold(view,item,hotspot,dt) end
            s.hotspot.size={item.w,item.h}; s.background.size={item.w,item.h}; s.accent.size={3,item.h}
            s.edge.size={item.w,1}; s.edge.offset={0,item.h-1,1}
            s.highlight.size={item.w,item.h}; s.frame.size={item.w,item.h}
            s.check.size={32,item.h}
            s.choice_arrow.offset={item.w-30,(item.h-18)/2,3}
            s.choice_arrow.angle=item.expanded and (item.upwards and math.pi/2 or -math.pi/2) or math.pi/2
            local padding=item.checkbox and 42 or item.center and 2 or 12
            s.text.size={math.max(1,item.w-padding-(item.text_right_padding or item.choice and 40 or item.center and 2 or 12)),item.h}; s.text.offset={padding,0,2}; s.text.font_size=item.font or 22
            s.text.text_horizontal_alignment=item.center and "center" or "left"
            s.text.text_vertical_alignment=item.vertical_alignment or "center"
            s.text.text_color=clone(item.danger and colors.danger or colors[item.color] or item.selected and colors.gold or colors.text)
            if item.key=="help" then ui.help_widget=widget end
            if item.tooltip then ui.help_targets[#ui.help_targets+1]={item=item,hotspot=c.hotspot} end
            if item.on_hover or item.hint or item.scroll then ui.hover_targets[#ui.hover_targets+1]={item=item,hotspot=c.hotspot} end
        end
    end
    local w=view._widgets_by_name
    visible(w.hcm_popup_blocker,ui.popup~=nil)
    Numeric.refresh(view,visible)
    Slider.refresh(view,ui,visible)
    w.hcm_popup_blocker.content.hotspot.pressed_callback=function()
        if view._hcm_number then Numeric.commit(view) else Paging.close_choice(view) end
    end
    w.hcm_previous.content.hotspot.disabled=ui.popup~=nil or view._hcm_page==1
    w.hcm_next.content.hotspot.disabled=ui.popup~=nil or view._hcm_page==ui.page_count
end
Paging.close_choice=function(view)
    if not view._hcm_choice then return false end
    view._hcm_choice=nil; view._hcm_refresh=true
    return true
end
Paging.update=function(view,input_service)
    Paging.fit(view)
    Numeric.update(view,input_service)
    Slider.update(view,input_service)
    Help.update(view)
    local ui=view._hcm_ui
    if not ui then return end
    local scroll=input_service:get("scroll_axis"); local amount=scroll and scroll[2] or 0; local hint
    if amount~=0 and Help.scroll(view,amount>0 and -1 or 1) then amount=0 end
    for _,target in ipairs(ui.hover_targets) do
        local item,hotspot=target.item,target.hotspot
        if hotspot.is_hover and not hotspot.disabled then
            if item.on_hover then item.on_hover() end
            if item.hint then hint=item.hint end
            if amount~=0 and item.scroll and ui.scrolls[item.scroll] then ui.scrolls[item.scroll](amount>0 and -1 or 1); amount=0 end
        end
    end
    if ui.help_widget and (not ui.help_initialized or ui.last_hint~=hint) then
        ui.help_initialized=true; ui.last_hint=hint
        ui.help_widget.content.text=hint and short_hint(hint) or ui.default_hint or mod:localize("ui_051")
    end
end
Paging.enter=function(view,settings)
    Paging.fit(view)
    local w=view._widgets_by_name
    w.hcm_previous.content.hotspot.pressed_callback=function() go(view,math.max(1,view._hcm_page-1)) end
    w.hcm_next.content.hotspot.pressed_callback=function() go(view,math.min(view._hcm_ui.page_count,view._hcm_page+1)) end
    local director=get_mod("HavocEnemyDirector")
    if director and director._open_settings_requested then director._open_settings_requested=nil; view._hcm_page=4 end
    Paging.refresh(view,settings)
end
mod._condition_paging_cache = { language = language, module = Paging }
return Paging
