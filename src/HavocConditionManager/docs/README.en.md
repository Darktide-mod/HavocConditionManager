# Havoc Condition Manager

Choose SoloPlay mission conditions and adjust enemy pacing. HCM provides broad controls; the optional Havoc Enemy Director edits individual fields in the same game templates. Realms sessions use the local host's settings.

Use HCM Overall tuning → Random seeds for condition-event probability streams. Use HED Director → Seeds for its scheduling streams and native roamer layout, with separate switches. Off follows the mission seed; HCM draws a fallback once per mission if that seed is unavailable. On enables integer input from 1 to 2147483646. Turning off retains the saved number. Changes apply next mission. These seeds do not choose the mission map or control all native horde, specialist, monster and scripted-event randomness. Lua authors using native math.random directly keep that separate random source.

## DIY conditions

DIY conditions share the main Conditions list with native conditions. Filters appear in this order: Havoc, Maelstrom, Events, DIY, All, Enabled. Loaded DIY entries also appear in All and Enabled when selected. Hover to read targets, values and trigger details; scroll through long descriptions. HCM applies every enabled checked condition without a quantity quota.

Conditions can select players or enemies by breed and tags, adjust initial enemy health, apply passive stats and keywords, react to native combat events, schedule temporary stacks, change supported resources and statuses, and emit named signals. Conditions can also pause supported native pacing categories or request bounded HED reinforcements. Timing, chance, cooldowns, per-owner/global scope and trigger limits are explicit fields.

Havoc Enemy Director is optional for reinforcement actions. HED deployment and native-template rules can check active DIY condition IDs and named signals. Ordinary DIY reinforcements carry their source through the shared spawn path. Queue admission still follows native placement, capacity and pacing checks.

Three-language guides, templates, the complete native identifier catalog and a row-by-row assessment of 120 supplied design rows are included in docs/diy. The assessment separates supported, partial, adapter-dependent and underspecified designs; the templates do not implement every proposed effect. Realms clients receive host-approved effects for their own player and clear stale effects when synchronization expires.

## Conditions and mission setup

- Import the current SoloPlay condition list and group eligible entries as Havoc, Auric/Maelstrom, events and general conditions.
- Add or remove conditions without a fixed slot count. A shared native mutator loads once even when several selected conditions include it.
- Choose mission, faction, difficulty and environment in the mission page. An unsupported map/environment pair falls back to Default.
- Apply the selected native pickup, health-station and hazard settings. Native replacement rules still govern conflicting effects.

Available entries depend on the installed game and SoloPlay. HCM supplies no separate Havoc or Maelstrom condition definitions.

## Overall tuning

Open HCM in Mod Options and select Overall tuning. The main page shows the intensity slider and linked values. The 20 individual controls are in Advanced settings; hover titles for details.

Level 1 preserves the native spawn configuration for the selected mission, difficulty and conditions when HED overrides are also at baseline. Levels 2–10 increase ordinary enemies gradually and increase elite, specialist and monster pressure more strongly. Intermediate levels interpolate between the following anchors; integer allowances may remain equal across adjacent levels. A level describes a preset, not a measured difficulty or kill-count multiplier.

- Route population: 1× / 1.2× / 1.5× at levels 1 / 5 / 10. Camp count and event budget: 1× / 1.1× / 1.25×.
- Ordinary enemies per horde or trickle wave: 1× / 1.1× / 1.25×. Horde frequency: 1× / 1.08× / 1.2×; trickle frequency: 1× / 1.05× / 1.1×. Ordinary horde wave counts stay native.
- Existing elite members in horde compositions and patrol teams: 1× / 1.75× / 3×. Ordinary members keep their separate counts. A patrol with 8 elites and 8 ordinary troops requests 24 elites and 8 ordinary troops at 3× elite members. Roamer packs and point-budget events keep native selection ratios and grow through population and budget.
- Specialist capacity: 1× / 2× / 3×; refill frequency: 1× / 2× / 3.25×; surge allowance: 1× / 3× / 6×. Capacity and frequency together represent nominal scheduling capacity, subject to native pauses, player-dependent limits and spawn checks.
- Map monster encounter allowance: 1× / 4× / 8×. Elite patrol encounter allowance: 1× / 3× / 6×. These counts are separate from patrol team size.
- Coordinated tactic allowance: 1× / 2× / 3×. Supported tactics' upper combat-load limit rises from 35 to 70 to 105. The medium-load lower bound stays at 8; capable-player, pacing-stage and other native conditions still apply. HED can append requirements to the adjusted conditions or explicitly replace them.
- General combat capacity: 1× / 1.5× / 2×; recovery duration: 1× / 0.85× / 0.7×. At level 10, the living-plus-queued admission threshold is 290 and the difficulty-5 horde threshold is 190. Condition encounter counts, escalation, mission objectives and separate scripted-event limits retain their settings.

