-- Local authority only. Keep initially plugged medicae empty; remove the
-- unpowered station/battery pair. Do not modify general healing or quest batteries.
local mod = get_mod("HavocConditionManager")
local HealthStation = require("scripts/extension_systems/health_station/health_station_extension")
local HealthStationSystem = require("scripts/extension_systems/health_station/health_station_system")
local PickupSystem = require("scripts/extension_systems/pickups/pickup_system")
local Pocketable = require("scripts/utilities/pocketable")

local blocked_pickups = {
    syringe_corruption_pocketable = true,
    medical_crate_pocketable = true,
}

local function pack(...)
    return { n = select("#", ...), ... }
end

local function controller(state, server)
    local current = state.current
    if current and current.active and server ~= false and mod.has_local_gameplay_authority()
        and Managers.state and Managers.state.game_session == current.session then
        return current
    end
end

local function transfer(current, fn, ...)
    current.transfer_depth = current.transfer_depth + 1
    local results = pack(pcall(fn, ...))
    current.transfer_depth = current.transfer_depth - 1
    if not results[1] then error(results[2], 0) end
    return unpack(results, 2, results.n)
end

local function install_hooks()
    -- DMF registers one handler per mod/method. Retain only a routing table
    -- between missions so a refreshed package can supply a new controller.
    local state = mod._diy_medical_map_hooks_v1
    if state then return state end
    state = {}
    mod._diy_medical_map_hooks_v1 = state

    mod:hook(HealthStation, "fixed_update", function(fn, self, ...)
        local current = controller(state, self._is_server)
        if not current then return fn(self, ...) end
        local decision = current:station_kind(self)
        if decision == "remove" then
            current.pending[self._unit] = self
            return
        end
        if current.cleared[self] then return fn(self, ...) end
        self._distributed_charges = 0
        local results = pack(fn(self, ...))
        current:empty_station(self)
        return unpack(results, 1, results.n)
    end)

    mod:hook(HealthStation, "spawn_battery", function(fn, self, ...)
        local current = controller(state, self._is_server)
        if current and not self._first_frame_setup and self:use_distribution_pool()
            and self._distributed_charges == nil then
            -- A component flow can run before distribution. Defer this spawn
            -- to native first-frame setup instead of caching an empty-socket
            -- decision before the station's placement has been assigned.
            return
        end
        if current and current:station_kind(self) == "remove" then
            current.pending[self._unit] = self
            return
        end
        return fn(self, ...)
    end)

    mod:hook(HealthStationSystem, "hot_join_sync", function(fn, self, sender, channel, ...)
        local results = pack(fn(self, sender, channel, ...))
        local current = controller(state, self._is_server)
        if current then
            for level_id in pairs(current.removed_stations) do
                RPC.rpc_health_station_despawn(channel, level_id)
            end
        end
        return unpack(results, 1, results.n)
    end)

    mod:hook(PickupSystem, "spawn_pickup", function(fn, self, name, ...)
        local current = controller(state, self._is_server)
        if current and current.transfer_depth == 0 and blocked_pickups[name] then
            return nil, nil
        end
        return fn(self, name, ...)
    end)

    -- Dropping/swapping an already carried item is not a new map supply.
    -- These native callers also expect a real returned unit for bookkeeping.
    mod:hook(PickupSystem, "player_spawn_pickup", function(fn, self, ...)
        local current = controller(state, self._is_server)
        if current then return transfer(current, fn, self, ...) end
        return fn(self, ...)
    end)
    for _,method in ipairs({ "drop_pocketable", "equip_pocketable" }) do
        mod:hook(Pocketable, method, function(fn, ...)
            local current = controller(state)
            if current then return transfer(current, fn, ...) end
            return fn(...)
        end)
    end
    return state
end

local function system(name)
    local extension = Managers.state and Managers.state.extension
    if extension and extension:has_system(name) then return extension:system(name) end
end

