-- Native managers keep ownership of scheduling, spawning and cleanup.
local mod=get_mod("HavocConditionManager")
local E=mod.template_runtime
mod:io_dofile("HavocConditionManager/scripts/mods/HavocConditionManager/spawn_queue_capacity")
mod:io_dofile("HavocConditionManager/scripts/mods/HavocConditionManager/spawn_smoothing")
mod:io_dofile("HavocConditionManager/scripts/mods/HavocConditionManager/spawn_placement")
mod:io_dofile("HavocConditionManager/scripts/mods/HavocConditionManager/spawn_flow")
mod:io_dofile("HavocConditionManager/scripts/mods/HavocConditionManager/event_spawn_tracking")
mod:io_dofile("HavocConditionManager/scripts/mods/HavocConditionManager/patrol_spawning")
mod:io_dofile("HavocConditionManager/scripts/mods/HavocConditionManager/encounter_locations")
mod:io_dofile("HavocConditionManager/scripts/mods/HavocConditionManager/buff_warning_summary")
mod:io_dofile("HavocConditionManager/scripts/mods/HavocConditionManager/spawn_tracking")
mod:io_dofile("HavocConditionManager/scripts/mods/HavocConditionManager/retirement_effects")
mod:io_dofile("HavocConditionManager/scripts/mods/HavocConditionManager/straggler_recycling")
local Pacing=require("scripts/managers/pacing/pacing_manager")
local Roamer=require("scripts/managers/pacing/roamer_pacing/roamer_pacing")
local Horde=require("scripts/managers/pacing/horde_pacing/horde_pacing")
local Special=require("scripts/managers/pacing/specials_pacing/specials_pacing")
local Monster=require("scripts/managers/pacing/monster_pacing/monster_pacing")
local Auto=require("scripts/managers/pacing/auto_event/auto_event")
local Mutator=require("scripts/managers/mutator/mutators/mutator_base")
local Terror=require("scripts/managers/terror_event/terror_event_manager")
local Nodes=require("scripts/managers/terror_event/terror_event_nodes")
local Dice=require("scripts/utilities/loaded_dice")
local function active() return mod.has_local_gameplay_authority() end
-- The shared placement search borrows this manager's traversal rules. Release
-- it before the native destructor releases those rules, even on direct teardown.
mod:hook(Roamer,"destroy",function(fn,self,...)
    mod.spawn_placement.finish()
    return fn(self,...)
end)
mod.reset_native_spawn_scaling=function()
    mod.finish_native_warning_summary()
    mod.finish_spawn_tracking()
    mod.finish_straggler_recycling()
    mod.finish_spawn_flow()
    local pacing=Managers.state.pacing
    if pacing and pacing._monster_pacing then mod.finish_encounter_reserve(pacing._monster_pacing) end
    mod.spawn_placement.finish()
    E.reset()
