# Inspeção chinesa usada pré-exportação: bateria SOH feita corretamente, além de verificação de acidentes, inundação e odômetro
## SEO Meta- dados
- ** Título SEO**: Inspeção EV chinesa usada: bateria SOH, inundação e odômetro Controlos
- ** Descrição do Meta**: Como inspecionar um EV chinês usado antes da exportação — o que SOH realmente significa sob padrões de bateria, um teste de carga medido, leitura de equilíbrio celular, triagem de acidentes/inundações e odômetro-vs-ciclo de verificação cruzada, sem limite legal inventado.
- ** URL sugerido**: /guides/used-chinese-ev-inspection/
- ** H1 **: Inspecionando um EV chinês usado antes da exportação: O que os números da bateria significam e o que rejeitar
- **Primary Keyword**: bateria de inspeção de EV usado chinês SOH checklist
- ** Termos de pesquisa secundários**: bateria EV padrão SOH QC/T 743, GB/T vida do ciclo 31484, desequilíbrio de tensão da célula EV usado, inspeção de danos de inundação EV, contagem de ciclo de bateria de rollback do odômetro
- ** Sugestões de ligação interna**: /guias/verify-china-car-export-supplier/; /guias/chinese-ev-charging-standard-compatibility/; /guias/importação-chinese-ev-to-russia-eac-ottc/
- ** Sugestões de imagens**: leitura de SOH e de tensão celular; metered 20–80% charge worksheet; Pontos de inspecção de subtrações de pilhas; Serviço/pedidos de registo de amostra
- ** Sugestões ALT**: "Relatório diagnóstico independente mostrando a diferença de SOH e máxima tensão celular"; "placa de teste de energia de carga medida"; "pontos de inspeção de undertray da bateria EV"
## Âmbito de aplicação: um manual de inspecção, não um debate utilizado em termos de novas tecnologias
A decisão de comprar **usado** é tomada como indicado; Esta página abrange a inspecção técnica ** antes da exportação **. A economia de um EV usado é dominada pela bateria de alta tensão: um corpo limpo com um pacote desgastado pode valer menos do que o custo de substituição após o transporte, por isso a ordem de inspeção das operações é diferente de um carro ICE. A central aim is to be precise about what "SOH 80%" actually is — an engineering reference, not a universal customs line.
## What SOH Is — and What the 80% Figure Actually Means
**State of Health (SOH)** expressa a capacidade máxima de uso atual de um pacote em relação à sua capacidade quando-nova nominal (SOH baseada em capacidade = capacidade de envelhecimento. É essencial separar uma convenção de fim de vida de ** engenharia de um limiar de importação legal**, porque eles são rotineiramente confusos:
- The **~80%** figure originates in **battery standards and warranty practice**, not import law. China's automotive-industry standard **QC/T 743** treats capacity falling to 80% of nominal as an end-of-life reference; **GB/T 31484 ** especifica a vida-ciclo da bateria de tração * métodos de teste *; **IEC 62660 ** (partes 1/2) padroniza o desempenho/vida das células de iões de lítio; e a nova norma nacional recomendada **GB/T 46991.1-2025 ** (desenvolvido sob MIIT/SAC) aborda a *precisão e durabilidade dos monitores SOH/SOC a bordo*. Trata-se de documentos de normalização (verified quanto ao que definem).
- **There is no single universal legal SOH threshold for importing a used EV.** No regulation cited in this research sets "80%" as a blanket customs or type-approval gate that applies across the EU, ASEAN or anywhere else. Be explicit about what 80% is **not**: é **não é um limiar de importação de carros usados**, é **não uma lei unificada de aposentadoria de bateria**, e é **não é o limiar de garantia de cada fabricante** (uma garantia dada pode usar um valor diferente). Um destino pode impor a sua própria regra de condição e um comprador pode definir uma linha comercial privada — mas cada um é um * instrumento diferente*. O organismo de certificação de destino / padrão de aceitação do importador próprio governa, e deve ser confirmado por país em vez de assumido.
Esta distinção altera a forma como você usa o número: treat the ~80% engineering convention purely as a **commercial/engineering reference for pricing and rejection**, while separately confirming whether the destination sets any legal condition. No chemistry-specific "85% NMC line" is asserted here because no standard or manufacturer source captured for this article establishes it as a rule.
## Obtendo um número de SOH defensável
- Leia o display de saúde no carro/cluster, mas não pare por aí – os displays a bordo são estimativas e o novo padrão de exibição-precisão GB/T 46991.1 aplica-se a nova produção, não necessariamente a unidades mais antigas usadas.
- Comissão um ** relatório diagnóstico independente de terceiros** que registra SOH ** e a diferença máxima de tensão célula-célula**: um grande desequilíbrio sinaliza módulos fracos mesmo quando o título SOH parece saudável.
- As marcas chinesas não partilham um protocolo OBD/diagnóstico e os formatos de relatório de terceiros não são normalizados, pelo que mantêm o relatório bruto (ferramenta, versão de software, data, temperatura ambiente) como prova. Os critérios de saúde/garantia da bateria/certificado oficiais devem ser solicitados à marca, quando disponível, em vez de ser adivinhada.
## Verificação cruzada com um teste de carga ao vivo medido (uma verificação cruzada de rastreio, não um cálculo SOH)
Um valor de SOH estático pode ser mal representado; um teste de carga exercita a embalagem. Charge from roughly **20% to 80%** on a **metered** charger, recording start/end SOC, kWh delivered, the power curve and elapsed time, and compare delivered energy against the expected ~60% of usable pack capacity. **Trate isso estritamente como uma verificação cruzada de triagem, não como uma maneira de calcular SOH.** Entrega do carregador kWh é *não * igual à energia armazenada nas células: a leitura é afetada por ** perdas de carga/conversão, sorteio térmico, temperatura ambiente e de embalagem, calibração do SOC BMS, e o buffer reserva/top-bottom**. Portanto, só pode sinalizar uma anomalia ** Gross**. Uma falha nesta tela não ** por si só prova perda de capacidade genuína (e uma tela limpa não prova saúde total); A figura de capacidade formal/SOH ainda requer um método de diagnóstico qualificado ou dados de teste fabricante/profissional. A incapacidade de manter a taxa de carga esperada é uma razão para encomendar essa inspeção mais profunda. Execute a tela ao lado da verificação padrão de carregamento (GB/T na China vs o conector de destino – veja o guia de compatibilidade) para que um pacote de som não seja falhado por uma entrada incompatível.
## A Tríade de Alta Voltagem Além de SOH
- **Pack underside**: remover/inspeccionar o escudo inferior para remoção/marcas de reseal, raspas, deformação ou reparação não-factory.
- ** Motor e eletrônica de energia**: códigos de falha de varredura, verificar as luzes de aviso e verificar o comportamento de acionamento / regen em um teste de estrada.
- ** Cabeamento de HV e conectores**: procure por corrosão, retermínio ou juntas não-facturadas.
## Rastreamento de Acidentes, Inundações e Incêndios
- Pull **maintenance records and insurance-claim (出险) records**; A reparação estrutural de chapas metálicas ou qualquer marcador de pedido de água de inundação é motivo para rejeitar.
- EVs inundados escondem degradação do pacote e corrosão do arnês: inspecionam conectores de sub-dash, trilhos de assento, caixas de fusíveis e o compartimento da bateria para linhas de água/corrosão.
- Verifique as lacunas do painel, a espessura da pintura e as marcas de testemunhas de fixação; trate qualquer sinal de que a bateria foi aberta fora de uma instalação qualificada como um sinal de parada.
## Odómetro vs Ciclos de Carga
Um EV com um relógio mostra um **odômetro inconsistente com a contagem de ciclo de bateria e desgaste**. Quando os diagnósticos expõem a contagem de ciclos, compare-a com a quilometragem e desgaste físico exibidos (sede, direção, pedais). Baixa quilometragem exibida emparelhada com altas contagens de ciclos ou componentes idosos é um aviso de retrocesso que um check-in de odômetro ICE sozinho perderia.
## Papelada e a Regra do Destino
Mantenha o relatório de SOH/imbalance independente, o registro de carga medido e o histórico de serviço/afirma no dossiê de exportação. Separately — and this is the correction to any blanket "you need 80% to import" claim — **obtain the destination's actual used-EV condition/type rule in writing** from its certification authority or your clearance agent. As regras próprias da China relativas à qualificação/idade de exportação de automóveis usados são estabelecidas pela MOFCOM e atualizadas (ver guias de venda de veículos de transporte e de aquisição de frotas); usar a posição do ano atual em vez de uma figura mais antiga do blog.
## O que o AutoBridge adiciona para além de uma lista de verificação genérica
Public checklists repeat "read SOH and reject below 80%." This guide instead recommends: (1) separating the engineering 80% convention from the destination's actual legal rule, so a buyer neither walks away from a compliant car nor ships a non-compliant one on a myth; (2) emparelhando uma verificação cruzada de triagem de energia medida com uma leitura de desequilíbrio celular em vez de confiar em uma captura de tela do painel; e (3) mantendo a nota de inspeção ligada ao **VIN e arquivo de exportação** usado para certificação, por isso o carro testado é rastreável para o carro enviado.
## Regras de Rejeição Difíceis
- Marcador de inundação/fogo em registros de reclamações, ou linhas de corrosão/água no pacote ou arnês HV.
- Reparação estrutural/acidente em áreas de alta tensão, ou evidência de que o pacote foi aberto fora de uma instalação qualificada.
- Odômetro inconsistente com a contagem de ciclos e desgaste, sem explicação confiável.
- O vendedor recusa um teste de carga medido ou um relatório diagnóstico independente.
- Capacity/imbalance that fails **your own documented acceptance line** (set from brand warranty + destination rule + commercial margin) — not a mythical universal 80% legal gate.
## Lista de Testes de Aceitação
- Relatório independente: SOH **e max cell-voltage desequilibration, com ferramenta/versão/data registrada.
- Metered 20→80% charge test (SOC, kWh, power curve, time).
- Conectores de bateria e HV inspecionados para remoção/corrosão.
- Serviço + histórico de sinistros de seguro puxado; colisão / inundação / marcadores de fogo verificados.
- Odômetro reconciliado com ciclos de carga e desgaste físico.
- Destination used-EV rule confirmed **in writing** and distinguished from the engineering 80% line.
- Compatibilidade de interface de carregamento (GB/T vs destino) verificada.
## Perguntas Mais Frequentes
**Is 80% SOH a legal import requirement?** No. Roughly 80% is an engineering/warranty end-of-life reference (e.g., QC/T 743; ensaio por GB/T 31484 / IEC 62660; não é um limiar de importação de carros usados, não é uma lei de aposentadoria unificada e não é uma linha de garantia de cada fabricante. There is no universal 80% customs gate, so confirm the destination's own rule.
**Why do people quote 80% then?** It comes from battery standards and warranty practice as an end-of-life/commercial reference; it is useful for pricing and rejection, but it is not import law, and no chemistry-specific 85% rule is asserted here.
**Can I calculate SOH from the charger's kWh between 20% and 80%?** Not directly. A energia fornecida é distorcida por perdas de carga, sorteio térmico, temperatura, calibração e tampão BMS; é uma verificação cruzada de rastreio que pode revelar anomalias grosseiras, com a SOH formal deixada para um diagnóstico qualificado.
**How should SOH be evidenced?** An independent report showing SOH and cell-voltage imbalance, cross-checked by a metered 20–80% charge test, kept with tool/version/date.
** Por que danos causados por inundações são especialmente perigosos em um VE?** Pode degradar o pacote e corroer arneses/conectores escondidos, causando falhas de segurança e confiabilidade após a exportação.
**Como é que a fraude de odómetros é detectada num EV?** Compare a quilometragem exibida com a contagem de ciclo da bateria e o desgaste físico; odômetro baixo com ciclos elevados é um aviso.
## Gravação de Imagens
- IMAGEM_ASSET_PATH: nenhum protegido no repositório
- ORIGINAL_ IMAGE_ URL: não capturado
- ORIGINAL_PAGE: não capturado
- DIREITOS_OLDER: não confirmado
- LICENSE_OR_USAGE_BASIS: nenhuma imagem segura — nenhuma imagem de terceiros pode ser publicada até que os direitos sejam compensados
- Data_ Marcada: 2026-09-05
- MODEL_TOPIC_ MATCH: deve corresponder ao modelo/versão exato (ou ao tópico guia) e ao mercado de referência acima
- IMAGEM_RIGHTS_STATUS: FALHA (não é aceita nenhuma propriedade licenciada capturada; uma nota de placeholder ou “reter imagem antiga”)
- ALT por língua:
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

## Fontes e Verificação
| Título do código fonte | Organização | Mercado | URL | Verificado | Confiança | Factos corroborados |
|---|---|---|---|---|---|---|
| GB/T 31484 requisitos de vida útil do ciclo de baterias de tração/métodos de ensaio | Padrão nacional chinês (** organismo de normas**) | NC | https://www.chinesestandard.net/PDF.aspx/GBT31484-2015 | 2026-09-03 | ** VERIFIFICADO** | Quadro de ensaio de capacidade/vida útil do ciclo; requisitos de capacidade inicial |
| Ensaios de desempenho/vida celular de iões de lítio IEC 62660-1/2 | IEC (organismo internacional ** normas**) | Global | https://www.iec.ch/ (IEC 62660 series) | 2026-09-03 | ** VERIFIFICADO** | Base de ensaio de desempenho/vida normalizada para a SOH |
| GB/T 46991.1-2025 a bordo SOH/SOC exibem precisão e durabilidade (MIIT/SAC) | Padrão nacional recomendado chinês (** corpo padrão**) | NC | reportado através de cobertura de normas; primário em canais SAC/MIIT | 2026-09-03 | CROSS_CHECKED | A precisão do dispositivo de saúde a bordo é normalizada separadamente (não uma linha de importação legal) |
| SOH formulations and the QC/T 743 80% end-of-life convention | LNC Explicador técnico das baterias (indústria) | Global | https://lnclibattery.com/blog/evaluation-of-the-health-status-soh-of-lithium-ion-batteries/ | 2026-09-03 | FONTE ÚNICA | Fórmula SOH baseada na capacidade; 80% as industry end-of-life reference |
| Pontos principais para comprar NEVs usados / métodos de teste de carga e triagem | Yiche, Dongchedi (referências de métodos de mídia automática) | NC | https://hao.m.yiche.com/wenzhang/107776270/ | 2026-09-03 | FONTE ÚNICA | Método de inspecção, ensaio de carga, prática de acidente/inundação/odómetro |
| 懂车帝 二手车电池检测内容 | 懂车帝（字节跳动） | NC | https://www.iesdouyin.com/share/video/7618925618490849457 | 2026-09-02 | FONTE ÚNICA | 20%-80% 充电验证衰减方法 |
| 懂车帝 二手电车三招排除事故/泡水/调表 | 懂车帝（视频） | NC | https://www.iesdouyin.com/share/video/7678314679869430004 | 2026-09-02 | FONTE ÚNICA | 事故/泡水/调表排查方法、电池包护板拆装痕迹 |
| Jingsuncar — 2026 二手新能源出口指南 | Jingsuncar（行业站） | NC | https://www.jingsuncar.com/news/2026-must-see-guide-for-buying-used-new-energy-85493284.html | 2026-09-02 | FONTE ÚNICA | 出口 SOH≥80% 认证门槛（EU/东盟） |

* Nota de confiança: what the battery standards define (SOH measurement, cycle testing, the 80% engineering convention) is VERIFIED/CROSS_CHECKED against standards bodies. The earlier "SOH ≥80% required to clear EU/ASEAN certification" claim had no official source and has been removed: Não existe um limiar legal universal de importação de SOH, e a regra da autoridade de destino deve ser obtida por país. Os vídeos de métodos de inspeção são usados apenas como referências de método. *
## Revisão Editorial
- **Autor / revisor**: [AutoBridge Export Editorial Team](/autores/) · método para o nosso [Política editorial](/editorial-policy/)
- ** Última revisão**: 2026-09-05
- **Mercado de referência**: Global (China usado-EV lado de exportação)
- ** Método de verificação**: Normas-base do corpo para conceitos SOH; meios utilizados apenas para método de inspeção; linha de engenharia mantida distinta de qualquer regra legal de destino
- ** Norma editorial**: Pesquisado e escrito a partir das fontes listadas acima (pesquisa de mesa; nenhuma condução em primeira mão, demolição ou importação é reivindicada). A confiança na fonte é mostrada por linha; qualquer ponto que não podemos confirmar independentemente é apresentado como um item de verificação em vez de afirmado como fato.
#AutoBridge #UsedEVInspection #BatterySOH #ExportProcurement #PrePurchaseCheck
