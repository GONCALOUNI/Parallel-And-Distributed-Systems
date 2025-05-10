<template>
    <div class="p-6 space-y-4">
      <h1 class="text-2xl font-semibold">Gestor de Key-Value</h1>
  
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label class="block mb-1 font-medium">Chave</label>
          <input
            v-model="key"
            type="text"
            placeholder="Insira a chave"
            class="w-full border rounded p-2"
          />
        </div>
        <div>
          <label class="block mb-1 font-medium">Valor</label>
          <input
            v-model="value"
            type="text"
            placeholder="Insira o valor"
            class="w-full border rounded p-2"
          />
        </div>
      </div>
  
      <div class="space-x-2">
        <button
          @click="handlePut"
          class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded"
        >
          Guardar
        </button>
        <button
          @click="handleGet"
          class="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded"
        >
          Obter
        </button>
        <button
          @click="handleDelete"
          class="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded"
        >
          Eliminar
        </button>
      </div>
  
      <div v-if="result" class="mt-4 p-4 bg-gray-100 rounded">
        <h2 class="font-medium mb-2">Resultado</h2>
        <pre class="whitespace-pre-wrap">{{ result }}</pre>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios'
  
  export default {
    name: 'KeyValueView',
    data() {
      return {
        key: '',
        value: '',
        result: null
      }
    },
    methods: {
      async handlePut() {
        try {
          const res = await axios.put('http://localhost:8000/', {
            data: { key: this.key, value: this.value }
          })
          this.result = res.data
        } catch (err) {
          this.result = err.response?.data || err.message
        }
      },
      async handleGet() {
        try {
          const res = await axios.get('http://localhost:8000/', {
            params: { key: this.key }
          })
          this.result = res.data
        } catch (err) {
          this.result = err.response?.data || err.message
        }
      },
      async handleDelete() {
        try {
          const res = await axios.delete('http://localhost:8000/', {
            params: { key: this.key }
          })
          this.result = res.data
        } catch (err) {
          this.result = err.response?.data || err.message
        }
      }
    }
  }
  </script>
  
  <style scoped>
  </style>  