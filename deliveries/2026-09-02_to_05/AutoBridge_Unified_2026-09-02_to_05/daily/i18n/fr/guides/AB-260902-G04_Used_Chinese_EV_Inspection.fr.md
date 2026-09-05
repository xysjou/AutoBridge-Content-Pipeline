# Inspection pré-exportation chinoise d'occasion: Batterie SOH correctement faite, plus accident, inondation et contrôle des odomètres
## OEuvre Métadonnées
- **Titre du référencement**: Inspection de la batterie de véhicules électriques chinois usagés: SOH, Flood & Odomètre Contrôles
- **Description détaillée**: Comment inspecter un véhicule électrique chinois usagé avant d'exporter — ce que signifie réellement la SOH en vertu des normes de batterie, un test de charge mesuré, la lecture du bilan cellulaire, le dépistage des accidents/inondations et les contrôles croisés des odomomètres-vs-cycle, sans seuil légal inventé.
- **URL suggérée**: /guides/used-chine-ev-inspection/
- ** H1 **: Inspection d'un VE chinois utilisé avant exportation: ce que signifient les numéros de batterie et ce qu'il faut rejeter
- **Mot-clé principal**: liste de contrôle de la batterie chinoise d'inspection des véhicules électriques
- **Termes de recherche secondaires**: Batterie EV standard SOH QC/T 743, GB/T 31484 cycle de vie, déséquilibre de tension des cellules EV utilisées, inspection des dommages causés par les inondations EV, compte du cycle de la batterie de retour de l'odomètre
- **Suggestions de lien interne**: /guides/vérify-china-car-export-fournisseur/; /guides/chinese-ev-charge-standard-compatibilité/; /guides/import-chinois-ev-to-russia-eac-ottc/
- **Suggestions d'image**: lecture de l'outil de diagnostic de la SOH et de la tension cellulaire; metered 20–80% charge worksheet; points d'inspection sous-marins de batterie; échantillon de l'enregistrement de la notification/demandes
- ** Suggestions de l'ALT**: "Rapport de diagnostic indépendant montrant la différence de SOH et de tension maximale des cellules"; "feuille de travail d'essai de charge-énergie mesurée"; "points d'inspection sous-marins du pack de batteries EV"
## Portée: un manuel d'inspection, pas un nouveau débat utilisé
La décision d'acheter **utilisée** est prise comme indiqué; Cette page couvre l'inspection technique ** avant exportation**. L'économie d'un véhicule électrique usagé est dominée par la batterie à haute tension: un corps propre avec un paquet usé peut être moins valable que le coût de remplacement après l'expédition, de sorte que l'ordre d'inspection des opérations est différent d'une voiture ICE. A central aim is to be precise about what "SOH 80%" actually is — an engineering reference, not a universal customs line.
## What SOH Is — and What the 80% Figure Actually Means
** État de santé (SOH)** exprime la capacité maximale utilisable actuelle d'un pack par rapport à sa capacité nominale nouvelle (SOH fondée sur la capacité = capacité vieillie ÷ capacité nominale). Il est essentiel de séparer une convention de fin de vie** de **l'importation légale**, car ils sont souvent confus:
- The **~80%** figure originates in **battery standards and warranty practice**, not import law. China's automotive-industry standard **QC/T 743** treats capacity falling to 80% of nominal as an end-of-life reference; **GB/T 31484 ** spécifie la durée de vie du cycle de traction-batterie *méthodes d'essai*; **CEI 62660 ** (parties 1/2) normalise les performances/essais de la cellule lithium-ion; et la nouvelle norme nationale recommandée **GB/T 46991.1-2025 ** (développée sous MIIT/SAC) traite de l'exactitude et de la durabilité des écrans embarqués SOH/SOC*. Ce sont des documents de l'organisme de normalisation (VERIFIÉ quant à ce qu'ils définissent).
- **There is no single universal legal SOH threshold for importing a used EV.** No regulation cited in this research sets "80%" as a blanket customs or type-approval gate that applies across the EU, ASEAN or anywhere else. Be explicit about what 80% is **not**: Il ne s'agit pas d'un seuil d'importation de voitures d'occasion**, il ne s'agit pas d'une loi unifiée sur la retraite des batteries**, et il ne s'agit pas du seuil de garantie de tous les fabricants** (une garantie donnée peut utiliser un chiffre différent). Une destination peut imposer sa propre règle de condition et un acheteur peut fixer une ligne commerciale privée — mais chacune est un instrument différent*. L'organisme de certification de destination/la norme d'acceptation de l'importateur régit et doit être confirmé par pays plutôt que supposé.
Cette distinction change la façon dont vous utilisez le numéro: treat the ~80% engineering convention purely as a **commercial/engineering reference for pricing and rejection**, while separately confirming whether the destination sets any legal condition. No chemistry-specific "85% NMC line" is asserted here because no standard or manufacturer source captured for this article establishes it as a rule.
## Obtenir un numéro de SOH défendable
- Lisez l'affichage santé dans la voiture/groupe, mais ne vous arrêtez pas là — les affichages embarqués sont des estimations et la nouvelle norme d'affichage GB/T 46991.1 s'applique à la nouvelle production, pas nécessairement aux anciennes unités utilisées.
- Commandez un rapport de diagnostic indépendant** qui enregistre la SOH ** et la différence de tension maximale de cellule à cellule**: un déséquilibre important annonce des modules faibles même lorsque la SOH semble en bonne santé.
- Les marques chinoises ne partagent pas un seul protocole OBD/diagnostic et les formats de rapport tiers ne sont pas normalisés, donc gardez le rapport brut (outil, version logicielle, date, température ambiante) comme preuve. Des critères de qualité de la batterie et de la garantie devraient être demandés à la marque, lorsque cela est possible, plutôt que de le deviner.
## Contrôle croisé avec un test de charge réelle mesuré (un contrôle croisé de dépistage, pas un calcul de SOH)
Une valeur statique de SOH peut être mal représentée; un test de charge exerce le pack. Charge from roughly **20% to 80%** on a **metered** charger, recording start/end SOC, kWh delivered, the power curve and elapsed time, and compare delivered energy against the expected ~60% of usable pack capacity. ** Traitez cela strictement comme un contrôle croisé, pas comme un moyen de calculer la SOH.** Chargeur livré kWh est *pas* égal à l'énergie stockée dans les cellules: la lecture est affectée par **pertes de charge/conversion, tirage thermique, température ambiante et température de conditionnement, calibration du BMS SOC et tampon de réserve/haute-fond**. Il ne peut donc que signaler une anomalie **brute**. Un déficit sur cet écran ne se révèle pas en soi une perte de capacité réelle (et un écran propre ne prouve pas la santé complète); la capacité officielle/le chiffre de SOH nécessite toujours une méthode de diagnostic qualifiée ou des données d'essai professionnelles du fabricant. L'incapacité de maintenir le taux de charge prévu est une raison pour effectuer cette inspection plus approfondie. Exécutez l'écran à côté du contrôle standard de charge (GB/T en Chine vs le connecteur de destination — voir le guide de compatibilité) de sorte qu'un pack son ne soit pas échoué par une entrée incompatible.
## La triade haute tension au-delà de la SOH
- **Emballer sous le dessous**: enlever/inspecter le bouclier inférieur pour enlever/résceller les marques, les éraflures, la déformation ou la réparation non-usine.
- **Motor et électronique de puissance**: codes de défaut de balayage, contrôle des feux d'avertissement et vérification du comportement de l'entraînement/régence lors d'un essai sur route.
- **Câblage HV et connecteurs**: recherche de la corrosion, de la rétermination ou des joints non-usines.
## Criblage des accidents, des inondations et des incendies
- Pull **maintenance records and insurance-claim (出险) records**; La réparation de tôle de construction ou tout marqueur de revendication d'eau de crue est un motif de rejet.
- Dégradation du pack de protection et corrosion du harnais par les EVs inondées: inspecter les connecteurs sous-marins, les rails de siège, les boîtes à fusibles et l'enceinte de la batterie pour les conduites d'eau/corrosion.
- Vérifier les trous de panneaux, l'épaisseur de la peinture et les marques de témoins de fixation; traiter tout signe que le pack de batterie a été ouvert à l'extérieur d'une installation qualifiée comme un signal d'arrêt.
## Cycles d'odomètres et de charges
Un EV à horloge montre un **odomètre incompatible avec le nombre de cycles de batterie et l'usure**. Lorsque le diagnostic expose le nombre de cycles, comparez-le au kilométrage affiché et à l'usure physique (siège, direction, pédales). Le kilométrage affiché faible associé à des comptes de cycles élevés ou à des composants vieillis est un avertissement de recul qu'un contrôle de l'odomètre ICE seul manquerait.
## Papeterie et règle de destination
Conservez le rapport indépendant de SOH/imbalance, le relevé de frais mesuré et l'historique de service/demandes dans le dossier d'exportation. Separately — and this is the correction to any blanket "you need 80% to import" claim — **obtain the destination's actual used-EV condition/type rule in writing** from its certification authority or your clearance agent. Les règles chinoises relatives à la qualification et à l'âge des exportations de voitures d'occasion sont établies par le MOFCOM et mises à jour (voir les guides sur les fournisseurs et les marchés publics de la flotte); utiliser la position de l'année en cours plutôt qu'un chiffre de blog plus ancien.
## Ce qu'autoBridge ajoute au-delà d'une liste de contrôle générique
Public checklists repeat "read SOH and reject below 80%." This guide instead recommends: (1) separating the engineering 80% convention from the destination's actual legal rule, so a buyer neither walks away from a compliant car nor ships a non-compliant one on a myth; (2) jumelant un contrôle de l'énergie mesurée à une lecture de l'équilibre cellulaire plutôt que de se fier à une capture d'écran du tableau de bord; et (3) en maintenant la note d'inspection liée au dossier **VIN et d'exportation** utilisé pour la certification, de sorte que le wagon testé est traçable au wagon expédié.
## Règles de rejet dur
- Marqueur de crue/incendie dans les registres des réclamations, ou lignes de corrosion/eau dans le pack ou le harnais HV.
- Réparation de structures/accidents dans des zones à haute tension, ou preuve que le paquet a été ouvert à l'extérieur d'une installation qualifiée.
- L'odomètre est incompatible avec le nombre et l'usure du cycle, sans explication crédible.
- Le vendeur refuse un test de charge mesuré ou un rapport de diagnostic indépendant.
- Capacity/imbalance that fails **your own documented acceptance line** (set from brand warranty + destination rule + commercial margin) — not a mythical universal 80% legal gate.
## Liste des essais d'acceptation
- Rapport indépendant: SOH ** et** déséquilibre de tension cellulaire max, avec outil/version/date enregistré.
- Metered 20→80% charge test (SOC, kWh, power curve, time).
- Connecteurs sous-tray et HV de batterie inspectés pour élimination/corrosion.
- Service + historique de la réclamation d'assurance tiré; collision/inondation/feux de marqueur vérifié.
- L'odomètre se rapproche des cycles de charge et de l'usure physique.
- Destination used-EV rule confirmed **in writing** and distinguished from the engineering 80% line.
- La compatibilité charge-interface (GB/T vs destination) a été vérifiée.
## Foire aux questions
**Is 80% SOH a legal import requirement?** No. Roughly 80% is an engineering/warranty end-of-life reference (e.g., QC/T 743; tested per GB/T 31484 / IEC 62660); Ce n'est pas un seuil d'importation de voitures d'occasion, pas une loi de retraite unifiée et pas la ligne de garantie de tous les fabricants. There is no universal 80% customs gate, so confirm the destination's own rule.
**Why do people quote 80% then?** It comes from battery standards and warranty practice as an end-of-life/commercial reference; it is useful for pricing and rejection, but it is not import law, and no chemistry-specific 85% rule is asserted here.
**Can I calculate SOH from the charger's kWh between 20% and 80%?** Not directly. L'énergie fournie est déformée par des pertes de charge, un tirage thermique, une température, un étalonnage et un tampon BMS; c'est un contrôle croisé qui peut révéler des anomalies graves, avec un SOH formel laissé à un diagnostic qualifié.
**How should SOH be evidenced?** An independent report showing SOH and cell-voltage imbalance, cross-checked by a metered 20–80% charge test, kept with tool/version/date.
**Pourquoi les dégâts causés par les inondations sont-ils particulièrement dangereux dans un EV?** Il peut dégrader le pack et corroder les harnais/connecteurs cachés, causant des défaillances de sécurité et de fiabilité après exportation.
**Comment la fraude au compteur est-elle repérée sur un VE?** Comparez le kilométrage affiché avec le nombre de cycles de batterie et l'usure physique; un odomètre bas avec des cycles élevés est un avertissement.
## Enregistrement d'image
- IMAGE_ASSET_PATH: aucun sécurisé dans le dépôt
- ORIGINAL_IMAGE_URL: non capturé
- SOURCE_PAGE: non capturé
- HÔTEL DE DROITS: NON CONfirmÉ
- LICENSE_OR_USAGE_BASIS: aucune image sécurisée — aucune image de tiers ne peut être publiée jusqu'à ce que les droits soient effacés
- _DATE DE CHERCHE: 2026-09-05
- MODEL_TOPIC_MATCH: doit correspondre au modèle exact/version (ou au sujet du guide) et au marché de référence ci-dessus
- IMAGE_RIGHTS_STATUS: FAIL (aucun actif autorisé capturé; un détenteur de place ou -tain vieille image - Note n'est pas accepté)
- ALAT par langue:
  - **EN**: AutoBridge export-buyer reference — Used Chinese EV pre-export inspection, vehicle-export procurement guide
  - **FR**: Référence AutoBridge pour acheteurs export — Used Chinese EV pre-export inspection, guide d’achat à l’export automobile
  - **DE**: AutoBridge-Referenz für Exportkäufer — Used Chinese EV pre-export inspection, Leitfaden für Fahrzeugexport-Einkauf
  - **ES**: Referencia AutoBridge para compradores de exportación — Used Chinese EV pre-export inspection, guía de compras para exportación de vehículos
  - **PT**: Referência AutoBridge para compradores de exportação — Used Chinese EV pre-export inspection, guia de compras para exportação de veículos
  - **JA**: AutoBridge 輸出バイヤー向けリファレンス｜Used Chinese EV pre-export inspection, 自動車輸出 調達ガイド
  - **KO**: AutoBridge 수출 바이어 참고 자료｜Used Chinese EV pre-export inspection, 자동차 수출 조달 가이드
  - **VI**: Tài liệu tham khảo AutoBridge cho người mua xuất khẩu — Used Chinese EV pre-export inspection, hướng dẫn thu mua xuất khẩu xe
  - **TH**: เอกสารอ้างอิง AutoBridge สำหรับผู้ซื้อเพื่อการส่งออก — Used Chinese EV pre-export inspection, คู่มือจัดซื้อเพื่อการส่งออกยานยนต์
  - **ID**: Referensi AutoBridge untuk pembeli ekspor — Used Chinese EV pre-export inspection, panduan pengadaan ekspor kendaraan
  - **AR**: مرجع AutoBridge لمشتري التصدير — Used Chinese EV pre-export inspection, دليل مشتريات تصدير المركبات
  - **ZH**: AutoBridge 出口采购参考｜Used Chinese EV pre-export inspection, 汽车出口采购指南

## Sources et vérification
| Titre de la source | Organisation | Marché | URL | Vérification | Confiance | Faits corroborés |
|---|---|---|---|---|---|---|
| Exigences/méthodes d'essai de cycle de batterie de traction GB/T 31484 | Norme nationale chinoise (**organisme de normalisation**) | NC | https://www.chinesestandard.net/PDF.aspx/GBT31484-2015 | 2026-09-03 | **VÉRIFIER** | Cadre d'essai de la capacité/de la durée de vie du cycle; prescriptions relatives à la capacité initiale |
| Performance/essai de la cellule lithium-ion IEC 62660-1/2 | IEC (organisme international de normalisation **) | Mondial | https://www.iec.ch/ (IEC 62660 series) | 2026-09-03 | **VÉRIFIER** | Base normalisée des performances cellulaires/d'essai de durée de vie pour les SOH |
| GB/T 46991.1-2025 on-board SOH/SOC display accuracy & durability (MIIT/SAC) | Norme nationale recommandée par la Chine (**organe de normalisation**) | NC | rapporté par le biais de la couverture standard; primaire sur les canaux SAC/MIIT | 2026-09-03 | _CHECTURE | La précision de l'affichage santé embarqué est normalisée séparément (pas une ligne d'importation légale). |
| SOH formulations and the QC/T 743 80% end-of-life convention | LNC Expliqueur technique des piles (industrie) | Mondial | https://lnclibattery.com/blog/evaluation-of-the-health-status-soh-of-lithium-ion-batteries/ | 2026-09-03 | SOURCE UNIQUE | Formule de SOH fondée sur la capacité; 80% as industry end-of-life reference |
| Points de base pour l'achat de VNE usagées / méthodes de test et de dépistage de charge | Yiche, Dongchedi (médias automatiques; références de méthode) | NC | https://hao.m.yiche.com/wenzhang/107776270/ | 2026-09-03 | SOURCE UNIQUE | Méthode d'inspection, essai de charge, pratique accident/inondation/odomètre |
| 懂车帝 二手车电池检测内容 | 懂车帝（字节跳动） | NC | https://www.iesdouyin.com/share/video/7618925618490849457 | 2026-09-02 | SOURCE UNIQUE | 20%-80% 充电验证衰减方法 |
| 懂车帝 二手电车三招排除事故/泡水/调表 | 懂车帝（视频） | NC | https://www.iesdouyin.com/share/video/7678314679869430004 | 2026-09-02 | SOURCE UNIQUE | 事故/泡水/调表排查方法、电池包护板拆装痕迹 |
| Jingsuncar — 2026 二手新能源出口指南 | Jingsuncar（行业站） | NC | https://www.jingsuncar.com/news/2026-must-see-guide-for-buying-used-new-energy-85493284.html | 2026-09-02 | SOURCE UNIQUE | 出口 SOH≥80% 认证门槛（EU/东盟） |

*Note de confiance: what the battery standards define (SOH measurement, cycle testing, the 80% engineering convention) is VERIFIED/CROSS_CHECKED against standards bodies. The earlier "SOH ≥80% required to clear EU/ASEAN certification" claim had no official source and has been removed: Il n'existe pas de seuil d'importation légal universel pour les produits de santé naturels et la règle de l'autorité de destination doit être obtenue par pays. Les vidéos de méthode d'inspection ne sont utilisées que comme références de méthode. *
## Révision de la rédaction
- **Auteur / réviseur**: [Équipe de rédaction d'AutoBridge Export](/auteurs/) · méthode selon notre [Politique éditoriale](/politique éditoriale/)
- **Dernière revue**: 2026-09-05
- **Marché de référence**: mondial (du côté des exportations de la Chine utilisant des VE)
- **Méthode de vérification**: Base des organismes de normalisation pour les concepts de SOH; supports utilisés uniquement pour la méthode d'inspection; ligne d'ingénierie maintenue distincte de toute règle juridique de destination
- **Norme de rédaction**: Recherches et écrits provenant des sources énumérées ci-dessus (recherches de bureau; aucune conduite directe, démontage ou importation n'est revendiquée). La confiance de la source est affichée par ligne; tout point que nous ne pouvons confirmer indépendamment est présenté comme un élément de vérification plutôt que comme un fait.
#AutoBridge #UsedEVInspection #BatterySOH #ExportProcurement #PrePurchaseCheck
