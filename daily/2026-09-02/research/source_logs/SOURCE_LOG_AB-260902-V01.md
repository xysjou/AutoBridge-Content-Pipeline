# SOURCE LOG — AB-260902-V01
**Topic**: BYD 元PLUS 2024 荣耀版
## SOURCE 01
- **Source Name**: 中关村在线 元PLUS 2024款参数表
- **Organization**: 中关村在线（ZOL 汽车频道）
- **URL**: https://detail.zol.com.cn/series/2530/69565/param_10855221_0_1.html
- **Source Type**: 汽车数据库/媒体
- **Market**: CHINA
- **Facts Supported**: 尺寸/轴距/电机/电池/续航/快充/ADAS/车机
- **Checked Date**: 2026-09-02
- **Authority Level**: 中（数据库类）
## SOURCE 02
- **Source Name**: 懂车帝 元PLUS 文章
- **Organization**: 懂车帝（字节跳动）
- **URL**: https://www-lf.dongchedi.com/article/7425573307363131931
- **Source Type**: 汽车数据库/媒体
- **Market**: CHINA
- **Facts Supported**: 电机 150kW/310N·m、刀片电池 60.48kWh、CLTC 510km、7.3s
- **Checked Date**: 2026-09-02
- **Authority Level**: 中（数据库类）
## SOURCE 03
- **Source Name**: 汽车之家 问答/车家号
- **Organization**: 汽车之家
- **URL**: https://www.autohome.com.cn/ask/23350747.html
- **Source Type**: 汽车数据库/媒体
- **Market**: CHINA
- **Facts Supported**: 电机参数、电池版本、荣耀版上市与价格
- **Checked Date**: 2026-09-02
- **Authority Level**: 中（数据库类）
## SOURCE 04
- **Source Name**: 太平洋汽车 参数页
- **Organization**: 太平洋汽车网
- **URL**: https://price.pcauto.com.cn/s48082/config.html
- **Source Type**: 汽车数据库/媒体
- **Market**: CHINA
- **Facts Supported**: 电机马力 204Ps、快充 80%
- **Checked Date**: 2026-09-02
- **Authority Level**: 中（数据库类）
## SOURCE 05
- **Source Name**: 汽车之家（车家号）荣耀版上市新闻
- **Organization**: 汽车之家
- **URL**: https://chejiahao.m.autohome.com.cn/info/14756991
- **Source Type**: 媒体新闻
- **Market**: CHINA
- **Facts Supported**: 上市时间 2024-03、指导价 11.98-14.78 万、全系降价 1.6 万
- **Checked Date**: 2026-09-02
- **Authority Level**: 中
**备注**: 核心参数由 3 个独立数据库（ZOL/懂车帝/汽车之家）交叉一致 → CROSS_CHECKED。未直接取得 BYD 官网页面，出口版（ATTO 3）参数标注"须以官网为准"。

## CONTROLLED RESEARCH PATCH — 2026-09-05 (Writing AI, second repair)
## SOURCE (OEM)
- Source Name: 比亚迪官网 元PLUS 车型中枢（王朝网，现行页）
- Organization: BYD Auto 比亚迪（厂商官方）
- URL: https://www.byd.com/cn/dynasty-home/models/yuan/3-yuan-plus
- Source Type: OEM official model hub
- Market: 中国
- Facts Supported: 元PLUS车系与代际身份。注意：现行页展示更新一代后驱车型，仅用于界定车系/代际，不作为本页2024荣耀版（前驱/430/510 CLTC）数值来源
- Checked Date: 2026-09-05
- Authority Level: T1 (model-line/generation scope)
PATCH_NOTE: 2024荣耀版 49.92/60.48kWh、150kW/310N·m、430/510 CLTC 由ZOL/懂车帝/汽车之家/太平洋多源对同一事实交叉；出口WLTP/NEDC不主张，以BYD目的地区现行页为准。
