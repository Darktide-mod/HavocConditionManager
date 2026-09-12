"""Native template compiler contracts, using checked-out game data."""
from native_harness import *
import json
L.execute("""
assert(#A.entries>100 and #S.coarse==20)
local defaults=S.coarse_config()
local changed={}
local entries,fields,rules,compositions,pools=0,0,0,0,0
for _,entry in ipairs(A.entries) do
    entries=entries+1; fields=fields+#entry.items; rules=rules+#entry.targets
    local root,n,invalid=S.apply(entry.root,entry.family,defaults,nil,A.breeds)
    assert(root==entry.root and n==0 and #invalid==0,"Default identity: "..entry.id)
    local first=E.prepare(entry.root,entry.family)
    assert(first==entry.root,"Default runtime identity: "..entry.id)
    for _,item in ipairs(entry.items) do
        if item.kind=="composition" then compositions=compositions+1 end
        if item.kind=="pool" then pools=pools+1 end
    end
end
for _,d in ipairs(S.coarse) do
    local cfg=S.coarse_config(); cfg[d.id]=2
    local count=0
    for _,entry in ipairs(A.entries) do
        for _,item in ipairs(entry.items) do if not S.equal(S.scaled(item,entry.family,cfg),item.value) then count=count+1 end end
    end
    if d.id=="coordinated_load" then
        for _,entry in ipairs(A.entries) do local _,n=S.apply(entry.root,entry.family,cfg,nil,A.breeds,A.by_table);count=count+n end
    end
    changed[d.id]=count
    assert(count>0 or d.id=="event_budget","Coarse control has no consumers: "..d.id)
end
native_statistics={entries=entries,fields=fields,rule_targets=rules,compositions=compositions,pools=pools,coarse=changed}
""")
def plain(v):
    if hasattr(v,"items"): return {str(k):plain(x) for k,x in v.items()}
    return v
stats=plain(L.globals().native_statistics)
(CHECKS/"native-template-coverage.json").write_text(json.dumps(stats,ensure_ascii=False,indent=2),encoding="utf-8")
print(json.dumps(stats,ensure_ascii=False))
print("Native template defaults and 20 coarse control mappings: PASS")


L.execute("""
-- Exact fine values override coarse values; copying one path breaks aliases.
local shared={{name="chaos_poxwalker",amount={3,6}}}
local fake={horde_compositions={a={breeds=shared},b={breeds=shared}}}
local original=S.copy(fake); local cfg=S.coarse_config({horde_size=2})
local edited=S.apply(fake,"hordes",cfg,{["horde_compositions/a/breeds"]={{name="chaos_poxwalker",amount={1,2}}}},A.breeds)
assert(edited.horde_compositions.a.breeds[1].amount[2]==2)
assert(edited.horde_compositions.b.breeds[1].amount[2]==12)
assert(S.equal(fake,original))
local special
for _,e in ipairs(A.entries) do if e.family=="specials" and e.fields.max_alive_specials then special=e; break end end
assert(special)
test_special_entry=special
local fine={patches={[special.id]={max_alive_specials=11}},rules={}}
mods.HavocEnemyDirector={is_gameplay_enabled=function() return true end,get_config=function() return fine end}
B.values.native_configuration_v3={special_slots=2}
Managers.state.game_session={}; E.reset()
local first=E.prepare(special.root,"specials")
assert(first.max_alive_specials==11 and first~=special.root)
assert(E.prepare(first,"specials")==first and E.prepare(special.root,"specials")==first)
fine.patches[special.id].max_alive_specials=13
assert(E.prepare(special.root,"specials")==first and E.config().fine.patches[special.id].max_alive_specials==11)
Managers.state.game_session={}
assert(E.prepare(special.root,"specials").max_alive_specials==13)
mods.HavocEnemyDirector.is_gameplay_enabled=function() return false end
Managers.state.game_session={}
assert(E.prepare(special.root,"specials").max_alive_specials==special.root.max_alive_specials*2)
host=false
assert(E.prepare(special.root,"specials")==special.root)
host=true; mods.HavocEnemyDirector=nil; B.values.native_configuration_v3={}; Managers.state.game_session={}; E.reset()
-- Identity hot path does not rediscover template fields.
local describe=S.describe; local scans=0
S.describe=function(...) scans=scans+1; return describe(...) end
for i=1,10000 do assert(E.prepare(special.root,"specials")==special.root) end
assert(scans==0)
S.describe=describe
-- Function rules keep native calls and add AND/OR clauses without code strings.
local context={players=2,load=40,stage="build_up_tension",monsters=0,events=1,hordes=0,progress=120,stationary=45,low_stage_time=60,combat_vector=10,low_coherency=true}
for _,d in ipairs(R.order) do
    local rule={mode="append",match="all",clauses={R.default_clause(d.id)}}
    assert(R.validate(rule))
    assert(type(R.evaluate(rule,context))=="boolean")
end
local rule={mode="append",match="all",clauses={{condition="players_min",value=3},{condition="event_active"}}}
assert(not R.evaluate(rule,context)); rule.match="any"; assert(R.evaluate(rule,context))
assert(not R.validate({mode="replace",match="all",clauses={{condition="loadstring",value="return true"}}}))
assert(not R.validate({mode="append",match="all",clauses={{condition="players_min",value=0}}}))
assert(not R.validate({mode="append",match="all",clauses={{condition="always",value=1}}}))
local calls=0; local originals={function(side) calls=calls+1; assert(side==2); return false end}
local compiled=R.compile(rule,originals,function(side) assert(side==2); return context end)
assert(#compiled==2 and compiled[1]==originals[1] and not compiled[1](2) and compiled[2](2) and calls==1)
rule.mode="replace"; compiled=R.compile(rule,originals,function() return context end)
assert(#compiled==1 and compiled[1](2))
assert(R.compile({clauses={}},originals,function() error("unused") end)==originals)
-- Unknown fields, non-finite numbers, malformed ranges and wrong breed roles fail.
local cfg,rejected=A.validate_config({patches={[special.id]={max_alive_specials=0,missing=1}},rules={[special.id]={encounter={mode="replace",match="all",clauses={{condition="always"}}}}}})
assert(#rejected==3 and not next(cfg.patches))
local slots=special.fields.max_alive_specials
assert(not S.validate_value(slots,0/0,A.breeds) and not S.validate_value(slots,math.huge,A.breeds))
assert(not S.validate_value(slots,2.5,A.breeds))
local pool
for _,item in ipairs(special.items) do if item.kind=="pool" and item.id=="breeds/all" then pool=item; break end end
assert(pool and not S.validate_value(pool,{"chaos_plague_ogryn"},A.breeds))
assert(not S.validate_value(pool,{},A.breeds))
-- Every published event field stays inside a battle node, away from mission flow.
for _,entry in ipairs(A.entries) do
    if entry.family=="mission_events" then
        for _,item in ipairs(entry.items) do
            local node=entry.root[item.path[1]]
            assert(node[1]=="spawn_by_points" and not node.mission_objective_id)
            assert(item.definition.key~="duration" and item.definition.key~="seed")
        end
    end
end
""")
print("Fine override precedence, alias isolation, session freeze, local authority, zero-scan defaults, rule algebra and validation: PASS")

