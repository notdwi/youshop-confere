# Plano de validação

## O que será testado

O teste do protótipo mede se o Confere identifica quando uma alteração rompe uma condição divulgada. O resultado esperado de cada caso é definido antes da execução. Os casos abaixo são planejados e usam dados fictícios.

| Caso | Resultado esperado |
|---|---|
| Cupom de 20% permanece elegível no plano divulgado | Compatível. |
| Mesmo código, mas desconto cai de 20% para 10% | Impactada. |
| O cupom deixa de aceitar o plano Completo | Impactada, com motivo de elegibilidade. |
| O rascunho adianta o fim do cupom e o instante fica fora da nova validade | Impactada, com motivo de validade. |
| O cupom já estava inválido nas duas versões | Divergência preexistente. |
| O rascunho recupera uma elegibilidade que estava incorreta | Compatível, com indicação de correção. |
| Preço anunciado em texto continua em R$ 99 | Compatível. |
| “Um quinto de desconto” e “20% de desconto” em campanhas equivalentes | Extrair o mesmo percentual e obter o mesmo resultado. |
| “Até 20%” sem indicação clara de plano ou condição aplicável | Revisão necessária se o material não permitir determinar o cenário. |
| “Condição especial” sem benefício nem valor | Revisão necessária. |
| Link cadastrado sem vínculo com a oferta analisada | Revisão necessária, com indicação do vínculo ausente. |
| O servidor MCP ou o modelo deixa de responder | Erro visível e tentativa de novo. Excluir o caso dos resultados de classificação e relatar a falha. |

Testar ainda arredondamento em centavos, limite do horário da oferta, separação entre rascunhos simultâneos e correção seguida de novo teste. Para a integração MCP, descobrir as duas ferramentas com um cliente real e verificar a resposta estruturada do servidor. Para a IA, incluir textos que mencionam preços de outros planos para verificar uso do contexto correto.

## Comparação

1. Definir rótulos com base na configuração da oferta e na legenda. Guardar um grupo de casos sem usar no ajuste do prompt.
2. Dar à revisão manual e à ferramenta as mesmas informações. Registrar tempo por caso, classificação e justificativa. Se a mesma pessoa preparar os casos e revisar os resultados, declarar essa limitação.
3. Comparar a leitura da IA com uma busca simples por percentuais, preços e códigos em um subconjunto de legendas. Isso ajuda a demonstrar em quais textos interpretar contexto melhora o resultado.
4. Relatar números absolutos, denominadores, erros e casos inconclusivos. Em uma amostra pequena, apresentar resultado como teste funcional exploratório.

| Métrica | Cálculo |
|---|---|
| Detecção de divergências novas | Campanhas impactadas corretamente sinalizadas ÷ campanhas com divergência nova conhecida. |
| Falsos alertas | Campanhas compatíveis sinalizadas como impactadas ÷ campanhas sabidamente compatíveis. |
| Tempo de revisão | Mediana do tempo para concluir cada análise, incluindo conferência humana necessária. |
| Casos inconclusivos | Análises com revisão necessária ÷ análises concluídas. Registrar o motivo de cada uma. |

O caso principal da demo é considerado aprovado quando acusa o cupom incompatível, cita o texto correto, mostra o total das duas versões e confirma o ajuste na segunda execução. Os exemplos compatível e ambíguo precisam permanecer distintos. Se o modelo alterar a faixa de desconto, inventar evidência ou confundir o plano, registrar o erro e ajustar antes de usar o fluxo na apresentação.

## Como medir num piloto futuro

Se a YouShop puder disponibilizar eventos e permissões do fluxo, usar como indicador principal **tentativas com desconto aplicado abaixo do prometido a cada 100 tentativas de usar o cupom no plano anunciado**, considerando campanhas incluídas no piloto. Comparar mudanças semelhantes com e sem a conferência em períodos comparáveis. Acompanhar conversão e volume de chamados relacionados como indicadores auxiliares. Volume de dados e acesso aos vínculos entre oferta, campanha e uso de cupom ainda precisam ser confirmados.

## Avaliação executada em 19/11/2026

Modelo NVIDIA Nemotron 3.5 Bolt. Executamos propostas pelo POST real, com leitura ao vivo e checkout via MCP. Os [12 casos principais](../backend/avaliacao/casos.tsv) e os [6 de reserva](../backend/avaliacao/reserva.tsv) incluem desconto por extenso, preço antigo e atual, múltiplas promessas, plano incompatível, cupom desconhecido e texto ambíguo. O gabarito fixa classificação e totais em centavos antes de cada conjunto ser enviado. A conferência exige também uma evidência literal; no caso da campanha com duas promessas exige os dois estados no detalhe.

- Na primeira execução, seis dos doze casos passaram. Dois lotes de três tiveram erro de integração. Uma nova execução intermediária expôs a leitura de R$ 99 como 99 centavos.
- Ajustamos as instruções e a temperatura, conferimos o valor extraído quando a evidência tem um preço explícito em reais e limitamos a uma nova tentativa quando o conteúdo não passa na validação. Falhas HTTP continuam visíveis e o prazo global continua valendo.
- Depois dos ajustes, duas execuções dos doze casos principais passaram integralmente. Os seis casos de reserva passaram antes e depois do ajuste final. São 18 exemplos fictícios distintos, com três vínculos de campanha; repetições não aumentam o tamanho da amostra. O conjunto principal orientou ajustes. O teste de evidência literal verifica a presença do trecho; isoladamente, não prova compreensão semântica.
- O backend passou em dez testes automatizados. O build do frontend passou. No navegador exercitamos uma simulação real, a abertura da evidência, o filtro de canal, a navegação a 360 px e a exibição de erro com uma resposta HTTP 502 simulada.
- Os resultados não medem prevalência da dor, redução de abandono ou precisão em campanhas reais. O serviço externo pode variar; em erro a aplicação permite tentar novamente.

Para repetir com a API local em modo NVIDIA, execute a partir da raiz (usa a cota do provedor):

```sh
python3 backend/avaliacao/executar.py
python3 backend/avaliacao/executar.py --conjunto reserva
```
