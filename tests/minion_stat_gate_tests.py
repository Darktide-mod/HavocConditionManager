"""Test the stat-hook class boundary; optionally compare identical mocked batches."""
import argparse
import hashlib
import json
import math
import platform
import re
import statistics
import subprocess
import sys
from time import perf_counter_ns

from project_env import CHECKS, GAME, PROJECT, SOURCES
import lupa
from lupa.luajit21 import LuaRuntime

ROOT = SOURCES / 'HavocConditionManager/scripts/mods/HavocConditionManager'
RELATIVE = 'src/HavocConditionManager/scripts/mods/HavocConditionManager/diy/diy_game.lua'
CURRENT = (PROJECT / RELATIVE).read_text(encoding='utf-8-sig')


def fixture(source, client_callback=True):
    lua = LuaRuntime(unpack_returned_tuples=True)
    lua.execute(r'''
modules={};require=function(path)return modules[path] or {}end
table.clear=function(t)for k in pairs(t)do t[k]=nil end end
counts={};instrument=true;role='host';character='character1'
function count(key)if instrument then counts[key]=(counts[key] or 0)+1 end end
function reset_counts()counts={}end
shared={};ALIVE={};HEALTH_ALIVE=ALIVE
local realms={is_enabled=function()return true end,_session={
    is_active_host=function()return role=='host' end,is_active_client=function()return role=='client' end}}
get_mod=function(name)return name=='DMF' and shared or name=='Realms' and realms end
Managers={state={game_session={}},connection={
    is_host=function()return role=='host' end,is_client=function()return role=='client' end,
    host=function()return 'HOST' end},player={}}
local_player={character_id=function()count('character');return character end,
    peer_id=function()return 'local' end,local_player_id=function()return 1 end}
function Managers.player:local_player_safe()count('local_player');return local_player end
function Managers.player:human_players()return {local_player}end
function native_stats(self)
    count('native');table.clear(self._stat_buffs);table.clear(self._keywords)
    self._stat_buffs.power=11;self._keywords.native=true
end
Player={_update_stat_buffs_and_keywords=native_stats,add_proc_event=function()end}
Minion={_update_stat_buffs_and_keywords=native_stats,add_proc_event=function()end,
    init=function()end,destroy=function()end,_on_remove_buff=function()end}
modules['scripts/extension_systems/buff/player_unit_buff_extension']=Player
modules['scripts/extension_systems/buff/minion_buff_extension']=Minion
local stored={};mod={};require_callbacks={}
function mod:persistent_table(name)stored[name]=stored[name] or {};return stored[name]end
function mod:is_enabled()return true end
function mod:hook_require(path,cb)
    require_callbacks[path]=require_callbacks[path] or {}
    table.insert(require_callbacks[path],cb)
    if modules[path] then cb(modules[path])end
end
function revisit_require(path)for _,cb in ipairs(require_callbacks[path])do cb(modules[path])end end
function mod:hook_safe(cls,name,cb)
    local original=assert(cls[name],name)
    cls[name]=function(...)local result=original(...);cb(...);return result end
end
function mod:hook(cls,name,cb)
    local original=assert(cls[name],name);cls[name]=function(...)return cb(original,...)end
end
ScriptUnit={has_extension=function(unit,name)
    if name=='buff_system' then return unit.ext end
    if name=='unit_data_system' then return {breed=function()return unit.breed end}end
end}
catalog={stats={power='value'},keywords={diy=true,remote=true},events={}}
function make_unit(kind,metadata)
    local unit={breed={breed_type=kind,name=kind,tags={}}};ALIVE[unit]=true
    local cls=kind=='player' and Player or Minion
    unit.ext=setmetatable({_unit=unit,_buffs={true},_update_enabled=true,
        _owner_system={enable_update_function=function()end},
        _buff_context=metadata and {breed=unit.breed} or nil,_stat_buffs={},_keywords={}}, {__index=cls})
    return unit
end
minion=make_unit('minion',true);player=make_unit('player',true)
local_player.player_unit=player
''')
    lua.globals().E = lua.execute((ROOT / 'diy/diy_engine.lua').read_text(encoding='utf-8-sig'))
    lua.globals().N = lua.execute((ROOT / 'diy/diy_network.lua').read_text(encoding='utf-8-sig'))
    lua.globals().G = lua.execute(source)
    lua.globals().client_callback = client_callback
    lua.execute(r'''
local context=N.context
N.context=function()count('context');return context()end
network=N.new(mod,catalog,{context=N.context,local_player=N.local_player,players=N.players,realms=N.realms})
local apply=E.apply
E.apply=function(...)count('apply');return apply(...)end
local options={name='HCM',skip_attack_report=true,context=function()return {}end,
    authority=function()count('authority');return role=='host' end,
    engine=function()count('engine');return engine end}
if client_callback then options.client_effects=function(unit)count('client_effects');return network.effects(unit)end end
api=G.new(mod,catalog,E,options)
document={id='gate',entries={
    {id='native',enabled=true,targets={kind='minions'},rules={},conditions={}},
    {id='minions',enabled=true,targets={kind='minions'},rules={},conditions={},passive={stats={power=3},keywords={'diy'}}},
    {id='players',enabled=true,targets={kind='players'},rules={},conditions={},passive={stats={power=5},keywords={'diy'}}}}}
function new_engine(selection)
    engine=E.new(document,catalog,api,1)
    local effects=engine.effects
    engine.effects=function(unit)count('effects');return effects(unit)end
    engine.set_global(selection or {});api.invalidate();return engine
end
function batch(unit,n)for i=1,n do unit.ext:_update_stat_buffs_and_keywords(0)end end
function state_packet()
    network.effects(player) -- establish native context/nonce before receiving
    network.receive('host',{protocol=1,kind='state',nonce=network.nonce,character=character,
        sequence=network.last_sequence+1,status='ready',effects={stats={power=7},keywords={'remote'}}})
end
function check_stats(unit,power,keyword)
    assert(unit.ext._stat_buffs.power==power, 'stat result changed')
    assert(unit.ext._keywords.native, 'native keyword lost')
    assert((unit.ext._keywords.diy or unit.ext._keywords.remote or false)==(keyword or false))
end
''')
    return lua


