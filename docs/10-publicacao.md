# Publicação

[Demo pública](https://youshop.noctyra.lol) · [Endereço alternativo do Pages](https://youshop-confere.pages.dev)

O projeto Cloudflare Pages `youshop-confere` está conectado diretamente ao repositório público `notdwi/youshop-confere`. Um push na `main` aciona a instalação e o build na Cloudflare. A raiz é `frontend`, o comando é `npm run build` e a saída é `dist`. O histórico de builds fica em Deployments no Pages. A variável pública de build `VITE_API_ORIGIN` contém apenas a origem HTTPS da API. Localmente, quando a variável está vazia, o Vite encaminha `/api/` ao Django.

A API roda no Termux dentro do ambiente Python `youshop-confere` e escuta em loopback na porta 18764. Um Cloudflare Tunnel dedicado publica `confere-api.noctyra.lol`. A chave NVIDIA é lida exclusivamente no servidor. Os serviços runit `youshop-api`, `youshop-tunnel` e `youshop-sync` mantêm a aplicação, o túnel e a sincronização ativos. O sincronizador verifica a main a cada 90 segundos com uma chave de deploy de leitura. Uma atualização com mudança de backend requer instalação das dependências, testes e reinício do processo. Os logs do projeto ficam no diretório logs do usuário Termux, com o prefixo youshop.

Para verificar a disponibilidade, abrir a demo em janela privada, executar uma simulação e expandir uma evidência. A API pública deve responder também a `GET /api/demo/`. Para diagnóstico no telefone, usar `sv status "$PREFIX/var/service/youshop-api" "$PREFIX/var/service/youshop-tunnel" "$PREFIX/var/service/youshop-sync"`. O celular precisa permanecer ligado, conectado à internet e com os processos Termux ativos para executar as análises. O frontend continua servido pelo Pages se o telefone ficar indisponível.

Este deploy usa arquivos estáticos, integração Git nativa do Pages e um Tunnel. O tráfego estático não invoca Pages Functions. A cota e a disponibilidade da NVIDIA aplicam-se separadamente. A renovação do domínio segue a contratação existente. [Integração Git](https://developers.cloudflare.com/pages/configuration/git-integration/) · [Preços do tráfego estático](https://developers.cloudflare.com/pages/functions/pricing/)
