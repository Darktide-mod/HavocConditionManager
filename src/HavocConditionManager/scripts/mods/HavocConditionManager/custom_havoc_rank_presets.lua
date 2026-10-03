-- Optional HED adapters live in HCM. External files and native protocols stay unchanged.
return function(api,mod,base)
    local R=api.rules
    local mode_key="hcm_custom_havoc_modes_v1"
    local bindings,installation={}
    local function clone(value) return type(value)=="table" and R.copy(value) or value end
    local function packed(...) return {n=select("#",...),...} end
    local function active_preset()
        local rank=api.get()
        if not rank or rank<=40 then return end
        return assert(R.preset(rank,function(key) return base:get(key) end),"Invalid selected custom Havoc preset")
    end
    local function save_keys(target,keys)
        local rows={}
        for _,key in ipairs(keys) do rows[#rows+1]={target=target,key=key,value=clone(target:get(key))} end
        return rows
    end
    local function state(director,view)
        local ui={}
        if view then
            for _,key in ipairs({"_current","_current_havoc_difficulty","_current_modifier","_modifier_customizable","_hed_path","_hed_item","_hed_rule_target","_hcm_offsets","_hcm_refresh"}) do ui[#ui+1]={key=key,value=clone(view[key])} end
        end
        return {
            view=view,ui=ui,
            director=save_keys(director,{"studio_coarse_v1","studio_context_hcm","studio_context_hed","studio_seed_hcm","studio_seed_hed","studio_mission_hcm","studio_mission_hed","studio_mode_v1","native_director_v3"}),
            config=director.get_saved_config and clone(director.get_saved_config()),
            base=save_keys(mod,{"native_configuration_v3","diy_seed_v1","diy_options_v1",R.storage_key,mode_key}),
            solo=save_keys(base,{"havoc_mission","havoc_difficulty","hcm_condition_selection_v3","havoc_theme_circumstance","havoc_difficulty_circumstance"}),
            selection=R.selection_state(function(key) return base:get(key) end),
            diy_options=mod.diy_library and clone(mod.diy_library.options),
        }
    end
    local function restore(director,previous)
        -- Restore cached config/options through their owners as well as saved keys.
        -- Attempt every restoration, then expose a rollback failure if any occurred.
        local problems={}
        local function attempt(fn,...)
            local ok,why=pcall(fn,...)
            if not ok then problems[#problems+1]=tostring(why) end
        end
        local function rows(saved)
            for _,entry in ipairs(saved) do attempt(entry.target.set,entry.target,entry.key,entry.value) end
        end
        api.native_writes(function()
            rows(previous.director);rows(previous.base)
            if previous.config and director.save_config then
                attempt(function() local ok,why=director.save_config(previous.config);assert(ok,why) end)
            end
            if previous.diy_options and mod.diy_library then
                attempt(function() local ok,why=mod.diy_library.set_options(previous.diy_options);assert(ok,why) end)
            end
            rows(previous.solo)
            for _,entry in ipairs(previous.selection) do attempt(base.set,base,entry.key,entry.value) end
            -- Owner setters normalize storage. Preserve the pre-transaction raw values.
            rows(previous.director);rows(previous.base)
        end)
        if mod.template_runtime then attempt(mod.template_runtime.reset) end
        if director.finish_director then attempt(director.finish_director) end
        if director.studio_dirty then attempt(director.studio_dirty) end
        if previous.view then
            local view=previous.view
            for _,entry in ipairs(previous.ui) do view[entry.key]=entry.value end
            if view._setup_havoc_badge then attempt(view._setup_havoc_badge,view) end
            if view._modifier_grid and view._update_modifiers_lock then attempt(view._update_modifiers_lock,view) end
        end
        assert(#problems==0,"Custom Havoc rollback failed: "..table.concat(problems,"; "))
    end
    local function transaction(director,view,fn,...)
        local before=state(director,view)
        local result=packed(pcall(fn,...))
        if not result[1] or not result[2] then
            local restored,why=pcall(restore,director,before)
            if not restored then error(tostring(result[2]).."; "..tostring(why),0) end
            if not result[1] then error(result[2],0) end
        end
        return unpack(result,2,result.n)
    end
    local function apply_owned(owned)
        if owned then
            assert(api.set(owned.requested_rank))
            for name,level in pairs(owned.modifiers) do base:set("havoc_modifier_"..name,level) end
            base:set("havoc_modifiers_customizable",owned.customizable)
        else mod:set(R.storage_key,nil) end
    end
    local function refresh(view)
        if not view then return end
        view._current_havoc_difficulty=api.get() or 16
        if view._setup_havoc_badge then view:_setup_havoc_badge() end
        if view._current_modifier then
            for name in pairs(view._current_modifier) do view._current_modifier[name]=base:get("havoc_modifier_"..name) or 0 end
        end
        view._modifier_customizable=base:get("havoc_modifiers_customizable")==true
        if view._modifier_grid and view._update_modifiers_lock then view:_update_modifiers_lock() end
        view._hcm_refresh=true
    end
    local function wrap(target,key,make)
        if type(target[key])~="function" then return end
        local original=target[key];local adapted=make(original);local token=installation
        local function wrapper(...)
            if not token.active or not mod:is_enabled() or get_mod("HavocEnemyDirector")~=token.director or token.director.presets~=token.presets or token.presets.codec~=token.codec then return original(...) end
            return adapted(...)
        end
        bindings[#bindings+1]={target=target,key=key,original=original,wrapper=wrapper}
        target[key]=wrapper
    end
    function api.uninstall_presets()
        if installation then installation.active=false end
        for i=#bindings,1,-1 do local b=bindings[i];if b.target[b.key]==b.wrapper then b.target[b.key]=b.original end end
        bindings={};installation=nil
        if mod._custom_havoc_preset_bridge and mod._custom_havoc_preset_bridge.api==api then mod._custom_havoc_preset_bridge=nil end
    end
    function api.install_presets()
        if not mod:is_enabled() then api.uninstall_presets();return false end
        local director=get_mod("HavocEnemyDirector")
        local presets=director and director.presets
        if not presets or not presets.codec or type(presets.codec.validate)~="function" then api.uninstall_presets();return false end
        local previous=mod._custom_havoc_preset_bridge
        if previous and previous.api==api and previous.director==director and previous.presets==presets and previous.codec==presets.codec then
            local owned=true
            for _,binding in ipairs(bindings) do if binding.target[binding.key]~=binding.wrapper then owned=false;break end end
            if owned then return true end
        end
        if previous then previous.api.uninstall_presets() end
        api.uninstall_presets()
        installation={active=true,director=director,presets=presets,codec=presets.codec}
        mod._custom_havoc_preset_bridge={api=api,director=director,presets=presets,codec=presets.codec}
        wrap(presets.codec,"validate",function(original) return function(doc,...)
            if type(doc)~="table" or getmetatable(doc)~=nil or doc.hcm_custom_havoc_v1==nil then return original(doc,...) end
            local owned=R.validate_preset(doc.hcm_custom_havoc_v1)
            if not owned then return nil,"custom_havoc_rank_invalid" end
            local stripped={};for key,value in pairs(doc) do if key~="hcm_custom_havoc_v1" then stripped[key]=value end end
            local checked,why=original(stripped,...)
            if not checked then return nil,why end
            local mission=checked.config and checked.config.studio and checked.config.studio.mission
            if mission and mission.rank~=owned.native_rank then return nil,"custom_havoc_rank_invalid" end
            checked.hcm_custom_havoc_v1=owned
            return checked,why
        end end)
        local function own_document(doc)
            local owned=active_preset()
            if not owned then return doc end
            doc=R.copy(doc)
            local mission=doc.config and doc.config.studio and doc.config.studio.mission
            if mission then mission.rank=owned.native_rank end
            doc.hcm_custom_havoc_v1=owned
            return presets.codec.validate(doc)
        end
        wrap(presets,"capture",function(original) return function(...)
            local doc,why=original(...)
            if doc then return own_document(doc) end
            return doc,why
        end end)
        wrap(presets,"apply",function(original) return function(doc,view,...)
            if not director:is_enabled() or director.studio_busy and director.studio_busy() then return original(doc,view,...) end
            local checked,why=presets.codec.validate(doc)
            if not checked then return nil,why end
            return transaction(director,view,function(...)
                local applied,err=original(checked,view,...)
                if not applied then return applied,err end
                apply_owned(checked.hcm_custom_havoc_v1);refresh(view)
                if director.studio_dirty then director.studio_dirty() end
                return applied,err
            end,...)
        end end)
        wrap(director,"studio_capture_context",function(original) return function(...)
            local snapshot,why=original(...)
            if snapshot and snapshot.document then
                local doc,err=own_document(snapshot.document)
                if not doc then return nil,err end
                snapshot.document=doc
            end
            return snapshot,why
        end end)
        wrap(director,"studio_refresh_view",function(original) return function(view,...)
            original(view,...);refresh(view)
        end end)
        wrap(director,"set_studio_mode",function(original) return function(mode,...)
            local current=director.studio_mode and director.studio_mode()
            if current==mode or mode~="hcm" and mode~="hed" or director.studio_busy and director.studio_busy() then return original(mode,...) end
            local modes=R.validate_modes(mod:get(mode_key))
            if not modes then return nil,"custom_havoc_modes_invalid" end
            local leaving=active_preset()
            return transaction(director,nil,function(...)
                local changed,why=api.native_writes(original,mode,...)
                if not changed then return changed,why end
                if current=="hcm" or current=="hed" then modes[current]=leaving end
                local target=modes[mode]
                if target and base:get("havoc_difficulty")~=target.native_rank then target=nil end
                apply_owned(target);mod:set(mode_key,modes)
                if director.studio_dirty then director.studio_dirty() end
                return changed,why
            end,...)
        end end)
        return true
    end
end
