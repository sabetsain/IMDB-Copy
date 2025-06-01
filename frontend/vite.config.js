import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  optimizeDeps: {
    include: ['prop-types']
  },
  define: {
    global: 'globalThis'
  },
  resolve: {
    alias: {
      'prop-types': 'prop-types/index.js'
    }
  }
})
