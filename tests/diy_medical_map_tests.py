"""Execute the custom package against native station and pickup methods.

Engine graphics/network/entity services are fixtures; this is not an in-game test.
Run with the bundled Python and DARKTIDE_TEST_RUNTIME when necessary.
"""
from pathlib import Path
import json
import os
import re
import subprocess
import sys

PROJECT = Path(__file__).resolve().parents[1]
ROOT = PROJECT.parents[1]
GAME = ROOT / 'dev-support/game-source'
sys.path.insert(0, os.environ.get('DARKTIDE_TEST_RUNTIME', str(ROOT / 'dev-support/test-runtime-py312')))
from lupa.luajit21 import LuaRuntime

PACKAGE = PROJECT / 'custom-packages/starter-conditions-no_healing'
RUNTIME = Path(os.environ.get('HCM_DIY_RUNTIME', str(ROOT.parents[1] / 'mods/HavocConditionManager/scripts/mods/HavocConditionManager/diy')))


def native(path):
    return subprocess.check_output(['git', '-c', 'gc.auto=0', 'show', 'HEAD:' + path], cwd=GAME).decode('utf-8-sig')


L = LuaRuntime(unpack_returned_tuples=True)
L.execute(r'''
modules = {}
local original_require = require
require = function(path)
    if path:sub(1, 8) == 'scripts/' then return modules[path] or {} end
    return original_require(path)
end
class = function(name, parent)
    local result = { super = parent and _G[parent] or {} }
    result.__index = result
    _G[name] = result
    return result
end
math.clamp = function(v, lo, hi) return math.max(lo, math.min(hi, v)) end
math.lerp = function(a, b, t) return a + (b-a)*t end
table.index_of = function(t, value) for i,v in ipairs(t) do if v == value then return i end end return -1 end
table.swap_delete = function(t, i) t[i] = t[#t]; t[#t] = nil end
table.set = function(t) local out = {}; for _,v in ipairs(t) do out[v] = true end; return out end
table.clear = function(t) for k in pairs(t) do t[k] = nil end end
ALIVE = setmetatable({}, { __index = function(_, u) return u and u.alive ~= false end })
Unit = { alive = function(u) return ALIVE[u] end, get_data = function(u, key) return u[key] end,
    set_scalar_for_materials = function() end, light = function() return {} end, flow_event = function() end }
Light = { set_enabled = function() end }
ScriptUnit = { extension = function(u, name) return assert(u.extensions[name], name) end,
    has_extension = function(u, name) return u.extensions[name] end }
Log = { error = function(...) error('native pickup bookkeeping error') end }
NetworkConstants = { invalid_game_object_id = 0, invalid_level_unit_id = 0 }
calls = { rpc = {}, late = {}, spawned = {}, deleted = {}, hooks = 0 }
RPC = { rpc_health_station_despawn = function(channel, id) calls.late[#calls.late+1] = {channel, id} end,
    rpc_health_station_hot_join = function() end }
local serial = 0
local spawner = {
    spawn_network_unit = function(_, name, template, position, rotation, material, settings)
        serial = serial + 1
        local unit = {id = 1000+serial, alive = true, pickup_type = settings.name}
        calls.spawned[#calls.spawned+1] = unit
        return unit, unit.id
    end,
    mark_for_deletion = function(_, u) u.marked = true; calls.deleted[u] = true end,
    is_marked_for_deletion = function(_, u) return u.marked == true end,
    level_index = function(_, u) return u.id end,
    game_object_id = function(_, u) return u.id end,
    game_object_id_or_level_index = function(_, u) return false, u.id end,
}
systems = {}
Managers = { state = { unit_spawner = spawner, game_session = {
    send_rpc_clients = function(_, name, ...) calls.rpc[#calls.rpc+1] = {name, ...} end },
    circumstance = { mission_overrides = function() return {} end },
    game_mode = { game_mode_name = function() return 'coop_complete_objective' end },
    out_of_bounds = { register_soft_oob_unit = function() end, unregister_soft_oob_unit = function() end },
    extension = { has_system = function(_, name) return systems[name] ~= nil end,
        system = function(_, name) return systems[name] end } } }
mod = { authority = true, has_local_gameplay_authority = function() return mod.authority end }
function mod:hook(class, method, handler)
    assert(type(class[method]) == 'function', method)
    calls.hooks = calls.hooks + 1
    local original = class[method]
    class[method] = function(...) return handler(original, ...) end
end
get_mod = function(name) assert(name == 'HavocConditionManager'); return mod end
Mods = { lua = { loadstring = loadstring, setfenv = setfenv, debug = debug } }
''')

