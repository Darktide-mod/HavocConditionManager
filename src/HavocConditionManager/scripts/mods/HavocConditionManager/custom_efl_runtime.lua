local mod,base=get_mod("HavocConditionManager"),get_mod("SoloPlay")
local R=mod:io_dofile("HavocConditionManager/scripts/mods/HavocConditionManager/custom_efl")
local api={rules=R}
local alive=true
local depth=0
local function packed(...) return {n=select("#",...),...} end
function api.native_writes(fn,...)
    depth=depth+1;local result=packed(pcall(fn,...));depth=depth-1
    if not result[1] then error(result[2],0) end
    return unpack(result,2,result.n)
end
local function dirty()
    local director=get_mod("HavocEnemyDirector")
    if director and director.studio_dirty then director.studio_dirty() end
end
function api.record()
    local saved=mod:get(R.storage_key)
    local clean=R.validate_record(saved)
    assert(saved==nil or clean,"Invalid saved custom EFL record")
    if clean and base:get("havoc_difficulty_circumstance")==R.native_ii then return clean end
end
function api.get()
    local record=api.record()
    return record and R.choices[record.tier] or base:get("havoc_difficulty_circumstance")
end
function api.set(choice)
    local tier=R.tier(choice)
    if not tier and choice~="default" then return false end
    api.native_writes(base.set,base,"havoc_difficulty_circumstance",tier and tier>=2 and R.native_ii or choice)
    mod:set(R.storage_key,tier and R.record(tier) or nil)
    if not tier or tier<3 then api.finish() end
    dirty();return true
end
function api.set_tier(tier) return R.valid_tier(tier) and api.set(R.choices[tier]) or false end
function api.decorate(context)
    local record=api.record()
    if not record then return context end
    assert(type(context)=="table" and type(context.havoc_data)=="string","Missing SoloPlay EFL context")
    local parsed=require("scripts/utilities/havoc").parse_data(context.havoc_data)
    local mission=require("scripts/settings/mission/mission_templates")[parsed.mission]
    assert(mission,"Unknown SoloPlay EFL mission")
    if mission.game_mode_name=="training_grounds" or mission.game_mode_name=="shooting_range" then return context end
    assert(R.native_ii_only(parsed),"Custom EFL launch requires exactly one native II circumstance")
    context.hcm_custom_efl_v1={version=record.version,tier=record.tier,native_id=record.native_id,native_data=context.havoc_data}
    return context
end
local owner,snapshot,finished_owner
local restorations={}
function api.finish()
    for _,restore in ipairs(restorations) do restore() end
    restorations={}
    finished_owner=owner or (Managers.state and Managers.state.difficulty)
    owner=nil;snapshot=nil
    if mod.template_runtime and mod.template_runtime.invalidate then mod.template_runtime.invalidate() end
end
function api.start()
    -- Mutators and pacing initialize before GameplayStateRun. Entering Run
    -- must retain their copies and any explicit retirement for this owner.
    local current=Managers.state and Managers.state.difficulty
    if current and (owner==current or finished_owner==current) then return end
    api.finish();finished_owner=nil
end
function api.session()
    -- A Realms listen host has local gameplay authority but is_soloplay=false.
    if not alive or not mod:is_enabled() or not mod.has_local_gameplay_authority() then return end
    local difficulty=Managers.state and Managers.state.difficulty
    if not difficulty or difficulty==finished_owner then return end
    if owner==difficulty then return snapshot end
    -- Mission transition without a callback still retires old private copies.
    api.finish();finished_owner=nil;owner=difficulty
    local mechanism=Managers.mechanism and Managers.mechanism._mechanism
    local context=mechanism and mechanism._context
    local saved=context and context.hcm_custom_efl_v1
    local data=mechanism and mechanism._mechanism_data
    local parsed=difficulty:get_parsed_havoc_data()
    if type(saved)~="table" or getmetatable(saved) or type(saved.native_data)~="string" or not data or data.havoc_data~=saved.native_data or context.havoc_data~=saved.native_data or not R.native_ii_only(parsed) then return end
    local native=require("scripts/utilities/havoc").parse_data(saved.native_data)
    local mission=require("scripts/settings/mission/mission_templates")[native.mission]
    if not R.native_ii_only(native) or parsed.mission~=native.mission or parsed.havoc_rank~=native.havoc_rank or not mission or mission.game_mode_name=="training_grounds" or mission.game_mode_name=="shooting_range" then return end
    for key in pairs(saved) do if key~="version" and key~="tier" and key~="native_id" and key~="native_data" then return end end
    snapshot=R.validate_record({version=saved.version,tier=saved.tier,native_id=saved.native_id})
    return snapshot
end
function api.prepare(original,prepared,entry)
    local selected=api.session()
    if not selected then return prepared end
    local result,restore=R.prepare(original,prepared,entry,mod.template_registry,selected.tier)
    if restore then restorations[#restorations+1]=restore end
    return result
end
local old=mod._custom_efl_observer
if old then old.active=false end
if old and base.set==old.wrapper then base.set=old.original end
local observer={active=true,original=base.set}
local function after_write(key,...)
    if observer.active and key=="havoc_difficulty_circumstance" and depth==0 then
        if mod:get(R.storage_key)~=nil then mod:set(R.storage_key,nil);dirty() end
        api.finish()
    end
    return ...
end
observer.wrapper=function(self,key,...) return after_write(key,observer.original(self,key,...)) end
base.set=observer.wrapper;mod._custom_efl_observer=observer
function api.unload()
    alive=false;api.finish();observer.active=false
    if base.set==observer.wrapper then base.set=observer.original end
    if mod._custom_efl_observer==observer then mod._custom_efl_observer=nil end
end
return api
