# HCM 的 Nexus 自动发布

Nexus 模组页为 https://www.nexusmods.com/warhammer40kdarktide/mods/1267 。此工程采用官方 v3 Upload API，无需读取浏览器登录信息。官方接口文档：https://api-docs.nexusmods.com/ ；官方 GitHub Action：https://github.com/Nexus-Mods/upload-action 。

## 首次配置

用模组作者或有发布权限的协作者账号登录 https://www.nexusmods.com/settings/api-keys ，在页面下方生成个人 API Key。将密钥保存在仓库外的 `%USERPROFILE%/.config/nexusmods/HCM.env`，内容为 `NEXUSMODS_API_KEY=你的密钥`。也可用同名环境变量配置，环境变量优先。不要把实际密钥填进 Git 文件或命令行参数。

## 打包和发布

1. 执行 `python tools/release.py`。完整离线检查通过后，重新校验既有测试候选包，将其原样复制到 `release/4.6.0-test.3/`。上传 ZIP 的 SHA-256 必须与 `publishing/release.json` 中记录的已验证候选一致，不能重新压缩或追加作者文档。
2. 执行 `python tools/publish_nexus.py`。默认只校验本地 ZIP、正文、简介、更新日志和发布类别，不发网络请求。
3. 执行 `python tools/publish_nexus.py --publish`。脚本认证并核对模组，检查远端是否已有同版本，通过官方分片接口上传 ZIP，完成上传并等待处理，创建新的 Optional Files 文件，加入本次英文 changelog，读回文件版本确认。
4. 上传回执保存在 `build/nexus/4.6.0-test.3/receipt.json`。它不包含密钥或签名存储地址；保留上传与文件 ID，可用于检查未完成的步骤。若写入请求结果不明，脚本不会盲目重试或重复上传。

此测试包不成为默认下载，不改变模组页的正式版本，不归档既有 Main Files。上传完成不代表病毒扫描通过；仍需检查 Nexus 的文件可下载状态。

本次已实际发布 `4.6.0-test.3`，文件编号 `8851`，并读回 Optional Files 类别、版本、非默认下载标志和 `246323` 字节的大小；本次英文 changelog 已同步。当前账号未获 Premium API 下载权限，下载链接接口返回 403 并说明需在网页获取链接，因此未通过 API 下载后重新比对远端哈希，不能把这个 403 当作文件被隔离。发布记录见 `docs/validation/nexus-4.6.0-test.3-20261007.json`。

## 页面说明

官方上传接口处理安装文件和版本 changelog。主页面 Description 与 Short description 仍需在 Nexus 网页填写：分别使用发布目录中的 `description.bbcode.txt` 与 `summary.en.txt`。当前电脑操作工具无法可靠识别浏览器网址，已停止网页自动化，不能声称主页面文案已同步。

`release/发布编号/` 始终只有一个 ZIP 和三份说明文件。内部上传配置在 `publishing/nexus.json`，凭据在仓库外，检查与回执在被 Git 忽略的 `build/`。
