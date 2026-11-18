<script setup lang="ts">
import { computed, ref } from "vue";
import AppShell from "./components/AppShell.vue";
import OfferComparison from "./components/OfferComparison.vue";
import ImpactSummary from "./components/ImpactSummary.vue";
import CampaignLibrary from "./components/CampaignLibrary.vue";
import CampaignResults from "./components/CampaignResults.vue";
import { initialDraft, simulate, type Draft } from "./domain/simulation";

const page = ref<"simulacao" | "campanhas">("simulacao");
const draft = ref<Draft>({ ...initialDraft });
const analyzed = ref<Draft>({ ...initialDraft });
const results = computed(() => simulate(analyzed.value));
const stale = computed(
  () =>
    draft.value.scope !== analyzed.value.scope ||
    draft.value.discount !== analyzed.value.discount,
);

function run() {
  const { discount } = draft.value;
  if (Number.isInteger(discount) && discount >= 0 && discount <= 100)
    analyzed.value = { ...draft.value };
}

function reset() {
  draft.value = { ...initialDraft };
  run();
}
</script>

<template>
  <AppShell :page="page" @navigate="page = $event">
    <template #heading>
      <template v-if="page === 'simulacao'">
        <h1>Simulação de ofertas</h1>
        <p>Confira o que muda no checkout antes de publicar uma oferta.</p>
      </template>
      <template v-else>
        <h1>Campanhas cadastradas</h1>
        <p>
          Consulte as divulgações e identifique quais entram na simulação da
          oferta.
        </p>
      </template>
    </template>

    <template v-if="page === 'simulacao'">
      <OfferComparison
        :draft="draft"
        @update="draft = $event"
        @submit="run"
        @reset="reset"
      />
      <CampaignResults :results="results" :stale="stale">
        <ImpactSummary :results="results" />
      </CampaignResults>
    </template>
    <CampaignLibrary v-else @back="page = 'simulacao'" />
  </AppShell>
</template>
