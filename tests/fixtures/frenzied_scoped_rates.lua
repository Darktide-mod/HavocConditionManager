-- Current release, real package loader/DMF/native AI and attack methods.
messages={};engine=start(shipped_package_files)
local current=mod._diy_frenzied_assault_hooks_v1.current
assert(mod._diy_frenzied_assault_hooks_v1.revision=='1.8.0' and current.profile==nil)
local u,breed=unit();local ai=brain(u,breed);ai:update(u,.1,0)
close(observed.attack,.6/1.2);close(observed.duration,1.2/1.2)
assert(u.ext.navigation_system._num_movement_modifiers==0)
assert(engine.effects(u).stats.ranged_attack_speed==nil)
close(current:animation_rate(ai),1.2)
local stacked,sb=unit();stacked.other_melee_speed=.3
local stacked_ai=brain(stacked,sb);stacked_ai:update(stacked,.1,0)
close(observed.attack,.6/1.5);close(observed.duration,1.2/1.5)
close(current:animation_rate(stacked_ai),1.5)
stacked.other_melee_speed=.6;stacked_ai:update(stacked,.1,.1)
close(current:animation_rate(stacked_ai),1.5)

-- Plain, elite and monster locomotion never acquires an owned modifier.
for _,name in ipairs({'chaos_poxwalker','chaos_armored_infected','renegade_gunner','cultist_gunner','chaos_ogryn_gunner','chaos_spawn','chaos_beast_of_nurgle'})do
    local enemy,breed=unit();breed.name=name
    local brain=brain(enemy,breed);brain._running_leaf_node={tree_node={'BtMeleeFollowTargetAction'}}
    brain._scratchpad={behavior_component={move_state='moving'}}
    current:movement(enemy,breed,brain)
    assert(enemy.ext.navigation_system._num_movement_modifiers==0)
    close(current:animation_rate(brain),1)
    brain._running_leaf_node={tree_node={'BtChargeAction'}};brain._scratchpad={state='charging'}
    enemy.ext.locomotion_system:set_wanted_velocity(Vector3(2,5,-3))
    close(enemy.ext.locomotion_system._engine_extension_id.velocity[2],5)
    close(current:animation_rate(brain),1)
end
-- The catalog comes from every native breed that declares tags.special=true.
for _,name in ipairs(native_special_names)do
    local enemy,breed=unit('minion',true);breed.name=name
    local brain=brain(enemy,breed);brain._running_leaf_node={tree_node={'BtMoveToPositionAction'}}
    brain._scratchpad={behavior_component={move_state='moving'}}
    current:movement(enemy,breed,brain)
    close(enemy.ext.navigation_system._max_speed_with_modifiers,6)
    close(current:animation_rate(brain),1.2)
    current:movement(enemy,breed,brain);assert(enemy.ext.navigation_system._num_movement_modifiers==1)
    brain._scratchpad.behavior_component.move_state='idle';close(current:animation_rate(brain),1)
    brain._scratchpad.behavior_component.move_state='moving';brain._scratchpad.stagger_duration=4
    close(current:animation_rate(brain),1)
end
local mutant,mb=unit('minion',true);mb.name='cultist_mutant'
local ma=brain(mutant,mb);ma._running_leaf_node={tree_node={'BtMutantChargerChargeAction'}};ma._scratchpad={state='charging'}
current:movement(mutant,mb,ma)
mutant.ext.locomotion_system:set_wanted_velocity(Vector3(2,5,-3))
close(mutant.ext.locomotion_system._engine_extension_id.velocity[2],6)
close(mutant.ext.locomotion_system._engine_extension_id.velocity[3],-3)
close(current:animation_rate(ma),1.2)

