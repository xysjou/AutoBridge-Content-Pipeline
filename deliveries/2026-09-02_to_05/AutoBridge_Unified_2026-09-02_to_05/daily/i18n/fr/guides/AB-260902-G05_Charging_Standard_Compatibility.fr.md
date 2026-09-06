# VE chinois Normes de charge à l'étranger: GB/T vs CCS2 vs CHAdeMO vs NACS Compatibilité

## OEuvre Métadonnées
- ** Titre du référencement**: GB/T vs CCS2 vs CHAdeMO vs NACS: Compatibilité des exportations de véhicules électriques chinois
- **Description détaillée**: Une charge d'EV du marché chinois en Europe, au Japon ou en Amérique du Nord? GB/T 20234.3/27930 expliqué, la carte de connecteur par région, les entrées de version export, les adaptateurs et la direction ChaoJi.
- **URL suggérée**: /guides/chinese-ev-chargement-norme-compatibilité/
- ** H1 **: Un VE chinois facturera-t-il outre-mer? GB/T, CCS2, CHAdeMO et NACS Compatibilité expliquée
- **Mot-clé principal**: GB/T CCS2 Compatibilité standard de charge CHAdeMO à l'exportation
- **Conditions de recherche secondaires**: adaptateur de charge pour EV chinois, GB/T 20234.3 DC, protocole GB/T 27930, CCS2 version d'exportation EV, ChaoJi standard
- **Suggestions de lien interne**: /véhicules/byd-yuan-plus/; /guides/drive-droite-chinois-cars/; /guides/utilisé-chinois-ev-inspection/
- **Suggestions d'image**: carte standard du connecteur mondial; comparaison GB/T vs CCS2 entrée; entrée export-version en usine; avertissement de conformité de l'adaptateur
- ** Suggestions d'ALT**: "Carte mondiale des normes de connecteurs à recharge rapide en courant continu"; "Inlets de recharge en gaz naturel et en gaz naturel et CCS2 côte à côte"; "Inlet d'exportation en EV chinois CCS2"

## Pourquoi le connecteur décide si la voiture est utilisable

Une EV domestique chinoise qui passe les douanes peut encore être inutilisable si son entrée de recharge ne correspond pas au réseau public de recharge. La compatibilité de charge est un problème de ** connecteur physique plus de protocole de communication**, et non une préférence de marque, et il doit être résolu **avant** le véhicule est spécifié pour l'exportation - la mise à niveau d'un entrée après l'arrivée est coûteuse et parfois non conforme.

## La carte des normes (charge rapide du DC)

| Norme | Déploiement primaire | Annexe |
|---|---|---|
| **GB/T 20234.3 ** (DC) + **GB/T 27930 ** (communication CAN) | Chine (véhicules nationaux chinois) | GB/T 20234.3-2023 élève la limite supérieure à ** 1500 V/ 800 A** (sources industrielles transcochées) |
| ** CCS2 (Combo 2)** | L'Europe et de nombreux marchés d'exportation | Inlet AC/DC combiné; dominant dans l'UE |
| ** CCS1 (Combo 1)** | Amérique du Nord | Variante régionale du CSC |
| **************************************************************************************************************************************************************************************************************************************************************** | Japon et marchés sélectionnés | Originaire du Japon |
| **NACS** | Amérique du Nord | Déploiement en Amérique du Nord (déploiement de 2026 non officiellement vérifié ici) |

Ces connecteurs DC sont ** physiquement incompatibles**: you cannot plug a GB/T gun into a CCS2 socket. L'entrée AC (faible/nuit) diffère également par le marché et doit être contrôlée séparément — une voiture peut se charger rapidement sur une norme alors que son entrée AC a encore besoin d'attention.

## Ce que signifie en pratique "Marché chinois GB/T"

