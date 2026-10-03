"""Native replacement/loading methods with real HCM schema/runtime boundaries.

Prepared for authorized Lua execution. Navigation, object construction and package
loading are fixtures; native scheduling/activation/dispatch method bodies run.
"""
import re
from project_env import GAME, SOURCES
from lupa.luajit21 import LuaRuntime

ROOT = SOURCES / 'HavocConditionManager/scripts/mods/HavocConditionManager'


def install(lua, path, owner, *names):
    source = (GAME / path).read_text(encoding='utf-8-sig')
    for name in names:
        body = re.search(r'^' + owner + r'\.' + name + r' = function\b.*?^end$', source, re.M | re.S)
        assert body, (path, owner, name)
        lua.execute(body.group(0))


def fixture():
    lua = LuaRuntime(unpack_returned_tuples=True)
    lua.execute('''
        modules={};require=function(path) modules[path]=modules[path] or {};return modules[path] end
        modules['scripts/managers/terror_event/terror_event_nodes']={spawn_by_points={}}
        host=true;mod={values={},hooks={},originals={}}
        get_mod=function(name) return name=='HavocConditionManager' and mod or nil end
        function mod:get(key) return self.values[key] end
        function mod:hook(target,name,callback)
            self.hooks[target]=self.hooks[target] or {}
            self.originals[target]=self.originals[target] or {}
            assert(not self.hooks[target][name],'duplicate owner/method hook: '..name)
            self.hooks[target][name]=callback
            local original=target[name];self.originals[target][name]=original or false
            if original then target[name]=function(...) return callback(original,...) end end
        end
        function mod:hook_safe(target,name,callback)
            self:hook(target,name,function(fn,...)
                local result=fn(...);callback(...);return result
            end)
        end
        function restore_hooks()
            for target,methods in pairs(mod.originals) do
                for name,original in pairs(methods) do target[name]=original or nil end
            end
            mod.hooks={};mod.originals={}
        end
        mod.has_local_gameplay_authority=function()return host end
        function table.clear(t) for k in pairs(t) do t[k]=nil end end
        function table.append(a,b) for _,v in ipairs(b) do a[#a+1]=v end return a end
        function table.clone(t) local out={} for k,v in pairs(t) do out[k]=v end return out end
        math.clamp=function(x,a,b)return math.max(a,math.min(b,x))end
        Log={warning=function()error('unexpected native warning')end,info=function()end}
        Managers={state={game_session={}}}
    ''')
    return lua