CASES = [
    ('nil engine', "engine=nil;reset_counts();batch(minion,1000);check_stats(minion,11)", 1000),
    ('native only', "new_engine({'native'});reset_counts();batch(minion,1000);check_stats(minion,11);assert(not counts.effects and not counts.apply)", 1000),
    ('global minion overlay/cache', "new_engine({'minions'});reset_counts();batch(minion,1000);check_stats(minion,14,true);assert(counts.effects==1 and counts.apply==1000)", 1000),
    ('missing breed context', "new_engine({'minions'});minion.ext._buff_context=nil;reset_counts();batch(minion,1000);check_stats(minion,14,true)", 1000),
    ('scoped minion first callback', "new_engine({});engine.set_passive_scope(minion,{minions=true});api.unit_scope_changed(minion);reset_counts();batch(minion,1000);check_stats(minion,14,true);assert(counts.effects==1 and counts.apply==1000)", 1000),
    ('host player', "new_engine({'players'});reset_counts();batch(player,1000);check_stats(player,16,true);assert(counts.effects==1 and counts.apply==1000)", None),
    ('client local player', "role='client';engine=nil;state_packet();reset_counts();batch(player,1000);check_stats(player,18,true);assert(counts.apply==1000 and not counts.engine)", None),
    ('client minion', "role='client';engine=nil;state_packet();reset_counts();batch(minion,1000);check_stats(minion,11);assert(not counts.apply)", 1000),
    ('client remote player', "role='client';engine=nil;state_packet();remote=make_unit('player',true);reset_counts();batch(remote,1000);check_stats(remote,11);assert(not counts.apply)", None),
    ('optional Realms absent', "get_mod=function(name)return name=='DMF' and shared end;role='local';engine=nil;reset_counts();batch(minion,1000);check_stats(minion,11)", 1000),
]


