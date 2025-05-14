<template>
  <form @submit.prevent="onSubmit">
    <h5 class="mb-3">Eliminar Par pela Chave</h5>
    <div class="row g-3 align-items-end">
      <div class="col-md-10">
        <label class="form-label">Chave</label>
        <input v-model="key" type="text" class="form-control" required />
      </div>
      <div class="col-md-2">
        <button type="submit" class="btn btn-unified w-100">Eliminar</button>
      </div>
    </div>
  </form>
</template>

<script setup>
import { ref } from 'vue'
const key = ref('')
const emit = defineEmits(['submit'])

function onSubmit() {
  emit('submit', key.value)
  key.value = ''
}
</script>