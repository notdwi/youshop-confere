<script setup lang="ts">
import type { Status } from "../domain/simulation";

defineProps<{ status: Status }>();
const tones = {
  "Divergência preexistente": "prior",
  Impactada: "impact",
  Compatível: "ok",
  "Revisão necessária": "review",
};
</script>
<template>
  <span class="status" :class="tones[status]"
    ><span aria-hidden="true"></span>{{ status }}</span
  >
</template>
