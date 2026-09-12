# Condition import behavior

HCM reads SoloPlay's ordered Havoc and general circumstance lists. A row is eligible only when its circumstance and referenced mutators exist in the current game. Non-default environment themes and difficulty modifiers remain in their dedicated mission selectors. The extended catalog is reversible when HCM is disabled.

Havoc entries retain their SoloPlay category. Native flash-mission entries appear under Auric/Maelstrom; event IDs or event descriptions identify the event group. Other eligible rows appear under General. HCM does not register condition aliases, copy external mod definitions or change network lookup tables.

Selected native mutators load once per identifier. Native condition order and replacement semantics remain significant; pickup extras use additive amounts, health-station/mission settings use native overrides, and the last selected hazard settings win. Mission-owned condition event listeners are released at teardown.

The old selection migrates valid IDs into SoloPlay's HCM selection key. Missing aliases are skipped, and the original legacy setting remains available. Default multipliers preserve native source templates; HED is optional.
