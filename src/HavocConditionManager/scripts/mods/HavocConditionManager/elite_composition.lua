-- Scale the native breeds already present, independently by enemy category.
local M={}
function M.role(breeds,name)
    local breed=breeds and breeds[name]
    if not breed then return end
    local tags=breed.tags or {}
    if tags.monster or tags.captain or tags.special then return end
    return tags.elite and "elite" or "common"
end
function M.fraction(list,breeds)
    local count,total=0,0
    for _,name in ipairs(list or {}) do
        local kind=M.role(breeds,name)
        if kind then total=total+1;if kind=="elite" then count=count+1 end end
    end
    return total>0 and count/total or 0
end
function M.list(value,factor,breeds)
    if factor==1 then return value end
    local counts,wanted,used={},{},{}
    for _,name in ipairs(value) do counts[name]=(counts[name] or 0)+1 end
    for name,count in pairs(counts) do
        wanted[name]=M.role(breeds,name)=="elite" and math.floor(count*factor+0.5) or count
    end
    local result={}
    for _,name in ipairs(value) do
        local n=(used[name] or 0)+1;used[name]=n
        local copies=math.floor(n*wanted[name]/counts[name])-math.floor((n-1)*wanted[name]/counts[name])
        for _=1,copies do result[#result+1]=name end
    end
    return result
end
function M.amounts(value,elite,breeds,copy,common)
    common=common or 1
    if elite==1 and common==1 then return value end
    local result=copy(value)
    for _,entry in ipairs(result) do
        local kind=M.role(breeds,entry.name)
        local factor=kind=="elite" and elite or kind=="common" and common or 1
        for i=1,2 do entry.amount[i]=math.max(0,math.floor(entry.amount[i]*factor+0.5)) end
    end
    return result
end
return M
