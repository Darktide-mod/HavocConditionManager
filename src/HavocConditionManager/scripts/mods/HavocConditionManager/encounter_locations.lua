-- Extend the native encounter lists using unused, authored spawn positions.
-- Native update, unit creation, patrol groups, objectives and cleanup own them.
local mod=get_mod("HavocConditionManager")
local E=mod.template_runtime
local Monster=require("scripts/managers/pacing/monster_pacing/monster_pacing")
local Settings=require("scripts/settings/monster/monster_settings")
local Reserve=mod:io_dofile("HavocConditionManager/scripts/mods/HavocConditionManager/encounter_reserve")
local planning
local function copy(t) local r={};for k,v in pairs(t) do r[k]=v end;return r end
local function roll(value)
    if type(value)=="table" then return math.random(value[1],value[2]) end
    return value or 0
end
-- Native section warnings describe the first placement pass. Delay only those
-- for the source being extended; final counts include the retained reserve.
mod.defer_native_encounter_warning=function(fn,tag,message,...)
    local _,source=...
    if planning and planning.monsters and tag=="MonsterPacing" and source=="monsters"
        and message=="Requested %s spawns for type %s but only had %s sections. Clamped." then
        planning.warnings[#planning.warnings+1]={fn=fn,tag=tag,message=message,args={...}}
        return true
    end
end

mod:hook(Monster,"_generate_spawns",function(fn,self,template)
    if not mod.has_local_gameplay_authority() then return fn(self,template) end
    local cfg=E.config().coarse
    local extend_monsters=cfg.monster_encounters>1 and template.num_spawns and template.num_spawns.monsters~=nil
    local extend_patrols=cfg.patrols>1 and template.boss_patrols and template.boss_patrols.num_boss_patrols_range
    if not extend_monsters and not extend_patrols then return fn(self,template) end
    -- Keep baseline-sized allocations for the shared native section pass so
    -- multiplying monsters cannot consume every section before patrols run.
    -- The final quotas are rolled once from the already-compiled template.
    local initial=copy(template)
    local wanted_monsters,wanted_patrols
    local monster_override,patrol_override=self._num_monsters_override,self._num_boss_patrol_override
    if extend_monsters then
        wanted_monsters=monster_override or roll(template.num_spawns.monsters)
        local initial_count=math.min(wanted_monsters,math.floor(wanted_monsters/cfg.monster_encounters+0.5))
        initial.num_spawns=copy(template.num_spawns);initial.num_spawns.monsters=initial_count
        if monster_override~=nil then self._num_monsters_override=initial_count end
        local mode=Managers.state.game_mode:game_mode()
        local havoc=mode and mode:extension("havoc")
        wanted_monsters=wanted_monsters+(havoc and havoc:get_modifier_value("add_num_monsters") or 0)
    end
    if extend_patrols then
        wanted_patrols=patrol_override or roll(template.boss_patrols.num_boss_patrols_range)
        local initial_count=math.min(wanted_patrols,math.floor(wanted_patrols/cfg.patrols+0.5))
        initial.boss_patrols=copy(template.boss_patrols)
        initial.boss_patrols.num_boss_patrols_range={initial_count,initial_count}
        -- The native override skips its section clamp altogether.
        self._num_boss_patrol_override=nil
    end
    local previous=planning
    local context={monsters=extend_monsters,warnings={}}
    planning=context
    local ok,result=pcall(fn,self,initial)
    planning=previous
    self._num_monsters_override,self._num_boss_patrol_override=monster_override,patrol_override
    if not ok or not result then
        for _,warning in ipairs(context.warnings) do warning.fn(warning.tag,warning.message,unpack(warning.args)) end
        if not ok then error(result,0) end
        return result
    end

    local monsters,patrols=self._monsters,self._boss_patrols
    local count_monsters,count_patrols=0,patrols and #patrols or 0
    local occupied,used_positions={},{}
    for _,monster in ipairs(monsters) do
        if monster.spawn_type=="monsters" then count_monsters=count_monsters+1 end
        occupied[#occupied+1]=monster.travel_distance
        used_positions[monster.travel_distance]=true
    end
    for _,patrol in ipairs(patrols or {}) do
        occupied[#occupied+1]=patrol.travel_distance
        used_positions[patrol.travel_distance+Settings.boss_patrol_extra_spawn_distance]=true
    end
    -- Preserve injected/objective records even if they exceed a zero quota.
    wanted_monsters=math.max(wanted_monsters or count_monsters,count_monsters)
    wanted_patrols=math.max(wanted_patrols or count_patrols,count_patrols)
    local candidates,seen={},{}
    for section,points in ipairs(self._spawn_type_point_sections.monsters or {}) do
        for _,point in ipairs(points) do
            local distance=point.spawn_travel_distance
            if distance>0 and not seen[distance] and not used_positions[distance] then
                seen[distance]=true;candidates[#candidates+1]={point=point,section=section,distance=distance}
            end
        end
    end
    table.sort(candidates,function(a,b) return a.distance<b.distance end)
    local min_gap=math.max(10,Settings.spawn_distance/math.max(cfg.monster_encounters,cfg.patrols))
    local function take_position(is_monster)
        local chosen,best
        local center=#candidates>0 and (candidates[1].distance+candidates[#candidates].distance)/2 or 0
        for i,candidate in ipairs(candidates) do
            local trigger=candidate.distance-(is_monster and 0 or Settings.boss_patrol_extra_spawn_distance)
            local gap=math.huge
            for _,distance in ipairs(occupied) do gap=math.min(gap,math.abs(trigger-distance)) end
            local score=#occupied>0 and gap or -math.abs(candidate.distance-center)
            if trigger>0 and gap>=min_gap and (not best or score>best) then chosen,best=i,score end
        end
        if not chosen then return end
        local candidate=table.remove(candidates,chosen)
        occupied[#occupied+1]=candidate.distance-(is_monster and 0 or Settings.boss_patrol_extra_spawn_distance)
        return candidate
    end
    local breeds=template.breed_names and template.breed_names.monsters
    local can_add_monsters=breeds and #breeds>0
    local can_add_patrols=template.boss_patrols and template.boss_patrols.breed_lists
    while can_add_monsters and count_monsters<wanted_monsters or can_add_patrols and count_patrols<wanted_patrols do
        local monster_pending=can_add_monsters and count_monsters<wanted_monsters
        local patrol_pending=can_add_patrols and count_patrols<wanted_patrols
        -- Balance both quotas when authored positions are scarce.
        local choose_monster=monster_pending and (not patrol_pending or count_monsters/wanted_monsters<=count_patrols/wanted_patrols)
        local candidate=take_position(choose_monster)
        if not candidate and monster_pending and patrol_pending then
            choose_monster=not choose_monster;candidate=take_position(choose_monster)
        end
        if not candidate then break end
        local point=candidate.point
        if choose_monster then
            local breed=breeds[math.random(#breeds)]
            monsters[#monsters+1]={travel_distance=point.spawn_travel_distance,breed_name=breed,position=point.position,
                section=candidate.section,spawn_type="monsters",stinger=template.spawn_stingers and template.spawn_stingers[breed],
                despawn_distance_when_passive=template.despawn_distance_when_passive and template.despawn_distance_when_passive[breed]}
            count_monsters=count_monsters+1
        else
            if not patrols then patrols={};self._boss_patrols=patrols end
            local settings=template.boss_patrols
            patrols[#patrols+1]={travel_distance=point.spawn_travel_distance-Settings.boss_patrol_extra_spawn_distance,
                breed_list=settings.breed_lists,section=candidate.section,spawn_point_travel_distance=point.spawn_point_travel_distance,
                sound_events=settings.sound_events}
            count_patrols=count_patrols+1
        end
    end
    local function by_distance(a,b) return a.travel_distance<b.travel_distance end
    table.sort(monsters,by_distance)
    if patrols then table.sort(patrols,by_distance) end
    local reserve_monsters=can_add_monsters and wanted_monsters-count_monsters or 0
    local reserve_patrols=can_add_patrols and wanted_patrols-count_patrols or 0
    Reserve.plan(self,reserve_monsters,reserve_patrols)
    return result
end)
return true
