"""Historical 1.6.5 to 1.6.6 seek regression on isolated units.

Runs the real Lua synchronizer and FFI layout reader, including real Windows
VirtualQuery. Only the native seek, Unit getters and world evaluation are
adapters over owned synthetic memory. Timings are NOT game FPS measurements.
"""
from project_env import PROJECT, CHECKS
from lupa.luajit21 import LuaRuntime
import json
import re
import statistics
import sys

package = PROJECT / 'custom-packages/template-library/starter-conditions-frenzied_assault/lua'
runtime = LuaRuntime(unpack_returned_tuples=True)
for name, path in {
    'old_bridge': PROJECT / 'tests/fixtures/frenzied_native_clock_1_6_5.lua',
    'new_bridge': PROJECT / 'tests/fixtures/frenzied_native_clock_1_6_6.lua',
    'old_animation': PROJECT / 'tests/fixtures/frenzied_animation_1_6_5.lua',
    'new_animation': PROJECT / 'tests/fixtures/frenzied_animation_1_6_6.lua',
}.items():
    runtime.globals()[name] = path.read_text(encoding='utf-8')
signatures = re.findall(r'\{(0x[0-9a-f]+),"([0-9a-f]+)"\}', runtime.globals().new_bridge)
runtime.globals().signatures = runtime.table_from([
    runtime.table_from([int(rva, 16), code]) for rva, code in signatures
])
runtime.execute(r'''
local ffi=require('ffi')
ffi.cdef[[typedef struct { void *base; void *allocation; uint32_t allocation_protect;
    uint16_t partition; uint16_t padding; size_t size; uint32_t state;
    uint32_t protect; uint32_t type; uint32_t tail; } BenchmarkFrenzyRegion;
    size_t VirtualQuery(const void *address, void *buffer, size_t length);
    int QueryPerformanceCounter(int64_t *value);
    int QueryPerformanceFrequency(int64_t *value);]]
local kernel=ffi.load('kernel32')
local counter,frequency=ffi.new('int64_t[1]'),ffi.new('int64_t[1]')
assert(kernel.QueryPerformanceFrequency(frequency)~=0)
local function timer()kernel.QueryPerformanceCounter(counter);return tonumber(counter[0])/tonumber(frequency[0])end
local uint32,float64=ffi.typeof('uint32_t *'),ffi.typeof('double *')
local address=ffi.typeof('uintptr_t')
local keep={}
local arena=ffi.new('uint8_t[?]',32*1024*1024);keep[1]=arena
local offset=0
local function allocate(size)
    local ptr=ffi.cast('uint8_t *',arena)+offset
    offset=offset+math.ceil(size/16)*16;assert(offset<ffi.sizeof(arena))
    return ptr
end
local function write(ptr,o,ctype,value)ffi.cast(ctype..' *',ptr+o)[0]=value end
local function pointer(ptr,o,value)write(ptr,o,'uintptr_t',ffi.cast('uintptr_t',value))end
local image=allocate(0x12f6268)
write(image,0,'uint16_t',0x5a4d);write(image,0x3c,'uint32_t',0x100)
write(image,0x100,'uint32_t',0x4550);write(image,0x108,'uint32_t',1786450566)
write(image,0x150,'uint32_t',41992192);write(image,0x118,'uint16_t',0x20b)
for _,spec in ipairs(signatures)do
    local data=spec[2]:gsub('..',function(v)return string.char(tonumber(v,16))end)
    ffi.copy(image+spec[1],data,#data)
end
local registry=allocate(16*0x20000);pointer(image,0x12f6260,registry)
local resource,states,state,blender=allocate(12),allocate(80),allocate(0xb8),allocate(32)
write(resource,8,'uint32_t',10)
for i=0,9 do pointer(states,i*8,state)end
local units,by_unit,by_instance={},{},{}
for index=1,200 do
    local object,instance,layers=allocate(0x270),allocate(0x12f0),allocate(10*0x50)
    pointer(registry,index*16+8,object);write(registry,index*16,'uint32_t',7)
    pointer(object,0x268,instance);pointer(instance,0x30,resource)
    pointer(instance,0x58,states);pointer(instance,0x12e8,layers);pointer(instance,0x40,blender)
    local unit=ffi.cast('void *',0x100000000+(7*0x20000+index)*4+3)
    local spec={unit=unit,layers=layers}
    units[index]=spec;by_unit[unit]=spec;by_instance[tonumber(ffi.cast(address,instance))]=spec
end
local seeks,queries,getters,has_machine,logs=0,0,0,0,0
local function seek(instance,layer,target)
    local spec=assert(by_instance[tonumber(ffi.cast(address,instance))])
    ffi.cast(float64,spec.layers+layer*0x50+8)[0]=target;seeks=seeks+1
end
local info=ffi.new('BenchmarkFrenzyRegion[1]')
local function query(ptr,buffer,size)queries=queries+1;return kernel.VirtualQuery(ptr,buffer,size)end
local function old_reader(ptr,size)
    local n=tonumber(ffi.cast('uintptr_t',ptr))
    if n<0x10000 or n+size>=0x800000000000 then return false end
    if query(ptr,info,48)~=48 then return false end
    local p=tonumber(info[0].protect);local access=p%0x100
    return info[0].state==0x1000 and p%0x200<0x100
        and (access==2 or access==4 or access==8 or access==0x20 or access==0x40 or access==0x80)
        and n+size<=tonumber(ffi.cast('uintptr_t',info[0].base))+tonumber(info[0].size)
end
local Old=assert(loadstring(old_bridge))()
local New=assert(loadstring(new_bridge))()
local reader,reset=New.memory_reader(ffi,query,info)
local clocks={old=assert(Old.create(ffi,image,old_reader,seek)),new=assert(New.create(ffi,image,reader,seek,reset))}
table.clear=function(t)for key in pairs(t)do t[key]=nil end end
ALIVE=setmetatable({},{__index=function()return true end})
World={get_data=function(_,key)return key=='active' end}
ScriptUnit={has_extension=function()return nil end}
Unit={
    has_animation_state_machine=function()has_machine=has_machine+1;return true end,
    animation_get_time=function(unit,buffer)
        getters=getters+1;buffer=buffer or {};local spec=assert(by_unit[unit])
        for i=1,10 do buffer[i]=tonumber(ffi.cast(float64,spec.layers+(i-1)*0x50+8)[0])end
        return buffer,10
    end,
    animation_get_state=function(unit,buffer)
        getters=getters+1;buffer=buffer or {}
        for i=1,10 do buffer[i]=i end;return buffer,10
    end,
    animation_get_animation=function(unit,buffer)
        getters=getters+1;buffer=buffer or {}
        for i=1,10 do buffer[i]=i==1 and -1 or i+100 end;return buffer,10
    end,
}
local animations={}
for name,clock in pairs(clocks)do
    local env=setmetatable({require=function()return clock end},{__index=_G})
    animations[name]=setfenv(assert(loadstring(name=='old' and old_animation or new_animation)),env)()
end
function benchmark(name,count,active_layers,frames,warmup)
    assert(arena[0]~=nil) -- Keep the backing allocation alive across explicit GC.
    local animation=animations[name]
    local current={world={},moves={},log=function()logs=logs+1 end,animation_rate=function()return 2 end}
    local node={tree_node={'BtMeleeFollowTargetAction'}}
    for index=1,count do
        local spec=units[index]
        current.moves[spec.unit]={brain={_breed={name='synthetic_minion'},_running_leaf_node=node,_scratchpad={}}}
        for i=0,9 do
            write(spec.layers,i*0x50,'uint32_t',i<active_layers and 15 or 0xffffffff)
            write(spec.layers,i*0x50+4,'float',10000)
            write(spec.layers,i*0x50+8,'double',1)
            write(spec.layers,i*0x50+0x20,'float',1)
        end
    end
    local function frame()
        local snapshots=animation.before(current,current.world,1/60)
        for index=1,count do
            local spec=units[index]
            for i=0,active_layers-1 do
                local p=ffi.cast(float64,spec.layers+i*0x50+8);p[0]=p[0]+1/60
            end
        end
        local updated,layers,failed=animation.after(snapshots,current)
        return updated,layers,failed
    end
    for i=1,warmup do frame()end
    collectgarbage('collect')
    local sample=units[1];local before=tonumber(ffi.cast(float64,sample.layers+8)[0])
    seeks,queries,getters,has_machine,logs=0,0,0,0,0
    local started=timer()
    for i=1,frames do
        local updated,layers,failed=frame()
        assert(updated==count and layers==count*active_layers and failed==0)
    end
    local ms=(timer()-started)*1000/frames
    local elapsed=tonumber(ffi.cast(float64,sample.layers+8)[0])-before
    assert(math.abs(elapsed-frames*2/60)<.003,'Preserve 2x playback at every density')
    assert(seeks==count*active_layers*frames,'Never reduce seek cadence to save time')
    assert(getters==count*frames*(name=='old' and 9 or 6),'No redundant full-unit readback')
    assert(logs==0,'Steady-state diagnostics must not log each frame')
    if name=='new' then assert(queries<=frames*2,'Synthetic region is queried once per pass, not per layer')end
    return {ms=ms,queries_per_frame=queries/frames,getters_per_frame=getters/frames,
        seeks_per_frame=seeks/frames,elapsed=elapsed}
end
''')

