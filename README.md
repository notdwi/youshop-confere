# YouShop Confere

Protótipo para o Desafio de Inovação do Programa de Estágio YouShop 2027. O Confere ajuda produtores a testar mudanças de oferta antes de publicar e a descobrir quais campanhas de creators precisam ser atualizadas.

Imagine que um creator anunciou 20% de desconto no curso completo. Na oferta proposta, o cupom só vale para o plano básico. O Confere mostra o trecho da divulgação, simula o checkout e aponta a diferença. O produtor ajusta a oferta ou a campanha e testa novamente.

A interface Vue, TypeScript e Vuetify envia o desconto e os planos elegíveis para uma API Django. O servidor valida o rascunho e calcula o impacto nas três campanhas fictícias. O servidor consulta e simula o checkout por MCP nas duas modalidades. A demonstração local usa extrações gravadas. Para interpretar novas legendas ao vivo, configure o modelo e a chave NVIDIA conforme o [guia de IA](docs/AI-SPEC.md).

## Executar localmente

Em um terminal, a partir da raiz do projeto, prepare o ambiente Python e inicie a API.

```sh
cd backend
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python manage.py runserver 127.0.0.1:8000
```

Em outro terminal, a partir da raiz, inicie o frontend com Node.js 20.19+ na linha 20 ou 22.12 ou superior.

```sh
cd frontend
npm ci
npm run dev
```

Abra [o Confere no navegador](http://127.0.0.1:5173/). O Vite encaminha as chamadas a `/api/` para o Django. Mantenha os dois processos ativos durante a demonstração.

Referências visuais: [tour do painel da YouShop](https://ajuda.youshop.co/guides/8170efc4-734d-4d5a-b50f-1f2e7b5bdd96) e [logo oficial da YouShop](https://www.youshop.co/assets/6cce18366f25af03e80ae1d0e4229c67e89feaf4-DYZdzxFX.png) e [dashboard do Haunt](https://haunt.gg/dashboard).

| Documento | Para que serve |
|---|---|
| [Frontend implementado](docs/08-frontend.md) | Telas, regras da demo, estrutura do código e como verificar. |
| [API de simulação](docs/09-api.md) | Contrato HTTP, validação e resultados esperados para o exemplo. |
| [Briefing do desafio](docs/01-desafio.md) | Requisitos do edital, formato da entrega e relação com a vaga. |
| [Diagnóstico e fontes](docs/02-diagnostico.md) | Evidências, originalidade, alternativas e perguntas de pesquisa. |
| [Especificação do protótipo](docs/03-especificacao.md) | Usuário, fluxo, escopo, cenários e critérios de aceite. |
| [Arquitetura e integração MCP](docs/04-arquitetura.md) | Componentes, contratos, regras de negócio e limites da IA. |
| [Plano de validação](docs/05-validacao.md) | Casos de teste, comparação com revisão manual e métricas de piloto. |
| [Plano de execução](docs/06-plano.md) | Etapas, entregáveis e critérios para avançar. |
| [Roteiro da apresentação](docs/07-apresentacao.md) | Ordem dos slides, rascunho do pitch e demonstração. |

A [apresentação em PDF](docs/apresentacao/confere.pdf) sintetiza o problema, a demonstração e os critérios de avaliação.

Para continuar de onde a implementação parou, consulte o [registro de retomada](docs/RETOMADA.md).