def regressions(source, gated):
    outcomes = {}
    for name, setup, minion_callbacks in CASES:
        lua = fixture(source)
        lua.execute(setup)
        counters = dict(lua.globals().counts.items())
        probes = 0 if gated and minion_callbacks else 1000
        assert counters.get('client_effects', 0) == probes, (name, counters)
        assert counters.get('context', 0) == probes, (name, counters)
        assert counters.get('local_player', 0) == probes * 2, (name, counters)
        assert counters.get('character', 0) == probes, (name, counters)
        assert counters['native'] == 1000
        outcomes[name] = counters

    # Exercise real Engine revisions, clock, per-unit scope and identity; no new
    # persistent network/authority cache is introduced by this optimization.
    lua = fixture(source)
    lua.execute(r'''
new_engine({'minions'});batch(minion,1);check_stats(minion,14,true)
reset_counts();batch(minion,10);assert(not counts.effects and counts.apply==10)
engine.set_global({});batch(minion,1);check_stats(minion,11)
engine.set_global({'minions'});batch(minion,1);check_stats(minion,14,true)
reset_counts();engine.tick(.1);batch(minion,1);assert(counts.effects==1)
reset_counts();api.invalidate();batch(minion,1);assert(counts.effects==1)
new_engine({});engine.set_passive_scope(minion,{minions=true});api.unit_scope_changed(minion)
batch(minion,1);check_stats(minion,14,true)
engine.set_passive_scope(minion,nil);batch(minion,1);check_stats(minion,11)
new_engine({'minions'});batch(minion,1);check_stats(minion,14,true)
engine.finish();batch(minion,1);check_stats(minion,11)
api.finish();new_engine({'native'});batch(minion,1);check_stats(minion,11)
new_engine({'minions'});batch(minion,1);check_stats(minion,14,true)
role='client';engine=nil;state_packet();batch(player,1);check_stats(player,18,true)
local old=player;player=make_unit('player',true);local_player.player_unit=player
batch(old,1);check_stats(old,11);batch(player,1);check_stats(player,18,true)
character='character2';batch(player,1);check_stats(player,11)
state_packet();batch(player,1);check_stats(player,18,true)
network.update(3.01);batch(player,1);check_stats(player,11)
state_packet();Managers.state.game_session={};batch(player,1);check_stats(player,11)
state_packet();network.finish();batch(player,1);check_stats(player,11)
''')
    # Repeated require stays idempotent on the existing native class. A fresh
    # fixture separately models a new adapter/class set, not a live DMF reload.
    lua = fixture(source)
    lua.execute("""
new_engine({'minions','players'})
revisit_require('scripts/extension_systems/buff/minion_buff_extension')
revisit_require('scripts/extension_systems/buff/player_unit_buff_extension')
reset_counts();batch(minion,1);check_stats(minion,14,true);assert(counts.apply==1)
reset_counts();batch(player,1);check_stats(player,16,true);assert(counts.apply==1 and counts.client_effects==1)
""")
    lua = fixture(source, client_callback=False)
    lua.execute("new_engine({'minions','players'});reset_counts();batch(minion,1);check_stats(minion,14,true);batch(player,1);check_stats(player,16,true);assert(not counts.client_effects and counts.apply==2)")
    return outcomes


def summary(samples):
    ordered = sorted(samples)
    return {'median_ms': statistics.median(ordered), 'p95_ms': ordered[math.ceil(len(ordered) * .95) - 1],
            'samples_ms': samples}


