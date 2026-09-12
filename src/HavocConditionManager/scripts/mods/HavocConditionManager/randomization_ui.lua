local mod=get_mod("HavocConditionManager")
local Seed=mod:io_dofile("HavocConditionManager/scripts/mods/HavocConditionManager/diy/diy_seed")
return function(view,ui)
    local settings=mod.diy_seed_settings or Seed.new(mod)
    local config=settings.get()
    local function loc(key,...)return mod:localize("diy_"..key,...)end
    ui:button("hcm_seed_back",180,224,260,50,loc("seed_back"),function()view._hcm_random_settings=nil end)
    ui:text("hcm_seed_heading",466,226,1274,52,loc("seed_settings"),28,"gold")
    ui:panel("hcm_seed_panel",180,302,1560,580)
    ui:checkbox("hcm_seed_enabled",206,326,1508,54,loc("seed_fixed_conditions"),function()
        local next_config=settings.get();next_config.enabled=not next_config.enabled;settings.set(next_config)
    end,config.enabled)
    ui:text("hcm_seed_value_label",206,412,460,58,loc("seed_value"),23)
    ui:number("hcm_seed_value",690,410,1024,56,tostring(config.value),config.enabled and {
        label=loc("seed_value"),value=config.value,min=1,max=Seed.maximum,integer=true,
        set=function(value)local next_config=settings.get();if next_config.enabled then next_config.value=value;settings.set(next_config)end end},25)
    ui:text("hcm_seed_help",206,498,1508,128,loc("seed_conditions_help"),23,"muted")
    ui:text("hcm_seed_scope",206,652,1508,96,loc("seed_other_scopes"),21,"muted")
    ui:text("hcm_seed_next",206,776,1508,78,loc("seed_next_mission"),22,"gold")
end