L.globals().Station = L.execute(native('scripts/extension_systems/health_station/health_station_extension.lua'))
L.globals().modules['scripts/extension_systems/health_station/health_station_extension'] = L.globals().Station
L.globals().Stations = L.execute(native('scripts/extension_systems/health_station/health_station_system.lua'))
L.globals().modules['scripts/extension_systems/health_station/health_station_system'] = L.globals().Stations
L.execute('PickupSystem = class("PickupSystem"); PICKUPS_BY_NAME = {}; PickupSettings = {skip_group={soft_cap=99,hard_cap=100}}')
source = native('scripts/extension_systems/pickups/pickup_system.lua')
for method in ('_skip_group_blocks', 'spawn_pickup', 'player_spawn_pickup', 'despawn_pickup', 'dropped'):
    L.execute(re.search(r'^PickupSystem\.' + method + r' = function .*?^end\s*$', source, re.M | re.S)[0])
L.execute(r'''
PickupSystem._reset_retained_pickup_charges = function() end
modules['scripts/extension_systems/pickups/pickup_system'] = PickupSystem
for _,name in ipairs({'medical_crate_pocketable','syringe_corruption_pocketable','syringe_power_boost_pocketable',
    'syringe_speed_boost_pocketable','syringe_ability_boost_pocketable','small_clip','ammo_cache_pocketable',
    'battery_01_luggable','battery_02_luggable'}) do
    PICKUPS_BY_NAME[name] = { name=name, unit_name=name, unit_template_name='pickup' }
end
pickups = setmetatable({_is_server=true, _spawned_pickups={}, _dropped_pickups={}, _pickup_to_owner_player={},
    _pickup_to_owner={}, _pickup_to_interactors={}, _pickup_to_spawner={}, _unit_to_skip_group={}, _skip_group_count={}}, PickupSystem)
systems.pickup_system = pickups
stations = setmetatable({_is_server=true, _unit_to_extension_map={}}, Stations)
stations.unit_to_extension_map = function(self) return self._unit_to_extension_map end
systems.health_station_system = stations
Pocketable = {}
for _,name in ipairs({'drop_pocketable','equip_pocketable'}) do
    Pocketable[name] = function(pickup_name, fail)
        if fail then error('transfer failed') end
        local unit, id = pickups:spawn_pickup(pickup_name, 0, 0)
        pickups:dropped(unit)
        return unit, nil, id
    end
end
modules['scripts/utilities/pocketable'] = Pocketable
local next_station = 0
function make_station(mode, pool, plug, initialized, plugged)
    next_station = next_station + 1
    local unit = {id=next_station, alive=true, extensions={}}
    local ext = setmetatable({}, Station)
    ext:init({is_server=true}, unit)
    unit.extensions.animation_system = { anim_event = function(_, event) unit.animation = event end }
    unit.extensions.point_of_interest_system = { set_tag = function(_, tag) unit.tag = tag end }
    unit.extensions.pickup_system = {
        spawn_item = function() return pickups:spawn_pickup('battery_01_luggable', 0, 0) end,
        despawn_item = function(_, battery) pickups:despawn_pickup(battery) end,
    }
    ext:setup_from_component(3, 0, pool, 'socket', mode)
    ext._plug_from_distribution = plug
    ext._distributed_charges = plug and 2 or 4
    ext._spawn_socket = function(self)
        self._socket_unit = {id=unit.id+500, alive=true}
        self._luggable_socket_extension = { is_occupied=function() return self.battery ~= nil end,
            socketed_unit=function() return self.battery end,
            socket_luggable=function(_, battery) self.battery=battery end,
            is_overlapping_with_luggable=function() return false end }
    end
    ext._teleport_battery_to_socket = function() end
    stations._unit_to_extension_map[unit] = ext
    if initialized then
        ext:_spawn_socket()
        ext:spawn_battery()
        if plugged then ext:socket_luggable(ext._spawned_battery_unit) end
        ext._first_frame_setup = true
        ext:set_charge_amount(plugged and 3 or 0)
    end
    return ext
end
existing_plugged = make_station('plugged',false,false,true,true)
existing_loose = make_station('pickup_location',false,false,true,false)
loose_battery = existing_loose:spawned_battery_unit()
quest_battery = pickups:spawn_pickup('battery_02_luggable',0,0)
existing_medkit = pickups:spawn_pickup('medical_crate_pocketable',0,0)
existing_medstimm = pickups:spawn_pickup('syringe_corruption_pocketable',0,0)
existing_ammo = pickups:spawn_pickup('small_clip',0,0)
carried_drop = pickups:player_spawn_pickup('medical_crate_pocketable',0,0,{},'player')
pickups:dropped(carried_drop)
''')

