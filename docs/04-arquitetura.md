# Arquitetura e integração MCP

## Componentes

| Componente | Responsabilidade |
|---|---|
| Vue + TypeScript + Vuetify | Exibir a oferta, coletar o rascunho, iniciar a análise e apresentar os resultados. |
| API Django | Validar a solicitação, coordenar o agente, conferir a resposta e devolver um relatório para a interface. |
| Agente em Python | Extrair condições da divulgação e solicitar dados e simulações ao servidor MCP. |
| Servidor MCP em Python | Oferecer duas ferramentas ao agente. Reutiliza as mesmas regras de simulação do backend. |
| JSON | Guardar ofertas, links, cupons, campanhas e respostas esperadas para avaliação. |

A interface chama a API Django. O agente usa um cliente MCP para pedir ao servidor que execute as regras do checkout. A resposta volta com o trecho da campanha e as simulações de antes e depois. Na versão local revisada, a API usa streams em memória do SDK oficial: cada proposta cria uma sessão cliente/servidor isolada no processo da API. A entrada por módulo também aceita clientes externos por stdio. O adaptador NVIDIA Build interpreta as legendas no modo ao vivo. O orquestrador Python controla as chamadas MCP e valida a saída do modelo. [SDK oficial do MCP](https://github.com/modelcontextprotocol/python-sdk) · [Transportes do cliente MCP](https://py.sdk.modelcontextprotocol.io/client/transports/) · [Vue com TypeScript](https://vuejs.org/guide/typescript/overview.html) · [Vuetify](https://vuetifyjs.com/en/getting-started/installation/)

Python/Django e Vue/Vuetify seguem a referência pública de recrutamento da YouShop em 2024. A vaga de estágio cita Python ou Node.js/TypeScript e coloca MCP entre as atividades. TypeScript com Vue é uma decisão do protótipo. [Anúncio técnico de 2024](https://pt.linkedin.com/posts/youshop-brasil_vemprayoushop-activity-7161392769054162944-misF) · [Descrição da vaga de estágio](https://drive.google.com/file/d/1ax3bbnxQ-KNtgszbVNZTl5LECOgrBpcJ/view)

A [API de simulação implementada](09-api.md) opera sobre uma única oferta fictícia e uma sessão MCP por análise.

## Contratos implementados

| Interface | Entrada | Saída |
|---|---|---|
| `GET /api/demo/` | Nenhum parâmetro obrigatório. | Oferta atual, rascunho de exemplo e campanhas cadastradas. |
| `POST /api/analises/` | Desconto, escopo, instante, validade e legendas opcionais. | Identificador da análise, modo da execução, estado por campanha, evidências e resultados de checkout. |
| MCP `consultar_oferta` | Versão (`atual` ou `proposta`). | Planos, preços, cupons e regras de elegibilidade da versão. |
| MCP `simular_checkout` | Versão, ID da campanha vinculada, plano e cupom opcional. A data pertence ao contexto da análise. | Plano resolvido, status do cupom, motivo, desconto e total em centavos. |

Cada análise trabalha com dois retratos das regras da oferta, um atual e um proposto, delimitados àquela execução. O cliente MCP é criado com esse contexto e o acessa durante a análise. Requisições simultâneas precisam manter os rascunhos separados. Uma versão, link ou plano ausente retorna um motivo explícito para o relatório. Simular ambas as versões na mesma data evita atribuir à alteração um cupom que teria expirado de qualquer forma.

## Dados e responsabilidades

- **Campanha:** identificador, creator fictício, trecho de divulgação, referência do link registrado e cupom opcional. O trecho original permanece disponível para conferência.
- **Oferta:** identificador, versão, planos e preço em centavos. Cada cupom tem código, percentual, planos elegíveis e intervalo de validade, quando configurado.
- **IA:** devolve tipo de condição, referência ao plano ou cupom, valor anunciado quando explícito e trecho de evidência. Pode declarar ambiguidade. A API confere que a evidência existe no texto e valida o formato da saída.
- **Regras:** resolvem o link e o plano, aplicam validade e elegibilidade do cupom, calculam o desconto em centavos e classificam o resultado a partir das duas simulações. Definir arredondamento de metade para cima nos casos com fração de centavo. Datas explícitas usam fuso `America/Sao_Paulo` nos exemplos da demo e um instante com fuso na API.
- **Relatório:** separa a condição extraída, os resultados das ferramentas e a classificação. Ajustar a proposta ou a campanha é decisão do produtor.

## Falhas, privacidade e publicação

Tratar materiais de campanha como dados. As ferramentas aceitam somente parâmetros previstos no esquema e consultam dados da própria demo. Manter credenciais no backend e registrar identificador da análise, ferramenta, duração e resultado, sem gravar chaves ou textos de terceiros nos logs. Colocar limite no tamanho da entrada e na duração de uma análise.

Os caminhos de pagamento e publicação ficam fora da integração MCP do protótipo. Em erro do provedor ou do MCP, mostrar o que falhou e permitir nova tentativa. Preparar uma execução gravada identificada como exemplo para a apresentação. O modo gravado não vale como evidência de uma chamada MCP ao vivo.

## Organização Django

O [roteador do projeto](../backend/config/urls.py) monta a aplicação `simulacoes` em `/api/` com `include()`. O [roteador da aplicação](../backend/simulacoes/urls.py) associa cada caminho à sua view. As views validam a requisição HTTP, `analise.py` coordena a execução e `checkout.py` aplica as regras da oferta. Na pasta `integracoes/`, o contrato de extração, o adaptador NVIDIA e o servidor MCP ficam em módulos distintos. O catálogo está em `dados/` e os testes da aplicação em `tests/`.
