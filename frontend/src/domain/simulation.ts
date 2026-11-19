export type Plan = "Básico" | "Completo";
export type Scope = Plan | "Todos";
export type Status =
  | "Impactada"
  | "Compatível"
  | "Revisão necessária"
  | "Divergência preexistente";
export interface Draft {
  scope: Scope;
  discount: number;
  expiresAt?: string | null;
  referenceTime?: string;
  texts?: Record<string, string>;
}
export interface Campaign {
  id: string;
  name: string;
  channel: string;
  initials: string;
  quote: string;
  plan?: Plan;
  inSimulation: boolean;
}

const brl = new Intl.NumberFormat("pt-BR", {
  style: "currency",
  currency: "BRL",
});
export const money = (cents: number | null) =>
  cents === null ? "—" : brl.format(cents / 100);

export interface Result {
  campaign: Campaign;
  status: Status;
  before: number | null;
  after: number | null;
  reason: string;
  evidence: string;
  details?: { evidence: string; reason: string; status: Status }[];
}

export interface Analysis {
  results: Result[];
  example: boolean;
  analysisId: string;
}

export interface Demo {
  example: boolean;
  referenceTime: string;
  current: Draft;
  initialDraft: Draft;
  campaigns: Campaign[];
}
