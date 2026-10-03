"""Exercise HCM boundaries with current game data and constructor arguments."""
from project_env import GAME, SOURCES
from lupa.luajit21 import LuaRuntime
import re

ROOT = SOURCES / 'HavocConditionManager/scripts/mods/HavocConditionManager'


def difficulty_picker():
    lua = LuaRuntime(unpack_returned_tuples=True)
    lua.execute('''
        settings=function(_,value) return value end
        Localize=function(key) return key end
        Color=setmetatable({}, {__index=function() return function() return {255,255,255,255} end end})
        math.clamp=function(x,a,b) return math.max(a,math.min(b,x)) end
        Managers={time={time=function() return 1 end}}
        modules={}
        modules['scripts/settings/ui/ui_sound_events']={}
        modules['scripts/utilities/ui/colors']={color_copy=function(from,to)
            for i,v in ipairs(from) do to[i]=v end
        end}
        require=function(path) return assert(modules[path],path) end
    ''')
    danger = lua.execute((GAME / 'scripts/settings/difficulty/danger_settings.lua').read_text(encoding='utf-8-sig'))
    lua.globals().modules['scripts/settings/difficulty/danger_settings'] = danger
    picker = lua.execute((ROOT / 'condition_manager_view/stepper_templates.lua').read_text(encoding='utf-8-sig'))
    lua.globals().picker = picker
    lua.globals().danger_settings = danger
    lua.execute('''
        function check_picker(levels)
            local renderer={input_service={get=function() return false end}}
            local content={danger=1,hotspot_left={},hotspot_right={}}
            for i=1,5 do content['hotspot_'..i]={} end
            for i=1,5 do
                content.danger=i; content.last_danger=nil
                picker.difficulty_stepper[1].value(nil,renderer,nil,content)
                assert(content.difficulty_text==levels[i].display_name)
                for _,pass in ipairs(picker.difficulty_stepper) do
                    if pass.change_function and pass.style_id and pass.style_id:find('difficulty') then
                        local style={color={},size={}}
                        pass.change_function(content,style)
                        for channel=2,4 do assert(style.color[channel]==levels[i].color[channel]) end
                        local index=tonumber(pass.style_id:match('difficulty_bar_(%d+)'))
                        assert(style.color[1]==(index<=i and 255 or 64))
                    end
                end
            end
        end
        check_picker(danger_settings.danger_levels)
    ''')
    # The same five positions remain valid with legacy flat data.
    lua.globals().modules['scripts/settings/difficulty/danger_settings'] = danger.danger_levels
    lua.globals().picker = lua.execute((ROOT / 'condition_manager_view/stepper_templates.lua').read_text(encoding='utf-8-sig'))
    lua.execute('check_picker(danger_settings.danger_levels)')


def runtime_hooks():
    lua = LuaRuntime(unpack_returned_tuples=True)
    lua.execute('''
        hooks={}; modules={}; host=true
        runtime={prepare=function(t) return t end,config=function() return {fine={}} end}
        mod={template_runtime=runtime,has_local_gameplay_authority=function() return host end,
            io_dofile=function() end,start_spawn_tracking=function() end}
        get_mod=function() return mod end
        require=function(path) modules[path]=modules[path] or {}; return modules[path] end
        local pacing=require('scripts/managers/pacing/pacing_manager')
        pacing._apply_template=function() end
        require('scripts/managers/pacing/heat_pacing/heat_pacing').resume=function() end
        require('scripts/managers/terror_event/terror_event_nodes').spawn_by_points={}
        function mod:hook(target,name,fn) hooks[target]=hooks[target] or {};hooks[target][name]=fn end
        function mod:hook_safe(target,name,fn) hooks[target]=hooks[target] or {};hooks[target][name..'_safe']=fn end
        Managers={state={}}
    ''')
    lua.execute((ROOT / 'native_runtime_hooks.lua').read_text(encoding='utf-8-sig'))
    lua.execute('''
        local roamer=require('scripts/managers/pacing/roamer_pacing/roamer_pacing')
        for _,enabled in ipairs({true,false}) do
            host=enabled
            local a,b,c=hooks[roamer].init(function(self,nav,template,seed,factions,forced,...)
                assert(seed==123 and forced=='cultist', 'forced sub-faction was dropped')
                assert(select('#',...)==2 and select(2,...)=='tail')
                return 17,nil,23
            end,{},nil,{},123,{},'cultist',nil,'tail')
            assert(a==17 and b==nil and c==23)
        end
    ''')