L.execute("""
-- Rules sample the native capable-player and coherency state, including unknowns.
local units={{help=false,coherency=1},{help=true,coherency=4},{help=false,coherency=3}}
local state={pacing={state=function() return "relax" end,total_challenge_rating=function() return 41 end,
 num_aggroed_monsters=function() return 1 end,get_mission_progression=function() return 120 end,
 low_state_duration=function() return 22 end,_time_since_forward_mission_progressed=33},
 terror_event={num_active_events=function() return 2 end},horde={num_active_hordes=function() return 3 end},
 extension={system=function(_,name)
  if name=="side_system" then return {get_side=function(_,side) assert(side==2); return {valid_player_units=units} end} end
  if name=="combat_vector_system" then return {num_aggroed_combat_vector_minions=function() return 9 end} end
 end}}
local context=R.capture({state=state},{requires_help=function(c) return c.help end},{has_extension=function(u,system)
 if system=="unit_data_system" then return {read_component=function() return u end} end
 if system=="coherency_system" then return {num_units_in_coherency=function() return u.coherency end} end
end},2)
assert(context.players==2 and context.low_coherency and context.load==41 and context.monsters==1)
assert(context.events==2 and context.hordes==3 and context.progress==120 and context.stationary==33 and context.combat_vector==9)
assert(not R.evaluate({match="all",clauses={{condition="monster_idle"}}},R.capture({},nil,nil)))
-- A single breed may have zero weights if another breed covers every live cell.
local root={composition={test={points=0,breeds={{name="chaos_poxwalker",weights={{1,1}}},{name="chaos_newly_infected",weights={{1,1}}}}}}}
local entry={root=root,family="events"}; entry.items,entry.fields=S.describe(root,"events",A.breeds)
local zero={}; local count=0
for _,item in ipairs(entry.items) do if item.definition.key=="weights" then zero[item.id]={0,0}; count=count+1 end end
assert(count==2)
local first=next(zero); assert(A.validate_patch(entry,{[first]={0,0}}))
assert(not A.validate_patch(entry,zero))
for _,entry in ipairs(A.entries) do if entry.family=="events" then
 for _,item in ipairs(entry.items) do
  assert(item.definition.key~="points")
  assert(item.path[1]~="captains_settings" and item.path[1]~="monster_settings" and item.path[1]~="twins_settings")
 end
end end
""")
print("Native rule context, cross-breed event weight validation and exclusion of runtime counters/captured constants: PASS")
