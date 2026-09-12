-- In-place AnimationInstance seek, verified against the 1.12.5 Windows image.
-- No patching, guessed crossfade handles, pending restore or layer rebuilding.
-- Build and pointer checks fail closed; an engine update needs a new audit.
local M={}
local signatures={
    {0x5a2460,"48895c24084889742410574883ec20488b41580f57c0448bc2488bf14a8b3cc04b8d1c8048c1e304480399e81200000f2fd00f86b80000008b13f30f5ad2f20f115308488b4940e884bd06008b13488b4e40e889c406004885c0740ac780d805000002000000f20f104b08448b43148b97a8000000660f5ac9f30f5e4b20443bc273330f1f4000660f1f840000000000418bc0488d0c40488b87b00000000f2f0c88721241ffc0448943148b97a8000000443bc272da8b4b183bca73330f1f008bc1488d1440488b87b0000000837c900804750ff30f104304f30f5c04900f2fc8720dffc1894b183b8fa800000072d0488b5c2430488b7424384883c4205fc3"},
    {0x5390f7,"488bc8c1e90281f9ffff0100741f8bc1c1e91125ffff010048c1e00448030546d1db00390875064c8b7008eb034d8bf7"},
    {0x53926b,"4d8b8e68020000498b4130448b7008"},
    {0x60e230,"40534883ec20488bd9e8020700004c8bc04885c0744c4533c94439482476439048"},
}
local function finite(n)return type(n)=="number" and n==n and math.abs(n)<1e9 end

