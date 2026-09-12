"""Load HCM's real entry point, without HED, and exercise the native Buff ring."""
from pathlib import Path

work = Path(__file__).resolve().parent
bootstrap = (work / 'standalone_hcm_tests.py').read_text(encoding='utf-8').split(
    'L.execute(\'\'\'\nassert(get_mod("HavocEnemyDirector")==nil)', 1)[0]
exec(compile(bootstrap, 'standalone_buff_bootstrap', 'exec'), globals())
source = (GAME / 'scripts/extension_systems/buff/buff_extension_base.lua').read_text(encoding='utf-8-sig')
prefix = 'local MAX_PROC_EVENTS=require("scripts/settings/buff/buff_settings").max_proc_events; local PROC_EVENTS_STRIDE=2; '
native = {}
for name in ('request_proc_event_param_table', 'add_proc_event', '_update_proc_events', '_clear_param_tables'):
    body = source.split('BuffExtensionBase.' + name + ' = function', 1)[1].split('\nend', 1)[0]
    native[name] = L.execute(prefix + 'return function' + body + '\nend')
L.globals().NativeProc = tbl(native)
L.execute('''
assert(get_mod("HavocEnemyDirector")==nil)
for _,h in ipairs(hooks) do
    assert(h.path~="scripts/extension_systems/buff/buff_extension_base","HCM must not own the Buff allocator")
    assert(h.name~="request_proc_event_param_table" and h.name~="_clear_param_tables")
end
local warnings=0
Log={warning=function() warnings=warnings+1 end}
table.clear=function(t) for k in pairs(t) do t[k]=nil end end
table.clear_array=table.clear
local e=setmetatable({_is_server=true,_proc_event_param_tables={},_num_proc_events=0,
    _num_params_table_in_use=0,_param_tables_start_index_reference=1,_unique_frame_proc={},
    _proc_events={},_proc_events_backup={},_buffs={}},{__index=NativeProc})
local consumed=0
e._buffs[1]={is_predicted=function() return false end,force_predicted_proc=function() return false end,
    skip_send_active_time_rpc=function() return false end,update_proc_events=function(_,t,events,n)
        for i=1,n do assert(events[2*i].sequence==consumed+i) end
        consumed=consumed+n; return false
    end}
for _,count in ipairs({100,300,300}) do
    local refs,seen={},{}
    for i=1,count do
        local p=e:request_proc_event_param_table(); assert(p and not seen[p])
        p.sequence=consumed+i; e:add_proc_event("hit",p); refs[i]=p; seen[p]=true
    end
    if count==300 then
        assert(e:request_proc_event_param_table()==nil and e._num_params_table_in_use==300)
    end
    e:_update_proc_events(0)
    assert(e._num_params_table_in_use==0 and e._num_proc_events==0)
    for _,p in ipairs(refs) do assert(next(p)==nil) end
end
assert(consumed==700 and warnings==2 and #e._proc_event_param_tables==300)
''')
print('Standalone HCM entry point: no Buff allocator hooks; native 300 boundary, overflow rejection, wrapped ring identity/order/reclamation: PASS')
