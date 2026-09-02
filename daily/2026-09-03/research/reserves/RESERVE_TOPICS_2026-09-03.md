# RESERVE TOPICS — 2026-09-03（备用候选包）

> 正式 20 个 MAIN 全部 READY 时，以下 4 个仅作备用（Research Status = RESERVE），不进入第二阶段默认写作队列；当某 MAIN 被拒/资料失效时按序递补。

## 车型备用（2）
| Article ID | Brand / Model | 类别 | Search Intent | 来源数 | 官方源 | Risk | 递补说明 |
|---|---|---|---|---|---|---|---|
| AB-260903-VR1 | Chery 瑞虎7 PLUS（2024/2025，1.6TGDI） | Compact SUV | 了解瑞虎7 PLUS 中国版参数（区别于历史已有的瑞虎8） | 4 | 否 | LOW | 与历史 Chery Tiggo 8 为不同车型，不构成重复 |
| AB-260903-VR2 | Zeekr 极氪001（2024-02 改款） | EV Liftback | 了解改款极氪001三电/800V 以评估高端纯电出口 | 4 | 否 | LOW | 2025 转 900V 为年款更新，写作须锁定 2024 款 |

## 采购指南备用（2）
| Article ID | Topic | 目标市场 | Search Intent | 来源数 | 官方源 | Risk | 递补说明 |
|---|---|---|---|---|---|---|---|
| AB-260903-GR1 | 欧盟 WVTA+GSR+网络安全(R155/R156)+电池护照时间线 | 欧盟 | 在 G03 认证体系基础上展开欧盟强制项与生效时间 | 4 | 否 | HIGH | 法规日期须以 EUR-Lex 原文终核，未核前仅框架 |
| AB-260903-GR2 | 哈萨克斯坦/乌兹别克斯坦进口清关与认证分国路径 | 中亚 | 区分 EAEU 成员（哈）与非成员（乌），避免一张 EAC 误用 | 4 | 是（商务部转引） | HIGH | 报废费/税率 TIME_SENSITIVE，须官方当期税则复核 |

## 递补规则
1. 任一 MAIN 出现 CONFLICT 无法消解、官方源缺失导致关键事实不可核验、或与新发现历史重复时，从同类型 RESERVE 递补。
2. 递补后须同步更新 daily_manifest.json（priority MAIN/status READY）与 RESEARCH_READY 计数。
3. RESERVE 不占用 20 个 MAIN 的 READY 名额，不得为凑数把 RESERVE 提前标 READY。