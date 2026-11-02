# 第二阶段交接 — 2026-11-02 / Work Cloud

状态：ADAPTER_IMPLEMENTATION_COMPLETE / OFFLINE_TESTED / REAL_CALL_NOT_AUTHORIZED。

启动时复核：

|对象|exact SHA|状态|
|---|---|---|
|main|92e97312f1f225023bd663ada41dfadfc9bfd848|未变|
|PR1 / feature/work-cloud-pilot-core-20261102|4419e40ff24d4f3ea14edf006e5cbb289dfe0072|草稿、未合并|
|PR2 / integration/work-cloud-pilot-m1-20261102（本轮父提交）|75d010eae1300532f6008988d01d65cdae3d1c86|草稿、未合并|

本轮新HEAD以PR2和最终任务答复为准，不在提交内伪造自身SHA。

仓库规则仍为Research1.1、Writing1.3。main未发生变化；核对了README、VERSIONING、LESSONS、Skills、最新适用交接的哈希，并复用本任务此前已完整读取的同版本规则。运行时每次请求完整加载 canonical rules，不用聊天摘要替代。未发现AGENTS或额外Skill reference文件。未修改Skills/LESSONS，也没有把新的工程测试当作已确认的编辑规则升级。

## 已完成的实际代码

1. `cloud_pilot/live/responses.py`：真实Responses POST代码、固定官方域、独立stateless角色请求；不自动重试。
2. `sources.py`：精确URL白名单、公网DNS校验、IP固定连接和TLS主机名核验、逐跳授权、访问/格式/大小/编码限制；保存原文哈希、文本哈希、时间、publisher/scope和不可变原文档案。
3. `stages.py`、`engine.py`：Research失败阻止Writing；Writing只交文章和证据，独立Review有自己的请求/response identity；哈希绑定；全文相似度；最多v1+两次返修；交付失败重用已完成模型结果。
4. `ledger.py`、`http.py`：真实GitHub Contents API CAS代码、单一程序真实费用账本、追加式事件/失败记录、原子结果与usage结算、内容寻址的大文件检查点、固定分支/路径、不可变候选、仅draft PR。
5. `__main__.py`：实际可运行的离线preflight；execute必须通过plan/pricing/rules/code SHA/受保护许可后才读密钥。没有任何自动启用路径。
6. `runtime/manual-api-pilot.yml.template`：未安装且if:false的运行方案；没有变动任何现有Actions文件。

## 实际验证

```sh
python -m unittest discover -s cloud_pilot/stage2_tests -v
python -m unittest discover -s cloud_pilot/tests -v
python -m cloud_pilot.pilot --verify
python -m cloud_pilot.live preflight
python -m compileall -q cloud_pilot/live
git diff --check
```

新增47项、原有41项全部通过（88项）。新测试包含真实线程CAS争用、发送前崩溃、发送后超时、提交成功但ACK丢失、未知usage、写入失败、整项目预算、最多两次返修、交付恢复、独立审核哈希与身份、来源SSRF/DNS/TLS/跳转/大小/编码边界。

两篇synthetic测试通过实际Responses适配器+mock HTTP走完6次角色请求，重跑不增加请求；这不是6次真实API调用，也不是实际文章。该测试的模拟结算US$0.029444仅在内存测试数据中，未计入真实账本。原M1 US$0.021也是mock。真实账本 `cloud_pilot/state/live-program.json` 当前0事件、US$0实际支出；整个本轮真实OpenAI请求0次。没有读取既有API key，没有探测models，没有调用token-count或真实汽车来源URL。

单次保守预留：Terra US$2.685，Luna US$0.2685；依据完整1,050,000上下文和8000最大输出、长上下文最高适用30m缓存写入/输出费率。回包按input/cache/read/write/output精确计费，reasoning不重复计。任何未知结果保留预留并停止全程序。预留可能让试点在实际支出达到US$3以前暂停，这是保守上限而不是承诺一定能在该上限内完成所有返修。

## 保留范围与运行副作用

main原有4874文件、93个CURRENT、174个版本文件不变；本轮亦不修改M1的40个文件。现有4个workflow保持原哈希。新增代码仅在cloud_pilot下，不触碰两个.migration触发路径；无push/PR触发新workflow、无schedule、无网站部署。上传前后回读远端HEAD及tree进行复核。

## 尚未完成 / 首次真实调用前必须具备

- 具体两篇真实英文试点的intake、每篇6来源/4归一机构、授权URL及跳转白名单，和独立语义去重结果。当前plan.pending.json为空，未假称完成真实Research。
- 专用OpenAI项目key、账号所选型号可用性验证；HTTP参数/usage字段在该账号上的真实接受情况仍未验证。PDF/非UTF8/JS渲染页面当前明确停止。
- 受保护云端执行环境的实际启用。当前CLI入口已可离线运行，但GitHub Secret不能直接注入Work Cloud。拟用Actions的workflow_dispatch要求默认分支有workflow；用户禁止修改/合并main，故不能在本轮启用。模板已准备，未作为可点击启动按钮交付。
- 明确的首次真实调用授权，绑定exact code SHA、plan、24小时内价格快照、规则与有效期。当前disabled permit保持false；没有自授HUMAN_REVIEWED/PUBLISH_APPROVED。

密钥位置和运行决策见 [STAGE2_RUNTIME.md](STAGE2_RUNTIME.md)。现在可以准备专用项目并把key保存到仓库Actions secret `OPENAI_API_KEY`；不要发到聊天。仅有key也不会开始运行。默认分支最小启动入口或其他受保护云端runner须另行决策，本轮不以任何方式绕过main禁令。

## 当前官方文档记录

价格/型号/上下文/TTL快照时间在 `runtime/prices-20261102.json`（UTC），每次模型请求都会检查24h有效性，未知型号/价格拒绝。

- https://developers.openai.com/api/docs/models/gpt-6.1-terra
- https://developers.openai.com/api/docs/models/gpt-6-luna
- https://developers.openai.com/api/docs/pricing
- https://developers.openai.com/api/docs/guides/prompt-caching （30m写费率1.25倍为总价，非附加费）
- https://developers.openai.com/api/docs/guides/migrate-to-responses （store:false）
- https://developers.openai.com/api/docs/guides/token-counting （上下文结构token不能用字符数猜测）
- https://developers.openai.com/api/docs/guides/rbac
- https://docs.github.com/en/actions/how-tos/manage-workflow-runs/manually-run-a-workflow （默认分支要求）

Responses超大API reference页面获取失败，改读取官方migration/结构化输出/token-counting文档；没有把失败页面当作已读取证据。账户可用性仍UNVERIFIED。
