# Chinesisches EV Im Ausland geltende Gebührenstandards: GB/T vs. CCS2 vs. CHAdeMO vs. NACS-Kompatibilität

## SEO Metadaten
- **SEO Titel **: GB / T vs CCS2 vs CHAdeMO vs NACS: Chinesische EV Export Kompatibilität
- **Meta Description**: Wird ein chinesisches Elektrofahrzeug in Europa, Japan oder Nordamerika aufgeladen? GB/T 20234.3/27930 erklärt, die Steckerkarte nach Region, Exportversion Eingänge, Adapter und die ChaoJi Richtung.
- **Vorgeschlagene URL**: /guides/chinese-ev-charging-standard-compatibility/
- ** H1 **: Wird ein chinesisches EV im Ausland aufladen? GB/T, CCS2, CHAdeMO und NACS Kompatibilität erklärt
- **Hauptschlüsselwort**: GB/T CCS2 CHAdeMO Ladestandard Exportkompatibilität
- **Secondary Search Terms**: Chinesischer EV-Exportladeadapter, GB/T 20234.3 DC Schnellladung, GB/T 27930 Protokoll, CCS2 Exportversion EV, ChaoJi Standard
- **Interne Linkvorschläge**: /Fahrzeuge/byd-yuan-plus/; /guides/right-hand-drive-chinese-cars/; /guides/used-chinese-ev-inspection/
- **Bildvorschläge**: Weltstecker-Standardkarte; GB/T vs. CCS2 Einlassvergleich; Fabrikexportversion Einlass; Adapter-Compliance-Warnung
- **ALT Vorschläge**: "Weltkarte der DC-Schnellladesteckernormen"; "GB/T und CCS2 Ladeeingänge nebeneinander"; "Chinesischer EV-Export-Version CCS2 Einlass"

## Warum der Connector entscheidet, ob das Auto verwendbar ist

Ein inländisches chinesisches EV, das den Zoll passiert, kann immer noch effektiv unbrauchbar sein, wenn seine Ladebuchse nicht mit dem öffentlichen Ladenetz übereinstimmt. Ladekompatibilität ist ein Problem mit einem physischen Steckverbinder und einem Kommunikationsprotokoll, keine Markenpräferenz, und es muss gelöst werden, bevor das Fahrzeug für den Export spezifiziert wird - die Nachrüstung eines Einlasses nach der Ankunft ist kostspielig und manchmal nicht konform.

## Die Standard-Karte (DC Fast Charging)

| Standard | Primäre Bereitstellung | Anmerkungen |
|---|---|---|
| **GB/T 20234.3 ** (DC) + **GB/T 27930 ** (CAN-Kommunikation) | China (inländische chinesische Fahrzeuge) | GB/T 20234.3-2023 hebt die Obergrenze auf ** 1500 V / 800 A** an (geprüfte Branchenquellen) |
| ** CCS2 (Combo 2)** | Europa und viele Exportmärkte | Kombinierter AC/DC-Einlass; dominant in der EU |
| ** CCS1 (Combo 1)** | Nordamerika | Regionale Variante von CCS |
| ****************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************** | Japan und ausgewählte Märkte | Ursprung in Japan |
| **NACS** | Nordamerika | Einsatz in ganz Nordamerika (2026 Rollout-Timing hier nicht offiziell verifiziert) |

Diese DC-Anschlüsse sind **physikalisch gegenseitig inkompatibel**: you cannot plug a GB/T gun into a CCS2 socket. Der AC-Einlass (langsam / über Nacht) unterscheidet sich ebenfalls vom Markt und muss separat überprüft werden - ein Auto kann sich auf einer Norm schnell aufladen, während sein AC-Einlass noch Aufmerksamkeit benötigt.

## Was "Chinese-Market GB/T" in der Praxis bedeutet

