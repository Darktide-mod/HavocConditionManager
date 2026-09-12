-- Committed enemies and verified rear ambient roamers share one quiet timer.
-- Native cached progress admits untouched roamers without pathfinding.
local mod=get_mod("HavocConditionManager")
local Roamer=require("scripts/managers/pacing/roamer_pacing/roamer_pacing")
local Monster=require("scripts/managers/pacing/monster_pacing/monster_pacing")
local Horde=require("scripts/managers/horde/horde_manager")
local Perception=require("scripts/extension_systems/perception/minion_perception_extension")
local Health=require("scripts/extension_systems/health/health_extension")
local Placement=mod.spawn_placement
local CHECK_INTERVAL,QUIET_TIME,DISTANCE_SQ=5,30,35*35
local READY_LIMIT,REMOVE_INTERVAL=64,0.25
local PASSIVE_REAR_DISTANCE,PASSIVE_ANCHOR_SQ=60,12*12
local MAX_CREDITS,MAX_CREDIT_UNITS,SPAWN_INTERVAL=32,256,0.25
local state,patrol_context
local function current()
    if not state then state={credits={},next_remove=0,next_spawn=0,credit_units=0,credit_cursor=1,
        ready={},ready_index=1,ready_size=0} end
    return state
end
local function extension(unit,name) return ScriptUnit.has_extension(unit,name) end
local function native_group(unit)
    local ext=extension(unit,"group_system")
    return ext and ext.group and ext:group()
end
local function attach(unit,owner,record,side_id,origin)
    local ext=unit and extension(unit,"perception_system")
    local breed=ext and ext._breed
    local tags=breed and breed.tags or {}
    if not breed or breed.breed_type~="minion" or tags.special or tags.monster or tags.captain or tags.companion then return end
    local group=native_group(unit)
    if group and origin then
        group._hcm_recycling=group._hcm_recycling or origin;origin=group._hcm_recycling
    end
    local meta=ext._hcm_straggler
    if not meta then
        current()
        meta={next_check=0,side_id=side_id};ext._hcm_straggler=meta
    end
    if owner then meta.owner=owner;meta.record=record;meta.kind="roamers" end
    meta.group=group;meta.origin=origin or meta.origin
    if origin then meta.kind=origin.kind;meta.health=origin.health;meta.replacement=origin.replacement end
    return meta
end
mod:hook_safe(Roamer,"_try_activate_roamer",function(self,record,side_id)
    if mod.has_local_gameplay_authority() and record.active and record.spawned_unit then
        attach(record.spawned_unit,self,record,side_id,record.patrol_id and {kind="roamers"})
    end
end)
-- Observe only native pacing patrol creation. Mission-controlled and expedition
-- loot patrols retain their original ownership and cannot enter this pool.
mod:hook(Monster,"_spawn_boss_patrol",function(fn,self,record,ahead_distance,side_id,...)
    if mod.has_local_gameplay_authority() and self._pacing_type=="default" then
        return mod.queue_native_patrol(self,record,side_id)
    end
    local previous=patrol_context
    patrol_context=mod.has_local_gameplay_authority() and
        (self._pacing_type=="default" or self._hcm_recyclable_patrol) and {kind="monsters"} or nil
    local ok,result=pcall(fn,self,record,ahead_distance,side_id,...)
    patrol_context=previous
    if not ok then error(result,0) end
    return result
end)
mod:hook(Horde,"horde",function(fn,self,kind,template,side_id,target_side_id,composition,...)
    local previous=patrol_context
    local previous_batch=mod.current_spawn_batch
    local params=select(9,...)
    patrol_context=mod.has_local_gameplay_authority() and template=="trickle_horde" and
        not (previous_batch and previous_batch.event) and
        not (params and (params.externally_controlled_patrol or params.mutator_name)) and
        {kind="trickle_hordes",health=select(5,...)} or nil
    if mod.has_local_gameplay_authority() and not previous_batch then
        local batch=mod.new_spawn_batch(template,side_id,target_side_id,params and (params.externally_controlled_patrol or params.mutator_name))
        batch.horde=true;batch.kind=template=="trickle_horde" and "trickle_hordes" or "hordes"
        mod.current_spawn_batch=batch
    end
    local ok,a,b,c,d,e=pcall(fn,self,kind,template,side_id,target_side_id,composition,...)
    patrol_context=previous
    mod.current_spawn_batch=previous_batch
    if not ok then error(a,0) end
    return a,b,c,d,e
end)

