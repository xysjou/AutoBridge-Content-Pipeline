# Inspeção chinesa usada pré-exportação: bateria SOH feita corretamente, além de verificação de acidentes, inundação e odômetro
## Metadados SEO
- **Título SEO**: Used Chinese  EV  Inspection: Bateria SOH, inundação e odômetro Controlos
- **Meta descrição**: Como inspecionar um chinês EV usado antes da exportação — o que SOH realmente significa sob padrões de bateria, um teste de carga medido, leitura de equilíbrio celular, triagem de acidentes/inundações e odômetro-vs-ciclo de verificação cruzada, sem limite legal inventado.
- **H1**: Inspecionando um chinês usado EV Antes da exportação: O que os números da bateria significam e o que rejeitar
- **Palavra-chave principal**: chinês usado EV bateria de inspeção SOH checklist
- **Termos de busca secundários**: EV bateria SOH padrão QC/T 743, GB/T 31484 vida útil do ciclo, usado EV desequilíbrio da tensão celular, EV inspeção de danos de inundação, contagem de ciclo da bateria de rollback odômetro
- **URL sugerida**: /guides/used-chinese-ev-inspection/
- **Intenção de busca**: Entender Inspecionar um chinês usado EV Antes da Exportação: O que os Números da Bateria significam e o que rejeitar: o que um exportador de veículos/partes deve verificar, documentar e decidir antes de se comprometer com uma ordem.
- **Sugestões de links internos**: /guides/verify-china-car-export-supplier/ ; /guides/chinese-ev-charging-standard-compatibility/ ; /guides/import-chinese-ev-to-russia-eac-ottc/
- **Sugestão de imagem**: diagnóstico-ferramenta SOH e leitura de tensão celular
- **Texto ALT**: Relatório diagnóstico independente mostrando SOH e diferença máxima de tensão celular
- **Escopo do schema**: Artigo (sem produto/oferta/preço/revisão/rating)

