local mod = get_mod("HavocConditionManager")
local localization = {
    frenzied_restart_required = {
        en = "Frenzied assault changed from %s to %s. Restart the game before starting another mission.",
        ["zh-cn"] = "狂暴攻势从 %s 更新到 %s，请重启游戏后开始新任务。",
        ["zh-tw"] = "狂暴攻勢從 %s 更新到 %s，請重新啟動遊戲後開始新任務。",
    },
	mod_name = {
		en = "Havoc Condition Manager",
		["zh-cn"] = "浩劫状况管理器",
		["zh-tw"] = "浩劫條件管理器",
	},
	open_condition_manager = {
		en = "Expanded local game interface",
		["zh-cn"] = "扩展本地游戏界面",
		["zh-tw"] = "擴充本機遊戲介面",
	},
	open = {
		en = "Open",
		["zh-cn"] = "打开",
		["zh-tw"] = "開啟",
	},
	default_text_select_to_add = {
		en = "Select a condition to add",
		["zh-cn"] = "选择要添加的状况",
		["zh-tw"] = "選擇要新增的條件",
	},
	default_text_select_to_remove = {
		en = "Select a condition to remove",
		["zh-cn"] = "选择要删除的状况",
		["zh-tw"] = "選擇要移除的條件",
	},
	label_add_havoc_circumstance = {
		en = "Add Havoc condition",
		["zh-cn"] = "添加浩劫状况",
		["zh-tw"] = "新增浩劫條件",
	},
	label_remove_havoc_circumstance = {
		en = "Remove Havoc condition",
		["zh-cn"] = "删除浩劫状况",
		["zh-tw"] = "移除浩劫條件",
	},
	label_selected_havoc_conditions = {
		en = "Selected Havoc conditions: %d / %d",
		["zh-cn"] = "已选择浩劫状况：%d / %d",
		["zh-tw"] = "已選擇浩劫條件：%d / %d",
	},
	message_havoc_condition_added = {
		en = "Added Havoc condition: %s",
		["zh-cn"] = "已添加浩劫状况：%s",
		["zh-tw"] = "已新增浩劫條件：%s",
	},
	message_havoc_condition_removed = {
		en = "Removed Havoc condition: %s",
		["zh-cn"] = "已删除浩劫状况：%s",
		["zh-tw"] = "已移除浩劫條件：%s",
	},
	message_havoc_condition_duplicate = {
		en = "That Havoc condition is already selected.",
		["zh-cn"] = "该浩劫状况已经添加。",
		["zh-tw"] = "該浩劫條件已經新增。",
	},
	message_havoc_condition_limit = {
		en = "A maximum of %d primary Havoc conditions is supported.",
		["zh-cn"] = "最多支持 %d 个主要浩劫状况。",
		["zh-tw"] = "最多支援 %d 個主要浩劫條件。",
	},
	message_havoc_condition_minimum = {
		en = "Keep at least one primary Havoc condition.",
		["zh-cn"] = "至少需要保留一个主要浩劫状况。",
		["zh-tw"] = "至少需要保留一個主要浩劫條件。",
	},
}

localization.mod_name = { en = "Havoc Condition Manager", ["zh-cn"] = "浩劫词条管理器", ["zh-tw"]="浩劫詞條管理器" }
localization.mod_description = { en = "Open the local-game interface: mission setup, SoloPlay conditions and Overall tuning. Optional HED adds Detailed tuning. Changes apply next mission.", ["zh-cn"] = "打开本地游戏界面：任务设置、SoloPlay 词条与整体调节；可选 HED 增加详细调节。修改在下一局生效。", ["zh-tw"] = "開啟本地遊戲介面：任務設定、SoloPlay 詞條與整體調節；可選 HED 新增詳細調節。修改在下一局生效。" }
localization.toggle_next_mission = { en = "Switch saved. The current mission keeps its configuration; the new state applies next mission.", ["zh-cn"] = "开关已保存；当前任务保持原配置，下一局应用新的开关状态。", ["zh-tw"]="開關已儲存；目前任務保持原配置，下一局套用新的開關狀態。" }
localization.page_home = { en = "Mission setup", ["zh-cn"] = "任务设置", ["zh-tw"]="任務設定" }
localization.page_conditions = { en = "Havoc conditions", ["zh-cn"] = "浩劫词条", ["zh-tw"]="浩劫詞條" }
localization.page_spawn = { en = "Enemy multipliers", ["zh-cn"] = "敌人生成倍率", ["zh-tw"]="敵人生成倍率" }
localization.select_all = { en = "Select all", ["zh-cn"] = "添加全部", ["zh-tw"]="新增全部" }
localization.clear_all = { en = "Clear selection", ["zh-cn"] = "清空所选词条", ["zh-tw"]="清空所選詞條" }
localization.selected_count = { en = "Selected", ["zh-cn"] = "已选", ["zh-tw"]="已選" }
localization.conditions_note = { en = "Click a condition to add or remove it. No slot limit. Native replacement and shared-effect rules still apply.", ["zh-cn"] = "点击词条添加或删除，翻页查看全部。保留原版同源效果的覆盖规则；环境与难度仍在任务页设置。", ["zh-tw"]="點選詞條新增或刪除，翻頁檢視全部。保留原版同源效果的覆蓋規則；環境與難度仍在任務頁設定。" }
localization.option_faction_switch = { en = "Switching factions", ["zh-cn"] = "阵营交替", ["zh-tw"]="陣營交替" }
localization.option_faction_combined = { en = "Combined factions", ["zh-cn"] = "阵营合流", ["zh-tw"]="陣營合流" }
for key,value in pairs(mod:io_dofile("HavocConditionManager/scripts/mods/HavocConditionManager/ui_localization")) do localization[key]=value end
for key,value in pairs(mod:io_dofile("HavocConditionManager/scripts/mods/HavocConditionManager/template_localization")) do localization[key]=value end
for key,value in pairs(mod:io_dofile("HavocConditionManager/scripts/mods/HavocConditionManager/diy/diy_localization")) do localization[key]=value end
return localization
