-- Enemy gameplay timings use action data rather than the player blue-stimm buff.
-- All changes are routed through the currently selected, authoritative mission.
local mod=get_mod("HavocConditionManager")
local AiBrain=require("scripts/extension_systems/behavior/ai_brain")
local Locomotion=require("scripts/extension_systems/locomotion/minion_locomotion_extension")
local Melee=require("scripts/extension_systems/behavior/nodes/actions/bt_melee_attack_action")
local HoundLeap=require("scripts/extension_systems/behavior/nodes/actions/bt_chaos_hound_leap_action")
local Leap=require("scripts/extension_systems/behavior/nodes/actions/bt_leap_action")
local ScriptWorld=require("scripts/foundation/utilities/script_world")
local MinionAttack=require("scripts/utilities/minion_attack")
local Difficulty=require("scripts/settings/difficulty/minion_difficulty_settings")
local AnimationSync=require("./animation.lua")
local MOVE,ATTACK,RANGED=2,2,2
local REVISION="1.6.6"
local function weak()return setmetatable({},{__mode="k"})end
local function pack(...)return {n=select("#",...),...}end
local function names(value)local out={};for name in value:gmatch("%S+")do out[name]=true end;return out end
local attack_nodes=names([[BtMeleeAttackAction BtBlockedAction BtGrenadierThrowAction BtQuickGrenadeThrowAction
    BtShootAction BtShootPositionAction BtRunStopAndShootAction BtStepShootAction BtStrafeShootAction
    BtSniperShootAction BtShootNetAction BtShootLiquidBeamAction BtValkyrieShootAction
    BtChaosDaemonhostWarpSweepAction BtChaosDaemonhostWarpGrabAction BtChaosSpawnGrabAction
    BtChaosHoundLeapAction BtChaosHoundTargetPouncedAction BtLeapAction BtChargeAction
    BtMutantChargerChargeAction BtBeastOfNurgleConsumeAction BtBeastOfNurgleConsumeMinionAction
    BtBeastOfNurgleSpitOutAction BtSmashObstacleAction BtChaosPoxwalkerExplodeAction
    BtReloadAction BtWeaponMalfunctionAction BtSwitchWeaponAction BtVoidShieldExplosionAction]])
local ranged_nodes=names([[BtShootAction BtShootPositionAction BtRunStopAndShootAction BtStepShootAction
    BtStrafeShootAction BtSniperShootAction BtValkyrieShootAction BtReloadAction
    BtWeaponMalfunctionAction BtSwitchWeaponAction]])
local shared_shoot_nodes=names([[BtShootAction BtShootPositionAction BtRunStopAndShootAction
    BtStepShootAction BtStrafeShootAction BtShootLiquidBeamAction]])
local move_nodes=names([[BtMeleeFollowTargetAction BtRangedFollowTargetAction BtMoveToCombatVectorAction
    BtMoveToCoverAction BtMoveToPositionAction BtInCoverAction BtChaosHoundApproachAction BtChaosHoundRoamAction
    BtChaosHoundSkulkAction BtBeastOfNurgleMovementAction BtBeastOfNurgleAlignAction
    BtErraticFollowAction BtFlamerApproachAction BtFleeAction BtGrenadierFollowAction
    BtPatrolAction BtPoxwalkerBomberApproachAction BtRenegadeFlamerPatrolAction
    BtRenegadeNetgunnerApproachAction BtRendezvousAction BtRunAwayAction BtSniperMovementAction
    BtDashAction BtExitSpawnerAction]])
local function node_kind(node)
    local name=node and node.tree_node and node.tree_node[1]
    if attack_nodes[name] or node and getmetatable(node)==Melee then return "attack",name end
    if move_nodes[name] then return "move",name end
    return "native",name
end
local function live_extension(unit,name,expected)
    return ALIVE[unit] and expected and not rawget(expected,"__deleted")
        and ScriptUnit.has_extension(unit,name)==expected
