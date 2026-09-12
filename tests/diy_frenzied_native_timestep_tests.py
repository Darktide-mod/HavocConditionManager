"""Execute the real x64 timestep detours on owned synthetic functions only.

Checks the real game build's entry signatures but never hooks/executes game
code or attaches to its process. MinHook runs inside this disposable Python
test process. Native detours must preserve ABI, scope, hash and dt semantics.
"""
from project_env import PROJECT, CHECKS
from pathlib import Path
import hashlib
import json
import re
import struct
from lupa.luajit21 import LuaRuntime

package = PROJECT / 'custom-packages/template-library/starter-conditions-frenzied_assault/lua'
source = (package / 'native_timestep.lua').read_text(encoding='utf-8')
dll = PROJECT / 'src/HavocConditionManager/native/HCM-MinHook-1.3.4.x64.dll'
assert hashlib.sha256(dll.read_bytes()).hexdigest() == '033e55af8995c3b260e56de73daf99ff4a7ce2fcbe4b3872db2270678d8c6585'
blob = (PROJECT.parents[3] / 'binaries/Darktide.exe').read_bytes()
pe = struct.unpack_from('<I', blob, 0x3c)[0]
count = struct.unpack_from('<H', blob, pe+6)[0]
optional = struct.unpack_from('<H', blob, pe+20)[0]
sections = [struct.unpack_from('<8sIIII', blob, pe+24+optional+i*40) for i in range(count)]
signatures = re.findall(r'\{(0x[0-9a-f]+),"([0-9a-f ]+)"\}', source)
assert len(signatures) == 4
for rva, hex_code in signatures:
    rva = int(rva, 16); expected = bytes.fromhex(hex_code)
    section = next(s for s in sections if s[2] <= rva < s[2]+s[3])
    offset = section[4]+rva-section[2]
    assert blob[offset:offset+len(expected)] == expected, hex(rva)

L = LuaRuntime(unpack_returned_tuples=True)
L.execute('Guard={};local old=require;require=function(p)if p=="./native_clock.lua" then return Guard end;return old(p)end')
L.globals().Native = L.execute(source)
guard_source = (package / 'native_clock.lua').read_text(encoding='utf-8')
L.globals().OwnerGuard = L.execute(guard_source)
L.globals().owner_signatures = L.table_from([L.table_from([int(rva,16), code])
    for rva, code in re.findall(r'\{(0x[0-9a-f]+),"([0-9a-f]+)"\}', guard_source)])