Patrols and monsters first use unused authored encounter points. Overflow waits for valid hidden navigation positions. Both queues share a minimum 20-second interval and receive turns weighted by their starting overflow quotas. A ready queue gets a turn after at most three successful admissions of the other queue. If one class is blocked or fails to spawn, the other may try; only successful spawns consume allowance. Supplemental bosses wait while three ordinary map monsters are alive, and at most two supplemental patrol groups remain active. Native pauses, positions and mission length can still leave allowance unused.

Route and supplemental elite patrols create one member at a time, at least 0.15 seconds apart, while retaining native breeds, group sounds and unit initialization. Route patrols keep native formation links and walk towards the verified player floor. Supplemental patrols use the current combat target. Ahead positions must remain hidden from every valid teammate, at least 35 metres from each teammate including bots, and 30–120 metres ahead along the main path. If these positions are unusable, a verified nearby hidden point may be used instead: at least 20 metres from every teammate and within 60 metres of the nearest teammate, including side or rear positions. Unavailable positions delay remaining members. Safe-zone restrictions and finite encounter quotas still apply; a patrol consumes its encounter allowance only after all members are created.

Extra patrols, supplemental encounters and recycled enemies validate positions before any unit is created. A candidate needs a complete route from the enemy position to the current player's actual navigation floor. Terrain and door connections follow native pathfinding, without additional HCM door-state or opening-permission checks. Ordinary extra encounters prefer hidden points about 60 metres ahead; recovery requests prefer nearby candidates when a new point is needed, while reusing an already valid shared point. Nearby points remain hidden from every valid teammate, at least 20 metres from each and within 60 metres of the nearest. Unfinished or failed checks never spawn a test enemy. Each formation point must connect to its approved anchor, and actual creation rechecks path validity, player position, distance and visibility. Deferred replacement requests repeat validation when the native queue consumes them.

Placement shares one asynchronous route search and one live path. New searches start at most once per second. Bounded candidates include up to two authored forward points, two authored nearby points and four local mesh points. Nearby authored points favor the player's floor. Local sampling checks at most eight offsets around the real player floor, alternating 28- and 40-metre radii, no more than once every four seconds; a projected point still needs the complete route check. Successful routes are reused across members, and short batches of at most eight replacement positions avoid oversized footprints. The game thread never waits for a search, and recovery decisions still do no pathfinding.

Ordinary hordes and mission events use native position selection, authored door groups and the adjusted template pacing. This includes the Courtroom ascender event and its native rear entrances. HCM adds no navigation-route approval or waiting period to those spawns.

Selecting a level replaces all 20 HCM values; individual edits show Custom. Exact saved presets from the previous curve migrate to the same level on the new curve. Other custom values and HED overrides remain. Changes save automatically and apply next mission.

Due spawners run across successive updates while retaining queues, order and completion callbacks. Ordinary and coordinated hordes defer their next wave while the central queue is congested. Temporary pacing refusals preserve unspawned map encounters. Repeated Buff-capacity warnings are summarized; the Buff event pool remains 300.

Known pacing patrol followers that lose their leader can rejoin native combat once, with recoveries spaced at least 0.15 seconds apart. This uses the existing perception updates and native alert/aggro methods. Mission ownership, player-owned units and traversal protections still apply, and a patrol being recycled is not woken by its own staged removal.

## Automatic rear-enemy recovery

Recovery runs on the local mission host at every intensity level, including level 1. Common enemies and elites that have been observed in combat, or belong to a known pacing patrol, can retire after 30 seconds out of contact while at least 35 metres from every living teammate, including bots. Samples are five seconds apart; queueing can extend the delay. Actual damage restarts the same timer, and current distance and immediate native visibility are checked again before removal.

Movement, loops, missing route data, patrol flags and the overall scripted-event state do not exempt committed enemies. Patrol members qualify individually. Native common enemies and elites are recognized at creation, including non-objective event waves; recovery does not depend on a spawn-source whitelist. Required mission targets, externally controlled or player-owned units, invulnerable enemies, specialists, bosses, captains and companions remain protected. A mark or persistent effect alone does not grant permanent immunity; ongoing damage resets the timer.

