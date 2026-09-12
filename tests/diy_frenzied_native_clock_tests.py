"""Validate the bridge on isolated FFI memory, never on the running game.

The real seek function is NOT invoked here. Its ABI/signatures are checked
against the executable; the call adapter verifies the guarded arguments and
models the documented live-layer update. This is not an in-game visual test.
"""
from project_env import PROJECT
from pathlib import Path
import re
import struct
from lupa.luajit21 import LuaRuntime

source=(PROJECT/'tests/fixtures/frenzied_native_clock_1_6_6.lua').read_text(encoding='utf-8')
guard_source=(PROJECT/'custom-packages/template-library/starter-conditions-frenzied_assault/lua/native_clock.lua').read_text(encoding='utf-8')
exe=PROJECT.parents[3]/'binaries/Darktide.exe'
blob=exe.read_bytes(); pe=struct.unpack_from('<I',blob,0x3c)[0]
assert struct.unpack_from('<I',blob,pe+8)[0]==1786450566
assert struct.unpack_from('<I',blob,pe+0x50)[0]==41992192
n=struct.unpack_from('<H',blob,pe+6)[0]; size=struct.unpack_from('<H',blob,pe+20)[0]
sections=[struct.unpack_from('<8sIIII',blob,pe+24+size+i*40) for i in range(n)]
signatures=[]
for rva,expected in re.findall(r'\{(0x[0-9a-f]+),"([0-9a-f]+)"\}',source):
    rva=int(rva,16); expected=bytes.fromhex(expected)
    for _,vsize,va,rawsize,raw in sections:
        if va<=rva<va+rawsize:
            assert blob[raw+rva-va:raw+rva-va+len(expected)]==expected,hex(rva)
            signatures.append((rva,expected.hex()));break
    else:raise AssertionError(hex(rva))
