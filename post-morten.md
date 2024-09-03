# Incidente aumento de custos nas contas AWS

Essa página contém o post mortem do problema do microsserviço `XPTO` relacionado a finops ocorrido na release 1 durante a sprint 1 do ano de 2024.

## Informações Importantes

**Data:** 30/08/2024

**Autores:**

Squad `Nome Squad back-end`: Danilo

Squad `Nome Squad SRE`: João

**Status:** Concluído, itens de ação em andamento

**Resumo:**
Geração de custos excessivos nas contas que suportam os microsserviço `XPTO` devido a alta geração de logs sendo ingeridos pelo cloud watch.

**Duração do problema:**

Os custos aumentaram desde o dia 09/08/2024 nas contas de desenvolvimento, homologação e produção e normalizaram dia 30/08/2024.

**Impacto:**

Impacto no finops, o custo diário com Cloud Watch considerando um cenário normal de ingestão é de 100 dólares, durante o período de impacto os custos ficaram com uma média de 250 dólares totalizando 3.150 doláres adicionais. Durante o problema não houve impacto em funcionalidades apra o cliente final.

**Causa Raiz:**

Identificado que após o dia 09/08/2024 foi implantado a versão `2.0.0` do microsserviço `XPTO` no qual foi inserido um bug no ambiente.

**O que desencadeou:**

Foi desencadeado por um deploy no dia 09/08/24 (`ID da Change`) onde foi realizado o rollout do microsserviço `XPTO` para a versão `2.0.0`.

**Detecção:**

Detecção manual através do time de SRE estava buscando por oportunidades de redução de custos durante o On-Call.

**Resolução:**

_Pontual_

Após identificar que o microsserviço `XPTO` estava gerando logs de forma atípica foi implementado um filtro no fluentbit (addon que faz shipping de logs) para que os logs gerados não fossem enviados para o backend que nesse caso era o serviço AWS Cloud Watch.

_Definitiva_

Será implementado um fix no microsserviço `XPTO` para implementação de sampling de logs através da lib zap utilizada para geração dos logs, sendo assim sempre será enviado apenas uma amostragem dos logs gerados, em caso de bugs similares não será gerado o mesmo impacto nos ambientes.

## Lições aprendidas

**Coisas que correram bem**

- Aplicação de uma medida paliativa com tempestividade uma vez que o problema foi identificado

**Coisas que correram mal**

- Não houve um processo de validação de change efetivo pós implementação
- Não haviam alertas de custos nas contas AWS
- Não houve um processo de validação nos ambientes de desenvolvimento e homologação
- Falta de testes automatizados
- Não havia alerta para detecção de anomalia nas contas AWS
- Não havia alertas para alta ingestão de logs no Cloud Watch

**Onde tivemos sorte?**

- Detecção manual através investigação de oportunidades de finops realizadas de forma periódica

**Itens de ação:**

**Prevenção/Mitigação de riscos**

| **Ação**                              | **Tipo** | **Componente** | **Prioridade** | **Proprietário** |
| ------------------------------------- | -------- | -------------- | -------------- | ---------------- |
| Implementação de testes automatizados | mitigar  | `XPTO`         | P2             | Danilo           |
| Implementar probes do kubernetes      | mitigar  | `XPTO`         | P1             | Danilo           |

**Monitoramento/Alertas**

| **Ação**                                                | **Tipo** | **Componente** | **Prioridade** | **Proprietário** |
| ------------------------------------------------------- | -------- | -------------- | -------------- | ---------------- |
| Criar alertas de custos nas contas AWS                  | evitar   | monitoria      | P0             | João             |
| Criar alertas para alta ingestão de logs do Cloud Watch | evitar   | monitoria      | P0             | João             |
| Criar alertas para detecção de anomalia nas contas AWS  | mitigar  | monitoria      | P1             | João             |

**Processos/Resposta de incidentes**

| **Ação**                                                          | **Tipo** | **Componente** | **Prioridade** | **Proprietário** |
| ----------------------------------------------------------------- | -------- | -------------- | -------------- | ---------------- |
| criar runbooks operacionais para validação do ambiente pós change | mitigar  | N/A            | P0             | João / Danilo    |

## Timeline

09/08/2024

- Executado a change `ID da Change` para atualização do microsserviço `XPTO` para versão `2.0.0`

30/08/2024
Manhã:

- João da squad `squad SRE` estava buscando por oportunidades de finops nas contas AWS
- João percebeu a anomalia nos custos de Cloud Watch nas contas de produção
- João encontrou uma query nas documentações da AWS para localizar os log groups com maior volume de ingestão diária
- João acionou o Danilo da squad `squad backend` para iniciar um troubleshooting mais focado no microsserviço `XPTO`
- Identificado que o alto volume de ingestão de logs iniciou após a change `ID da Change`
- João adicionou um filtro no fluentbit para exclusão do envio dos logs do microsserviço `XPTO` para o Cloud Watch
- Identificado que o impacto foi mitigado pois os logs deixaram de ser registrados no log group

## Evidências

Hisórico de consumo do Cloud Watch na conta de produção

`Adicionar prints`

Hisórico de consumo do Cloud Watch na conta de homologação

`Adicionar prints`

Hisórico de consumo do Cloud Watch na conta de desenvolvimento

`Adicionar prints`
