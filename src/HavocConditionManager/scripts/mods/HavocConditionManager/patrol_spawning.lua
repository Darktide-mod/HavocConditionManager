-- Native patrol composition, groups, formation and unit creation, admitted one
-- member at a time. Only finite route/reserve patrols use this pending list.
local mod=get_mod("HavocConditionManager")
local Placement=mod.spawn_placement
local MainPath=require("scripts/utilities/main_path_queries")
local Blackboard=require("scripts/extension_systems/blackboard/utilities/blackboard")
local Patrols=require("scripts/utilities/minion_patrols")
local INTERVAL,RETRY=0.15,2
local function new_job(self,record,side_id,reserve)
    local faction=Managers.state.pacing:current_faction()
    local templates=record.breed_list[faction].challenge_templates
    local lists=Managers.state.difficulty:get_table_entry_by_challenge(templates)
    local list=lists[math.random(1,#lists)]
    local job={breeds=list,index=1,units={},side_id=side_id,next_at=0,reserve=reserve,
        sound=record.sound_events and record.sound_events[faction]}
    if record.spawn_point_travel_distance then
        local position=MainPath.position_from_distance(record.spawn_point_travel_distance)
        if position then job.anchor=Vector3Box(position) end
    elseif record.spawn_position then job.anchor=record.spawn_position end
    local jobs=self._hcm_patrol_jobs or {}
    self._hcm_patrol_jobs=jobs;jobs[#jobs+1]=job
    return job
end
mod.queue_native_patrol=new_job
local function positions(self,job,context,t)
    local preferred=job.anchor and job.anchor:unbox()
    local position,reason=Placement.anchor(context,job,preferred)
    if not position then job.next_at=t+(reason=="pending" and 0.25 or RETRY);return end
    job.anchor=nil
    local output={}
    local count=GwNavQueries.flood_fill_from_position(self._nav_world,position,2,2,
        #job.breeds-job.index+1,output)
    if not count or count<1 then job.next_at=t+RETRY;return end
    job.positions={};job.position_index=1
    for i=1,count do job.positions[i]=Vector3Box(output[i]) end
end
local function setup_patrol(job,unit,context)
    local patrol=Blackboard.write_component(BLACKBOARDS[unit],"patrol")
    local index=job.index
    local follow=index>1 and job.units[Patrols.get_follow_index(index)]
    if not HEALTH_ALIVE[follow] then
        follow=nil
        for i=index-1,1,-1 do if HEALTH_ALIVE[job.units[i]] then follow=job.units[i];break end end
    end
    patrol.patrol_index=follow and index or 1;patrol.should_patrol=true
    if follow then patrol.patrol_leader_unit=follow
    else patrol.walk_position:store(context.reachable_target);patrol.auto_patrol=true end
    job.units[index]=unit
end
mod.update_patrol_spawns=function(self,t,side_id,target_side_id)
    local jobs=self._hcm_patrol_jobs
    if not jobs or #jobs==0 or self._disabled or not mod.has_local_gameplay_authority() then return end
    local job=jobs[1]
    if t<job.next_at or t<(self._hcm_next_patrol_member or 0) then return end
    job.next_at=t+INTERVAL;self._hcm_next_patrol_member=t+INTERVAL
    local pacing=Managers.state.pacing
    if not pacing:spawn_type_enabled("monsters") then return end
    local context=Placement.context(job.side_id,target_side_id,t)
    if not context then return end
    local manager=Managers.state.minion_spawn
    local capacity=math.floor(145*mod.template_runtime.config().coarse.combat_tolerance+0.5)
    if manager._spawn_queue_size>=16 or manager:total_allocated_num_enemies()>=capacity-4 then return end
    if not job.positions then positions(self,job,context,t) end
    if not job.positions then return end
    local position=job.positions[job.position_index]:unbox()
    local valid,_,_,mode=Placement.valid(context,position)
    if not valid then
        job.position_index=job.position_index+1
        if mode~="footprint" or job.position_index>#job.positions then job.positions=nil;job.next_at=t+RETRY end
        return
    end
    local system=Managers.state.extension:system("group_system")
    if not job.group_id then
        job.group_id=system:generate_group_id()
        system:lock_group_id(job.group_id)
        local group=system:group_from_id(job.group_id)
        group._hcm_recycling={kind="monsters"}
        if job.sound then group.group_start_sound_event=job.sound.start;group.group_stop_sound_event=job.sound.stop end
        if job.reserve then job.reserve.groups[#job.reserve.groups+1]=job.group_id end
    end
    local params=manager:request_param_table()
    params.optional_aggro_state=job.reserve and "aggroed" or "passive"
    params.optional_target_unit=job.reserve and context.target or nil
    params.optional_group_id=job.group_id;params.spawn_source="hcm_patrol"
    job.batch=job.batch or mod.new_spawn_batch(job.reserve and "reserve_patrol" or "route_patrol",job.side_id,target_side_id)
    params._hcm_batch=job.batch
    local unit=manager:spawn_minion(job.breeds[job.index],position,Quaternion.identity(),job.side_id,params)
    if not unit then job.next_at=t+RETRY;return end
    if job.reserve then job.units[job.index]=unit else setup_patrol(job,unit,context) end
    job.index=job.index+1;job.position_index=job.position_index+1
    if job.position_index>#job.positions then job.positions=nil end
    if job.index>#job.breeds then
        system:unlock_group_id(job.group_id)
        job.completed=true;job.finished_at=t;table.remove(jobs,1)
    end
end
mod.finish_patrol_spawns=function(self)
    local jobs=self._hcm_patrol_jobs
    if jobs then
        local system=Managers.state.extension and Managers.state.extension:system("group_system")
        for _,job in ipairs(jobs) do
            if system and job.group_id then system:unlock_group_id(job.group_id) end
        end
    end
    self._hcm_patrol_jobs=nil;self._hcm_next_patrol_member=nil
end
return true
