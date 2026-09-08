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
- Regra do destino utilizado-V confirmado ** por escrito**  and  distinguished from the engineering 80% line.
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

## Fontes e Verificação
| Título do código fonte | Organização | Mercado | URL | Verificado | Confiança | Factos corroborados |
|---|---|---|---|---|---|---|
| GB/T traction-battery cycle-life requirements/test methods | Padrão nacional chinês (** organismo de normas**) | NC | https://www.chinesestandard.net/PDF.aspx/GBT31484-2015 | 2026-09-03 | ** VERIFIFICADO** | Quadro de ensaio de capacidade/vida útil do ciclo; requisitos de capacidade inicial | 31484
| IEC 62660-1/2 – Ensaios de desempenho/vida celular de iões de lítio | IEC (organismo internacional ** normas**) | Global | https://www.iec.ch/ (série IEC 62660) | 2026-09-03 | ** VERIFIFICADO** | Base de ensaio de desempenho/vida normalizada para a SOH |
| GB/T 46991.1-2025 a bordo SOH/SOC display de precisão e durabilidade (MIIT/SAC) | Padrão nacional recomendado chinês (** corpo padrão**) | NC | reportado através de cobertura de normas; primário em canais SAC/MIIT | 2026-09-03 | CROSS_CHECKED | A precisão do dispositivo de saúde a bordo é normalizada separadamente (não uma linha de importação legal) |
| Formulações SOH e a convenção de fim de vida QC/T 743 80% | LNC Explicador técnico das baterias (indústria) | Global | https://lnclibattery.com/blog/evaluation-of-the-health-status-soh-of-lithium-ion-batteries/ | 2026-09-03 | FONTE ÚNICA | Fórmula SOH baseada na capacidade; 80% como referência no fim da vida útil da indústria |
| Pontos principais para comprar NEVs usados métodos de teste de carga e triagem | Yiche, Dongchedi (referências de métodos de mídia automática) | NC | https://hao.m.yiche.com/wenzhang/107776270/ | 2026-09-03 | FONTE ÚNICA | Método de inspecção, ensaio de carga, prática de acidente/inundação/odómetro |
| 懂车帝 二手车电池检测内容 | 懂车帝 (字节跳动) | NC | https://www.iesdouyin.com/share/video/7618925618490849457 | 2026-09-02 | FONTE ÚNICA | 20% - 80% 充电验证衰减方法 |
| 懂车帝 二手电车三招排除事故 泡水 调表 | 懂车帝 (视频) | NC | https://www.iesdouyin.com/share/video/7678314679869430004 | 2026-09-02 | FONTE ÚNICA | 事故/泡水/调表排查方法、电池包护板拆装痕迹 |
| Jingsuncar — 2026 二手新能源出口指南 | Jingsuncar(行业站) | NC | https://www.jingsuncar.com/news/2026-must-see-guide-for-buying-used-new-energy-85493284.html | 2026-09-02 | FONTE ÚNICA | 出口 SOH. 80% 认证门槛 (EU/ 东盟) |

* Nota de confiança: o que os padrões de bateria definem (medição SOH, teste de ciclo, a convenção de engenharia 80%) é VERIFIED/CROSS_CHECKED contra corpos de normas. A alegação anterior de "SOH ≥ 80% necessária para a certificação UE/ASEAN" não tinha fonte oficial e foi removida: não existe um limiar legal universal de importação SOH, e a regra da autoridade de destino deve ser obtida por país. Os vídeos de métodos de inspeção são usados apenas como referências de método. *
## Revisão Editorial
- **Autor revisor**: [AutoBridge Export Editorial Team](/autores/) · método para o nosso [Política editorial](/editorial-policy/)
- ** Última revisão**: 2026-09-05
- **Mercado de referência**: Global (China usado-EV lado de exportação)
- ** Método de verificação**: Normas-base do corpo para conceitos SOH; meios utilizados apenas para método de inspeção; linha de engenharia mantida distinta de qualquer regra legal de destino
- ** Norma editorial**: Pesquisado e escrito a partir das fontes listadas acima (pesquisa de mesa; nenhuma condução em primeira mão, demolição ou importação é reivindicada). A confiança na fonte é mostrada por linha; qualquer ponto que não podemos confirmar independentemente é apresentado como um item de verificação em vez de afirmado como fato.
#AutoBridge #UsedEVInspection #BatterySOH #ExportProcurement #PrePurchaseCheck
