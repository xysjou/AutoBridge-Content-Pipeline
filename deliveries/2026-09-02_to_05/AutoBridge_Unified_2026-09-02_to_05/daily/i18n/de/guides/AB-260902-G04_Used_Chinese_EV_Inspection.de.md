# Gebrauchte chinesische EV-Vorausfuhrkontrolle: Batterie-SOH richtig gemacht, plus Unfall, Flut und Kilometerzählerprüfungen
## SEO Metadaten
- **SEO Titel**: Gebrauchte chinesische EV-Inspektion: Batterie SOH, Flut & Odometer Kontrollen
- **Meta Description**: Wie man ein gebrauchtes chinesisches EV vor dem Export inspiziert - was SOH tatsächlich unter Batteriestandards, einem gemessenen Ladetest, Zellbilanzmessung, Unfall- / Flut-Screening und Kilometerzähler-Vs-Zyklus-Gegenkontrollen ohne erfundenen gesetzlichen Schwellenwert bedeutet.
- **Vorgeschlagene URL**: /guides/used-chinese-ev-inspection/
- ** H1 **: Inspektion eines gebrauchten chinesischen EV vor dem Export: Was die Batterienummern bedeuten und was abzulehnen ist
- ** Primäres Keyword**: gebrauchte chinesische EV-Inspektionsbatterie SOH Checkliste
- **Secondary Search Terms**: EV Batterie SOH Standard QC/T 743, GB/T 31484 Zykluslebensdauer, verwendete EV Zelle Spannungsungleichgewicht, EV Flutschaden Inspektion, Kilometerzähler Rollback Batteriezykluszahl
- **Interne Linkvorschläge**: /guides/verify-china-car-export-supplier/; /guides/chinese-ev-charging-standard-compatibility/; /guides/import-chinese-ev-to-russia-eac-ottc/
- **Bildvorschläge**: SOH-Diagnosegerät und Zellenspannungsauslese; metered 20–80% charge worksheet; Prüfpunkte für den Batterieboden; Dienst/Ansprüche — Muster
- **ALT-Vorschläge**: "Unabhängiger Diagnosebericht mit SOH und maximaler Zellspannungsdifferenz"; "Mess-Arbeitsblatt für den Ladeenergie-Prüfstrom"; "Unterboden-Prüfpunkte des EV-Batteriepacks"
## Scope: ein Inspektionshandbuch, keine New-vs-Used-Debatte
Die Entscheidung, **used** zu kaufen, wird als gegeben angenommen; Diese Seite behandelt die **technische Inspektion vor dem Export**. Die Wirtschaftlichkeit eines gebrauchten EV wird von der Hochvoltbatterie dominiert: Ein sauberer Körper mit einer abgenutzten Packung kann weniger wert sein als die Ersatzkosten nach dem Versand, so dass sich die Inspektionsreihenfolge von einem ICE-Auto unterscheidet. A central aim is to be precise about what "SOH 80%" actually is — an engineering reference, not a universal customs line.
## What SOH Is — and What the 80% Figure Actually Means
**State of Health (SOH)** drückt die aktuelle maximale nutzbare Kapazität eines Pakets im Verhältnis zu seiner neuen Nennkapazität aus (kapazitätsbasierte SOH = gealterte Kapazität ÷ Nennkapazität). Es ist wichtig, eine ** Engineering-End-of-Life-Konvention** von einer ** legalen Importschwelle** zu trennen, da sie routinemäßig verwirrt sind:
- The **~80%** figure originates in **battery standards and warranty practice**, not import law. China's automotive-industry standard **QC/T 743** treats capacity falling to 80% of nominal as an end-of-life reference; **GB/T 31484 ** spezifiziert Traktions-Batteriezyklus-Lebensdauer *Prüfmethoden*; **IEC 62660 ** (Teile 1/2) standardisiert die Leistung von Lithium-Ionen-Zellen/Lebensdauerprüfung; und der neuere empfohlene nationale Standard **GB/T 46991.1-2025 ** (entwickelt unter MIIT/SAC) befasst sich mit der *Genauigkeit und Haltbarkeit von On-Board-SOH/SOC-Displays*. Dies sind Dokumente von Standards-Body (VERIFIZIERT, was sie definieren).
- **There is no single universal legal SOH threshold for importing a used EV.** No regulation cited in this research sets "80%" as a blanket customs or type-approval gate that applies across the EU, ASEAN or anywhere else. Be explicit about what 80% is **not**: Es ist ** kein Gebrauchtwagen-Importschwellenwert **, es ist ** kein einheitliches Batterie-Ruhestandsgesetz ** und es ist **nicht der Garantieschwellenwert jedes Herstellers ** (eine gegebene Garantie kann eine andere Zahl verwenden). Ein Zielort kann seine eigene Bedingungsregel auferlegen und ein Käufer kann eine private kommerzielle Linie festlegen - aber jedes ist ein *anderes Instrument *. Die Bestimmungszertifizierungsstelle / Importeurs eigenen Akzeptanzstandard gilt, und muss pro Land bestätigt werden, anstatt angenommen.
Diese Unterscheidung ändert, wie Sie die Nummer verwenden: treat the ~80% engineering convention purely as a **commercial/engineering reference for pricing and rejection**, while separately confirming whether the destination sets any legal condition. No chemistry-specific "85% NMC line" is asserted here because no standard or manufacturer source captured for this article establishes it as a rule.
## Erhalten einer vertretbaren SOH-Zahl
- Read the in-car/cluster health display, but do not stop there — on-board displays are estimates and the new GB/T 46991.1 display-accuracy standard applies to new production, not necessarily to older used units.
- Beauftragen Sie einen **unabhängigen Diagnosebericht eines Drittanbieters**, der SOH** und die maximale Spannung von Zelle zu Zelle** aufzeichnet: Ein großes Ungleichgewicht markiert schwache Module, selbst wenn die Überschrift SOH gesund aussieht.
- Chinesische Marken teilen nicht ein OBD-/Diagnoseprotokoll und die Berichtsformate von Drittanbietern sind nicht standardisiert, daher behalten Sie den Rohbericht (Tool, Softwareversion, Datum, Umgebungstemperatur) als Beweis. Markenoffizielle Batteriegesundheits-/Garantiekriterien sollten bei der Marke angefordert werden, wenn verfügbar, anstatt erraten zu werden.
## Cross-Check mit einem gemessenen Live-Charge-Test (ein Screening-Cross-Check, keine SOH-Berechnung)
Ein statischer SOH-Wert kann falsch dargestellt werden; ein Ladungstest übt die Packung aus. Charge from roughly **20% to 80%** on a **metered** charger, recording start/end SOC, kWh delivered, the power curve and elapsed time, and compare delivered energy against the expected ~60% of usable pack capacity. **Behandeln Sie dies streng als Screening-Kreuzprüfung, nicht als eine Möglichkeit, SOH zu berechnen. ** Ladegerät geliefert kWh ist *nicht* gleich der in den Zellen gespeicherten Energie: die Messung wird durch **Lade-/Umwandlungsverluste, Wärmemanagement-Abnahme, Umgebungs- und Packungstemperatur, BMS-SOC-Kalibrierung und den Reserve-/Oberbodenpuffer** beeinflusst. Es kann daher nur eine **grobe Anomalie** markieren. Ein Fehlbetrag auf diesem Bildschirm beweist **nicht ** an sich einen echten Kapazitätsverlust (und ein sauberer Bildschirm beweist nicht die volle Gesundheit); die formale Kapazität/SOH-Zahl erfordert noch eine qualifizierte Diagnosemethode oder Hersteller-/professionelle Testdaten. Die Unfähigkeit, den erwarteten Gebührensatz zu halten, ist ein Grund, diese tiefere Inspektion in Auftrag zu geben. Führen Sie den Bildschirm neben der Ladestandardprüfung (GB / T in China gegenüber dem Zielstecker - siehe Kompatibilitätshandbuch) aus, damit ein Soundpaket nicht durch einen inkompatiblen Einlass ausfällt.
## Die Hochspannungs-Triade jenseits von SOH
- **Unterseite der Verpackung **: Entfernen/Inspizieren der unteren Abschirmung auf Entfernung/Wiederversiegelung von Markierungen, Kratzern, Verformung oder Reparatur ohne Werk.
- **Motor- und Leistungselektronik**: Fehlercodes scannen, Warnleuchten prüfen und Fahr-/Regenerierungsverhalten bei einem Straßentest überprüfen.
- **HV-Verkabelung und Steckverbinder **: suchen Sie nach Korrosion, Retermination oder nicht-fabrikalen Verbindungen.
## Unfall, Überschwemmung und Brand-Screening
- Pull **maintenance records and insurance-claim (出险) records**; Reparatur von Baublechen oder jegliches Hinweiszeichen für die Behauptung von Überschwemmungswasser sind Gründe für eine Ablehnung.
- Überflutete Elektrofahrzeuge verbergen die Verschlechterung der Verpackung und die Korrosion des Harnischs: Unterbrettverbinder, Sitzschienen, Sicherungsboxen und das Batteriegehäuse auf Wasserleitungen/Korrosion prüfen.
- Prüfen Sie die Lücken der Platten, die Farbstärke und die Zeugenzeichen des Befestigungselements; behandeln Sie jedes Zeichen, das der Akkupack außerhalb einer qualifizierten Einrichtung geöffnet wurde, als Stoppsignal.
## Kilometerzähler vs. Ladezyklen
Ein getaktetes EV zeigt einen ** Kilometerzähler, der mit der Anzahl der Batteriezyklen und dem Verschleiß nicht übereinstimmt **. Wenn die Diagnose die Zykluszahl aussetzt, vergleichen Sie sie mit der angezeigten Kilometerleistung und dem körperlichen Verschleiß (Sitz, Lenkung, Pedale). Niedrig angezeigte Kilometerleistung gepaart mit hohen Zykluszahlen oder gealterten Komponenten ist eine Rollback-Warnung, die eine ICE-Kilometer-Überprüfung allein verpassen würde.
## Papierkram und die Destination Rule
Bewahren Sie den unabhängigen SOH/Ungleichgewichtsbericht, die Aufzeichnung der gemessenen Ladung und die Service-/Anforderungshistorie im Exportdossier auf. Separately — and this is the correction to any blanket "you need 80% to import" claim — **obtain the destination's actual used-EV condition/type rule in writing** from its certification authority or your clearance agent. Chinas eigene Exportqualifikations-/Altersregeln für Gebrauchtwagen werden von MOFCOM festgelegt und aktualisiert (siehe die Leitfaden für Lieferantenprüfung und Flottenbeschaffung). Verwenden Sie die Position des aktuellen Jahres anstelle einer älteren Blogfigur.
## Was AutoBridge über eine generische Checkliste hinausfügt
Public checklists repeat "read SOH and reject below 80%." This guide instead recommends: (1) separating the engineering 80% convention from the destination's actual legal rule, so a buyer neither walks away from a compliant car nor ships a non-compliant one on a myth; (2) Kopplung eines Messwert-Screening-Kreuztests mit einem Messwert für das Ungleichgewicht der Zellen, anstatt sich auf einen Dashboard-Screenshot zu verlassen; und (3) halten Sie den Inspektionshinweis an das **VIN und Exportdossier für die Zertifizierung verwendet, so dass das getestete Auto auf das ausgelieferte Auto rückverfolgbar ist.
## Harte Ablehnungsregeln
- Hochwasser-/Brandmarker in Schadensaufzeichnungen oder Korrosions-/Wasserlinien in der Packung oder im HV-Geschirr.
- Bauliche/Unfallreparatur in Hochspannungsbereichen oder Nachweis, dass das Paket außerhalb einer qualifizierten Einrichtung geöffnet wurde.
- Kilometerzähler, der mit der Anzahl der Zyklen und dem Verschleiß nicht übereinstimmt, ohne glaubwürdige Erklärung.
- Der Verkäufer lehnt einen Test der abgemessenen Ladung oder einen unabhängigen Diagnosebericht ab.
- Capacity/imbalance that fails **your own documented acceptance line** (set from brand warranty + destination rule + commercial margin) — not a mythical universal 80% legal gate.
## Akzeptanztestliste
- Unabhängiger Bericht: SOH ** und ** max Zellspannungsungleichgewicht, mit Werkzeug / Version / Datum aufgezeichnet.
- Metered 20→80% charge test (SOC, kWh, power curve, time).
- Batterieunterbau und HV-Steckverbinder, die auf Entfernung/Korrosion geprüft werden.
- Service + Versicherungsforderung Geschichte gezogen; Kollision / Flut / Brandmarker überprüft.
- Odometer in Übereinstimmung mit Ladezyklen und körperlichem Verschleiß.
- Destination used-EV rule confirmed **in writing** and distinguished from the engineering 80% line.
- Verifizierte Ladeschnittstellenkompatibilität (GB/T vs. Zielort).
## Häufig gestellte Fragen
**Is 80% SOH a legal import requirement?** No. Roughly 80% is an engineering/warranty end-of-life reference (e.g., QC/T 743; getestet nach GB/T 31484 / IEC 62660; Es ist keine Gebrauchtwagen-Importschwelle, kein einheitliches Rentengesetz und nicht die Garantielinie jedes Herstellers. There is no universal 80% customs gate, so confirm the destination's own rule.
**Why do people quote 80% then?** It comes from battery standards and warranty practice as an end-of-life/commercial reference; it is useful for pricing and rejection, but it is not import law, and no chemistry-specific 85% rule is asserted here.
**Can I calculate SOH from the charger's kWh between 20% and 80%?** Not directly. Die abgegebene Energie wird durch Ladeverluste, Wärmeabzug, Temperatur, BMS-Kalibrierung und Puffer verzerrt; Es ist ein Screening-Kreuzcheck, der grobe Anomalien aufdecken kann, wobei formale SOH einer qualifizierten Diagnose überlassen werden.
**How should SOH be evidenced?** An independent report showing SOH and cell-voltage imbalance, cross-checked by a metered 20–80% charge test, kept with tool/version/date.
**Warum ist Hochwasserschäden in einem EV besonders gefährlich?** Es kann die Packung verschlechtern und versteckte Kabelbäume / Steckverbinder korrodieren, was zu Sicherheits- und Zuverlässigkeitsfehlern nach dem Export führt.
**Wie wird Kilometerzähler-Betrug auf einem EV entdeckt?** Vergleichen Sie die angezeigte Kilometerzahl mit der Anzahl der Batteriezyklen und dem körperlichen Verschleiß; ein niedriger Kilometerzähler mit hohen Zyklen ist eine Warnung.
## Bildaufzeichnung
- IMAGE_ASSET_PATH: keine gesicherte Datei
- ORIGINAL_IMAGE_URL: nicht erfasst
- SOURCE_PAGE: nicht erfasst
- RIGHTS_HOLDER: nicht bestätigt
- LICENSE_OR_USAGE_BASIS: keine gesicherte — kein Bild von Dritten darf veröffentlicht werden, bis die Rechte gelöscht sind
- CHECKED_DATUM: 2026-09-05
- MODEL_TOPIC_MATCH: muss mit dem genauen Modell/der genauen Version (oder dem Leitthema) und dem Referenzmarkt oben übereinstimmen
- IMAGE_RIGHTS_STATUS: FAIL (kein lizenziertes Asset erfasst; ein Platzhalter oder ein Hinweis „altes Bild behalten wird nicht akzeptiert)
- ALT nach Sprache:
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

## Quellen & Verifizierung
| Quelle: | Organisation | Markt | URL | Geprüft | Vertrauen | Belegte Fakten |
|---|---|---|---|---|---|---|
| GB/T 31484 Anforderungen an die Lebensdauer von Traktionsbatterien/Prüfmethoden | Chinesische nationale Norm (**standards body**) | CN | https://www.chinesestandard.net/PDF.aspx/GBT31484-2015 | 2026-09-03 | ** ÜBERPRÜFUNG** | Rahmen für die Prüfung von Kapazität und Lebenszyklus; Anforderungen an die Erstkapazität |
| IEC 62660-1/2 Lithium-Ionen-Zelle Leistung/Lebensdauer-Test | IEC (internationales **Normengremium**) | Global | https://www.iec.ch/ (IEC 62660 series) | 2026-09-03 | ** ÜBERPRÜFUNG** | Standardisierte Zellleistung/Lebensdauertestbasis für SOH |
| GB/T 46991.1-2025 On-Board SOH/SOC Anzeigegenauigkeit & Haltbarkeit (MIIT/SAC) | Chinesisch empfohlene nationale Norm (**standards body**) | CN | Berichterstattung über Standards; primär auf SAC/MIIT-Kanälen | 2026-09-03 | CROSS_CHECKED | Die Genauigkeit des Bordzustandsdisplays ist separat standardisiert (keine legale Importlinie) |
| SOH formulations and the QC/T 743 80% end-of-life convention | LN Technischer Erklärer für Batterien (Industrie) | Global | https://lnclibattery.com/blog/evaluation-of-the-health-status-soh-of-lithium-ion-batteries/ | 2026-09-03 | SINGLE_SOURCEN | Kapazitätsbasierte SOH-Formel; 80% as industry end-of-life reference |
| Kernpunkte für den Kauf von gebrauchten NEVs / Charge-Test & Screening-Methoden | Yiche, Dongchedi (Auto-Medien; Methodenreferenzen) | CN | https://hao.m.yiche.com/wenzhang/107776270/ | 2026-09-03 | SINGLE_SOURCEN | Prüfungsverfahren, Aufladungsprüfung, Unfall/Flutung/Kilometerprüfung |
| 懂车帝 二手车电池检测内容 | 懂车帝（字节跳动） | CN | https://www.iesdouyin.com/share/video/7618925618490849457 | 2026-09-02 | SINGLE_SOURCEN | 20%-80% 充电验证衰减方法 |
| 懂车帝 二手电车三招排除事故/泡水/调表 | 懂车帝（视频） | CN | https://www.iesdouyin.com/share/video/7678314679869430004 | 2026-09-02 | SINGLE_SOURCEN | 事故/泡水/调表排查方法、电池包护板拆装痕迹 |
| Jingsuncar — 2026 二手新能源出口指南 | Jingsuncar（行业站） | CN | https://www.jingsuncar.com/news/2026-must-see-guide-for-buying-used-new-energy-85493284.html | 2026-09-02 | SINGLE_SOURCEN | 出口 SOH≥80% 认证门槛（EU/东盟） |

*Vertrauensbeweis: what the battery standards define (SOH measurement, cycle testing, the 80% engineering convention) is VERIFIED/CROSS_CHECKED against standards bodies. The earlier "SOH ≥80% required to clear EU/ASEAN certification" claim had no official source and has been removed: Es gibt keine universelle gesetzliche SOH-Einfuhrschwelle, und die Regel der Bestimmungsbehörde muss pro Land eingeholt werden. Videos zur Inspektionsmethode werden nur als Methodenreferenzen verwendet. *
## Editorial Review
- **Autor / Rezensent**: [AutoBridge Export Editorial Team](/Autoren/) · Methode nach unserer [Editorial Policy](/editorial-policy/]
- **Zuletzt überprüft**: 2026-09-05
- **Referenzmarkt**: Global (China Gebraucht-EV-Exportseite)
- **Verifizierungsmethode**: Standard-Body-Basis für SOH-Konzepte; Medien nur für die Inspektionsmethode verwendet; Engineering-Linie getrennt von jeder Bestimmungsgesetzgebung
- **Editorialstandard**: Recherchiert und geschrieben aus den oben aufgeführten Quellen (Desk-Recherche; kein Fahren aus erster Hand, Teardown oder Import wird beansprucht). Das Vertrauen in die Quelle wird pro Zeile angezeigt; jeder Punkt, den wir nicht unabhängig bestätigen können, wird als Verifizierungselement dargestellt und nicht als Tatsache behauptet.
#AutoBridge #UsedEVInspection #BatterySOH #ExportProcurement #PrePurchaseCheck
