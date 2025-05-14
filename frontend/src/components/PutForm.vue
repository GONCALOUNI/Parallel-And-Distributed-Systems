<template>
  <form @submit.prevent="onSubmit" class="mb-4">
    <h5 class="mb-3">Inserir Par Chave-Valor</h5>
    <div class="row g-3 align-items-end">
      <div class="col-md-5">
        <label class="form-label">Chave</label>
        <input v-model="key" type="text" class="form-control" required />
      </div>
      <div class="col-md-5">
        <label class="form-label">Valor</label>
        <input v-model="value" type="text" class="form-control" required />
      </div>
      <div class="col-md-2">
        <button type="submit" class="btn btn-unified w-100">Guardar</button>
      </div>
    </div>
  </form>
</template>

<script setup>
import { ref } from 'vue'
const key = ref('')
const value = ref('')
const emit = defineEmits(['submit'])

function onSubmit() {
  emit('submit', { key: key.value, value: value.value })
  key.value = ''
  value.value = ''
}
</script>