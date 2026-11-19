# Extração das condições anunciadas

O produtor precisa saber qual promessa deixaria de ser cumprida por uma mudança no checkout. A IA lê o que o creator escreveu, identifica o plano e o benefício e cita as palavras que sustentam a interpretação. A classificação e os cálculos em centavos ficam nas regras do backend.

## Dois modos de execução

Em `recorded`, o servidor reconhece os textos dos exemplos e recupera as condições anotadas. Um material sem anotação correspondente gera uma condição inconclusiva. Isso permite demonstrar o fluxo sem credenciais.

Para habilitar `nvidia`, copie `backend/.env.example` para `backend/.env`, defina `CONFERE_MODE=nvidia` e informe o identificador do modelo habilitado na sua conta em `NVIDIA_MODEL`. Guarde a chave em `NVIDIA_API_KEY`. Variáveis do processo têm precedência. O modelo deve aceitar mensagens de sistema e conseguir devolver JSON na API de chat. O backend chama o endpoint HTTPS oficial com autenticação Bearer. [API de modelos da NVIDIA](https://docs.api.nvidia.com/nim/reference/llm-apis)

## Contrato e dados

Uma requisição agrupa os IDs e textos das campanhas participantes. As legendas podem conter instruções escritas por terceiros. O prompt as trata como dados. O backend exige um resultado por ID, valida tipos e campos, aceita apenas planos conhecidos e verifica a presença literal de cada evidência na legenda correspondente. Para preços, o modelo informa centavos. Para cupons, informa código e percentual inteiro. Uma condição imprecisa pode incluir seu trecho original e marcar o caso para revisão.

O provedor recebe o conteúdo das legendas analisadas. A demo usa dados fictícios. A presença de uma citação literal comprova a origem das palavras, mas um modelo ainda pode interpretar incorretamente o plano, o valor ou o contexto da frase. A revisão humana pode conferir a legenda e os cálculos antes da publicação.

## Verificação

Em `backend`, execute `.venv/bin/python -m unittest test_extraction`. As respostas simuladas cobrem o contrato HTTP, evidência inventada, identificador ausente ou duplicado, percentual booleano, indisponibilidade do provedor e edição de uma legenda gravada. Uma falha de serviço interrompe a análise e permite nova tentativa.

Para testar um modelo real, configure-o no backend, simule as três campanhas e verifique as extrações de Ana (20%, ANACURSO, Completo), Bruno (9900 centavos, Básico) e Camila (ambígua). Anote modelo, data, número de condições corretas, citação de suporte e casos inconclusivos. Avalie separadamente uma paráfrase inédita e uma promessa ambígua antes de atribuir uma taxa de acerto ao modelo.

## Escolha do modelo para a primeira avaliação

O candidato escolhido para o próximo teste é `moonshotai/kimi-k3.1-pro`, com esforço de raciocínio baixo. A aplicação envia somente as legendas em texto e recebe uma resposta JSON completa. A primeira alternativa pesquisada foi `mistralai/mistral-nemotron`, divulgado com endpoint gratuito para prototipagem e foco em seguir instruções. Disponibilidade e limites dependem da conta. O projeto não mediu latência nem precisão desse modelo em produção. Na comparação, registrar tempo total por lote, respostas com JSON válido, trecho literal e classificação correta. O contrato Claim permite testar outros modelos do catálogo pela variável NVIDIA_MODEL. Integrações diretas com Claude ou modelos da OpenAI exigem adaptador e credenciais próprios. [NVIDIA Build](https://build.nvidia.com/mistralai/mistral-nemotron)
