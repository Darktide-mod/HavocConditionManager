-- Runs after the real package/DMF integration suite, using the native game
-- actions and owned unit/navigation facades. No live game modifications.
Vector3.direction_length=function(v)local length=Vector3.length(v);return Vector3.normalize(v),length end
Vector3.equal=function(a,b)return Vector3.distance_squared(a,b)<1e-12 end
Vector3.angle=function()return .5 end
local function copied(files)local out={};for k,v in pairs(files)do out[k]=v end;return out end
local old=copied(package_files)
old['lua/main.lua'],old['lua/animation.lua']=diagnostic_main,diagnostic_animation
old['package.json']=old['package.json']:gsub('"package_version": "1.7.4"','"package_version": "1.7.1"')
local function spawn(steps,dt,exit,animated,expect_rate)
    local u,breed=unit();breed.name='cultist_mutant';breed.run_speed=7.1
    u.position={0,0,0}
    local ai=brain(u,breed);ai:update(u,.1,50)
    local current=mod._diy_frenzied_assault_hooks_v1.current
    local nav,loco=u.ext.navigation_system,u.ext.locomotion_system
    nav.destination=function()return Vector3.zero()end
    nav.stop=function(self)self.stopped=true end
    local spawner={ext={minion_spawner_system={spawn_type=function()return 'door' end,
        exit_position_boxed=function()return Vector3Box(exit)end,
        spawn_height=function()return 3 end,spawn_horizontal_length=function()return 2 end}}}
    local bb={spawn={spawner_unit=spawner,spawner_spawn_index=1,is_exiting_spawner=true,anim_translation_scale_factor=1},behavior={}}
    local action=setmetatable({tree_node={'BtExitSpawnerAction'}},BtExitSpawnerAction)
    local data={run_anim_event='run'}
    if animated then
        data.spawn_type_anim_events={door='emerge'}
        data.anim_driven_anim_event_durations={emerge=1.5}
        data.spawn_type_anim_lengths={door={emerge={vertical_length=2,horizontal_length=4}}}
    end
    assert(current.action_copy(data,false,'native','BtExitSpawnerAction',2)==nil,'Spawn data is never rewritten')
    local pad={};ai._running_leaf_node=action;ai._scratchpad=pad
    action:enter(u,breed,bb,pad,data,100)
    close(current:animation_rate(ai),expect_rate)
    if animated then
        close(pad.anim_duration,101.5)
        local scale=loco:anim_translation_scale();close(scale.x,.5);close(scale.z,1.5)
        assert(loco._engine_extension_id.anim_driven)
        assert(action:run(u,breed,bb,pad,data,dt,101.49)=='running')
        assert(action:run(u,breed,bb,pad,data,dt,101.5)=='done')
    else
        local done=false
        for i=1,steps do
            if action:run(u,breed,bb,pad,data,dt,100+i*dt)=='done' then done=true;break end
            local v=loco._engine_extension_id.velocity
            u.position={u.position[1]+v[1]*dt,u.position[2]+v[2]*dt,u.position[3]+v[3]*dt}
        end
        if expect_rate==2 then
            assert(not done,'Released 1.7.1 must reproduce the never-ending final-step oscillation')
            close(Vector3.distance(POSITION_LOOKUP[u],exit),Vector3.length(exit))
            return
        end
        assert(done,'The native exit action must complete')
        assert(Vector3.distance(POSITION_LOOKUP[u],exit)<=.01)
    end
    action:leave(u,breed,bb,pad,data,102,'done',false)
    assert(not bb.spawn.is_exiting_spawner and bb.spawn.spawner_unit==nil and bb.spawn.spawner_spawn_index==-1)
    assert(loco.movement_type=='snap_to_navmesh' and nav.stopped)
    if animated then
        assert(not loco._engine_extension_id.anim_driven)
        local scale=loco:anim_translation_scale();close(scale.x,1);close(scale.y,1);close(scale.z,1)
    end
    ai._running_leaf_node={tree_node={'BtMoveToPositionAction'}};ai._scratchpad={behavior_component={move_state='moving'}}
    close(current:animation_rate(ai),2)
    close(nav._max_speed_with_modifiers,10)
