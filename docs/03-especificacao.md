# Especificação do protótipo

## Usuário e objetivo

O produtor quer alterar o preço ou as regras de um cupom sem surpreender compradores que chegam por campanhas já publicadas. O Confere devolve uma lista das campanhas cadastradas e explica como cada uma se comportaria no checkout proposto.

## Fluxo

1. O produtor abre uma oferta fictícia e vê sua versão atual e as campanhas vinculadas.
2. Ele prepara um rascunho de alteração, por exemplo restringe o cupom ao plano básico.
3. O agente analisa as legendas cadastradas e extrai a condição anunciada, citando as palavras que a sustentam.
4. Pelas ferramentas MCP, o agente consulta a oferta e simula o mesmo cenário de compra antes e depois da alteração.
5. A interface mostra o que a campanha promete, os resultados das duas versões e o motivo do alerta. O produtor pode editar o rascunho ou o material cadastrado e testar novamente.

## Escopo da primeira versão

Um produto digital fictício com plano Básico e Completo, duas versões da oferta, valores em reais e três campanhas em texto. Testar o vínculo entre link, plano, preço, validade do cupom e desconto. A tela compara o antes e o depois, abre o detalhe de cada resultado e oferece nova simulação após ajuste.

Os materiais entram por cadastro de exemplo ou texto fornecido pelo usuário. Publicações externas, leitura de vídeos, assinaturas, meios de pagamento reais e atualização automática de conteúdo ficam fora desta versão.

| Campanha | Informação disponível | Resultado esperado com o rascunho |
|---|---|---|
| Ana | “Use ANACURSO e pague 20% a menos no plano Completo.” | **Impactada.** O cupom funcionava no plano Completo e deixa de ser aplicável. |
| Bruno | “Com meu link, o plano Básico sai por R$ 99.” | **Compatível.** O preço no plano Básico continua em R$ 99. |
| Camila | “Tem uma condição especial se você entrar hoje.” | **Revisão necessária.** A condição anunciada não informa benefício suficiente para comparar. |

Na demo, o plano Completo custa R$ 199,00 e sai por R$ 159,20 com 20% de desconto. Se o cupom deixa de valer, o Confere mostra os dois valores e a regra de elegibilidade que mudou. Restaurar a elegibilidade no rascunho deve deixar a campanha compatível. Todos os nomes, preços e resultados desse cenário são fictícios.

## Resultados possíveis

| Estado | Quando usar |
|---|---|
| `impactada` | A condição anunciada era atendida na oferta atual e passa a divergir no rascunho. |
| `compativel` | A condição está clara e o rascunho continua atendendo ao que foi divulgado. |
| `divergencia_preexistente` | A condição já divergia na oferta atual e continua divergindo. A mudança proposta não recebe a causa desse problema. |
| `revisao_necessaria` | O texto é ambíguo, falta vínculo ou há informação insuficiente para concluir. |

Se a alteração corrigir uma divergência antiga, mostrar `compativel` e indicar que o rascunho corrigiu a situação. Se não houve condições claras para rodar os dois cenários, mostrar o que falta. Uma campanha com várias condições fica impactada quando pelo menos uma divergência nova é confirmada; qualquer condição ainda incerta aparece no detalhe.

## Critérios de aceite

- Distinguir as três campanhas do exemplo e apresentar os resultados esperados.
- Mostrar a evidência em texto e os dados da simulação, com valores de antes e de depois quando houver diferença.
- Corrigir a proposta e rodar novamente, preservando a oferta original da demo.
- Registrar chamadas MCP reais no fluxo com IA. A interface identifica o exemplo gravado quando usá-lo como alternativa de demonstração.
- Exibir estado de erro se a integração falhar. Uma falha da ferramenta não conta como campanha compatível.
- Executar o fluxo completo em um ambiente de teste com dados fictícios e sem gerar pedidos ou cobranças.
