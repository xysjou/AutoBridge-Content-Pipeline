# 下一阶段停点：不要把 API key 发到聊天

本轮到 mock 交付为止。现在无需提供 key；即使环境中已有 key，代码也不会读取或调用。进入真实试点还需明确批准，不是放入 secret 就自动开始。

准备真实试点时：

1. 打开 https://platform.openai.com/ ，进入项目设置，新建专用项目，例如 `AutoBridge-Pilot`；不要复用生产项目。
2. 在该项目的模型访问/Limits设置中，仅启用拟用 `gpt-6-luna` 与 `gpt-6.1-terra`。账号是否支持尚未核实；若不可选，停止并重新审定型号与价格，不自动换型号。
3. 在该项目 API keys 创建专用 key，选择 Restricted。仅授予创建 Responses 所需 Write/Request权限；若界面使用 RBAC，项目角色与key权限均须满足。只有确实需要 `/v1/models` 只读可用性检查时才加 Models Read。Files、Assistants、Batch、Fine-tuning、管理权限等设为 None；不为省事开放 All。具体权限名以当前控制台为准，不能保证每个账户的界面相同。
4. 在 GitHub 仓库 https://github.com/xysjou/AutoBridge-Content-Pipeline/settings/secrets/actions 进入 Settings → Secrets and variables → Actions → New repository secret，Name填 `OPENAI_API_KEY`，Secret填刚生成的key并保存。不要填到 Variables、代码、issue、PR或聊天。若生成时未保存，撤销重建，不尝试找回日志。
5. 只回复“专用项目和 secret 已设置”；不要回复 key 本身。后续由 Work Cloud继续完成已列出的真实适配器/计费与状态校验，并在发出第一个真实请求前再次核对明确的真实调用授权。

项目支出告警只通知，不会停请求。官方现行文档还提供可选项目 hard limit，但执行有延迟，可能轻微超额；它是月度平台控制。程序的 US$3 是整个本次试点生命周期预算，不按天、聊天、文章或重跑刷新；两者不是同一控制。建议专用项目配置告警和可用的硬限额作为第二层保护，不能用它们替代调用前的持久化预留账本。

下一次批准范围应明确为：在独立分支完善真实适配器、核实账号模型可用性，在全项目US$3上限内做两篇英文真实试点并提交draft PR；仍不合并、不发布、不改CURRENT、不启用定时。只有先完成真实成本/CAS/来源/独立审核门，才能请求这个批准。本轮不索取真实调用批准，也不执行真实调用。
