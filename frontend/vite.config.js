import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  // 构建输出到项目根目录的 static 文件夹
  build: {
    outDir: "../static",
    emptyOutDir: true,
  },
  // 开发时代理后端 API
  server: {
    port: 3000,
    proxy: {
      "/chat": "http://127.0.0.1:8000",
      "/tools": "http://127.0.0.1:8000",
      "/model": "http://127.0.0.1:8000",
    },
  },
});