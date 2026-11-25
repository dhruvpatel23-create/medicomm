import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import { posix } from "node:path";

const privateTheoryAssets = {
  name: "private-theory-assets",
  configureServer(server) {
    server.middlewares.use((request, response, next) => {
      const url = new URL(request.url, "http://localhost");
      let pathname;
      try {
        pathname = posix.normalize(decodeURIComponent(url.pathname).replaceAll("\\", "/"));
      } catch {
        return next();
      }
      if (/^\/(?:short-notes\.json$|theory-answers\/)/i.test(pathname)) {
        // Route encoded and case-variant paths through the proxy before Vite serves public files.
        const route = pathname.toLowerCase() === "/short-notes.json" ? "/short-notes.json" : "/theory-answers/";
        request.url = route + encodeURI(pathname.slice(route.length)) + url.search;
      }
      next();
    });
  },
};

export default defineConfig({
  plugins: [react(), privateTheoryAssets],
  optimizeDeps: {
    entries: ["index.html"],
  },
  server: {
    host: "127.0.0.1",
    port: 4173,
    strictPort: true,
    watch: {
      ignored: [
        "**/.tmp/**",
        "**/output/**",
        "**/scratch/**",
        "**/runtime-data/**",
      ],
    },
    proxy: {
      "/api": "http://127.0.0.1:4174",
      "/uploads": "http://127.0.0.1:4174",
      "/short-notes.json": "http://127.0.0.1:4174",
      "/theory-answers/": "http://127.0.0.1:4174",
    },
    fs: {
      deny: [".env", ".env.*", "*.{crt,pem}", "**/.git/**", "**/short-notes.json", "**/theory-answers/**"],
    },
  },
});
