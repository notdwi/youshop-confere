# YouShop Confere

Protótipo para o Desafio de Inovação do Programa de Estágio YouShop 2027. O Confere ajuda produtores a testar mudanças de oferta antes de publicar e a descobrir quais campanhas de creators precisam ser atualizadas.

Imagine que um creator anunciou 20% de desconto no curso completo. Na oferta proposta, o cupom só vale para o plano básico. O Confere mostra o trecho da divulgação, simula o checkout e aponta a diferença. O produtor ajusta a oferta ou a campanha e testa novamente.

A versão atual tem **frontend Vue, TypeScript e Vuetify**, com dados fictícios e uma simulação local. As duas telas permitem editar condições da oferta, conferir o impacto no checkout e consultar campanhas. O backend Django e a integração MCP estão descritos no plano de arquitetura.

## Prévia local

Use Node.js 20.19+ na linha 20 ou 22.12 ou superior.

```sh
cd frontend
npm ci
npm run dev
```

Abra [http://127.0.0.1:5173/](http://127.0.0.1:5173/). Use `npm run build` para verificar os tipos e gerar a versão estática.

Referências visuais: [tour do painel da YouShop](https://ajuda.youshop.co/guides/8170efc4-734d-4d5a-b50f-1f2e7b5bdd96) e [logo oficial da YouShop](https://www.youshop.co/assets/6cce18366f25af03e80ae1d0e4229c67e89feaf4-DYZdzxFX.png) e [dashboard do Haunt](https://haunt.gg/dashboard).

| Documento | Para que serve |
|---|---|
| [Frontend implementado](docs/08-frontend.md) | Telas, regras da demo, estrutura do código e como verificar. |
| [Briefing do desafio](docs/01-desafio.md) | Requisitos do edital, formato da entrega e relação com a vaga. |
| [Diagnóstico e fontes](docs/02-diagnostico.md) | Evidências, originalidade, alternativas e perguntas de pesquisa. |
| [Especificação do protótipo](docs/03-especificacao.md) | Usuário, fluxo, escopo, cenários e critérios de aceite. |
| [Arquitetura e integração MCP](docs/04-arquitetura.md) | Componentes, contratos, regras de negócio e limites da IA. |
| [Plano de validação](docs/05-validacao.md) | Casos de teste, comparação com revisão manual e métricas de piloto. |
| [Plano de execução](docs/06-plano.md) | Etapas, entregáveis e critérios para avançar. |
| [Roteiro da apresentação](docs/07-apresentacao.md) | Ordem dos slides, rascunho do pitch e demonstração. |