mod.track_redeployed_unit=function(unit)
    local board=BLACKBOARDS and BLACKBOARDS[unit]
    local sides=Managers.state.extension:system("side_system")
    local side=sides.side_by_unit[unit]
    if not board or not side then return end
    local group=native_group(unit)
    local batch=mod.current_spawn_batch
    local meta=attach(unit,nil,nil,side.side_id,group and group._hcm_recycling or patrol_context)
    if not meta then return end
    meta.kind=meta.kind or batch and batch.kind or "hordes"
    meta.protected=batch and (batch.protected_objective or batch.event and batch.source~="mission_spawner")
    if board.spawn and board.spawn.spawn_source=="hcm_redeployed" then meta.replacement=true end
end
local function has_objective(unit)
    local objective=extension(unit,"mission_objective_target_system")
    if not objective then return false end
    if not objective.objective_name then return true end
    local name=objective:objective_name()
    return objective._registered_objective or name and name~="" and name~="default"
end
local function sample(ext,unit,meta)
    local board=BLACKBOARDS and BLACKBOARDS[unit]
    local perception=board and board.perception
    if not HEALTH_ALIVE[unit] or ext._is_perception_disabled or not perception then return end
    if perception.aggro_state=="aggroed" then meta.engaged=true end
    if perception.has_line_of_sight then return end
    local side=ext._side_system and ext._side_system.side_by_unit[unit]
    local players=side and side.enemy_player_units
    local position=POSITION_LOOKUP[unit]
    if not position or not players or #players==0 or #players>8 then return end
    local count,nearest=0,math.huge
    for _,player in ipairs(players) do
        if HEALTH_ALIVE[player] then
            local player_position=POSITION_LOOKUP[player]
            if not player_position then return end
            local distance=Vector3.distance_squared(position,player_position)
            nearest=math.min(nearest,distance)
            if ext:has_line_of_sight(player) then return end
            count=count+1
        end
    end
    if count==0 then return end
    if nearest<DISTANCE_SQ then return end
    local spawn=board.spawn
    if not spawn or spawn.is_exiting_spawner then return end
    local group=board.group_data
    if meta.protected or has_objective(unit) or group and group.owning_auto_event_id and group.owning_auto_event_id~="" then
        return
    end
    if meta.record and (meta.record._hcm_retired or meta.record.spawned_unit~=unit) then return end
    local manager=Managers.state.minion_spawn
    if not manager or not manager._spawned_minions_index_lookup[unit] or manager._minions_with_owners[unit] then
        return
    end
    local health=extension(unit,"health_system")
    if not health or health.is_invulnerable and health:is_invulnerable() then return end
    if not meta.engaged and not meta.origin then
        -- Only the still-local authored record proves an untouched roamer's
        -- location. Never use the leading player's progress or a guessed
        -- projection on stacked floors, open maps or a wandering unit.
        local record=meta.record
        local main=Managers.state.main_path
        local pacing=Managers.state.pacing
        if not record or not record.position or not record.travel_distance or not main or
            not main.is_main_path_ready or not main:is_main_path_ready() or
            not main.path_type or main:path_type()~="linear" or not main.behind_unit or
            not pacing or not pacing._target_side_id then
            return
        end
        if Vector3.distance_squared(position,record.position:unbox())>PASSIVE_ANCHOR_SQ then
            return
        end
        local behind,progress=main:behind_unit(pacing._target_side_id)
        if not behind or not HEALTH_ALIVE[behind] or not progress or progress~=progress or
            math.abs(progress)==math.huge or record.travel_distance~=record.travel_distance or
            math.abs(record.travel_distance)==math.huge then
            return
        end
        if progress-record.travel_distance<PASSIVE_REAR_DISTANCE then return end
    end
    return players
end
local function rejoin_orphan(ext,unit,meta,t)
    if t<(current().next_rejoin or 0) or meta.rejoined or not meta.group or not meta.origin or meta.replacement then return end
    local board=BLACKBOARDS[unit];local patrol=board and board.patrol;local perception=board and board.perception
    local group=board and board.group_data
    if not HEALTH_ALIVE[unit] or ext._is_perception_disabled or not patrol or not patrol.should_patrol or
        (patrol.patrol_index or 0)<=1 or HEALTH_ALIVE[patrol.patrol_leader_unit] or not perception or perception.target_unit or
        perception.lock_target or group and (group.group_target or group.owning_auto_event_id and group.owning_auto_event_id~="") or
        meta.protected or has_objective(unit) then return end
    local nav=extension(unit,"navigation_system");local manager=Managers.state.minion_spawn
    if not nav or not nav.is_using_smart_object or nav:is_using_smart_object() or not manager or manager._minions_with_owners[unit] then return end
    local side=ext._side_system.side_by_unit[unit]
    for _,player in ipairs(side and side.enemy_player_units or {}) do
        if HEALTH_ALIVE[player] and side.ai_target_units and side.ai_target_units[player] then
            ext:alert(player);ext:aggro();meta.rejoined=true
            current().next_rejoin=t+0.15
            return
        end
    end
