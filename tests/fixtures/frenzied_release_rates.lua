-- Use the unmodified release files, including their actual passive stats.
messages={};engine=start(rate_test_files or shipped_package_files)
local current=mod._diy_frenzied_assault_hooks_v1.current
assert(current.profile==nil and native_dt.traced)
local u,breed=unit();local ai=brain(u,breed);ai:update(u,.1,0)
close(observed.attack,.6/1.4);close(observed.duration,1.2/1.4)
close(u.ext.navigation_system._max_speed_with_modifiers,5*1.2)
close(current:animation_rate(ai),1.4)
u.other_melee_speed=.3
ai._running_leaf_node=nil;ai._running_child_nodes={};ai._old_running_child_nodes={}
current.moves[u].node=nil;current.moves[u].attack_rate=nil
ai:update(u,.1,1)
close(observed.attack,.6/1.7);close(observed.duration,1.2/1.7)
close(current:animation_rate(ai),1.7)
u.other_melee_speed=nil
local gun,gb=unit();local attack=modules['scripts/utilities/minion_attack']
for _,name in ipairs({'BtShootAction','BtShootPositionAction','BtRunStopAndShootAction','BtStepShootAction','BtStrafeShootAction','BtInCoverAction','BtSniperShootAction'})do
    close(current:attack_rate(gun,name),1.4)
end
for _,name in ipairs({'BtShootAction','BtRunStopAndShootAction','BtStepShootAction','BtStrafeShootAction'})do
    local data=current.action_copy({aim_duration=1.2,shoot_timing={step=.6},shoot_template={},time_per_shot={{.24,.24}},
        shoot_cooldown={{3.6,3.6}},before_shoot_effect_template_timing=.12},false,'attack',name,1.4)
    local pad={perception_component={target_unit=target},perception_extension={alert_nearby_allies=function()end},scope_reflection_timing=true}
    attack.start_shooting(gun,pad,0,data,data.shoot_timing.step,true)
    close(pad.next_shoot_timing,.6/1.4);close(pad.before_shoot_effect_template_timing,(.6-.12)/1.4)
    pad.num_shots=3;pad.fx_system={start_template_effect=function()return 1 end,stop_template_effect=function()end}
    local shoot=attack.shoot;attack.shoot=function()end
    attack.update_shooting(gun,pad,.6/1.4,data);attack.shoot=shoot
    close(pad.next_shoot_timing,(.6+.24)/1.4)
    close(data.shoot_cooldown[1][1],3.6/1.4)
end
for _,name in ipairs({'BtGrenadierThrowAction','BtQuickGrenadeThrowAction','BtShootNetAction','BtShootLiquidBeamAction','BtChaosHoundLeapAction','BtChaosHoundTargetPouncedAction','BtMutantChargerChargeAction'})do
    close(current:attack_rate(gun,name),1.4)
end
for _,name in ipairs({'BtMeleeFollowTargetAction','BtGrenadierFollowAction','BtChaosHoundApproachAction','BtChaosHoundRoamAction','BtChaosHoundSkulkAction'})do
    ai._running_leaf_node={tree_node={name}};ai._scratchpad={behavior_component={move_state='moving'}}
    close(current:animation_rate(ai),1.2)
    ai._scratchpad.behavior_component.move_state='idle';close(current:animation_rate(ai),1)
end
ai._running_leaf_node={tree_node={'BtMutantChargerChargeAction'}};ai._scratchpad={state='charging'}
u.ext.locomotion_system:set_wanted_velocity(Vector3(2,5,-3))
close(u.ext.locomotion_system._engine_extension_id.velocity[1],2*1.2)
close(u.ext.locomotion_system._engine_extension_id.velocity[2],5*1.2)
close(u.ext.locomotion_system._engine_extension_id.velocity[3],-3)
close(current:animation_rate(ai),1.2)
ai._scratchpad.state='smashing';current.moves[u].attack_rate=1.4;close(current:animation_rate(ai),1.4)
local trajectory=require('scripts/utilities/trajectory');local sweep=trajectory.sphere_sweep_collision_check
local from,to
trajectory.sphere_sweep_collision_check=function(_,_,_,x,y,_,_,_,a,b)
    from,to=a,b;close(x,10);close(y,4);return nil,nil,Vector3(0,10*b,4*b)
