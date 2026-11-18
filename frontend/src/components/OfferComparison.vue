<script setup lang="ts">
import { current, type Draft, type Scope } from "../domain/simulation";

defineProps<{ draft: Draft }>();
defineEmits<{ update: [draft: Draft]; submit: []; reset: [] }>();
const scopes: Scope[] = ["Todos", "Básico", "Completo"];
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
    <footer class="editor-footer">
      <button type="button" class="text-button" @click="$emit('reset')">
        <v-icon icon="mdi-restore" size="17" /> Restaurar exemplo</button
      ><v-btn
        type="submit"
        class="run-button"
        color="primary"
        elevation="0"
        prepend-icon="mdi-swap-horizontal"
        >Simular alteração</v-btn
      >
    </footer>
  </form>
</template>
