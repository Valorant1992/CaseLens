import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'path';

export default defineConfig({
  plugins: [react()],
  server: {
    // Allow Vite to serve files from the parent directory (where /data lives)
    fs: {
      allow: [path.resolve(__dirname, '..'), __dirname],
    },
  },
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
});
