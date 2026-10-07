-- Selected production methods from installed SoloPlay 2.6.9 and Realms.
-- Native transport, actors and mission VO are test boundaries.
local mod=get_mod("SoloPlay")
local HOST_TYPES=require("scripts/settings/network/matchmaking_constants").HOST_TYPES
local SoloPlaySettings=local_host_solo_settings
local _mission_giver_vo_override=function() return "sergeant_a" end
local ConnectionHost={}
mod.is_soloplay = function ()
	if not Managers.state.game_mode then
		return false
	end
	local game_mode_name = Managers.state.game_mode:game_mode_name()
	if game_mode_name == "training_grounds" or game_mode_name == "shooting_range" then
		return false
	end
	if not Managers.multiplayer_session then
		return false
	end
	local host_type = Managers.multiplayer_session:host_type()
	return host_type == HOST_TYPES.singleplay
end

mod.has_local_gameplay_authority = function ()
	local multiplayer_session = Managers.multiplayer_session
	if not multiplayer_session then
		return false
	end

	local host_type = multiplayer_session:host_type()
	if host_type ~= HOST_TYPES.singleplay and host_type ~= HOST_TYPES.player then
		return false
	end

	local game_session = Managers.state and Managers.state.game_session
	return game_session and game_session:is_server()
end

mod.gen_havoc_mission_context = function ()
	local rank = mod:get("havoc_difficulty")
	local challenge, resistance
	if rank <= 10 then
		challenge = 3
		resistance = 3
	elseif rank >= 11 and rank <= 20 then
		challenge = 4
		resistance = 4
	elseif rank >= 21 and rank <= 30 then
		challenge = 5
		resistance = 4
	else
		challenge = 5
		resistance = 5
	end

	local mission, params = mod.parse_mission_params(mod:get("havoc_mission"))
	local faction = mod:get("havoc_faction")
	local circumstance1 = mod:get("havoc_circumstance1")
	local circumstance2 = mod:get("havoc_circumstance2")
	local theme_circumstance = mod:get("havoc_theme_circumstance")
	local difficulty_circumstance = mod:get("havoc_difficulty_circumstance")
	local theme = SoloPlaySettings.lookup.theme_of_circumstances[theme_circumstance]

	local chosen_circumstances_table = {}
	if circumstance1 ~= "default" then
		chosen_circumstances_table[#chosen_circumstances_table+1] = circumstance1
	end
	if circumstance2 ~= "default" and circumstance2 ~= circumstance1 then
		chosen_circumstances_table[#chosen_circumstances_table+1] = circumstance2
	end
	if theme_circumstance ~= "default" then
		chosen_circumstances_table[#chosen_circumstances_table+1] = theme_circumstance
	end
	if difficulty_circumstance ~= "default" then
		chosen_circumstances_table[#chosen_circumstances_table+1] = difficulty_circumstance
	end
	-- Keep empty lists between semicolons; the native splitter drops empty fields but parses ":" as an empty list.
	local chosen_circumstances = #chosen_circumstances_table > 0 and table.concat(chosen_circumstances_table, ":") or ":"

	local chosen_modifiers_table = {}
	for modifier_name in pairs(SoloPlaySettings.lookup.havoc_modifiers_max_level) do
		local modifier_id = NetworkLookup.havoc_modifiers[modifier_name]
		local level = mod:get("havoc_modifier_" .. modifier_name) or 0
		if level > 0 then
			chosen_modifiers_table[#chosen_modifiers_table+1] = string.format("%d.%d", modifier_id, level)
		end
	end
	local chosen_modifiers = #chosen_modifiers_table > 0 and table.concat(chosen_modifiers_table, ":") or ":"

	local data = string.format("%s;%d;%s;%s;%s;%s;%s;%s", mission, rank, theme, faction, chosen_circumstances, chosen_modifiers, challenge, resistance)

	local mission_context = {
		mission_name = mission,
		challenge = challenge,
		resistance = resistance,
		mission_giver_vo_override = _mission_giver_vo_override(mission, mod:get("havoc_mission_giver")),
		havoc_data = data,
		custom_params = params,
	}
	return mission_context
end

ConnectionHost.host_type = function (self)
	return HOST_TYPES.player
end
return ConnectionHost
