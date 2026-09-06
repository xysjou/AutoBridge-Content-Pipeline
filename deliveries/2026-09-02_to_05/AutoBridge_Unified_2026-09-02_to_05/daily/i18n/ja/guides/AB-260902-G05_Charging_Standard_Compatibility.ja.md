# 中国のEV 充電規格 概要:GB/T対CCS2対CHAdeMO対NACSの両立性

## ツイート メタデータ
- **SEOのタイトル**:GB T対CCS2対CHAdeMO対NACS:中国EVの輸出互換性
- **メタ 記述**: 欧州、日本、北米で中国市場EV充電できますか? GB/T 20234.3/27930は、地域、輸出バージョンの入口、アダプター、ChaoJi方向によるコネクタマップについて説明しました。
- **混雑したURL**: /guides/chinese-ev-charging-standard-compatibility/
- H1 ホテル **:中国EV充電は海外ですか? GB/T、CCS2、CHAdeMOおよびNACSの両立性は説明しました
- **主なキーワード**:GB/T CCS2 CHAdeMOの充満標準的な輸出両立性
- **二次検索条件**:中国EV輸出充電アダプター、GB T 20234.3 DC高速充電、GB T 27930プロトコル、CCS2エクスポートバージョンEV、ChaoJi標準
- **内部リンクの提案**: /vehicles/byd-yuan-plus/; /guides/right-hand-drive-chinese-cars/; /guides/used-chinese-ev-inspection/
- **イメージ提案**:世界コネクタ標準マップ;GB T対CCS2入口比較;工場輸出バージョン入口;アダプタのコンプライアンス警告
- **ALTの提案**:「DCの速い充満コネクターの標準の世界の地図」;側面によって側面を充電するGB/TおよびCCS2;「中国のEVの輸出版CCS2の入口」

## コネクタが車が使用可能なかどうかを判断する理由

税関を通過する中国国内のEVは、充電入口が公共充電ネットワークに一致しない場合、依然として有効に利用できなくなります。 充電互換性は、**物理コネクタと通信プロトコル**の問題であり、ブランドの設定ではなく、車両が輸出のために指定されている**前に、到着後に入口を改装することは費用がかかり、時には非準拠である必要があります。

## 規格マップ(DC高速充電)

| スタンダード | 第一次展開 | インフォメーション |
|---|---|---|
| **GB/T 20234.3 ** (DC) + **GB/T 27930 ** (通信可能) | 中国(国内中国車) | GB/T 20234.3-2023 は、1500 V/800 A** (業界情報全般) の上限を上げます。 |
| CCS2 (Combo 2)** | ヨーロッパおよび多くの輸出市場 | AC/DC 入口を結合しました。EU の優位 |
| CCS1 (Combo 1)** | 北アメリカ | CCSの地域的変種 |
| **CHAdeMO******(アデモ)** | 日本とセレクト市場 | 日本での原産 |
| ナックス** | 北アメリカ | 北米(2026のロールアウトタイミングが正式に検証されていない)の展開 |

これらのDCコネクタは、**物理的に相互に互換性がない**です。 you cannot plug a GB/T gun into a CCS2 socket. AC(夜遅く)の入口は市場によって同様に異なります  and  must be checked separately — a car may fast-charge on one standard while its AC inlet still needs attention.

## 実務における「中国市場GB/T」の意味

国内の中国EVは、一般的に**GB T** DC充電とGB T 27930 CANベースの通信ハンシャクで出荷します。 先物ネットワークが前身に動くとき** CCS2(ヨーロッパ)、CHAdeMO(日本)、NACS/CCS1(北アメリカ)**、これは、輸入業者が設計しなければならない互換性ボトルネックを作成します。 直面的に、**GB/T と CCS2 は直接物理的互換性がないため、アダプターはブリッジに必要** (EVSE業界比較ごとに)、アダプターは通信ハンカク作業を行わなければならないだけでなく、単に機械的にフィットする。

## Three Ways to Solve It — in Order of Preference

1. **工場出荷版の出荷版を出荷先の入口で注文して下さい。** 中国のメーカーの多くは、国内GB/T入口ではなく、ターゲットコネクタ(CCS2など)に装着された輸出市場品種をビルドします。 入口、オンボードソフトウェア、認証が整列されるため、最もクリーンなルートです。 ブランドの公式エクスポート設定で、VIN/model を必ず確認して下さい** - 国産版と「same」モデルのエクスポート版は異なります。
2. **認証アダプタ(GB/T ↔ 宛先)を使用してください。** アダプターの充満速度および手掛りの信頼性は艦隊のロールアウトの前にテストされなければなりません。
3. **インフラ側には溶かします。** ターミナル/フリート演算子は、公共ネットワークに依存しない、公共ステーションに依存する小売顧客には、クローズドフリートに有効である、自分の敷地にGB T対応の充電器をインストールすることができます。

## ChaoJi: 未来の方向、今日のデフォルトではなく