full = '--benchmark' in sys.argv
results = []
for count, layers in ([(100, 2), (200, 2), (200, 4)] if full else [(200, 2)]):
    samples = {'old': [], 'new': []}
    for _ in range(3 if full else 1):
        for name in ('old', 'new'):
            sample = dict(runtime.globals().benchmark(name, count, layers, 30 if full else 8, 10 if full else 3).items())
            samples[name].append(sample)
    row = {'units': count, 'total_layers': 10, 'active_layers': layers}
    for name in samples:
        row[name] = dict(samples[name][-1], ms=statistics.median(s['ms'] for s in samples[name]))
    row['reduction_percent'] = 100 * (1 - row['new']['ms'] / row['old']['ms'])
    assert abs(row['old']['elapsed'] - row['new']['elapsed']) < .00001
    results.append(row)
report = {'scope': 'Synthetic owned memory; real Lua/FFI/VirtualQuery; simulated native seek/getters/world. Not game FPS.', 'results': results}
(CHECKS / ('frenzied-performance.json' if full else 'frenzied-performance-regression.json')).write_text(json.dumps(report, indent=2), encoding='utf-8')
for row in results:
    print(f"PASS historical 1.6.5 -> 1.6.6: {row['units']} units x {row['active_layers']}/10 active layers: "
          f"{row['old']['ms']:.3f} -> {row['new']['ms']:.3f} ms/pass; "
          f"VirtualQuery {row['old']['queries_per_frame']:.0f} -> {row['new']['queries_per_frame']:.0f}; "
          f"getters {row['old']['getters_per_frame']:.0f} -> {row['new']['getters_per_frame']:.0f}; "
          f"same {row['new']['seeks_per_frame']:.0f} seeks/frame and 2x playhead. Synthetic benchmark, not game FPS.")
