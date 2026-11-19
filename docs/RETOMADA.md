# Entrega do YouShop Confere

**Única pendência:** enviar a [apresentação](apresentacao/confere.pdf) e o [link da demo](https://youshop.noctyra.lol/) pelo [formulário oficial](https://go.youshop.com.br/QJMPLSBWYM) até 22/11/2026 às 23h59.

Os registros abaixo descrevem etapas anteriores do projeto.

## Retomada do YouShop Confere • 18/11/2026

O trabalho de backend, integração e apresentação está no diretório local. O último commit confirmado anteriormente na main é 7757073, referente ao menu mobile. O candidato pediu autorização expressa antes de enviar qualquer alteração ao Git. Preservar o trabalho local.

## Fechamento de 18/11/2026 e prazo confirmado

O e-mail do Time de Pessoas informa entrega até **domingo, 22/11/2026, às 23h59**, pelo [formulário oficial](https://go.youshop.com.br/QJMPLSBWYM). Em 18/11 estávamos dentro do prazo. O e-mail não explicita o fuso. Planejar o envio até sábado, 21/11, deixa margem para corrigir problemas de acesso. Entregas atrasadas implicam reprovação automática. [Instruções enviadas pela YouShop](https://go.youshop.com.br/1FQHCHRSEJ)

O RH também pediu confirmação de recebimento e participação. Gean deve conferir se já respondeu. Não há registro de submissão do projeto. A apresentação está em [PDF](apresentacao/confere.pdf), com nove slides. As alterações seguem locais. Qualquer envio ao Git depende de autorização.

**Ordem de retomada sugerida**

1. **Viabilizar o acesso da banca.** Escolher com Gean uma demo acessível externamente ou uma simulação compartilhável. Conferir em janela anônima e em outra rede. Antes de qualquer demo pública com inferência ao vivo, substituir a chave compartilhada e definir limites de uso.
2. **Testar o ponto de maior incerteza.** Rotular antes do teste 8 a 12 legendas inéditas, incluindo preço antigo e novo no mesmo texto, desconto por extenso e benefício ambíguo. Registrar acertos, falsos alertas e casos enviados para revisão. Conferir se a frase citada sustenta o valor extraído. O teste existente com três campanhas fictícias confirma o fluxo; o desempenho com novas legendas continua em aberto.
3. **Fortalecer o diagnóstico se houver tempo.** Pedir a um produtor ou creator um exemplo real de alteração de oferta e registrar o que aconteceu. Diferenciar observação, hipótese e impacto medido.
4. **Finalizar a apresentação.** Atualizar o slide 8 com os resultados realmente observados, validar a autoria e os fatos do pitch com Gean, incluir o link da demo e revisar a exportação final. Guardar o comprovante após o envio pelo formulário.
5. **Refinamento técnico opcional.** Aproveitar os dados retornados por consultar_oferta para explicar a regra alterada. Hoje a classificação já usa os dois checkouts simulados por MCP. Priorizar avaliação e acesso da banca antes de ampliar funcionalidades.

Para reiniciar os dois serviços, seguir o [README](../README.md#executar-localmente). A configuração local ativa usa nvidia/nemotron-3.5-bolt-e4b. A [documentação HTTP](09-api.md) cobre a consulta do exemplo e o envio de análises. Entre os últimos ajustes visuais estão o aviso no canto superior direito que fecha ao navegar, o foco interno no campo de desconto e o alinhamento das divisórias em Campanhas.

## Estado funcional

Vue carrega a demonstração do Django. A biblioteca permite editar legendas no rascunho. A API valida a entrada e cria uma sessão MCP via stdio para cada análise. O orquestrador descobre as ferramentas, consulta a oferta e simula as versões atual e proposta. O checkout verifica plano, cupom, desconto e validade. O relatório contém os totais em centavos, motivo, trecho literal e identificador da análise.

O modo recorded roda sem chave, com extrações pré-definidas e chamadas MCP reais. O fluxo foi verificado no navegador em desktop e em largura de 360 px. O modo nvidia envia um lote de legendas ao provedor e valida o esquema e a presença literal da evidência. A integração HTTP do provedor foi testada com respostas simuladas. Latência e qualidade do Kimi ao vivo ainda estão por medir.

## Verificações repetíveis

Na pasta backend, executar `.venv/bin/python manage.py test`. Na pasta frontend, executar `npm run build`. O cenário principal mostra Ana passando de R$ 159,20 para R$ 199,00, Bruno permanecendo em R$ 99,00 e Camila exigindo revisão. Esses resultados são fictícios. A redução de chamados ou abandono ainda é hipótese de piloto.

Atualização posterior: o modo local ativo é NVIDIA com nvidia/nemotron-3.5-bolt-e4b. Um teste ao vivo do fluxo com as três legendas em português e chamadas MCP levou 2,5 segundos e obteve as três classificações esperadas. O Kimi respondeu à API, mas houve também formato inválido e timeout. A chave está apenas na configuração local ignorada pelo Git. Esta medição isolada não estima a latência em horários de pico.

A interface identifica exemplos gravados pelo campo booleano example. Os detalhes do provedor ficam no backend. O botão de simulação mostra o progresso, o formulário mantém o foco dentro dos campos e as ações de edição, restauração e simulação têm confirmação visual.

Confirmado no navegador: o aviso de sucesso usa o componente VSnackbar registrado e fecha ao trocar de tela. Uma simulação que termina enquanto o usuário está em Campanhas também não abre o aviso nessa tela.

## Conferência da entrega com o PDF original da YouShop

A missão é propor uma aplicação incomum de IA a um problema relevante do ecossistema. O Confere atende à missão ao comparar uma promessa já publicada com o checkout antes e depois de uma mudança proposta. A área é Atendimento ao produtor. O uso real das ferramentas MCP também demonstra a competência da vaga de desenvolvimento.

| Pergunta da banca | Onde está respondida |
|---|---|
| Problema e público | Slide 2, produtor, creator e comprador |
| Por que Gean | Slide 1, gateways de pagamento e colaboração no chat de IA |
| Origem do diagnóstico | Slide 3, guias e pesquisa documental |
| Importância e perdas | Slides 2 e 3, frustração de preço e hipótese de retrabalho e abandono |
| Solução e papel da IA | Slides 4 a 6, extração literal, checkout por MCP e revisão humana |
| Alternativas descartadas | Slide 7, briefing, auditoria isolada e monitoramento de cupom |
| Métrica de sucesso | Slide 8, falhas por 100 tentativas de aplicar o cupom |
| Limites e ética | Slide 9, cobertura, autorização, dados fictícios e decisão humana |

Formato conferido: PDF de nove slides, pitch na abertura, solução nomeada. Os seis critérios têm material na apresentação. O diagnóstico tem respaldo documental, mas a frequência e o custo da dor na YouShop permanecem hipóteses. O teste funcional de três casos registrado acima demonstra viabilidade. O slide 8 ainda descreve esse teste no futuro; vale incorporar o resultado observado e explicitar o tamanho da amostra.

Antes do envio: disponibilizar um link da demo ou simulação acessível à banca e testá-lo fora da rede local; validar o pitch pessoal com Gean; enviar pelo formulário até 22/11/2026 às 23h59. Para fortalecer o diagnóstico, se houver tempo, registrar um caso concreto relatado por um produtor ou creator, com autorização. Entrevista e medição em produção não são requisitos formais do PDF.
Encerramento verificado em 18/11: Django e as duas instâncias do Vite foram desligados. Portas 8000 e 5173 livres.

Em 19/11 o backend foi reorganizado em config/ e simulacoes/. A API conserva os caminhos GET /api/demo/ e POST /api/analises/. A suíte Django executou oito testes com sucesso, incluindo o fluxo pelo novo módulo MCP. Os comandos de inicialização seguem no README.

19/11: avaliação ao vivo com 18 legendas fictícias, duas falhas corrigidas e dez testes de backend aprovados. Ver [avaliação e reprodução](05-validacao.md#avaliação-executada-em-19112026).

19/11: apresentação revisada para dez slides após pesquisa de pitch e evidência externa. Versão atual e mapa das oito perguntas em docs/07-apresentacao.md. Para submissão, falta o endereço da demo acessível à banca.

19/11: demo publicada em https://youshop.noctyra.lol com frontend no Pages e Django/MCP via Termux. O teste pelo navegador público retornou as três classificações com IA ao vivo. O favicon usa a marca da YouShop. Consultar docs/10-publicacao.md.

## Pausa após publicar • 19/11/2026

O frontend está publicado em https://youshop.noctyra.lol, com favicon da YouShop, pipeline Git nativa na main e backend público em https://confere-api.noctyra.lol. Pelo navegador externo, a simulação ao vivo retornou HTTP 200 e as três classificações esperadas. O repositório permanece privado. A chave NVIDIA está no ambiente privado do backend do Termux. O commit 98f8c48 teve deploy confirmado; 2d291df contém o guia de publicação. Conferir o estado do último build no Pages na retomada.

**Disponibilidade após reinicialização.** O celular já possui Termux:Boot, script de boot com wake-lock e inicialização de service-daemon. Os serviços runit youshop-api, youshop-tunnel e youshop-sync estavam habilitados e em execução. Falta validar um reboot físico combinado com Gean, incluindo eventual primeiro desbloqueio do Android e recuperação da conexão. Evitar reiniciar o aparelho durante uso dos demais serviços.

**Desempenho medido e intervenção pendente.** Duas execuções do fluxo no Termux levaram 9,24 s e 9,15 s; extração NVIDIA: 2,61 s e 2,38 s. O GET público da demo levou 0,15 s. O restante inclui inicialização do processo MCP via stdio, descoberta, chamadas das ferramentas e encerramento. Avaliar manter MCP pré-inicializado em loopback com contexto da proposta isolado por análise; a otimização ainda não foi implementada. Testar concorrência com propostas diferentes, comparar latência antes/depois, rodar a suíte e repetir o POST pelo domínio público. Não registrar segredos nos logs.

**Outras pendências.** Verificar sincronização e reinício automático do backend após mudança na main; renovar a chave exposta anteriormente antes de ampliar divulgação; revisar o pitch e incluir o endereço público no material de entrega quando Gean retomar a apresentação. Formulário até 22/11 às 23h59. Instruções operacionais em [Publicação](10-publicacao.md).

Revisão local do pitch e desempenho: capa com formação, experiência e proposta em duas colunas, nova explicação das responsabilidades no slide 6, link público no slide 10. Conferidas as dez páginas exportadas. No mesmo celular, duas execuções ao vivo do fluxo anterior levaram 11,90 e 10,86 s; em cópia isolada com MCP em memória, 3,32 e 2,23 s. Tempos do fluxo de análise, sem incluir rede até o navegador. Amostra curta. O transporte em memória evita iniciar um interpretador por proposta; cada sessão mantém suas próprias regras. O cliente independente via stdio também descobriu e chamou as ferramentas. Onze testes passaram, incluindo concorrência. O site público continua na versão publicada anteriormente. API e frontend locais iniciados para revisão. Nenhum commit ou push nesta etapa.