local function new_controller()
    local current = {
        active = true,
        session = Managers.state.game_session,
        decisions = setmetatable({}, { __mode = "k" }),
        cleared = setmetatable({}, { __mode = "k" }),
        pending = {},
        removed_stations = {},
        transfer_depth = 0,
        scanned_pickups = nil,
        scanned_stations = nil,
    }

    function current:station_kind(extension)
        local known = self.decisions[extension]
        if known then return known end
        local plugged
        if extension._first_frame_setup then
            plugged = extension:battery_in_slot()
        else
            -- Match the native first-frame placement decision, before zeroing
            -- its charge count. A full distribution can intentionally be loose.
            local mode = extension:battery_spawning_mode()
            plugged = mode == "plugged"
            if extension:use_distribution_pool() then
                plugged = mode == "plugged_with_charge" and extension._plug_from_distribution
            end
            local circumstance = Managers.state.circumstance
            local overrides = circumstance and circumstance:mission_overrides().health_station
            if overrides and overrides.skip_battery_spawning then plugged = false end
        end
        local decision = plugged and "keep" or "remove"
        self.decisions[extension] = decision
        return decision
    end

    function current:empty_station(extension)
        extension._distributed_charges = 0
        if extension:charge_amount() ~= 0 then
            extension:set_charge_amount(0)
            extension:sync_charge_amount()
            if extension:battery_in_slot() then extension:play_anim("close") end
        else
            -- Native socketing may already have synchronized zero. This call
            -- keeps late activation consistent without changing battery state.
            extension:sync_charge_amount()
        end
        self.cleared[extension] = true
    end

    function current:scan_existing()
        local stations = system("health_station_system")
        if stations and stations._is_server and self.scanned_stations ~= stations then
            self.scanned_stations = stations
            for unit, extension in pairs(stations:unit_to_extension_map()) do
                -- Uninitialized distribution fields are not a placement result.
                -- The first fixed update handles stations still being set up.
                if ALIVE[unit] and extension._first_frame_setup then
                    if self:station_kind(extension) == "keep" then self:empty_station(extension)
                    else self.pending[unit] = extension end
                end
            end
        end
        local pickups = system("pickup_system")
        if pickups and pickups._is_server and self.scanned_pickups ~= pickups then
            self.scanned_pickups = pickups
            local remove = {}
            for _,unit in ipairs(pickups._spawned_pickups) do
                if ALIVE[unit] and not pickups._dropped_pickups[unit]
                    and not pickups._pickup_to_owner_player[unit]
                    and blocked_pickups[Unit.get_data(unit, "pickup_type")] then
                    remove[#remove + 1] = unit
                end
            end
            for _,unit in ipairs(remove) do pickups:despawn_pickup(unit) end
        end
    end

    function current:remove_pending()
        local spawner = Managers.state.unit_spawner
        if not spawner then return end
        for unit, extension in pairs(self.pending) do
            if ALIVE[unit] then
                -- This is the station's own tracked battery, never every
                -- battery_01/battery_02 pickup used by other mission objectives.
                extension:unspawn_battery()
                local level_id = spawner:level_index(unit)
                if level_id and not self.removed_stations[level_id] then
                    Managers.state.game_session:send_rpc_clients("rpc_health_station_despawn", level_id)
                    self.removed_stations[level_id] = true
                end
                if not spawner:is_marked_for_deletion(unit) then spawner:mark_for_deletion(unit) end
            end
            self.pending[unit] = nil
        end
    end
    return current
end

return {
    api_version = { major = 1, minor = 0 },
    entries = {
        no_healing = {
            interval = 0.1,
            on_activate = function(ctx)
                local hooks = install_hooks()
                local current = new_controller()
                hooks.current = current
                ctx.state.current = current
                ctx:on_cleanup(function()
                    current.active = false
                    if hooks.current == current then hooks.current = nil end
                    current.pending = {}
                    ctx.state.current = nil
                end)
                current:scan_existing()
                current:remove_pending()
            end,
            on_update = function(ctx)
                local current = ctx.state.current
                if not current or not current.active or not mod.has_local_gameplay_authority()
                    or Managers.state.game_session ~= current.session then return end
                current:scan_existing()
                current:remove_pending()
            end,
        },
    },
}
