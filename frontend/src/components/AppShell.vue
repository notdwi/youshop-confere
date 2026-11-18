<script setup lang="ts">
import { nextTick, ref } from "vue";
import BrandLockup from "./BrandLockup.vue";
type Page = "simulacao" | "campanhas";

defineProps<{ page: Page }>();
const emit = defineEmits<{ navigate: [page: Page] }>();
const menuOpen = ref(false);
const menuTrigger = ref<HTMLButtonElement | null>(null);
const drawerClose = ref<HTMLButtonElement | null>(null);

async function openMenu() {
  menuOpen.value = true;
  await nextTick();
  drawerClose.value?.focus();
}

function onNavigationBlur(event: FocusEvent) {
  const related = event.relatedTarget;
  if (
    related instanceof Node &&
    !(event.currentTarget as HTMLElement).contains(related)
  ) {
    closeMenu();
  }
}

function closeMenu(restoreFocus = false) {
  if (!menuOpen.value) return;
  menuOpen.value = false;
  if (restoreFocus) menuTrigger.value?.focus();
}

function navigate(page: Page) {
  closeMenu(true);
  emit("navigate", page);
}

const items = [
  { id: "simulacao", label: "Simulação", icon: "mdi-tune-variant" },
  { id: "campanhas", label: "Campanhas", icon: "mdi-bullhorn-outline" },
] as const;
</script>

<template>
  <v-app>
    <a class="skip" href="#conteudo">Pular para o conteúdo</a>
    <div class="shell">
      <aside
        class="sidebar"
        aria-label="YouShop Confere"
        @keydown.esc="closeMenu(true)"
        @focusout="onNavigationBlur"
      >
        <BrandLockup />
        <button
          ref="menuTrigger"
          type="button"
          class="mobile-menu-trigger"
          aria-controls="primary-navigation"
          :aria-expanded="menuOpen"
          @click="openMenu"
        >
          <v-icon icon="mdi-menu" size="21" aria-hidden="true" />
          Menu
        </button>
        <div
          v-if="menuOpen"
          class="mobile-menu-scrim"
          aria-hidden="true"
          @click="closeMenu(true)"
        ></div>
        <nav
          id="primary-navigation"
          :class="{ 'is-open': menuOpen }"
          aria-label="Navegação principal"
        >
          <div class="mobile-drawer-header">
            <span>Navegação</span>
            <button
              ref="drawerClose"
              type="button"
              aria-label="Fechar menu"
              @click="closeMenu(true)"
            >
              <v-icon icon="mdi-close" size="21" aria-hidden="true" />
            </button>
          </div>
          <button
            v-for="item in items"
            :key="item.id"
            type="button"
            :aria-current="page === item.id ? 'page' : undefined"
            @click="navigate(item.id)"
          >
            <v-icon :icon="item.icon" size="19" />
            {{ item.label }}
          </button>
          <div class="mobile-drawer-footer">
            <BrandLockup />
            <span>Ambiente de demonstração</span>
          </div>
        </nav>
        <div class="sidebar-footer">
          <v-icon icon="mdi-flask-outline" size="19" />
          <div>Ambiente de demonstração<small>Dados fictícios</small></div>
        </div>
      </aside>
      <main id="conteudo" class="workspace" tabindex="-1" @click="closeMenu()">
        <header class="workspace-heading">
          <div class="heading-main">
            <p class="breadcrumb">
              <v-icon icon="mdi-storefront-outline" size="17" />
              <span>Produtor</span>
              <v-icon icon="mdi-chevron-right" size="15" />
              <strong>{{
                page === "simulacao" ? "Simulação" : "Campanhas"
              }}</strong>
            </p>
            <slot name="heading" />
          </div>
          <span class="demo-tag"
            ><span aria-hidden="true"></span> Dados fictícios</span
          >
        </header>
        <div
          class="content"
          :class="{ 'simulation-content': page === 'simulacao' }"
        >
          <slot />
        </div>
      </main>
    </div>
  </v-app>
</template>
