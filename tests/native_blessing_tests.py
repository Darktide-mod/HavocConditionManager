"""Exercise HCM registration against native Buff data and a protected lookup."""
from pathlib import Path
import argparse
import json
from project_env import PROJECT, GAME

work = Path(__file__).resolve().parent
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--source', type=Path, help='Reference module to check, for reproducing an older release.')
args = parser.parse_args()
module = args.source or PROJECT / 'src/HavocConditionManager/scripts/mods/HavocConditionManager/reference_conditions.lua'
bootstrap = (work / 'harness.py').read_text(encoding='utf-8').split(
    "load_mod('HavocConditionManager/scripts/mods/HavocConditionManager/reference_conditions')", 1)[0]
native_source = (GAME / 'scripts/settings/buff/mutator_buff_templates.lua').read_text(encoding='utf-8')
native_table = native_source.split('templates.mutator_minion_nurgle_blessing_tougher = ', 1)[1].split('\nlocal CORRUPTION_DAMAGE_TYPE', 1)[0]
reports = []

for enabled in (True, False):
    for order in ('hcm_first', 'other_first'):
        env = {'__file__': str(work / 'harness.py')}
        exec(compile(bootstrap, 'native_blessing_bootstrap', 'exec'), env)
        L, cache, tbl = env['L'], env['cache'], env['tbl']
        L.globals().buff_settings = env['require']('scripts/settings/buff/buff_settings')
        native_buff = L.execute('''
local buff_keywords, buff_targets = buff_settings.keywords, buff_settings.targets
local buff_stat_buffs, minion_effects_priorities = buff_settings.stat_buffs, buff_settings.minion_effects_priorities
return ''' + native_table)
        native_buff.name = 'mutator_minion_nurgle_blessing_tougher'
        buffs = cache['scripts/settings/buff/buff_templates']
        buffs[native_buff.name] = native_buff
        buffs.NON_PREDICTED[native_buff.name] = native_buff.name
        lookup = tbl(['vanilla_before', native_buff.name, 'vanilla_after'])
        env['init_lookup']('buff_templates', lookup)
        cache['scripts/network_lookup/network_lookup'].buff_templates = lookup
        L.globals().lookup, L.globals().buffs = lookup, buffs
        L.globals().mods.HavocConditionManager._enabled = enabled
        L.execute('''
function string.split(s, delimiter)
    local result, first = {}, 1
    while true do
        local last = s:find(delimiter, first, true)
        result[#result+1] = s:sub(first, last and last-1 or #s)
        if not last then return result end
        first = last + #delimiter
    end
end
function equal(a, b)
    if type(a) ~= type(b) then return false end
    if type(a) ~= "table" then return a == b end
    for k,v in pairs(a) do if not equal(v,b[k]) then return false end end
    for k in pairs(b) do if a[k] == nil then return false end end
    return true
end
function register_other_mod()
    -- Same append rule used by custom-buff mods; no game-specific ID is assumed.
    for _,name in ipairs({"cwah_arc_chain", "cwah_arc_shock"}) do
        if not rawget(lookup,name) then
            local id = #lookup+1
            lookup[id], lookup[name] = name, id
        end
    end
end
original_buff = buffs.mutator_minion_nurgle_blessing_tougher
original_mutator = require("scripts/settings/mutator/mutator_templates").mutator_minion_nurgle_blessing
original_mutator_copy = table.clone_instance(original_mutator)
buffs_before = table.clone_instance(buffs)
''')
        if order == 'other_first':
            L.execute('register_other_mod()')
        L.execute('lookup_before=table.clone_instance(lookup)')
        L.execute(module.read_text(encoding='utf-8-sig'), name='@' + str(module))
        L.execute('''
assert(equal(lookup,lookup_before), "HCM changed the Buff network lookup")
assert(equal(buffs,buffs_before), "HCM changed or added a Buff template")
assert(buffs.mutator_minion_nurgle_blessing_tougher == original_buff)
assert(not rawget(lookup,"more_havoc_nurgle_blessing_tougher"))
assert(not buffs.more_havoc_nurgle_blessing_tougher)
local mutators = require("scripts/settings/mutator/mutator_templates")
local custom = mutators.more_havoc_nurgle_blessing
assert(custom.random_spawn_buff_templates.buffs[1] == original_buff.name)
assert(lookup[lookup[custom.random_spawn_buff_templates.buffs[1]]] == original_buff.name)
assert(custom.random_spawn_buff_templates.breed_chances ~= original_mutator.random_spawn_buff_templates.breed_chances)
assert(equal(original_mutator,original_mutator_copy))
local H=mods.HavocConditionManager
local base_chances=original_mutator.random_spawn_buff_templates.breed_chances
local function check(rank,selected,scaling)
    H:set("nurgle_blessing_rank_scaling",scaling)
    local context={havoc_data="cm_habs;"..rank..";;;"..(selected and "more_havoc_nurgle_blessing" or "")..";;"}
    assert(H.prepare_reference_conditions(context)==context)
    for name,chance in pairs(base_chances) do
        local expected = selected and scaling and rank>0 and chance>0
            and math.clamp(chance+0.005*rank,0,1) or chance
        assert(math.abs(custom.random_spawn_buff_templates.breed_chances[name]-expected)<1e-10,name)
    end
    assert(equal(original_mutator,original_mutator_copy),"Native spawn probabilities changed")
    assert(equal(buffs,buffs_before),"Buff effect changed during rank scaling")
    assert(equal(lookup,lookup_before),"Mission preparation changed Buff IDs")
end
check(40,true,false)
check(40,true,true)
check(1,true,true)
check(0,true,true)
check(1000,true,true)
check(40,false,true)
check(40,true,true)
check(40,true,false)
''')
        # Rebind an existing circumstance, including one pointing to the old copy.
        L.execute('''
require("scripts/settings/mutator/mutator_templates").more_havoc_nurgle_blessing
    .random_spawn_buff_templates.buffs={"more_havoc_nurgle_blessing_tougher"}
''')
        L.execute(module.read_text(encoding='utf-8-sig'), name='@' + str(module))
        L.execute('''
assert(require("scripts/settings/mutator/mutator_templates").more_havoc_nurgle_blessing
    .random_spawn_buff_templates.buffs[1] == original_buff.name)
assert(equal(lookup,lookup_before))
assert(equal(buffs,buffs_before))
assert(equal(original_mutator,original_mutator_copy))
register_other_mod()
assert(lookup.cwah_arc_chain==4 and lookup.cwah_arc_shock==5)
assert(lookup.mutator_minion_nurgle_blessing_tougher==2)
''')
        reports.append({'framework_enabled': enabled, 'load_order': order,
                        'buff_lookup_unchanged': True, 'native_buff_unchanged': True,
                        'rank_scaling_and_reset': 'passed', 'reload': 'passed',
                        'other_mod_ids': {'cwah_arc_chain': 4, 'cwah_arc_shock': 5}})

print(json.dumps({'status': 'passed', 'cases': reports}, ensure_ascii=False, indent=2))