end
mod:hook_safe(Perception,"update",function(self,unit,dt,t)
    local meta=self._hcm_straggler
    if not meta or not mod.has_local_gameplay_authority() or t<meta.next_check then return end
    meta.next_check=t+CHECK_INTERVAL
    rejoin_orphan(self,unit,meta,t)
    local s=current()
    local players=sample(self,unit,meta)
    if not players then
        meta.since=nil;return
    end
    if not meta.since then meta.since=t end
    if t-math.max(meta.since,meta.last_damage or 0)<QUIET_TIME then return end
    if meta.enqueued then return end
    if s.ready_size<READY_LIMIT then
        s.ready[(s.ready_index+s.ready_size-1)%READY_LIMIT+1]=unit
        s.ready_size=s.ready_size+1;meta.enqueued=true
    end
end)
mod:hook_safe(Health,"add_damage",function(self,amount)
    if not amount or amount<=0 then return end
    local ext=self._unit and extension(self._unit,"perception_system")
    local meta=ext and ext._hcm_straggler
    if meta then meta.engaged=true;meta.last_damage=Managers.time:time("gameplay");if meta.since then meta.since=meta.last_damage end end
end)
local function add_credit(s,meta,breed,t)
    if meta.replacement then return end
    if s.credit_units>=MAX_CREDIT_UNITS then return end
    local last
    for _,credit in ipairs(s.credits) do
        if not credit.inflight and #credit.breeds<64 and credit.kind==meta.kind and
            credit.side_id==meta.side_id and credit.health==meta.health then last=credit;break end
    end
    if last then
        last.breeds[#last.breeds+1]=breed
    elseif #s.credits<MAX_CREDITS then
        if #s.credits==0 then s.next_spawn=math.max(s.next_spawn,t+SPAWN_INTERVAL) end
        s.credits[#s.credits+1]={breeds={breed},side_id=meta.side_id,kind=meta.kind,health=meta.health}
    else return end
    s.credit_units=s.credit_units+1
end
local function recycle(s,t)
    if s.ready_size==0 or t<s.next_remove then return end
    local unit=s.ready[s.ready_index]
    s.ready[s.ready_index]=nil;s.ready_index=s.ready_index%READY_LIMIT+1;s.ready_size=s.ready_size-1
    -- One per update, spaced in time; no catch-up burst after a slow frame.
    s.next_remove=t+REMOVE_INTERVAL
    local ext=extension(unit,"perception_system");local meta=ext and ext._hcm_straggler
    if not meta then return end
    meta.enqueued=nil
    if not meta.since or t-math.max(meta.since,meta.last_damage or 0)<QUIET_TIME then return end
    local players=sample(ext,unit,meta)
    if not players or not ext.immediate_line_of_sight_check then
        meta.since=nil;return
    end
    for _,player in ipairs(players) do
        if HEALTH_ALIVE[player] then
            if ext:immediate_line_of_sight_check(player) then
                meta.since=nil;return
            end
        end
    end
    local manager=Managers.state.minion_spawn
    mod.retiring_units[unit]=true;manager:despawn_minion(unit)
    if manager._spawned_minions_index_lookup[unit] then mod.retiring_units[unit]=nil;return end
    ext._hcm_straggler=nil
    if meta.record then meta.record._hcm_retired=true;meta.record.active=true;meta.owner._roamer_lookup[unit]=nil end
    add_credit(s,meta,ext._breed.name,t)
end
local function replenish(s,pacing,t)
    if t<s.next_spawn or #s.credits==0 then return end
    s.next_spawn=t+SPAWN_INTERVAL
    if s.inflight then return end
    local manager=Managers.state.minion_spawn
    -- Native admission checks use '>'; leave headroom for other spawners.
    local capacity=math.floor(145*mod.template_runtime.config().coarse.combat_tolerance+0.5)
    if manager._spawn_queue_size>=16 or manager:total_allocated_num_enemies()+1>capacity-4 then
        s.next_spawn=t+1;return
    end
    -- A paused class cannot monopolize the head of the finite allowance list.
    -- Only one selected credit can query positions or enter the native queue.
    local credit
    local n=#s.credits
    for offset=0,n-1 do
        local index=(s.credit_cursor+offset-1)%n+1
        local candidate=s.credits[index]
        if t>=(candidate.next_try or 0) then
            if pacing:spawn_type_enabled(candidate.kind or "roamers") then
                credit=candidate;s.credit_cursor=index%n+1;break
            end
            candidate.next_try=t+1
        end
    end
    if not credit then return end
    local count=#credit.breeds-(credit.index or 1)+1
    local context=Placement.context(credit.side_id,pacing._target_side_id,t)
    if not context then credit.next_try=t+1;return end
    context.prefer_near=true
    if not credit.positions then
        local anchor,reason=Placement.anchor(context,credit)
        if not anchor then
            credit.next_try=t+(reason=="pending" and 0.25 or 1)
            return
        end
        local positions={}
        local num=GwNavQueries.flood_fill_from_position(pacing._nav_world,anchor,2,2,math.min(count,8),positions)
        if not num or num<1 then credit.next_try=t+1;return end
        credit.positions={};credit.position_index=1
        for i=1,num do credit.positions[i]=Vector3Box(positions[i]) end
    end
    local position=credit.positions[credit.position_index]:unbox()
    local valid,_,_,reason=Placement.valid(context,position)
    if not valid then
        credit.position_index=credit.position_index+1
        if reason~="footprint" or credit.position_index>#credit.positions then credit.positions=nil end
        return
    end
    if #credit.breeds>1 and not credit.group_id then
        local system=Managers.state.extension:system("group_system")
        credit.group_id=system:generate_group_id()
        system:lock_group_id(credit.group_id)
        system:group_from_id(credit.group_id)._hcm_recycling={kind=credit.kind,replacement=true}
    end
    local params=manager:queue_minion_to_spawn(credit.breeds and credit.breeds[credit.index or 1] or credit.breed,
        position,Quaternion.identity(),credit.side_id)
    params.spawn_source="hcm_redeployed";params.optional_aggro_state="aggroed"
    params.optional_target_unit=context.target;params.optional_group_id=credit.group_id;params.optional_health_modifier=credit.health
    params._hcm_redeployment={owner=s,credit=credit,target_side_id=pacing._target_side_id}
    credit.inflight=true;s.inflight=credit
end
-- A queued native request may wait several frames. Validate again at actual
-- consumption, and return a refused unit to its credit instead of losing it.
mod.prepare_redeployment=function(ticket,entry)
    if ticket.owner~=state or not mod.has_local_gameplay_authority() then return false end
    local pacing=Managers.state.pacing
    local t=Managers.time:time("gameplay")
    local credit=ticket.credit
    if not pacing:spawn_type_enabled(credit.kind or "roamers") then return false end
    local context=Placement.context(credit.side_id,ticket.target_side_id,t)
    if not context or not Placement.valid(context,entry.position:unbox()) then return false end
    entry.optional_target_unit=context.target
    return true
end
mod.finish_redeployment=function(ticket,unit)
    local s,credit=ticket.owner,ticket.credit
    credit.inflight=nil
    if s~=state then return end
    s.inflight=nil
    local t=Managers.time:time("gameplay")
    s.next_spawn=math.max(s.next_spawn,t+SPAWN_INTERVAL)
    if not unit then credit.positions=nil;credit.next_try=t+0.25;return end
    credit.index=(credit.index or 1)+1;credit.position_index=credit.position_index+1;s.credit_units=s.credit_units-1
    if credit.position_index>#credit.positions then credit.positions=nil end
    if credit.index>(credit.breeds and #credit.breeds or 1) then
        for index,item in ipairs(s.credits) do
            if item==credit then
                table.remove(s.credits,index)
                if index<s.credit_cursor then s.credit_cursor=s.credit_cursor-1 end
                break
            end
        end
        s.credit_cursor=(s.credit_cursor-1)%math.max(#s.credits,1)+1
        if credit.group_id then Managers.state.extension:system("group_system"):unlock_group_id(credit.group_id) end
        s.next_spawn=t+SPAWN_INTERVAL
    end
end

mod.update_straggler_recycling=function(pacing,t)
    if not state or not mod.has_local_gameplay_authority() then return end
    recycle(state,t);replenish(state,pacing,t)
end
mod.finish_straggler_recycling=function()
    if state then
        local s=state
        local system=Managers.state.extension and Managers.state.extension:system("group_system")
        for _,credit in ipairs(s.credits) do if system and credit.group_id then system:unlock_group_id(credit.group_id) end end
    end
    state=nil;patrol_context=nil
end
return true