Untouched native ambient roamers can also enter recovery when their authored position is at least 60 metres behind the native cached rear-player progress on a linear map and they remain within 12 metres of that position. They must meet the same 35-metre, visibility and 30-second quiet conditions. This reads existing progress without projecting enemy positions or searching a route. Ahead encounters, enemies between teammates, roamers that have moved too far from their recorded position, open maps and uncertain records retain native handling. Returning teammates cancel admission; a roamer already retired cannot reactivate while engine deletion is pending.

The native perception schedule feeds a fixed ring of at most 64 ready unit references. There is no motion history, main-path projection, remaining-path query, separate pathfinding probe or whole-map scan in the recovery decision. Final attempts are at least 0.25 seconds apart, at most four per second and one per update, with native visibility checks against living teammates. Slow frames never trigger a catch-up burst. Known orphaned patrol followers can still rejoin native combat once through the existing alert/aggro methods.

Recovery uses native removal and recreation. Each original provides at most one replacement of the same breed. Compatible allowances combine into batches of up to 64 members, with at most 32 records and 256 pending units. Accepted allowances remain available until mission end instead of expiring during a blocked encounter. Credits beyond the fixed limits are discarded. Ready batches take turns, so a paused class cannot block later ready classes. Replacement requests are at least 0.25 seconds apart, at most four per second and one per update, with one HCM replacement request in flight globally. There is no extra eight-second gap between batches. Native pacing, capacity, safe-zone, distance, visibility and pre-spawn reachability checks still apply. Failed requests retain their allowance; a replacement never earns another replacement. Health is initialized again and random modifiers may be rerolled; available original health multipliers are retained. Rotten-armour retirement preserves existing non-death cleanup handling.

## Fine editing and saved settings

Havoc Enemy Director adds Detailed tuning. HCM first supplies broad changes; a HED field override then sets that field's exact value. Native difficulty and condition modifiers can still change the final result. Mission combat-node budgets are a specific case: HCM's event-budget multiplier scales the final budget and its native cap after the node's base values and native modifiers.

Values save automatically and apply when the next mission starts. A running mission retains its starting configuration. DMF switches apply immediately in the hub and are deferred during a mission. Disabling HCM restores SoloPlay's menu and suspends HED for later missions.

The first use imports valid native IDs from the previous HCM selection. Retired condition aliases are omitted; the original saved value is retained. Old category multipliers and custom-generator settings are not converted into native template edits. Start from the new defaults and configure the controls before your next mission.

English, Simplified Chinese and Traditional Chinese follow the game language. Native identifiers remain visible where needed to distinguish exact templates.

Package IDs, versions, dependencies, conflicts and capabilities are validated. Selected local Lua runs on the authority with separate module environments, resource snapshots and cleanup callbacks. Package updates apply next mission. JSON, Lua, resources and dependency fingerprints participate in Mortis room compatibility; network messages never carry executable Lua. Three-language API guides and complete examples are included.

DIY manager reads No healing directly from the mod folder, with no template extraction or copied built-in files. Built-in packages remain loaded in the manager; gameplay effects still require selection on the Conditions page. External packages remain under %APPDATA%/Fatshark/Darktide/HavocConditionManager/diy/packages. Refresh after adding or editing packages; active missions keep their starting snapshot. Older external copies with the same package ID remain on disk but the built-in or companion source takes precedence.

Frenzied assault and its compiled animation resources are distributed separately in HavocConditionPacks: https://github.com/Darktide-mod/HavocConditionPacks . HCM does not ship PowerShell/CMD installers or animation patches. Its package loading API still supports authored Lua and optional resource integrations. This packaging change is not a guarantee of Nexus approval.

## Requirements

Darktide Mod Loader, Darktide Mod Framework and SoloPlay are required. Realms is optional for co-op. Havoc Enemy Director is optional. Other mods replacing the same native templates or scheduling methods may conflict.

## Vortex installation

- Close the game and install the requirements. Import this ZIP with Install From File, enable it and select Deploy Mods.
- Enable HavocConditionManager in Load Order after SoloPlay. Place the optional HavocEnemyDirector after HavocConditionManager.
- Restart the game and open Havoc Condition Manager in Mod Options.

## Manual installation

- Close the game. When upgrading, remove the previous HavocConditionManager installation folder before extracting the new ZIP; saved settings are stored separately.
- Extract the ZIP into Darktide/mods, producing mods/HavocConditionManager.
- Add HavocConditionManager on its own line after SoloPlay in mods/mod_load_order.txt. Place the optional HavocEnemyDirector after it.
- Restart the game and open HCM in Mod Options.

## Credits

SoloPlay and the original UI foundation: deluxghost. Native game systems and assets: Fatshark. Game-source reference: Aussiemon/Darktide-Source-Code.
