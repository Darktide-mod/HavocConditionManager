-- Extra encounters require a route from the spawn to the real player floor.
-- One shared asynchronous search and live path serve every member of a batch.
-- Native pathfinding decides traversal, including door and terrain links.
-- Native mission doors keep their own spawning; this only selects extra spawns.
local mod=get_mod("HavocConditionManager")
local SpawnPoints=require("scripts/managers/main_path/utilities/spawn_point_queries")
local MainPath=require("scripts/utilities/main_path_queries")
local NavQueries=require("scripts/utilities/nav_queries")
local HordeUtilities=require("scripts/managers/horde/utilities/horde_utilities")
local M={}
local MIN_DISTANCE,MIN_AHEAD,PREFERRED_AHEAD,MAX_AHEAD=35,30,60,120
local NEAR_DISTANCE,NEAR_MAX=20,60
local state

function M.context(side_id,target_side_id,t)
    local pacing=Managers.state.pacing
    local main=Managers.state.main_path
    if not pacing or pacing:get_in_safe_zone() or not main or not main:is_main_path_ready() then return end
    local target,distance,path_position=main:ahead_unit(target_side_id)
    local position=target and POSITION_LOOKUP[target]
    local side=Managers.state.extension:system("side_system"):get_side(side_id)
    local horde=Managers.state.horde
    if not position or not distance or not side or not horde or not horde._physics_world
        or not side.valid_enemy_player_units_positions or #side.valid_enemy_player_units_positions==0 then return end
    path_position=path_position or MainPath.position_from_distance(distance)
    if not path_position then return end
    return {main=main,target=target,distance=distance,position=position,path_position=path_position,side=side,side_id=side_id,
        nav=pacing._nav_world,physics=horde._physics_world,t=t or Managers.time:time("gameplay"),
        traverse=pacing.roamer_traverse_logic and pacing:roamer_traverse_logic()}
end

function M.within_limits(context,position,near)
    if near==nil then near=state and state.proof and state.proof.near end
    local minimum=near and NEAR_DISTANCE or MIN_DISTANCE
    local maximum=near and NEAR_MAX or MAX_AHEAD
    local nearest=math.huge
    for _,player_position in ipairs(context.side.valid_enemy_player_units_positions) do
        local d=Vector3.distance_squared(position,player_position)
        if d<minimum*minimum then return end
        nearest=math.min(nearest,d)
    end
    if nearest>maximum*maximum then return end
    local progress=context.main:travel_distance_from_position(position,true)
    local ahead=progress and progress-context.distance
    if not near and (not ahead or ahead<MIN_AHEAD or ahead>MAX_AHEAD) then return end
    return ahead or 0,math.sqrt(nearest)
end

local function hidden(context,position,near)
    local ahead,distance=M.within_limits(context,position,near)
    if not ahead then return end
    if HordeUtilities.position_has_line_of_sight_to_any_enemy_player(context.physics,position+Vector3.up(),
        context.side,"filter_ray_aim_assist_line_of_sight") then return end
    return true,ahead,distance
end

local function player_floor(context)
    -- Tight projection avoids accepting the main path on a different storey.
    return NavQueries.position_on_mesh_with_outside_position(context.nav,context.traverse,context.position,1,1,1)
end

local function route_current(context,s)
    local proof=s and s.proof
    if not proof or s.nav~=context.nav or proof.side_id~=context.side_id
        or Vector3.distance_squared(context.position,proof.player:unbox())>12*12
        or not GwNavAStar.is_valid(s.live,s.astar) then return end
    local goal=proof.goal:unbox()
    if Vector3.distance_squared(context.position,proof.player:unbox())>0.01 then
        local current_goal=player_floor(context)
        if not current_goal or not GwNavQueries.raycango(context.nav,goal,current_goal,context.traverse) then return end
        goal=current_goal
    end
    context.reachable_target=goal
    return proof
end

function M.valid(context,position)
    local proof=route_current(context,state)
    if not proof then return nil,nil,nil,"stale_route" end
    local anchor=proof.position:unbox()
    -- A flood-fill result can lie across a ledge or on another island. Each
    -- actual member must walk back to the already verified anchor.
    local offset=Vector3.distance_squared(position,anchor)
    if offset>12*12 or offset>0.01 and
        not GwNavQueries.raycango(context.nav,position,anchor,context.traverse) then return nil,nil,nil,"footprint" end
    local ok,ahead,distance=hidden(context,position,proof.near)
    if ok then return true,ahead,distance,proof.near and "nearby" or "ahead" end
    return nil,nil,nil,"position"
end

function M.finish()
    local s=state
    if not s then return end
    -- Match native navigation ownership: destroy the live path before AStar.
    if s.live then GwNavAStar.destroy_live_path(s.live) end
    if s.astar then GwNavAStar.destroy(s.astar) end
    state=nil
end

local function current(context)
    if state and state.nav~=context.nav then M.finish() end
    if not state then
        state={nav=context.nav,next_start=0,next_poll=0,next_scan=0,failed={},local_phase=0,local_next_scan=0}
    end
    return state
end

