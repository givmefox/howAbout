<template>
  <Navbar />
  <div class="main-container">
    <SearchBar />
  </div>
  <router-view />
</template>

<script>
import Navbar from './components/NavbarComponent.vue';
import SearchBar from "./components/SearchBarComponent.vue";

export default{
  name: 'App',
  data() {
  },
  methods: {
  },
  components: {
    Navbar: Navbar,
    SearchBar: SearchBar,
  }
}
</script>

<style>
body {
  margin: 0 auto;
  padding: 20px;
  text-align: center;
}

.main-container {
  display: flex;
  justify-content: center; /* 검색창 중앙 정렬 */
  align-items: center;
  height: 10vh; /* 높이 조정 */
}
</style>
