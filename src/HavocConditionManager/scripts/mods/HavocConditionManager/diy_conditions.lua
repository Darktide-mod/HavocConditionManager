local mod=get_mod("HavocConditionManager")
local path="HavocConditionManager/scripts/mods/HavocConditionManager/diy/"
local function load(name) return mod:io_dofile(path..name) end
local Schema,Codec,Catalog,Engine=load("diy_schema"),load("diy_codec"),load("diy_catalog"),load("diy_engine")
local Library,Files,Game=load("diy_library"),load("diy_files"),load("diy_game")
local Network=load("diy_network")
local PackageLibrary,Packages,Hash,Scripts=load("diy_package_library"),load("diy_packages"),load("diy_sha256"),load("diy_scripts")
local PackageAPI=Packages.new(Schema,Codec,Hash)
local Bundled=load("diy_bundled")
local package_providers={}
local Assets=load("diy_assets")
local assets
local Seed=load("diy_seed")
mod.diy_seed_settings=Seed.new(mod)
local engine,owner,api,elapsed,network,finish
local function busy()
    local manager=Managers.state and Managers.state.game_mode
    local name=manager and manager:game_mode_name()
    return name and name~="hub" and name~="prologue_hub" or false
end
local library=PackageLibrary.new(mod,"conditions",Catalog,Schema,Codec,Files,Library,Packages,Hash,
    {name="HavocConditionManager",busy=busy,bundled=function()
        local sources={{name="HavocConditionManager",builtin=true}}
        local names={};for name in pairs(package_providers)do names[#names+1]=name end;table.sort(names)
        for _,name in ipairs(names)do sources[#sources+1]={name=name} end
        for _,source in ipairs(sources)do
            source.directory="mods/"..source.name.."/diy/packages"
            source.files,source.error=Bundled.read(mod,source.name,Codec,Packages)
        end
        return sources
     end,
     before_reload=function()
        if not busy() then
            if finish then finish()end
            if assets then assets.clear_cache()end
        end
        if api then api.invalidate()end
     end})
mod.diy_library=library
assets=Assets.new(mod,Hash,{error=library.runtime_error})
finish=function()
    if engine then engine.finish() elseif api then api.finish() end
    if assets then assets.close_all("manager_end") end
    engine=nil;owner=nil;elapsed=0
end
local function ensure()
    if not mod.has_local_gameplay_authority() or not busy() then
        if engine then finish() end
        return
    end
    local state=Managers.state or {};local current=state.game_session or state.difficulty
    if not current then return end
    if owner~=current then
        finish();owner=current
        local snap=library.snapshot()
        if snap.options.enabled and #snap.document.entries>0 then
            local pacing=state.pacing
            local mission_seed=pacing and type(pacing.level_seed)=="function" and pacing:level_seed() or pacing and pacing._level_seed
            local seed=mod.diy_seed_settings.resolve(mission_seed)
            engine=Scripts.attach(Engine.new(snap.document,Catalog,api,seed),snap,
                {Schema=Schema,Packages=Packages,PackageAPI=PackageAPI,Engine=Engine,native=api,catalog=Catalog,error=library.runtime_error,assets=assets,authority=function()return mod.has_local_gameplay_authority() and busy() end,
                 log=function(id,message)mod:info("[DIY %s] %s",id,message)end})
            engine.set_global(Engine.choose(snap.document,snap.options,seed))
        end
    end
    return engine
end
network=Network.new(mod,Catalog,{context=Network.context,realms=Network.realms,local_player=Network.local_player,players=Network.players,
    request=function() return {version=1} end,
    accept=function(_,request) return type(request)=="table" and request.version==1,"ready" end,
    snapshot=function(player,accepted)
        local e=ensure();return e and accepted and player.player_unit and e.effects(player.player_unit),e and "ready" or "host_disabled"
    end})
api=Game.new(mod,Catalog,Engine,{name="HavocConditionManager",engine=ensure,authority=mod.has_local_gameplay_authority,
    client_effects=network.effects,
    language=function() return mod:localize("native_language") end,
    context=function()
        local c={}
        if mod.template_runtime then for k,v in pairs(mod.template_runtime.context(1)) do c[k]=v end end
        c.native_condition={}
        local difficulty=Managers.state and Managers.state.difficulty
        local data=difficulty and difficulty.get_parsed_havoc_data and difficulty:get_parsed_havoc_data()
        for _,id in ipairs(data and data.circumstances or {}) do c.native_condition[id]=true end
        local circumstance=Managers.state and Managers.state.circumstance and Managers.state.circumstance._circumstance_name
        if circumstance then c.native_condition[circumstance]=true end
        local hed=get_mod("HavocEnemyDirector")
        if hed and hed.diy_api and hed.diy_api.status then local status=hed.diy_api.status();c.phase=status and status.phase end
        return c
    end})
mod.finish_diy_conditions=function() network.finish();finish() end
mod.update_diy_conditions=function(dt)
    assets.update(dt)
    network.update(dt)
    local current=ensure();if not current then return end
    elapsed=(elapsed or 0)+dt;if elapsed<.1 then return end
    local step=elapsed;elapsed=0;api.update();current.tick(step)
end
mod.diy_on_spawn=function(unit,breed,batch)
    local current=ensure()
    if current then current.dispatch("spawn",unit,{target=unit,spawn_source=batch and batch.source or "native"}) end
end
local Difficulty=require("scripts/managers/difficulty/difficulty_manager")
mod:hook(Difficulty,"get_minion_max_health",function(fn,self,breed_name,...)
    local value=fn(self,breed_name,...)
    local current=ensure();local info=Catalog.breeds[breed_name]
    if current and info then return math.min(1000000,value*current.health_multiplier(info)) end
    return value
end)
mod.diy_api={version=1,minor=2}
-- Companion mods register only their own fixed, declared package directory.
function mod.diy_api.register_package_source(name)
    if type(name)~="string" or not name:match("^[%w_]+$") or name=="HavocConditionManager" or not get_mod(name) then return nil,"diy_package_path" end
    if package_providers[name] then return true end
    package_providers[name]=true
    return library.scan()
end
function mod.diy_api.unregister_package_source(name)
    if not package_providers[name] then return true end
    package_providers[name]=nil
    return library.scan()
end
local function scope_supported(entry)
    return entry and entry.enabled and entry.passive~=nil and not entry.script and not entry.spawn
        and #(entry.rules or {})==0 and entry.targets and entry.targets.kind~="players"
end
function mod.studio_scope_available(id)
    for _,entry in ipairs(library.document.entries) do if entry.id==id then return scope_supported(entry) end end
    return false
end
function mod.diy_api.passive_scope(unit,values)
    local current=ensure();if not current then return nil,"DIY engine inactive" end
    if type(values)~="table" then return nil,"unit scope" end
    local count=0
    for id,value in pairs(values) do
        count=count+1
        if count>64 or type(value)~="boolean" or not scope_supported(current.entry_by_id[id]) then return nil,"unsupported unit effect" end
    end
    current.set_passive_scope(unit,values)
    api.unit_scope_changed(unit)
    return true
end
-- Local views/HUDs may acquire resources on clients without creating an
-- authority engine. Close the scope when the consuming view exits.
function mod.diy_api.open_assets(package_id,active)
    if not Packages.id(package_id) then return nil,"diy_package_missing" end
    local pack=library.snapshot().packages[package_id]
    if not pack then return nil,"diy_package_missing" end
    return assets.open(pack,active)
end
mod.diy_api.assets_available=assets.available
mod.diy_api.asset_status=assets.status
function mod.diy_api.qualify(package_id,entry_id)
    if not Packages.id(package_id) or not Packages.id(entry_id) then return nil end
    local pack=library.packages[package_id]
    return pack and PackageAPI.entry_identity(pack,entry_id) or PackageAPI.identity(package_id,entry_id)
end
function mod.diy_api.active() local current=ensure();return current and current.active_ids() or {} end
function mod.diy_api.emit_signal(name,duration) local current=ensure();return current and current.emit_signal(name,duration) or false end
function mod.diy_api.paused(family)
    local current=ensure();if current and current.paused(family) then return true end
    local mortis=get_mod("MortisBuffManager")
    return mortis and mortis.diy_api and mortis.diy_api.paused(family) or false
end
function mod.diy_api.context(c)
    local current=ensure();c=c or {};c.affix={};c.signal={}
    if current then
        for _,id in ipairs(current.active_ids()) do
            c.affix[id]=true
            local source=current.package_sources and current.package_sources[id]
            if source then c.affix[source.entry_id]=true end -- Legacy external template integrations.
        end
        for name,t in pairs(current.signals) do if t>current.now then c.signal[name]=true end end
    end
    local mortis=get_mod("MortisBuffManager")
    if mortis and mortis.diy_api then mortis.diy_api.context(c) end
    return c
end
function mod.diy_api.status()
    local current=ensure()
    return {version=1,active=current~=nil,network=network.status,seed=current and current.seed,selected=current and current.active_ids() or {},
        queue=current and #current.queue or 0,metrics=current and Schema.copy(current.metrics) or {}}
end
return true
