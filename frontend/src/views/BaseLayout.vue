<template>
    <div class="layout">
      <NavBar />
      <main class="layout-main" :style="{ maxWidth: maxWidth }">
        <slot />
      </main>
    </div>
  </template>
  
<script setup>
  import NavBar from '@/components/NavBar.vue'
  
  defineProps({
    maxWidth: {
      type: String,
      default: '1000px'
    }
  })
</script>
  
<style scoped>
  .layout {
    min-height: 100vh;
    background: var(--bg);
  }
  .layout-main {
    margin: 0 auto;
    padding: 2.5rem 2rem;
  }
</style>