def ability_actions():
    """Run the real resource consumers; stub engine construction/proc sinks."""
    lua = LuaRuntime(unpack_returned_tuples=True)
    lua.execute('''
        modules={}; require=function(path) modules[path]=modules[path] or {};return modules[path] end
        table.keys=function(t) local out={} for k in pairs(t) do out[#out+1]=k end return out end
        math.clamp=function(x,a,b) return math.max(a,math.min(b,x)) end
        math.round=function(x) return math.floor(x+.5) end
        modules['scripts/settings/player_character/player_character_constants']={ability_configuration={}}
        modules['scripts/settings/buff/buff_settings']={keywords={},proc_events={}}
        ALIVE={}; Managers={state={}}; shared={}
        get_mod=function() return shared end
        ScriptUnit={has_extension=function(unit,name)
            return name=='ability_system' and unit.ability or nil
        end}
        mod={hook_require=function() end}
        unit={};ALIVE[unit]=true;events={};stats={}
    ''')
    constants = (GAME / 'scripts/network_lookup/network_constants.lua').read_text(encoding='utf-8-sig')
    precision = re.search(r'NetworkConstants\.ability_resource_precision = (\d+)', constants)
    assert precision, 'Native resource precision changed; update the fixture explicitly'
    lua.execute('NetworkConstants={ability_resource_precision=' + precision.group(1) + '}')
    lua.execute((GAME / 'scripts/foundation/utilities/class.lua').read_text(encoding='utf-8-sig'))
    lua.globals().Ability = lua.execute((GAME / 'scripts/extension_systems/ability/player_unit_ability_extension.lua').read_text(encoding='utf-8-sig'))
    lua.globals().adapter = lua.execute((ROOT / 'diy/diy_game.lua').read_text(encoding='utf-8-sig'))
    lua.execute('''
        api=adapter.new(mod,{events={}},{},{name='HCM',authority=function()return true end,engine=function()end})
        function setup(abilities,resources)
            stats={};events={}
            local components={}
            for kind,ability in pairs(abilities) do
                local resource=resources[kind] or 0
                local cost=ability.only_uses_charges and 1 or ability.resource_cost_per_charge
                components[kind]={enabled=true,resource=math.round(resource*NetworkConstants.ability_resource_precision),
                    num_charges=ability.usage_cost_type=='resource' and 0 or math.floor(resource/cost)}
            end
            ext=setmetatable({_equipped_abilities=abilities,_ability_components=components,_charge_replenished={},
                _buff_extension={stat_buffs=function()return stats end,has_keyword=function()return false end}},Ability)
            for _,name in ipairs({'_proc_ability_resource_restored_event','_proc_ability_resource_consumed_event',
                '_proc_ability_charge_replenished_event','_proc_ability_charge_consumed_event','_record_ability_charge_gained_stat'}) do
                ext[name]=function(self,kind,target,actual) events[#events+1]={name=name,kind=kind,target=target,actual=actual} end
            end
            unit.ability=ext
        end
        function cooldown(value,kind,event)
            return api.action({type='ability_cooldown',amount=value,amount_kind=kind},unit,event)
        end
        function resource_is(kind,value,charges)
            assert(math.abs(ext:remaining_ability_resource(kind)-value)<.00001)
            if charges then assert(ext:remaining_ability_charges(kind)==charges) end
        end
        setup({combat_ability={max_charges=2,resource_cost_per_charge=20,resource_regen_per_second=1}}, {combat_ability=5})
        assert(cooldown(.25,'fraction'));resource_is('combat_ability',10,0)
        assert(cooldown(5,'absolute'));resource_is('combat_ability',15,0)
        assert(cooldown(.25,'event_damage',{damage=40}));resource_is('combat_ability',25,1)
        assert(ext._charge_replenished.combat_ability)
        stats.combat_ability_resource_flat_restored=2;stats.combat_ability_resource_restored_modifier=.5
        assert(cooldown(4,'absolute'));resource_is('combat_ability',28,1)
        assert(cooldown(-5,'absolute'));resource_is('combat_ability',23,1)
        assert(cooldown(-1,'fraction'));resource_is('combat_ability',3,0)
        stats={};assert(cooldown(100,'absolute'));resource_is('combat_ability',40,2)
        local before=#events
        assert(cooldown(-100,'absolute'));resource_is('combat_ability',40,2);assert(#events==before)
        ext._ability_components.combat_ability.enabled=false
        assert(not cooldown(1,'absolute'));resource_is('combat_ability',40)
        setup({combat_ability={max_charges=2,only_uses_charges=true}}, {combat_ability=0})
        assert(not cooldown(1,'fraction'));resource_is('combat_ability',0,0)
        setup({combat_ability={usage_cost_type='resource',max_resource=100,resource_regen_percent_per_second=.02}}, {combat_ability=20})
        assert(cooldown(5,'absolute'));resource_is('combat_ability',30)
        assert(cooldown(.25,'fraction'));resource_is('combat_ability',55)
        ext._equipped_abilities.combat_ability.resource_regen_per_second=1
        assert(cooldown(5,'absolute'));resource_is('combat_ability',70)
        assert(cooldown(-100,'absolute'));resource_is('combat_ability',0)
        ext._equipped_abilities.combat_ability.resource_regen_per_second=0
        ext._equipped_abilities.combat_ability.resource_regen_percent_per_second=0
        assert(not cooldown(5,'absolute'));resource_is('combat_ability',0)
        setup({combat_ability={max_charges=2,resource_cost_per_charge=20,resource_regen_per_second=1}}, {combat_ability=30})
        stats.combat_ability_resource_flat_regen=8;stats.combat_ability_resource_regen_modifier=9
        assert(cooldown(5,'flat'));resource_is('combat_ability',35,1)
        stats.combat_ability_resource_flat_consumed=2;stats.combat_ability_resource_consumed_modifier=.5
        assert(cooldown(-6,'flat'));resource_is('combat_ability',31,1)
        setup({combat_ability={max_charges=1,resource_cost_per_charge=20,resource_pool_override='grenade_ability'},
            grenade_ability={max_charges=2,resource_cost_per_charge=20,resource_regen_per_second=1}}, {grenade_ability=5})
        assert(cooldown(20,'absolute'));resource_is('grenade_ability',25,1);resource_is('combat_ability',0,0)
        assert(cooldown(-10,'absolute'));resource_is('grenade_ability',15,0)
        setup({grenade_ability={max_charges=3,only_uses_charges=true}}, {grenade_ability=1})
        assert(not cooldown(1,'absolute'))
        assert(api.action({type='grenades',amount=1,amount_kind='absolute'},unit));resource_is('grenade_ability',2,2)
        assert(api.action({type='grenades',amount=-5,amount_kind='absolute'},unit));resource_is('grenade_ability',0,0)
        -- Existing flat cooldown API remains the selected legacy boundary.
        local delta
        unit.ability={has_ability_type=function()return true end,max_ability_cooldown=function()return 40 end,
            reduce_ability_cooldown_time=function(self,kind,value)assert(kind=='combat_ability');delta=value end}
        assert(cooldown(.25,'fraction') and delta==10)
        assert(cooldown(3,'absolute') and delta==3)
        assert(cooldown(.5,'event_damage',{damage_amount=8}) and delta==4)
        assert(cooldown(-5,'absolute') and delta==-5)
        assert(shared._diy_action_depth==0)
        unit.ability=nil;assert(not cooldown(1,'absolute'))
    ''')


if __name__ == '__main__':
    difficulty_picker()
    print('Current/legacy difficulty labels and colors: PASS')
    runtime_hooks()
    print('Roamer forced sub-faction, trailing nil arguments and return values: PASS')
    ability_actions()
    print('Native charged/continuous/shared resources, disabled/inventory abilities, grenades and legacy cooldown boundary: PASS')
