# Viabilidade — AC 1º turno (Eleições 2026)

ZIP: `E:\urna-logs-2026\data\raw\bu_imgbu_logjez_rdv_vscmr_2026_1t_AC.zip` (393,536,972 bytes)
Eventos parseados: **11,618,809**
Habilitações no log: **488,718**

## Decisão por análise

| Análise | Status | Motivo |
|---|---|---|
| Total de votos (log × BU) | **go** | BU presente no pacote e/ou habilitações no log |
| % votos/habilitações sem digital | **go** | Habilitações biométricas e/ou manuais identificáveis no log; em 2026 o fluxo sem digital aparece como 'habilitação manual' (ano de nascimento + digital do mesário). Mensagem explícita 'não possui biometria' rara/ausente neste pacote. |
| Impacto após 17h | **go** | Timestamps parseáveis com eventos de habilitação |

## Sinais encontrados no log

- `solicita_digital`: 696,111
- `tipo_habilitacao_bio`: 446,429
- `tipo_habilitacao_qualquer`: 446,429
- `eleitor_habilitado`: 488,718
- `voto_confirmado`: 2,926,754
- `habilitacao_manual`: 25,643
- `digital_mesario`: 30,333
- `encerramento`: 8,018

## Extensões no pacote ZIP

- `bu`: 2,270
- `rdv`: 2,270
- `assinatura`: 2,270
- `logjez`: 2,270
- `imgbu`: 2,270
- `pdf`: 1

## Amostra de métricas (pipeline)

- Total habilitações classificadas: 488,718
- % sem digital (sem_biometria + manual_falha): 4.9922
- % após 17h: 0.0219
- Por tipo: `{'biometrica': 446418, 'manual_falha': 24398, 'desconhecido': 17902}`

## Amostras de mensagens

### eleitor_habilitado
- `04/10/2026 06:02:36 VOTA Eleitor foi habilitado`
- `04/10/2026 06:06:34 VOTA Eleitor foi habilitado`
- `04/10/2026 06:08:29 VOTA Eleitor foi habilitado`
- `04/10/2026 06:10:44 VOTA Eleitor foi habilitado`
- `04/10/2026 06:12:58 VOTA Eleitor foi habilitado`

### tipo_habilitacao_bio
- `04/10/2026 06:02:36 VOTA Tipo de habilitação do eleitor [biométrica]`
- `04/10/2026 06:08:29 VOTA Tipo de habilitação do eleitor [biométrica]`
- `04/10/2026 06:10:44 VOTA Tipo de habilitação do eleitor [biométrica]`
- `04/10/2026 06:12:58 VOTA Tipo de habilitação do eleitor [biométrica]`
- `04/10/2026 06:15:00 VOTA Tipo de habilitação do eleitor [biométrica]`

### habilitacao_manual
- `04/10/2026 06:06:09 VOTA Solicitação de dado pessoal do eleitor para habilitação manual`
- `04/10/2026 06:30:48 VOTA Solicitação de dado pessoal do eleitor para habilitação manual`
- `04/10/2026 07:13:37 VOTA Solicitação de dado pessoal do eleitor para habilitação manual`
- `04/10/2026 07:30:36 VOTA Solicitação de dado pessoal do eleitor para habilitação manual`
- `04/10/2026 08:18:38 VOTA Solicitação de dado pessoal do eleitor para habilitação manual`

### digital_mesario
- `04/10/2026 06:06:22 VOTA Solicita digital do mesário`
- `04/10/2026 06:06:29 VOTA Capturada a digital do mesário`
- `04/10/2026 06:30:58 VOTA Solicita digital do mesário`
- `04/10/2026 06:31:07 VOTA Capturada a digital do mesário`
- `04/10/2026 07:13:45 VOTA Solicita digital do mesário`

### tipo_habilitacao_qualquer
- `04/10/2026 06:02:36 VOTA Tipo de habilitação do eleitor [biométrica]`
- `04/10/2026 06:08:29 VOTA Tipo de habilitação do eleitor [biométrica]`
- `04/10/2026 06:10:44 VOTA Tipo de habilitação do eleitor [biométrica]`
- `04/10/2026 06:12:58 VOTA Tipo de habilitação do eleitor [biométrica]`
- `04/10/2026 06:15:00 VOTA Tipo de habilitação do eleitor [biométrica]`

### solicita_digital
- `04/10/2026 06:01:55 VOTA Solicita digital. Tentativa [1] de [4]`
- `04/10/2026 06:04:11 VOTA Solicita digital. Tentativa [1] de [4]`
- `04/10/2026 06:04:57 VOTA Solicita digital. Tentativa [2] de [4]`
- `04/10/2026 06:05:23 VOTA Solicita digital. Tentativa [3] de [4]`
- `04/10/2026 06:05:39 VOTA Solicita digital. Tentativa [4] de [4]`

### voto_confirmado
- `04/10/2026 06:02:48 VOTA Voto confirmado para [Deputado Federal]`
- `04/10/2026 06:02:59 VOTA Voto confirmado para [Deputado Estadual]`
- `04/10/2026 06:03:04 VOTA Voto confirmado para [Senador]`
- `04/10/2026 06:03:12 VOTA Voto confirmado para [Senador]`
- `04/10/2026 06:03:17 VOTA Voto confirmado para [Governador]`

### encerramento
- `04/10/2026 15:03:20 VOTA Título digitado para encerramento: 003439892453`
- `04/10/2026 15:03:23 VOTA Procedimento de encerramento confirmado`
- `04/10/2026 15:04:14 VOTA Inicio do Encerramento`
- `04/10/2026 08:53:30 VOTA Áudio desativado pelo fim da votação`
- `04/10/2026 11:12:15 VOTA Áudio desativado pelo fim da votação`

## Notas do spike AC 2026

- Pacote por UF traz `-bu.dat`, `-log.jez`, `-rdv.dat`, `-vota.vsc` (sem imgbu neste conjunto).
- Logs internos: `logd.dat` (latin-1) dentro de cada `-log.jez`.
- Tipo biométrico: `Tipo de habilitação do eleitor [biométrica]`.
- Liberação sem reconhecimento digital: fluxo `Solicitação de dado pessoal... habilitação manual` + digital do mesário.
- Mensagem clássica `O eleitor não possui biometria` pode estar ausente; use o fluxo manual como proxy de “sem digital”.

## Próximos passos

- Escalar download para demais UFs e 2º turno.
- Cruzar totais do BU (ASN.1/`-bu.dat`) com habilitações por seção.
- Ajustar fuso (AC UTC-5) se a análise de 17h precisar de hora local oficial vs relógio da urna.
