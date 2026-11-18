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

Se a YouShop puder disponibilizar eventos e permissões do fluxo, usar como indicador principal **tentativas com falha ao aplicar um cupom anunciado a cada 100 tentativas registradas desse cupom**, considerando campanhas incluídas no piloto. Comparar mudanças semelhantes com e sem a conferência em períodos comparáveis. Acompanhar conversão e volume de chamados relacionados como indicadores auxiliares. Volume de dados e acesso aos vínculos entre oferta, campanha e uso de cupom ainda precisam ser confirmados.