Les véhicules électriques chinois de transport sont généralement expédiés avec une recharge à courant continu **GB/T**  and  la poignée de main de communication basée sur le GB/T 27930 CAN. Lorsque le réseau de destination est principalement composé de ** CCS2 (Europe), CHAdeMO (Japon) ou NACS/ CCS1 (Amérique du Nord)**, cela crée le goulot de compatibilité que l'importateur doit concevoir. Surtout, **GB/T et CCS2 n'ont pas de compatibilité physique directe — un adaptateur est nécessaire pour les relier** (par comparaison avec l'industrie EVSE), et un adaptateur doit également faire fonctionner la poignée de main de communication, et non pas simplement s'adapter mécaniquement.

## Trois façons de résoudre Il — par ordre de préférence

1. **Commander la version d'exportation de l'usine avec l'entrée de destination.** De nombreux fabricants chinois construisent des variantes du marché d'exportation équipées du connecteur cible (par exemple CCS2) plutôt que de l'entrée nationale GB/T. C'est la route la plus propre car les entrées, les logiciels embarqués et la certification sont alignés. Confirmer le connecteur exact **par VIN/modèle sur la configuration officielle d'exportation de la marque** — les versions nationales et d'exportation du modèle « même » diffèrent.
2. **Utilisez un adaptateur certifié (à destination du GB/T --).** Lorsqu'une version d'exportation d'usine n'est pas disponible, un adaptateur permet de combler les différences physiques/de communication. Traitez cela comme une question de conformité, et non comme du matériel: ** certains marchés limitent l'utilisation de l'adaptateur**, et la certification/le statut juridique de l'adaptateur n'a pas été saisi d'une source officielle – vérifier localement et porter les documents de certification de l'adaptateur. La vitesse de charge de l'adaptateur et la fiabilité de la poignée de main doivent être testées avant le déploiement de la flotte.
3. **Solve-le du côté de l'infrastructure.** Les exploitants de dépôts/fleet peuvent installer des chargeurs capables de GB/T dans leurs propres locaux, ce qui élimine la dépendance au réseau public, viable pour les flottes fermées, et non pour les clients de détail qui dépendent de stations publiques.

## ChaoJi: la direction future, pas la faute d'aujourd'hui

La Chine et le Japon **Le projet ChaoJi** ultra-rapide de recharge est conçu de manière à ce qu'une interface physique commune soit compatible avec les systèmes **GB/T, CHAdeMO et CCS** et qu'elle soit considérée comme une future direction de normalisation DC (sur un document officiel de l'Association CHAdeMO). C'est un contexte tourné vers l'avenir: ne **pas** supposer qu'un véhicule GB/T de production actuel bénéficie déjà de ChaoJi – vérifier le support du modèle officiellement avant de l'utiliser comme point de vente.

## Ce qu'autoBridge ajoute au-delà d'un graphique de connecteur
Un graphique standard vous indique que GB/T diffère de CCS2; il ne vous indique pas si *ce VIN* sera chargé. La méthode recommandée consiste à enregistrer **inlet physique, protocole de poignée de main et cote de chargeur embarqué comme une note liée au VIN**, à distinguer un adaptateur matériel ** (mécanique seulement) d'une passerelle de protocole (GB/T 27930 poignée de main)** dans le dossier d'achat, et à confirmer l'effet de légalité et de garantie de l'adaptateur ** dans la destination** avant le dépôt plutôt qu'après l'arrivée.
## Matrice de vérification par véhicule

Pour chaque modèle/trim que vous exportez, enregistrez-le dans une feuille:

- Entrée intérieure: GB/T DC + type d'entrée AC
- Entrée(s) d'exportation disponible(s): CCS2 CHAdeMO NACS CCS1 par VIN
- Protocole de communication et si le firmware d'exportation supporte la poignée de main de destination
- Si adaptateur: modèle d'adaptateur, certification, courant max/tension et légalité locale
- Réalité du réseau public dans la destination (standard DC dominant; standard de prise AC)
- Incidences de la garantie de toute modification d'entrée/d'adaptation

## Avant paiement

- Confirmer les normes de connecteur AC DC ** et** dominantes de la destination.
- Obtenir la confirmation officielle de la marque pour le connecteur de conversion à l'exportation pour le VIN exact — ne pas déduire de la spécification nationale.
- Si vous vous fiez à un adaptateur, confirmez la légalité/certification locale et testez une vraie session de recharge rapide.
- Pour les flottes, décider si les chargeurs de dépôts éliminent la dépendance du réseau public.
- Traiter les revendications de ChaoJi comme faisant face à l'avenir, sauf si elles sont officiellement confirmées pour l'unité.

## Foire aux questions

**Une taxe de VE GB/T chinoise peut-elle être directement appliquée sur l'Europe CCS2 ?** Non — GB/T et CCS2 sont physiquement incompatibles; vous avez besoin d'une version d'exportation CCS2 d'usine ou d'un adaptateur adapté et conforme localement.
**Qu'est-ce que GB/T 27930 ?** C'est le protocole de communication basé sur CAN utilisé à côté du connecteur GB/T 20234.3 DC en Chine; la poignée de main compte autant que la forme de la prise.
**Un adaptateur est-il une solution permanente?** Elle peut combler l'écart, mais la légalité de l'adaptateur varie selon le marché et la vitesse/fiabilité doit être testée; l'entrée d'exportation de l'usine est préférée.
**Les marques chinoises vendent-elles des versions CCS2?** Beaucoup de versions d'exportation de construction avec le connecteur de destination — confirmer par modèle/VIN sur la configuration officielle d'exportation plutôt que de supposer.
**Est-ce que Chao Ji rend tous les connecteurs compatibles maintenant?** ChaoJi est une direction future conçue pour la compatibilité; les voitures de production actuelles ont encore besoin de confirmation par modèle.

## Enregistrement d'image
- IMAGE_ASSET_PATH: aucun sécurisé dans le dépôt
- ORIGINAL_IMAGE_URL: non capturé
- SOURCE_PAGE: non capturé
- SOURCE_FILE_PAGE: sans objet — aucun fichier multimédia candidat identifié (aucune licence pour affirmer)
- HÔTEL DE DROITS: NON CONfirmÉ
- LICENSE_OR_USAGE_BASIS: aucune image sécurisée — aucune image de tiers ne peut être publiée jusqu'à ce que les droits soient effacés
- _DATE DE CONTRÔLE: 2026-09-06
- MODEL_TOPIC_MATCH: doit correspondre au modèle exact/version (ou au sujet du guide) et au marché de référence ci-dessus
- IMAGE_SCOPE_NOTE: correspond à la famille/sujet du modèle exact seulement; ne doit pas impliquer une taille/modèle spécifique-année, VIN réel, inspection en personne ou transaction réelle
- IMAGE_RIGHTS_STATUS: FAIL (aucun actif autorisé capturé; un détenteur de place ou -tain vieille image - Note n'est pas accepté)
- C'est une question de "relation" Aucune image réutilisable ne peut être sécurisée: Wikimedia Commons/Flickr sont inaccessibles depuis l'environnement de recherche, les bibliothèques de stock nécessitent un accès authentifié API/licence, et une image de page web OEM n'est PAS une subvention de réutilisation commerciale; aucune photo appartenant à AutoBridge n'existe. Il a gardé la FAIL plutôt que de l'affirmer.
- ALAT par langue:
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

## Sources et vérification

| Titre de la source | Organisation | Marché | URL | Vérification | Confiance | Faits corroborés |
|---|---|---|---|---|---|---|
| Présentation standard de ChaoJi (officielle) | CHAdeMO Association (organisme de normalisation) | CN/JP/Global | https://www.chademo.com/wp2016/wp-content/uploads/ChaoJi202006/ChaoJi_Presenataion_EN.pdf | 2026-09-02 | VÉRIFIER | ChaoJi conçu compatible avec GB/T/CHAdeMO/CCS |
| Voies de certification standard de charge | Essais Huayu (organisme de certification) | Mondial | http://www.huayutest.com/zixun/87747.html | 2026-09-02 | _CHECTURE | Déploiement régional CHAdeMO/CCS, différences de certification |
| Normes de charge des connecteurs | céhome (médias industriels) | NC | https://m.cehome.com/news/20260809/389612.shtml | 2026-09-02 | _CHECTURE | GB/T 20234.3-2023 1500V/800A, GB/T 27930, ChaoJi |
| GB/T, CCS2, Type 2, NACS, CHAdeMO comparé | (industrie) | Mondial | https://www.evse-chargers.com/news/understanding-ev-charging-standards-gb-t-ccs2-type-2-nacs-and-chademo-compared-283319.html | 2026-09-02 | _CHECTURE | GB/T-CCS2 nécessite un adaptateur; matrice de compatibilité |
| Guide des normes mondiales de recharge des véhicules électriques | MARUIKEL (industrie) | Mondial | https://www.maruikel.com/es/blog/guide-to-global-ev-charging-standards-type-1-type-2-ccs-chademo-gbt.html | 2026-09-02 | _CHECTURE | Connecteur national GB/T par rapport au connecteur de destination de la version export |
| Adaptateur GB/T-à-CHAdeMO B2B guide | Auto électrique Chine (industrie) | Mondial | https://www.electricautochina.com/comprehensive-b2b-guide-to-gbt-to-chademo-adapters-for-exported-chines/ | 2026-09-02 | _CHECTURE | Compatibilité des exportations goulot d'étranglement |

*Note de confiance (standard AutoBridge): les faits de niveau standard sont VÉRIFIÉS/CROSS_CHECKED (CHadeMO) L'association est un organisme de normalisation). Les connecteurs d'exportation par modèle, la légalité de l'adaptateur par pays et le calendrier de déploiement du NACS n'ont pas été saisis et doivent être confirmés par le NIV et par l'autorité de destination. *

## Révision de la rédaction
- **Auteur réviseur**: [Équipe de rédaction d'AutoBridge Export](/auteurs/) · méthode selon notre [Politique éditoriale](/politique éditoriale/)
- **Dernière révision**: 2026-09-05
- **Marché de référence**: mondial (du côté des exportations de la Chine; déploiement UE/JP/NA)
- **Méthode de vérification**: Document de la caisse de normalisation et sources industrielles vérifiées par recoupement; connecteurs spécifiques au modèle laissés à la confirmation officielle par NIV
- **Norme de rédaction**: Recherches et écrits provenant des sources énumérées ci-dessus (recherches de bureau; aucune conduite directe, démontage ou importation n'est revendiquée). La confiance de la source est affichée par ligne; tout point que nous ne pouvons confirmer indépendamment est présenté comme un élément de vérification plutôt que comme un fait.
#AutoBridge #ChargingStandards #GBTvsCCS #EVExport #ConnectorCompatibility