end
mod:hook_safe(Pacing,"init",function(self)
    if active() then
        self._template=E.prepare(self._template,"pacing")
        self._heat_pacing._template=self._template
        mod.start_spawn_tracking()
    end
end)
mod:hook(Roamer,"init",function(fn,self,nav,template,seed,factions)
    if active() then template=E.prepare(template,"roamers"); seed=E.config().fine.seed or seed end
    return fn(self,nav,template,seed,factions)
end)
-- This method returns boxed positions/rotations only. Large maps can otherwise
-- retain every temporary vector from every candidate location until frame end.
mod:hook(Roamer,"_create_sub_zone_location",function(fn,self,spawn_position,density,group)
    if not active() or not E.config().changed or not Script.temp_byte_count or not Script.set_temp_byte_count then
        return fn(self,spawn_position,density,group)
    end
    local marker=Script.temp_byte_count()
    local location,count=fn(self,spawn_position,density,group)
    Script.set_temp_byte_count(marker)
    return location,count
end)
-- A temporary pacing refusal must not erase an unspawned map encounter.
-- The native updater otherwise sends these records to dead-unit cleanup.
mod:hook(Roamer,"update",function(fn,self,...)
    if active() and E.config().changed then
        local allowed=Managers.state.pacing:spawn_type_enabled("roamers")
        self._hcm_defer_unspawned_roamers=not allowed
    end
    local result=fn(self,...)
    self._hcm_defer_unspawned_roamers=nil
    return result
end)
mod:hook(Roamer,"_deactivate_roamer",function(fn,self,roamer)
    -- Retirement unregisters immediately; engine deletion can finish later.
    -- Keep a passive record consumed until native dead-record cleanup runs.
    if roamer._hcm_retired and HEALTH_ALIVE[roamer.spawned_unit] then return false end
    if self._hcm_defer_unspawned_roamers and not roamer.active and not roamer.spawned_unit then
        -- Consume one native update slot and advance, without deleting the plan.
        -- Otherwise a refused update scans every pending record each frame.
        self._roamer_update_index=self._roamer_update_index%self._num_roamers+1
        return true
    end
    return fn(self,roamer)
end)
-- Cloned packs need their own dice and names; native init indexes global packs.
mod:hook(Roamer,"_generate_roamers",function(fn,self,zones,roamers)
    if active() and E.config().changed then
        self._hcm_pack_cache=self._hcm_pack_cache or setmetatable({},{__mode="k"})
        self._hcm_pack_count=self._hcm_pack_count or 0
        for _,zone in ipairs(zones) do
            local packs=zone.roamer_packs
            if packs then
                local cached=self._hcm_pack_cache[packs]
                if not cached then
                    local probabilities={}; local total=0
                    for i,pack in ipairs(packs) do probabilities[i]=pack.weight; total=total+pack.weight end
                    if total>0 then
                        local prob,alias=Dice.create(probabilities,false)
                        self._hcm_pack_count=self._hcm_pack_count+1
                        cached={}; for k,v in pairs(packs) do cached[k]=v end
                        cached.name="hcm_instance_pack_"..self._hcm_pack_count
                        self._roamer_pack_probabilities[cached.name]={prob=prob,alias=alias}
                        self._hcm_pack_cache[packs]=cached
                    end
                end
                if cached then zone.roamer_packs=cached end
            end
        end
    end
    return fn(self,zones,roamers)
end)
for _,class in ipairs({Horde,Monster}) do
    local family=class==Horde and "hordes" or "monsters"
    mod:hook(class,"on_gameplay_post_init",function(fn,self,level,template) return fn(self,level,E.prepare(template,family)) end)
end
mod:hook(Pacing,"get_horde_pacing_override_tempate",function(fn,self) return E.prepare(fn(self),"hordes") end)
mod:hook(Special,"on_spawn_points_generated",function(fn,self,template) return fn(self,E.prepare(template,"specials")) end)
mod:hook(Special,"_setup",function(fn,self,template,first) return fn(self,E.prepare(template,"specials"),first) end)
local strike_timing
mod:hook(Special,"_check_and_activate_coordinated_strike",function(fn,self,template,slot)
    local frequency=active() and E.config().coarse.special_frequency or 1
    if frequency==1 then return fn(self,template,slot) end
    local previous=strike_timing
    strike_timing={owner=self,frequency=frequency}
    local ok,result=pcall(fn,self,template,slot)
    strike_timing=previous
    if not ok then error(result,0) end
    return result
end)
mod:hook(Special,"_setup_specials_slot",function(fn,self,slots,slot,template,modifier,breed,timer,...)
    if strike_timing and strike_timing.owner==self and timer~=nil then
        -- Native coordinated attacks add a fixed 3–6 interval to each slot.
        -- Keep the already-scaled first warning, and scale the following gaps.
        strike_timing.first=strike_timing.first or timer
        timer=strike_timing.first+(timer-strike_timing.first)/strike_timing.frequency
    end
    return fn(self,slots,slot,template,modifier,breed,timer,...)
end)
mod:hook(Special,"set_monster_spawn_config",function(fn,self,config) return fn(self,E.prepare(config,"mutators")) end)
mod:hook(Horde,"add_trickle_horde",function(fn,self,template) return fn(self,E.prepare(template,"hordes")) end)
mod:hook(Mutator,"init",function(fn,self,is_server,delegate,template,nav,world,seed)
    if is_server then template=E.prepare(template,"mutators") end
    return fn(self,is_server,delegate,template,nav,world,seed)
end)
mod:hook_safe(Auto,"init",function(self)
    if active() then self._template=E.prepare(self._template,"events"); self._original_template=self._template end
end)
for _,method in ipairs({"swap_auto_event_template","restore_auto_event_template"}) do
    mod:hook_safe(Auto,method,function(self) self._template=E.prepare(self._template,"events") end)
