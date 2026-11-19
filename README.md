<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="frontend/public/youshop-logo-light.png">
    <img src="frontend/public/youshop-logo.png" width="170" alt="YouShop">
  </picture>
</p>

<h1 align="center">YouShop Confere</h1>

<p align="center">
  Entrega do desafio técnico de Gean Carlos para o Programa de Estágio YouShop 2027.<br>
  <strong>Vaga de Desenvolvimento – Integrações com Agentes de IA (MCP)</strong>
</p>

<p align="center">
  <a href="https://youshop.noctyra.lol/"><strong>Experimentar a demo</strong></a>
  &nbsp;·&nbsp;
  <a href="docs/apresentacao/confere.pdf">Ler a apresentação em PDF</a>
</p>

Este repositório reúne o protótipo, a apresentação e as decisões técnicas do Desafio de Inovação. Com o Confere, antes de mudar um cupom, o produtor pode testar **quais publicações de creators passariam a prometer um desconto diferente do cobrado**.

## Experimente com a campanha da Ana

Na demo, Ana anuncia 20% de desconto no plano Completo. Simule a mudança do cupom para o Básico e abra **Ver evidência**. O post continua prometendo R$ 159,20, mas o comprador pagaria R$ 199,00. Inclua novamente o Completo e simule para conferir o ajuste. As campanhas e os valores são fictícios.

**Disponibilidade.** O frontend fica no Cloudflare Pages. Hospedo a API Django no meu celular via Termux, com acesso por Cloudflare Tunnel. Se o celular desligar ou perder a conexão, a simulação pode ficar temporariamente indisponível. O PDF inclui uma captura do resultado. [Detalhes da publicação](docs/10-publicacao.md)

## Decisões técnicas

- **IA para ler a promessa.** O backend extrai plano, cupom e valor e verifica se a evidência citada existe na legenda. O modelo reserva assume em caso de demora ou falha recuperável. [Integração com IA](docs/AI-SPEC.md) · [Contrato da API e fallback](docs/09-api.md)
- **MCP para conferir o preço.** O backend consulta as regras e simula a mesma compra nas duas versões da oferta. O checkout calcula em centavos. Uma promessa ambígua segue para revisão. [Arquitetura e ferramentas MCP](docs/04-arquitetura.md)
- **Interface separada da API.** Vue, TypeScript e Vuetify cuidam da interação. Django valida os dados recebidos e mantém as credenciais no servidor. [Frontend](docs/08-frontend.md)

## Como medir o impacto

O indicador do piloto é o número de tentativas com desconto divergente por 100 tentativas de usar o cupom no plano anunciado. A comparação proposta é entre campanhas semelhantes com e sem conferência prévia. A redução em produção depende de um piloto. [Diagnóstico e fontes](docs/02-diagnostico.md) · [Validação e resultados dos testes](docs/05-validacao.md)

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

O modo local padrão usa extrações gravadas e dispensa chave. Para interpretar legendas ao vivo, consulte o [guia de IA](docs/AI-SPEC.md).

## Documentação do projeto

[Briefing do desafio](docs/01-desafio.md) · [Escopo da solução](docs/03-especificacao.md) · [Plano de execução](docs/06-plano.md) · [Roteiro da apresentação](docs/07-apresentacao.md) · [Registro de entrega](docs/RETOMADA.md)
