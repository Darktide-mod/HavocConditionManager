-- HCM management only. Gameplay selections live on the main condition page.
local M={}
function M.build(ui,view,mod,library,Schema,D)
    local function loc(key)return mod:localize("diy_"..key)end
    local function change(fn)return function()
        if not mod:is_enabled() then return end
        fn();view._hcm_refresh=true
    end end
    local extract=ui:button("diy_extract_templates",105,219,390,50,D.word("extract",mod),library.extract_templates and change(library.extract_templates))
    extract.tooltip=D.word("extract_help",mod)
    ui:button("diy_scan",511,219,300,50,loc("scan"),change(library.scan))
    ui:button("diy_directory",827,219,300,50,loc("copy_dir"),change(library.copy_directory))
    ui:button("diy_export",1143,219,300,50,loc("export"),change(function()library.export()end))
    ui:button("diy_paste",1459,219,336,50,loc("paste"),change(function()
        local raw=Clipboard and Clipboard.get and Clipboard.get()
        if type(raw)=="string" then library.import_text(raw,"clipboard") else library.last_error="diy_no_clipboard" end
    end))
    ui:text("diy_manage_help",105,282,1690,66,D.word("manage_help",mod),21,"muted")
    local files=library.files
    local selected=library.selected_file or 1
    if view._diy_inspect_file then for i,id in ipairs(files)do if id==view._diy_inspect_file then selected=i;break end end end
    selected=math.max(1,math.min(selected,#files));library.selected_file=selected
    local file=files[selected];view._diy_inspect_file=file
    local function entry_for(id)
        for _,entry in ipairs(library.document.entries)do
            local source=library.entry_sources[entry.id]
            if source and source.package_id==id then return entry end
        end
        local package=library.packages[id]
        return package and package.document.entries[1]
    end
    local shown=file and entry_for(file)
    ui:text("diy_packages_count",105,355,714,40,D.word("manager",mod).."  ·  "..#files,27,"gold")
    ui:button("diy_import",1405,353,390,46,loc(file and library.package_disabled(file) and "package_enable" or "package_disable"),file and change(function()library.toggle_package(file)end))
    local offset=ui:window("diy_packages",#files,8,1,105,403,714)
    for i=1,math.min(8,#files-offset)do
        local id=files[offset+i];local entry=entry_for(id)
        local name=entry and D.name(entry,Schema,mod) or D.clean(id)
        local row=ui:button("diy_package_"..i,105,447+(i-1)*53,714,47,name,change(function()
            library.selected_file=offset+i;view._diy_inspect_file=id;view._diy_detail_page=1
        end),id==file)
        row.center=false;row.scroll="diy_packages";row.text_right_padding=116
        row.tooltip_title=name;row.tooltip=entry and D.describe(entry,library,Schema,mod) or loc("package_missing")
        ui:text("diy_package_state_"..i,703,row.y,110,47,D.word(library.package_disabled(id) and "unloaded" or "loaded",mod),17,"muted")
    end
    if #files==0 then ui:text("diy_empty",105,445,700,185,D.word("empty",mod),22,"muted") end
    ui:panel("diy_detail_panel",851,413,944,457)
    ui:text("diy_detail_title",870,424,900,58,shown and D.name(shown,Schema,mod) or D.word("inspect",mod),28,"gold")
    local text=shown and D.describe(shown,library,Schema,mod) or D.word("empty",mod)
    if file and library.package_disabled(file) then text=text.."\n\n"..loc("package_disabled") end
    local pages=D.pages(text,78,12)
    local page=math.max(1,math.min(view._diy_detail_page or 1,#pages));view._diy_detail_page=page
    local detail=ui:text("diy_detail",870,487,900,316,pages[page],20)
    detail.vertical_alignment="top"
    if #pages>1 then
        ui:button("diy_detail_prev",870,819,180,40,D.word("previous",mod),page>1 and change(function()view._diy_detail_page=page-1 end))
        ui:text("diy_detail_page",1066,819,500,40,D.word("more",mod,page,#pages),18,"muted")
        ui:button("diy_detail_next",1578,819,198,40,D.word("next",mod),page<#pages and change(function()view._diy_detail_page=page+1 end))
    end
    local summary,issue=library.status_message()
    local message=library.last_error or library.last_message
    if message then summary=summary.."\n"..(library.format_message and library.format_message(message) or mod:localize(message))end
    local status=D.pages(D.clean(summary),144,2)
    if view._diy_status_text~=summary then view._diy_status_text=summary;view._diy_status_page=1 end
    local status_page=math.max(1,math.min(view._diy_status_page or 1,#status))
    ui:text("diy_status",105,887,1490,76,status[status_page],19,(issue or library.last_error) and "danger" or "muted")
    if #status>1 then ui:button("diy_status_more",1621,903,174,42,D.word("next",mod),change(function()view._diy_status_page=status_page%#status+1 end))end
end
return M