中国・日本 **ChaoJi**超高速充電プロジェクトは、一般的な物理的なインターフェイスが**GB T、CHAdeMOおよびCCS**システム全体で互換性があり、将来のDC標準化方向(公式CHAdeMO協会文書)とみなされるように設計されている。 先見のコンテキスト:******は、現在の生産GB T車両はすでにChaoJiの恩恵を想定しています。モデルのサポートは、販売ポイントとして使用する前に正式に確認します。

## AutoBridge がコネクタチャートを超えて追加する
基準チャートは、GB/T が CCS2 と異なることを伝えます。 *this VIN* が充電されるかどうかは、通知しません。 推奨方法は、VIN-bound Note** として**物理インレット、ハンドシェイクプロトコル、およびオンボードチャーレーティングを録音し、プロトコルゲートウェイ(GB/T 27930ハンドシェイク)から**ハードウェアアダプター(機械のみ)を区別し、購入ファイルで** を入金する前に、** の** を 確認します。
## 車両検証マトリックス



- 国内入口:GB/T DC + AC入口のタイプ
- 利用できる工場輸出入口: CCS2 CHAdeMO NACS CCS1 VIN
- 通信プロトコルとエクスポートファームウェアが宛先ハンカケをサポートしているかどうか
- アダプターベースの場合:
- 目的地(DC規格の優位、ACソケット規格)の公共ネットワーク現実
-

## お支払い前

- 目的地の優位DC **と** ACコネクタ規格を確認してください。
- ブランドの公式エクスポートバージョンのコネクター確認をVINで入手し、国内仕様から干渉しません。
-
- 艦隊については、デポの充電器が公共ネットワーク依存を解除するかを決定します。
- 正式にユニットを確認しない限り、ChaoJiは将来の面で主張します。

## よくある質問

**欧州CCS2で中国GB/T EVの充満を直接缶詰にして下さいか。** いいえ — GB/T と CCS2 は物理的に互換性がありません。工場 CCS2 エクスポート バージョンまたは、ローカル 準拠のアダプターが必要です。
**GB/T 27930 は何ですか。** 中国GB/T 20234.3 DCコネクタと併用したCANベースの通信プロトコルです。 プラグ形状と同じくらい手作業が重要になります。
**アダプターは、永久的なソリューションですか?**
**中国ブランドはCCS2バージョンを販売していますか?** 宛先コネクタでエクスポートバリアントを多く構築する — 想定するよりも、公式のエクスポート設定でモデル/VIN で確認する。
Does Chao, キプロス ジは、すべてのコネクタを今互換性がありますか?** ChaoJiは、設計の互換性のある未来の方向です。現在の製造車は、モデルごとの確認が必要です。

## 映像の記録
- IMAGE_ASSET_PATH:リポジトリで保護されていない
- ORIGINAL_IMAGE_URL: キャプチャされていない
- SOURCE_PAGE: キャプチャされていない
- SOURCE_FILE_PAGE: 該当なし — 特定候補のメディアファイル (アサートするライセンスなし)
- 権利_ホルダー:未確認
- LICENSE_OR_USAGE_BASIS: 保護されていない — 権利がクリアされるまで、第三者の画像が公開されない
- CHECKED_DATE: 2026-09-06(税抜き)
- MODEL_TOPIC_MATCH:
- IMAGE_SCOPE_NOTE: 完全モデルファミリー/トピックのみにマッチします。特定のトリム/モデル年、実際のVIN、インパースペクションまたは実際の取引を暗黙的に行う必要はありません。
- IMAGE_RIGHTS_STATUS: FAIL(ライセンス資産の収集、プレースホルダー、または「古い画像の保持」のメモは受け付けていません)
- ブロック解除: 再使用可能なイメージが保護できません:Wikimedia Commons/Flickrは、研究環境から到達できないため、ストックライブラリは認証されたAPI/ライセンスアクセスを必要とし、OEMページイメージは商用再利用の付与ではありません。AutoBridgeが所有する写真は存在しません。 割礼ではなく、FAILを割り当てる。
- 言語によるALT:
  - **EN**: AutoBridge export-buyer reference — EV charging-standard compatibility GB/T CCS CHAdeMO NACS, vehicle-export procurement guide
  - **FR**: Référence AutoBridge pour acheteurs export — EV charging-standard compatibility GB/T CCS CHAdeMO NACS, guide d’achat à l’export automobile
  - **DE**: AutoBridge-Referenz für Exportkäufer — EV charging-standard compatibility GB/T CCS CHAdeMO NACS, Leitfaden für Fahrzeugexport-Einkauf
  - **ES**: Referencia AutoBridge para compradores de exportación — EV charging-standard compatibility GB/T CCS CHAdeMO NACS, guía de compras para exportación de vehículos
  - **PT**: Referência AutoBridge para compradores de exportação — EV charging-standard compatibility GB/T CCS CHAdeMO NACS, guia de compras para exportação de veículos
  - **JA**: AutoBridge 輸出バイヤー向けリファレンス｜EV charging-standard compatibility GB/T CCS CHAdeMO NACS, 自動車輸出 調達ガイド
  - **KO**: AutoBridge 수출 바이어 참고 자료｜EV charging-standard compatibility GB/T CCS CHAdeMO NACS, 자동차 수출 조달 가이드
  - **VI**: Tài liệu tham khảo AutoBridge cho người mua xuất khẩu — EV charging-standard compatibility GB/T CCS CHAdeMO NACS, hướng dẫn thu mua xuất khẩu xe
  - **TH**: เอกสารอ้างอิง AutoBridge สำหรับผู้ซื้อเพื่อการส่งออก — EV charging-standard compatibility GB/T CCS CHAdeMO NACS, คู่มือจัดซื้อเพื่อการส่งออกยานยนต์
  - **ID**: Referensi AutoBridge untuk pembeli ekspor — EV charging-standard compatibility GB/T CCS CHAdeMO NACS, panduan pengadaan ekspor kendaraan
  - **AR**: مرجع AutoBridge لمشتري التصدير — EV charging-standard compatibility GB/T CCS CHAdeMO NACS, دليل مشتريات تصدير المركبات
  - **ZH**: AutoBridge 出口采购参考｜EV charging-standard compatibility GB/T CCS CHAdeMO NACS, 汽车出口采购指南

