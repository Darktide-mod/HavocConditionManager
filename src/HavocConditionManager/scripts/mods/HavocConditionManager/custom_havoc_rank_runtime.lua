local mod=get_mod("HavocConditionManager")
local base=get_mod("SoloPlay")
local R=mod:io_dofile("HavocConditionManager/scripts/mods/HavocConditionManager/custom_havoc_rank")
local api={rules=R}
function api.get()
    local native=base:get("havoc_difficulty")
    local saved=mod:get(R.storage_key)
    local custom=R.validate_record(saved)
    assert(saved==nil or custom,"Invalid saved custom Havoc rank record")
    if native==nil and saved==nil then return end
    assert(R.validate(native) and native<=40,"SoloPlay native Havoc rank must be a finite integer from 1 to 40")
    -- A legacy preset/native SoloPlay edit to a different rank invalidates the
    -- previous custom selection. Same-rank40 preset changes are handled by its adapter.
    if custom and custom.requested_rank>40 and native==custom.native_rank then return custom.requested_rank end
    return native
end
function api.set(rank)
    if not R.validate(rank) then return false end
    base:set("havoc_difficulty",math.min(rank,40))
    mod:set(R.storage_key,rank>40 and R.record(rank) or nil)
    return true
end
function api.validate_launch()
    local native=base:get("havoc_difficulty")
    local saved=mod:get(R.storage_key)
    assert(R.validate(native) and native<=40,"SoloPlay native Havoc rank must be a finite integer from 1 to 40")
    assert(saved==nil or R.validate_record(saved),"Invalid saved custom Havoc rank record")
end
function api.generate(fn,rank,...) return R.generate(fn,rank,...) end
function api.decorate(context)
    local rank=api.get() or 16
    if rank<=40 then return context end
    assert(type(context)=="table" and type(context.havoc_data)=="string","Missing SoloPlay Havoc context")
    local parsed=require("scripts/utilities/havoc").parse_data(context.havoc_data)
    local mission=require("scripts/settings/mission/mission_templates")[parsed.mission]
    assert(mission and mission.game_mode_name~="training_grounds" and mission.game_mode_name~="shooting_range","Custom Havoc ranks41-50 require a supported SoloPlay mission")
    assert(parsed.havoc_rank==40,"Custom Havoc launch requires its separate native rank40 identity")
    local snapshot=R.capture(rank,parsed.modifiers)
    snapshot.native_data=context.havoc_data
    context.hcm_custom_havoc_v1=snapshot
    return context
end
local owner,snapshot,buff_cache,finished_owner
function api.finish()
    finished_owner=owner or (Managers.state and Managers.state.difficulty)
    owner=nil;snapshot=nil;buff_cache=nil
end
function api.start() owner=nil;snapshot=nil;buff_cache=nil;finished_owner=nil end
local function eligible()
    return mod.has_local_gameplay_authority() and base.is_soloplay and base.is_soloplay()
end
function api.session()
    if not eligible() then return end
    local difficulty=Managers.state and Managers.state.difficulty
    if not difficulty or difficulty==finished_owner then return end
    if owner==difficulty then return snapshot end
    owner=difficulty;snapshot=nil;buff_cache={}
    -- MechanismBase retains the original launch context. Adventure transports
    -- only native fields, so custom metadata never enters its RPC contract.
    local mechanism=Managers.mechanism and Managers.mechanism._mechanism
    local context=mechanism and mechanism._context
    local custom=context and context.hcm_custom_havoc_v1
    local parsed=difficulty:get_parsed_havoc_data()
    local data=mechanism and mechanism._mechanism_data
    if not custom or not parsed or parsed.havoc_rank~=40 or not data or data.havoc_data~=custom.native_data then return end
    local record=R.validate_record(custom.record)
    if not record or record.requested_rank<=40 or context.havoc_data~=custom.native_data or not R.same_modifiers(custom.modifiers,parsed.modifiers) then return end
    snapshot=R.copy(custom)
    return snapshot
end
local HavocExtension=require("scripts/managers/game_mode/game_mode_extensions/game_mode_extension_havoc")
local function finish_modifiers(self,selected,...)
    local current=self._is_server and api.session()
    if current and R.same_modifiers(current.modifiers,selected) then R.apply_scalars(current,self._modifiers) end
    return ...
end
mod:hook(HavocExtension,"_initialize_modifiers",function(fn,self,selected,...)
    return finish_modifiers(self,selected,fn(self,selected,...))
end)
local applying_unit
local function packed(...) return {n=select("#",...),...} end
local function native_buff_application(fn,self,unit,...)
    if not self._is_server or not api.session() then return fn(self,...) end
    local previous=applying_unit
    applying_unit=unit
    local result=packed(pcall(fn,self,...))
    applying_unit=previous
    if not result[1] then error(result[2],0) end
    return unpack(result,2,result.n)
end
mod:hook(HavocExtension,"_on_player_unit_spawned",function(fn,self,player,...)
    return native_buff_application(fn,self,player.player_unit,player,...)
end)
mod:hook(HavocExtension,"_on_minion_unit_spawned",function(fn,self,unit,...)
    return native_buff_application(fn,self,unit,unit,...)
end)
mod:hook_require("scripts/extension_systems/buff/buffs/buff",function(Buff)
    mod:hook(Buff,"init",function(fn,self,context,template,...)
        -- Identical native names can also be instantiated by DIY independently.
        local current=applying_unit==context.unit and context.is_server and api.session()
        if current then template=R.prepare_buff(current,template,buff_cache) end
        return fn(self,context,template,...)
    end)
end)
-- Keep raw native rank40 for skin (.5), the exact-rank40 boss gate and all
-- unextended rank consumers. Requested rank is HCM metadata, never a backend rank.
return api
