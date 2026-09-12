-- Finite overflow from the route plan. Retry real, hidden navigation positions
-- in later waves; do not manufacture positions or discard unavailable quotas.
local mod=get_mod("HavocConditionManager")
local Monster=require("scripts/managers/pacing/monster_pacing/monster_pacing")
local Placement=mod.spawn_placement
local M={}
local INTERVAL,RETRY,MAX_MONSTERS,MAX_PATROLS=20,2,3,2
function M.plan(self,monsters,patrols)
    self._hcm_encounter_reserve=nil
    if monsters>0 or patrols>0 then
        self._hcm_encounter_reserve={monsters=monsters,patrols=patrols,initial_monsters=monsters,initial_patrols=patrols,groups={},next_check=0}
    end
end
local function active_monsters(self)
    local count=0
    local breeds=mod.template_registry.breeds
    for _,record in ipairs(self._alive_monsters or {}) do
        local breed=breeds[record.breed_name]
        local tags=breed and breed.tags or {}
        if HEALTH_ALIVE[record.spawned_unit] and tags.monster and not tags.captain then count=count+1 end
    end
    return count
end
local function active_patrols(reserve,system)
    for i=#reserve.groups,1,-1 do
        local group=system:group_from_id(reserve.groups[i])
        if not group or #group.members==0 then table.remove(reserve.groups,i) end
    end
    return #reserve.groups
end
local function spawn_patrol(self,reserve,position,side_id)
    local settings=self._template.boss_patrols
    local record={breed_list=settings.breed_lists,spawn_position=Vector3Box(position),sound_events=settings.sound_events}
    reserve.job=mod.queue_native_patrol(self,record,side_id,reserve)
    return reserve.job and "pending" or false
end
local function served(reserve,monster,t)
    reserve.next_at=math.max(reserve.next_at or 0,t+INTERVAL)
    reserve.run=reserve.last_monster==monster and (reserve.run or 0)+1 or 1
    reserve.last_monster=monster
end
local function replenish(self,reserve,t,side_id,target_side_id)
    reserve.next_check=t+RETRY
    if reserve.job then
        if reserve.job.completed then
            reserve.patrols=reserve.patrols-1
            served(reserve,false,reserve.job.finished_at)
            reserve.job=nil
        end
    end
    local pacing=Managers.state.pacing
    if pacing:get_in_safe_zone() then reserve.next_at=nil;return end
    if not reserve.next_at then reserve.next_at=t+INTERVAL;return end
    if t<reserve.next_at then return end
    if not Managers.state.pacing:spawn_type_enabled("monsters") then return end
    local main=Managers.state.main_path
    local target,distance=main:ahead_unit(target_side_id)
    local target_position=target and POSITION_LOOKUP[target]
    if not target_position or not distance then return end
    -- Let an already-due route encounter use this update first.
    for _,record in ipairs(self._monsters or {}) do if record.travel_distance<=distance then return end end
    for _,record in ipairs(self._boss_patrols or {}) do if record.travel_distance<=distance then return end end
    local group_system=Managers.state.extension:system("group_system")
    local monster_ready=reserve.monsters>0 and active_monsters(self)<MAX_MONSTERS
    local patrol_ready=reserve.patrols>0 and not reserve.job and active_patrols(reserve,group_system)<MAX_PATROLS
    if not monster_ready and not patrol_ready then return end
    -- Weighted finish time: a large boss backlog cannot starve patrols.
    local choose_monster=monster_ready and (not patrol_ready or
        (reserve.initial_monsters-reserve.monsters+1)/reserve.initial_monsters<=
        (reserve.initial_patrols-reserve.patrols+1)/reserve.initial_patrols)
    -- Even a highly unequal custom quota gives a waiting, ready class a turn
    -- after at most three successful admissions of the other class.
    if monster_ready and patrol_ready and (reserve.run or 0)>=3 and reserve.last_monster==choose_monster then
        choose_monster=not choose_monster
    end
    local context=Placement.context(side_id,target_side_id,t)
    local position=context and Placement.anchor(context,reserve)
    if not position then return end
    local function attempt(monster)
        local success
        if monster then
            local template=self._template
            local breeds=template.breed_names.monsters
            local breed=breeds[math.random(#breeds)]
            local record={travel_distance=distance,breed_name=breed,position=Vector3Box(position),spawn_type="monsters",
                stinger=template.spawn_stingers and template.spawn_stingers[breed],
                despawn_distance_when_passive=template.despawn_distance_when_passive and template.despawn_distance_when_passive[breed]}
            self:_spawn_monster(record,target,side_id)
            success=record.spawned_unit~=nil
            if success then reserve.monsters=reserve.monsters-1 end
        else
            success=spawn_patrol(self,reserve,position,side_id)
        end
        return success
    end
    local success=attempt(choose_monster)
    if not success and (choose_monster and patrol_ready or not choose_monster and monster_ready) then
        choose_monster=not choose_monster;success=attempt(choose_monster)
    end
    -- Reserve an admission interval without charging an unfinished patrol.
    -- If its footprint stays blocked, ready monsters still get later turns.
    if success=="pending" then reserve.next_at=t+INTERVAL;return
    elseif success then
        served(reserve,choose_monster,t)
    end
end
mod:hook(Monster,"update",function(fn,self,dt,t,side_id,target_side_id)
    mod.update_patrol_spawns(self,t,side_id,target_side_id)
    local reserve=self._hcm_encounter_reserve
    if reserve and not self._disabled and mod.has_local_gameplay_authority() and t>=reserve.next_check then
        if reserve.monsters==0 and reserve.patrols==0 then self._hcm_encounter_reserve=nil
        else replenish(self,reserve,t,side_id,target_side_id) end
    end
    return fn(self,dt,t,side_id,target_side_id)
end)
mod.finish_encounter_reserve=function(self)
    self._hcm_encounter_reserve=nil
    mod.finish_patrol_spawns(self)
end
mod:hook_safe(Monster,"destroy",mod.finish_encounter_reserve)
return M