end
engine=start(old)
spawn(120,1/60,Vector3(.04,0,0),false,2)
local retired=mod._diy_frenzied_assault_hooks_v1;engine.finish()
engine=start();assert(retired.current==nil and mod._diy_frenzied_assault_hooks_v1.revision=='1.7.4')
for _,dt in ipairs({1/30,1/60,1/120})do
    for _,exit in ipairs({Vector3(.04,0,0),Vector3(-.03,.04,0),Vector3(.02,.02,.02),Vector3(2,-3,1)})do
        spawn(300,dt,exit,false,1)
    end
end
spawn(1,1/60,Vector3(.04,0,0),true,1)
-- Native smart-object door acquire, authored rotate/open waits, and release.
local current=mod._diy_frenzied_assault_hooks_v1.current
local u,breed=unit();local ai=brain(u,breed);ai:update(u,.1,60)
local nav,loco=u.ext.navigation_system,u.ext.locomotion_system
nav._behavior_component={move_medium='ground'}
nav._nav_smart_object_component={id=1,type='doors',entrance_position=Vector3Box(Vector3.zero()),exit_position=Vector3Box(Vector3(1,0,0))}
function nav:_update_next_smart_object()end
local blocked,opened=true,false
local door={ext={door_system={can_open=function()return not opened end,
    open=function(_,_,opener,duration)assert(opener==u);close(duration,.6);opened=true end,
    nav_blocked=function()return blocked end}}}
nav._nav_smart_object_component.unit=door
local bb={nav_smart_object=nav._nav_smart_object_component,behavior={}}
local pad={};local action=setmetatable({tree_node={'BtOpenDoorAction'}},BtOpenDoorAction)
local data={rotation_duration=.3,open_door_time=.4}
ai._running_leaf_node=action;ai._scratchpad=pad
assert(current.action_copy(data,false,'native','BtOpenDoorAction',2)==nil)
action:enter(u,breed,bb,pad,data,100)
assert(nav:is_using_smart_object() and nav._nav_bot.manual)
close(current:animation_rate(ai),1);close(pad.rotation_done_time,100.3)
assert(action:run(u,breed,bb,pad,data,.1,100.2)=='running' and not opened)
assert(action:run(u,breed,bb,pad,data,.1,100.31)=='running' and opened)
close(pad.open_door_time,100.71)
blocked=false;assert(action:run(u,breed,bb,pad,data,.1,100.6)=='running')
assert(action:run(u,breed,bb,pad,data,.1,100.8)=='done')
action:leave(u,breed,bb,pad,data,100.8,'done',false)
assert(not nav:is_using_smart_object() and not nav._nav_bot.manual)
-- Cover approach is endpoint-constrained too; charges still accelerate
-- except while native navigation owns a smart-object traversal.
ai._running_leaf_node={tree_node={'BtInCoverAction'}};ai._scratchpad={state='entering'}
close(current:animation_rate(ai),1)
loco:set_wanted_velocity(Vector3(.1,.2,-3));close(loco._engine_extension_id.velocity[1],.1)
ai._scratchpad.state='shooting';close(current:animation_rate(ai),2)
for _,name in ipairs({'BtMutantChargerChargeAction','BtChargeAction'})do
    ai._running_leaf_node={tree_node={name}};ai._scratchpad={state='charging'}
    for _,method in ipairs({'set_wanted_velocity','set_wanted_velocity_flat'})do
        loco[method](loco,Vector3(2,3,-4));close(loco._engine_extension_id.velocity[1],4);close(loco._engine_extension_id.velocity[3],-4)
        assert(nav:use_smart_object(true));close(current:animation_rate(ai),1)
        loco[method](loco,Vector3(2,3,-4));close(loco._engine_extension_id.velocity[1],2);close(loco._engine_extension_id.velocity[3],-4)
        nav:use_smart_object(false);close(current:animation_rate(ai),2)
    end
end
engine.finish()
