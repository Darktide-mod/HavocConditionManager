-- Read-only unit-owner guard for the native timestep hooks, audited on 1.12.5.
-- No animation layers or playback times are read or written here.
-- Build and pointer checks fail closed; an engine update needs a new audit.
local M={}
local signatures={
    {0x5390f7,"488bc8c1e90281f9ffff0100741f8bc1c1e91125ffff010048c1e00448030546d1db00390875064c8b7008eb034d8bf7"},
    {0x53926b,"4d8b8e68020000498b4130448b7008"},
}

-- The constructor also accepts an isolated memory reader for
-- regression tests. Production always supplies VirtualQuery and the image.
function M.create(ffi,base,readable,reset_reader)
    local byte=ffi.typeof("uint8_t *")
    local uint32,uint16=ffi.typeof("uint32_t *"),ffi.typeof("uint16_t *")
    local address=ffi.typeof("uintptr_t *")
    local carrier,low32=ffi.typeof("uintptr_t"),ffi.typeof("uint32_t")
    local function ptr(p)return ffi.cast(byte,p)end
    base=ptr(base)
    local function u32(p,o)return tonumber(ffi.cast(uint32,p+o)[0])end
    local function pointer(p,o)return ptr(ffi.cast(address,p+o)[0])end
    local function encode(unit)return tonumber(ffi.cast(low32,ffi.cast(carrier,unit)))end
    if not readable(base,0x40) or u32(base,0)%0x10000~=0x5a4d then return nil,"invalid executable image" end
    local pe=u32(base,0x3c)
    if pe>0x1000 or not readable(base+pe,0x90) or u32(base,pe)~=0x4550
        or u32(base,pe+8)~=1786450566 or u32(base,pe+0x50)~=41992192
        or tonumber(ffi.cast(uint16,base+pe+0x18)[0])~=0x20b then
        return nil,"unsupported game executable; expected audited 1.12.5 build"
    end
    for _,spec in ipairs(signatures)do
        local expected=spec[2]:gsub("..",function(h)return string.char(tonumber(h,16))end)
        if not readable(base+spec[1],#expected) or ffi.string(base+spec[1],#expected)~=expected then
            return nil,string.format("engine signature mismatch at RVA %x",spec[1])
        end
    end
    if not readable(base+0x12f6260,8) then return nil,"unit registry unavailable" end
    local clock={base=base}
    local active=false
    function clock.begin_frame()
        active=true
        if reset_reader then reset_reader(true)end
    end
    function clock.end_frame()
        active=false
        if reset_reader then reset_reader(false)end
    end
    -- Resolve only the two native animation owners. The timestep path does
    -- not inspect, read back or seek individual layers.
    function clock.bind(unit,context)
        if not active then return nil,"clock pass inactive" end
        if type(unit)~="userdata" and type(unit)~="cdata" then return nil,"invalid unit reference" end
        local ok,encoded=pcall(encode,unit)
        if not ok then return nil,"unit reference conversion failed" end
        local ref=math.floor(encoded/4);local index=ref%0x20000
        if index==0x1ffff then return nil,"invalid unit index" end
        local registry=pointer(base,0x12f6260);local entry=registry+index*16
        if not readable(registry,16) or not readable(entry,16) or u32(entry,0)~=math.floor(ref/0x20000) then return nil,"expired unit generation" end
        local object=pointer(entry,8)
        if not readable(object,0x270) then return nil,"unit unavailable" end
        local instance,blender=pointer(object,0x268),pointer(object,0x260)
        if not readable(instance,0x58) or not readable(blender,0xf0) then return nil,"animation owners unavailable" end
        local resource=pointer(instance,0x30)
        if not readable(resource,12) or u32(resource,8)<1 or u32(resource,8)>32
            or u32(instance,0x50)~=u32(resource,8) or pointer(instance,0x40)~=blender then return nil,"animation owner layout mismatch" end
        context=context or {}
        context.instance,context.blender=instance,blender
        return context
    end
    return clock
end

-- Cache OS memory-region permissions only during one synchronous binding pass.
-- Live values (generation, pointers and counts) are
-- still read each time. Clear before returning to any native world update.
function M.memory_reader(ffi,query,info)
    local uintptr=ffi.typeof("uintptr_t")
    local ends={}
    local caching,last_start,last_end=false,0,0
    local function reset(enabled)
        for page in pairs(ends)do ends[page]=nil end
        caching=enabled;last_start,last_end=0,0
    end
    local function readable(address,size)
        local n=tonumber(ffi.cast(uintptr,address))
        if n<0x10000 or size<0 or n+size>=0x800000000000 then return false end
        local page=math.floor(n/4096)
        if caching then
            if n>=last_start and n+size<=last_end then return true end
            if ends[page] and n+size<=ends[page] then return true end
        end
        if query(address,info,48)~=48 then return false end
        local p=tonumber(info[0].protect)
        local access=p%0x100
        local start=tonumber(ffi.cast(uintptr,info[0].base))
        local finish=start+tonumber(info[0].size)
        local valid=info[0].state==0x1000 and p%0x200<0x100
            and (access==2 or access==4 or access==8 or access==0x20 or access==0x40 or access==0x80)
            and n>=start and n+size<=finish
        if valid and caching then
            last_start,last_end=start,finish
            if start<=page*4096 then ends[page]=finish end
        end
        return valid
    end
    return readable,reset
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
        local readable,reset=M.memory_reader(ffi,kernel.VirtualQuery,info)
        return M.create(ffi,kernel.GetModuleHandleA(nil),readable,reset)
    end)
    if ok then instance,reason=result,why else reason=tostring(result)end
    return instance~=nil,reason
end
function M.begin_frame()if instance then instance.begin_frame()end end
function M.end_frame()if instance then instance.end_frame()end end
function M.bind(...)return instance.bind(...)end
function M.image_base()return instance and instance.base end
return M