local function reject(s,context)
    local request=s.request
    if #s.failed>=8 then table.remove(s.failed,1) end
    s.failed[#s.failed+1]={position=request.position,expires=context.t+20}
end

local function poll(context,s)
    if not s.running or context.t<s.next_poll then return end
    s.next_poll=context.t+0.25
    if not GwNavAStar.processing_finished(s.astar) then return end
    s.running=nil
    local request=s.request
    if not GwNavAStar.path_found(s.astar) then reject(s,context);return end
    local count=GwNavAStar.node_count(s.astar)
    if not count or count<2 or Vector3.distance_squared(GwNavAStar.node_at_index(s.astar,count),request.goal:unbox())>1 then
        reject(s,context);return
    end
    GwNavAStar.init_live_path(s.live,s.astar)
    s.proof=request
    if not route_current(context,s) then s.proof=nil;return end
    s.candidates=nil
end

local function candidates(context,s,preferred)
    local points=context.main:nav_spawn_points()
    local groups=points and GwNavSpawnPoints.get_count(points)
    if not groups or groups<1 then return end
    local goal=player_floor(context)
    if not goal then return end
    local disallowed={}
    for i=#s.failed,1,-1 do
        if s.failed[i].expires<context.t then table.remove(s.failed,i)
        else disallowed[#disallowed+1]=s.failed[i].position end
    end
    local output={}
    local function add(position,near)
        for _,bad in ipairs(disallowed) do if Vector3.distance_squared(position,bad:unbox())<8*8 then return end end
        for _,item in ipairs(output) do if Vector3.distance_squared(position,item.position:unbox())<4*4 then return end end
        if not hidden(context,position,near) then return end
        output[#output+1]={position=Vector3Box(position),goal=Vector3Box(goal),player=Vector3Box(context.position),
            near=near,side_id=context.side_id}
        return true
    end
    if preferred then add(preferred,false) end
    local wanted=MainPath.position_from_distance(context.distance+PREFERRED_AHEAD)
    local function collect(origin,near,limit)
        if not origin then return end
        local found,count=SpawnPoints.get_occluded_positions(context.nav,points,origin,
            context.side.valid_enemy_player_units_positions,4,groups,near and NEAR_DISTANCE or MIN_DISTANCE,
            near and NEAR_MAX or MAX_AHEAD,near and 4 or nil,not near,disallowed)
        local choices={}
        for i=1,math.min(count or 0,32) do
            local position=found[i]
            local ahead,distance=M.within_limits(context,position,near)
            if ahead then
                local score=near and math.abs(distance-28)+math.abs(position.z-goal.z)*2 or math.abs(ahead-PREFERRED_AHEAD)
                local index=1
                while choices[index] and choices[index].score<=score do index=index+1 end
                if index<=8 then table.insert(choices,index,{position=position,score=score});choices[9]=nil end
            end
        end
        for _,choice in ipairs(choices) do if #output>=limit then break end;add(choice.position,near) end
    end
    collect(wanted,false,2)
    collect(goal,true,#output+2)
    -- Authored occlusion groups can all be on a different storey or behind
    -- the same unusable transition. Sample a small ring on the player's real
    -- floor as another source of candidates; every result still needs AStar.
    if context.t>=s.local_next_scan then
        s.local_next_scan=context.t+4
        local phase=s.local_phase;s.local_phase=phase+1
        local radius=phase%2==0 and 28 or 40
        local offsets={0,4,2,6,1,5,3,7}
        local added=0
        for _,offset in ipairs(offsets) do
            local angle=(offset+phase%2*0.5)*math.pi/4
            local wanted_local=goal+Vector3(math.cos(angle)*radius,math.sin(angle)*radius,0)
            local position=NavQueries.position_on_mesh_with_outside_position(context.nav,context.traverse,wanted_local,1,1,1)
            if position and add(position,true) then added=added+1;if added>=4 then break end end
        end
    end
    s.candidates=output;s.index=1;s.next_scan=context.t+8
end

function M.anchor(context,owner,preferred)
    -- Engine APIs are required; absence never counts as a successful path.
    if not context.nav or not context.traverse or not GwNavAStar or not GwNavQueries.raycango then return nil,"navigation_unavailable" end
    local s=current(context)
    if context.prefer_near then s.near_until=context.t+4 end
    poll(context,s)
    if s.proof then
        local position=s.proof.position:unbox()
        if M.valid(context,position) then return position end
        s.proof=nil;s.candidates=nil;s.next_scan=0
    end
    if s.running then return nil,"pending" end
    if s.candidates and s.index>#s.candidates then s.candidates=nil end
    if not s.candidates then
        if context.t<s.next_scan then return nil,"no_position" end
        candidates(context,s,preferred)
    end
    if s.candidates and s.near_until and context.t<=s.near_until then
        for index=s.index,#s.candidates do
            if s.candidates[index].near then
                s.candidates[s.index],s.candidates[index]=s.candidates[index],s.candidates[s.index];break
            end
        end
    end
    local request=s.candidates and s.candidates[s.index]
    if not request then return nil,"no_position" end
    if context.t<s.next_start then return nil,"pending" end
    if Vector3.distance_squared(context.position,request.player:unbox())>12*12 then
        s.candidates=nil;s.next_scan=0;return nil,"pending"
    end
    if not hidden(context,request.position:unbox(),request.near) then s.index=s.index+1;return nil,"pending" end
    if not s.astar then s.astar=GwNavAStar.create(context.nav);s.live=GwNavAStar.create_live_path() end
    s.request=request;s.index=s.index+1;s.running=true;s.next_start=context.t+1;s.next_poll=context.t+0.25
    GwNavAStar.start_with_propagation_box(s.astar,context.nav,request.position:unbox(),request.goal:unbox(),40,context.traverse)
    -- Consume finished work immediately; unfinished work is polled on later
    -- scheduled spawn attempts, never waited on in the game thread.
    s.next_poll=context.t;poll(context,s)
    if s.proof and M.valid(context,s.proof.position:unbox()) then return s.proof.position:unbox() end
    return nil,"pending"
end

mod.spawn_placement=M
return M

