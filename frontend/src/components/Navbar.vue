<template>
  <nav
    class="navbar navbar-expand-lg navbar-dark"
    style="background: linear-gradient(45deg, #fc8200, #fc2c00);"
  >
    <div class="container-fluid">
      <router-link class="navbar-brand text-white fw-bold" to="/">
        KVerse
      </router-link>

      <button
        class="navbar-toggler border-0"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#navbarNav"
        aria-controls="navbarNav"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon"></span>
      </button>

      <div class="collapse navbar-collapse" id="navbarNav">

        <ul class="navbar-nav me-auto mb-2 mb-lg-0">
          <li class="nav-item">
            <router-link class="nav-link text-white" to="/store">Store</router-link>
          </li>
          <li class="nav-item">
            <a
              class="nav-link text-white"
              href="http://localhost:5051"
              target="_blank"
              rel="noopener"
            >
              Ver BD
            </a>
          </li>
        </ul>

        <ul class="navbar-nav align-items-center">
          <li class="nav-item dropdown me-3">
            <a
              class="nav-link dropdown-toggle text-white"
              href="#"
              id="langDropdown"
              role="button"
              data-bs-toggle="dropdown"
              aria-expanded="false"
            >
              <i class="bi bi-globe"></i>
            </a>
            <ul class="dropdown-menu dropdown-menu-end" aria-labelledby="langDropdown">
              <li>
                <a class="dropdown-item d-flex align-items-center" href="#">
                  <span class="me-2">🇵🇹</span>
                  Português
                </a>
              </li>
              <li>
                <a class="dropdown-item d-flex align-items-center" href="#">
                  <span class="me-2">🇬🇧</span>
                  English
                </a>
              </li>
            </ul>
          </li>
          <li class="nav-item">
            <button
              class="btn btn-sm text-white"
              @click="toggleTheme"
              :title="isDark ? 'Light Mode' : 'Dark Mode'"
            >
              <i v-if="isDark" class="bi bi-sun-fill"></i>
              <i v-else class="bi bi-moon-stars-fill"></i>
            </button>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const isDark = ref(false)
function toggleTheme() {
  isDark.value = !isDark.value
  document.documentElement.classList.toggle('dark', isDark.value)
  localStorage.setItem('theme', isDark.value ? 'dark' : 'light')
}

onMounted(() => {
  const saved = localStorage.getItem('theme')
  if (saved === 'dark' || (!saved && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
    isDark.value = true
    document.documentElement.classList.add('dark')
  }
})
</script>

<style scoped>
.navbar-nav .nav-link {
  transition: color 0.3s, transform 0.2s ease, box-shadow 0.2s ease;
}
.navbar-nav .nav-link:hover {
  color: #ffe5d5;
  transform: translateY(-2px) scale(1.05);
  box-shadow: 0 4px 6px rgba(0,0,0,0.15);
}

.navbar-brand {
  transition: transform 0.2s ease;
}
.navbar-brand:hover {
  transform: scale(1.05);
}

.navbar-toggler {
  transition: transform 0.2s ease;
}
.navbar-toggler:hover {
  transform: scale(1.1);
}
</style>