-- No firearm/sniper/flame action copies, swaps or native animation bindings.
local attack=modules['scripts/utilities/minion_attack']
for _,name in ipairs({'BtShootAction','BtShootPositionAction','BtRunStopAndShootAction','BtStepShootAction','BtStrafeShootAction',
    'BtInCoverAction','BtSniperShootAction','BtShootLiquidBeamAction','BtValkyrieShootAction','BtReloadAction','BtWeaponMalfunctionAction','BtSwitchWeaponAction'})do
    local gun,breed=unit('minion',true);local brain=brain(gun,breed)
    local data={aim_duration=1.2,shoot_timing={step=.6},shoot_template={},time_per_shot={{.24,.24}},shoot_cooldown={{3.6,3.6}}}
    local node={identifier=name,tree_node={name,action_data=data},children=function()return {}end,leave=function()end}
    function node:enter(unit,breed,bb,pad,actual)
        assert(actual==data);pad.perception_component={target_unit=target};pad.perception_extension={alert_nearby_allies=function()end};pad.scope_reflection_timing=true
        attack.start_shooting(unit,pad,0,actual,actual.shoot_timing.step,true)
        close(pad.next_shoot_timing,.6);close(pad.shoot_attack_speed,1)
    end
    function node:run()return 'running',false end
    brain._behavior_tree={root=function()return node end};brain:update(gun,.1,0)
    assert(#current.trees[brain._behavior_tree]==0 and current.moves[gun].swap_slots==nil)
    assert(current.action_copy(data,false,'attack',name,1.2)==nil)
    close(current:attack_rate(gun,name),1);close(current:animation_rate(brain),1)
    for _=1,50 do brain:update(gun,.1,1)end
    assert(current.moves[gun].swap_slots==nil and node.tree_node.action_data==data)
    -- Other buffs still pass through the game's ranged timing path unchanged.
    gun.ext.buff_system.stat_buffs=function()return {ranged_attack_speed=1.3}end
    attack.start_shooting(gun,brain._scratchpad,0,data,.6,true)
    close(brain._scratchpad.next_shoot_timing,.6/1.3)
end
local flamer,fb=unit('minion',true);local fa=brain(flamer,fb)
fa._running_leaf_node={tree_node={'BtRenegadeFlamerPatrolAction'}};fa._scratchpad={behavior_component={move_state='moving'}}
current:movement(flamer,fb,fa);close(current:animation_rate(fa),1.2)
fa._scratchpad.shoot_state='shooting';close(current:animation_rate(fa),1)
assert(current.action_copy({attack_duration=2,place_liquid_timing_speed=8},false,'move','BtRenegadeFlamerPatrolAction',1.2)==nil)
for _,name in ipairs({'BtGrenadierThrowAction','BtQuickGrenadeThrowAction','BtShootNetAction','BtChaosHoundLeapAction','BtChaosHoundTargetPouncedAction','BtMutantChargerChargeAction'})do
    close(current:attack_rate(u,name),1.2)
    local copy=current.action_copy({aim_duration=1.2,shoot_net_cooldown=12,throw_timing={throw=.6},throw_duration=2.4},false,'attack',name,1.2)
    close(copy.aim_duration,1);close(copy.shoot_net_cooldown,10);close(copy.throw_timing.throw,.5)
end

projectiles=0
-- Every native animation of both grenadier breeds, including quick throws,
-- must shorten release/recovery and explicit/default difficulty cooldowns.
for breed_name,actions in pairs(grenade_actions)do
    for name,data in pairs(actions)do
        local quick=name=='quick_throw_grenade'
        local class=quick and BtQuickGrenadeThrowAction or BtGrenadierThrowAction
        for anim,release_time in pairs(data.throw_timings or data.throw_timing)do
            local bomber,bb=unit('minion',true)
            local action_node=setmetatable({identifier='throw',tree_node={quick and 'BtQuickGrenadeThrowAction' or 'BtGrenadierThrowAction',action_data=data}},class)
            function action_node:children()return {}end
            local captured
            function action_node:enter(u,breed,blackboard,pad,modified,t)
                class.enter(self,u,breed,blackboard,pad,modified,t)
                close(pad.throw_timing-t,release_time/1.2)
                close(pad.action_duration-t,data.action_durations[anim]/1.2)
                close(pad.effect_template_timing-t,data.effect_template_timings[anim]/1.2)
                if data.start_drop_grenade_timing then close(pad.start_drop_grenade_timing-t,data.start_drop_grenade_timing[anim]/1.2)end
                captured=modified
                self:_throw_grenade(u,breed,pad,modified,'throw',Vector3.zero(),Vector3(1,0,0),blackboard,t)
                pad.throw_timing=nil
                if quick then class.leave(self,u,breed,blackboard,pad,modified,t)end
                local native_cooldown=data.cooldown or modules['scripts/settings/difficulty/minion_difficulty_settings'].cooldowns.grenadier_throw
                close(blackboard.throw_grenade.next_throw_at_t-t,native_cooldown[1]/1.2)
                return nil,'native return'
            end
            function action_node:run()return 'running',false end
            function action_node:leave()end
            local bomber_brain=brain(bomber,bb)
            bomber_brain._behavior_tree={root=function()return action_node end}
            bomber_brain._blackboard.throw_grenade={anim_event=anim}
            bomber_brain:update(bomber,.1,20)
            assert(action_node.tree_node.action_data==data and captured~=data)
            close(bomber.ext.navigation_system._max_speed_with_modifiers,6)
            close(bomber.ext.locomotion_system._engine_extension_id.scale[1],1)
        end
    end
end
assert(projectiles==8,'All six standard and two quick native grenade animations were exercised')
assert(grenade_actions.renegade.throw_grenade.cooldown==nil,'Do not mutate shared fallback data')


-- Idle/ranged-only frames never prepare or publish a native rate table.
local Native=modules['./native_timestep.lua']
local original_begin,original_bind=Native.begin,Native.bind
local begins,binds=0,0
Native.begin=function(...)begins=begins+1;return original_begin(...)end
Native.bind=function(...)binds=binds+1;return original_bind(...)end
local animation=assert(loadstring(shipped_package_files['lua/animation.lua']))()
local native_unit={anim={times={0},states={1},ids={1},layers=1}}
local fake={world=level_world,moves={[native_unit]={brain={}}},animation_rate=function()return 1 end}
for _=1,60 do assert(not animation.before(fake,level_world,1/60))end
assert(begins==0 and binds==0 and not native_dt.enabled)
fake.animation_rate=function()return 1.2 end
assert(animation.before(fake,level_world,.1));animation.after()
assert(begins==1 and binds==1 and not native_dt.enabled)
fake.animation_rate=function()return 1 end
assert(not animation.before(fake,level_world,.1) and not native_dt.enabled)
assert(begins==1 and binds==1 and fake.animation_records[native_unit]==nil)
Native.begin,Native.bind=original_begin,original_bind
-- Exercise the real bomber approach/lunge and death deadline at 1.2x.
local systems=Managers.state.extension.system
Managers.state.extension.system=function(self,name)
    if name=='side_system' then return {side_by_unit=setmetatable({},{__index=function()return {relation_sides=function()return {}end}end})}end
    if name=='group_system' then return {bot_groups_from_sides=function()return {}end}end
    return systems(self,name)
end
local bomber,bb=unit('minion',true);bb.name='chaos_poxwalker_bomber';bb.run_speed=5
bomber.anim={times={0},states={1},ids={1},layers=1};bomber.wanted_root_position={.12,0,0}
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
local duration=bomber_actions.approach.lunge_duration/1.2
close(ba._scratchpad.lunge_duration,100+duration)
close(ba._scratchpad.move_during_lunge_duration,100+bomber_actions.approach.move_during_lunge_duration/1.2)
close(ba._blackboard.death.fuse_timer,101.5);close(current:animation_rate(ba),1.2)
assert(nav._num_movement_modifiers==0)
ba:update(bomber,.1,100+duration-.001);assert(kills==0)
close(nav._max_speed_with_modifiers,1.2)
ba:update(bomber,.1,100+duration+.001);assert(kills==1)
attacks.execute=execute;Managers.state.extension.system=systems

local victim=unit('player');local first_person=unit('player')
victim.ext.unit_data_system.components.disabled_character_state={disabling_unit=u}
victim.ext.first_person_system={first_person_unit=function()return first_person end}
ai._running_leaf_node={tree_node={'BtMutantChargerChargeAction'}};ai._scratchpad={state='smashing',grabbed_target=victim}
animation_units={u,victim,first_person,bomber}
for _,who in ipairs(animation_units)do who.anim={times={0},states={1},ids={1},layers=1}end
local world=modules['scripts/foundation/utilities/script_world']
world.update(level_world,.1)
for _,who in ipairs(animation_units)do close(who.anim.times[1],.12)end
victim.ext.unit_data_system.components.disabled_character_state.disabling_unit=nil
world.update(level_world,.1);close(victim.anim.times[1],.22);close(first_person.anim.times[1],.22)

assert(#messages==0)
engine.finish();assert(not native_dt.enabled);animation_units={}
