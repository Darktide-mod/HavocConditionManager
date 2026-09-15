-- Shared settings for HCM and Studio; captured once by the mission runtime.
local C={}
C.defaults={enabled=true,check_interval=5,quiet_time=30,distance=35,rear_distance=60,remove_interval=0.25,spawn_interval=0.25,replenish=true}
C.limits={check_interval={2,30},quiet_time={10,180},distance={25,200},rear_distance={30,300},remove_interval={0.1,5},spawn_interval={0.1,5}}
function C.validate(raw)
    raw=raw or {}
    if type(raw)~="table" or getmetatable(raw) then return nil,"recycling settings" end
    for k in pairs(raw) do if C.defaults[k]==nil then return nil,"recycling field" end end
    local out={}
    for k,default in pairs(C.defaults) do
        local v=raw[k];if v==nil then v=default end
        local limit=C.limits[k]
        if limit then
            if type(v)~="number" or v~=v or v<limit[1] or v>limit[2] then return nil,"recycling "..k end
        elseif type(v)~="boolean" then return nil,"recycling "..k end
        out[k]=v
    end
    return out
end
return C