for alias, name in [('S','schema'),('C','codec'),('K','catalog'),('E','engine'),('P','packages'),('H','sha256'),('Scripts','scripts')]:
    L.globals()[alias] = L.execute((RUNTIME / f'diy_{name}.lua').read_text(encoding='utf-8'))
files = {p.relative_to(PACKAGE).as_posix(): p.read_text(encoding='utf-8') for p in PACKAGE.rglob('*') if p.is_file()}
L.globals().package_files = L.table_from(files)
L.execute(r'''
A = P.new(S,C,H)
package_checked = assert(A.validate(package_files,K,'conditions','starter-conditions-no_healing'))
assert(package_checked.document.entries[1].script and not package_checked.document.entries[1].passive)
snapshot = A.compose({['starter-conditions-no_healing']=package_checked}, K, 'conditions')
assert(#snapshot.document.entries == 1)
entry_id = snapshot.document.entries[1].id
native_api = {key=function() return 'u' end, info=function() return {kind='players'} end, alive=function() return true end,
    context=function() return {} end, units=function() return {} end, action=function() return true end,
    error=function(e) error(e) end}
function start_engine()
    local engine = Scripts.attach(E.new(snapshot.document,K,native_api,1),snapshot,
        {Schema=S,Packages=P,PackageAPI=A,Engine=E,native=native_api,catalog=K})
    engine.set_global({entry_id})
    return engine
end
engine = start_engine()
assert(existing_plugged:charge_amount() == 0 and existing_plugged:battery_in_slot())
assert(not existing_plugged._unit.marked and not existing_plugged:spawned_battery_unit().marked)
assert(existing_loose._unit.marked and loose_battery.marked)
assert(existing_medkit.marked and existing_medstimm.marked)
assert(not existing_ammo.marked and not quest_battery.marked and not carried_drop.marked)
assert(#engine.effects({}).keywords == 0, 'general healing must not be blocked')

local function first_frame(ext)
    ext:fixed_update(ext._unit,.1,1)
    engine.tick(.1)
end
new_plugged = make_station('plugged',false,false,false,false)
first_frame(new_plugged)
assert(new_plugged:battery_in_slot() and new_plugged:charge_amount()==0 and not new_plugged._unit.marked)
distributed_plugged = make_station('plugged_with_charge',true,true,false,false)
first_frame(distributed_plugged)
assert(distributed_plugged:battery_in_slot() and distributed_plugged:charge_amount()==0 and not distributed_plugged._unit.marked)
early_flow = make_station('plugged_with_charge',true,false,false,false)
early_flow._distributed_charges = nil
early_flow._plug_from_distribution = nil
early_flow:spawn_battery()
assert(early_flow:spawned_battery_unit()==nil)
early_flow:assign_distributed_charge(2,true)
first_frame(early_flow)
assert(early_flow:battery_in_slot() and early_flow:charge_amount()==0 and not early_flow._unit.marked)
for _,spec in ipairs({{'pickup_location',false,false},{'none',false,false},{'plugged_with_charge',true,false},
    {'pickup_location',true,true}}) do
    local ext = make_station(spec[1],spec[2],spec[3],false,false)
    local before = #calls.spawned
    first_frame(ext)
    assert(ext._unit.marked and #calls.spawned==before and ext:spawned_battery_unit()==nil)
    ext:spawn_battery()
    assert(#calls.spawned==before, 'component flow must not respawn a removed station battery')
end
-- The rule is initial placement/charges, not an interception of insertion or healing.
new_plugged:set_charge_amount(2)
first_frame(new_plugged)
assert(new_plugged:charge_amount()==2, 'do not continuously clamp later charge changes')
for _,name in ipairs({'medical_crate_pocketable','syringe_corruption_pocketable'}) do
    assert(pickups:spawn_pickup(name,0,0)==nil)
    assert(pickups:spawn_pickup(name,0,0,nil,nil,nil,{})==nil, 'DIY supplies also blocked')
end
for _,name in ipairs({'small_clip','ammo_cache_pocketable','syringe_power_boost_pocketable',
    'syringe_speed_boost_pocketable','syringe_ability_boost_pocketable','battery_01_luggable','battery_02_luggable'}) do
    assert(pickups:spawn_pickup(name,0,0), name)
end
assert(pickups:player_spawn_pickup('medical_crate_pocketable',0,0,{},'player'))
local dropped, middle, id = Pocketable.drop_pocketable('syringe_corruption_pocketable')
assert(dropped and middle==nil and id==dropped.id)
assert(Pocketable.equip_pocketable('medical_crate_pocketable'))
assert(not pcall(Pocketable.drop_pocketable,'medical_crate_pocketable',true))
assert(pickups:spawn_pickup('medical_crate_pocketable',0,0)==nil, 'failed transfer must release its exemption')
stations:hot_join_sync('peer','channel')
assert(#calls.late>=5, 'late joiners must also lose the removed level stations')
local hook_count = calls.hooks
mod.authority = false
assert(pickups:spawn_pickup('medical_crate_pocketable',0,0), 'no authority means no policy')
mod.authority = true
local session = Managers.state.game_session
Managers.state.game_session = {}
assert(pickups:spawn_pickup('medical_crate_pocketable',0,0), 'old session must not affect a new one')
Managers.state.game_session = session
engine.finish()
assert(mod._diy_medical_map_hooks_v1.current==nil)
assert(pickups:spawn_pickup('medical_crate_pocketable',0,0), 'finish restores normal generation')
ordinary = make_station('pickup_location',false,false,false,false)
ordinary:fixed_update(ordinary._unit,.1,1)
assert(ordinary:spawned_battery_unit() and not ordinary._unit.marked)
engine = start_engine()
assert(calls.hooks==hook_count, 'new mission must not stack DMF hooks')
assert(pickups:spawn_pickup('medical_crate_pocketable',0,0)==nil)
engine.finish()
''')

assert json.loads(files['definitions.json'])['entries'][0]['id'] == 'no_healing'
print('PASS: package/schema and real script loader; existing/new plugged stations remain empty; loose station/battery pairs removed; native battery flows, map supplies, player transfers, late join, authority/session guards, cleanup and next-mission hook reuse.')