def pacing_replacement():
    lua = fixture()
    # Real pure HCM modules; unrelated registration modules are explicit stubs.
    def load_module(path):
        name = path.rsplit('/', 1)[-1]
        if name in ('coordinated_load', 'elite_composition', 'recycling_config'):
            return lua.execute((ROOT / (name + '.lua')).read_text(encoding='utf-8-sig'))
        return lua.table()
    lua.globals().load_module = load_module
    lua.execute('''
        function mod:io_dofile(path)return load_module(path)end
        mod.values.native_configuration_v3={combat_tolerance=2}
        mod.template_registry={by_table={},children={},breeds={},
            validate_config=function(raw)return raw or {patches={},rules={}}end}
        mod.template_conditions={}
        mod.spawn_placement={finish=function()cleanup_calls=cleanup_calls+1 end}
        cleanup_calls=0;created=0;deleted=0
        for _,name in ipairs({'finish_native_warning_summary','finish_spawn_tracking','finish_straggler_recycling',
            'finish_spawn_flow','finish_encounter_reserve','start_spawn_tracking'}) do mod[name]=function()end end
        PacingManager={init=function()end};HeatPacing={};RoamerPacing={};AutoEvent={};AutoEventsTemplates={}
        function RoamerPacing:init(nav,template,seed,factions,forced)
            self._template=template;self.forced=forced;self.seed=seed
        end
        function RoamerPacing:new(...)
            created=created+1;local obj=setmetatable({}, {__index=self});obj:init(...);return obj
        end
        function RoamerPacing:destroy()deleted=deleted+1 end
        function RoamerPacing:delete()self:destroy()end
        function RoamerPacing:on_gameplay_post_init(level)self.level=level end
        function RoamerPacing:on_spawn_points_generated()self.generated=true end
        PacingTemplates={}
        function root(name,threshold,heat)
            return {name=name,progression_type='fixture',starting_state='relax',state_orders={'relax'},
                combat_state_settings={1},state_settings={1},max_tension={100},ramp_up_frequency_modifiers={1},
                challenge_rating_thresholds={roamers={threshold}},min_wound_tension_requirement={0},
                heat_settings=heat and {threshold=1} or nil,roamer_pacing_template={name=name},
                horde_pacing_template={resistance_templates={{name=name}}},
                monster_pacing_template={challenge_templates={{name=name}}},
                specials_pacing_template={resistance_templates={{name=name}}},auto_event_template=name}
        end
        PacingTemplates.a=root('a',20,true);PacingTemplates.b=root('b',30,true)
        PacingTemplates.c=root('c',40,false);PacingTemplates.default=PacingTemplates.a
        for name,template in pairs(PacingTemplates) do
            mod.template_registry.by_table[template]={id=name,root=template,family='pacing'}
            AutoEventsTemplates[name]={name=name}
        end
        modules['scripts/managers/pacing/pacing_manager']=PacingManager
        modules['scripts/managers/pacing/pacing_templates']=PacingTemplates
        modules['scripts/managers/pacing/heat_pacing/heat_pacing']=HeatPacing
        modules['scripts/managers/pacing/roamer_pacing/roamer_pacing']=RoamerPacing
        modules['scripts/managers/pacing/auto_event/auto_event']=AutoEvent
        Managers.state.difficulty={get_table_entry_by_challenge=function(_,t)return t[1]end,
            get_table_entry_by_resistance=function(_,t)return t[1]end}
    ''')
    lua.globals().mod.template_schema = lua.execute((ROOT / 'template_schema.lua').read_text(encoding='utf-8-sig'))
    lua.globals().mod.template_runtime = lua.execute((ROOT / 'template_runtime.lua').read_text(encoding='utf-8-sig'))
    install(lua, 'scripts/managers/pacing/pacing_manager.lua', 'PacingManager',
            '_apply_template', 'set_pacing_template', 'on_spawn_points_generated', 'reset')
    install(lua, 'scripts/managers/pacing/heat_pacing/heat_pacing.lua', 'HeatPacing', 'resume', 'suspend')
    install(lua, 'scripts/managers/pacing/auto_event/auto_event.lua', 'AutoEvent', 'swap_auto_event_template')
    hooks_source = (ROOT / 'native_runtime_hooks.lua').read_text(encoding='utf-8-sig')
    lua.execute(hooks_source)
    lua.execute('''
        assert(mod.hooks[PacingManager]._apply_template and mod.hooks[PacingManager].set_pacing_template and mod.hooks[HeatPacing].resume,
            'Replacement methods must exist before hooks load; do not gate this coverage off')
        E=mod.template_runtime
        function manager()
            local self=setmetatable({_template=E.prepare(PacingTemplates.a,'pacing'),_level_name='fixture',
                _level_seed=123,_sub_faction_types={},_mission_sub_faction_override='cultist',
                _change_state=function(self,t,state)self.state=state;self.state_t=t end,
                update_only_injected_slots=function()end,set_horde_pacing_rate_modifier=function()end,
                set_horde_pacing_timer_modifier=function()end}, {__index=PacingManager})
            self._heat_pacing=setmetatable({_template=self._template,_active=true,
                _change_heat_condition=function(self)self.resume_calls=(self.resume_calls or 0)+1 end},{__index=HeatPacing})
            self._roamer_pacing=RoamerPacing:new(nil,PacingTemplates.a.roamer_pacing_template,123,{},'cultist')
            self._auto_event=setmetatable({}, {__index=AutoEvent})
            self._horde_pacing={on_gameplay_post_init=function(self,level,tpl)self.received=tpl end}
            self._specials_pacing={on_spawn_points_generated=function(self,tpl)self.received=tpl end}
            self._monster_pacing={on_gameplay_post_init=function(self,level,tpl)
                self.calls=(self.calls or 0)+1;self.received=tpl
            end}
            Managers.state.pacing=self;return self
        end
        pm=manager();local before=created
        pm:set_pacing_template('a',1);assert(created==before and deleted==0)
        pm:set_pacing_template('b',2)
        assert(created==before+1 and deleted==1 and cleanup_calls==1)
        assert(pm._challenge_rating_thresholds.roamers==60 and pm.state_t==2)
        assert(pm._template==E.prepare(PacingTemplates.b,'pacing'))
        assert(pm._heat_pacing._template==pm._template and pm._pending_monster_template==pm._template)
        assert(pm._roamer_pacing.forced=='cultist' and pm._roamer_pacing.seed==123)
        assert(pm._auto_event._template==AutoEventsTemplates.b)
        pm:set_pacing_template('b',3);assert(created==before+1 and deleted==1)
        pm:on_spawn_points_generated();assert(pm._pending_monster_template==nil)
        assert(pm._monster_pacing.calls==1 and pm._monster_pacing.received.name=='b')
        pm:on_spawn_points_generated();assert(pm._monster_pacing.calls==1)
        mod.values.native_configuration_v3={combat_tolerance=3}
        pm:set_pacing_template('c',4)
        assert(pm._challenge_rating_thresholds.roamers==80,'Settings stay captured for this mission')
        assert(not pm._heat_pacing._active and pm._heat_pacing._suspended)
        pm:set_pacing_template('b',5)
        assert(pm._heat_pacing._active and not pm._heat_pacing._suspended and pm._heat_pacing.resume_calls==1)
        local count=created;pm:reset();assert(created==count+1 and pm._roamer_pacing.forced=='cultist')
        assert(PacingTemplates.b.challenge_rating_thresholds.roamers[1]==30,'Native globals remain unchanged')
        Managers.state.game_session={};pm=manager();pm:set_pacing_template('b',6)
        assert(pm._challenge_rating_thresholds.roamers==90,'New mission captures new settings')
        mod.reset_native_spawn_scaling()
        mod.values.native_configuration_v3={};Managers.state.game_session={};pm=manager()
        pm:set_pacing_template('b',7);assert(pm._template==PacingTemplates.b and pm._challenge_rating_thresholds.roamers==30)
        host=false;pm:set_pacing_template('c',8)
        assert(pm._template==PacingTemplates.c and pm._pending_monster_template==PacingTemplates.c)
        assert(not pm._heat_pacing._active)
        pm:set_pacing_template('unknown',8)
        assert(pm._template==PacingTemplates.default and pm._heat_pacing._template==PacingTemplates.default)
        host=true;mod.reset_native_spawn_scaling();restore_hooks()
    ''')
    # Reload the registrations after native methods are restored; do not stack hooks.
    lua.execute(hooks_source)
    lua.execute('''
        mod.values.native_configuration_v3={combat_tolerance=4};Managers.state.game_session={}
        pm=manager();pm:set_pacing_template('b',9)
        local count=created;pm:set_pacing_template('b',10)
        assert(pm._challenge_rating_thresholds.roamers==120 and created==count)
        pm:set_pacing_template('unknown',11);count=created;pm:set_pacing_template('unknown',12)
        assert(pm._template==E.prepare(PacingTemplates.default,'pacing') and created==count)
        local custom={_template={},_pending_monster_template=PacingTemplates.b}
        local a,b,c=mod.hooks[PacingManager].set_pacing_template(function(self,name,...)
            assert(name=='b' and select('#',...)==2 and select(2,...)=='tail')
            return 17,nil,23
        end,custom,'b',nil,'tail')
        assert(a==17 and b==nil and c==23 and custom._pending_monster_template==E.prepare(PacingTemplates.b,'pacing'))
        -- Legacy sources lack these replacement methods; registration stays optional.
        restore_hooks();PacingManager._apply_template=nil;PacingManager.set_pacing_template=nil;HeatPacing.resume=nil
    ''')
    lua.execute(hooks_source)
    lua.execute('assert(not mod.hooks[PacingManager]._apply_template and not mod.hooks[PacingManager].set_pacing_template and not mod.hooks[HeatPacing])')


