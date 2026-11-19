# Frontend implementado

O YouShop Confere é um protótipo para produtores conferirem o impacto de uma mudança no checkout sobre campanhas de creators. A interface roda no navegador e envia as propostas à API Django para calcular os valores de checkout e a classificação das campanhas. As campanhas são fictícias. O relatório identifica o modo gravado ou NVIDIA. A biblioteca permite editar o texto das campanhas vinculadas para a simulação atual. O editor de oferta permite testar a validade do cupom e a data do checkout.

## Executar

Inicie a API conforme o [guia de execução](../README.md#executar-localmente). O frontend requer Node.js 20.19+ na linha 20 ou Node.js 22.12 ou superior, com npm.

```sh
cd frontend
npm ci
npm run dev
```

Abra [http://127.0.0.1:5173/](http://127.0.0.1:5173/). O Vite escuta na interface de loopback. Para verificar os tipos e gerar o bundle estático, rode `npm run build`. O resultado fica em `frontend/dist/`.

## Fluxos que funcionam

- **Simulação.** A tela começa com um cenário preenchido. No exemplo, o cupom de 20% deixa de valer no plano Completo se o produtor restringir a oferta ao plano Básico. O relatório mostra as três campanhas, o preço antes e depois e a evidência que explica cada estado. Edite o desconto ou os planos e clique em **Simular alteração**. Ao editar, o relatório identifica que ainda corresponde à última simulação. **Restaurar exemplo** repõe as condições originais da demo.
- **Campanhas.** A biblioteca contém sete divulgações fictícias. As três usadas na simulação são marcadas na lista. Busca por creator, canal ou texto e filtro por canal podem ser combinados. O botão no rodapé leva de volta à simulação.
- **Navegação móvel.** O menu abre pela direita, mantém parte da página visível e fecha ao selecionar uma opção, tocar fora ou pressionar Escape. O rodapé da gaveta mostra o logo e identifica o ambiente de demonstração. No desktop, o menu fica na lateral. As duas telas usam rolagem normal da página quando o conteúdo não cabe na janela.

## Onde cada responsabilidade fica

| Arquivo ou pasta | Responsabilidade |
|---|---|
| [`frontend/src/App.vue`](../frontend/src/App.vue) | Tela ativa, rascunho da oferta e último resultado da simulação. |
| [`frontend/src/components/`](../frontend/src/components/) | Estrutura de página, navegação, assinatura visual, editor, resumo, lista de resultados e biblioteca de campanhas. |
| [`simulation.ts`](../frontend/src/domain/simulation.ts) | Tipos da simulação e formatação de preços para exibição. |
| [`campanhas.json`](../backend/simulacoes/dados/campanhas.json) | Catálogo com os casos simuláveis e os exemplos adicionais da biblioteca. |
| [`style.css`](../frontend/src/style.css) | Paleta, tipografia, espaçamento e regras de adaptação a telas menores. |
| [`vite.config.ts`](../frontend/vite.config.ts) | Proxy para a API Django e cabeçalhos do servidor local. |

Os preços são tratados em centavos e formatados em reais para exibição. A página mostra legendas fictícias como texto. A demo não solicita dados de compradores, não envia cobranças e não publica alterações em ofertas reais.

## Conferência manual

1. Na Simulação, abra a evidência de Ana Martins e confirme a mudança de R$ 159,20 para R$ 199,00.
2. Em **Oferta proposta**, selecione **Básico e Completo** e rode a simulação. O cupom de 20% volta a valer para Ana.
3. Abra **Campanhas**, filtre por TikTok e confira os dois exemplos. Limpe o filtro e volte à simulação.
4. Em uma janela estreita, abra o menu, navegue entre as telas e confira o fechamento por Escape e pelo clique fora.

Os fluxos foram conferidos no navegador durante o desenvolvimento. O [plano de validação](05-validacao.md) registra os testes e a avaliação de impacto previstos para a integração completa.

## Referências visuais

[Tour do dashboard YouShop](https://ajuda.youshop.co/guides/8170efc4-734d-4d5a-b50f-1f2e7b5bdd96) · [Guia do app YouShop Creators](https://ajuda.youshop.co/guides/IQ2WaPblIMMUqNhDSKdY) · [Logo publicada pela YouShop](https://www.youshop.co/assets/6cce18366f25af03e80ae1d0e4229c67e89feaf4-DYZdzxFX.png) · [Dashboard do Haunt](https://haunt.gg/dashboard).