end
local leap={locomotion_extension=u.ext.locomotion_system,state='leaping',leap_start_position=Vector3Box(Vector3.zero()),leap_velocity=Vector3Box(Vector3(0,10,4))}
BtChaosHoundLeapAction:_check_leap_for_collisions(leap,{}, {},.2,.3,leap.leap_start_position:unbox(),leap.leap_velocity:unbox())
close(from,.2*1.4);close(to,.3*1.4);trajectory.sphere_sweep_collision_check=sweep

-- Exercise the real bomber approach/lunge and death deadline at 1.4x.
local systems=Managers.state.extension.system
Managers.state.extension.system=function(self,name)
    if name=='side_system' then return {side_by_unit=setmetatable({},{__index=function()return {relation_sides=function()return {}end}end})}end
    if name=='group_system' then return {bot_groups_from_sides=function()return {}end}end
    return systems(self,name)
end
local bomber,bb=unit('minion',true);bb.name='chaos_poxwalker_bomber';bb.run_speed=5
bomber.anim={times={0},states={1},ids={1},layers=1};bomber.wanted_root_position={.14,0,0}
local nav=bomber.ext.navigation_system
nav.nav_world=function()return {}end;nav.traverse_logic=function()return {}end
nav.destination=function()return POSITION_LOOKUP[target]end
nav.set_enabled=function(self,enabled,speed)self.enabled=enabled;if speed then self:set_max_speed(speed)end end
local ba=brain(bomber,bb);ba._blackboard.stagger={num_triggered_staggers=0,duration=2};ba._blackboard.death={is_dead=false,fuse_timer=0,damage_profile_name=''}
local bn=setmetatable({identifier='bomber',tree_node={'BtPoxwalkerBomberApproachAction',action_data=bomber_actions.approach}},BtPoxwalkerBomberApproachAction)
function bn:children()return {}end
function bn:enter(unit,breed,blackboard,pad,data,t)
    BtPoxwalkerBomberApproachAction.enter(self,unit,breed,blackboard,pad,data,t)
    self:_start_lunge(unit,blackboard,pad,data,target,t)
end
ba._behavior_tree={root=function()return bn end}
local attacks=modules['scripts/utilities/attack/attack'];local execute=attacks.execute;local kills=0
attacks.execute=function(victim)assert(victim==bomber);kills=kills+1 end
ba:update(bomber,.1,100)
local duration=bomber_actions.approach.lunge_duration/1.4
close(ba._scratchpad.lunge_duration,100+duration)
close(ba._scratchpad.move_during_lunge_duration,100+bomber_actions.approach.move_during_lunge_duration/1.4)
close(ba._blackboard.death.fuse_timer,101.5);close(current:animation_rate(ba),1.4)
assert(nav._num_movement_modifiers==0)
ba:update(bomber,.1,100+duration-.001);assert(kills==0)
close(nav._max_speed_with_modifiers,1.4)
ba:update(bomber,.1,100+duration+.001);assert(kills==1)
attacks.execute=execute;Managers.state.extension.system=systems

local victim=unit('player');local first_person=unit('player')
victim.ext.unit_data_system.components.disabled_character_state={disabling_unit=u}
victim.ext.first_person_system={first_person_unit=function()return first_person end}
ai._scratchpad={state='smashing',grabbed_target=victim}
animation_units={u,victim,first_person,bomber}
for _,who in ipairs(animation_units)do who.anim={times={0},states={1},ids={1},layers=1}end
local world=modules['scripts/foundation/utilities/script_world']
world.update(level_world,.1)
for _,who in ipairs(animation_units)do close(who.anim.times[1],.14)end
victim.ext.unit_data_system.components.disabled_character_state.disabling_unit=nil
world.update(level_world,.1);close(victim.anim.times[1],.24);close(first_person.anim.times[1],.24)
assert(#messages==0 and current.profile==nil and current.animation_snapshots==nil)
engine.finish();assert(not native_dt.enabled);animation_units={}
