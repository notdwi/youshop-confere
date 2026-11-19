<script setup lang="ts">
import { computed, onMounted, ref } from "vue";
import AppShell from "./components/AppShell.vue";
import OfferComparison from "./components/OfferComparison.vue";
import ImpactSummary from "./components/ImpactSummary.vue";
import CampaignLibrary from "./components/CampaignLibrary.vue";
import CampaignResults from "./components/CampaignResults.vue";
import type { Analysis, Demo, Draft } from "./domain/simulation";

const page = ref<"simulacao" | "campanhas">("simulacao");
const demo = ref<Demo>();
const draft = ref<Draft>();
const analyzed = ref<string>();
const analysis = ref<Analysis>();
const error = ref("");
const loading = ref(false);
const message = ref("");
const noticeId = ref(0);
const noticeOpen = ref(false);
function navigate(destination: typeof page.value) {
  if (page.value === destination) return;
  noticeOpen.value = false;
  page.value = destination;
}

function notify(text: string) {
  message.value = text;
  noticeId.value++;
  noticeOpen.value = true;
}
const stale = computed(() => JSON.stringify(draft.value) !== analyzed.value);

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  let response: Response;
  try {
    response = await fetch((import.meta.env.VITE_API_ORIGIN || "") + path, options);
  } catch {
    throw new Error(
      "A conexão com a API falhou. Verifique sua conexão e tente novamente.",
    );
  }
  const data = await response.json().catch(() => null);
  if (!response.ok || data === null) {
    throw new Error(
      typeof data?.error === "string"
        ? data.error
        : "A API está indisponível. Tente novamente.",
    );
  }
  return data;
}

function initialDraft(data: Demo): Draft {
  return {
    expiresAt: data.current.expiresAt ?? null,
    ...data.initialDraft,
    referenceTime: data.referenceTime,
  };
}

async function load() {
  error.value = "";
  try {
    const data = await request<Demo>("/api/demo/");
    demo.value = data;
    draft.value = initialDraft(data);
    if (data.example) await run(false);
  } catch (cause) {
    error.value =
      cause instanceof Error
        ? cause.message
        : "Falha ao carregar a demonstração.";
  }
}

async function run(announce = true) {
  if (!draft.value || loading.value) return;
  const proposal = JSON.stringify(draft.value);
  loading.value = true;
  error.value = "";
  try {
    analysis.value = await request<Analysis>("/api/analises/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: proposal,
    });
    analyzed.value = proposal;
    if (announce && page.value === "simulacao") notify("Simulação concluída. Confira o impacto nas campanhas.");
  } catch (cause) {
    error.value =
      cause instanceof Error ? cause.message : "Falha ao simular a oferta.";
  } finally {
    loading.value = false;
  }
}

function updateText(id: string, text: string) {
  if (!demo.value || !draft.value) return;
  const texts = { ...draft.value.texts };
  if (
    text === demo.value.campaigns.find((campaign) => campaign.id === id)?.quote
  ) {
    delete texts[id];
  } else {
    texts[id] = text;
  }
  draft.value = {
    ...draft.value,
    texts: Object.keys(texts).length ? texts : undefined,
  };
  const campaign = demo.value.campaigns.find(item => item.id === id);
  notify(`Divulgação de ${campaign?.name ?? "campanha"} atualizada no rascunho.`);
}

function reset() {
  if (!demo.value || loading.value) return;
  draft.value = initialDraft(demo.value);
  notify("Rascunho restaurado para a oferta e as campanhas do exemplo.");
  if (demo.value.example) run(false);
  else error.value = "";
}

onMounted(load);
</script>

<template>
  <AppShell :page="page" @navigate="navigate">
    <template #heading>
      <template v-if="page === 'simulacao'">
        <h1>Simulação de ofertas</h1>
        <p>Confira o que muda no checkout antes de publicar uma oferta.</p>
      </template>
      <template v-else>
        <h1>Campanhas cadastradas</h1>
        <p>Consulte as divulgações e ajuste o texto que entra no rascunho.</p>
      </template>
    </template>

    <p v-if="error" class="api-notice" role="alert">
      {{ error }}
      <button v-if="!demo" class="text-button" @click="load">
        Tentar novamente
      </button>
    </p>
    <p v-if="!demo && !error" role="status">Carregando demonstração…</p>
    <template v-if="demo && draft && page === 'simulacao'">
      <OfferComparison
        :current="demo.current"
        :draft="draft"
        :example="demo.example"
        :loading="loading"
        @update="draft = $event"
        @submit="run()"
        @reset="reset"
      />
      <CampaignResults
        v-if="analysis"
        :results="analysis.results"
        :example="analysis.example"
        :stale="stale"
      >
        <ImpactSummary :results="analysis.results" />
      </CampaignResults>
    </template>
    <CampaignLibrary
      v-else-if="demo && draft && page === 'campanhas'"
      :library-campaigns="demo.campaigns"
      :texts="draft.texts ?? {}"
      :example="demo.example"
      @edit="updateText"
      @back="navigate('simulacao')"
    />
    <v-snackbar location="top end" :key="noticeId" v-model="noticeOpen" :timeout="4500" color="#193752" rounded="lg">
      <span class="action-confirmation" role="status"><v-icon icon="mdi-check-circle-outline" size="20" color="primary" aria-hidden="true" />{{ message }}</span>
      <template #actions><v-btn icon="mdi-close" aria-label="Fechar aviso" @click="noticeOpen = false" /></template>
    </v-snackbar>
  </AppShell>
</template>
