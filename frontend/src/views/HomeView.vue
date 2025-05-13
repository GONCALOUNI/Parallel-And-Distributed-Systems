<template>
  <div class="d-flex vh-100 align-items-center justify-content-center bg-white dark:bg-gray-900">
    <div
      class="p-5 rounded-3 bg-white dark:bg-gray-800 text-center fade-down"
      style="max-width: 800px; width: 100%;"
    >
      <h1 class="display-4 fw-bold mb-3">Seja bem-vind@ ao KVerse!</h1>
      <p class="fs-5 mb-4 fade-in">
        Utilize o menu para navegar e gerir os seus pares key-value.
      </p>
      <button
        @click="$router.push('/store')"
        class="btn text-white px-4 py-2 pulse"
      >
        <span class="btn-text">Começar</span>
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'HomeView'
}
</script>

<style scoped>
@keyframes fadeInDown {
  from { opacity: 0; transform: translateY(-50px); }
  to   { opacity: 1; transform: translateY(0); }
}
@keyframes fadeIn {
  from { opacity: 0; }
  to   { opacity: 1; }
}
@keyframes pulse {
  0%,100% { transform: scale(1); }
  50%     { transform: scale(1.05); }
}

.fade-down { animation: fadeInDown 0.8s ease-out both; }
.fade-in   { animation: fadeIn 1s ease-out 0.5s both; }
.pulse     { animation: pulse 1.5s ease-in-out infinite; }

button.pulse {
  background: linear-gradient(45deg, #fc8200, #fc2c00);
  border: none;
}

.btn-text {
  background: linear-gradient(45deg, #fc8200, #fc2c00);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

:root.dark button.pulse {
  background: #121212 !important;
}
</style>