end
local function scale_numbers(value,factor)
    if type(value)=="number" then return value>0 and value*factor or value end
    if type(value)~="table" then return value end
    local copy={};for k,v in pairs(value)do copy[k]=scale_numbers(v,factor)end;return copy
end
-- Exact action-data fields consumed by the native attack classes. Do not
-- blanket-match "time": time_per_shot already uses ranged_attack_speed;
-- wall_stun_time/in_air_stagger_duration are received reactions; projectile
-- flight/lifetime and damage-profile tables must retain their native values.
local timing_names=names([[aim_duration aim_durations shoot_interval shot_interval
    time_between_shots time_between_bursts burst_interval sweep_ground_impact_fx_timing
    aoe_threat_timing aoe_threat_duration effect_template_start_timings move_start_timings
    charge_up_time windup_duration recovery_duration grab_timings grab_durations
    grab_durations_missed total_grab_durations smash_timings smash_durations
    smash_sweep_start_timings start_leap_timing land_impact_timing landing_duration
    throw_timing throw_timings throw_duration start_drop_grenade_timing effect_template_timings
    scope_reflection_timing action_duration action_durations after_throw_taunt_duration
    align_duration anim_driven_charge_anim_durations anim_durations anim_move_speed_durations
    aoe_bot_threat_duration aoe_bot_threat_timing attack_anim_damage_timing attack_anim_damage_timings
    attack_anim_duration attack_anim_durations attack_duration attack_sweep_damage_timings
    before_shoot_effect_template_timing blend_timings can_hit_wall_durations charge_direction_durations
    charge_durations close_attack_anim_damage_timing close_attack_anim_duration consume_durations
    consume_timing damage_timings dash_direction_durations dash_durations drag_anim_delay
    drag_anim_exit_delay duration end_durations execute_duration execute_timing fire_timing
    grab_anim_duration heal_durations melee_attack_rotation_durations miss_durations move_durations
    reached_destination_durations rotation_duration rotation_durations scope_reflection_timing_before_shooting
    scope_reflection_timing_effect_template scope_reflection_timing_sfx shoot_timing smash_anim_duration
    smash_damage_timings start_aim_durations start_colliding_with_players_timing start_duration
    start_duration_short start_eat_timings start_effect_timing start_move_rotation_timings
    start_movement_duration start_rotation_timings step_anim_durations step_move_timing stop_duration
    tongue_in_durations tongue_out_durations wall_jump_rotation_duration wall_jump_rotation_timing
    wall_land_duration dodge_tell_sfx_delay damage_frequency lerp_position_time
    first_damage_delay start_execute_at_t max_duration damage_start_time sphere_cast_frequency
    in_sight_duration_shoot_requirement lost_los_fail_duration time_per_shot
    reload_duration switch_weapon_duration malfunction_duration]])
local untouched_tables=names([[damage_profile damage_profiles smash_damage_profile throw_config
    projectile_template liquid_template effect_template attack_intensities utility_weight utility_weights]])
local function factor(key,native_melee,kind,name,rate)
    if kind=="native" then return end
    -- Locomotion transitions and smart-object trajectories use authored
    -- durations/distances. A navigation multiplier is not a traversal clock.
    if kind=="move" then return end
    if name=="BtBlockedAction" then return end -- Native recovery already reads melee_attack_speed.
    -- Shared shooting divides these delays by ranged_attack_speed itself.
    -- Keep the source values intact; the shooting hook supplies the one rate.
    if shared_shoot_nodes[name] and (key=="shoot_timing" or key=="first_shoot_timing" or key=="time_per_shot") then return end
    if key:find("cooldown",1,true) then return 1/(rate or ATTACK) end
    if key=="place_liquid_timing_speed" then return rate or ATTACK end
    if timing_names[key] then
        return 1/(rate or ATTACK)
    end
