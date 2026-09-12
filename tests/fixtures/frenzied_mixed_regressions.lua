local old={};for k,v in pairs(package_files)do old[k]=v end
old['lua/main.lua'],old['lua/animation.lua']=last_main,last_animation
old['package.json']=old['package.json']:gsub('"package_version": "1.7.4"','"package_version": "1.7.2"')
local systems=Managers.state.extension.system
local threat_duration
Managers.state.extension.system=function(self,name)
    if name=='side_system' then return {side_by_unit=setmetatable({},{__index=function()return {relation_sides=function()return {}end}end})}end
    if name=='group_system' then return {bot_groups_from_sides=function()return {{aoe_threat_created=function(_,_,_,_,_,duration)threat_duration=duration end}}end}end
    return systems(self,name)
end
local damage=modules['scripts/settings/damage/damage_profile_templates']
damage.poxwalker_bomber_instakill={test='instakill'}
local attacks=modules['scripts/utilities/attack/attack'];local saved_attack=attacks.execute
local clock=100;Managers.time={time=function()return clock end}
local function setup_bomber()
    local u,breed=unit('minion',true);breed.name='chaos_poxwalker_bomber';breed.run_speed=5
    u.anim={times={0},states={1},ids={1},layers=1};u.wanted_root_position={.2,0,0}
    local nav=u.ext.navigation_system
    nav.nav_world=function()return {}end;nav.traverse_logic=function()return {}end
    nav.destination=function()return POSITION_LOOKUP[target]end
    nav.set_enabled=function(self,enabled,speed)self.enabled=enabled;if speed then self:set_max_speed(speed)end end
    local ai=brain(u,breed)
    ai._blackboard.stagger={num_triggered_staggers=0,duration=2}
    ai._blackboard.death={is_dead=false,fuse_timer=0,damage_profile_name=''}
    local node=setmetatable({identifier='bomber',tree_node={'BtPoxwalkerBomberApproachAction',action_data=bomber_actions.approach}},BtPoxwalkerBomberApproachAction)
    function node:children()return {}end
    function node:enter(u,b,bb,pad,data,t)
        BtPoxwalkerBomberApproachAction.enter(self,u,b,bb,pad,data,t)
        self:_start_lunge(u,bb,pad,data,target,t)
    end
    ai._behavior_tree={root=function()return node end}
    local killed=0
    attacks.execute=function(victim,profile,...)
        if profile==damage.poxwalker_bomber_instakill then assert(victim==u);killed=killed+1;ai._blackboard.death.is_dead=true end
    end
    return u,breed,ai,node,function()return killed end
end
for _,legacy in ipairs({true,false})do
    engine=start(legacy and old or nil)
    local current=mod._diy_frenzied_assault_hooks_v1.current
    local u,breed,ai,node,kills=setup_bomber();local nav=u.ext.navigation_system
    nav:add_movement_modifier(1.3) -- Independent gas/mod multiplier must survive.
    clock=100;ai:update(u,.1,clock)
    local pad=ai._scratchpad;local duration=bomber_actions.approach.lunge_duration/(legacy and 1 or 2)
    close(pad.lunge_duration,100+duration)
    close(pad.move_during_lunge_duration,100+bomber_actions.approach.move_during_lunge_duration/(legacy and 1 or 2))
    close(threat_duration,duration);close(ai._blackboard.death.fuse_timer,101.5)
    close(current:animation_rate(ai),2)
    clock=100.6;ai:update(u,.1,clock)
    close(nav._max_speed_with_modifiers,2*1.3*(legacy and 2 or 1))
    assert(nav._num_movement_modifiers==(legacy and 2 or 1))
    animation_units={u};modules['scripts/foundation/utilities/script_world'].update(level_world,.6)
    close(u.anim.times[1],1.2);assert(kills()==0)
    clock=100+duration-.0001;ai:update(u,.1,clock);assert(kills()==0)
    clock=100+duration+.0001;ai:update(u,.1,clock);assert(kills()==1 and bomber_is_dead(u,ai._blackboard))
    assert(node.tree_node.action_data==bomber_actions.approach,'Shared source data is always restored')
    engine.finish();assert(nav._num_movement_modifiers==1,'Only the other modifier remains after cleanup')
end
engine=start();local current=mod._diy_frenzied_assault_hooks_v1.current
-- Native push and received-stagger branches retain their defensive windows.
for _,lunging in ipairs({false,true})do
    local u,breed,ai,node,kills=setup_bomber()
    clock=200;ai:update(u,.1,clock)
    local pad=ai._scratchpad;local bb=ai._blackboard
    bb.stagger.staggered_by_melee_push=not lunging
    bb.stagger.num_triggered_staggers=lunging and 1 or 0
    if not lunging then pad.lunge_duration=nil;pad.state='running';bb.death.fuse_timer=0 end
    local data=current.action_copy(bomber_actions.approach,false,'move','BtPoxwalkerBomberApproachAction',2)
    node:leave(u,breed,bb,pad,data,201,'aborted',false)
    close(bb.stagger.duration,2*.175);assert(bb.death.staggered_during_lunge)
    close(bb.death.fuse_timer,lunging and 201.5 or 202.5)
    clock=bb.death.fuse_timer-.001;assert(not bomber_is_dead(u,bb))
    clock=bb.death.fuse_timer;assert(bomber_is_dead(u,bb))
    ai._running_leaf_node={tree_node={'BtStaggerAction'}};ai._scratchpad={}
    current:sync_root_motion(current.moves[u]);close(current:animation_rate(ai),1)
    assert(u.ext.navigation_system._num_movement_modifiers==1)
