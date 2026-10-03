"""Use native Buff and extension deletion to verify DIY update ownership."""
from functools import lru_cache
from pathlib import Path
import os
import subprocess

from project_env import PROJECT, GAME
from lupa.luajit21 import LuaRuntime

relative = 'diy/diy_game.lua' if PROJECT.name == 'HavocConditionManager' else 'modules/diy/diy_game.lua'
source = Path(os.environ.get('DIY_LIFECYCLE_SOURCE', PROJECT / 'src' / PROJECT.name / 'scripts/mods' / PROJECT.name / relative))
adapter_source = source.read_text(encoding='utf-8-sig')


@lru_cache(None)
def native(path):
    return subprocess.check_output(['git', '-c', 'safe.directory=' + GAME.as_posix(), '-c', 'gc.auto=0',
                                    'show', 'HEAD:' + path + '.lua'], cwd=GAME).decode('utf-8-sig')


def fixture(owners, active, pause_during_add=False):
    lua = LuaRuntime(unpack_returned_tuples=True)
    lua.execute(r'''
modules={}; require=function(path) modules[path]=modules[path] or {};return modules[path] end
Unit={};WwiseWorld={};Network={type_info=function()return {max_size=32}end}
Script={new_array=function()return {}end,new_map=function()return {}end};Profiler={start=function()end,stop=function()end}
table.clear=function(t)for k in pairs(t)do t[k]=nil end end
Log={exception=function()error('unexpected native buff error')end}
modules['scripts/utilities/fixed_frame']={get_latest_fixed_time=function()return 1 end}
modules['scripts/settings/buff/buff_settings']={stat_buff_type_base_values={},max_proc_events=300}
ALIVE={};HEALTH_ALIVE=ALIVE;Managers={state={}};mods={};shared={};apis={};engines={}
get_mod=function(name)return name=='DMF' and shared or mods[name]end
ScriptUnit={has_extension=function(u,name)return name=='buff_system' and u.ext or nil end,
    remove_extension=function(u,name)
        assert(ALIVE[u], 'Unit remains alive throughout native extension destruction')
        u.ext:delete();assert(ALIVE[u]);u.ext=nil
    end}
function make_mod(name)
    local mod={};mods[name]=mod
    function mod:hook_require(path,cb)if modules[path] then cb(modules[path])end end
    function mod:hook_safe(cls,name,cb)
        if name=='_update_stat_buffs_and_keywords' then self.stat_callback=cb end
        local original=assert(cls[name],name)
        cls[name]=function(...)local result=original(...);cb(...);return result end
    end
    function mod:hook(cls,name,cb)
        local original=assert(cls[name],name)
        cls[name]=function(...)return cb(original,...)end
    end
    return mod
end
''')
    lua.execute(native('scripts/foundation/utilities/class'))
    for path in ['scripts/extension_systems/buff/buff_extension_base',
                 'scripts/extension_systems/buff/minion_buff_extension',
                 'scripts/foundation/managers/extension/extension_system_base']:
        lua.globals().modules[path] = lua.execute(native(path))
    if pause_during_add:
        lua.execute(r'''
local System=modules['scripts/foundation/managers/extension/extension_system_base']
local original=System.on_add_extension
System.on_add_extension=function(self,...)
    local created=original(self,...)
    self:disable_update_function(created._unit,'update','add_pause')
    return created
end
''')
    for name in owners:
        lua.globals().adapter = lua.execute(adapter_source)
        lua.globals().owner = name
        lua.globals().active = name in active
        lua.execute(r'''
local enabled=active
local e={now=0,revision=1,finished=false,needs_minion_updates=function()return enabled end}
engines[owner]=e
local own_mod=make_mod(owner)
apis[#apis+1]=adapter.new(own_mod,{events={}},{apply=function()own_mod.effect_applies=(own_mod.effect_applies or 0)+1 end},
    {name=owner,authority=function()return own_mod.test_authority or false end,engine=function()return e end,skip_attack_report=true})
''')
    lua.execute(r'''
local Native=modules['scripts/extension_systems/buff/minion_buff_extension']
local System=modules['scripts/foundation/managers/extension/extension_system_base']
u={};ALIVE[u]=true;deleted_buffs=0;stats_calls=0;update_calls=0
ext=setmetatable({_unit=u,_update_enabled=false,_is_server=true,_is_hub=true,
    _buffs={},_buffs_by_index={},_update_proc_events=function()end,
    _update_stat_buffs_and_keywords=function()stats_calls=stats_calls+1 end,
    _update_buffs=function()update_calls=update_calls+1 end,_move_looping_sfx_sources=function()end},Native)
update_list={}
system=setmetatable({_name='buff_system',_extensions={MinionBuffExtension=1},_total_num_extensions=1,
    _update_list={MinionBuffExtension={update=update_list}},_hot_join_sync_list={},_fixed_update_extensions={},
    _disable_reasons={MinionBuffExtension={update={[u]={__default_disable_reason__=true}}}},
    _unit_to_extension_map={[u]=ext},_extension_to_unit_map={[ext]=u},_uninitiated_units={},
    _profiler_names={MinionBuffExtension='MinionBuffExtension [ALL]'},_staggered_update_iterators={}},System)
ext._owner_system=system;u.ext=ext
Managers.state.minion_spawn={spawned_minions=function()return {u}end}
for _,api in ipairs(apis)do api.update()end
function add_native_buff(index)
    local buff={template=function()return {}end,stack_count=function()return 1 end,
        instance_id=function()return index end,delete=function(self,extension_destroyed)
            self.__deleted=true;deleted_buffs=deleted_buffs+1
        end}
    ext:_on_add_buff(buff)
    ext._buffs[#ext._buffs+1]=buff;ext._buffs_by_index[index]=buff
end
function remove_unit()
    system:on_remove_extension(u,'MinionBuffExtension')
    assert(rawget(ext,'__deleted'))
    assert(update_list[u]==nil,'Destroyed MinionBuffExtension was registered again during native Buff removal')
    if shared._diy_minion_updates then assert(shared._diy_minion_updates.owned[ext]==nil,'Destroyed extension retained in DIY ownership')end
    ALIVE[u]=nil
    system:update({},.016,18.9588167)
end
function finish_all()
    for _,api in ipairs(apis)do api.finish()end
end
''')
    return lua


