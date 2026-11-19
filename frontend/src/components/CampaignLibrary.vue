<script setup lang="ts">
import { computed, ref } from "vue";
import type { Campaign } from "../domain/simulation";

const props = defineProps<{
  libraryCampaigns: Campaign[];
  texts: Record<string, string>;
  example: boolean;
}>();

const emit = defineEmits<{ back: []; edit: [id: string, text: string] }>();
const editing = ref<string | null>(null);
const editText = ref("");

function startEdit(campaign: Campaign) {
  editing.value = campaign.id;
  editText.value = props.texts[campaign.id] ?? campaign.quote;
}

function saveEdit(id: string) {
  const text = editText.value.trim();
  if (!text) return;
  emit("edit", id, text);
  editing.value = null;
}

const query = ref("");
const channel = ref("");
const channels = Array.from(
  new Set(props.libraryCampaigns.map((item) => item.channel)),
).sort();
const normalize = (value: string) =>
  value
    .normalize("NFD")
    .replace(/\p{Diacritic}/gu, "")
    .toLowerCase();

const matches = computed(() => {
  const term = normalize(query.value.trim());
  return props.libraryCampaigns.filter((item) => {
    const searchable = normalize(
      [item.name, item.channel, props.texts[item.id] ?? item.quote].join(" "),
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
        <blockquote>{{ texts[campaign.id] ?? campaign.quote }}</blockquote>
        <div class="library-actions">
          <button
            v-if="campaign.inSimulation"
            class="text-button"
            :aria-label="'Editar divulgação de ' + campaign.name"
            @click="startEdit(campaign)"
          >
            <v-icon icon="mdi-pencil-outline" size="16" /> Editar
          </button>
          <span
            class="campaign-source"
            :class="{ included: campaign.inSimulation }"
          >
            {{
              texts[campaign.id]
                ? "Rascunho"
                : campaign.inSimulation
                  ? "Na simulação"
                  : "Exemplo adicional"
            }}
          </span>
        </div>
        <form
          v-if="editing === campaign.id"
          class="quote-editor"
          @submit.prevent="saveEdit(campaign.id)"
        >
          <label :for="'quote-' + campaign.id"
            >Divulgação de {{ campaign.name }}</label
          >
          <textarea
            :id="'quote-' + campaign.id"
            v-model="editText"
            required
            maxlength="800"
            rows="3"
          ></textarea>
          <p>
            {{
              example
                ? "No exemplo gravado, uma legenda nova precisa de revisão."
                : "A alteração vale apenas para este rascunho."
            }}
          </p>
          <button
            type="submit"
            class="text-button"
            :disabled="!editText.trim()"
          >
            Aplicar ao rascunho
          </button>
          <button type="button" class="text-button" @click="editing = null">
            Cancelar
          </button>
        </form>
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
