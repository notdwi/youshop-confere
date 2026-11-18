<script setup lang="ts">
import { computed, ref } from "vue";
import { libraryCampaigns } from "../domain/campaignLibrary";

defineEmits<{ back: [] }>();

const query = ref("");
const channel = ref("");
const channels = Array.from(
  new Set(libraryCampaigns.map((item) => item.channel)),
).sort();
const normalize = (value: string) =>
  value
    .normalize("NFD")
    .replace(/\p{Diacritic}/gu, "")
    .toLowerCase();

const matches = computed(() => {
  const term = normalize(query.value.trim());
  return libraryCampaigns.filter((item) => {
    const searchable = normalize(
      [item.name, item.channel, item.quote].join(" "),
    );
    return (
      (!channel.value || item.channel === channel.value) &&
      searchable.includes(term)
    );
  });
});

function clearFilters() {
  query.value = "";
  channel.value = "";
}
</script>

<template>
  <section class="panel" aria-labelledby="library-heading">
    <header class="panel-header library-header">
      <div class="section-icon">
        <v-icon icon="mdi-bullhorn-outline" size="20" />
      </div>
      <div class="library-label">
        <h2 id="library-heading">Materiais de divulgação</h2>
        <p aria-live="polite">
          {{ matches.length }} de {{ libraryCampaigns.length }} campanhas
        </p>
      </div>
    </header>
    <div class="library-toolbar">
      <label class="campaign-search">
        <v-icon icon="mdi-magnify" size="18" />
        <input
          v-model="query"
          type="search"
          aria-label="Buscar campanhas"
          placeholder="Buscar por creator ou divulgação"
        />
      </label>
      <select
        v-model="channel"
        class="channel-filter"
        aria-label="Filtrar por canal"
      >
        <option value="">Todos os canais</option>
        <option v-for="item in channels" :key="item" :value="item">
          {{ item }}
        </option>
      </select>
    </div>
    <ul
      v-if="matches.length"
      class="campaign-list"
      aria-label="Lista de campanhas"
    >
      <li v-for="campaign in matches" :key="campaign.id">
        <div class="creator">
          <span class="avatar" :class="campaign.id">{{
            campaign.initials
          }}</span>
          <span
            >{{ campaign.name }}<small>{{ campaign.channel }}</small></span
          >
        </div>
        <blockquote>{{ campaign.quote }}</blockquote>
        <span
          class="campaign-source"
          :class="{ included: campaign.inSimulation }"
        >
          {{ campaign.inSimulation ? "Na simulação" : "Exemplo adicional" }}
        </span>
      </li>
    </ul>
    <div v-else class="empty">
      <p>Nenhuma campanha corresponde aos filtros.</p>
      <button class="text-button" type="button" @click="clearFilters">
        Limpar filtros
      </button>
    </div>
    <footer class="library-footer">
      <p>As campanhas marcadas entram no cenário de simulação.</p>
      <v-btn
        class="run-button library-back"
        color="primary"
        elevation="0"
        prepend-icon="mdi-arrow-left"
        @click="$emit('back')"
        >Voltar à simulação</v-btn
      >
    </footer>
  </section>
</template>
