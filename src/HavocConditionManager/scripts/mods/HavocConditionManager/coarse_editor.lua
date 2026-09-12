local mod=get_mod("HavocConditionManager")
local S=mod.template_schema
local Profile=mod:io_dofile("HavocConditionManager/scripts/mods/HavocConditionManager/intensity_profile")
local Randomization=mod:io_dofile("HavocConditionManager/scripts/mods/HavocConditionManager/randomization_ui")
return function(view,ui)
    if view._hcm_random_settings then return Randomization(view,ui) end
    local lang=mod:localize("native_language")
    local function text(d) return S.text(d,lang) end
    local groups={{"map","Map population","地图布置"},{"hordes","Horde encounters","尸潮遭遇"},{"trickle","Trickle waves","小股敌潮"},
        {"specials","Specialists","特感调度"},{"encounters","Monsters & events","怪物与事件"},{"pacing","Combat pacing","战斗节奏"}}
    local cfg=S.coarse_config(mod:get("native_configuration_v3"))
    view._hcm_coarse_group=view._hcm_coarse_group or "map"
    local function row(key,x,y,label_width,track_width,d,value,description,mixed)
        local label=ui:text(key.."_label",x,y-5,label_width,56,text(d),20)
        label.tooltip=description; label.tooltip_title=text(d)
        local spec={label=text(d),value=value,min=d.min,max=d.max,step=d.step,mixed=mixed,set=d.set,always_apply=mixed,integer=d.integer,format=d.format}
        local slider=ui:add(key.."_slider",x+label_width+15,y,track_width,46,"",{slider=spec})
        slider.value_key=key.."_value"
        ui:number(key.."_value",x+label_width+track_width+35,y,140,46,mixed and mod:localize("native_mixed") or d.format and d.format(value) or string.format("%.4g×",value),spec,22)
    end
    local strength=Profile.match(cfg)
    local mixed=strength==nil
    local global={en="Overall intensity",cn="整体强度",min=Profile.min,max=Profile.max,step=Profile.step,integer=true,
        format=function(value) return mod:localize("native_intensity_value",value) end,
        set=function(value) local next_cfg=Profile.values(value); if next_cfg then mod:set("native_configuration_v3",next_cfg) end end}
    ui:panel("native_global_panel",180,224,1560,170)
    row("native_global",200,236,290,1015,global,strength or 1,mod:localize("native_global_help"),mixed)
    ui:text("native_intro",200,288,1520,28,mod:localize("native_coarse_intro"),18,"muted")
    ui:text("native_profile_summary",200,334,1520,42,mod:localize("native_profile_summary",cfg.patrols,cfg.monster_encounters,cfg.special_slots,cfg.special_frequency),21)
    ui:button("native_advanced_toggle",180,410,1158,48,mod:localize(view._hcm_coarse_advanced and "native_advanced_close" or "native_advanced_open"),
        function() view._hcm_coarse_advanced=not view._hcm_coarse_advanced end,view._hcm_coarse_advanced)
    ui:button("hcm_seed_settings",1354,410,386,48,mod:localize("diy_seed_settings"),function()view._hcm_random_settings=true end)
    if not view._hcm_coarse_advanced then
        return
    end
    ui:panel("native_groups",180,478,260,417)
    for i,group in ipairs(groups) do
        ui:button("native_group_"..group[1],190,490+(i-1)*60,240,48,text({en=group[2],cn=group[3]}),
            function() view._hcm_coarse_group=group[1] end,view._hcm_coarse_group==group[1])
    end
    local n=0
    for _,d in ipairs(S.coarse) do if d.group==view._hcm_coarse_group then
        local y=490+n*82; n=n+1
        local definition={en=d.en,cn=d.cn,min=d.min,max=d.max,step=d.step,set=function(value)
            local current=S.coarse_config(mod:get("native_configuration_v3")); current[d.id]=S.normalize(value,d); mod:set("native_configuration_v3",current)
        end}
        ui:panel("native_row_"..d.id,465,y-8,1275,64)
        row("native_"..d.id,480,y,270,760,definition,cfg[d.id],S.text(d,lang,true))
    end end
end