## Âmbito de aplicação: um manual de inspecção, não um debate utilizado em termos de novas tecnologias
A decisão de comprar **usado** é tomada como indicado; esta página abrange a **inspecção técnica antes da exportação**. A economia de um EV usado são dominadas pela bateria de alta tensão: um corpo limpo com um pacote desgastado pode valer menos do que o custo de substituição após o transporte, então a ordem de inspeção das operações é diferente de um carro ICE. Um objectivo central é ser preciso sobre o que "SOH 80%" realmente é — uma referência de engenharia, não uma linha alfandegária universal.
## Que SOH É — e o que significa realmente a figura de 80%
**State of Health (SOH)** expressa a capacidade máxima de uso atual de um pacote em relação à sua capacidade quando-nova nominal (SOH baseada em capacidade = capacidade de envelhecimento. É essencial separar uma convenção de fim de vida de ** engenharia de um limiar de importação legal**, porque eles são rotineiramente confusos:
- A figura **~ 80% ** origina-se em ** padrões de bateria e prática de garantia**, não lei de importação. A norma da China para a indústria automóvel **QC/T 743 ** trata a capacidade de cair para 80% de referência nominal como fim de vida; **GB/T ** especifica a vida-ciclo da bateria de tração * métodos de teste *; **IEC 62660 ** (partes 1/2) padroniza o desempenho/vida das células de íon de lítio; e o novo padrão nacional recomendado **GB/T 46991.1-2025 ** (desenvolvido sob MIIT/SAC) aborda a *precisão e durabilidade dos monitores de SOH/SOC a bordo*. Trata-se de documentos de normalização (verified quanto ao que eles definem). 31484
- ** Não existe um único limite legal universal de SOH para importar um EV usado.** Nenhum regulamento citado nesta pesquisa define " 80% " como uma porta de alfândegas ou de homologação que se aplica em toda a UE, ASEAN ou em qualquer outro lugar. Seja explícito sobre o que 80% é **not**: é **not um limite de importação usado-carro**, é **not uma lei unificada bateria-aposentadoria**, e não é **not um limiar de garantia de cada fabricante** (uma garantia dada pode usar um valor diferente). Um destino pode impor a sua própria regra de condição e um comprador pode definir uma linha comercial privada — mas cada um é um * instrumento diferente*. O organismo de certificação de destino padrão de aceitação do importador próprio governa, e deve ser confirmado por país em vez de assumido.
Esta distinção altera a forma como utiliza o número: trata a convenção de engenharia ~ 80% como uma referência ** comercial/engenharia para preços e rejeição**, confirmando separadamente se o destino define qualquer condição legal. Nenhuma linha NMC 85% específica para química é afirmada aqui porque nenhuma fonte padrão ou fabricante capturada para este artigo estabelece como uma regra.
## Obtendo um número de SOH defensável
- Leia o display de saúde no carro/cluster, mas não pare por aí – os displays a bordo são estimativas e o novo padrão GB/T 46991.1 é aplicável a novas produções, não necessariamente a unidades mais antigas usadas.
- Comissão um ** relatório diagnóstico independente de terceiros** que registra SOH ** e a diferença máxima de tensão célula-célula**: um grande desequilíbrio sinaliza módulos fracos mesmo quando o título SOH parece saudável.
- As marcas chinesas não partilham um protocolo OBD/diagnóstico e os formatos de relatório de terceiros não são normalizados, pelo que mantêm o relatório bruto (ferramenta, versão de software, data, temperatura ambiente) como prova. Os critérios de saúde/garantia da bateria/certificado oficiais devem ser solicitados à marca, quando disponível, em vez de ser adivinhada.
## Verificação cruzada com um teste de carga ao vivo medido (uma verificação cruzada de rastreio, não um cálculo SOH)
Um valor de SOH estático pode ser mal representado; um teste de carga exercita o pacote. Carga de aproximadamente ** 20% a 80% ** em um carregador ** medido, gravação de SOC inicial final, kWh entregue, a curva de potência e tempo decorrido, e comparar energia fornecida contra a capacidade de embalagem utilizável esperada ~ 60%. **Trate isso estritamente como uma verificação cruzada de triagem, não como uma maneira de calcular SOH.** Entrega do carregador kWh é *não* igual a energia armazenada nas células: a leitura é afetada por ** perdas de carga/conversão, sorteio térmico, temperatura ambiente e de embalagem, calibração SOC BMS, e o buffer reserva/top-bottom**. Portanto, só pode sinalizar uma anomalia ** Gross**. Uma falha nesta tela não **** por si só prova perda de capacidade genuína (e uma tela limpa não prova saúde plena); a capacidade formal figura SOH ainda requer um método de diagnóstico qualificado ou fabricante dados de teste profissional. A incapacidade de manter a taxa de carga esperada é uma razão para encomendar essa inspeção mais profunda. Execute a tela ao lado da verificação padrão de carregamento (GB/T na China vs o conector de destino – veja o guia de compatibilidade) para que um pacote de som não seja falhado por uma entrada incompatível.
## A Tríade de Alta Voltagem Além de SOH
- **Pack underside**: remover/inspeccionar o escudo inferior para remoção/marcas de reseal, raspas, deformação ou reparação não-factory.
- ** Motor e eletrônica de energia**: códigos de falha de varredura, verificar as luzes de aviso e verificar o comportamento de acionamento regen em um teste de estrada.
- ** Cabeamento de HV e conectores**: procure por corrosão, retermínio ou juntas não-facturadas.
## Rastreamento de Acidentes, Inundações e Incêndios
- Puxe ** registros de manutenção e seguro-alegação (出险) registros**; reparação estrutural chapa-metal ou qualquer marcador de reivindicação de inundação é motivo para rejeitar.
- EVs inundados escondem degradação do pacote e corrosão do arnês: inspecionam conectores de sub-dash, trilhos de assento, caixas de fusíveis e o compartimento da bateria para linhas de água/corrosão.
- Verifique as lacunas do painel, a espessura da pintura e as marcas de testemunhas de fixação; trate qualquer sinal de que a bateria foi aberta fora de uma instalação qualificada como um sinal de parada.
## Odómetro vs Ciclos de Carga
Um EV com um relógio mostra um **odômetro inconsistente com a contagem de ciclo de bateria e desgaste**. Quando os diagnósticos expõem a contagem de ciclos, compare-a com a quilometragem e desgaste físico exibidos (sede, direção, pedais). Baixa quilometragem exibida emparelhada com altas contagens de ciclos ou componentes idosos é um aviso de retrocesso que um check-in de odômetro ICE sozinho perderia.
## Papelada e a Regra do Destino
Mantenha o relatório de SOH/imbalance independente, o registro de carga medido e o histórico de serviço/afirma no dossiê de exportação. Separadamente — e esta é a correcção para qualquer pedido de "precisa de 80% para importar" — **obtenha por escrito a condição/regras de tipo V utilizada do destino** da sua autoridade de certificação ou do seu agente de autorização. As regras próprias de exportação de carros usados/idade da China são definidas pela MOFCOM e atualizadas (ver guias de venda de fornecedores e de frotas); use a posição atual em vez de uma figura mais antiga do blog.
## O que o AutoBridge adiciona para além de uma lista de verificação genérica
Listas de verificação públicas repetem "ler SOH e rejeitar abaixo de 80%." Este guia recomenda em vez disso: (1) separando a convenção de engenharia 80% da regra legal do destino, de modo que um comprador não sai de um carro compatível nem envia um não conforme a um mito; (2) emparelhando uma verificação de triagem de energia medida com uma leitura de desequilíbrio celular em vez de confiar em uma imagem do painel; e (3) mantendo a nota de inspeção ligada ao ** VIN e arquivo de exportação** usado para certificação, de modo que o carro testado é rastreável para o carro enviado.
## Regras de Rejeição Difíceis
- Marcador de inundação/fogo em registros de reclamações, ou linhas de corrosão/água no pacote ou arnês HV.
- Reparação estrutural/acidente em áreas de alta tensão, ou evidência de que o pacote foi aberto fora de uma instalação qualificada.
- Odômetro inconsistente com a contagem de ciclos e desgaste, sem explicação confiável.
- O vendedor recusa um teste de carga medido ou um relatório diagnóstico independente.
- Capacidade/iquilíbrio que falha **sua própria linha de aceitação documentada** (configurada a partir da garantia da marca + regra de destino + margem comercial) — não uma mítica porta legal universal de 80%.
## Lista de Testes de Aceitação
- Relatório independente: SOH **e max cell-voltage desequilibration, com ferramenta/versão/data registrada.
- Ensaio de carga com medição 20 → 80% (SOC, kWh, curva de potência, tempo).
- Conectores de bateria e HV inspecionados para remoção/corrosão.
- Serviço + histórico de sinistros de seguro puxado; colisão inundação marcadores de fogo verificados.
- Odômetro reconciliado com ciclos de carga e desgaste físico.
- Regra de veículo usado do destino confirmada **por escrito** e distinguida do patamar técnico de 80%.
- Compatibilidade de interface de carregamento (GB/T vs destino) verificada.
## Perguntas Mais Frequentes
**Is 80% SOH a legal import requirement?** No. Aproximadamente 80% é uma referência de engenharia/garantia em fim de vida (por exemplo, QC/T 743; Ensaiado por GB/T IEC 62660; não é um limiar de importação de carros usados, não é uma lei de aposentadoria unificada e não é uma linha de garantia de cada fabricante. Não há portão universal de 80% alfândegas, então confirme a regra do destino. 31484
** Por que as pessoas citam 80% então?** Ele vem de padrões de bateria e prática de garantia como uma referência de fim de vida comercial; é útil para preços e rejeição, mas não é lei de importação, e nenhuma regra química específica 85% é afirmada aqui.
** Posso calcular o SOH a partir do kWh do carregador entre 20% e 80% ?** Não directamente. A energia fornecida é distorcida por perdas de carga, sorteio térmico, temperatura, calibração e tampão BMS; é uma verificação cruzada de triagem que pode revelar anomalias brutas, com SOH formal deixada para um diagnóstico qualificado.
** Como deve ser evidenciado o SOH?** Um relatório independente que mostre a SOH  and  desequilíbrio entre células e tensões,  cross-checked by a metered 20–80% charge test, Mantido com ferramenta/versão/data.
** Por que danos causados por inundações são especialmente perigosos em um VE?** Pode degradar o pacote e corroer arneses/conectores escondidos, causando falhas de segurança e confiabilidade após a exportação.
**Como é que a fraude de odómetros é detectada num EV?** Compare a quilometragem exibida com a contagem de ciclo da bateria e o desgaste físico; odômetro baixo com ciclos elevados é um aviso.
## Gravação de Imagens
- IMAGE_ASSET_PATH: none secured in repository
- ORIGINAL_IMAGE_URL: not captured
- SOURCE_PAGE: not captured
- SOURCE_FILE_PAGE: not applicable — no candidate media file identified (no licence to assert)
- RIGHTS_HOLDER: unconfirmed
- LICENSE_OR_USAGE_BASIS: none secured — no third-party image may be published until rights are cleared
- CHECKED_DATE: 2026-09-06
- MODEL_TOPIC_MATCH: must match the exact model/version (or the guide topic) and reference market above
- IMAGE_SCOPE_NOTE: match the exact model family/topic only; must not imply a specific trim/model-year, real VIN, in-person inspection or actual transaction
- IMAGE_RIGHTS_STATUS: FAIL (no licensed asset captured; a placeholder or “retain old image” note is not accepted)
- BLOCK_REASON: No reusable image could be secured: Wikimedia Commons/Flickr are unreachable from the research environment, stock libraries require authenticated API/licence access, and an OEM webpage image is NOT a commercial reuse grant; no AutoBridge-owned photo exists. Kept FAIL rather than asserted.
- ALT by language:
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

## Sources & Verification
| Source title | Organization | Market | URL | Checked | Confidence | Supported facts |
|---|---|---|---|---|---|---|
| 商务部等《关于二手车出口有关事项的公告》（2024年第6号） | 中华人民共和国商务部（wms.mofcom 子站，与 www.mofcom 归一为同一母机构） | CN（出口监管） | https://wms.mofcom.gov.cn/zcfb/wmgl/art/2024/art_52f62edf8132411fa206542d851edfc7.html | 2026-09-08 | VERIFIED | 出口前第三方检测报告要求、企业条件、禁出情形 |
| 商务部等《关于支持在条件成熟地区开展二手车出口业务的通知》 | 中华人民共和国商务部 | CN | https://www.mofcom.gov.cn/zfxxgk/gkml/art/2021/art_29ef062444784bd5af9400546a1ecb75.html | 2026-09-08 | VERIFIED | 第三方检测报告制度源头、报废/抵押车辆禁出 |
| 商务部等四部门《关于进一步加强二手车出口管理工作的通知》 | 中华人民共和国商务部 | CN | http://www.mofcom.gov.cn/zcfb/dwmygl/art/2025/art_543d1fcc6a1048d5bf301a8d59ed723e.html | 2026-09-08 | VERIFIED / TIME_SENSITIVE | 质量与售后责任、售后维修服务确认书 |
| 中国政府网政策库收录（加强二手车出口管理） | 中国政府网/国务院 | CN | https://www.gov.cn/zhengce/zhengceku/202511/content_7048644.htm | 2026-09-08 | VERIFIED | 发布主体、施行时间交叉印证 |
| 中国汽车流通协会（CADA）二手车鉴定评估技术资料（引 GB/T 30323-2013） | 中国汽车流通协会 CADA | CN | https://www.cada.cn/Content/ueditor/net/upload/file/20180708/6366665897945162707573052.pdf | 2026-09-08 | CROSS_CHECKED | GB/T 30323-2013 框架、SOH 技术定义、事故/泡水/火烧判别 |
| 易车 — 二手新能源选购核心要点 | 易车 | CN | https://hao.m.yiche.com/wenzhang/107776270/ | 2026-09-02 | single source | SOH 概念、检测方法 |
| 懂车帝/抖音 二手 EV 检测视频（20%-80% 充电验证） | 字节系（懂车帝/抖音，归一为 1 个母机构） | CN | https://www.iesdouyin.com/share/video/7618925618490849457 | 2026-09-02 | single source | 充电验证衰减方法 |
| 懂车帝/抖音 二手电车事故/泡水/调表排查 | 字节系（与 SOURCE 07 同母机构） | CN | https://www.iesdouyin.com/share/video/7678314679869430004 | 2026-09-02 | single source | 事故/泡水/调表排查、电池护板 |
| 抖音 电池老化阈值经验 | 字节系（同母机构） | CN | https://www.iesdouyin.com/share/video/7674527923274474225 | 2026-09-02 | single source | 铁锂/三元老化经验阈值（非法规） |
| Jingsuncar — 2026 二手新能源出口指南 | Jingsuncar（行业站） | GLOBAL（出口） | https://www.jingsuncar.com/news/2026-must-see-guide-for-buying-used-new-energy-85493284.html | 2026-09-02 | single source | 行业经验参考线（非法定） |
| 抖音 磷酸铁锂/三元 SOH 警戒线 | 字节系（同母机构，URL 与 SOURCE 09 同族，保留方法出处） | CN | https://www.iesdouyin.com/share/video/7674527923274474225 | 2026-09-02 | single source | 经验阈值 |

*Confidence note: what the battery standards define (SOH measurement, cycle testing, the 80% engineering convention) is VERIFIED/CROSS_CHECKED against standards bodies. The earlier "SOH ≥80% required to clear EU/ASEAN certification" claim had no official source and has been removed: no universal legal SOH import threshold exists, and the destination authority's rule must be obtained per country. Inspection-method videos are used only as method references.*
## Revisão Editorial
- **Autor revisor**: [AutoBridge Export Editorial Team](/autores/) · método para o nosso [Política editorial](/editorial-policy/)
- ** Última revisão**: 2026-09-05
- **Mercado de referência**: Global (China usado-EV lado de exportação)
- ** Método de verificação**: Normas-base do corpo para conceitos SOH; meios utilizados apenas para método de inspeção; linha de engenharia mantida distinta de qualquer regra legal de destino
- ** Norma editorial**: Pesquisado e escrito a partir das fontes listadas acima (pesquisa de mesa; nenhuma condução em primeira mão, demolição ou importação é reivindicada). A confiança na fonte é mostrada por linha; qualquer ponto que não podemos confirmar independentemente é apresentado como um item de verificação em vez de afirmado como fato.
#AutoBridge #UsedEVInspection #BatterySOH #ExportProcurement #PrePurchaseCheck
