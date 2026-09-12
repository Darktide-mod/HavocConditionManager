-- Keep the game's spawn queue and one-request-per-update behavior. A full ring
-- must grow before another request writes into an unconsumed entry.
local mod=get_mod("HavocConditionManager")
local Minion=require("scripts/managers/minion/minion_spawn_manager")
local function grow(self,capacity)
    local old=self._spawn_queue
    local size=self._spawn_queue_size
    local read=self._spawn_queue_read_index
    local next_capacity=capacity*2
    local queue=Script.new_array(next_capacity)
    for i=1,size do queue[i]=old[(read+i-2)%capacity+1] end
    for i=size+1,next_capacity do queue[i]={} end
    self._spawn_queue=queue
    self._spawn_queue_read_index=1
    self._spawn_queue_write_index=size+1
    self._hcm_spawn_queue_capacity=next_capacity
    return next_capacity
end
mod:hook(Minion,"queue_minion_to_spawn",function(fn,self,breed,position,rotation,side)
    local capacity=self._hcm_spawn_queue_capacity
    if not capacity then
        capacity=#self._spawn_queue
        if self._spawn_queue_size<capacity or not mod.has_local_gameplay_authority() then
            local entry=fn(self,breed,position,rotation,side)
            return mod.tag_spawn_request and mod.tag_spawn_request(entry) or entry
        end
    end
    if self._spawn_queue_size>=capacity then capacity=grow(self,capacity) end
    local write=self._spawn_queue_write_index
    local entry=self._spawn_queue[write]
    entry.breed_name=breed
    entry.position=Vector3Box(position)
    entry.rotation=QuaternionBox(rotation)
    entry.side_id=side
    self._spawn_queue_write_index=write%capacity+1
    self._spawn_queue_size=self._spawn_queue_size+1
    -- Callers attach spawn-source, objective and event data to this same table.
    return mod.tag_spawn_request and mod.tag_spawn_request(entry) or entry
end)
mod:hook(Minion,"_update_spawn_queue",function(fn,self)
    if not self._hcm_spawn_queue_capacity and not mod.has_local_gameplay_authority() then return fn(self) end
    if self._spawn_queue_size==0 or self._hcm_spawn_queue_draining then return end
    local entry=self._spawn_queue[self._spawn_queue_read_index]
    self._hcm_spawn_queue_draining=true
    local ticket=entry._hcm_redeployment
    local allowed=not ticket or mod.prepare_redeployment(ticket,entry)
    entry._hcm_redeployment=nil
    local unit
    if allowed then unit=self:spawn_minion(entry.breed_name,entry.position:unbox(),entry.rotation:unbox(),entry.side_id,entry) end
    if ticket then mod.finish_redeployment(ticket,unit) end
    self._hcm_spawn_queue_draining=nil
    table.clear(entry)
    -- Spawn callbacks may have enqueued more requests and grown/rebased the ring.
    local capacity=self._hcm_spawn_queue_capacity or #self._spawn_queue
    self._spawn_queue_read_index=self._spawn_queue_read_index%capacity+1
    self._spawn_queue_size=self._spawn_queue_size-1
end)
return true
