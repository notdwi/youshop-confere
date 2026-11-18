import { createApp } from "vue";
import { createVuetify } from "vuetify";
import { VApp, VBtn, VIcon } from "vuetify/components";
import "vuetify/styles";
import "@mdi/font/css/materialdesignicons.css";
import "@fontsource-variable/inter";
import App from "./App.vue";
import "./style.css";

createApp(App)
  .use(
    createVuetify({
      components: { VApp, VBtn, VIcon },
      theme: {
        defaultTheme: "confere",
        themes: {
          confere: {
            dark: false,
            colors: {
              primary: "#b3eb35",
              background: "#f4f6f8",
              surface: "#ffffff",
            },
          },
        },
      },
    }),
  )
  .mount("#app");