def comparison(baseline_source, baseline_ref):
    before = regressions(baseline_source, False)
    after = regressions(CURRENT, True)
    for name in before:
        for key in ('native', 'apply', 'effects', 'authority', 'engine'):
            assert before[name].get(key, 0) == after[name].get(key, 0), (name, key)
    report = {'kind': 'mocked Lua stat-callback microbenchmark; no gameplay/frame-time/FPS measurement',
              'environment': {'python': sys.version, 'platform': platform.platform(), 'lupa': lupa.__version__,
                              'lua': str(LuaRuntime().eval('_VERSION')), 'luajit': str(LuaRuntime().eval('jit.version')),
                              'source_head': subprocess.check_output(
                                  ['git', '-c', 'safe.directory=' + GAME.as_posix(), 'rev-parse', 'HEAD'], cwd=GAME, text=True).strip()},
              'baseline_ref': baseline_ref,
              'baseline_sha256': hashlib.sha256(baseline_source.encode()).hexdigest(),
              'candidate_sha256': hashlib.sha256(CURRENT.encode()).hexdigest(),
              'workload': 'One fixed minion, 1000 native stat resets + HCM callbacks, fixed engine clock; same fixture for both versions',
              'semantic_call_counts': {'before': before, 'after': after}, 'timings': {}}
    for name, selection in [('nil_engine', None), ('native_only', ['native']), ('active_passive', ['minions'])]:
        runtimes = [fixture(baseline_source), fixture(CURRENT)]
        for lua in runtimes:
            if selection is not None:
                lua.globals().selection = lua.table_from(selection)
                lua.execute('new_engine(selection)')
            lua.execute('instrument=false;batch(minion,500);collectgarbage("collect")')
        samples = [[], []]
        # Alternating order reduces ordering bias; counters are disabled for
        # timing, the actual Network effects/context and Engine functions remain.
        for repetition in range(30):
            for index in ([0, 1] if repetition % 2 == 0 else [1, 0]):
                lua = runtimes[index]
                batch = lua.globals().batch
                unit = lua.globals().minion
                started = perf_counter_ns();batch(unit, 1000)
                samples[index].append((perf_counter_ns() - started) / 1_000_000)
        allocations = []
        for lua in runtimes:
            allocations.append(lua.execute('collectgarbage("collect");collectgarbage("stop");local kb=collectgarbage("count");batch(minion,1000);local delta=collectgarbage("count")-kb;collectgarbage("restart");return delta'))
        report['timings'][name] = {'before': summary(samples[0]), 'after': summary(samples[1]),
                                  'lua_gc_heap_growth_kib_1000_callbacks': {'before': allocations[0], 'after': allocations[1]},
                                  'median_change_percent': (statistics.median(samples[1]) / statistics.median(samples[0]) - 1) * 100}
    path = CHECKS / 'minion-stat-gate-comparison.json'
    path.write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print('Mocked comparison saved: ' + str(path))
    for name, data in report['timings'].items():
        print(f"{name}: median {data['before']['median_ms']:.4f} -> {data['after']['median_ms']:.4f} ms/1000 callbacks; "
              f"p95 {data['before']['p95_ms']:.4f} -> {data['after']['p95_ms']:.4f} ms; {data['median_change_percent']:+.1f}%")


parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--baseline-ref', help='Full/abbreviated hexadecimal compatibility commit for an optional mocked comparison')
args = parser.parse_args()
regressions(CURRENT, True)
print('PASS: 10 class/authority/overlay cases (1000 callbacks each), scope/settings/time/engine changes, respawn, character/mission/timeout, repeated require, omitted client callback and mocked reload boundaries.')
if args.baseline_ref:
    if not re.fullmatch(r'[0-9a-fA-F]{7,40}', args.baseline_ref):
        parser.error('--baseline-ref must be a hexadecimal commit ID')
    baseline = subprocess.check_output(['git', 'show', args.baseline_ref + ':' + RELATIVE], cwd=PROJECT).decode('utf-8-sig')
    comparison(baseline, args.baseline_ref)