cases = 0
for owners, active in [([], []), (['HCM'], []), (['HCM'], ['HCM']),
                      (['MBM'], ['MBM']), (['HCM', 'MBM'], ['HCM']),
                      (['HCM', 'MBM'], ['MBM']), (['HCM', 'MBM'], ['HCM', 'MBM']),
                      (['MBM', 'HCM'], ['HCM', 'MBM'])]:
    for buff_count in (0, 1, 3):
        lua = fixture(owners, active)
        lua.globals().buff_count = buff_count
        lua.execute('for i=1,buff_count do add_native_buff(i)end;remove_unit();assert(deleted_buffs==buff_count);finish_all();finish_all()')
        cases += 1

# Removing the last buff from a live enemy must preserve DIY updates. The first
# manager finishing must not disable updates still needed by the second manager.
lua = fixture(['HCM', 'MBM'], ['HCM', 'MBM'])
lua.execute(r'''
add_native_buff(1);ext:_remove_buff(1)
assert(update_list[u]==ext and ext._update_enabled)
system:update({},.016,1);assert(update_calls==1)
apis[1].finish();assert(update_list[u]==ext)
system:update({},.016,2);assert(update_calls==2)
apis[2].finish();assert(update_list[u]==nil and not ext._update_enabled)
apis[1].finish();apis[2].finish()
-- A subsequent mission reuses the hooks and registers live enemies normally.
apis[1].update();assert(update_list[u]==ext and ext._update_enabled)
add_native_buff(2);remove_unit();assert(deleted_buffs==2);finish_all()
''')

# A real native buff retains its own update subscription when DIY finishes.
lua = fixture(['HCM', 'MBM'], ['HCM'])
lua.execute(r'''
add_native_buff(1);finish_all()
assert(update_list[u]==ext and ext._update_enabled)
ext:_remove_buff(1);assert(update_list[u]==nil and not ext._update_enabled)
remove_unit()
''')

# Robust cleanup also ignores an already-deleted legacy reference even when its
# unit still appears alive. Do not invoke methods on a replaced/deleted extension.
lua = fixture(['HCM'], ['HCM'])
lua.execute(r'''
remove_unit();local before=stats_calls
ALIVE[u]=true;ext._diy_minion_destroying=nil
shared._diy_minion_updates.owned[ext]=true
finish_all();assert(stats_calls==before and next(shared._diy_minion_updates.owned)==nil)
''')

# Native red-stimm scripts use the game's buff system without a DIY overlay.
# Exercise the actual installed stat callback; dynamic/player effects still work.
lua = fixture(['HCM'], [])
lua.execute(r'''
mods.HCM.test_authority=true
ext._buff_context={breed={breed_type='minion'}}
local reads=0
engines.HCM.effects=function()reads=reads+1;return {stats={}}end
for i=1,1000 do mods.HCM.stat_callback(ext)end
assert(reads==0 and not mods.HCM.effect_applies)
engines.HCM.needs_minion_updates=function()return true end
mods.HCM.stat_callback(ext);assert(reads==1 and mods.HCM.effect_applies==1)
engines.HCM.needs_minion_updates=function()return false end
ext._buff_context.breed.breed_type='player';engines.HCM.now=1
mods.HCM.stat_callback(ext);assert(reads==2 and mods.HCM.effect_applies==2)
''')

# Unit-local Studio passives register only their chosen extension. They do not
# activate a provider-wide scan, and two managers retain separate ownership.
lua = fixture(['HCM', 'MBM'], [])
lua.execute(r'''
local scans=0
Managers.state.minion_spawn.spawned_minions=function()scans=scans+1;return {u}end
apis[1].unit_scope_changed(u);apis[2].unit_scope_changed(u)
assert(scans==0 and update_list[u]==ext)
assert(not shared._diy_minion_updates.providers.HCM and not shared._diy_minion_updates.providers.MBM)
add_native_buff(1);ext:_remove_buff(1)
assert(update_list[u]==ext)
apis[1].finish();assert(update_list[u]==ext)
apis[2].finish();assert(update_list[u]==nil)
remove_unit();finish_all()
''')

