# AutoBridge API 试点：预算停点（2026-11-03）

**尚无可交付的 API 文章。当前没有完成“两篇英文 + 12语种”的目标。**

修复代码：`99aaf70dce6ad5cd9552cb149360588c48b6ec87`。离线检查 167 项通过（79 多语种、47 Stage2、41 原始套件）。最新两项代码复审缺陷已修复并增加实际输入/恢复回归测试，但修复版尚待新的独立 API 复审，不能标成代码审核通过。

两篇选题独立去重通过：Q05 2026 BEV 的城市采购筛选决策、成品冷藏车的装运前验收演示与证据。通过回执 `resp_0cc8bc21bdea976e016ae979acb3a087d18779f96c09514f61` 已按实际请求、响应、来源和历史语料核验；技术基线变化时不会伪造新的付费回执。

| 项目 | 实际值 |
|---|---:|
| 用户已批准的整个试点累计上限 | US$3.000000000 |
| 累计已结算 | US$2.980099325 |
| 余额 | US$0.019900675 |
| 下一次请求所需保守预留 | US$0.284661250 |
| 本次预算停点新增付费生成 | 0 |
| 累计付费响应 | 20 |
| 未决/未知推理请求 | 0 |
| 实际 API 英文文章 | 0 |
| 实际 API 多语种文章 | 0 |

[实际预算停点运行](https://github.com/xysjou/AutoBridge-Content-Pipeline/actions/runs/41593146158) 在付费生成前停止，原因 `PROGRAM_CAP_EXCEEDED`。原 US$3 上限未提高、未按阶段/文章/重跑刷新，全部既有费用与回执保留。

登录和现有环境 API Secret 可用；阻塞来自任务预算及修复版待复审。文章发布、CURRENT 提升、人类审核和图片权利均未授权或完成。旧的聊天稿不能作为真实 API 生产结果。

## 费用用途

| 用途 | 付费调用数 | 累计美元 |
|---|---:|---:|
| 独立代码复审（gpt-6.1-terra） | 12 | 2.739887250 |
| 独立选题去重（gpt-6-luna） | 8 | 0.240212075 |

## 逐次已结算回执

| # | 操作 | 模型 | Response ID | 美元 |
|---|---|---|---|---:|
| 1 | activation-code:43d2af3ca9cfd29f6dd50357117a72515198ae75 | gpt-6.1-terra | resp_07f96fc8bf34f651016ae859a873ac87d1a45feff92bbdb6bf | 0.088774250 |
| 2 | activation-code:fa49a0d70b0afb5a5f76d86e369d6e4717dd7878 | gpt-6.1-terra | resp_01b77663746170ef016ae85e53ddac87d1b16b08a5028fa893 | 0.153316750 |
| 3 | activation-dedup:7ae3b0e6e2facdb0109f0358ebcc012ccfe9d7bdd952fcbf83632e88320a7027 | gpt-6-luna | resp_0cb502476a28dc0f016ae85ec3c8b087d1bd14ce7cd75fd8df | 0.017795425 |
| 4 | activation-code:672cbbfe01007e134a6cf0d144f897c25d4c1def | gpt-6.1-terra | resp_0ee7727ff1eba5dc016ae9477f40dc87d1a0d1dcb747d9d65c | 0.164813000 |
| 5 | activation-code:b1df1dfcef2694d6024119d375a7e39577a07e3e | gpt-6.1-terra | resp_0a5fe5ff9adaed51016ae94f45ff7c87d1913894a3743a60ad | 0.231231750 |
| 6 | activation-code:ac1303e64dc595a35d8c978b9792e51cd1443ff9 | gpt-6.1-terra | resp_0e1da463929e02d3016ae95bd0a88c87d19650f491555f72c5 | 0.235524250 |
| 7 | activation-dedup:bfedff2f808d72860e1a47919695f21082cd8be71a100285fca35416dceba5f3 | gpt-6-luna | resp_02c32733b0a2772a016ae95c4e0ee487d191c1fd1ced189647 | 0.022031050 |
| 8 | activation-code:bf787e70837dbfa9217299d16aed55fa98078d93 | gpt-6.1-terra | resp_07a73bc4b76cd52e016ae95f8a8e4087d183cb12f08e6ef8bf | 0.239364250 |
| 9 | activation-dedup:e7f60fa19a38d933b7e1eb9cf6fe8ca288cb3a163665c1bfa3af987e2aab92ab | gpt-6-luna | resp_00be06ae07043e97016ae95fe5516487d196d6378502508edc | 0.023147300 |
| 10 | activation-code:831e42fb5aca58de02078badf651e226d6d1eba4 | gpt-6.1-terra | resp_09333204076948df016ae964c416c487d29bd9b51ebae1099d | 0.244233000 |
| 11 | activation-dedup:21b9085739a51b95e24b86401ef9a4fe0985417576bb430f452a9888ac7784b2 | gpt-6-luna | resp_06d8a3bd0459d97b016ae96527524887d296706cde4c2c8725 | 0.026277050 |
| 12 | activation-code:e59f6fa1a028dd1705f17c228a5742d5995d78ee | gpt-6.1-terra | resp_00d8f5d212734a78016ae96d4939c887d28c69a0cf28918e48 | 0.246971750 |
| 13 | activation-dedup:ab333fcd192f8670c1f2415412f2a9c8e7b05b239b2cef5fe4837cdb5af23854 | gpt-6-luna | resp_06ebb34d1fb0da48016ae96daab0b487d2a297376f7a707215 | 0.025963925 |
| 14 | activation-code:12128a37394445f66c8cba08fbf109e2158b617a | gpt-6.1-terra | resp_02be6de1f7d56798016ae9709d862c87d184468f65d65a5bfa | 0.251976750 |
| 15 | activation-dedup:8f704e502568872606725756f84427dce7c9a7db640b2bd64b5af82658e4c443 | gpt-6-luna | resp_051f577e6a2e08e8016ae970f5c2b487d19d41381764d55dbe | 0.025929800 |
| 16 | activation-code:7fc794a55b09c1b09ffd21a6d0c412eb5c46b0b2 | gpt-6.1-terra | resp_0a283754cf334589016ae9755a45ec87d1afb481b51fb8acce | 0.359100500 |
| 17 | activation-dedup:16bb477a688a0fa54598a1410f77f5468acf3e51aab3bea323ca0c8a2f03697a | gpt-6-luna | resp_037fe04979684318016ae975c7433887d19d0d3347b3fab0f3 | 0.070165850 |
| 18 | activation-code:a829406bfe55fa1df649badbf8e75f35ce26b134 | gpt-6.1-terra | resp_01fb8e53966d0752016ae979631d6487d1820d2d6f8a6ebbc9 | 0.254339250 |
| 19 | activation-dedup:4022a906eb425b00b76b67a932c16c6ce66e4faf2fa6daa2826a856efe795dba | gpt-6-luna | resp_0cc8bc21bdea976e016ae979acb3a087d18779f96c09514f61 | 0.028901675 |
| 20 | activation-code:d581b4578fe0b7b0ccae5bc2dcf04330fdde2f0a | gpt-6.1-terra | resp_02fc2ae9e51be048016ae97fcdec1c87d1b16d775bc672aadf | 0.270241750 |

## 后续需要的授权

继续付费前需要用户明确批准新的**整个试点累计总上限**。新的上限必须保留上述 US$2.980099325 历史费用，不能新建一个“重置为零”的阶段预算。

如获授权，先完成修复版独立复审、两篇英文研究/写作/审稿并交付真实 Markdown，再按同一累计余额继续12语种。仍不发布网站。费用按实际使用结算，上限不是预付金额。
