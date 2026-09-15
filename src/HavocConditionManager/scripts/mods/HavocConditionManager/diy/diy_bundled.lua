-- Read declared package files in place through DMF. No extraction or execution.
local B={}
function B.read(mod,name,Codec,Packages)
    if type(name)~="string" or not name:match("^[%w_]+$") then return nil,"diy_package_path" end
    local root=name.."/diy/"
    local function read(relative)
        local io=Mods and Mods.lua and Mods.lua.io
        if io and io.open then
            local file=io.open("./../mods/"..root..relative,"rb")
            if not file then return nil end
            local text=file:read(8388609);file:close()
            return text and #text<=8388608 and text or nil
        end
        local stem,extension=relative:match("^(.*)%.([^./]+)$")
        if not stem then return nil end
        return mod:io_read_content(root..stem,extension)
    end
    local index,why=Codec.decode(read("index.json") or "")
    if not index or index.version~=1 or type(index.packages)~="table" or #index.packages>256 then return nil,why or "diy_package_manifest" end
    local batch,total={},0
    for _,id in ipairs(index.packages)do
        if not Packages.id(id) or batch[id] then return nil,"diy_package_path" end
        local prefix="packages/"..id.."/"
        local manifest_text=read(prefix.."package.json")
        local manifest=manifest_text and Codec.decode(manifest_text)
        if not manifest or manifest.id~=id or type(manifest.files)~="table" or #manifest.files>256 then return nil,"diy_package_manifest: "..id end
        local files={["package.json"]=manifest_text}
        for _,path in ipairs(manifest.files)do
            if not Packages.path(path) or files[path] then return nil,"diy_package_path" end
            local text=read(prefix..path)
            if type(text)~="string" or #text>8388608 then return nil,"diy_package_io: "..id.."/"..path end
            total=total+#text;if total>Packages.max_library_bytes then return nil,"diy_package_limit" end
            files[path]=text
        end
        batch[id]=files
    end
    return batch
end
return B
