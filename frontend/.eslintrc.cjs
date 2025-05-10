module.exports = {
    root: true,
    env: { browser: true, es2021: true },
    extends: [
      'standard',
      'plugin:vue/vue3-recommended'
    ],
    parserOptions: { ecmaVersion: 'latest', sourceType: 'module' },
    plugins: ['vue'],
    rules: {
      'no-console': 'off',
    }
  }  