def mutator_readiness():
    lua = fixture()
    lua.execute('''
        MutatorManager={};MutatorBase={};MutatorTemplates={};CircumstanceTemplates={};packages={};created=0
        data={circumstances={'one','duplicate'}}
        CircumstanceTemplates.one={mutators={'delayed','ready','manual'}}
        CircumstanceTemplates.duplicate={mutators={'delayed','ready'}}
        local stim='scripts/managers/mutator/mutators/mutator_stimmed_minions'
        MutatorTemplates.delayed={class='fixture/mutator',delay=true,activate_on_load=true,buff_templates={'fixture'}}
        MutatorTemplates.ready={class='fixture/mutator',activate_on_load=true,buff_templates={'fixture'}}
        MutatorTemplates.manual={class='fixture/mutator',activate_on_load=false}
        MutatorTemplates.stim={class=stim,activate_on_load=false}
        function new_events()
            return {listeners={},unregister=function(self,obj,event)self.listeners[obj]=nil end}
        end
        Managers.event=new_events();Managers.package={has_loaded=function(_,name)return packages[name] end}
        Managers.state.difficulty={get_parsed_havoc_data=function()return data end}
        ALIVE={}
        local Constructor={}
        function Constructor:new(server,delegate,template)
            created=created+1
            local obj=setmetatable({_is_server=server,_template=template,_is_active=false,_is_loaded=not template.delay,
                _required_packages=template.delay and {'fixture/package'} or {},sequence={},registrations=0,buff_adds=0},
                {__index=MutatorBase})
            obj._register_event_listeners=function(self)self.registrations=self.registrations+1 end
            obj._remove_event_listeners=function()end;obj._remove_buffs=function()end
            obj._add_buffs=function(self)self.buff_adds=self.buff_adds+1 end
            obj._on_minion_unit_spawned=function(self,unit)self.sequence[#self.sequence+1]='spawn' end
            obj.update=function(self)self.sequence[#self.sequence+1]='update' end
            if template.class==stim then Managers.event.listeners[obj]=true end
            return obj
        end
        modules['scripts/managers/mutator/mutator_manager']=MutatorManager
        modules['scripts/settings/circumstance/circumstance_templates']=CircumstanceTemplates
        modules['fixture/mutator']=Constructor;modules[stim]=Constructor
        function manager(server)return setmetatable({_mutators={},_deferred_callbacks={},_is_server=server},{__index=MutatorManager})end
    ''')
    install(lua, 'scripts/managers/mutator/mutators/mutator_base.lua', 'MutatorBase',
            'is_loading_done', 'is_loading', 'is_active', 'activate', 'deactivate')
    install(lua, 'scripts/managers/mutator/mutator_manager.lua', 'MutatorManager',
            '_load_mutators', 'load_mutator_from_name', 'activate_mutator', 'deactivate_mutator', 'destroy',
            'is_loading', 'update', '_defer_callback', '_flush_deferred_callbacks', '_on_minion_unit_spawned')
    source = (ROOT / 'condition_compatibility.lua').read_text(encoding='utf-8-sig')
    lua.execute(source)
    lua.execute('''
        owner=manager(true);owner:_load_mutators('one')
        local delayed,ready,manual=owner._mutators.delayed,owner._mutators.ready,owner._mutators.manual
        assert(created==3 and not delayed:is_active() and ready:is_active() and not manual:is_active())
        assert(not owner._hcm_loading_mutator)
        owner:_load_mutators('one');assert(created==3 and owner._mutators.delayed==delayed and ready.registrations==1)
        local unit={};ALIVE[unit]=true;owner:_on_minion_unit_spawned(unit)
        assert(#owner._deferred_callbacks==1 and #delayed.sequence==0)
        assert(owner:is_loading() and not delayed:is_active() and #owner._deferred_callbacks==1)
        packages['fixture/package']=true
        assert(not owner:is_loading() and delayed:is_active() and delayed.registrations==1 and delayed.buff_adds==1)
        assert(not owner:is_loading() and delayed.registrations==1 and not manual:is_active())
        owner:update(.1,1)
        assert(#owner._deferred_callbacks==0 and delayed.sequence[1]=='spawn' and delayed.sequence[2]=='update')
        assert(ready.sequence[1]=='spawn' and ready.sequence[2]=='update' and #manual.sequence==0)
        owner:activate_mutator('manual');assert(manual:is_active() and manual.registrations==1)
        -- Outside HCM's load, retain native immediate activation semantics.
        local foreign=manager(true);local outside=foreign:load_mutator_from_name('delayed')
        assert(outside:is_active() and not outside:is_loading_done())
        -- Restore scope even when a native construction failure propagates.
        local loader=owner.load_mutator_from_name
        owner.load_mutator_from_name=function()error('fixture construction failure')end
        CircumstanceTemplates.failure={mutators={'missing'}};data={circumstances={'failure'}}
        owner._hcm_loading_mutator='outer'
        local ok,err=pcall(owner._load_mutators,owner,'failure')
        assert(not ok and err:find('fixture construction failure') and owner._hcm_loading_mutator=='outer')
        owner._hcm_loading_mutator=nil;owner.load_mutator_from_name=loader
        -- Repeated loads retain the original event owner; foreign instances stay foreign.
        CircumstanceTemplates.stim={mutators={'stim'}};data={circumstances={'stim','stim'}}
        local first_events=Managers.event;local own=manager(true);own:_load_mutators('stim')
        local stim=own._mutators.stim;assert(first_events.listeners[stim])
        Managers.event=new_events();own:_load_mutators('stim')
        assert(own._hcm_aggro_listeners[stim]==first_events)
        Managers.state.mutator=own;mod.cleanup_condition_listeners();mod.cleanup_condition_listeners()
        assert(not first_events.listeners[stim])
        local preexisting=manager(true);local external=preexisting:load_mutator_from_name('stim')
        preexisting:_load_mutators('stim');assert(not preexisting._hcm_aggro_listeners)
        Managers.state.mutator=preexisting;mod.cleanup_condition_listeners();assert(Managers.event.listeners[external])
        -- New managers capture their own loading state; clients use the native bulk path.
        data={circumstances={'one'}};packages={};owner:destroy();owner:destroy()
        local next_mission=manager(true);next_mission:_load_mutators('one')
        assert(not next_mission._mutators.delayed:is_active() and next_mission._mutators.ready.registrations==1)
        retained=next_mission
        host=false;local client=manager(false);client:_load_mutators('one')
        assert(not client._mutators.delayed:is_active() and client._mutators.ready:is_active())
        host=true;restore_hooks()
    ''')
    lua.execute(source)
    lua.execute('''
        local same_delayed=retained._mutators.delayed
        retained:_load_mutators('one')
        assert(retained._mutators.delayed==same_delayed and retained._mutators.ready.registrations==1)
        assert(retained:is_loading() and not same_delayed:is_active())
        packages['fixture/package']=true
        assert(not retained:is_loading() and same_delayed.registrations==1)
        local reload=manager(true);reload:_load_mutators('one');reload:_load_mutators('one')
        assert(reload._mutators.ready.registrations==1 and not reload._mutators.delayed:is_active())
        -- The old API has no readiness method and keeps its original immediate activation.
        MutatorBase.is_loading_done=nil
        local legacy=manager(true);legacy:_load_mutators('one');assert(legacy._mutators.delayed:is_active())
    ''')


if __name__ == '__main__':
    pacing_replacement()
    print('Native pacing replacement, prepared identity, heat transitions, deferred monsters, mission snapshot, reload and legacy boundaries: PASS')
    mutator_readiness()
    print('Native mutator readiness/activation, deduplication, deferred spawning, scope cleanup, mission/reload and foreign ownership: PASS')
