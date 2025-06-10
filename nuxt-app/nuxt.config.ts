// https://nuxt.com/docs/api/configuration/nuxt-config
import type { NuxtPage } from "nuxt/schema";
import Aura from "@primeuix/themes/aura";
export default defineNuxtConfig({
  css: ["~/assets/scss/main.scss"],
  app: {
    head: {
      meta: [
        { name: "viewport", content: "width=device-width, initial-scale=1.0" },
      ],
    },
  },
  compatibilityDate: "2024-11-01",
  devtools: { enabled: true },
  modules: [
    "@nuxtjs/tailwindcss",
    "@primevue/nuxt-module",
    "@nuxt/icon",
    "nuxt-auth-utils",
    "@pinia/nuxt",
    "pinia-plugin-persistedstate/nuxt",
    "nuxt-swiper",
  ],
  primevue: {
    autoImport: false,
    options: {
      theme: {
        preset: Aura,
        options: {
          prefix: "p",
          darkModeSelector: "white",
          cssLayer: false,
        },
      },
    },
  },
  icon: {
    serverBundle: {
      collections: ["mdi"],
    },
  },
  runtimeConfig: {
    public: {
      apiBase: process.env.API_URL || "http://localhost:8000",
    },
  },
  hooks: {
    "pages:extend"(pages) {
      function setMiddleware(pagesArray: any[]) {
        for (const page of pagesArray) {
          page.meta = page.meta || {};
          page.meta.middleware = ["auth"];

          if (page.children && page.children.length > 0) {
            setMiddleware(page.children);
          }

          if (page.name == "admin") {
            page.meta.middleware = ["admin"];
          }
        }
      }

      setMiddleware(pages);
    },
  },
});