end
mod:hook(Terror,"_load_mission_event_templates",function(fn,self,mission)
    local events,random=fn(self,mission)
    if active() and self._is_server then
        for name,template in pairs(events) do events[name]=E.prepare(template,"mission_events") end
    end
    return events,random
end)
for _,method in ipairs({"get_terror_event_point_modifier","get_max_points_modifer"}) do
    mod:hook(Terror,method,function(fn,self)
        local value=fn(self)
        if active() then value=value*E.config().coarse.event_budget end
        return value
    end)
end
mod:hook(Pacing,"update",function(fn,self,dt,t,...)
    E.clear_context()
    local result=fn(self,dt,t,...)
    mod.update_native_warning_summary(t)
    mod.update_straggler_recycling(self,t)
    return result
end)
local source_members={roamers={"_roamer_pacing","_roamer_template"},hordes={"_horde_pacing","_template"},
    trickle_hordes={"_horde_pacing","_template"},specials={"_specials_pacing","_template"},monsters={"_monster_pacing","_template"}}
local function expanded_capacity_allowed(self,source,capacity)
    -- The native 145 check returns before checking challenge, pauses and heat.
    -- Replace only that threshold; all later refusals must still be evaluated.
    if capacity<=145 or Managers.state.minion_spawn:total_allocated_num_enemies()>capacity then
        return false,"Hard_allocated_limit_reached"
    end
    local threshold=self._challenge_rating_thresholds[source]
    if threshold and threshold<self._total_challenge_rating then return false,"disabled_by_challenge_rating" end
    if self._paused_spawn_types[source] then return false,"paused" end
    if not self._allowed_spawn_types or not self._allowed_spawn_types[source] and not self._heat_pacing:active() then return false,"not_allowed" end
    if self._heat_pacing:active() and not self._heat_pacing:current_stage_settings().allowed_spawn_types[source] then
        return false,"disabled_by_heat_stage"
    end
    return true
end
for _,method in ipairs({"spawn_type_enabled","spawn_type_allowed"}) do
    mod:hook(Pacing,method,function(fn,self,source)
        local allowed,reason=fn(self,source)
        if allowed and active() and mod.diy_api and mod.diy_api.paused(source) then return false,"HCM_DIY_pause" end
        if method=="spawn_type_enabled" and (allowed or reason=="Hard_allocated_limit_reached") and active() then
            local factor=E.config().coarse.combat_tolerance
            if factor~=1 then
                local capacity=math.floor(145*factor+0.5)
                if allowed then
                    if Managers.state.minion_spawn:total_allocated_num_enemies()>capacity then allowed,reason=false,"Hard_allocated_limit_reached" end
                else
                    allowed,reason=expanded_capacity_allowed(self,source,capacity)
                end
            end
        end
        local member=source_members[source]; local manager=member and self[member[1]]
        if allowed and active() and manager and not E.allowed(manager[member[2]],self._target_side_id) then return false,"HCM_condition" end
        return allowed,reason
    end)
end
mod:hook(Special,"_spawn_special",function(fn,self,slot,side,target)
    if active() and not E.allowed(self._template,target) then return false end
    return fn(self,slot,side,target)
end)
mod:hook(Auto,"update",function(fn,self,dt,t)
    if active() and E.has_gate(self._template) and not E.allowed(self._template,self._target_side_id) then
        for _,data in pairs(self._active_events) do
            if not data.primary_wave_event_sent then
                data.wave_cooldown=math.max(data.wave_cooldown,t+dt)
                if not data.pre_stinger_played then data.pre_stinger_delay=math.max(data.pre_stinger_delay,t+dt) end
            end
        end
    end
    return fn(self,dt,t)
end)
mod:hook(Nodes.spawn_by_points,"update",function(fn,node,scratchpad,t,dt)
    if active() and not scratchpad.started_spawn and not E.node_allowed(node) then return false end
    return mod.run_event_spawn_node(fn,node,scratchpad,t,dt)
end)
local Havoc=require("scripts/managers/mutator/mutators/mutator_modify_havoc")
mod:hook_safe(Havoc,"init",function(self)
    if not active() or not self._is_server then return end
    local data=self._template and self._template.init_modify_horde
    local manager=Managers.state.game_mode
    local mode=manager and manager:game_mode()
    local havoc=mode and mode:extension("havoc")
    if data and havoc then havoc:init_horde_buff(data) end
end)
