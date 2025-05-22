<template>
  <div class="d-flex flex-column min-vh-100">
    <Navbar />

    <main class="container flex-grow-1 pt-3 pb-5">
      <div class="p-4 bg-white dark-bg-secondary rounded-3">
        <h2 class="mb-4 fw-bold">Gestor de Key-Value</h2>

        <PutForm @submit="handlePut" class="mb-5" />
        <GetForm @submit="handleGet" class="mb-5" />
        <DeleteForm @submit="handleDelete" class="mb-4" />

        <!-- Caixa de resultado única sem pre-formatação -->
        <div v-if="alertMessage" :class="['alert', alertClass, 'mt-4']" role="alert">
          <h5 class="alert-heading">Resultado</h5>
          <p class="mb-0">{{ alertMessage }}</p>
        </div>
      </div>
    </main>

    <Footer />
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import axios from 'axios'
import Navbar from '../components/Navbar.vue'
import Footer from '../components/Footer.vue'
import PutForm from '../components/PutForm.vue'
import GetForm from '../components/GetForm.vue'
import DeleteForm from '../components/DeleteForm.vue'

const alertMessage = ref('')
const alertType = ref('')

const alertClass = computed(() => alertType.value === 'success' ? 'alert-success' : 'alert-danger')

async function handlePut({ key, value }) {
  try {
    await axios.put('http://localhost:8000/kv', { data: { key, value } })
    alertType.value = 'success'
    alertMessage.value = `Sucesso! Guardada a key "${key}" com valor "${value}".`
  } catch (err) {
    alertType.value = 'danger'
    alertMessage.value = `Erro: ${err.response?.data?.detail || err.message}`
  }
}

async function handleGet(key) {
  try {
    const res = await axios.get('http://localhost:8000/kv', { params: { key } })
    const val = res.data?.data?.value ?? res.data
    alertType.value = 'success'
    alertMessage.value = `Sucesso! Obtida a key "${key}" com valor "${val}".`
  } catch (err) {
    alertType.value = 'danger'
    alertMessage.value = `Erro: ${err.response?.data?.detail || err.message}`
  }
}

async function handleDelete(key) {
  try {
    const res = await axios.delete('http://localhost:8000/kv', { params: { key } })
    const val = res.data?.data?.value
    alertType.value = 'success'
    alertMessage.value = val
      ? `Sucesso! Removida a key "${key}" com valor "${val}".`
      : `Sucesso! Removida a key "${key}".`
  } catch (err) {
    alertType.value = 'danger'
    alertMessage.value = `Erro: ${err.response?.data?.detail || err.message}`
  }
}
</script>

<style scoped>
@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(10px); }
  to   { opacity: 1; transform: translateY(0); }
}

:root.dark .dark-bg-secondary {
  background-color: #2c2c2c !important;
}

.btn-unified {
  background: none;
  border: 2px solid;
  font-weight: 500;
  transition: transform 0.2s ease, box-shadow 0.2s ease, background 0.3s ease, border-color 0.3s ease;
}
:root.dark .btn-unified {
  color: white !important;
  border-color: white !important;
}
:root .btn-unified {
  color: black;
  border-color: black;
}

.btn-unified:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 6px rgba(0,0,0,0.15);
}
.btn-unified:active {
  transform: translateY(0);
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

input {
  transition: background-image 0.3s ease, box-shadow 0.3s ease, border 0.3s ease;
}
input:focus {
  border: 2px solid transparent;
  outline: none;
  background-clip: padding-box;
  border-radius: 0.375rem;
  box-shadow: 0 0 0 2px transparent;
  background-image:
    linear-gradient(white, white),
    var(--main-gradient);
  background-origin: border-box;
  background-clip: padding-box, border-box;
}

:root.dark input:focus {
  background-image:
    linear-gradient(#2c2c2c, #2c2c2c),
    var(--main-gradient) !important;
}

h2, h5, .form-label {
  font-weight: 600;
}

form {
  margin-bottom: 2.5rem;
  animation: fadeInUp 0.5s ease-out both;
}
</style>