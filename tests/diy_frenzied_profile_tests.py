"""Bounded real-clock diagnostics: classify costs without changing gameplay."""
from project_env import PROJECT
from lupa.luajit21 import LuaRuntime
source=(PROJECT/'tests/fixtures/frenzied_profile_1_7_3.lua').read_text(encoding='utf-8')
L=LuaRuntime(unpack_returned_tuples=True)
L.globals().Profile=L.execute(source)
L.execute(r'''
table.clear=function(t)for k in pairs(t)do t[k]=nil end end
World={get_data=function(w,k)return w[k]end}
local world={active=true};local other={active=true};local now=0;local logs={}
local p=Profile.new(function(s)logs[#logs+1]=s end,world,function()return now end)
assert(p and p:begin(other,.02)==nil and not p.started)
for frame=1,500 do
    now=(frame-1)*.02
    local a=p:begin(world,.02)
    if a then
        -- 1 ms mod preparation, 8 ms engine/callback work, .1 ms cleanup.
        p:ended(a,a+.001,a+.009,a+.0091,12,4,{queries=6,regions=5})
        -- Separate AI timing, allowed to overlap world callback time.
        p:ai(a,a+.0002,a+.0012,a+.0013,8)
    end
end
assert(p.samples==50 and p.ai_calls==50 and #logs==1)
now=10;p:begin(world,.02)
assert(#logs==2)
local row=logs[2]
for _,field in ipairs({'fps=50.0','frame_ms=20.00','samples=50','tracked=12.0/12','animated=4.0/4',
    'prepare_ms=1.000','world_ms=8.000','after_ms=0.100','ai_own_total_ms=15.000','ai_inner_total_ms=50.000','node_swaps=400','memory_queries=6.0/6','memory_regions=5.0/5'})do
    assert(row:find(field,1,true),field..' missing in '..row)
end
-- A pause or a different world cannot create a fake long frame or AI sample.
world.paused=true;now=30;assert(p:begin(world,0)==nil and not p.sampling)
local intervals=p.intervals
world.paused=false;now=31;p:begin(world,.02)
assert(p.intervals==intervals and p.frame_max<100)
now=181;p:begin(world,.02)
assert(p.stopped and not p.sampling)
local count=#logs;p:begin(world,.02);p:stop();assert(#logs==count)
-- Real QPC factory is exercised in this isolated process and stays monotonic.
local real=assert(Profile.new(function()end,world));local a=real.clock();local b=real.clock();assert(b>=a)
real:stop()
''')
print('PASS: real QPC, sampled phase/AI attribution, total vs own cost separation, wall-frame intervals, population counts, pause/world filtering, ten-second summaries, three-minute stop and idempotent cleanup; no gameplay-rate changes.')
