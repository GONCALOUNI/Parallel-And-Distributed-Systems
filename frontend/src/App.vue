<template>
  <div class="min-h-screen bg-gray-50">
    <nav class="bg-white shadow p-4">
      <ul class="flex space-x-4">
        <li>
          <router-link to="/" class="text-blue-600 hover:underline">Home</router-link>
        </li>
        <li>
          <router-link to="/store" class="text-blue-600 hover:underline">Store</router-link>
        </li>
      </ul>
    </nav>

    <main class="p-6">
      <router-view />
    </main>
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style>
</style>