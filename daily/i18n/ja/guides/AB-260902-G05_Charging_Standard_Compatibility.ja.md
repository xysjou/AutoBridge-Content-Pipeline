# ChinaのEV 充電規格 概要:GB/T対CCS2対CHAdeMO対NACSの両立性
## SEOメタデータ
- SEOタイトル: GB/T対CCS2対CHAdeMO対NACS:ChinaEV輸出互換性
- メタディスクリプション: 欧州、日本、北米でChina市場EVの料金を請求しますか? GB/T 20234.3/27930は、地域別コネクタマップ、輸出バージョンの入口、アダプタ、ChaoJi方向を説明しました。
- H1: ChinaのEVは海外に満たしますか。GB/T、CCS2、CHAdeMOおよびNACS両立性は説明しました
- 主要キーワード: GB/T CCS2 CHAdeMOの充満標準的な輸出両立性
- 関連検索語: ChinaのEVの輸出充満アダプター、GB/T 20234.3 DCの速い充満、GB/T 27930の議定書、CCS2の輸出版EVのChaoJiの標準
- 推奨URL: /guides/chinese-ev-charging-standard-compatibility/
- 検索意図: 理解ChinaEV充満海外か。GB/T、CCS2、CHAdeMOおよびNACS両立性 説明: 車両/部品輸出業者が注文をコミットする前に検証、文書化、決定しなければならないもの。
- 内部リンク候補: /vehicles/byd-yuan-plus/ ; /guides/right-hand-drive-chinese-cars/ ; /guides/used-chinese-ev-inspection/
- 画像候補: 世界コネクタ標準地図
- ALTテキスト: DC高速充電コネクタ規格の世界地図
- スキーマ範囲: 記事(商品・オファー・価格・レビュー・料金なし)
## コネクタが車が使用可能なかどうかを判断する理由
税関を通過するChina国内のEVは、充電入口が公共充電ネットワークに一致しない場合、依然として有効に利用できなくなります。 充電互換性は、物理コネクタと通信プロトコルの問題であり、ブランドの設定ではなく、車両が輸出のために指定されている前に、到着後に入口を改装することは費用がかかり、時には非準拠である必要があります。
## 規格マップ(DC高速充電)
| スタンダード | 第一次展開 | インフォメーション |
| --- | --- | --- |
| GB/T 20234.3 (DC) + GB/T 27930 (通信可能) | China(国内China車) | GB/T 20234.3-2023 は、1500 V/800 A (業界情報全般) の上限を上げます。 |
| CCS2 (Combo 2) | ヨーロッパおよび多くの輸出市場 | AC/DC 入口を結合しました。EU の優位 |
| CCS1 (Combo 1) | 北アメリカ | CCSの地域的変種 |
| CHAdeMO(アデモ) | 日本とセレクト市場 | 日本での原産 |
| ナックス | 北アメリカ | 北米(2026のロールアウトタイミングが正式に検証されていない)の展開 |
これらのDCコネクタは、物理的に相互に互換性がないです。 GB/Tの充電ガンをCCS2ソケットに差し込むことはできません. AC(夜遅く)の入口は市場によって同様に異なります and must be checked separately — ある規格で急速充電できても、AC充電口の確認は別途必要な場合がある.
## 実務における「China市場GB/T」の意味
国内のChinaEVは、一般的にGB T DC充電とGB T 27930 CANベースの通信ハンシャクで出荷します。 先物ネットワークが前身に動くとき CCS2(ヨーロッパ)、CHAdeMO(日本)、NACS/CCS1(北アメリカ)、これは、輸入業者が設計しなければならない互換性ボトルネックを作成します。 直面的に、GB/T と CCS2 は直接物理的互換性がないため、アダプターはブリッジに必要 (EVSE業界比較ごとに)、アダプターは通信ハンカク作業を行わなければならないだけでなく、単に機械的にフィットする。
## 解決の3つの方法 — 優先順位どおりに
1. 工場出荷版の出荷版を出荷先の入口で注文して下さい。 Chinaのメーカーの多くは、国内GB/T入口ではなく、ターゲットコネクタ(CCS2など)に装着された輸出市場品種をビルドします。 入口、オンボードソフトウェア、認証が整列されるため、最もクリーンなルートです。 ブランドの公式エクスポート設定で、VIN/model を必ず確認して下さい - 国産版と「same」モデルのエクスポート版は異なります。
2. 認証アダプタ(GB/T ↔ 宛先)を使用してください。 アダプターの充満速度および手掛りの信頼性は艦隊のロールアウトの前にテストされなければなりません。
3. インフラ側には溶かします。 ターミナル/フリート演算子は、公共ネットワークに依存しない、公共ステーションに依存する小売顧客には、クローズドフリートに有効である、自分の敷地にGB T対応の充電器をインストールすることができます。
## ChaoJi: 未来の方向、今日のデフォルトではなく
China・日本 ChaoJi超高速充電プロジェクトは、一般的な物理的なインターフェイスがGB T、CHAdeMOおよびCCSシステム全体で互換性があり、将来のDC標準化方向(公式CHAdeMO協会文書)とみなされるように設計されている。 先見のコンテキスト:は、現在の生産GB T車両はすでにChaoJiの恩恵を想定しています。モデルのサポートは、販売ポイントとして使用する前に正式に確認します。
## AutoBridge がコネクタチャートを超えて追加する
基準チャートは、GB/T が CCS2 と異なることを伝えます。 *this VIN* が充電されるかどうかは、通知しません。 推奨方法は、VIN-bound Note として物理インレット、ハンドシェイクプロトコル、およびオンボードチャーレーティングを録音し、プロトコルゲートウェイ(GB/T 27930ハンドシェイク)からハードウェアアダプター(機械のみ)を区別し、購入ファイルで を入金する前に、 の を 確認します。
## 車両検証マトリックス
- 国内入口:GB/T DC + AC入口のタイプ
- 利用できる工場輸出入口: CCS2 CHAdeMO NACS CCS1 VIN
- 通信プロトコルとエクスポートファームウェアが宛先ハンカケをサポートしているかどうか
- アダプターベースの場合:
- 目的地(DC規格の優位、ACソケット規格)の公共ネットワーク現実
-
## お支払い前
- 目的地の優位DC と ACコネクタ規格を確認してください。
- ブランドの公式エクスポートバージョンのコネクター確認をVINで入手し、国内仕様から干渉しません。
-
- 艦隊については、デポの充電器が公共ネットワーク依存を解除するかを決定します。
- 正式にユニットを確認しない限り、ChaoJiは将来の面で主張します。
## よくある質問
欧州CCS2でChinaGB/T EVの充満を直接缶詰にして下さいか。 いいえ — GB/T と CCS2 は物理的に互換性がありません。工場 CCS2 エクスポート バージョンまたは、ローカル 準拠のアダプターが必要です。
GB/T 27930 は何ですか。 ChinaGB/T 20234.3 DCコネクタと併用したCANベースの通信プロトコルです。 プラグ形状と同じくらい手作業が重要になります。
アダプターは、永久的なソリューションですか?
ChinaブランドはCCS2バージョンを販売していますか? 宛先コネクタでエクスポートバリアントを多く構築する — 想定するよりも、公式のエクスポート設定でモデル/VIN で確認する。
Does Chao, キプロス ジは、すべてのコネクタを今互換性がありますか? ChaoJiは、設計の互換性のある未来の方向です。現在の製造車は、モデルごとの確認が必要です。
## Sources & Verification
| 出典 | 機関 | 市場 | URL | 確認日 | 裏付けられた事実 |
| --- | --- | --- | --- | --- | --- |
| ChaoJi standard presentation (official) | CHAdeMO Association (standards body) | CN/JP/Global | https://www.chademo.com/wp2016/wp-content/uploads/ChaoJi202006/ChaoJi_Presenataion_EN.pdf | 2026-09-02 | ChaoJi designed compatible with GB/T/CHAdeMO/CCS |
| Charging-standard certification paths | Huayu Testing (certification body) | Global | http://www.huayutest.com/zixun/87747.html | 2026-09-02 | CHAdeMO/CCS regional rollout, certification differences |
| Charging connector standards | cehome (industry media) | CN | https://m.cehome.com/news/20260809/389612.shtml | 2026-09-02 | GB/T 20234.3-2023 1500V/800A, GB/T 27930, ChaoJi |
| GB/T, CCS2, Type 2, NACS, CHAdeMO compared | evse-chargers.com (industry) | Global | https://www.evse-chargers.com/news/understanding-ev-charging-standards-gb-t-ccs2-type-2-nacs-and-chademo-compared-283319.html | 2026-09-02 | GB/T↔CCS2 requires adapter; compatibility matrix |
| Guide to global EV charging standards | MARUIKEL (industry) | Global | https://www.maruikel.com/es/blog/guide-to-global-ev-charging-standards-type-1-type-2-ccs-chademo-gbt.html | 2026-09-02 | Domestic GB/T vs export-version destination connector |
| GB/T-to-CHAdeMO adapter B2B guide | Electric Auto China (industry) | Global | https://www.electricautochina.com/comprehensive-b2b-guide-to-gbt-to-chademo-adapters-for-exported-chines/ | 2026-09-02 | Export compatibility bottleneck |

## 編集レビュー
- 著者: AutoBridge Export Editorial Team · [authors](/authors/) · [編集方針](/editorial-policy/)
- 最終確認日: 2026-09-05
- 参照市場: グローバル
- 検証方法: 定められたルールは規制当局・政府の一次資料に基づき、メディア間で矛盾する数値は断定せず確認項目として残し、時間に敏感な事項は所管当局での最新確認を案内する。
- 編集基準: 上記の出典に基づき調査・執筆（デスクリサーチ。実車走行・分解・輸入の一次体験は主張しない）。独立して確認できない点は、事実として断定せず確認項目として示す。
- 透明性: 執筆と翻訳にAI支援を使用。本稿はデスクリサーチに基づく。明示的な記録がある場合を除き一次試験は主張せず、最終的な人間による編集レビューは未完了。
#AutoBridge #ChargingStandards #GBTvsCCS #EVExport #ConnectorCompatibility
