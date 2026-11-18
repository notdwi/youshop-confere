<script setup lang="ts">
import { ref } from "vue";
import { money, type Result } from "../domain/simulation";
import StatusBadge from "./StatusBadge.vue";

defineProps<{ results: Result[]; stale: boolean }>();
const selected = ref<string | null>(null);

function toggle(id: string) {
  selected.value = selected.value === id ? null : id;
}
</script>

<template>
  <section class="panel results" aria-labelledby="results-title">
    <header class="panel-header">
      <div class="section-icon">
        <v-icon icon="mdi-clipboard-check-outline" size="21" />
      </div>
      <div>
        <h2 id="results-title">Impacto nas campanhas</h2>
        <p>Resultados da última simulação</p>
      </div>
    </header>
    <slot />
    <p v-if="stale" class="stale" role="status">
      <v-icon icon="mdi-information-outline" size="17" /> Rascunho alterado.
      Rode uma nova simulação.
    </p>
    <ul class="results-list">
      <li v-for="item in results" :key="item.campaign.id" class="result-item">
        <div class="result-top">
          <div class="creator">
            <span class="avatar" :class="item.campaign.id">{{
              item.campaign.initials
            }}</span>
            <span
              >{{ item.campaign.name
              }}<small>{{ item.campaign.channel }}</small></span
            >
          </div>
          <StatusBadge :status="item.status" />
        </div>
        <div class="result-bottom">
          <dl class="checkout-values">
            <div>
              <dt>Checkout atual</dt>
              <dd>{{ money(item.before) }}</dd>
            </div>
            <div>
              <dt>Checkout proposto</dt>
              <dd :class="{ changed: item.status === 'Impactada' }">
                {{ money(item.after) }}
              </dd>
            </div>
          </dl>
          <button
            type="button"
            class="text-button details-button"
            :aria-expanded="selected === item.campaign.id"
            :aria-controls="'evidence-' + item.campaign.id"
            :aria-label="'Evidência de ' + item.campaign.name"
            @click="toggle(item.campaign.id)"
          >
            {{
              selected === item.campaign.id
                ? "Ocultar evidência"
                : "Ver evidência"
            }}
            <v-icon
              :icon="
                selected === item.campaign.id
                  ? 'mdi-chevron-up'
                  : 'mdi-chevron-down'
              "
              size="17"
            />
          </button>
        </div>
        <div
          v-show="selected === item.campaign.id"
          :id="'evidence-' + item.campaign.id"
          class="evidence"
        >
          <blockquote>{{ item.campaign.quote }}</blockquote>
          <p>{{ item.reason }}</p>
        </div>
      </li>
    </ul>
  </section>
</template>
