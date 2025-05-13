<template>
  <div class="d-flex flex-column min-vh-100">
    <Navbar />

    <main class="container flex-grow-1 py-5">
      <div
        class="p-4 rounded-3 bg-light dark-bg-secondary text-dark text-white-50"
      >
        <h2 class="mb-4">Gestor de Key-Value</h2>

        <form @submit.prevent="handlePut" class="row g-3 mb-3">
          <div class="col-md-5">
            <label for="inputKey" class="form-label">Chave</label>
            <input
              v-model="key"
              id="inputKey"
              type="text"
              class="form-control"
              placeholder="Insira a chave"
            />
          </div>
          <div class="col-md-5">
            <label for="inputValue" class="form-label">Valor</label>
            <input
              v-model="value"
              id="inputValue"
              type="text"
              class="form-control"
              placeholder="Insira o valor"
            />
          </div>
          <div class="col-md-2 d-flex align-items-end">
            <button type="submit" class="btn btn-success me-2">Guardar</button>
            <button @click.prevent="handleGet" type="button" class="btn btn-info me-2">
              Obter
            </button>
            <button @click.prevent="handleDelete" type="button" class="btn btn-danger">
              Eliminar
            </button>
          </div>
        </form>

        <div v-if="result" class="alert alert-secondary" role="alert">
          <h5 class="alert-heading">Resultado</h5>
          <pre class="mb-0">{{ result }}</pre>
        </div>
      </div>
    </main>

    <Footer />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import Navbar from '../components/Navbar.vue'
import Footer from '../components/Footer.vue'

const key = ref('')
const value = ref('')
const result = ref(null)

async function handlePut() {
  try {
    const res = await axios.put('http://localhost:8000/', {
      data: { key: key.value, value: value.value }
    })
    result.value = JSON.stringify(res.data, null, 2)
  } catch (err) {
    result.value = err.response?.data || err.message
  }
}

async function handleGet() {
  try {
    const res = await axios.get('http://localhost:8000/', {
      params: { key: key.value }
    })
    result.value = JSON.stringify(res.data, null, 2)
  } catch (err) {
    result.value = err.response?.data || err.message
  }
}

async function handleDelete() {
  try {
    const res = await axios.delete('http://localhost:8000/', {
      params: { key: key.value }
    })
    result.value = JSON.stringify(res.data, null, 2)
  } catch (err) {
    result.value = err.response?.data || err.message
  }
}
</script>

<style>
.bg-light {
  background-color: #ffffff !important;
}

html.dark .dark-bg-secondary {
  background-color: #2c2c2c !important;
  color: #e1e1e1 !important;
}
</style>