Inländische chinesische EVs liefern in der Regel mit **GB / T ** DC-Ladung und dem GB / T 27930 CAN-basierten Kommunikationshandshake. Wenn das Zielnetz überwiegend ** CCS2 (Europa), CHAdeMO (Japan) oder NACS/ CCS1 (Nordamerika)** läuft, entsteht der Kompatibilitätsengpass, den ein Importeur herum entwerfen muss. Entscheidend ist, dass **GB/T und CCS2 keine direkte physische Kompatibilität haben - ein Adapter ist erforderlich, um sie zu überbrücken ** (nach einem EVSE-Branchenvergleich), und ein Adapter muss auch den Kommunikations-Handshake funktionieren lassen, nicht nur mechanisch passen.

## Drei Wege zu lösen Es — in der Reihenfolge der Präferenz

1. **Bestellen Sie die Factory Export Version mit dem Zieleingang. ** Viele chinesische Hersteller bauen Exportmarktvarianten, die mit dem Zielstecker (z. B. CCS2) anstelle des inländischen GB / T-Einlasses ausgestattet sind. Dies ist die sauberste Route, da Einlass, Onboard-Software und Zertifizierung aufeinander abgestimmt sind. Bestätigen Sie den genauen Stecker ** pro VIN / Modell in der offiziellen Exportkonfiguration der Marke ** - Inlands- und Exportversionen des "gleichen" Modells unterscheiden sich.
2. ** Verwenden Sie einen zertifizierten Adapter (GB/T ↔ Ziel).** Wenn eine Factory Export Version nicht verfügbar ist, überbrückt ein Adapter physische/Kommunikationsunterschiede. Behandeln Sie dies als Compliance-Frage, nicht nur als Hardware: ** Einige Märkte beschränken die Verwendung von Adaptern **, und die Adapterzertifizierung / der rechtliche Status wurde nicht von einer offiziellen Quelle erfasst - überprüfen Sie dies lokal und tragen Sie die Zertifizierungsdokumente des Adapters. Die Ladegeschwindigkeit und die Zuverlässigkeit des Handshakes von Adaptern sollten vor dem Rollout der Flotte getestet werden.
3. **Löse es auf der Infrastrukturseite.** Depot-/Flottenbetreiber können GB/T-fähige Ladegeräte in ihren eigenen Räumlichkeiten installieren, wodurch die Abhängigkeit vom öffentlichen Netz beseitigt wird – für geschlossene Flotten, nicht für Endkunden, die auf öffentliche Stationen angewiesen sind.

## ChaoJi: Die zukünftige Richtung, nicht der heutige Zahlungsausfall

China-Japan **ChaoJi** Ultra-Schnellladeprojekt ist so konzipiert, dass eine gemeinsame physische Schnittstelle zwischen **GB/T, CHAdeMO und CCS** Systemen kompatibel ist und als zukünftige DC-Standardisierungsrichtung betrachtet wird (laut einem offiziellen Dokument der CHAdeMO Association). Es ist ein zukunftsgerichteter Kontext: Gehen Sie nicht davon aus, dass ein aktuelles GB / T-Fahrzeug bereits von ChaoJi profitiert - überprüfen Sie die Modellunterstützung offiziell, bevor Sie es als Verkaufsargument verwenden.

## Was AutoBridge über ein Connector-Diagramm hinausfügt
Ein Standarddiagramm sagt Ihnen, dass GB / T von CCS2 abweicht; es sagt Ihnen nicht, ob * diese VIN * aufgeladen wird. Die empfohlene Methode ist, den physischen Einlass, das Handshake-Protokoll und die Bordladefunktion als eine VIN-gebundene Notiz zu erfassen **, einen **Hardwareadapter (nur mechanisch) von einem Protokoll-Gateway (GB / T 27930 Handshake) ** in der Kaufdatei zu unterscheiden und die Rechtmäßigkeit und den Garantieeffekt des ** Adapters am Zielort ** vor der Einzahlung und nicht nach der Ankunft zu bestätigen.
## Matrix für die Fahrzeugverifikation

Für jedes Modell / Trimm, das Sie exportieren, notieren Sie in einem Blatt:

- Inländische Einlassvorrichtung: GB/T DC + AC-Einlassvorrichtung
- Verfügbare Fabrik-Ausfuhreinfuhren: CCS2 / CHAdeMO / NACS / CCS1 by VIN
- Kommunikationsprotokoll und ob die Export-Firmware den Ziel-Handshake unterstützt
- Wenn Adapter-basiert: Adapter-Modell, Zertifizierung, max. Strom/Spannung und lokale Legalität
- Public-Network-Reality im Zielort (dominanter DC-Standard; AC-Sockel-Standard)
- Auswirkungen auf die Gewährleistung einer Änderung des Einlasses/Adapters

## Vor Zahlung

- Bestätigen Sie die dominanten DC ** und ** AC-Anschlussstandards des Ziels.
- Erhalten Sie die offizielle Exportversionsbestätigung der Marke für die genaue VIN - schließen Sie nicht auf die inländische Spezifikation.
- Wenn Sie sich auf einen Adapter verlassen, bestätigen Sie die lokale Legalität / Zertifizierung und testen Sie eine echte Schnellladesitzung.
- Bei Flotten ist zu entscheiden, ob Depot-Ladegeräte die Abhängigkeit des öffentlichen Netzes beseitigen.
- Behandeln ChaoJi Ansprüche als zukunftsgerichtet, es sei denn, offiziell für die Einheit bestätigt.

## Häufig gestellte Fragen

**Kann ein chinesisches GB/T EV direkt auf europäische CCS2 aufgeladen werden? ** Nein - GB / T und CCS2 sind physisch inkompatibel; Sie benötigen eine werkseigene Exportversion CCS2 oder einen geeigneten, lokal kompatiblen Adapter.
**Was ist GB/T 27930? ** Es ist das CAN-basierte Kommunikationsprotokoll, das neben dem GB/T 20234.3 DC-Anschluss in China verwendet wird; der Handschlag ist ebenso wichtig wie die Steckerform.
**Ist ein Adapter eine dauerhafte Lösung?** Es kann die Lücke schließen, aber die Legalität des Adapters variiert je nach Markt und Geschwindigkeit / Zuverlässigkeit sollte getestet werden; Der Fabrikexporteingang wird bevorzugt.
**Verkaufen chinesische Marken CCS2 Versionen?** Viele bauen Exportvarianten mit dem Zielstecker - bestätigen Sie pro Modell / VIN auf der offiziellen Exportkonfiguration, anstatt anzunehmen.
**Does Chao Ji macht jetzt alle Steckverbinder kompatibel?** ChaoJi ist eine für Kompatibilität zukünftige Richtung entworfen; aktuelle Serienautos müssen noch pro Modell bestätigt werden.

## Bildaufzeichnung
- IMAGE_ASSET_PATH: keine gesicherte Datei
- ORIGINAL_IMAGE_URL: nicht erfasst
- SOURCE_PAGE: nicht erfasst
- SOURCE_FILE_PAGE: Entfällt — keine Kandidaten-Mediendatei identifiziert (keine Lizenz zur Geltendmachung)
- RIGHTS_HOLDER: nicht bestätigt
- LICENSE_OR_USAGE_BASIS: keine gesicherte — kein Bild von Dritten darf veröffentlicht werden, bis die Rechte gelöscht sind
- CHECKED_DATUM: 2026-09-06
- MODEL_TOPIC_MATCH: muss mit dem genauen Modell/der genauen Version (oder dem Leitthema) und dem Referenzmarkt oben übereinstimmen
- IMAGE_SCOPE_NOTE: nur die genaue Modellfamilie/das genaue Thema angeben; darf keine spezifische Trimm-/Modelljahr-, echte VIN-, persönliche Inspektion oder tatsächliche Transaktion implizieren
- IMAGE_RIGHTS_STATUS: FAIL (kein lizenziertes Asset erfasst; ein Platzhalter oder ein Hinweis „altes Bild behalten wird nicht akzeptiert)
- BLOCK_REASON: Es konnte kein wiederverwendbares Bild gesichert werden: Wikimedia Commons/Flickr sind aus der Forschungsumgebung nicht erreichbar, Lagerbibliotheken erfordern authentifizierten API/Lizenzzugriff und ein OEM-Webseitenbild ist KEIN kommerzielles Wiederverwendungsstipendium; es gibt kein AutoBridge-eigenes Foto. Nein, aber nicht nur vereitelt.
- ALT nach Sprache:
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

