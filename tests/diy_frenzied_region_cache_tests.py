"""Replay owner validation across interleaved Windows allocations, not game memory."""
from project_env import PROJECT, CHECKS
import json,re
from lupa.luajit21 import LuaRuntime
L=LuaRuntime(unpack_returned_tuples=True)
source=(PROJECT/'custom-packages/template-library/starter-conditions-frenzied_assault/lua/native_clock.lua').read_text(encoding='utf-8')
L.globals().Guard=L.execute(source)
L.globals().Previous=L.execute((PROJECT/'tests/fixtures/frenzied_native_clock_1_7_1.lua').read_text(encoding='utf-8'))
L.globals().signatures=L.table_from([L.table_from([int(r,16),s]) for r,s in re.findall(r'\{(0x[0-9a-f]+),"([0-9a-f]+)"\}',source)])
L.execute(r'''
local ffi=require('ffi')
ffi.cdef[[typedef struct {void *base;void *allocation;uint32_t allocation_protect;
    uint16_t partition;uint16_t padding;size_t size;uint32_t state;
    uint32_t protect;uint32_t type;uint32_t tail;} RegionCacheTestInfo;
    void *VirtualAlloc(void *,size_t,uint32_t,uint32_t);
    int VirtualFree(void *,size_t,uint32_t);
    size_t VirtualQuery(const void *,void *,size_t);
    int VirtualProtect(void *,size_t,uint32_t,uint32_t *);
    int QueryPerformanceCounter(int64_t *);int QueryPerformanceFrequency(int64_t *);]]
local kernel=ffi.load('kernel32');local keep={}
local function alloc(n)
    local p=kernel.VirtualAlloc(nil,n,0x3000,4);assert(p~=nil)
    keep[#keep+1]=p;return ffi.cast('uint8_t *',p)
end
local function write(p,o,t,v)ffi.cast(t..' *',p+o)[0]=v end
local function ptr(p,o,v)write(p,o,'uintptr_t',ffi.cast('uintptr_t',v))end
local image,registry=alloc(0x1300000),alloc(16*0x20000)
local objects,instances,blenders,resource=alloc(400*4096),alloc(400*4096),alloc(400*4096),alloc(4096)
write(image,0,'uint16_t',0x5a4d);write(image,0x3c,'uint32_t',0x100)
write(image,0x100,'uint32_t',0x4550);write(image,0x108,'uint32_t',1786450566)
write(image,0x150,'uint32_t',41992192);write(image,0x118,'uint16_t',0x20b)
for _,s in ipairs(signatures)do local bytes=s[2]:gsub('..',function(h)return string.char(tonumber(h,16))end);ffi.copy(image+s[1],bytes,#bytes)end
ptr(image,0x12f6260,registry);write(resource,8,'uint32_t',10)
local units,contexts={},{}
for i=1,400 do
    local object,instance,blender=objects+(i-1)*4096,instances+(i-1)*4096,blenders+(i-1)*4096
    write(registry,i*16,'uint32_t',7);ptr(registry,i*16+8,object)
    ptr(object,0x268,instance);ptr(object,0x260,blender)
    ptr(instance,0x30,resource);ptr(instance,0x40,blender);write(instance,0x50,'uint32_t',10)
    units[i]=ffi.cast('void *',0x100000000+(7*0x20000+i)*4+3);contexts[i]={}
end
local counter,freq=ffi.new('int64_t[1]'),ffi.new('int64_t[1]');assert(kernel.QueryPerformanceFrequency(freq)~=0)
local function timer()kernel.QueryPerformanceCounter(counter);return tonumber(counter[0])/tonumber(freq[0])end
results={}
for _,count in ipairs({20,100,200,400})do
    local row={units=count}
    for _,variant in ipairs({'old','new'})do
        local query_count=0
        local info=ffi.new('RegionCacheTestInfo[1]')
        local reader,reset,stats=(variant=='old' and Previous or Guard).memory_reader(ffi,function(p,out,n)
            query_count=query_count+1;return kernel.VirtualQuery(p,out,n)
        end,info)
        local clock=assert(Guard.create(ffi,image,reader,reset))
        local function pass()
            clock.begin_frame()
            for i=1,count do assert(clock.bind(units[i],contexts[i])==contexts[i])end
            if stats then assert(stats.queries==5 and stats.regions==5)end
            clock.end_frame()
        end
        for i=1,25 do pass()end
        query_count=0;local started=timer();local passes=80
        for i=1,passes do pass()end
        row[variant..'_ms']=(timer()-started)*1000/passes
        row[variant..'_queries']=query_count/passes
        if variant=='new' then assert(query_count==5*passes)else assert(query_count>=3*count*passes)end
    end
    results[#results+1]=row
end
-- Region caches end with the synchronous pass. Protection changes and live
-- generations/owners must still invalidate subsequent bindings immediately.
local info=ffi.new('RegionCacheTestInfo[1]');local reader,reset,stats=Guard.memory_reader(ffi,kernel.VirtualQuery,info)
local clock=assert(Guard.create(ffi,image,reader,reset));local old=ffi.new('uint32_t[1]')
clock.begin_frame();assert(clock.bind(units[1]));write(registry,16,'uint32_t',8)
assert(clock.bind(units[1])==nil,'Generation is never cached');write(registry,16,'uint32_t',7)
ptr(instances,0x40,blenders+4096);assert(clock.bind(units[1])==nil,'Owner relation is never cached');ptr(instances,0x40,blenders)
clock.end_frame();assert(kernel.VirtualProtect(objects,4096,1,old)~=0)
clock.begin_frame();assert(clock.bind(units[1])==nil,'Next pass must re-query no-access protection');clock.end_frame()
assert(kernel.VirtualProtect(objects,4096,4,old)~=0)
clock.begin_frame();assert(clock.bind(units[1]));clock.end_frame()
assert(kernel.VirtualProtect(objects+4096,4096,2,old)~=0)
reset(true);assert(reader(objects+4096-8,8));assert(not reader(objects+4096-8,16),'Cross-region reads fail closed');reset(false)
assert(kernel.VirtualProtect(objects+4096,4096,0x104,old)~=0)
assert(not reader(objects+4096,8),'Guard pages fail closed')
assert(not reader(ffi.cast('void *',1),8))
for _,p in ipairs(keep)do assert(kernel.VirtualFree(p,0,0x8000)~=0)end
''')
rows=[dict(L.globals().results[i].items()) for i in range(1,len(L.globals().results)+1)]
(CHECKS/'frenzied-region-cache.json').write_text(json.dumps({'scope':'owned synthetic Windows allocations; no live game access; not an FPS prediction','rows':rows,'cross_pass_protection_and_live_owner_checks':True},indent=2)+'\n',encoding='utf-8')
print('PASS: actual VirtualQuery across interleaved arenas; released page-cache query amplification reproduced, complete-region cache needs five queries per pass; generations, owner relations, region boundaries, guard pages and next-pass protection changes remain checked.')
print(json.dumps(rows))
