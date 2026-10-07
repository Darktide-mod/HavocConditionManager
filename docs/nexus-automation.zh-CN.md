# HCM 的 Nexus 自动发布

模组页：https://www.nexusmods.com/warhammer40kdarktide/mods/1267 。使用 Nexus 官方 v3 API，最新接口规范：https://api.nexusmods.com/openapi.yaml 。官方上传 Action：https://github.com/Nexus-Mods/upload-action 。不读取浏览器会话。

## 凭据

用模组作者或有发布权限的协作者账号登录 https://www.nexusmods.com/settings/api-keys ，在页面下方生成个人 API Key。将密钥保存在仓库外的 `%USERPROFILE%/.config/nexusmods/HCM.env`，内容为 `NEXUSMODS_API_KEY=你的密钥`。也可使用同名环境变量，环境变量优先。实际密钥不进入 Git 文件、命令行参数或回执。

## 发布步骤

1. 更新源码版本、publishing/metadata.json 和 publishing/release.json。正式版使用正式版本号与 Main Files；测试版使用测试版本号与 Optional Files。
2. 同步英文／简体中文长期正文、英文／简体中文简介，以及英文 changelog。主页面正文不放版本号或测试报告；这些内容放在 changelog。Nexus Short description 将两种语言合并为不超过 350 字符的一段。
3. 执行 `python tools/release.py`，完整检查通过后生成一个 ZIP 与三份发布文案。runtime_only 排除作者手册和示例，保留运行脚本、内置 DIY、加载器、metadata 和 attribution。测试候选有 candidate_sha256 时原样复制；正式包重新校验源码与诊断残留后构建，不修改历史候选。
4. 执行 `python tools/publish_nexus.py`，默认只检查本地，不发网络请求。
5. 执行 `python tools/publish_nexus.py --publish`。认证并核对模组及既有文件，上传分片并完成处理，创建新文件或既有文件的新版本，然后同步本次英文 changelog、中英文 BBCode 正文和双语简介。
6. 读回文件版本、类别和默认下载标志，再检查主页面正式版本、正文、简介和旧版归档。回执在 `build/nexus/发布编号/receipt.json`，不进入发布目录。写入请求结果不明时，不能盲目重试。

## 正式版策略

当前正式版为 4.6.1，发布资料目录为4.6.1-r2，属于 Main Files 和默认下载。r2仅表示补齐帝皇之光说明的文案修订，79个运行文件与已验证的本地4.6.1检查点一致。publishing/nexus.json 指定既有文件链及此次被替换的4.6.0版本；准备下一版时应先读回当前正式版本，再更新previous_version_id。创建新版本时使用 `archive_existing_file=true`、`primary_mod_manager_download=true` 和 `update_mod_version=true`。先准备并校验新包，再替换旧版本；实际归档状态必须从远端读回确认。

本次读回确认：正式文件8853已成为 Main Files／默认下载，网页版本为4.6.1，4.6.0（8852）由API归档，全部12份旧文件均为Archived。中英文正文、双语简介和本次更新记录与本地发布文案一致，验证记录在docs/validation/nexus-4.6.1-20261007.json。相同安装包也发布为GitHub v4.6.1，服务器返回的SHA256摘要与本地一致。

`archive_existing_file` 只归档指定的上一版本，不会归档整个历史链。历史4.6.0发布时，上一正式文件8275（4.5.0）由API归档；旧测试版8851与更早的8062、8012、8011、8003由用户在网页归档并逐份读回确认。当前官方v3规范未提供独立归档接口，先前的网页电脑操作被用户按Esc停止，因此那些历史文件由用户完成归档。此次无需浏览器操作。

批量移动版本接口返回未包裹 `data` 的结果；主页面编辑成功返回无正文的 204。存储分片 PUT 的暂时失败可以用相同字节重试；完成上传的 POST 与公开创建文件的 POST 不盲目重试。重启流程先查远端版本与上传状态，避免重复发布。

旧 4.6.0-test.3 包及其本地记录仍保留用于追溯。网页长介绍与简介通过官方 `PATCH /mods/{id}` 更新，成功响应为 204；不依赖之前已停止的电脑网页自动操作。

上传完成不代表病毒扫描通过。当前账号没有 Premium API 下载权限；下载链接接口的 403 说明需要在网页获取链接，不代表文件隔离。完整发布验证记录位于 docs/validation；build 下的回执保留上传 ID 以处理未完成步骤。
