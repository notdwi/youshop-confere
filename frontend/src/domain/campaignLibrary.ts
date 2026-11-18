import { campaigns } from "./simulation";

const examples = [
  {
    id: "davi",
    name: "Davi Nunes",
    initials: "DN",
    channel: "TikTok",
    quote: "Comece a editar com o plano Básico por R$ 99 no meu link.",
  },
  {
    id: "laura",
    name: "Laura Mendes",
    initials: "LM",
    channel: "YouTube",
    quote: "Use LAURA10 para ter 10% de desconto no plano Completo.",
  },
  {
    id: "rafael",
    name: "Rafael Lima",
    initials: "RL",
    channel: "Instagram",
    quote:
      "O plano Completo inclui as aulas avançadas e os arquivos de prática.",
  },
  {
    id: "sofia",
    name: "Sofia Alves",
    initials: "SA",
    channel: "TikTok",
    quote:
      "Acesse pelo meu perfil para conferir o desconto disponível no checkout.",
  },
];

export const libraryCampaigns = [
  ...campaigns.map((campaign) => ({ ...campaign, inSimulation: true })),
  ...examples.map((campaign) => ({ ...campaign, inSimulation: false })),
];