## ソースと検証

| ソースタイトル | 組織図 | マーケット | ページの先頭へ | チェック済み | 自信の秘境 | 対応する事実 |
|---|---|---|---|---|---|---|
| チャオジ標準プレゼンテーション(公式) | CHAdeMO協会(規格体) | CN/JP/Global の検索結果 | 以下は、 https://www.chademo.com/wp2016/wp-content/uploads/ChaoJi202006/ChaoJi_Presenataion_EN.pdf | 2026-09-02 | 検証済み | チャオジはGB/T/CHAdeMO/CCSと互換性がある設計しました |
| 充電標準認証パス | 華湯試験(認証ボディ) | 営業拠点 | 担当: http://www.huayutest.com/zixun/87747.html の | 2026-09-02 | CROSS_CHECKED(クロス) | CHAdeMO/CCS 地域展開、認証の違い |
| 充満コネクターの標準 | cehome(産業媒体) | CN の | 以下は、 https://m.cehome.com/news/20260809/389612.shtml の | 2026-09-02 | CROSS_CHECKED(クロス) | GB/T 20234.3-2023 1500V/800A、GB/T 27930のChaoJi |
| GB/T、CCS2のタイプ2のNACS、CHAdeMOは比較しました | | 営業拠点 | 以下は、 https://www.evse-chargers.com/news/understanding-ev-charging-standards-gb-t-ccs2-type-2-nacs-and-chademo-compared-283319.html | 2026-09-02 | CROSS_CHECKED(クロス) | GB/T↔ CCS2 はアダプターを要求します; 両立性行列 |
| 世界的なEV充電基準ガイド | マルイクラー(産業) | 営業拠点 | 以下は、 | 2026-09-02 | CROSS_CHECKED(クロス) | 国内GB/T対輸出バージョンの宛先コネクタ | https://www.maruikel.com/es/blog/guide-to-global-ev-charging-standards-type-1-type-2-ccs-chademo-gbt.html
| GB/T-to-CHAdeMO アダプター B2B ガイド | 電気自動車中国(産業) | 営業拠点 | 以下は、 の特長 | 2026-09-02 | CROSS_CHECKED(クロス) | 輸出互換性ボトルネック | https://www.electricautochina.com/comprehensive-b2b-guide-to-gbt-to-chademo-adapters-for-exported-chines/

*Confidence Note(AutoBridge標準):標準レベルの事実はVERIFIED/CROSS_CHECKED(CHAdeMO)です 協会は、規格の体です。 機種ごとの輸出コネクタ、国別アダプターの合法性、NACSのロールアウトタイミングがキャプチャされず、VINと宛先ごとの確認が必要であった。 ふりがな

## 編集レビュー
- **著者/査読者**:【AutoBridge 輸出編集チーム】(/authors/)・方法による【編集ポリシー】(/editorial-policy/)
- **最終審査**:2026-09-05
- **参考市場**:グローバル(中国輸出国;EU/JP/NA展開)
- **検証方法**: 規格ボディ文書と交差チェック業界ソース;モデル固有のコネクタは、公式のper-VIN確認に残します
- ** 編集規格**: 上記情報源(デスクリサーチ、片手運転、涙流、輸入)から研究・執筆 ソースの自信は行ごとに示されます。 私たちが独立して確認できない点は、事実として主張するのではなく、検証項目として提示されます。
#AutoBridge #ChargingStandards #GBTvsCCS #EVExport #ConnectorCompatibility
