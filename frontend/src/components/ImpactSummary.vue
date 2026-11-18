<script setup lang="ts">
import type { Result, Status } from "../domain/simulation";

const props = defineProps<{ results: Result[] }>();
const metrics: { status: Status; label: string; icon: string; tone: string }[] =
  [
    {
      status: "Impactada",
      label: "Campanhas impactadas",
      icon: "mdi-alert-circle-outline",
      tone: "impact",
    },
    {
      status: "Compatível",
      label: "Campanhas compatíveis",
      icon: "mdi-check-circle-outline",
      tone: "ok",
    },
    {
      status: "Revisão necessária",
      label: "Precisam de revisão",
      icon: "mdi-text-search",
      tone: "review",
    },
  ];
const count = (status: Status) =>
  props.results.filter((item) => item.status === status).length;
</script>

<template>
  <dl class="metrics" aria-label="Resumo da última simulação">
    <div v-for="metric in metrics" :key="metric.status" class="metric">
      <dt>{{ metric.label }}</dt>
      <dd>{{ count(metric.status) }}</dd>
      <v-icon
        :class="metric.tone"
        :icon="metric.icon"
        size="22"
        aria-hidden="true"
      />
    </div>
  </dl>
</template>