## Quellen & Verifizierung

| Quelle: | Organisation | Markt | URL | Geprüft | Vertrauen | Belegte Fakten |
|---|---|---|---|---|---|---|
| ChaoJi Standardpräsentation (offiziell) | CHAdeMO Association (Standards Body) | CN/JP/Global | https://www.chademo.com/wp2016/wp-content/uploads/ChaoJi202006/ChaoJi_Presenataion_EN.pdf | 2026-09-02 | ÜBERPRÜFUNG | ChaoJi kompatibel mit GB/T/CHAdeMO/CCS |
| Standard-Entgeltungspfade für die Gebührenerhebung | Huayu Testing (Zertifizierungsstelle) | Global | http://www.huayutest.com/zixun/87747.html | 2026-09-02 | CROSS_CHECKED | CHAdeMO/CCS-Regionaleinsatz, Zertifizierungsunterschiede |
| Standards für Ladesteckverbinder | cehome (Industriemedien) | CN | https://m.cehome.com/news/20260809/389612.shtml | 2026-09-02 | CROSS_CHECKED | GB/T 20234.3-2023 1500V/800A, GB/T 27930, ChaoJi |
| GB/T, CCS2, Typ 2, NACS, CHAdeMO verglichen | evse-chargers.com (Industrie) | Global | https://www.evse-chargers.com/news/understanding-ev-charging-standards-gb-t-ccs2-type-2-nacs-and-chademo-compared-283319.html | 2026-09-02 | CROSS_CHECKED | GB/T ↔ CCS2 erfordert Adapter; Kompatibilitätsmatrix |
| Leitfaden für globale EV-Ladestandards | MARUIKEL (Industrie) | Global | https://www.maruikel.com/es/blog/guide-to-global-ev-charging-standards-type-1-type-2-ccs-chademo-gbt.html | 2026-09-02 | CROSS_CHECKED | Inländische GB/T vs Exportversion Destination Connector |
| GB/T-zu-CHAdeMO-Adapter B2B Führung | Electric Auto China (Industrie) | Global | https://www.electricautochina.com/comprehensive-b2b-guide-to-gbt-to-chademo-adapters-for-exported-chines/ | 2026-09-02 | CROSS_CHECKED | Engpass bei der Ausfuhrverträglichkeit |

*Vertrauenserklärung (AutoBridge-Standard): Standard-Level-Fakten sind VERIFIZIERT/CROSS_CHECKED (CHAdeMO) Die Vereinigung ist ein Standardisierungsgremium. Pro Modell Exportsteckverbinder, Adapter Legalität nach Land und NACS Rollout Timing wurden nicht erfasst und müssen pro VIN und pro Zielbehörde bestätigt werden. *

## Editorial Review
- **Autor / Rezensent**: [AutoBridge Export Editorial Team](/Autoren/) · Methode nach unserer [Editorial Policy](/editorial-policy/]
- **Zuletzt überprüft**: 2026-09-05
- **Referenzmarkt**: Global (China-Exportseite; EU/JP/NA-Einsatz)
- **Verifizierungsmethode**: Standard-Body-Dokument plus abgeglichene Branchenquellen; modellspezifische Konnektoren, die der offiziellen Bestätigung per VIN überlassen werden
- **Editorialstandard**: Recherchiert und geschrieben aus den oben aufgeführten Quellen (Desk-Recherche; kein Fahren aus erster Hand, Teardown oder Import wird beansprucht). Das Vertrauen in die Quelle wird pro Zeile angezeigt; jeder Punkt, den wir nicht unabhängig bestätigen können, wird als Verifizierungselement dargestellt und nicht als Tatsache behauptet.
#AutoBridge #ChargingStandards #GBTvsCCS #EVExport #ConnectorCompatibility
