# Plano de execução

O cronograma usa etapas e dependências com prazo final confirmado em 22/11/2026 às 23h59. A prioridade é um fluxo completo com três campanhas e uma apresentação que explique o problema, a decisão e o teste.

| Ordem | Trabalho | Pronto quando |
|---|---|---|
| 1 | Organizar a base do projeto. Fixar versões compatíveis, escolher o provedor de IA e preparar o conjunto fictício. | As três campanhas têm texto, oferta, referência de link, alterações e resultados esperados. |
| 2 | Implementar as regras de oferta no backend. | Simular a versão atual e a proposta produz os valores esperados para plano, preço e cupom. Os testes distinguem erro, divergência nova e preexistente. |
| 3 | Implementar o servidor MCP e a API. Integrar a extração do modelo. | Um cliente real descobre e chama as duas ferramentas. A API devolve evidência citada e resultados conferíveis. |
| 4 | Montar a interface Vue. | O produtor consegue alterar o rascunho, rodar uma análise, revisar a evidência e simular novamente após corrigir. |
| 5 | Executar o plano de validação e coletar evidências para a apresentação. | Resultados e limitações estão documentados. O fluxo de demonstração pode ser repetido com o mesmo cenário de entrada. |
| 6 | Preparar e revisar a entrega. | Slides com pitch na abertura, arquivos e links revisados, protótipo identificável como demo e formulário localizado no e-mail. |

A pesquisa exploratória pode ocorrer em paralelo às etapas 1 a 4. Se a validação trouxer um fluxo diferente, ajustar o cenário antes de concluir a interface. Se o tempo ficar curto, preservar a demonstração de antes/depois e a verificação MCP. A prova de conceito pode usar campanhas já carregadas e uma única edição de oferta. Uma gravação curta do mesmo cenário dá apoio à demonstração quando a conexão estiver indisponível.

## Pendências para a entrega

- Enviar até 22/11/2026 às 23h59 pelo [formulário da YouShop](https://go.youshop.com.br/QJMPLSBWYM).
- Completar o pitch com um episódio da experiência do candidato e revisar a atribuição do trabalho em equipe.
- Registrar entrevistas caso aconteçam e atribuir corretamente o que veio da documentação, de conversas e da simulação.
- Testar a abertura do PDF e do link da demo em uma sessão independente. Confirmar que a demonstração não exige credencial pessoal do avaliador.
- Revisar textos e imagens para manter o exemplo fictício explícito e remover qualquer dado pessoal ou credencial.

O fluxo de interface, API e MCP está integrado. A configuração NVIDIA e a avaliação do modo ao vivo estão no [contrato de IA](AI-SPEC.md). Pesquisa com participantes e medição de impacto em produção continuam como etapas de um piloto.