assert len(signatures)==4
L=LuaRuntime(unpack_returned_tuples=True)
L.globals().Bridge=L.execute(source)
L.globals().Guard=L.execute(guard_source)
L.globals().LegacyBridge=L.execute((PROJECT/'tests/fixtures/frenzied_native_clock_1_6_4.lua').read_text(encoding='utf-8'))
L.globals().signatures=L.table_from([L.table_from(pair) for pair in signatures])
L.execute(r'''
local ffi=require('ffi')
local keep,regions={},{}
local function allocate(n)
    local storage=ffi.new('uint8_t[?]',n);keep[#keep+1]=storage
    local p=ffi.cast('uint8_t *',storage);local addr=tonumber(ffi.cast('uintptr_t',p))
    regions[#regions+1]={addr,n};return p
end
local blocked
local function readable(p,n)
    local addr=tonumber(ffi.cast('uintptr_t',p))
    if blocked and addr==blocked then return false end
    for _,region in ipairs(regions)do if addr>=region[1] and addr+n<=region[1]+region[2] then return true end end
    return false
end
local function write(p,o,t,v)ffi.cast(t..' *',p+o)[0]=v end
local function read(p,o,t)return ffi.cast(t..' *',p+o)[0]end
local image=allocate(0x12f6268)
write(image,0,'uint16_t',0x5a4d);write(image,0x3c,'uint32_t',0x100)
write(image,0x100,'uint32_t',0x4550);write(image,0x108,'uint32_t',1786450566)
write(image,0x150,'uint32_t',41992192);write(image,0x118,'uint16_t',0x20b)
for _,spec in ipairs(signatures)do
    local data=spec[2]:gsub('..',function(v)return string.char(tonumber(v,16))end)
    ffi.copy(image+spec[1],data,#data)
end
local registry=allocate(16*0x20000);write(image,0x12f6260,'uintptr_t',ffi.cast('uintptr_t',registry))
local object=allocate(0x270);local instance=allocate(0x12f0)
local resource=allocate(12);local layers=allocate(0xa0);local states=allocate(16)
local state=allocate(0xb8);local events=allocate(36);local blender=allocate(0xf0)
local function pointer(p,o,v)write(p,o,'uintptr_t',ffi.cast('uintptr_t',v))end
pointer(registry,2*16+8,object);write(registry,2*16,'uint32_t',7)
pointer(object,0x268,instance);pointer(instance,0x30,resource)
pointer(object,0x260,blender);write(instance,0x50,'uint32_t',2)
pointer(instance,0x58,states);pointer(instance,0x12e8,layers);pointer(instance,0x40,blender)
write(resource,8,'uint32_t',2);pointer(states,0,state);pointer(states,8,state)
pointer(state,0xb0,events);write(state,0xa8,'uint32_t',0)
write(layers,0,'uint32_t',15);write(layers,4,'float',10);write(layers,8,'double',1)
write(layers,0x20,'float',1);write(layers,0x50,'uint32_t',0xffffffff)
-- Custom-blend resource type. Its public animation id is -1, which is
-- irrelevant to this bridge: it uses the existing root player handle.
write(state,0x18,'uint32_t',2)
local unit=ffi.cast('void *',(7*0x20000+2)*4)
local calls,fail=0,false
local function seek(p,layer,time)
    assert(p==instance and layer==0 and time>0)
    calls=calls+1
    if not fail then write(layers,8,'double',time)end
end
local clock=assert(Bridge.create(ffi,image,readable,seek))
local legacy=assert(LegacyBridge.create(ffi,image,readable,seek))
local function rejected(why,...)
    local count=calls;local value,reason=clock.advance(...)
    assert(value==nil and reason==why,tostring(value)..' '..tostring(reason))
    assert(calls==count,'Rejected memory must never enter native code')
end
-- Native getter truncates ECX before shifting, rather than rejecting tag
-- bits or the upper word. 1.6.4's tests used only untagged cdata and missed
-- this exact reason for every in-game layer being rejected.
for _,upper in ipairs({0,0x100000000,0x10000000000})do
    for tag=0,3 do
        local tagged=ffi.cast('void *',upper+(7*0x20000+2)*4+tag)
        write(layers,8,'double',1)
        if upper~=0 or tag~=0 then
            local before=calls;local rejected,reason=legacy.advance(tagged,1,1,1.25,2)
            assert(rejected==nil and reason=='invalid unit reference' and calls==before,
                'Released 1.6.4 rejects tagged references before any native animation call')
        end
        assert(clock.advance(tagged,1,1,1.25,2)==1.25)
    end
end
-- Exercise an actual Lua lightuserdata, not just a cdata<void *> surrogate.
local captured=1;local function closure()return captured end
local light=debug.upvalueid(closure,1)
assert(type(light)=='userdata')
local low=tonumber(ffi.cast('uint32_t',ffi.cast('uintptr_t',light)))
local ref=math.floor(low/4);local index=ref%0x20000
assert(index~=0x1ffff and index~=2)
write(registry,index*16,'uint32_t',math.floor(ref/0x20000));pointer(registry,index*16+8,object)
write(layers,8,'double',1)
local old_value,old_reason=legacy.advance(light,1,1,1.25,2)
assert(old_value==nil and old_reason=='invalid unit reference')
assert(clock.advance(light,1,1,1.25,2)==1.25)
assert(calls==13)
local wide=ffi.new('uint64_t',0x20000000000000)+ffi.new('uint64_t',(7*0x20000+2)*4+3)
write(layers,8,'double',1)
assert(clock.advance(ffi.cast('void *',wide),1,1,1.25,2)==1.25,
    'Do not round the full 64-bit carrier through a Lua number before truncating it')
assert(read(states,0,'uintptr_t')==ffi.cast('uintptr_t',state))
rejected('live clock mismatch',unit,1,1,1.5,2)
rejected('invalid clock request',unit,0,1.25,1.5,2)
rejected('invalid clock request',unit,1,0/0,1.5,2)
rejected('invalid unit reference',nil,1,1.25,1.5,2)
rejected('invalid unit reference',{},1,1.25,1.5,2)
rejected('unit unavailable',ffi.cast('void *',0x100000000),1,1.25,1.5,2)
rejected('unit unavailable',ffi.cast('void *',3),1,1.25,1.5,2)
rejected('invalid unit index',ffi.cast('void *',0x1ffff*4),1,1.25,1.5,2)
write(registry,2*16,'uint32_t',8)
rejected('expired unit generation',unit,1,1.25,1.5,2)
write(registry,2*16,'uint32_t',7)
blocked=tonumber(ffi.cast('uintptr_t',instance))
rejected('animation instance unavailable',unit,1,1.25,1.5,2);blocked=nil
write(resource,8,'uint32_t',3)
rejected('animation layout mismatch',unit,1,1.25,1.5,2);write(resource,8,'uint32_t',2)
local prior=calls
local inactive,why=clock.advance(unit,2,0,1,2)
assert(inactive==false and why=='inactive layer' and calls==prior,'Empty auxiliary layers are normal, not quarantined failures')
write(state,0xa8,'uint32_t',4097)
rejected('event layout mismatch',unit,1,1.25,1.5,2)
write(state,0xa8,'uint32_t',1);write(events,0,'float',1.4)
local value=clock.advance(unit,1,1.25,1.5,2)
assert(value>1.39 and value<1.4,'Do not seek past the next native animation event')
assert(read(layers,0x14,'uint32_t')==0,'Normal evaluation must still see the event')
local count=calls
assert(clock.advance(unit,1,value,1.5,2)==false and calls==count,'Let normal evaluation cross the boundary')
write(state,0xa8,'uint32_t',0);write(layers,4,'float',1.6)
value=clock.advance(unit,1,value,3,2)
assert(value>1.59 and value<1.6,'Normal evaluation owns clip end and transition')
write(layers,4,'float',10);write(state,0xa8,'uint32_t',1)
write(layers,0x14,'uint32_t',1);write(events,0,'float',8);write(events,8,'uint32_t',4)
value=clock.advance(unit,1,value,3,2)
assert(value>1.99 and value<2,'Reverse/end event cursor is preserved too')
write(state,0xa8,'uint32_t',0);write(layers,0x14,'uint32_t',0)
write(layers,0x18,'uint32_t',1)
rejected('event cursor mismatch',unit,1,value,3,2);write(layers,0x18,'uint32_t',0)
fail=true
local bad,why=clock.advance(unit,1,value,3,2)
assert(bad==nil and why=='seek readback mismatch');fail=false
-- A prepared layout can be reused for layers in exactly one pre-world pass.
clock.begin_frame()
local context=assert(clock.prepare(unit,2,{}))
write(layers,8,'double',1)
assert(clock.advance_prepared(context,1,1,1.25)==1.25)
clock.end_frame()
local prior=calls
local expired,why=clock.advance_prepared(context,1,1.25,1.5)
assert(expired==nil and why=='expired clock pass' and calls==prior)
assert(clock.prepare(unit,2)==nil)
clock.begin_frame()
assert(clock.advance_prepared(context,1,1.25,1.5)==nil,'Starting a new pass cannot revive a saved pointer')
write(registry,2*16,'uint32_t',8)
assert(clock.prepare(unit,2,context)==nil,'Generation is checked again every pass')
write(registry,2*16,'uint32_t',7)
local replacement=allocate(0x12f0)
pointer(object,0x268,replacement)
assert(clock.prepare(unit,2,context)==nil,'Replaced instances cannot reuse the old validated layout')
pointer(object,0x268,instance)
context=assert(clock.prepare(unit,2,context))
-- An empty layer can reactivate with unchanged public state/clip identifiers.
write(layers,0,'uint32_t',0xffffffff)
assert(clock.advance_prepared(context,1,1.25,1.5)==false)
write(layers,0,'uint32_t',15)
assert(clock.advance_prepared(context,1,1.25,1.5)==1.5)
clock.end_frame()

-- Current 1.7.0 reads only the owner identities; no layer/player calls remain.
local guard=assert(Guard.create(ffi,image,readable))
assert(guard.bind(unit,{})==nil)
guard.begin_frame()
local binding={}
assert(guard.bind(unit,binding)==binding and binding.instance==instance and binding.blender==blender)
assert(guard.bind(light,{}) and guard.bind(ffi.cast('void *',wide),{}))
local prior=calls
write(registry,2*16,'uint32_t',8)
assert(guard.bind(unit,binding)==nil,'Recheck generation before publishing each frame')
write(registry,2*16,'uint32_t',7)
pointer(object,0x260,state)
assert(guard.bind(unit,binding)==nil,'Reject a detached/mismatched blender')
pointer(object,0x260,blender)
write(instance,0x50,'uint32_t',3)
assert(guard.bind(unit,binding)==nil,'Owner/resource counts must agree')
write(instance,0x50,'uint32_t',2)
blocked=tonumber(ffi.cast('uintptr_t',instance))
assert(guard.bind(unit,binding)==nil);blocked=nil
pointer(object,0x268,replacement)
assert(guard.bind(unit,binding)==nil,'A reused handle cannot reuse the previous owner')
pointer(object,0x268,instance)
assert(guard.bind(unit,binding)==binding and calls==prior,'Binding never calls native seek')
guard.end_frame();assert(guard.bind(unit,binding)==nil)

-- The same production region reader is tested with controlled OS replies.
ffi.cdef[[typedef struct { void *base; void *allocation; uint32_t allocation_protect;
    uint16_t partition; uint16_t padding; size_t size; uint32_t state;
    uint32_t protect; uint32_t type; uint32_t tail; } TestFrenzyRegion;]]
local info=ffi.new('TestFrenzyRegion[1]')
local queries,protection,commit,result=0,4,0x1000,48
local reader,reset=Guard.memory_reader(ffi,function(p,out,n)
    queries=queries+1;assert(n==48)
    out[0].base=ffi.cast('void *',0x10000);out[0].size=0x3000
    out[0].protect=protection;out[0].state=commit
    return result
end,info)
reset(true)
assert(reader(ffi.cast('void *',0x10100),16))
assert(reader(ffi.cast('void *',0x12ff0),16) and queries==1,'One region validation covers a synchronous pass')
assert(not reader(ffi.cast('void *',0x12ff0),17),'A cached region never permits an out-of-bounds read')
reset(false);protection=1
assert(not reader(ffi.cast('void *',0x10100),16),'Protection is checked again after the pass ends')
reset(true);protection=0x104
assert(not reader(ffi.cast('void *',0x10100),16),'Guard pages fail closed')
protection=4;commit=0x2000
assert(not reader(ffi.cast('void *',0x10100),16),'Uncommitted pages fail closed')
commit=0x1000;result=0
assert(not reader(ffi.cast('void *',0x10100),16),'VirtualQuery failure fails closed')
result=48;assert(reader(ffi.cast('void *',0x10100),16))
reset(true);protection=1
assert(not reader(ffi.cast('void *',0x10100),16),'The next pass cannot reuse the previous memory map')
reset(false)
assert(not reader(ffi.cast('void *',0),16))
-- Every independent executable identity check is mandatory.
write(image,0x108,'uint32_t',0)
assert(Bridge.create(ffi,image,readable,seek)==nil);write(image,0x108,'uint32_t',1786450566)
write(image,0x150,'uint32_t',1)
assert(Bridge.create(ffi,image,readable,seek)==nil);write(image,0x150,'uint32_t',41992192)
for _,spec in ipairs(signatures)do
    local first=image[spec[1]];image[spec[1]]=0xcc
    local denied,reason=Bridge.create(ffi,image,readable,seek)
    assert(denied==nil and reason:find('signature mismatch',1,true));image[spec[1]]=first
end
assert(Bridge.create(ffi,image,readable,seek))
-- The real Windows loader/query wrapper sees Python's executable, so it must
-- refuse it without calling a game address. This also exercises FFI cdefs.
local available,reason=Bridge.available()
assert(not available and reason:find('unsupported game executable',1,true),tostring(reason))
available,reason=Guard.available()
assert(not available and reason:find('unsupported game executable',1,true),tostring(reason))
''')
print('PASS: released 1.6.4 rejection reproduced; tagged/upper-word handles and real Lua lightuserdata; exact low32 decoding without 64-bit rounding; executable signatures, generations, pointers, layer/seek ABI, event boundaries and readback failure. No game process or real native seek invoked.')