end
attacks.execute=saved_attack;animation_units={}
local function via_brain(name,data,run)
    local u,breed=unit();local ai=brain(u,breed)
    local node={identifier=name,tree_node={name,action_data=data},children=function()return {}end,leave=function()end}
    function node:enter(u,b,bb,pad,modified,t)
        pad.animation_extension=u.ext.animation_system;pad.locomotion_extension=u.ext.locomotion_system
        pad.navigation_extension=u.ext.navigation_system;pad.behavior_component={move_state='moving'}
        pad.perception_component={target_unit=target};pad.aim_component={}
        run(u,ai,pad,modified,t)
    end
    function node:run()return 'running',false end
    ai._behavior_tree={root=function()return node end}
    ai:update(u,.1,300);assert(node.tree_node.action_data==data)
    return u,ai
end
local cover_data={peek_duration=.8,peek_anim_events={left='peek'},aim_duration={.8,1.2},aim_anim_event='aim',
    start_aiming_at_target_timings={aim=.4},enter_cover_durations={enter=2},suppressed_duration={2,4},
    shoot_template={first_shoot_timing=.6},time_per_shot=.2}
local u,ai=via_brain('BtInCoverAction',cover_data,function(u,ai,pad,data,t)
    assert(data~=cover_data and data.enter_cover_durations==cover_data.enter_cover_durations and data.suppressed_duration==cover_data.suppressed_duration)
    BtInCoverAction._start_peeking({},u,pad,data,{},'left',t);close(pad.peek_duration,t+.4)
    BtInCoverAction._start_aiming({},u,pad,data,t);close(pad.aim_duration,t+.5);close(pad.start_aiming_at_target_timing,t+.2)
    assert(data.time_per_shot==.2 and data.shoot_template.first_shoot_timing==.6,'Native shooting applies the rate itself')
end)
close(current:animation_rate(ai),2)
for _,state in ipairs({'entering','suppressed'})do ai._scratchpad.state=state;close(current:animation_rate(ai),1)end
ai._scratchpad.state='shooting';current.moves[u].attack_rate=2.3;close(current:animation_rate(ai),2.3)
local dash_data={dash_anim_events='dash',dash_durations={dash=1.2},dash_direction_durations={left=1.4},
    start_move_rotation_timings={left=.4},start_rotation_durations={left=.8},
    reached_destination_anim_events='end_dash',reached_destination_durations={end_dash=.8},max_duration=20,dash_speed=5}
local dash,dash_ai=via_brain('BtDashAction',dash_data,function(u,ai,pad,data,t)
    BtDashAction._start_dash_anim({},u,pad,data,t);close(pad.dash_duration,t+.6)
    close(data.dash_direction_durations.left,.7);close(data.start_move_rotation_timings.left,.2);close(data.start_rotation_durations.left,.4)
    assert(data.max_duration==20 and data.dash_speed==5)
    BtDashAction._start_reached_destination({},u,pad,data,t);close(pad.reached_destination_duration,t+.4)
end)
close(current:animation_rate(dash_ai),2);assert(dash.ext.navigation_system._num_movement_modifiers==0)
dash_ai._scratchpad.state='dashing';current:sync_root_motion(current.moves[dash]);assert(dash.ext.navigation_system._num_movement_modifiers==1)
dash_ai._scratchpad.is_anim_driven=true;close(current:animation_rate(dash_ai),2)
local flamer_data={aim_duration={aim={{1,1.4}}},attack_duration=2,end_duration=1,end_durations={finish=1.2},
    place_liquid_timing_speed=8,durations={walk=3},liquid_area_template={duration=10}}
local flamer,flamer_ai=via_brain('BtRenegadeFlamerPatrolAction',flamer_data,function(u,ai,pad,data,t)
    local action=setmetatable({_set_game_object_field=function()end},BtRenegadeFlamerPatrolAction)
    action:_start_aiming(u,t,pad,data);close(pad.aim_duration,.6)
    close(data.attack_duration,1);close(data.end_duration,.5);close(data.end_durations.finish,.6);close(data.place_liquid_timing_speed,16)
    assert(data.durations==flamer_data.durations and data.liquid_area_template==flamer_data.liquid_area_template)
end)
close(current:animation_rate(flamer_ai),2)
flamer_ai._scratchpad.behavior_component.move_state='idle';close(current:animation_rate(flamer_ai),2)
-- The actual native running-stagger scratchpad field is stagger_duration.
ai._running_leaf_node={tree_node={'BtMeleeFollowTargetAction'}};ai._scratchpad={stagger_duration=400}
close(current:animation_rate(ai),1)
engine.finish();Managers.state.extension.system=systems
