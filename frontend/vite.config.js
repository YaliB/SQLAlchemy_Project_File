import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite' // Importing the new v4 engine

export default defineConfig({
  plugins: [
    react(),
    tailwindcss(), // Adding Tailwind as a Vite plugin
  ],
})