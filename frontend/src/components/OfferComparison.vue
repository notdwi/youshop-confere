<script setup lang="ts">
import type { Draft, Scope } from "../domain/simulation";

const props = defineProps<{
  draft: Draft;
  current: Draft;
  example: boolean;
  loading: boolean;
}>();
const emit = defineEmits<{ update: [draft: Draft]; submit: []; reset: [] }>();
const scopes: Scope[] = ["Todos", "Básico", "Completo"];
const timezone = Intl.DateTimeFormat().resolvedOptions().timeZone;

function localTime(value?: string | null) {
  if (!value) return "";
  const date = new Date(value);
  return new Date(date.getTime() - date.getTimezoneOffset() * 60_000)
    .toISOString()
    .slice(0, 19);
}

function updateTime(field: "expiresAt" | "referenceTime", event: Event) {
  const value = (event.target as HTMLInputElement).value;
  emit("update", {
    ...props.draft,
    [field]: value ? new Date(value).toISOString() : null,
  });
}
</script>

<template>
  <form class="panel editor" @submit.prevent="$emit('submit')">
    <header class="panel-header">
      <div class="section-icon">
        <v-icon icon="mdi-tag-outline" size="21" />
      </div>
      <div>
        <h2>Oferta em análise</h2>
        <p>Curso de Edição de Vídeo · ANACURSO</p>
      </div>
      <span v-if="example" class="analysis-mode">Exemplo gravado</span>
    </header>
    <div class="offer-grid">
      <section class="offer offer-current">
        <h3><span class="small-dot"></span> Oferta atual</h3>
        <dl>
          <div>
            <dt>Desconto</dt>
            <dd>{{ current.discount }}%</dd>
          </div>
          <div>
            <dt>Planos elegíveis</dt>
            <dd>Básico e Completo</dd>
          </div>
        </dl>
      </section>
      <section class="offer offer-draft">
        <h3><v-icon icon="mdi-pencil-outline" size="17" /> Oferta proposta</h3>
        <div class="fields">
          <label for="discount"
            >Desconto
            <span class="number"
              ><input
                id="discount"
                type="number"
                min="0"
                max="100"
                step="1"
                required
                :value="draft.discount"
                @input="
                  $emit('update', {
                    ...draft,
                    discount: ($event.target as HTMLInputElement).valueAsNumber,
                  })
                "
              /><span>%</span></span
            ></label
          >
          <label for="scope"
            >Planos elegíveis
            <select
              id="scope"
              :value="draft.scope"
              @change="
                $emit('update', {
                  ...draft,
                  scope: ($event.target as HTMLSelectElement).value as Scope,
                })
              "
            >
              <option v-for="scope in scopes" :key="scope" :value="scope">
                {{ scope === "Todos" ? "Básico e Completo" : scope }}
              </option>
            </select>
          </label>
        </div>
      </section>
    </div>
    <details class="time-options">
      <summary>Validade do cupom e horário do checkout</summary>
      <div class="fields">
        <label
          >Fim da validade proposta
          <input
            type="datetime-local"
            step="1"
            :value="localTime(draft.expiresAt)"
            @change="updateTime('expiresAt', $event)"
        /></label>
        <label
          >Horário do checkout
          <input
            type="datetime-local"
            step="1"
            required
            :value="localTime(draft.referenceTime)"
            @change="updateTime('referenceTime', $event)"
        /></label>
      </div>
      <p>
        Horários em {{ timezone }}. A validade atual é
        {{
          current.expiresAt
            ? new Date(current.expiresAt).toLocaleString("pt-BR", {
                dateStyle: "short",
                timeStyle: "short",
              })
            : "indeterminada"
        }}. Deixe a validade proposta em branco para simular um cupom sem
        vencimento.
      </p>
    </details>
    <footer class="editor-footer">
      <button
        type="button"
        class="text-button"
        :disabled="loading"
        @click="$emit('reset')"
      >
        <v-icon icon="mdi-restore" size="17" /> Restaurar exemplo</button
      ><v-btn
        type="submit"
        :aria-busy="loading"
        :disabled="loading"
        class="run-button"
        color="primary"
        elevation="0"
        :prepend-icon="loading ? undefined : 'mdi-swap-horizontal'"
        ><v-progress-circular v-if="loading" indeterminate :size="16" :width="2" class="mr-2" /><span role="status">{{ loading ? "Verificando campanhas…" : "Simular alteração" }}</span></v-btn
      >
    </footer>
  </form>
</template>