-- The constructor also accepts an isolated memory reader/call adapter for
-- regression tests. Production always supplies VirtualQuery and the image.
function M.create(ffi,base,readable,call)
    local byte=ffi.typeof("uint8_t *")
    local function ptr(p)return ffi.cast(byte,p)end
    base=ptr(base)
    local function at(p,offset,ctype)return ffi.cast(ctype.." *",ptr(p)+offset)[0]end
    local function u32(p,o)return tonumber(at(p,o,"uint32_t"))end
    local function f32(p,o)return tonumber(at(p,o,"float"))end
    local function pointer(p,o)return ptr(at(p,o,"uintptr_t"))end
    if not readable(base,0x40) or u32(base,0)%0x10000~=0x5a4d then return nil,"invalid executable image" end
    local pe=u32(base,0x3c)
    if pe>0x1000 or not readable(base+pe,0x90) or u32(base,pe)~=0x4550
        or u32(base,pe+8)~=1786450566 or u32(base,pe+0x50)~=41992192
        or tonumber(at(base,pe+0x18,"uint16_t"))~=0x20b then
        return nil,"unsupported game executable; expected audited 1.12.5 build"
    end
    for _,spec in ipairs(signatures)do
        local expected=spec[2]:gsub("..",function(h)return string.char(tonumber(h,16))end)
        if not readable(base+spec[1],#expected) or ffi.string(base+spec[1],#expected)~=expected then
            return nil,string.format("engine signature mismatch at RVA %x",spec[1])
        end
    end
    if not readable(base+0x12f6260,8) then return nil,"unit registry unavailable" end
    local seek=call or ffi.cast("void (*)(void *, uint32_t, float)",base+0x5a2460)
    local clock={}
    function clock.advance(unit,layer,before,target,count)
        if not finite(before) or not finite(target) or target<=before or target<=0
            or count<1 or count>32 or layer<1 or layer>count then return nil,"invalid clock request" end
        -- UnitRef is encoded as a lightuserdata, shifted left by two bits.
        local ok,encoded=pcall(function()return tonumber(ffi.cast("uintptr_t",unit))end)
        if not ok or encoded<0 or encoded>0xffffffff or encoded%4~=0 then return nil,"invalid unit reference" end
        local ref=encoded/4
        local index=ref%0x20000
        if index==0x1ffff then return nil,"invalid unit index" end
        local registry=pointer(base,0x12f6260)
        local entry=registry+index*16
        if not readable(registry,16) or not readable(entry,16) or u32(entry,0)~=math.floor(ref/0x20000) then
            return nil,"expired unit generation"
        end
        local object=pointer(entry,8)
        if not readable(object,0x270) then return nil,"unit unavailable" end
        local instance=pointer(object,0x268)
        if not readable(instance,0x12f0) then return nil,"animation instance unavailable" end
        local resource=pointer(instance,0x30)
        local states,layers,blender=pointer(instance,0x58),pointer(instance,0x12e8),pointer(instance,0x40)
        if not readable(resource,12) or u32(resource,8)~=count or not readable(states,count*8)
            or not readable(layers,count*0x50) or not readable(blender,0x20) then return nil,"animation layout mismatch" end
        local state=pointer(states,(layer-1)*8)
        local live=layers+(layer-1)*0x50
        if not readable(state,0xb8) or u32(live,0)==0xffffffff then return nil,"inactive layer" end
        local now=tonumber(at(live,8,"double"))
        if not finite(now) or math.abs(now-before)>.0001 then return nil,"live clock mismatch" end
        local divisor,duration=f32(live,0x20),f32(live,4)
        if not finite(divisor) or divisor<=0 or not finite(duration) or duration<=0 then return nil,"inactive layer" end
        local events=u32(state,0xa8)
        local list=pointer(state,0xb0)
        if events>4096 or events>0 and not readable(list,events*12) then return nil,"event layout mismatch" end
        local first,last=u32(live,0x14),u32(live,0x18)
        if first>events or last>events then return nil,"event cursor mismatch" end
        -- Leave the next authored event and clip end for normal evaluation.
        -- Seeking past those cursors would silently omit animation events.
        local limit=duration*divisor
        if first<events then limit=math.min(limit,f32(list,first*12)*divisor)end
        for i=last,events-1 do
            if u32(list,i*12+8)==4 then
                limit=math.min(limit,(duration-f32(list,i*12))*divisor);break
            end
        end
        if not finite(limit) then return nil,"invalid event time" end
        target=tonumber(ffi.cast("float",math.min(target,limit-.0001)))
        if target<=before then return false,"native boundary" end
        -- Existing root blend and all of its child clips retain their handles,
        -- weights and outgoing transitions; the engine seeks those players.
        seek(instance,layer-1,target)
        if pointer(states,(layer-1)*8)~=state or u32(resource,8)~=count
            or math.abs(tonumber(at(live,8,"double"))-target)>.0001 then return nil,"seek readback mismatch" end
        return target
    end
    return clock
end

local instance,reason,attempted
function M.available()
    if attempted then return instance~=nil,reason end
    attempted=true
    local ok,result,why=pcall(function()
        local ffi=Mods and Mods.lua and Mods.lua.ffi or require("ffi")
        if not ffi or ffi.os~="Windows" or not ffi.abi("64bit") then return nil,"Windows x64 LuaJIT FFI required" end
        if not pcall(ffi.typeof,"HCMFrenzyMemoryInfo164") then
            ffi.cdef[[
                typedef struct { void *base; void *allocation; uint32_t allocation_protect;
                    uint16_t partition; uint16_t padding; size_t size; uint32_t state;
                    uint32_t protect; uint32_t type; uint32_t tail; } HCMFrenzyMemoryInfo164;
                void *GetModuleHandleA(const char *name);
                size_t VirtualQuery(const void *address, void *buffer, size_t length);
            ]]
        end
        local kernel=ffi.load("kernel32")
        local info=ffi.new("HCMFrenzyMemoryInfo164[1]")
        assert(ffi.sizeof(info)==48,"unexpected memory-info layout")
        local function readable(address,size)
            local n=tonumber(ffi.cast("uintptr_t",address))
            if n<0x10000 or n+size>=0x800000000000 then return false end
            if kernel.VirtualQuery(address,info,48)~=48 then return false end
            local p=tonumber(info[0].protect)
            local access=p%0x100
            return info[0].state==0x1000 and p%0x200<0x100
                and (access==2 or access==4 or access==8 or access==0x20 or access==0x40 or access==0x80)
                and n+size<=tonumber(ffi.cast("uintptr_t",info[0].base))+tonumber(info[0].size)
        end
        return M.create(ffi,kernel.GetModuleHandleA(nil),readable)
    end)
    if ok then instance,reason=result,why else reason=tostring(result)end
    return instance~=nil,reason
end
function M.advance(...)
    if not instance then return nil,reason or "native clock unavailable" end
    return instance.advance(...)
end
return M
