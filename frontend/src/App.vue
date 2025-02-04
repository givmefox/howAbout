<template>
  <Navbar />
  <router-view />
</template>

<script>
import Navbar from './components/NavbarComponent.vue';

export default{
  name: 'App',
  data() {
  },
  methods: {
  },
  components: {
    Navbar: Navbar,
  }
}
</script>

<style>
body {
  margin: 0 auto;
  padding: 20px;
}

h1, h2, h3 {
  margin-bottom: 1rem;
}

p {
  margin-bottom: 0.5rem;
}

button {
  margin-right: 10px;
}
</style>
