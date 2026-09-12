from project_env import SOURCES
from lupa.luajit21 import LuaRuntime
lua=LuaRuntime(unpack_returned_tuples=True)
def module(mod,path):
    return lua.execute((SOURCES/mod/'scripts/mods'/mod/path).read_text(encoding='utf-8-sig'))
lua.globals().H=module('HavocConditionManager','havoc_conditions.lua')
lua.execute('''
local ids={}
for i=1,80 do ids[i]="condition_"..i end
assert(#H.sanitize(ids)==80)
local combined=H.compose(ids,{"condition_1","theme","difficulty"})
assert(#combined==82)
local ctx={havoc_data="a;;rank;faction;old;modifiers;seed;tail"}
local _,ok=H.apply_to_mission_context(ctx,ids,{"theme"})
assert(ok and ctx.havoc_data:find("a;;rank;faction;",1,true)==1)
assert(ctx.havoc_data:find(";modifiers;seed;tail",1,true))
H.apply_to_mission_context(ctx,{}, {})
assert(ctx.havoc_data=="a;;rank;faction;;modifiers;seed;tail")
local broken={havoc_data="bad"}; local _,changed=H.apply_to_mission_context(broken,ids,{})
assert(not changed and broken.havoc_data=="bad")
assert(#H.remove({"a"},"a",0)==0)
''')
print('Core behavior: PASS')
