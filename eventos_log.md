# Eventos do log da urna

Amostra: 50 primeiros logs de bu_imgbu_logjez_rdv_vscmr_2026_2t_AC.zip, ordem de nome. 668 moldes, 444905 eventos.
O molde troca cada sequência de dígitos por N. O exemplo é o texto de uma linha real.
Detector só entra no código se a frase exata estiver nesta lista.

## Frases usadas

Presentes na amostra, texto exato:

- `O voto do eleitor foi computado`
- `Data e hora atualizada` — não traz o novo horário nem o deslocamento. Na amostra cai na carga da mídia, dias antes da eleição. Conta só no dia do turno; não desloca a janela.
- `Reiniciando a urna`
- `Início do procedimento de contingência`
- `Modo de carga da UE - Urna de contingência`

Ausente na amostra: votação por cédula, horário estendido e substituição de urna consumada. A frase que manda substituir a urna é um erro de captura de digital, não o registro da troca. Esses três testes não rodam.

| Contagem | Molde | Exemplo |
|---:|---|---|
| 37262 | Tecla indevida pressionada | Tecla indevida pressionada |
| 29363 | Solicita digital. Tentativa [N] de [N] | Solicita digital. Tentativa [1] de [4] |
| 29013 | Capturada a digital. Tentativa [N] de [N] | Capturada a digital. Tentativa [1] de [4] |
| 23402 | Aguardando digitação do identificador do eleitor | Aguardando digitação do identificador do eleitor |
| 22382 | Identificador do eleitor digitado pelo mesário | Identificador do eleitor digitado pelo mesário |
| 21119 | Voto confirmado para [Senador] | Voto confirmado para [Senador] |
| 20222 | Eleitor foi habilitado | Eleitor foi habilitado |
| 20217 | O voto do eleitor foi computado | O voto do eleitor foi computado |
| 20211 | Voto confirmado para [Governador] | Voto confirmado para [Governador] |
| 20211 | Voto confirmado para [Presidente] | Voto confirmado para [Presidente] |
| 19422 | Foto do eleitor apresentada | Foto do eleitor apresentada |
| 18431 | Tipo de habilitação do eleitor [biométrica] | Tipo de habilitação do eleitor [biométrica] |
| 17359 | Identificador digitado pelo mesário foi: (Título de eleitor) | Identificador digitado pelo mesário foi: (Título de eleitor) |
| 10582 | Número de tentativas de reconhecimento do dedo. Tentativa [N] de [N] | Número de tentativas de reconhecimento do dedo. Tentativa [1] de [4] |
| 10562 | Voto confirmado para [Deputado Federal] | Voto confirmado para [Deputado Federal] |
| 10560 | Voto confirmado para [Deputado Estadual] | Voto confirmado para [Deputado Estadual] |
| 3985 | Identificador digitado pelo mesário foi: (CPF) | Identificador digitado pelo mesário foi: (CPF) |
| 3726 | Batimento de digitais retornou o score N | Batimento de digitais retornou o score 5 |
| 2461 | Espaço livre na MI [N.N GB] | Espaço livre na MI [3.4 GB] |
| 2461 | Espaço livre na MV [N.N MB] | Espaço livre na MV [376.9 MB] |
| 2461 | Quantidade de memória livre [N.N GB] | Quantidade de memória livre [3.2 GB] |
| 2461 | Quantidade de memória total [N.N GB] | Quantidade de memória total [3.7 GB] |
| 2461 | Quantidade de memória usada [N.N MB] | Quantidade de memória usada [476.8 MB] |
| 2334 | Urna ligada conectada na rede CA em [N.NV] e na Bateria Interna com [N.NV/NA] | Urna ligada conectada na rede CA em [130.17V] e na Bateria Interna com [13.44V/0A] |
| 2261 | Tecla pressionada: N | Tecla pressionada: 8 |
| 2214 | Espaço utilizado na MI [N.N MB] | Espaço utilizado na MI [1.0 MB] |
| 2206 | Espaço utilizado na MV [N.N MB] | Espaço utilizado na MV [1.2 MB] |
| 2044 | Verificação de assinatura - Etapa [N] - [/uenux/bin/avpartN.vst] - [SUCESSO] | Verificação de assinatura - Etapa [12] - [/uenux/bin/avpart91.vst] - [SUCESSO] |
| 1965 | Biometria coletada não é do mesário N (N) | Biometria coletada não é do mesário 006908122488 (854012) |
| 1215 | Identificação do Modelo de Urna: UEN | Identificação do Modelo de Urna: UE2022 |
| 1207 | Eleitor corrigiu na tela de confirmação de candidato | Eleitor corrigiu na tela de confirmação de candidato |
| 1127 | Solicita digital do mesário | Solicita digital do mesário |
| 1126 | Solicitação de dado pessoal do eleitor para habilitação manual | Solicitação de dado pessoal do eleitor para habilitação manual |
| 1123 | Início de impressão | Início de impressão |
| 1121 | Fim de impressão | Fim de impressão |
| 1087 | Iniciando aplicação - Nº turno | Iniciando aplicação - 1º turno |
| 1087 | Versão da aplicação: N.N.N.N - Praia da Barra do Cahy | Versão da aplicação: 10.23.0.0 - Praia da Barra do Cahy |
| 1072 | Dado digitado confere | Dado digitado confere |
| 1022 | Verificação de assinatura - Etapa [N] - [/dsk/fi/estatico/oNac-ce.vsc] - [SUCESSO] | Verificação de assinatura - Etapa [32] - [/dsk/fi/estatico/o06257ac-ce.vsc] - [SUCESSO] |
| 1022 | Verificação de assinatura - Etapa [N] - [/dsk/fi/estatico/oNac-ste.vsc] - [SUCESSO] | Verificação de assinatura - Etapa [30] - [/dsk/fi/estatico/o03220ac-ste.vsc] - [SUCESSO] |
| 1022 | Verificação de assinatura - Etapa [N] - [/uenux/bin/avusrbin.vst] - [SUCESSO] | Verificação de assinatura - Etapa [1] - [/uenux/bin/avusrbin.vst] - [SUCESSO] |
| 1002 | Finalização de aplicativo | Finalização de aplicativo |
| 991 | Identificador do eleitor digitado inválido | Identificador do eleitor digitado inválido |
| 844 | Operador confirmou o registro de mesários | Operador confirmou o registro de mesários |
| 825 | Eleitor sem atividade por N segundos | Eleitor sem atividade por 45 segundos |
| 761 | Turno da UE: Nº turno | Turno da UE: 1º turno |
| 740 | Ano de nascimento digitado é igual ao do cadastro | Ano de nascimento digitado é igual ao do cadastro |
| 723 | Pedido de leitura da biometria do mesário N | Pedido de leitura da biometria do mesário 004758852445 |
| 711 | Eleitor voltou a digitar enquanto estava sendo suspenso | Eleitor voltou a digitar enquanto estava sendo suspenso |
| 689 | Mesário N registrado | Mesário 004758852445 registrado |
| 688 | Operador indagado se continua registrando mesários | Operador indagado se continua registrando mesários |
| 669 | Inspeção da urna confirmada | Inspeção da urna confirmada |
| 669 | Inspeção da urna iniciada | Inspeção da urna iniciada |
| 669 | Inspeção da urna terminada | Inspeção da urna terminada |
| 622 | Tamanho da MR: N.N MB | Tamanho da MR: 954.0 MB |
| 583 | Município: N | Município: 01007 |
| 583 | Seção Eleitoral: N | Seção Eleitoral: 0001 |
| 583 | Zona Eleitoral: N | Zona Eleitoral: 0009 |
| 567 | Detectada impressora com serial N | Detectada impressora com serial 30702804 |
| 563 | Data e hora da geração da mídia de votação: N/N/N N:N:N | Data e hora da geração da mídia de votação: 19/09/2026 08:35:15 |
| 563 | Lendo o serial da MV presente na urna | Lendo o serial da MV presente na urna |
| 563 | Mídia de votação gerada pelo usuário: N | Mídia de votação gerada pelo usuário: 009847462348 |
| 556 | Bateria interna com carga plena | Bateria interna com carga plena |
| 549 | Mesário N habilitou o eleitor | Mesário 004758852445 habilitou o eleitor |
| 538 | Urna operando com rede elétrica | Urna operando com rede elétrica |
| 529 | Fase da UE: Oficial | Fase da UE: Oficial |
| 529 | Tamanho da partição dinâmica de dados da MI: N.N GB | Tamanho da partição dinâmica de dados da MI: 3.4 GB |
| 517 | Resultado da verificação da mídia externa dinâmica : N | Resultado da verificação da mídia externa dinâmica : 0 |
| 517 | Resultado da verificação da mídia externa estática : N | Resultado da verificação da mídia externa estática : 0 |
| 515 | Modo de carga da UE - Votação | Modo de carga da UE - Votação |
| 514 | Estrutura de diretórios da ME: OK | Estrutura de diretórios da ME: OK |
| 513 | Impressora OK | Impressora OK |
| 511 | Verificação de assinatura - Etapa [N] - [/bin/avbin.vst] - [SUCESSO] | Verificação de assinatura - Etapa [5] - [/bin/avbin.vst] - [SUCESSO] |
| 511 | Verificação de assinatura - Etapa [N] - [/boot/boot/avboot.vst] - [SUCESSO] | Verificação de assinatura - Etapa [3] - [/boot/boot/avboot.vst] - [SUCESSO] |
| 511 | Verificação de assinatura - Etapa [N] - [/boot/boot/avbootcfg.vsu] - [SUCESSO] | Verificação de assinatura - Etapa [4] - [/boot/boot/avbootcfg.vsu] - [SUCESSO] |
| 511 | Verificação de assinatura - Etapa [N] - [/dsk/fi/estatico/N-lo.vsc] - [SUCESSO] | Verificação de assinatura - Etapa [25] - [/dsk/fi/estatico/0100700090001-lo.vsc] - [SUCESSO] |
| 511 | Verificação de assinatura - Etapa [N] - [/dsk/fi/estatico/chave/avusrchave.vst] - [SUCESSO] | Verificação de assinatura - Etapa [24] - [/dsk/fi/estatico/chave/avusrchave.vst] - [SUCESSO] |
| 511 | Verificação de assinatura - Etapa [N] - [/dsk/fi/estatico/dadoscarga.vsu] - [SUCESSO] | Verificação de assinatura - Etapa [27] - [/dsk/fi/estatico/dadoscarga.vsu] - [SUCESSO] |
| 511 | Verificação de assinatura - Etapa [N] - [/dsk/fi/estatico/oN-cp.vsc] - [SUCESSO] | Verificação de assinatura - Etapa [28] - [/dsk/fi/estatico/o01219-cp.vsc] - [SUCESSO] |
| 511 | Verificação de assinatura - Etapa [N] - [/dsk/fi/estatico/oNbr-pu.vsc] - [SUCESSO] | Verificação de assinatura - Etapa [29] - [/dsk/fi/estatico/o00000br-pu.vsc] - [SUCESSO] |
| 511 | Verificação de assinatura - Etapa [N] - [/etc/RHVoice/avrhvoice.vst] - [SUCESSO] | Verificação de assinatura - Etapa [7] - [/etc/RHVoice/avrhvoice.vst] - [SUCESSO] |
| 511 | Verificação de assinatura - Etapa [N] - [/etc/avetc.vst] - [SUCESSO] | Verificação de assinatura - Etapa [6] - [/etc/avetc.vst] - [SUCESSO] |
| 511 | Verificação de assinatura - Etapa [N] - [/lib/avlib.vst] - [SUCESSO] | Verificação de assinatura - Etapa [18] - [/lib/avlib.vst] - [SUCESSO] |
| 511 | Verificação de assinatura - Etapa [N] - [/lib/modules/avmod.vst] - [SUCESSO] | Verificação de assinatura - Etapa [16] - [/lib/modules/avmod.vst] - [SUCESSO] |
| 511 | Verificação de assinatura - Etapa [N] - [/lib/modules/ueN/avmodue.vst] - [SUCESSO] | Verificação de assinatura - Etapa [17] - [/lib/modules/ue2022/avmodue.vst] - [SUCESSO] |
| 511 | Verificação de assinatura - Etapa [N] - [/lib/plugins/generic/avlibqtgeneric.vst] - [SUCESSO] | Verificação de assinatura - Etapa [19] - [/lib/plugins/generic/avlibqtgeneric.vst] - [SUCESSO] |
| 511 | Verificação de assinatura - Etapa [N] - [/lib/plugins/imageformats/avlibqtimageformats.vst] - [SUCESSO] | Verificação de assinatura - Etapa [20] - [/lib/plugins/imageformats/avlibqtimageformats.vst] - [SUCESSO] |
| 511 | Verificação de assinatura - Etapa [N] - [/lib/plugins/platforms/avlibqtplatforms.vst] - [SUCESSO] | Verificação de assinatura - Etapa [21] - [/lib/plugins/platforms/avlibqtplatforms.vst] - [SUCESSO] |
| 511 | Verificação de assinatura - Etapa [N] - [/share/RHVoice/languages/Brazilian-Portuguese/avsharerhvoicelang.vst] - [SUCESSO] | Verificação de assinatura - Etapa [8] - [/share/RHVoice/languages/Brazilian-Portuguese/avsharerhvoicelang.vst] - [SUCESSO] |
| 511 | Verificação de assinatura - Etapa [N] - [/share/RHVoice/languages/Brazilian-Portuguese/userdict/src/avsharerhvoicelangdict.vst] - [SUCESSO] | Verificação de assinatura - Etapa [9] - [/share/RHVoice/languages/Brazilian-Portuguese/userdict/src/avsharerhvoicelangdict.vst] - [SUCESSO] |
| 511 | Verificação de assinatura - Etapa [N] - [/share/RHVoice/voices/Leticia-FN/N/avsharerhvoiceNkhz.vst] - [SUCESSO] | Verificação de assinatura - Etapa [11] - [/share/RHVoice/voices/Leticia-F123/16000/avsharerhvoice24khz.vst] - [SUCESSO] |
| 511 | Verificação de assinatura - Etapa [N] - [/share/RHVoice/voices/Leticia-FN/avsharerhvoiceleticia.vst] - [SUCESSO] | Verificação de assinatura - Etapa [10] - [/share/RHVoice/voices/Leticia-F123/avsharerhvoiceleticia.vst] - [SUCESSO] |
| 511 | Verificação de assinatura - Etapa [N] - [/uenux/lib/avusrlib.vst] - [SUCESSO] | Verificação de assinatura - Etapa [22] - [/uenux/lib/avusrlib.vst] - [SUCESSO] |
| 511 | Verificação de assinatura - Etapa [N] - [/uenux/lib/avusrlibue.vst] - [SUCESSO] | Verificação de assinatura - Etapa [23] - [/uenux/lib/avusrlibue.vst] - [SUCESSO] |
| 509 | Mídia externa presente | Mídia externa presente |
| 509 | Tamanho da partição dinâmica de dados da MV: N.N MB | Tamanho da partição dinâmica de dados da MV: 377.3 MB |
| 509 | Tamanho da partição estática de dados da MV: N.N MB | Tamanho da partição estática de dados da MV: 97.9 MB |
| 509 | Verificação de assinatura - Etapa [N] - [/dsk/fe/estatico/infomidia.vsc] - [SUCESSO] | Verificação de assinatura - Etapa [26] - [/dsk/fe/estatico/infomidia.vsc] - [SUCESSO] |
| 487 | Início das operações do logd | Início das operações do logd |
| 483 | Urna ligada em N/N/N às N:N:N | Urna ligada em 27/09/2026 às 13:56:10 |
| 463 | Iniciando registro do log na MI e na ME | Iniciando registro do log na MI e na ME |
| 463 | Lendo o serial da MV original a partir da MI | Lendo o serial da MV original a partir da MI |
| 459 | Verificação de assinatura - Etapa [N] - [/dsk/fe/estatico/N-lo.vsc] - [SUCESSO] | Verificação de assinatura - Etapa [27] - [/dsk/fe/estatico/0100700090001-lo.vsc] - [SUCESSO] |
| 418 | Fechando o arquivo de Log | Fechando o arquivo de Log |
| 398 | Urna operando na rede elétrica | Urna operando na rede elétrica |
| 392 | Imprimindo relatório [BU] via nº [N] | Imprimindo relatório [BU] via nº [1] |
| 387 | Mesário N não é eleitor da seção | Mesário 008281662410 não é eleitor da seção |
| 386 | Desligando a urna | Desligando a urna |
| 383 | Biometria do mesário N encontrada nos arquivos coletados (N) | Biometria do mesário 003812512402 encontrada nos arquivos coletados (910543) |
| 359 | Capturada a digital do mesário | Capturada a digital do mesário |
| 359 | Não encontrou digital coletada em nenhum dos arquivos, vai salvar a digital em novo arquivo. | Não encontrou digital coletada em nenhum dos arquivos, vai salvar a digital em novo arquivo. |
| 351 | Urna desligada pela chave | Urna desligada pela chave |
| 331 | Mudança do estado da chave: URNA DESLIGADA | Mudança do estado da chave: URNA DESLIGADA |
| 330 | Timeout de reconhecimento do dedo. Tentativa [N] de [N] | Timeout de reconhecimento do dedo. Tentativa [2] de [4] |
| 326 | O eleitor identificado já votou | O eleitor identificado já votou |
| 302 | Mesário N é eleitor da seção | Mesário 004758852445 é eleitor da seção |
| 284 | Aguardando data e hora para emissão da zerésima | Aguardando data e hora para emissão da zerésima |
| 270 | Verificação de assinatura de aplicação por etapa [N] - [Pacote: /lib/modules/ueN/avmodueN.vst] - [SUCESSO] | Verificação de assinatura de aplicação por etapa [9] - [Pacote: /lib/modules/ue2022/avmodue2022.vst] - [SUCESSO] |
| 270 | Verificação de assinatura de aplicação por etapa [N] - [Pacote: /uenux/lib/avusrlibueN.vst] - [SUCESSO] | Verificação de assinatura de aplicação por etapa [4] - [Pacote: /uenux/lib/avusrlibue2022.vst] - [SUCESSO] |
| 264 | Operador indagado se finaliza registro mesários | Operador indagado se finaliza registro mesários |
| 263 | Eleitor não encontrado para o identificador informado | Eleitor não encontrado para o identificador informado |
| 260 | Biometria coletada não é do mesário N | Biometria coletada não é do mesário 004758852445 |
| 255 | Espaço utilizado na MV [N.N KB] | Espaço utilizado na MV [366.0 KB] |
| 247 | Espaço utilizado na MI [N.N KB] | Espaço utilizado na MI [429.0 KB] |
| 234 | Operador encerrou ciclo de registro de mesários | Operador encerrou ciclo de registro de mesários |
| 234 | Operador indagado se ocorrerá registro de mesários | Operador indagado se ocorrerá registro de mesários |
| 231 | Dados carregados da geração de MR | Dados carregados da geração de MR |
| 231 | Data e hora da geração da MR: N/N/N às N:N:N | Data e hora da geração da MR: 11/10/2026 às 12:12:11 |
| 231 | MR gerada pelo computador: ZACNSTDN | MR gerada pelo computador: ZAC001STD17 |
| 231 | MR gerada pelo usuário: N | MR gerada pelo usuário: 000000010191 |
| 230 | Aplicativo presente na MR [VOTA] | Aplicativo presente na MR [VOTA] |
| 230 | Iniciando aplicação - ELEIÇÃO OFICIAL SEGUNDO TURNO - Nº turno | Iniciando aplicação - ELEIÇÃO OFICIAL SEGUNDO TURNO - 2º turno |
| 228 | Instalada ou alterada informação complementar de municípios | Instalada ou alterada informação complementar de municípios |
| 228 | Mídia de resultado de Nº turno | Mídia de resultado de 2º turno |
| 227 | Iniciando aplicação - ELEIÇÃO OFICIAL PRIMEIRO TURNO - Nº turno | Iniciando aplicação - ELEIÇÃO OFICIAL PRIMEIRO TURNO - 1º turno |
| 223 | Solicitação ao INIT para executar o aplicativo - ELEIÇÃO OFICIAL PRIMEIRO TURNO | Solicitação ao INIT para executar o aplicativo - ELEIÇÃO OFICIAL PRIMEIRO TURNO |
| 221 | Fim do teste de Teclado do TE - Sucesso | Fim do teste de Teclado do TE - Sucesso |
| 221 | Início do teste de Teclado do TE | Início do teste de Teclado do TE |
| 217 | Tecla pressionada: CORRIGE | Tecla pressionada: CORRIGE |
| 214 | Tecla pressionada: CONFIRMA | Tecla pressionada: CONFIRMA |
| 210 | Realizada a conferência da biometria do mesário | Realizada a conferência da biometria do mesário |
| 208 | Chave ligada | Chave ligada |
| 178 | Problema ao desmontar a MR | Problema ao desmontar a MR |
| 178 | Solicitação ao INIT para executar o aplicativo - ELEIÇÃO OFICIAL SEGUNDO TURNO | Solicitação ao INIT para executar o aplicativo - ELEIÇÃO OFICIAL SEGUNDO TURNO |
| 175 | Justificativa recebida | Justificativa recebida |
| 168 | Digitado título inválido para o registro de mesário | Digitado título inválido para o registro de mesário |
| 166 | Imprimindo relatório de estado da urna | Imprimindo relatório de estado da urna |
| 145 | Mesário indagado se eleitor está votando | Mesário indagado se eleitor está votando |
| 143 | Digital coletada bate com uma digital gravada após o registro inicial de mesário. Não é possível associar a habilitação a um mesário. | Digital coletada bate com uma digital gravada após o registro inicial de mesário. Não é possível associar a habilitação a um mesário. |
| 138 | Mídia de votação gerada pelo computador (nome - tpm - instalação): ZACNSTDN - NBNBNENDDNEN - NFCNE | Mídia de votação gerada pelo computador (nome - tpm - instalação): ZAC001STD013 - 2B8B5E241531DD88E866 - 731FC82E |
| 138 | Mídia de votação gerada pelo computador (nome - tpm - instalação): ZACNSTDN - NCANEAENCNABD - NDN | Mídia de votação gerada pelo computador (nome - tpm - instalação): ZAC001STD33 - 17CA6EAE9570613C8ABD - 8161D583 |
| 137 | Teste de Teclado do TE não executado | Teste de Teclado do TE não executado |
| 129 | Biometria do mesário N encontrada em eleitores | Biometria do mesário 004758852445 encontrada em eleitores |
| 128 | Urna operando na bateria interna | Urna operando na bateria interna |
| 126 | Mídia de votação gerada pelo computador (nome - tpm - instalação): ZACNSTDN - NBNBCNCNFNFN - N | Mídia de votação gerada pelo computador (nome - tpm - instalação): ZAC001STD39 - 0B552BC1572C88F860F6 - 37638090 |
| 121 | Carga da [ALIMENTAÇÃO BATERIA INTERNA]: [PLENA] | Carga da [ALIMENTAÇÃO BATERIA INTERNA]: [PLENA] |
| 109 | Início dos testes | Início dos testes |
| 109 | Mesário indagado sobre qualidade do Boletim de Urna | Mesário indagado sobre qualidade do Boletim de Urna |
| 109 | Operador cancelou o registro de mesários | Operador cancelou o registro de mesários |
| 108 | Operador selecionou: Encerrar votação | Operador selecionou: Encerrar votação |
| 108 | Verificação de assinatura de aplicação por etapa [N] - [Pacote: /lib/modules/avmod.vst] - [SUCESSO] | Verificação de assinatura de aplicação por etapa [8] - [Pacote: /lib/modules/avmod.vst] - [SUCESSO] |
| 108 | Verificação de assinatura de aplicação por etapa [N] - [Pacote: /uenux/lib/avusrlib.vst] - [SUCESSO] | Verificação de assinatura de aplicação por etapa [3] - [Pacote: /uenux/lib/avusrlib.vst] - [SUCESSO] |
| 108 | Verificação de assinatura de dado por etapa [N] - [Pacote: /dsk/fe/estatico/oNac-ce.vsc] - [Arquivo: oNac-ce.dat] - [SUCESSO] | Verificação de assinatura de dado por etapa [1] - [Pacote: /dsk/fe/estatico/o06257ac-ce.vsc] - [Arquivo: o06257ac-ce.dat] - [SUCESSO] |
| 108 | Verificação de assinatura de dado por etapa [N] - [Pacote: /dsk/fe/estatico/oNac-ce.vsc] - [Arquivo: oNac-ce.pid] - [SUCESSO] | Verificação de assinatura de dado por etapa [2] - [Pacote: /dsk/fe/estatico/o06257ac-ce.vsc] - [Arquivo: o06257ac-ce.pid] - [SUCESSO] |
| 107 | Início do teste Teclado TM | Início do teste Teclado TM |
| 107 | Tecla pressionada: BRANCO | Tecla pressionada: BRANCO |
| 107 | Urna pronta para receber votos | Urna pronta para receber votos |
| 106 | Chave desligada | Chave desligada |
| 106 | Fim do teste Alto-falante - SUCESSO | Fim do teste Alto-falante - SUCESSO |
| 106 | Fim do teste CPU - SUCESSO | Fim do teste CPU - SUCESSO |
| 106 | Fim do teste Comunicação TE - SUCESSO | Fim do teste Comunicação TE - SUCESSO |
| 106 | Fim do teste Firmware - SUCESSO | Fim do teste Firmware - SUCESSO |
| 106 | Fim do teste MSE - SUCESSO | Fim do teste MSE - SUCESSO |
| 106 | Fim do teste Memória - SUCESSO | Fim do teste Memória - SUCESSO |
| 106 | Fim do teste Mídia Externa - SUCESSO | Fim do teste Mídia Externa - SUCESSO |
| 106 | Fim do teste Mídia Interna - SUCESSO | Fim do teste Mídia Interna - SUCESSO |
| 106 | Fim do teste Mídia de Resultado - SUCESSO | Fim do teste Mídia de Resultado - SUCESSO |
| 106 | Fim do teste Teclado do TE - SUCESSO | Fim do teste Teclado do TE - SUCESSO |
| 106 | Fim do teste Vídeo - SUCESSO | Fim do teste Vídeo - SUCESSO |
| 106 | Fim do teste Áudio - SUCESSO | Fim do teste Áudio - SUCESSO |
| 106 | Início do teste Alto-falante | Início do teste Alto-falante |
| 106 | Início do teste CPU | Início do teste CPU |
| 106 | Início do teste Comunicação TE | Início do teste Comunicação TE |
| 106 | Início do teste Firmware | Início do teste Firmware |
| 106 | Início do teste MSE | Início do teste MSE |
| 106 | Início do teste Memória | Início do teste Memória |
| 106 | Início do teste Mídia Externa | Início do teste Mídia Externa |
| 106 | Início do teste Mídia Interna | Início do teste Mídia Interna |
| 106 | Início do teste Mídia de Resultado | Início do teste Mídia de Resultado |
| 106 | Início do teste Sensor da Chave | Início do teste Sensor da Chave |
| 106 | Início do teste Teclado do TE | Início do teste Teclado do TE |
| 106 | Início do teste Vídeo | Início do teste Vídeo |
| 106 | Início do teste Áudio | Início do teste Áudio |
| 106 | Montando lista de testes | Montando lista de testes |
| 106 | Montando lista de testes TM | Montando lista de testes TM |
| 106 | Montando lista de testes biometria | Montando lista de testes biometria |
| 106 | Montando lista de testes impressora | Montando lista de testes impressora |
| 106 | Solicitação ao INIT para executar o aplicativo - SISTEMA DE AUTOTESTE | Solicitação ao INIT para executar o aplicativo - SISTEMA DE AUTOTESTE |
| 106 | Urna não testada | Urna não testada |
| 105 | Fim do teste Sensor da Fonte - SUCESSO | Fim do teste Sensor da Fonte - SUCESSO |
| 105 | Início do teste Sensor da Fonte | Início do teste Sensor da Fonte |
| 105 | Operando com a bateria interna | Operando com a bateria interna |
| 105 | Operando com a rede elétrica | Operando com a rede elétrica |
| 104 | Fim do teste Biometria - SUCESSO | Fim do teste Biometria - SUCESSO |
| 104 | Fim do teste Biometria Firmware - SUCESSO | Fim do teste Biometria Firmware - SUCESSO |
| 104 | Fim do teste Bipe TM - SUCESSO | Fim do teste Bipe TM - SUCESSO |
| 104 | Fim do teste Impressora - SUCESSO | Fim do teste Impressora - SUCESSO |
| 104 | Fim do teste LCD TM - SUCESSO | Fim do teste LCD TM - SUCESSO |
| 104 | Fim do teste Led TM - SUCESSO | Fim do teste Led TM - SUCESSO |
| 104 | Fim do teste Sensor da Chave - SUCESSO | Fim do teste Sensor da Chave - SUCESSO |
| 104 | Fim do teste Teclado TM - SUCESSO | Fim do teste Teclado TM - SUCESSO |
| 104 | Identifica que a Urna está testada | Identifica que a Urna está testada |
| 104 | Imprimindo comprovante de carga | Imprimindo comprovante de carga |
| 104 | Início do teste Biometria | Início do teste Biometria |
| 104 | Início do teste Biometria Firmware | Início do teste Biometria Firmware |
| 104 | Início do teste Bipe TM | Início do teste Bipe TM |
| 104 | Início do teste Impressora | Início do teste Impressora |
| 104 | Início do teste LCD TM | Início do teste LCD TM |
| 104 | Início do teste Led TM | Início do teste Led TM |
| 104 | Urna testada com sucesso | Urna testada com sucesso |
| 102 | Imprimindo relatório [RESUMO DA ZERÉSIMA] via nº [N] | Imprimindo relatório [RESUMO DA ZERÉSIMA] via nº [1] |
| 102 | Imprimindo relatório [ZERÉSIMA] via nº [N] | Imprimindo relatório [ZERÉSIMA] via nº [1] |
| 102 | Operador indagado se todas as pessoas presentes votaram | Operador indagado se todas as pessoas presentes votaram |
| 102 | Todas as pessoas presentes já votaram? SIM | Todas as pessoas presentes já votaram? SIM |
| 101 | Aguardando confirmação para emissão da zerésima | Aguardando confirmação para emissão da zerésima |
| 101 | Gerando relatório [RESUMO DA ZERÉSIMA] [INÍCIO] | Gerando relatório [RESUMO DA ZERÉSIMA] [INÍCIO] |
| 101 | Gerando relatório [RESUMO DA ZERÉSIMA] [TÉRMINO] | Gerando relatório [RESUMO DA ZERÉSIMA] [TÉRMINO] |
| 101 | Gerando relatório [ZERÉSIMA] [INÍCIO] | Gerando relatório [ZERÉSIMA] [INÍCIO] |
| 101 | Gerando relatório [ZERÉSIMA] [TÉRMINO] | Gerando relatório [ZERÉSIMA] [TÉRMINO] |
| 100 | Gerando arquivo de resultado [bu.dat] + [Início] | Gerando arquivo de resultado [bu.dat] + [Início] |
| 100 | Gerando arquivo de resultado [bu.dat] + [Término] | Gerando arquivo de resultado [bu.dat] + [Término] |
| 100 | Gerando arquivo de resultado [hash.dat] + [Início] | Gerando arquivo de resultado [hash.dat] + [Início] |
| 100 | Gerando arquivo de resultado [hash.dat] + [Término] | Gerando arquivo de resultado [hash.dat] + [Término] |
| 100 | Gerando arquivo de resultado [imgbu.dat] + [Início] | Gerando arquivo de resultado [imgbu.dat] + [Início] |
| 100 | Gerando arquivo de resultado [imgbu.dat] + [Término] | Gerando arquivo de resultado [imgbu.dat] + [Término] |
| 100 | Gerando arquivo de resultado [imgze.dat] + [Início] | Gerando arquivo de resultado [imgze.dat] + [Início] |
| 100 | Gerando arquivo de resultado [imgze.dat] + [Término] | Gerando arquivo de resultado [imgze.dat] + [Término] |
| 100 | Gerando arquivo de resultado [jufa.dat] + [Início] | Gerando arquivo de resultado [jufa.dat] + [Início] |
| 100 | Gerando arquivo de resultado [jufa.dat] + [Término] | Gerando arquivo de resultado [jufa.dat] + [Término] |
| 100 | Gerando arquivo de resultado [log.jez] + [Início] | Gerando arquivo de resultado [log.jez] + [Início] |
| 100 | Gerando arquivo de resultado [mr.ver] + [Início] | Gerando arquivo de resultado [mr.ver] + [Início] |
| 100 | Gerando arquivo de resultado [mr.ver] + [Término] | Gerando arquivo de resultado [mr.ver] + [Término] |
| 100 | Gerando arquivo de resultado [rdv.dat] + [Início] | Gerando arquivo de resultado [rdv.dat] + [Início] |
| 100 | Gerando arquivo de resultado [rdv.dat] + [Término] | Gerando arquivo de resultado [rdv.dat] + [Término] |
| 100 | Gerando arquivo de resultado [wsqbio.jez] + [Início] | Gerando arquivo de resultado [wsqbio.jez] + [Início] |
| 100 | Gerando arquivo de resultado [wsqbio.jez] + [Término] | Gerando arquivo de resultado [wsqbio.jez] + [Término] |
| 100 | Gerando arquivo de resultado [wsqman.jez] + [Início] | Gerando arquivo de resultado [wsqman.jez] + [Início] |
| 100 | Gerando arquivo de resultado [wsqman.jez] + [Término] | Gerando arquivo de resultado [wsqman.jez] + [Término] |
| 100 | Gerando arquivo de resultado [wsqmes.jez] + [Início] | Gerando arquivo de resultado [wsqmes.jez] + [Início] |
| 100 | Gerando arquivo de resultado [wsqmes.jez] + [Término] | Gerando arquivo de resultado [wsqmes.jez] + [Término] |
| 100 | Gerando relatório [BIM] [INÍCIO] | Gerando relatório [BIM] [INÍCIO] |
| 100 | Gerando relatório [BIM] [TÉRMINO] | Gerando relatório [BIM] [TÉRMINO] |
| 100 | Gerando relatório [BUJ] [INÍCIO] | Gerando relatório [BUJ] [INÍCIO] |
| 100 | Gerando relatório [BUJ] [TÉRMINO] | Gerando relatório [BUJ] [TÉRMINO] |
| 100 | Gerando relatório [BU] [INÍCIO] | Gerando relatório [BU] [INÍCIO] |
| 100 | Gerando relatório [BU] [TÉRMINO] | Gerando relatório [BU] [TÉRMINO] |
| 100 | Gerando relatório [ELEITORES HABILITADOS BIOGRAFICAMENTE] [INÍCIO] | Gerando relatório [ELEITORES HABILITADOS BIOGRAFICAMENTE] [INÍCIO] |
| 100 | Gerando relatório [ELEITORES HABILITADOS BIOGRAFICAMENTE] [TÉRMINO] | Gerando relatório [ELEITORES HABILITADOS BIOGRAFICAMENTE] [TÉRMINO] |
| 100 | Inicio do Encerramento | Inicio do Encerramento |
| 100 | Mesário indicou qualidade OK para Boletim de Urna | Mesário indicou qualidade OK para Boletim de Urna |
| 100 | Procedimento de encerramento confirmado | Procedimento de encerramento confirmado |
| 100 | Título digitado para encerramento: N | Título digitado para encerramento: 004758852445 |
| 97 | Registrando mesários antes da votação | Registrando mesários antes da votação |
| 97 | Registrando mesários após a votação | Registrando mesários após a votação |
| 96 | Eleitor está votando | Eleitor está votando |
| 94 | Habilitação cancelada durante confirmação de dado do eleitor | Habilitação cancelada durante confirmação de dado do eleitor |
| 93 | Votação encerrada | Votação encerrada |
| 92 | Mesário indagado sobre quantidade de vias adicionais | Mesário indagado sobre quantidade de vias adicionais |
| 75 | Urna ligada conectada na rede CA em [N.NV] e na Bateria Interna com [N.NV/N.NA] | Urna ligada conectada na rede CA em [125.12V] e na Bateria Interna com [13.59V/1.21A] |
| 69 | Digital capturada não corresponde a digital do eleitor: Polegar Direito [score N], Polegar Esquerdo [score N], Indicador Direito [score N], Indicador Esquerdo [score N] | Digital capturada não corresponde a digital do eleitor: Polegar Direito [score 5], Polegar Esquerdo [score 4], Indicador Direito [score 3], Indicador Esquerdo [score 4] |
| 66 | Mídia de votação gerada pelo computador (nome - tpm - instalação): ZACNSTDN - NBFCNBAFF - NFN | Mídia de votação gerada pelo computador (nome - tpm - instalação): ZAC001STD34 - 53992BFC29499366BAFF - 6113F745 |
| 56 | Habilitação cancelada durante reconhecimento biométrico | Habilitação cancelada durante reconhecimento biométrico |
| 54 | Confirmação do extrato de carga | Confirmação do extrato de carga |
| 54 | Código de carga N.N.N.N.N.N.N.N gravado na tabela de correspondência | Código de carga 997.198.101.523.282.243.858.675 gravado na tabela de correspondência |
| 54 | Cópia de Log da ME para MI realizada com sucesso. | Cópia de Log da ME para MI realizada com sucesso. |
| 54 | Data e hora atualizada | Data e hora atualizada |
| 54 | Data e hora da geração da mídia de carga: N/N/N N:N:N | Data e hora da geração da mídia de carga: 19/09/2026 10:42:03 |
| 54 | Data e hora que foi digitada pelo operador: N/N/N - N:N:N | Data e hora que foi digitada pelo operador: 27/09/2026 - 14:00:00 |
| 54 | Data e hora solicitadas | Data e hora solicitadas |
| 54 | Estrutura da mídia criada | Estrutura da mídia criada |
| 54 | Formatação realizada com sucesso | Formatação realizada com sucesso |
| 54 | Identificação de assinatura do arquivo EG GAP N MI | Identificação de assinatura do arquivo EG GAP 1 MI |
| 54 | Identificação de assinatura do arquivo EG Geral MI | Identificação de assinatura do arquivo EG Geral MI |
| 54 | Identificação de assinatura do arquivo EG RED MI | Identificação de assinatura do arquivo EG RED MI |
| 54 | Identificação de assinatura do arquivo EG SA MI | Identificação de assinatura do arquivo EG SA MI |
| 54 | Identificação de assinatura do arquivo EG VOTA MI | Identificação de assinatura do arquivo EG VOTA MI |
| 54 | Identificação de assinatura do arquivo Tabela de correspondência | Identificação de assinatura do arquivo Tabela de correspondência |
| 54 | Identificação de assinatura do arquivo UENUX CFG | Identificação de assinatura do arquivo UENUX CFG |
| 54 | Imprimindo extrato de carga | Imprimindo extrato de carga |
| 54 | Iniciando cópia de Log da ME para MI | Iniciando cópia de Log da ME para MI |
| 54 | Início da formatação da MI | Início da formatação da MI |
| 54 | Início da montagem dos dados | Início da montagem dos dados |
| 54 | Início do particionamento da MI | Início do particionamento da MI |
| 54 | Local de Votação: N | Local de Votação: 1104 |
| 54 | Montagem realizada com sucesso | Montagem realizada com sucesso |
| 54 | Mídia de carga gerada pelo usuário: N | Mídia de carga gerada pelo usuário: 002327472437 |
| 54 | Particionamento realizado com sucesso | Particionamento realizado com sucesso |
| 54 | Resultado da verificação da mídia interna: NORMAL | Resultado da verificação da mídia interna: NORMAL |
| 54 | Tamanho da memória: N.N GB | Tamanho da memória: 3.7 GB |
| 54 | Tamanho da mídia interna: N.N GB | Tamanho da mídia interna: 3.7 GB |
| 54 | Urna carregada com sucesso | Urna carregada com sucesso |
| 54 | Verificação de assinatura de aplicação por etapa [N] - [Pacote: /bin/avbin.vst] - [SUCESSO] | Verificação de assinatura de aplicação por etapa [1] - [Pacote: /bin/avbin.vst] - [SUCESSO] |
| 54 | Verificação de assinatura de aplicação por etapa [N] - [Pacote: /boot/boot/avboot.vst] - [SUCESSO] | Verificação de assinatura de aplicação por etapa [5] - [Pacote: /boot/boot/avboot.vst] - [SUCESSO] |
| 54 | Verificação de assinatura de aplicação por etapa [N] - [Pacote: /boot/boot/avbootcfg.vst] - [SUCESSO] | Verificação de assinatura de aplicação por etapa [6] - [Pacote: /boot/boot/avbootcfg.vst] - [SUCESSO] |
| 54 | Verificação de assinatura de aplicação por etapa [N] - [Pacote: /dsk/fe/estatico/chave/avusrchave.vst] - [SUCESSO] | Verificação de assinatura de aplicação por etapa [29] - [Pacote: /dsk/fe/estatico/chave/avusrchave.vst] - [SUCESSO] |
| 54 | Verificação de assinatura de aplicação por etapa [N] - [Pacote: /etc/RHVoice/avrhvoice.vst] - [Arquivo: RHVoice.conf] - [SUCESSO] | Verificação de assinatura de aplicação por etapa [24] - [Pacote: /etc/RHVoice/avrhvoice.vst] - [Arquivo: RHVoice.conf] - [SUCESSO] |
| 54 | Verificação de assinatura de aplicação por etapa [N] - [Pacote: /etc/avetc.vst] - [SUCESSO] | Verificação de assinatura de aplicação por etapa [23] - [Pacote: /etc/avetc.vst] - [SUCESSO] |
| 54 | Verificação de assinatura de aplicação por etapa [N] - [Pacote: /lib/avlib.vst] - [SUCESSO] | Verificação de assinatura de aplicação por etapa [7] - [Pacote: /lib/avlib.vst] - [SUCESSO] |
| 54 | Verificação de assinatura de aplicação por etapa [N] - [Pacote: /lib/plugins/generic/avlibqtgeneric.vst] - [SUCESSO] | Verificação de assinatura de aplicação por etapa [10] - [Pacote: /lib/plugins/generic/avlibqtgeneric.vst] - [SUCESSO] |
| 54 | Verificação de assinatura de aplicação por etapa [N] - [Pacote: /lib/plugins/imageformats/avlibqtimageformats.vst] - [SUCESSO] | Verificação de assinatura de aplicação por etapa [11] - [Pacote: /lib/plugins/imageformats/avlibqtimageformats.vst] - [SUCESSO] |
| 54 | Verificação de assinatura de aplicação por etapa [N] - [Pacote: /lib/plugins/platforms/avlibqtplatforms.vst] - [SUCESSO] | Verificação de assinatura de aplicação por etapa [12] - [Pacote: /lib/plugins/platforms/avlibqtplatforms.vst] - [SUCESSO] |
| 54 | Verificação de assinatura de aplicação por etapa [N] - [Pacote: /share/RHVoice/languages/Brazilian-Portuguese/avsharerhvoicelang.vst] - [SUCESSO] | Verificação de assinatura de aplicação por etapa [25] - [Pacote: /share/RHVoice/languages/Brazilian-Portuguese/avsharerhvoicelang.vst] - [SUCESSO] |
| 54 | Verificação de assinatura de aplicação por etapa [N] - [Pacote: /share/RHVoice/languages/Brazilian-Portuguese/userdict/src/avsharerhvoicelangdict.vst] - [Arquivo: dict.txt] - [SUCESSO] | Verificação de assinatura de aplicação por etapa [26] - [Pacote: /share/RHVoice/languages/Brazilian-Portuguese/userdict/src/avsharerhvoicelangdict.vst] - [Arquivo: dict.txt] - [SUCESSO] |
| 54 | Verificação de assinatura de aplicação por etapa [N] - [Pacote: /share/RHVoice/voices/Leticia-FN/N/avsharerhvoiceNkhz.vst] - [SUCESSO] | Verificação de assinatura de aplicação por etapa [28] - [Pacote: /share/RHVoice/voices/Leticia-F123/16000/avsharerhvoice24khz.vst] - [SUCESSO] |
| 54 | Verificação de assinatura de aplicação por etapa [N] - [Pacote: /share/RHVoice/voices/Leticia-FN/avsharerhvoiceleticia.vst] - [SUCESSO] | Verificação de assinatura de aplicação por etapa [27] - [Pacote: /share/RHVoice/voices/Leticia-F123/avsharerhvoiceleticia.vst] - [SUCESSO] |
| 54 | Verificação de assinatura de aplicação por etapa [N] - [Pacote: /uenux/bin/avusrbin.vst] - [SUCESSO] | Verificação de assinatura de aplicação por etapa [2] - [Pacote: /uenux/bin/avusrbin.vst] - [SUCESSO] |
| 54 | Verificação de assinatura de dado por etapa [N] - [Pacote: /dsk/fe/estatico/jez/avgm.vsc] - [SUCESSO] | Verificação de assinatura de dado por etapa [5] - [Pacote: /dsk/fe/estatico/jez/avgm.vsc] - [SUCESSO] |
| 54 | Verificação de assinatura de dado por etapa [N] - [Pacote: /dsk/fe/estatico/jez/avpart_ofi.vst] - [SUCESSO] | Verificação de assinatura de dado por etapa [12] - [Pacote: /dsk/fe/estatico/jez/avpart_ofi.vst] - [SUCESSO] |
| 54 | Verificação de assinatura de dado por etapa [N] - [Pacote: /dsk/fe/estatico/jez/vota_apl.vst] - [SUCESSO] | Verificação de assinatura de dado por etapa [10] - [Pacote: /dsk/fe/estatico/jez/vota_apl.vst] - [SUCESSO] |
| 54 | Verificação de assinatura de dado por etapa [N] - [Pacote: /dsk/fe/estatico/jez/vota_ofi.vst] - [SUCESSO] | Verificação de assinatura de dado por etapa [11] - [Pacote: /dsk/fe/estatico/jez/vota_ofi.vst] - [SUCESSO] |
| 54 | Verificação de assinatura de dado por etapa [N] - [Pacote: /dsk/fe/estatico/oNacN-ca.vsc] - [SUCESSO] | Verificação de assinatura de dado por etapa [8] - [Pacote: /dsk/fe/estatico/o06259ac00000-ca.vsc] - [SUCESSO] |
| 54 | Verificação de assinatura de dado por etapa [N] - [Pacote: /dsk/fe/estatico/oNacN-fo.vsc] - [Arquivo: oNacN-fo.dat] - [SUCESSO] | Verificação de assinatura de dado por etapa [9] - [Pacote: /dsk/fe/estatico/o06259ac00000-fo.vsc] - [Arquivo: o06259ac00000-fo.dat] - [SUCESSO] |
| 54 | Verificação de assinatura de dado por etapa [N] - [Pacote: /dsk/fe/estatico/oNbrN-ca.vsc] - [SUCESSO] | Verificação de assinatura de dado por etapa [6] - [Pacote: /dsk/fe/estatico/o06257br00000-ca.vsc] - [SUCESSO] |
| 54 | Verificação de assinatura de dado por etapa [N] - [Pacote: /dsk/fe/estatico/oNbrN-fo.vsc] - [Arquivo: oNbrN-fo.dat] - [SUCESSO] | Verificação de assinatura de dado por etapa [7] - [Pacote: /dsk/fe/estatico/o06257br00000-fo.vsc] - [Arquivo: o06257br00000-fo.dat] - [SUCESSO] |
| 54 | Versão do UEFI: IYEAN_P | Versão do UEFI: IYEA26_P |
| 53 | Solicitada a retirada da mídia de resultado | Solicitada a retirada da mídia de resultado |
| 52 | Mídia de carga gerada pelo computador (nome - tpm - instalação): ZACNSTDN - NFNCCNDNABNBN - FFNFENBN | Mídia de carga gerada pelo computador (nome - tpm - instalação): ZAC001STD29 - 6F4108493CC3D22AB9B7 - FF1FE3B5 |
| 52 | Urna ligada desconectada da rede CA em [N.NV] e na Bateria Interna com [N.NV/-N.NA] | Urna ligada desconectada da rede CA em [0.00V] e na Bateria Interna com [13.30V/-0.76A] |
| 50 | Copiando arquivo de resultado para ME: [bu.dat] | Copiando arquivo de resultado para ME: [bu.dat] |
| 50 | Copiando arquivo de resultado para ME: [hash.dat] | Copiando arquivo de resultado para ME: [hash.dat] |
| 50 | Copiando arquivo de resultado para ME: [imgbu.dat] | Copiando arquivo de resultado para ME: [imgbu.dat] |
| 50 | Copiando arquivo de resultado para ME: [imgze.dat] | Copiando arquivo de resultado para ME: [imgze.dat] |
| 50 | Copiando arquivo de resultado para ME: [jufa.dat] | Copiando arquivo de resultado para ME: [jufa.dat] |
| 50 | Copiando arquivo de resultado para ME: [log.jez] | Copiando arquivo de resultado para ME: [log.jez] |
| 50 | Copiando arquivo de resultado para ME: [mr.ver] | Copiando arquivo de resultado para ME: [mr.ver] |
| 50 | Copiando arquivo de resultado para ME: [rdv.dat] | Copiando arquivo de resultado para ME: [rdv.dat] |
| 50 | Copiando arquivo de resultado para ME: [vota.vsc] | Copiando arquivo de resultado para ME: [vota.vsc] |
| 50 | Copiando arquivo de resultado para ME: [wsqbio.jez] | Copiando arquivo de resultado para ME: [wsqbio.jez] |
| 50 | Copiando arquivo de resultado para ME: [wsqman.jez] | Copiando arquivo de resultado para ME: [wsqman.jez] |
| 50 | Copiando arquivo de resultado para ME: [wsqmes.jez] | Copiando arquivo de resultado para ME: [wsqmes.jez] |
| 50 | Copiando arquivo de resultado para MI: [bu.dat] | Copiando arquivo de resultado para MI: [bu.dat] |
| 50 | Copiando arquivo de resultado para MI: [hash.dat] | Copiando arquivo de resultado para MI: [hash.dat] |
| 50 | Copiando arquivo de resultado para MI: [imgbu.dat] | Copiando arquivo de resultado para MI: [imgbu.dat] |
| 50 | Copiando arquivo de resultado para MI: [imgze.dat] | Copiando arquivo de resultado para MI: [imgze.dat] |
| 50 | Copiando arquivo de resultado para MI: [jufa.dat] | Copiando arquivo de resultado para MI: [jufa.dat] |
| 50 | Copiando arquivo de resultado para MI: [log.jez] | Copiando arquivo de resultado para MI: [log.jez] |
| 50 | Copiando arquivo de resultado para MI: [mr.ver] | Copiando arquivo de resultado para MI: [mr.ver] |
| 50 | Copiando arquivo de resultado para MI: [rdv.dat] | Copiando arquivo de resultado para MI: [rdv.dat] |
| 50 | Copiando arquivo de resultado para MI: [wsqbio.jez] | Copiando arquivo de resultado para MI: [wsqbio.jez] |
| 50 | Copiando arquivo de resultado para MI: [wsqman.jez] | Copiando arquivo de resultado para MI: [wsqman.jez] |
| 50 | Copiando arquivo de resultado para MI: [wsqmes.jez] | Copiando arquivo de resultado para MI: [wsqmes.jez] |
| 50 | Cópia dos diretórios da MI para a nova MV | Cópia dos diretórios da MI para a nova MV |
| 50 | Final de cópia do log da MI para ME | Final de cópia do log da MI para ME |
| 50 | Finaliza a sessão no MSE | Finaliza a sessão no MSE |
| 50 | Gerando arquivo de resultado [log.jez] + [Término] | Gerando arquivo de resultado [log.jez] + [Término] |
| 50 | Imprimindo extrato de Nº turno | Imprimindo extrato de 2º turno |
| 50 | Imprimindo relatório [BIM] via nº [N] | Imprimindo relatório [BIM] via nº [1] |
| 50 | Imprimindo relatório [BUJ] via nº [N] | Imprimindo relatório [BUJ] via nº [1] |
| 50 | Imprimindo relatório [ELEITORES HABILITADOS BIOGRAFICAMENTE] via nº [N] | Imprimindo relatório [ELEITORES HABILITADOS BIOGRAFICAMENTE] via nº [1] |
| 50 | Inicia uma sessão no MSE | Inicia uma sessão no MSE |
| 50 | Instalada ou alterada informação de candidatura | Instalada ou alterada informação de candidatura |
| 50 | Início de cópia do log da MI para ME | Início de cópia do log da MI para ME |
| 50 | Início do procedimento de assinatura dos arquivos de resultados | Início do procedimento de assinatura dos arquivos de resultados |
| 50 | Início do procedimento de preparação da MV para utilização | Início do procedimento de preparação da MV para utilização |
| 50 | Mesário não solicitou emissão de vias adicionais | Mesário não solicitou emissão de vias adicionais |
| 50 | Mídia de resultado gravada | Mídia de resultado gravada |
| 50 | Mídia de resultado retirada | Mídia de resultado retirada |
| 50 | Mídia de votação sendo utilizada pela primeira vez | Mídia de votação sendo utilizada pela primeira vez |
| 50 | Preparando para assinatura dos arquivos de resultados | Preparando para assinatura dos arquivos de resultados |
| 50 | Preparação de MV para utilização executada com sucesso | Preparação de MV para utilização executada com sucesso |
| 50 | Serial da MV registrada na MI | Serial da MV registrada na MI |
| 50 | Seção informada pelo operador: N | Seção informada pelo operador: 0001 |
| 50 | Término do procedimento de assinatura dos arquivos de resultados | Término do procedimento de assinatura dos arquivos de resultados |
| 50 | Término do processo de preparação da MV para utilização | Término do processo de preparação da MV para utilização |
| 50 | Urna transitada para Nº Turno | Urna transitada para 2º Turno |
| 47 | Dado digitado não confere | Dado digitado não confere |
| 45 | Solicitado ao mesário que conecte o fone de ouvido | Solicitado ao mesário que conecte o fone de ouvido |
| 45 | Solicitado ao mesário que desconecte o fone de ouvido | Solicitado ao mesário que desconecte o fone de ouvido |
| 45 | Áudio ativado conforme cadastro | Áudio ativado conforme cadastro |
| 45 | Áudio desativado pelo fim da votação | Áudio desativado pelo fim da votação |
| 41 | Solicitada a emissão de [N] vias adicionais | Solicitada a emissão de [3] vias adicionais |
| 40 | Identificador inválido para o tipo informado | Identificador inválido para o tipo informado |
| 38 | Mesário N já registrado | Mesário 008979462445 já registrado |
| 37 | Biometria do mesário N encontrada em eleitores (N) | Biometria do mesário 004670752429 encontrada em eleitores (666128) |
| 37 | Fone de ouvido desconectado | Fone de ouvido desconectado |
| 36 | Fone de ouvido conectado | Fone de ouvido conectado |
| 35 | Ciclo de teste reiniciado | Ciclo de teste reiniciado |
| 35 | Dado digitado está incompleto | Dado digitado está incompleto |
| 35 | Operador escolheu a opção de reiniciar o ciclo de teste | Operador escolheu a opção de reiniciar o ciclo de teste |
| 32 | Operador selecionou: Registrar mesários | Operador selecionou: Registrar mesários |
| 31 | Urna operando com bateria interna | Urna operando com bateria interna |
| 28 | Teste Teclado TM | Teste Teclado TM |
| 27 | Mesário cancelou entrada dos dados | Mesário cancelou entrada dos dados |
| 25 | Eleitor impedido - título suspenso | Eleitor impedido - título suspenso |
| 25 | Serial da MV: N | Serial da MV: 20536168 |
| 23 | Mesário digitou o título para suspender o eleitor | Mesário digitou o título para suspender o eleitor |
| 23 | Mídia de votação gerada pelo computador (nome - tpm - instalação): ZACNSTDN - NFADBNCNDNBDN - EDAAFNBN | Mídia de votação gerada pelo computador (nome - tpm - instalação): ZAC001STD35 - 4FADB8C72D2471BD0673 - EDAAF7B1 |
| 21 | Falha do teste: Tecla esperada N. Tecla pressionada N | Falha do teste: Tecla esperada 3. Tecla pressionada 2 |
| 21 | Habilitação cancelada durante a captura de digital do mesário | Habilitação cancelada durante a captura de digital do mesário |
| 21 | Mídia de votação gerada pelo computador (nome - tpm - instalação): ZACNSTDN - NANANEFCNDNDCCFN - ENBN | Mídia de votação gerada pelo computador (nome - tpm - instalação): ZAC001STD17 - 795A88A4EFC41D2DCCF7 - E893B062 |
| 21 | Registrando mesários durante a votação | Registrando mesários durante a votação |
| 21 | Serial da MV original da urna que está registrada na MI: N | Serial da MV original da urna que está registrada na MI: 20536168 |
| 20 | Mídia de votação gerada pelo computador (nome - tpm - instalação): ZACNSTDN - NDFFNBBDNANFN - ACNFC | Mídia de votação gerada pelo computador (nome - tpm - instalação): ZAC001STD13 - 497DFF7616BBD89A3F60 - AC6017FC |
| 18 | Eleitor não está votando | Eleitor não está votando |
| 18 | Modo de carga da UE - Urna de contingência | Modo de carga da UE - Urna de contingência |
| 18 | Solicitado título eleitoral para suspensão do eleitor | Solicitado título eleitoral para suspensão do eleitor |
| 17 | Carga da [ALIMENTAÇÃO BATERIA INTERNA]: [PARCIAL] | Carga da [ALIMENTAÇÃO BATERIA INTERNA]: [PARCIAL] |
| 16 | Serial da MV: NFCECN | Serial da MV: 4FCEC908 |
| 14 | Operador selecionou: Exibir contadores | Operador selecionou: Exibir contadores |
| 14 | Serial da MV original da urna que está registrada na MI: NFCECN | Serial da MV original da urna que está registrada na MI: 4FCEC908 |
| 14 | Serial da MV: BNEN | Serial da MV: B8E41237 |
| 14 | Serial da MV: NBEDCNCN | Serial da MV: 6BEDC1C8 |
| 13 | Serial da MV: CNAANAA | Serial da MV: C1AA19AA |
| 13 | Serial da MV: NCBEN | Serial da MV: 593CBE92 |
| 13 | Serial da MV: NCNCNCN | Serial da MV: 8C39C7C4 |
| 13 | Serial da MV: NENBA | Serial da MV: 9184E5BA |
| 12 | Ano de nascimento digitado é diferente do cadastro | Ano de nascimento digitado é diferente do cadastro |
| 12 | Bateria interna com carga parcial | Bateria interna com carga parcial |
| 12 | Serial da MV original da urna que está registrada na MI: BNEN | Serial da MV original da urna que está registrada na MI: B8E41237 |
| 12 | Serial da MV original da urna que está registrada na MI: NBEDCNCN | Serial da MV original da urna que está registrada na MI: 6BEDC1C8 |
| 12 | Serial da MV: DN | Serial da MV: D7072612 |
| 12 | Serial da MV: EANCN | Serial da MV: EA7C7972 |
| 12 | Serial da MV: FNA | Serial da MV: F343134A |
| 12 | Serial da MV: NBN | Serial da MV: 2634B711 |
| 12 | Serial da MV: NCAEN | Serial da MV: 0158CAE1 |
| 12 | Serial da MV: NDNC | Serial da MV: 9951D57C |
| 12 | Serial da MV: NDNCNBN | Serial da MV: 2D7C8B54 |
| 12 | Serial da MV: NE | Serial da MV: 4315341E |
| 12 | Serial da MV: NENCB | Serial da MV: 3E5833CB |
| 12 | Serial da MV: NFCAN | Serial da MV: 1FCA8338 |
| 12 | Título N é inválido para suspender a votação | Título 000058851470 é inválido para suspender a votação |
| 12 | Urna desligada a pedido do aplicativo | Urna desligada a pedido do aplicativo |
| 11 | Eleitor foi suspenso pelo mesário | Eleitor foi suspenso pelo mesário |
| 11 | Eleitor já justificou | Eleitor já justificou |
| 11 | Identificador da mídia de carga: NBNFAN | Identificador da mídia de carga: 1B734FA9 |
| 11 | Mídia de votação gerada pelo computador (nome - tpm - instalação): ZACNSTDN - NCBNBNECNEN - ENANA | Mídia de votação gerada pelo computador (nome - tpm - instalação): ZAC001STD14 - 8CB18558264B33EC8E89 - E31A988A |
| 11 | Serial da MV original da urna que está registrada na MI: CNAANAA | Serial da MV original da urna que está registrada na MI: C1AA19AA |
| 11 | Serial da MV original da urna que está registrada na MI: NCBEN | Serial da MV original da urna que está registrada na MI: 593CBE92 |
| 11 | Serial da MV original da urna que está registrada na MI: NCNCNCN | Serial da MV original da urna que está registrada na MI: 8C39C7C4 |
| 11 | Serial da MV original da urna que está registrada na MI: NENBA | Serial da MV original da urna que está registrada na MI: 9184E5BA |
| 11 | Serial da MV: DNENANA | Serial da MV: D86E1A9A |
| 11 | Serial da MV: FDECNF | Serial da MV: FDEC728F |
| 11 | Serial da MV: FNDN | Serial da MV: F6265D68 |
| 11 | Serial da MV: NANFNCN | Serial da MV: 34A5F9C5 |
| 11 | Serial da MV: NBND | Serial da MV: 4B08131D |
| 11 | Serial da MV: NCENFN | Serial da MV: 65CE36F6 |
| 11 | Serial da MV: NCNDA | Serial da MV: 9920C4DA |
| 11 | Serial da MV: NDBF | Serial da MV: 33887DBF |
| 11 | Serial da MV: NDFNENCE | Serial da MV: 5DF0E5CE |
| 11 | Serial da MV: NEANFAN | Serial da MV: 35EA3FA4 |
| 11 | Serial da MV: NEENENC | Serial da MV: 6EE70E1C |
| 11 | Serial da MV: NFCEDN | Serial da MV: 49FCED80 |
| 11 | Título N é válido para suspender a votação | Título 005885812470 é válido para suspender a votação |
| 10 | Identificador da mídia de carga: FBNDENB | Identificador da mídia de carga: FB7DE83B |
| 10 | Identificador da mídia de carga: NBN | Identificador da mídia de carga: 99B02793 |
| 10 | Identificador da mídia de carga: NENBN | Identificador da mídia de carga: 0E1B9855 |
| 10 | Mídia de votação gerada pelo computador (nome - tpm - instalação): ZACNSTDN - NAENFNDNCFNFDN - FNEN | Mídia de votação gerada pelo computador (nome - tpm - instalação): ZAC001STD15 - 7124AE6F94D7CF47FD41 - F1E18385 |
| 10 | Mídia de votação gerada pelo computador (nome - tpm - instalação): ZACNSTDN - NDNENABBNANBA - DFDAAANB | Mídia de votação gerada pelo computador (nome - tpm - instalação): ZAC001STD12 - 44D2E2930ABB2348A4BA - DFDAAA6B |
| 10 | Número de série da MR: DEEDFDCN | Número de série da MR: DEEDFDC2 |
| 10 | Serial da MV original da urna que está registrada na MI: DN | Serial da MV original da urna que está registrada na MI: D7072612 |
| 10 | Serial da MV original da urna que está registrada na MI: EANCN | Serial da MV original da urna que está registrada na MI: EA7C7972 |
| 10 | Serial da MV original da urna que está registrada na MI: FNA | Serial da MV original da urna que está registrada na MI: F343134A |
| 10 | Serial da MV original da urna que está registrada na MI: NBN | Serial da MV original da urna que está registrada na MI: 2634B711 |
| 10 | Serial da MV original da urna que está registrada na MI: NCAEN | Serial da MV original da urna que está registrada na MI: 0158CAE1 |
| 10 | Serial da MV original da urna que está registrada na MI: NDNC | Serial da MV original da urna que está registrada na MI: 9951D57C |
| 10 | Serial da MV original da urna que está registrada na MI: NDNCNBN | Serial da MV original da urna que está registrada na MI: 2D7C8B54 |
| 10 | Serial da MV original da urna que está registrada na MI: NE | Serial da MV original da urna que está registrada na MI: 4315341E |
| 10 | Serial da MV original da urna que está registrada na MI: NENCB | Serial da MV original da urna que está registrada na MI: 3E5833CB |
| 10 | Serial da MV original da urna que está registrada na MI: NFCAN | Serial da MV original da urna que está registrada na MI: 1FCA8338 |
| 10 | Serial da MV: ANFNCN | Serial da MV: A82F5C10 |
| 10 | Serial da MV: CANFN | Serial da MV: CA7030F4 |
| 10 | Serial da MV: CCDFNFBN | Serial da MV: CCDF2FB4 |
| 10 | Serial da MV: CNANENB | Serial da MV: C7A30E5B |
| 10 | Serial da MV: CNEANBCN | Serial da MV: C4EA7BC8 |
| 10 | Serial da MV: DCEAND | Serial da MV: DCEA667D |
| 10 | Serial da MV: DCNEN | Serial da MV: DC7799E9 |
| 10 | Serial da MV: EAN | Serial da MV: EA280908 |
| 10 | Serial da MV: ENENEANB | Serial da MV: E5E2EA7B |
| 10 | Serial da MV: NAANCN | Serial da MV: 16AA09C6 |
| 10 | Serial da MV: NAEN | Serial da MV: 8AE02059 |
| 10 | Serial da MV: NAN | Serial da MV: 99347A72 |
| 10 | Serial da MV: NANCN | Serial da MV: 30A8C945 |
| 10 | Serial da MV: NANEEN | Serial da MV: 1A1EE069 |
| 10 | Serial da MV: NDAN | Serial da MV: 9520DA60 |
| 10 | Serial da MV: NDNAFBF | Serial da MV: 8D33AFBF |
| 10 | Serial da MV: NDNBAN | Serial da MV: 235D5BA4 |
| 10 | Serial da MV: NFCN | Serial da MV: 39FC9434 |
| 10 | Serial da MV: NFEN | Serial da MV: 98642FE1 |
| 9 | Identificador da mídia de carga: FNCND | Identificador da mídia de carga: F38C758D |
| 9 | Mesário indicou reimprimir Boletim de Urna | Mesário indicou reimprimir Boletim de Urna |
| 9 | Não encontrou estado geral na mídia de votação em UE sem MR nem ME | Não encontrou estado geral na mídia de votação em UE sem MR nem ME |
| 9 | Serial da MV original da urna que está registrada na MI: DNENANA | Serial da MV original da urna que está registrada na MI: D86E1A9A |
| 9 | Serial da MV original da urna que está registrada na MI: FDECNF | Serial da MV original da urna que está registrada na MI: FDEC728F |
| 9 | Serial da MV original da urna que está registrada na MI: FNDN | Serial da MV original da urna que está registrada na MI: F6265D68 |
| 9 | Serial da MV original da urna que está registrada na MI: NANFNCN | Serial da MV original da urna que está registrada na MI: 34A5F9C5 |
| 9 | Serial da MV original da urna que está registrada na MI: NBND | Serial da MV original da urna que está registrada na MI: 4B08131D |
| 9 | Serial da MV original da urna que está registrada na MI: NCENFN | Serial da MV original da urna que está registrada na MI: 65CE36F6 |
| 9 | Serial da MV original da urna que está registrada na MI: NCNDA | Serial da MV original da urna que está registrada na MI: 9920C4DA |
| 9 | Serial da MV original da urna que está registrada na MI: NDBF | Serial da MV original da urna que está registrada na MI: 33887DBF |
| 9 | Serial da MV original da urna que está registrada na MI: NDFNENCE | Serial da MV original da urna que está registrada na MI: 5DF0E5CE |
| 9 | Serial da MV original da urna que está registrada na MI: NEANFAN | Serial da MV original da urna que está registrada na MI: 35EA3FA4 |
| 9 | Serial da MV original da urna que está registrada na MI: NEENENC | Serial da MV original da urna que está registrada na MI: 6EE70E1C |
| 9 | Serial da MV original da urna que está registrada na MI: NFCEDN | Serial da MV original da urna que está registrada na MI: 49FCED80 |
| 9 | Urna de contingência pronta para eleição | Urna de contingência pronta para eleição |
| 8 | Log interno da urna de contingência validado com sucesso | Log interno da urna de contingência validado com sucesso |
| 8 | Número de série da MR: NAN | Número de série da MR: 7A658997 |
| 8 | Serial da MV original da urna que está registrada na MI: ANFNCN | Serial da MV original da urna que está registrada na MI: A82F5C10 |
| 8 | Serial da MV original da urna que está registrada na MI: CANFN | Serial da MV original da urna que está registrada na MI: CA7030F4 |
| 8 | Serial da MV original da urna que está registrada na MI: CCDFNFBN | Serial da MV original da urna que está registrada na MI: CCDF2FB4 |
| 8 | Serial da MV original da urna que está registrada na MI: CNANENB | Serial da MV original da urna que está registrada na MI: C7A30E5B |
| 8 | Serial da MV original da urna que está registrada na MI: CNEANBCN | Serial da MV original da urna que está registrada na MI: C4EA7BC8 |
| 8 | Serial da MV original da urna que está registrada na MI: DCEAND | Serial da MV original da urna que está registrada na MI: DCEA667D |
| 8 | Serial da MV original da urna que está registrada na MI: DCNEN | Serial da MV original da urna que está registrada na MI: DC7799E9 |
| 8 | Serial da MV original da urna que está registrada na MI: EAN | Serial da MV original da urna que está registrada na MI: EA280908 |
| 8 | Serial da MV original da urna que está registrada na MI: ENENEANB | Serial da MV original da urna que está registrada na MI: E5E2EA7B |
| 8 | Serial da MV original da urna que está registrada na MI: NAANCN | Serial da MV original da urna que está registrada na MI: 16AA09C6 |
| 8 | Serial da MV original da urna que está registrada na MI: NAEN | Serial da MV original da urna que está registrada na MI: 8AE02059 |
| 8 | Serial da MV original da urna que está registrada na MI: NAN | Serial da MV original da urna que está registrada na MI: 99347A72 |
| 8 | Serial da MV original da urna que está registrada na MI: NANCN | Serial da MV original da urna que está registrada na MI: 30A8C945 |
| 8 | Serial da MV original da urna que está registrada na MI: NANEEN | Serial da MV original da urna que está registrada na MI: 1A1EE069 |
| 8 | Serial da MV original da urna que está registrada na MI: NDAN | Serial da MV original da urna que está registrada na MI: 9520DA60 |
| 8 | Serial da MV original da urna que está registrada na MI: NDNAFBF | Serial da MV original da urna que está registrada na MI: 8D33AFBF |
| 8 | Serial da MV original da urna que está registrada na MI: NDNBAN | Serial da MV original da urna que está registrada na MI: 235D5BA4 |
| 8 | Serial da MV original da urna que está registrada na MI: NFCN | Serial da MV original da urna que está registrada na MI: 39FC9434 |
| 8 | Serial da MV original da urna que está registrada na MI: NFEN | Serial da MV original da urna que está registrada na MI: 98642FE1 |
| 7 | Mesário abortou processo de suspensão | Mesário abortou processo de suspensão |
| 7 | Número de série da MR: ENENAF | Número de série da MR: E501E3AF |
| 6 | Atribuido voto nulo por suspensão [Presidente] | Atribuido voto nulo por suspensão [Presidente] |
| 6 | Eleitor votou parcialmente e em seguida foi suspenso | Eleitor votou parcialmente e em seguida foi suspenso |
| 6 | Encerramento só pode ser solicitado após as N:N:N horas | Encerramento só pode ser solicitado após as 15:00:00 horas |
| 6 | Não é possível continuar a execução / Erro inesperado (N) / ERROR opening the biometric reader - -N Tire uma foto dessa tela em que apareça o QR Code ao lado e envie para a equipe de suporte para receber auxílio para resolução do problema. Desligue e l | Não é possível continuar a execução / Erro inesperado (5326) / ERROR opening the biometric reader - -2 Tire uma foto dessa tela em que apareça o QR Code ao lado e envie para a equipe de suporte para receber auxílio para resolução do problema. Desligue e l |
| 6 | Número de série da MR: EANAF | Número de série da MR: EA3824AF |
| 6 | Número de série da MR: NCNF | Número de série da MR: 9C23009F |
| 6 | Quantidade de vias adicionais excede o máximo permitido | Quantidade de vias adicionais excede o máximo permitido |
| 6 | Solicitada a emissão de [N] via adicional | Solicitada a emissão de [1] via adicional |
| 6 | Tempo limite de espera usando bateria interna atingido | Tempo limite de espera usando bateria interna atingido |
| 6 | WHAT: void api::CFingerScanner::Open():N:N - ERROR opening the biometric reader - -N | WHAT: void api::CFingerScanner::Open():151:5326 - ERROR opening the biometric reader - -2 |
| 5 | Atribuido voto nulo por suspensão [Senador] | Atribuido voto nulo por suspensão [Senador] |
| 5 | Eleitor foi suspenso e não confirmou nenhum voto | Eleitor foi suspenso e não confirmou nenhum voto |
| 5 | Eleitor impedido - título cancelado | Eleitor impedido - título cancelado |
| 5 | Falha do teste: Tecla esperada CORRIGE. Tecla pressionada N | Falha do teste: Tecla esperada CORRIGE. Tecla pressionada 0 |
| 5 | Número de série da MR: BNDFN | Número de série da MR: B47DF838 |
| 5 | Número de série da MR: CCBNANF | Número de série da MR: CCB8A23F |
| 5 | Número de série da MR: CDNBN | Número de série da MR: CD591B99 |
| 5 | Número de série da MR: CFDNENBN | Número de série da MR: CFD0E5B0 |
| 5 | Número de série da MR: CNFNBNBN | Número de série da MR: C6F4B0B9 |
| 5 | Número de série da MR: CNFNCN | Número de série da MR: C24F8C79 |
| 5 | Número de série da MR: DCNENCE | Número de série da MR: DC5E76CE |
| 5 | Número de série da MR: EBENAN | Número de série da MR: EBE82A17 |
| 5 | Número de série da MR: ENBNFCN | Número de série da MR: E4B5FC10 |
| 5 | Número de série da MR: NACNFAN | Número de série da MR: 0AC35FA3 |
| 5 | Número de série da MR: NADNCN | Número de série da MR: 658AD4C2 |
| 5 | Número de série da MR: NBDNF | Número de série da MR: 3321BD8F |
| 5 | Número de série da MR: NCCAN | Número de série da MR: 31CCA779 |
| 5 | Número de série da MR: NCNENDAN | Número de série da MR: 7C3E3DA9 |
| 5 | Número de série da MR: NENANAD | Número de série da MR: 55E9A1AD |
| 5 | Número de série da MR: NFEN | Número de série da MR: 449FE495 |
| 5 | Número de série da MR: NFFNDN | Número de série da MR: 412FF5D6 |
| 4 | A chave pública (N.pub) foi encontrada na mídia de resultado | A chave pública (99.pub) foi encontrada na mídia de resultado |
| 4 | Contingência executada com sucesso | Contingência executada com sucesso |
| 4 | Copiando conteúdo da pasta logs da MI para ME | Copiando conteúdo da pasta logs da MI para ME |
| 4 | Fim da cópia do conteúdo da pasta logs da MI para ME | Fim da cópia do conteúdo da pasta logs da MI para ME |
| 4 | Iniciando aplicação VERIFICAÇÃO DE ASSINATURAS | Iniciando aplicação VERIFICAÇÃO DE ASSINATURAS |
| 4 | Início do procedimento de contingência | Início do procedimento de contingência |
| 4 | Número de série da MR: ADCNCNBN | Número de série da MR: ADC0C7B6 |
| 4 | Número de série da MR: BCNEN | Número de série da MR: BC5E5640 |
| 4 | Número de série da MR: BDNDAN | Número de série da MR: BD4DA216 |
| 4 | Número de série da MR: BNBANA | Número de série da MR: B8BA277A |
| 4 | Número de série da MR: CENA | Número de série da MR: CE17135A |
| 4 | Número de série da MR: CN | Número de série da MR: C0915870 |
| 4 | Número de série da MR: CNANFDN | Número de série da MR: C8A22FD0 |
| 4 | Número de série da MR: CNDFNDN | Número de série da MR: C0DF9D46 |
| 4 | Número de série da MR: EN | Número de série da MR: E1409716 |
| 4 | Número de série da MR: FENDFN | Número de série da MR: FE3DF397 |
| 4 | Número de série da MR: FNBN | Número de série da MR: F0B66231 |
| 4 | Número de série da MR: FNBNFN | Número de série da MR: F9B44F58 |
| 4 | Número de série da MR: NACNB | Número de série da MR: 5AC2983B |
| 4 | Número de série da MR: NANBNCN | Número de série da MR: 34A8B6C7 |
| 4 | Número de série da MR: NANFN | Número de série da MR: 07A54F45 |
| 4 | Número de série da MR: NBNAN | Número de série da MR: 7B9A7954 |
| 4 | Número de série da MR: NC | Número de série da MR: 9775895C |
| 4 | Número de série da MR: NCEADN | Número de série da MR: 254CEAD1 |
| 4 | Número de série da MR: NDBNDN | Número de série da MR: 684DB2D6 |
| 4 | Número de série da MR: NDNBAC | Número de série da MR: 03D74BAC |
| 4 | Número de série da MR: NDNFCN | Número de série da MR: 2D4FC975 |
| 4 | Número de série da MR: NECNDFF | Número de série da MR: 9EC03DFF |
| 4 | Número de série da MR: NEFND | Número de série da MR: 83EF725D |
| 4 | Número de série da MR: NENBN | Número de série da MR: 15E29B86 |
| 4 | Número de série da MR: NFDN | Número de série da MR: 1FD51655 |
| 4 | Número de série da MR: NFNEFND | Número de série da MR: 41F0EF6D |
| 4 | Número de série da MR: NFNF | Número de série da MR: 3714F03F |
| 4 | O número de série da chave pública (N.pub): NENEN | O número de série da chave pública (99.pub): 36452507285E23E9 |
| 4 | O operador confirmou o reinício da urna | O operador confirmou o reinício da urna |
| 4 | Operador selecionou: Ativar áudio | Operador selecionou: Ativar áudio |
| 4 | Reiniciando a urna | Reiniciando a urna |
| 4 | Seção informada pelo operador: N - Urna de contingência | Seção informada pelo operador: 0000 - Urna de contingência |
| 4 | Sincronismo de mídia - Etapa Atualização da correspondência: OK | Sincronismo de mídia - Etapa Atualização da correspondência: OK |
| 4 | Sincronismo de mídia - Etapa Atualização de log: OK | Sincronismo de mídia - Etapa Atualização de log: OK |
| 4 | Sincronismo de mídia - Etapa Atualização do ID da UE: OK | Sincronismo de mídia - Etapa Atualização do ID da UE: OK |
| 4 | Sincronismo de mídia - Etapa Atualização do SerialV: OK | Sincronismo de mídia - Etapa Atualização do SerialV: OK |
| 4 | Sincronismo de mídia - Etapa Atualização do backup de estado geral: OK | Sincronismo de mídia - Etapa Atualização do backup de estado geral: OK |
| 4 | Sincronismo de mídia - Etapa Atualização do modo de carga: OK | Sincronismo de mídia - Etapa Atualização do modo de carga: OK |
| 4 | Sincronismo de mídia - Etapa Atualização dos diretórios: OK | Sincronismo de mídia - Etapa Atualização dos diretórios: OK |
| 4 | Sincronismo de mídia - Etapa Backup do estado geral MI: OK | Sincronismo de mídia - Etapa Backup do estado geral MI: OK |
| 4 | Sincronismo de mídia - Etapa Cópia do estado geral atualizado da MI para MV: OK | Sincronismo de mídia - Etapa Cópia do estado geral atualizado da MI para MV: OK |
| 4 | Sincronismo de mídia - Etapa Início do sincronismo: OK | Sincronismo de mídia - Etapa Início do sincronismo: OK |
| 4 | Sincronismo de mídia - Etapa Remoção do antigo estado geral da MV: OK | Sincronismo de mídia - Etapa Remoção do antigo estado geral da MV: OK |
| 4 | Solicitação ao INIT para executar o aplicativo - VERIFICAÇÃO DE ASSINATURAS | Solicitação ao INIT para executar o aplicativo - VERIFICAÇÃO DE ASSINATURAS |
| 4 | Teste Teclado do TE | Teste Teclado do TE |
| 4 | Término do processo de contingência | Término do processo de contingência |
| 4 | Urna reiniciada a pedido do aplicativo | Urna reiniciada a pedido do aplicativo |
| 3 | Arquivo NME.jez referente ao log corrompido da ME | Arquivo 020477112510202604411301ME.jez referente ao log corrompido da ME |
| 3 | Atribuido voto nulo por suspensão [Governador] | Atribuido voto nulo por suspensão [Governador] |
| 3 | Copiando conteúdo da pasta logs da ME para a MI | Copiando conteúdo da pasta logs da ME para a MI |
| 3 | Eleitor impedido - eleitor convocado pela Justiça Eleitoral | Eleitor impedido - eleitor convocado pela Justiça Eleitoral |
| 3 | Falha do teste: Tecla esperada N. Tecla pressionada CONFIRMA | Falha do teste: Tecla esperada 0. Tecla pressionada CONFIRMA |
| 3 | Falha do teste: Tecla esperada N. Tecla pressionada CORRIGE | Falha do teste: Tecla esperada 1. Tecla pressionada CORRIGE |
| 3 | Fim da cópia do conteúdo da pasta logs da ME para a MI | Fim da cópia do conteúdo da pasta logs da ME para a MI |
| 3 | Identificado arquivo de log corrompido na ME | Identificado arquivo de log corrompido na ME |
| 3 | O operador optou por reexecutar os testes pendentes | O operador optou por reexecutar os testes pendentes |
| 3 | Testes concluídos com erro | Testes concluídos com erro |
| 2 | Ano de nascimento inválido | Ano de nascimento inválido |
| 2 | Atribuido voto nulo por suspensão [Deputado Estadual] | Atribuido voto nulo por suspensão [Deputado Estadual] |
| 2 | GAP erro N / Validação do VOTA / O aplicativo Software de Votação precisa de uma mídia de votação para ser executado. Desligue a urna, insira uma mídia de votação válida e tente novamente. | GAP erro 70 / Validação do VOTA / O aplicativo Software de Votação precisa de uma mídia de votação para ser executado. Desligue a urna, insira uma mídia de votação válida e tente novamente. |
| 2 | Impressora atolada. Aguardando ação do operador | Impressora atolada. Aguardando ação do operador |
| 2 | Mídia de carga gerada pelo computador (nome - tpm - instalação): ZACNSTDN - NBNBNAFNANBDNFDN - NFFEN | Mídia de carga gerada pelo computador (nome - tpm - instalação): ZAC001STD25 - 29B7B62AF8A49BD65FD3 - 5372FFE5 |
| 2 | Mídia externa ausente | Mídia externa ausente |
| 2 | O arquivo temporário N-lo.dat foi encontrado e removido | O arquivo temporário 0100700090136-lo.dat foi encontrado e removido |
| 2 | O arquivo temporário N-lo.vsc foi encontrado e removido | O arquivo temporário 0100700090136-lo.vsc foi encontrado e removido |
| 2 | Operador cancelou o encerramento da votação | Operador cancelou o encerramento da votação |
| 2 | Operador confirmou que concluiu a manutenção na impressora | Operador confirmou que concluiu a manutenção na impressora |
| 2 | WHAT: virtual std::vector<std::unique_ptr<const gap::gatilho::CGatilho> > gap::gatilho::fabricas::CVotaOficialSimulado::Cria() const:N | WHAT: virtual std::vector<std::unique_ptr<const gap::gatilho::CGatilho> > gap::gatilho::fabricas::CVotaOficialSimulado::Cria() const:139 |
| 1 | Adicionando informação do log da ME | Adicionando informação do log da ME |
| 1 | Aplicativos presentes na MR [SA,RED,VPP,ATUE] | Aplicativos presentes na MR [SA,RED,VPP,ATUE] |
| 1 | Arquivo N-N.jez referente ao log da ME | Arquivo 0204663004102026062808-01.jez referente ao log da ME |
| 1 | Bateria interna ausente | Bateria interna ausente |
| 1 | Captura da digital do eleitor / Falha na captura da digital (N) / Ocorreu um erro durante captura da digital do eleitor. Desligue e ligue a urna. Se o erro persistir, substitua a urna. | Captura da digital do eleitor / Falha na captura da digital (5330) / Ocorreu um erro durante captura da digital do eleitor. Desligue e ligue a urna. Se o erro persistir, substitua a urna. |
| 1 | Carga da [ALIMENTAÇÃO BATERIA INTERNA]: [CRÍTICA] | Carga da [ALIMENTAÇÃO BATERIA INTERNA]: [CRÍTICA] |
| 1 | Código de liberação aceito | Código de liberação aceito |
| 1 | Eleitor impedido - eleitor não tem idade mínima para votar | Eleitor impedido - eleitor não tem idade mínima para votar |
| 1 | Falha do teste: Tecla esperada BRANCO. Tecla pressionada N | Falha do teste: Tecla esperada BRANCO. Tecla pressionada 1 |
| 1 | Falha do teste: Tecla esperada CONFIRMA. Tecla pressionada N | Falha do teste: Tecla esperada CONFIRMA. Tecla pressionada 0 |
| 1 | Fim da adição de informação do log da ME | Fim da adição de informação do log da ME |
| 1 | Fim da visualização de arquivos de eleitores e candidatos | Fim da visualização de arquivos de eleitores e candidatos |
| 1 | Fim da visualização de candidatos do Nº turno | Fim da visualização de candidatos do 1º turno |
| 1 | Identificador da mídia de carga: ANENBNCC | Identificador da mídia de carga: A9E1B4CC |
| 1 | Identificador da mídia de carga: ECCENDD | Identificador da mídia de carga: ECCE29DD |
| 1 | Identificador da mídia de carga: NAN | Identificador da mídia de carga: 995077A0 |
| 1 | Identificador da mídia de carga: NDDDAFB | Identificador da mídia de carga: 76DDDAFB |
| 1 | Imprimindo relatório [HASHES ARQUIVOS] [arquivos estáticos] | Imprimindo relatório [HASHES ARQUIVOS] [arquivos estáticos] |
| 1 | Iniciando aplicação VERIFICAÇÃO PRÉ E PÓS | Iniciando aplicação VERIFICAÇÃO PRÉ E PÓS |
| 1 | Início da visualização de arquivos de eleitores e candidatos | Início da visualização de arquivos de eleitores e candidatos |
| 1 | Início da visualização de candidatos do Nº turno | Início da visualização de candidatos do 1º turno |
| 1 | Início do modo de demonstração da votação - Nº turno | Início do modo de demonstração da votação - 1º turno |
| 1 | Limite de mesários registrados atingido. Limite máximo: N | Limite de mesários registrados atingido. Limite máximo: 6 |
| 1 | Mesário indagado se quer imprimir a zerésima | Mesário indagado se quer imprimir a zerésima |
| 1 | Número de série da MR: NBDFN | Número de série da MR: 04BDF373 |
| 1 | Solicita código de liberação de aplicativo | Solicita código de liberação de aplicativo |
| 1 | Solicitação ao INIT para executar o aplicativo - VERIFICAÇÃO PRÉ E PÓS | Solicitação ao INIT para executar o aplicativo - VERIFICAÇÃO PRÉ E PÓS |
| 1 | Teclado TM - Na tecla N: Falha do teste: Tecla esperada CONFIRMA. Tecla pressionada N | Teclado TM - Na tecla 0: Falha do teste: Tecla esperada CONFIRMA. Tecla pressionada 0 |
| 1 | Teclado TM - Na tecla N: Falha do teste: Tecla esperada N. Tecla pressionada N | Teclado TM - Na tecla 1: Falha do teste: Tecla esperada 2. Tecla pressionada 1 |
| 1 | Teclado TM - Timeout no teste do terminal do mesário: Número de tentativas excedido | Teclado TM - Timeout no teste do terminal do mesário: Número de tentativas excedido |
| 1 | Teste Alto-falante | Teste Alto-falante |
| 1 | Teste Led TM | Teste Led TM |
| 1 | Teste Áudio | Teste Áudio |
| 1 | Votação suspensa | Votação suspensa |
| 1 | WHAT: virtual void api::CFingerScanner::StartAcquireImage():N:N - ERROR starting image acquisition - -N | WHAT: virtual void api::CFingerScanner::StartAcquireImage():236:5330 - ERROR starting image acquisition - -6 |
| 1 | Áudio ativado pelo mesário | Áudio ativado pelo mesário |