L.globals().animation_source = (package / 'animation.lua').read_text(encoding='utf-8')
L.globals().dll_path = str(dll)
L.execute(r'''
local ffi=require('ffi');Native.cdef(ffi)
assert(Native.library_path('F:/library/Darktide/binaries/Darktide.exe')=='F:/library/Darktide/mods/HavocConditionManager/native/HCM-MinHook-1.3.4.x64.dll')
assert(Native.library_path([[F:\library\Darktide\binaries\Darktide.exe]])==[[F:\library\Darktide/mods/HavocConditionManager/native/HCM-MinHook-1.3.4.x64.dll]])
assert(not pcall(Native.library_path,'Darktide.exe'),'Library loading must not depend on the working directory')
local kernel=ffi.load('kernel32');local hooks=ffi.load(dll_path)
local function bytes(hex)return (hex:gsub('%s',''):gsub('..',function(s)return string.char(tonumber(s,16))end))end
-- Windows x64 ABI: RCX=owner, XMM1=dt, R8/R9=sentinels, fifth argument on stack.
local body=bytes('f3 0f 11 09 4c 89 41 08 4c 89 49 10 48 8b 44 24 28 48 89 41 18 0f 28 c1 c3')..string.rep('\x90',40)
local targets,functions={},{}
for i=1,4 do
    local page=assert(kernel.VirtualAlloc(nil,4096,0x3000,0x40))
    ffi.copy(page,body,#body)
    assert(kernel.FlushInstructionCache(kernel.GetCurrentProcess(),page,4096)~=0)
    targets[i]=page
    functions[i]=ffi.cast('float (*)(void *, float, uint64_t, uint64_t, uint64_t)',page)
end
local driver=Native.create_driver(ffi,kernel,hooks,targets)
assert(driver:enable())
local arena=ffi.new('uint8_t[?]',0x110000)
local a=ffi.cast('uint8_t *',arena)+64
local b=a+0x80000 -- Deliberate collision in the native hash.
local plain=a+128
local function read(p,offset,ctype)return tonumber(ffi.cast(ctype..' *',p+offset)[0])end
local function call(i,p,dt,rate)
    local value=functions[i](p,dt,0x12345678,0x1234567890,0x76543210)
    assert(math.abs(value-dt*rate)<.00001,tostring(value)..' vs '..dt*rate)
    assert(math.abs(read(p,0,'float')-dt*rate)<.00001)
    assert(read(p,8,'uint64_t')==0x12345678 and read(p,16,'uint64_t')==0x1234567890
        and read(p,24,'uint64_t')==0x76543210,'Detour must preserve registers and stack arguments')
end
for i=1,4 do call(i,a,.125,1)end
driver:begin()
local slot_a=driver:add(a,2);local slot_b=driver:add(b,3)
assert(slot_b==(slot_a+1)%32768,'Collision must use linear probing')
for i=1,4 do call(i,a,.125,1)end -- Unpublished maps never affect workers.
driver:commit()
for i=1,4 do call(i,a,.125,2);call(i,b,.125,3);call(i,plain,.125,1)end
assert(driver.entries[slot_a].hits==15 and driver.entries[slot_b].hits==15)
assert(not pcall(driver.add,driver,a,4),'An active map is immutable')
driver:finish()
for i=1,4 do call(i,a,.125,1)end
driver:begin();driver:add(a,2.4);driver:commit()
for i=1,4 do call(i,a,.05,2.4);call(i,b,.05,1)end
driver:finish()
-- Arbitrary internal clip changes use the same owner dt without a new seek.
driver:begin();driver:add(a,2);driver:commit()
local root,clock,event,blend=0,0,0,0
for frame=1,60 do
    local dt=functions[2](a,1/60,1,2,3)
    clock=clock+dt;root=root+4*dt;blend=blend+dt
    if clock>=.4 and event==0 then event=1 end
    if frame==20 then ffi.cast('uint32_t *',a+32)[0]=37 end -- Internal state change.
end
assert(math.abs(clock-2)<.00001 and math.abs(root-8)<.00001 and event==1 and math.abs(blend-2)<.00001)
driver:finish()
-- The same native functions return to 1x immediately for a traversal policy.
driver:begin();driver:commit()
for i=1,4 do call(i,a,.125,1)end
driver:finish();assert(driver:disable())
for i=1,4 do call(i,a,.125,1)end
assert(driver:enable());driver:begin();driver:add(a,2);driver:commit();call(2,a,.125,2)
driver:finish();assert(driver:disable())
-- Complete production animation pass: real owner guard, OS region query,
-- native map publication and all native detours. Only the world/Unit facade
-- and native engine bodies are synthetic owned memory, never game entities.
ffi.cdef[[typedef struct { void *base; void *allocation; uint32_t allocation_protect;
    uint16_t partition; uint16_t padding; size_t size; uint32_t state;
    uint32_t protect; uint32_t type; uint32_t tail; } NativeDtBenchmarkRegion;
    size_t VirtualQuery(const void *, void *, size_t);
    int QueryPerformanceCounter(int64_t *);
    int QueryPerformanceFrequency(int64_t *);]]
local region=ffi.new('NativeDtBenchmarkRegion[1]');local queries=0
local reader,reset=OwnerGuard.memory_reader(ffi,function(p,out,n)
    queries=queries+1;return kernel.VirtualQuery(p,out,n)
end,region)
local storage=ffi.new('uint8_t[?]',32*1024*1024);local offset=0
local function alloc(n)local p=ffi.cast('uint8_t *',storage)+offset;offset=offset+math.ceil(n/16)*16;assert(offset<ffi.sizeof(storage));return p end
local function write(p,o,t,v)ffi.cast(t..' *',p+o)[0]=v end
local function ptr(p,o,v)write(p,o,'uintptr_t',ffi.cast('uintptr_t',v))end
local image=alloc(0x12f6268)
write(image,0,'uint16_t',0x5a4d);write(image,0x3c,'uint32_t',0x100)
write(image,0x100,'uint32_t',0x4550);write(image,0x108,'uint32_t',1786450566)
write(image,0x150,'uint32_t',41992192);write(image,0x118,'uint16_t',0x20b)
for _,spec in ipairs(owner_signatures)do local code=bytes(spec[2]);ffi.copy(image+spec[1],code,#code)end
local registry=alloc(16*0x20000);ptr(image,0x12f6260,registry)
local resource=alloc(16);write(resource,8,'uint32_t',10)
local units={}
for i=1,400 do
    local object,instance,blender=alloc(0x270),alloc(0x60),alloc(0xf0)
    ptr(registry,i*16+8,object);write(registry,i*16,'uint32_t',7)
    ptr(object,0x268,instance);ptr(object,0x260,blender)
    ptr(instance,0x30,resource);ptr(instance,0x40,blender);write(instance,0x50,'uint32_t',10)
    units[i]={unit=ffi.cast('void *',0x100000000+(7*0x20000+i)*4+3),instance=instance,blender=blender}
end
local clock=assert(OwnerGuard.create(ffi,image,reader,reset))
Guard.available=function()return true end
Guard.begin_frame,Guard.end_frame,Guard.bind=clock.begin_frame,clock.end_frame,clock.bind
local saved={driver=driver}
get_mod=function()return {persistent_table=function()return saved end}end
assert(Native.available()) -- Reuse the actual pinned driver after disable.
table.clear=function(t)for k in pairs(t)do t[k]=nil end end
ALIVE=setmetatable({},{__index=function()return true end})
local machine_checks=0
Unit=setmetatable({has_animation_state_machine=function()machine_checks=machine_checks+1;return true end},
    {__index=function(_,key)error('Unexpected public animation getter/setter: '..key)end})
World={get_data=function(_,key)return key=='active' end}
ScriptUnit={has_extension=function()return nil end}
local env=setmetatable({require=function(path)if path=='./native_clock.lua' then return Guard end;assert(path=='./native_timestep.lua');return Native end},{__index=_G})
local animation=setfenv(assert(loadstring(animation_source)),env)()
local counter,freq=ffi.new('int64_t[1]'),ffi.new('int64_t[1]')
assert(kernel.QueryPerformanceFrequency(freq)~=0)
local function timer()kernel.QueryPerformanceCounter(counter);return tonumber(counter[0])/tonumber(freq[0])end
performance_results={}
for _,count in ipairs({100,200,400})do
    assert(storage[0]~=nil)
    assert(animation.available() and driver.traced)
    local logs=0;local current={world={},moves={},animation_rate=function()return 2 end,log=function()logs=logs+1 end}
    for i=1,count do current.moves[units[i].unit]={brain={_breed={name='synthetic'},_running_leaf_node={tree_node={'BtMeleeFollowTargetAction'}},_scratchpad={}}}end
    local function frame()
        local bindings=animation.before(current,current.world,1/60)
        assert(bindings==true and driver.count==count*2)
        for i=1,count do
            local u=units[i]
            local state=functions[2](u.instance,1/60,1,2,3)
            local blend=functions[3](u.blender,1/60,1,2,3)
            local playback=functions[4](u.blender,1/60,1,2,3)
            assert(math.abs(state-2/60)<1e-7 and state==blend and blend==playback)
        end
        animation.after(bindings,current)
        assert(driver.state[0].active==0)
    end
    for i=1,15 do frame()end
    assert(logs==0 and driver.state[0].trace==0,'Production disables diagnostics from the first frame')
    collectgarbage('collect');queries=0;machine_checks=0
    local started=timer();local frames=100
    for i=1,frames do frame()end
    local ms=(timer()-started)*1000/frames
    assert(queries<=frames*2 and machine_checks==frames*count)
    assert(logs==0,'No per-frame logs or atomic trace writes')
    performance_results[#performance_results+1]={units=count,ms_per_pass=ms,queries_per_frame=queries/frames,
        owner_bindings=count*2,native_dt_calls=count*3,layer_getters=0,seeks=0}
end
-- Empty accelerated scope must keep the real native detours inactive and
-- avoid both the 512 KiB map reset and owner memory queries.
local original_begin=driver.begin;local empty_begins=0
driver.begin=function(self)empty_begins=empty_begins+1;return original_begin(self)end
local empty={world={},moves={},animation_rate=function()return 1 end}
for i=1,400 do empty.moves[units[i].unit]={brain={}}end
queries=0
for frame=1,100 do
    assert(not animation.before(empty,empty.world,1/60))
    assert(driver.state[0].active==0)
    call(2,units[1].instance,1/60,1)
end
assert(empty_begins==0 and queries==0)
driver.begin=original_begin
assert(Native.cleanup())
assert(Native.available() and not driver.traced,'A new mission must re-arm its one-time native confirmation')
assert(Native.cleanup())
-- The detours are scene-wide: include many unregistered animated objects
-- with only ten selected owners. This scope was absent from the old sample.
local backdrop=ffi.new('uint8_t[?]',10000*64)
local backdrop_ptr=ffi.cast('uint8_t *',backdrop)
scope_results={}
local function backdrop_pass(count)
    for i=0,count-1 do
        local p=backdrop_ptr+i*64
        functions[2](p,1/60,1,2,3);functions[3](p,1/60,1,2,3);functions[4](p,1/60,1,2,3)
    end
end
for _,count in ipairs({100,1000,10000})do
    local times={}
    for _,enabled in ipairs({false,true})do
        if enabled then
            assert(driver:enable());driver:begin()
            for i=1,10 do driver:add(units[i].instance,2);driver:add(units[i].blender,2)end
            driver.traced=true;driver.state[0].trace=0;driver:commit()
        end
        for i=1,10 do backdrop_pass(count)end
        local started=timer()
        for i=1,100 do backdrop_pass(count)end
        times[enabled and 2 or 1]=(timer()-started)*10
        assert(math.abs(read(backdrop_ptr,0,'float')-1/60)<1e-7,'Unselected objects retain their native dt')
        if enabled then driver:finish();assert(driver:disable())end
    end
    scope_results[#scope_results+1]={selected=10,unselected=count,native_calls=count*3,
        disabled_ms=times[1],enabled_ms=times[2],difference_ms=times[2]-times[1]}
end
-- These functions have no other callers or worker threads in this isolated
-- process, so test-only removal/free is safe after all synchronous calls end.
for i,target in ipairs(targets)do
    assert(hooks.MH_RemoveHook(target)==0)
    assert(kernel.RtlDeleteFunctionTable(driver.tables[i])~=0)
    assert(kernel.VirtualFree(driver.pages[i],0,0x8000)~=0)
    assert(kernel.VirtualFree(target,0,0x8000)~=0)
end
''')
results = [dict(row.items()) for _,row in L.globals().performance_results.items()]
scope_results = [dict(row.items()) for _,row in L.globals().scope_results.items()]
(CHECKS / 'frenzied-native-scene-scope.json').write_text(json.dumps({
    'scope': 'Ten selected owners, unselected synthetic native animation calls. Detour lookup only, not engine animation/rendering or game FPS.',
    'results': scope_results},indent=2),encoding='utf-8')
for row in scope_results:
    print(f"PASS scene scope: 10 selected, {row['unselected']} unselected: native entry overhead "
          f"{row['difference_ms']:.4f} ms/pass; synthetic native bodies only.")
(CHECKS / 'frenzied-native-timestep-performance.json').write_text(json.dumps({
    'scope': 'Synthetic owned memory and native bodies; real complete Lua/FFI/VirtualQuery/MinHook detour pass. Not game FPS.',
    'results': results},indent=2),encoding='utf-8')
for row in results:
    print(f"PASS current native dt: {row['units']} units, {row['ms_per_pass']:.3f} ms/pass, "
          f"{row['queries_per_frame']:.0f} region queries, zero layer getters/seeks; synthetic, not game FPS.")
animation = (package / 'animation.lua').read_text(encoding='utf-8')
assert 'Unit.animation_get_' not in animation and '.advance(' not in animation
assert 'set_time' not in animation and 'set_state' not in animation
print('PASS: four audited native entry signatures; official helper digest; real x64 dt detours, MinHook enable/disable/re-enable, register/stack ABI, collision lookup, inactive scope, immutable publication, no cross-unit leakage, 2x/2.4x clocks/root/events and internal transitions. Executed only synthetic owned functions; no game process/native game function invoked.')
