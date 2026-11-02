# 运行与密钥交接 — 仍停在真实调用之前

目前可实际执行的入口是隔离分支中的：

`python -m cloud_pilot.live preflight`

这是只读离线预检，不读取密钥。真实执行入口已编码为 `execute`，但当前空 intake 与 disabled permit 会先阻断。不能把代码通过测试说成已接通真实模型。

## 推荐的受保护运行方式

Work Cloud继续负责代码、审计、测试与PR；拟由获准的 GitHub Actions 手动任务读取 repository secret。`runtime/manual-api-pilot.yml.template` 是未安装的审阅模板，不在 `.github/workflows`，并额外设有 `if: false`；当前不会触发，也没有改变任何现有 workflow。

GitHub的workflow_dispatch要求workflow文件存在于默认分支。当前main没有这份真实API工作流，而用户禁止推main/合并。因此不能在现有限制下声称已经有可点击的Actions真实启动按钮。下一步必须单独决定：批准最小的默认分支启动入口，或提供经过核实的其他受保护云端运行环境。此轮不选择、不启用、不修改main；也不以push事件偷偷代替手动触发。

## 用户保存密钥的准确位置

1. 在 https://platform.openai.com/ 选择接收API额度的组织，新建专用项目 AutoBridge-Pilot。
2. 仅启用拟用模型 gpt-6-luna 和 gpt-6.1-terra；账号是否可用仍未验证。
3. 创建 Restricted 项目key，开启创建Responses所需Write/Request权限；如需GET models再开启Models Read；其他无关权限None。不要把key发到聊天。
4. 打开 https://github.com/xysjou/AutoBridge-Content-Pipeline/settings/secrets/actions 。在 Settings → Secrets and variables → Actions → New repository secret 中新增 `OPENAI_API_KEY`，Secret填API key。
5. 只回复“OPENAI_API_KEY已设置”。GitHub Secret不会自动进入Work Cloud沙箱，连接器也不能读取其明文；真正运行时由获准的运行环境注入。

后续拟用环境 `autobridge-pilot` 还须在仓库 Settings → Environments 配置所需的人工审批与隔离分支限制，核实平台是否支持；本轮没有创建环境或宣称保护已生效。模板使用自动颁发的 github.token（仅contents/write和pull-requests/write），不要求另建长期GitHub个人token。

## 首次真实请求授权必须绑定的内容

- 两篇具体英文试点的 intake、精确授权来源URL/跳转URL，以及独立语义去重结论。
- 当次读取的main SHA、规则文件哈希、24小时内官方价格快照、经过审核的代码exact SHA。
- 专用项目模型可用性和受保护运行环境的实际验证。
- 试点全生命周期US$3；不合并、不改CURRENT、不发布网站、不启用生产定时。

只有用户明确批准真实调用后，才准备 `approved-permit.json` 并将它的SHA256保存在受保护环境secret `AUTOBRIDGE_LIVE_APPROVAL_SHA256`；将代码SHA设为环境变量 `AUTOBRIDGE_APPROVED_CODE_SHA`。不要自行把 disabled example 中authorized改为true。代码会在读取API key之前核对许可、plan、prices、rules、code SHA和有效期；运行前每次再核对main。

平台Spend alert只通知；官方还支持可选hard limit，但执行有延迟。它们均不能代替程序的持久化调用前预留。此次真实API花费0，没有进行GET models、Responses、token-count或真实汽车来源获取请求。