# New native update reasons belong to their own owners. DIY must release and
# restore only the native no-buffs reason, even while another owner pauses it.
lua = fixture(['HCM'], [])
lua.execute(r'''
system:disable_update_function(u,'update','external_pause')
apis[1].unit_scope_changed(u)
local reasons=system._disable_reasons.MinionBuffExtension.update[u]
assert(reasons.external_pause and not reasons.__default_disable_reason__)
assert(update_list[u]==nil,'DIY must not override another owner\'s pause')
apis[1].finish()
reasons=system._disable_reasons.MinionBuffExtension.update[u]
assert(reasons.external_pause and reasons.__default_disable_reason__)
system:enable_update_function(u,'update','external_pause')
assert(update_list[u]==nil,'Empty minions remain disabled after external resume')
add_native_buff(1);assert(update_list[u]==ext)
ext:_remove_buff(1);assert(update_list[u]==nil)
remove_unit();finish_all()
''')

# Exercise native construction, not only a preconstructed extension. The base
# constructor's engine dependencies are stubbed; native MinionBuff.init,
# on_add_extension, registration and proc-table allocation remain real.
for owners, pause_in_add in [(owners, pause) for owners in (['HCM'], ['HCM', 'MBM'], ['MBM', 'HCM']) for pause in (False, True)]:
    lua = fixture(owners, owners, pause_during_add=pause_in_add)
    lua.globals().pause_in_add = pause_in_add
    lua.execute(r'''
remove_unit()
local Native=modules['scripts/extension_systems/buff/minion_buff_extension']
local Base=modules['scripts/extension_systems/buff/buff_extension_base']
local original_init=Base.init
Base.init=function(self,context,unit)
    self._unit=unit;self._is_server=true;self._is_hub=true
    self._update_enabled=false;self._buffs={};self._buffs_by_index={}
    self._num_params_table_in_use=0;self._param_tables_start_index_reference=1
    self._proc_event_param_tables={}
    self._update_stat_buffs_and_keywords=function()stats_calls=stats_calls+1 end
end
system._extension_init_context={owner_system=system,is_server=true}
ScriptUnit.add_extension=function(context,unit,name,alias,init_data)
    assert(name=='MinionBuffExtension' and alias=='buff_system')
    local created=Native:new(context,unit,init_data)
    assert(system._unit_to_extension_map[unit]==nil)
    assert(not created._update_enabled,'Init must wait for native registration')
    assert(created:request_proc_event_param_table()==nil)
    unit.ext=created;return created
end
local fresh={};ALIVE[fresh]=true
local created=system:on_add_extension({},fresh,'MinionBuffExtension',{})
Base.init=original_init
assert(system._unit_to_extension_map[fresh]==created)
assert(created._update_enabled and (pause_in_add and update_list[fresh]==nil or not pause_in_add and update_list[fresh]==created))
-- A spawn callback can request a proc before the next DIY update tick.
assert(type(created:request_proc_event_param_table())=='table')
system:disable_update_function(fresh,'update','spawn_pause')
system:register_extension_update(fresh,'MinionBuffExtension',created)
local reasons=system._disable_reasons.MinionBuffExtension.update[fresh]
assert(reasons.spawn_pause and not reasons.__default_disable_reason__)
assert(update_list[fresh]==nil and created._update_enabled)
system:register_extension_update(fresh,'MinionBuffExtension',created)
reasons=system._disable_reasons.MinionBuffExtension.update[fresh]
assert(reasons.spawn_pause and not reasons.__default_disable_reason__)
system:enable_update_function(fresh,'update','spawn_pause')
if pause_in_add then
    assert(update_list[fresh]==nil,'The pause present before HCM construction callback must survive')
    system:enable_update_function(fresh,'update','add_pause')
end
assert(update_list[fresh]==created,'Releasing the construction pause must resume DIY updates')
system:register_extension_update(fresh,'MinionBuffExtension',created)
local count=0;for _ in pairs(update_list)do count=count+1 end
assert(count==1 and update_list[fresh]==created)
system:on_remove_extension(fresh,'MinionBuffExtension')
assert(rawget(created,'__deleted') and update_list[fresh]==nil)
ALIVE[fresh]=nil;finish_all()
''')

# A live stale reference must not disable or rebuild a replacement extension
# mapped to the same unit during cleanup.
lua = fixture(['HCM'], ['HCM'])
lua.execute(r'''
local replacement={_unit=u,_update_enabled=true}
system._unit_to_extension_map[u]=replacement;update_list[u]=replacement
local before=stats_calls
finish_all()
assert(stats_calls==before and update_list[u]==replacement and replacement._update_enabled)
assert(shared._diy_minion_updates.owned[ext]==nil)
system._unit_to_extension_map[u]=ext;update_list[u]=ext
remove_unit()
''')
print(f'PASS: {cases} native deletion cases; ownership, cleanup, mission reuse, external pause, construction/first proc and replaced extension; native-only scripts skip 1000 empty overlays; scoped passives perform zero global scans.')