end
local function action_copy(data,native_melee,kind,name,rate,seen)
    kind=kind or "attack"
    local root=seen==nil
    seen=seen or {};if seen[data] then return end;seen[data]=true
    local changed=false;local copy={}
    for key,value in pairs(data)do
        local f=type(key)=="string" and factor(key,native_melee,kind,name,rate)
        if f and (type(value)=="table" or type(value)=="number") then copy[key]=scale_numbers(value,f);changed=true
        elseif type(value)=="table" and not untouched_tables[key] then
            local nested=action_copy(value,native_melee,kind,name,rate,seen);copy[key]=nested or value;changed=changed or nested~=nil
        else copy[key]=value end
    end
    seen[data]=nil
    -- The standard grenadier reads a difficulty default when no cooldown is
    -- present. Supply it on the private copy so that path is accelerated too.
    if kind=="attack" and data.throw_timings and data.throw_config and not data.cooldown then
        copy.cooldown=scale_numbers(Difficulty.cooldowns.grenadier_throw,1/(rate or ATTACK));changed=true
    end
    if root and kind=="attack" then copy._diy_frenzied_rate=rate or ATTACK;changed=true end
    return changed and copy or nil
end
local function controller(state,unit,breed)
    local current=state.current
    if not current or not current.active or not mod.has_local_gameplay_authority()
        or not Managers.state or Managers.state.game_session~=current.session then return end
    if not breed then
        local data=ScriptUnit.has_extension(unit,"unit_data_system")
        breed=data and data:breed()
    end
    if breed and breed.breed_type=="minion" then return current end
