export type Plan = "Básico" | "Completo";
export type Scope = Plan | "Todos";
export type Status = "Impactada" | "Compatível" | "Revisão necessária";
export interface Draft {
  scope: Scope;
  discount: number;
}
interface Campaign {
  id: string;
  name: string;
  channel: string;
  initials: string;
  quote: string;
  plan?: Plan;
  kind: "coupon" | "price" | "unknown";
}

export const current: Draft = { scope: "Todos", discount: 20 };
export const initialDraft: Draft = { scope: "Básico", discount: 20 };
export const campaigns: Campaign[] = [
  {
    id: "ana",
    name: "Ana Martins",
    initials: "AM",
    channel: "Instagram",
    quote: "Use ANACURSO e pague 20% a menos no plano Completo.",
    plan: "Completo",
    kind: "coupon",
  },
  {
    id: "bruno",
    name: "Bruno Costa",
    initials: "BC",
    channel: "YouTube",
    quote: "Com meu link, o plano Básico sai por R$ 99.",
    plan: "Básico",
    kind: "price",
  },
  {
    id: "camila",
    name: "Camila Rocha",
    initials: "CR",
    channel: "Instagram",
    quote: "Tem uma condição especial se você entrar hoje.",
    kind: "unknown",
  },
];

const brl = new Intl.NumberFormat("pt-BR", {
  style: "currency",
  currency: "BRL",
});
export const money = (cents: number | null) =>
  cents === null ? "—" : brl.format(cents / 100);

export function simulate(draft: Draft) {
  return campaigns.map((campaign) => {
    if (!campaign.plan)
      return {
        campaign,
        status: "Revisão necessária" as const,
        before: null,
        after: null,
        reason:
          "A divulgação não informa o valor nem o plano da condição especial.",
      };
    if (campaign.kind === "price")
      return {
        campaign,
        status: "Compatível" as const,
        before: 9900,
        after: 9900,
        reason: "O preço anunciado para o plano Básico continua válido.",
      };
    const eligible = draft.scope === "Todos" || draft.scope === campaign.plan;
    const before = 19900 - Math.round((19900 * current.discount) / 100);
    const after = eligible
      ? 19900 - Math.round((19900 * draft.discount) / 100)
      : 19900;
    const status: Status = before === after ? "Compatível" : "Impactada";
    const reason = !eligible
      ? "O cupom ANACURSO deixa de valer para o plano Completo."
      : draft.discount === current.discount
        ? "O plano Completo continua com os 20% anunciados."
        : "O percentual do cupom difere da condição anunciada.";
    return { campaign, status, before, after, reason };
  });
}

export type Result = ReturnType<typeof simulate>[number];
