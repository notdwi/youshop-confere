# API de simulação

O produtor pode mudar o desconto e os planos elegíveis sem publicar uma oferta. A API calcula o resultado para o cenário fictício do Curso de Edição de Vídeo. A biblioteca inclui divulgações adicionais para explorar os filtros. Apenas as três campanhas vinculadas ao cenário entram no cálculo.

## Rodar a análise

Inicie Django e Vite conforme o [guia de execução](../README.md#executar-localmente). Use o botão **Simular alteração** ou envie o rascunho diretamente ao Django.

```sh
curl -i http://127.0.0.1:8000/api/analises/ \
  -H 'Content-Type: application/json' \
  --data '{"scope":"Básico","discount":20}'
```

| Campo | Valor aceito |
|---|---|
| `scope` | Uma das strings `"Todos"`, `"Básico"` ou `"Completo"`. |
| `discount` | Inteiro entre 0 e 100, inclusive. |

A propriedade `results` reúne uma entrada por campanha. Cada entrada apresenta o trecho da divulgação em `campaign.quote`, a classificação em `status`, o motivo em `reason` e os totais do checkout em centavos em `before` e `after`.

| Campanha | Resultado com o exemplo acima | Antes | Depois |
|---|---|---:|---:|
| Ana | Impactada pela perda de elegibilidade do cupom no plano Completo | 15920 | 19900 |
| Bruno | Compatível com o preço anunciado para o Básico | 9900 | 9900 |
| Camila | Revisão necessária porque a legenda é ambígua | `null` | `null` |

Envie novamente com `"scope":"Todos"` e o mesmo desconto. O total de Ana volta a 15920 e o resultado passa a compatível. Para verificar a validação do servidor, envie o primeiro exemplo com `"discount":101` e confira a resposta de erro.

## Limites da etapa

O modo gravado reconhece legendas da demo. Uma legenda nova precisa do modo NVIDIA para extração ao vivo. Ambos os modos consultam o servidor MCP por uma sessão em memória na versão local revisada. Cada resposta inclui `analysisId`, `example` e resultados com `details` por condição e `evidence` literal. Resultados preexistentes distinguem um problema anterior de uma mudança introduzida pelo produtor.

O corpo admite também `referenceTime` e `expiresAt` em ISO 8601 com fuso. O instante exato do vencimento ainda aceita o cupom. Omitir a validade preserva a data da oferta atual, enviar `null` remove o vencimento. `texts` mapeia IDs de campanhas incluídas para legendas de até 800 caracteres. Edições valem apenas para aquele rascunho. A API limita o corpo a 16 KiB, duas análises simultâneas por processo e 90 s por análise. Sob carga retorna 429, em falha de integração 502 e em timeout global 504.

## Inicialização e verificação

O frontend consulta `GET /api/demo/` para obter `current`, `initialDraft` e `campaigns`. O campo `inSimulation` indica quais materiais entram no relatório. O Vite encaminha as chamadas de mesma origem ao Django em loopback.

Na pasta `backend`, execute `.venv/bin/python manage.py test`. Os testes exercitam o catálogo, as três classificações, o recálculo e as rejeições de entrada. A API retorna HTTP 400 para contrato inválido, 413 para corpo acima de 16384 bytes, 415 para formato diferente de JSON e 405 para método incompatível.