end
local function install_hooks()
    local previous=mod._diy_frenzied_assault_hooks_v1
    assert(not (previous and previous.current and previous.current.active),
        "Frenzied assault: finish the active mission before loading updated hooks")
    local available,why=AnimationSync.available()
    assert(available,"Frenzied assault: "..tostring(why))
    local dmf=get_mod("DMF")
    assert(dmf and type(dmf.set_internal_data)=="function","Frenzied assault needs DMF hook replacement support")
    -- Each mission loads fresh package files, including edits that keep the
    -- same version. Never reactivate a legacy state: removed hooks retain it.
    local state={revision=REVISION,previous_revision=previous and previous.revision}
    local hooks={}
    local function hook(object,method,handler)
        assert(type(object[method])=="function","Frenzied assault missing hook target: "..method)
        hooks[#hooks+1]={object,method,handler}
    end
    hook(AiBrain,"update",function(fn,self,unit,...)
        local current=controller(state,unit,self._breed)
        if not current then return fn(self,unit,...)end
        current:movement(unit,self._breed,self)
        local tree=self._behavior_tree
        local nodes=current.trees[tree]
        if not nodes then
            nodes={};local seen={}
            local function visit(node)
                if seen[node] then return end;seen[node]=true
                if node.tree_node and node.tree_node.action_data then
                    local kind,name=node_kind(node)
                    if kind=="attack" then
                        local speed=(name=="BtMeleeAttackAction" or name=="BtBlockedAction") and "melee"
                            or ranged_nodes[name] and "ranged" or "special"
                        nodes[speed]=true
                        nodes[#nodes+1]={tree_node=node.tree_node,native_melee=getmetatable(node)==Melee,
                            kind=kind,name=name,speed=speed,cache=weak()}
                    end
                end
                for _,child in ipairs(node:children())do visit(child)end
            end
            visit(tree:root());current.trees[tree]=nodes
        end
        -- Native brains share tree nodes. Swap only during this synchronous
        -- update and restore even when native code raises an error.
        local record=current.moves[unit]
        -- Reuse swap storage, including a separate slot for a reentrant hook.
        -- Movement data is unchanged and never needs copying or swapping.
        local depth=(record.swap_depth or 0)+1;record.swap_depth=depth
        local slots=record.swap_slots or {};record.swap_slots=slots
        local slot=slots[depth]
        if not slot then slot={originals={},replacements={}};slots[depth]=slot end
        local originals,replacements=slot.originals,slot.replacements
        local melee_rate=nodes.melee and current:attack_rate(unit,"BtMeleeAttackAction")
        local ranged_rate=nodes.ranged and current:attack_rate(unit,"BtShootAction")
        for i,entry in ipairs(nodes)do
            local node=entry.tree_node
            local original=node.action_data;originals[i]=original
            -- Keep one action's rate fixed through all of its hit/FX/recovery
            -- phases. New actions pick up other native speed buffs normally.
            local rate=record.node and record.node.tree_node==node and record.attack_rate
                or (entry.speed=="melee" and melee_rate or entry.speed=="ranged" and ranged_rate or ATTACK)
            local cache=entry.cache[rate]
            if not cache then cache=weak();entry.cache[rate]=cache end
            local modified=cache[original]
            if modified==nil then modified=current.action_copy(original,entry.native_melee,entry.kind,entry.name,rate) or false;cache[original]=modified end
            replacements[i]=modified
        end
        for i,entry in ipairs(nodes)do if replacements[i] then entry.tree_node.action_data=replacements[i]end end
        local results=pack(pcall(fn,self,unit,...))
        local leaf=self._running_leaf_node
        record.node=leaf
        record.attack_rate=leaf and leaf.tree_node.action_data and leaf.tree_node.action_data._diy_frenzied_rate
        for i,entry in ipairs(nodes)do entry.tree_node.action_data=originals[i]end
        table.clear(originals);table.clear(replacements);record.swap_depth=depth-1
        if not results[1] then error(results[2],0)end
        current:sync_motion(record)
        return unpack(results,2,results.n)
    end)
    hook(Melee,"_start_attack_anim",function(fn,self,unit,breed,target,t,spawn,pad,data,...)
        local current=data._diy_frenzied_rate and controller(state,unit,breed)
        if not current then return fn(self,unit,breed,target,t,spawn,pad,data,...)end
        -- The whole animation has already been scaled. Prevent the native
        -- recovery-only speed path from shortening it a second time.
        local speed=pad.melee_attack_speed;pad.melee_attack_speed=nil
        local results=pack(pcall(fn,self,unit,breed,target,t,spawn,pad,data,...))
        pad.melee_attack_speed=speed
        if not results[1] then error(results[2],0)end
        local hit=pad.start_sweep_t or pad.attack_timing
        if not current.melee_timing_logged and type(hit)=="number" and type(pad.attack_duration)=="number" then
            current.melee_timing_logged=true
            current.log(string.format("[Frenzied assault %s] attack_timing=melee rate=%.2f first_hit_delay=%.4f action_end_delay=%.4f",REVISION,data._diy_frenzied_rate,hit-t,pad.attack_duration-t))
        end
        return unpack(results,2,results.n)
    end)
    -- Advance along the native leap curve faster, retaining its geometry and
    -- sweeping the entire travelled interval. The caller still uses real dt.
    for _,spec in ipairs({{HoundLeap,3},{Leap,2}})do
        local class,index=spec[1],spec[2]
        hook(class,"_check_leap_for_collisions",function(fn,self,pad,...)
            local loco=pad.locomotion_extension
            if not loco or not controller(state,loco._unit) or pad.state=="in_air_stagger" or pad.state=="falling" then
                return fn(self,pad,...)
            end
            local args=pack(...)
            args[index],args[index+1]=args[index]*ATTACK,args[index+1]*ATTACK
            return fn(self,pad,unpack(args,1,args.n))
        end)
    end
    -- Script-driven charges bypass both navigation and animation translation.
    -- Scale their horizontal desired velocity once; leave gravity/knockback alone.
    for _,method in ipairs({"set_wanted_velocity","set_wanted_velocity_flat"})do
        hook(Locomotion,method,function(fn,self,velocity)
            local current=controller(state,self._unit)
            local record=current and current.moves[self._unit]
            local _,name=node_kind(record and record.brain and record.brain._running_leaf_node)
            if name=="BtMutantChargerChargeAction" or name=="BtChargeAction" or name=="BtExitSpawnerAction" or name=="BtInCoverAction" then
                velocity=Vector3(velocity.x*MOVE,velocity.y*MOVE,velocity.z)
            end
            return fn(self,velocity)
        end)
    end
    hook(MinionAttack,"start_shooting",function(fn,unit,pad,t,data,...)
        local prior=pad.before_shoot_effect_template_timing
        local results=pack(fn(unit,pad,t,data,...))
        if controller(state,unit) and data._diy_frenzied_rate then
            local rate=data._diy_frenzied_rate
            pad.next_shoot_timing=t+(pad.next_shoot_timing-t)*pad.shoot_attack_speed/rate
            pad.shoot_attack_speed=rate
            local current=state.current
            if not current.shoot_timing_logged then
                current.shoot_timing_logged=true
                current.log(string.format("[Frenzied assault %s] attack_timing=shoot rate=%.2f first_shot_delay=%.4f",REVISION,rate,pad.next_shoot_timing-t))
            end
        end
        if controller(state,unit) and data.before_shoot_effect_template_timing and not prior then
            -- Native first-shot FX uses the unscaled first_shoot_timing.
            pad.before_shoot_effect_template_timing=pad.next_shoot_timing-data.before_shoot_effect_template_timing
        end
        return unpack(results,1,results.n)
    end)
    hook(ScriptWorld,"update",function(fn,world,dt,...)
        local current=state.current
        local snapshots=current and current.active and mod.has_local_gameplay_authority()
            and Managers.state and Managers.state.game_session==current.session and AnimationSync.before(current,world,dt)
        local results=pack(fn(world,dt,...))
        if snapshots and state.current==current and current.active then
            AnimationSync.after(snapshots,current)
        end
        return unpack(results,1,results.n)
    end)
    hook(Locomotion,"set_anim_translation_scale",function(fn,self,value)
        local current=controller(state,self._unit)
        local record=current and current.moves[self._unit]
        if record and record.loco==self then
            if record.translation then record.translation:store(value)else record.translation=Vector3Box(value)end
            local traversal=live_extension(self._unit,"navigation_system",record.nav) and record.nav:is_using_smart_object()
            return fn(self,value*(traversal and 1 or record.multiplier))
        end
        return fn(self,value)
    end)
    hook(Locomotion,"anim_translation_scale",function(fn,self)
        local current=controller(state,self._unit)
        local record=current and current.moves[self._unit]
        if record and record.loco==self and record.translation then return record.translation:unbox()end
        return fn(self)
    end)
    -- DMF replaces this owner's handler in place, preserving other mods and
    -- the hook's enabled state. Limit rehook permission to this synchronous
    -- registration; inactive partial installs safely pass through on failure.
    local allowed=mod:get_internal_data("allow_rehooking")
    dmf.set_internal_data(mod,"allow_rehooking",true)
    local ok,why=pcall(function()
        for _,spec in ipairs(hooks)do mod:hook(unpack(spec))end
    end)
    dmf.set_internal_data(mod,"allow_rehooking",allowed)
    if not ok then error(why,0)end
    mod._diy_frenzied_assault_hooks_v1=state
    return state
end
local function activate(ctx)
    local state=install_hooks()
    local current={active=true,session=Managers.state.game_session,world=Managers.world:world("level_world"),
        moves=weak(),trees=weak(),action_copy=action_copy,log=function(message)ctx:log(message)end}
    function current:attack_rate(unit,name)
        if name~="BtMeleeAttackAction" and name~="BtBlockedAction" and not ranged_nodes[name] then return ATTACK end
        local buffs=ScriptUnit.has_extension(unit,"buff_system")
        local stats=buffs and buffs:stat_buffs()
        local speed=stats and stats[ranged_nodes[name] and "ranged_attack_speed" or "melee_attack_speed"]
        return speed and speed>0 and speed or (ranged_nodes[name] and RANGED or ATTACK)
    end
    function current:animation_rate(brain)
        if not brain then return 1 end
        local kind,name=node_kind(brain._running_leaf_node)
        if kind=="native" then return 1 end
        local record=self.moves[brain._unit]
        if record and live_extension(brain._unit,"navigation_system",record.nav) and record.nav:is_using_smart_object() then return 1 end
        local pad=brain._scratchpad
        if pad.state=="in_air_stagger" or pad.state=="falling" or pad.running_stagger_duration then return 1 end
        if kind=="move" then
            -- Authored start/stop/root-driven intervals keep their native
            -- clock. Once moving, this also covers constant-speed clips and
            -- custom blends which never read anim_move_speed.
            if pad.is_anim_driven or pad.start_move_event_anim_speed_duration
                or pad.behavior_component and pad.behavior_component.move_state=="idle" then return 1 end
            return MOVE
        end
        if name=="BtMutantChargerChargeAction" or name=="BtChargeAction" then
            if pad.state=="charging" or pad.state=="navigating" then
                if name=="BtMutantChargerChargeAction" and pad.current_charge_speed
                    and not pad.is_anim_driven and not pad.anim_move_speed_duration then
                    local data=brain._running_leaf_node.tree_node.action_data
                    local ratio=pad.current_charge_speed/data.animation_charge_speed
                    local native_variable=math.clamp(ratio,data.min_animation_variable,data.max_animation_variable)
                    return native_variable>0 and ratio*MOVE/native_variable or MOVE
                end
                return MOVE
            end
        end
        return kind=="attack" and (record and record.attack_rate or ATTACK) or MOVE
    end
    function current:sync_motion(record)
        local brain=record.brain
        local pad=brain and brain._scratchpad or {}
        local kind=node_kind(brain and brain._running_leaf_node)
        local traversal=live_extension(brain._unit,"navigation_system",record.nav) and record.nav:is_using_smart_object()
        local reacting=pad.state=="in_air_stagger" or pad.state=="falling" or pad.running_stagger_duration
        -- Seeking skips root motion; its attack path retains the
        -- compensation. Native locomotion playback must not multiply distance
        -- again, and smart objects must retain their exact XYZ geometry.
        local multiplier=kind=="attack" and not traversal and not reacting and MOVE or 1
        if record.multiplier~=multiplier then
            record.multiplier=multiplier
            if record.translation and live_extension(brain._unit,"locomotion_system",record.loco) then
                record.loco:set_anim_translation_scale(record.translation:unbox())
            end
        end
    end
    function current:movement(unit,breed,brain)
        if self.moves[unit] then self.moves[unit].brain=brain;return end
        local nav=ScriptUnit.has_extension(unit,"navigation_system")
        local loco=ScriptUnit.has_extension(unit,"locomotion_system")
        local record={nav=nav,loco=loco,multiplier=1,brain=brain};self.moves[unit]=record
        if live_extension(unit,"navigation_system",nav) then record.modifier=nav:add_movement_modifier(MOVE)end
        if live_extension(unit,"locomotion_system",loco) then
            local translation=loco:anim_translation_scale()
            record.translation=Vector3Box(translation)
            loco:set_anim_translation_scale(translation)
        end
    end
    ctx:on_cleanup(function()
        current.active=false
        if state.current==current then state.current=nil end
        for unit,record in pairs(current.moves)do
            if record.modifier and live_extension(unit,"navigation_system",record.nav) then record.nav:remove_movement_modifier(record.modifier)end
            if record.translation and live_extension(unit,"locomotion_system",record.loco) then record.loco:set_anim_translation_scale(record.translation:unbox())end
        end
        current.moves=weak();current.trees=weak()
        current.animation_records=nil;current.animation_snapshots=nil;current.animation_seen=nil
    end)
    state.current=current
    if state.previous_revision then
        ctx:log(string.format("[Frenzied assault %s] hooks=reloaded previous=%s scope=new_mission",REVISION,tostring(state.previous_revision)))
    end
    ctx:log(string.format("[Frenzied assault %s] move=%.2f melee=+%.2f ranged=+%.2f special=%.2f stagger=native movement_animation=in_place traversal=native attack_animation=in_place engine=1.12.5 unit_ref=low32_shift2 clock_validation=per_unit_pass scope=local_authority",REVISION,MOVE,ATTACK-1,RANGED-1,ATTACK))
end
return {api_version={major=1,minor=0},entries={frenzied_assault={on_activate=activate}}}
