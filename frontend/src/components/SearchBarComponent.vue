<template>
    <div class="search-bar">
      <input 
        type="text" 
        v-model="searchQuery" 
        placeholder="키워드를 검색하세요..." 
        @keyup.enter="emitSearch"
      />
      <button @click="emitSearch">검색</button>
    </div>
  </template>
  
  <script setup>
  import { ref, defineEmits } from "vue";
  
  const searchQuery = ref(""); 
  const emit = defineEmits(["search"]);
  
  const emitSearch = () => {
    emit("search", searchQuery.value);
  };
  </script>
  
  <style scoped>
  .search-bar {
    display: flex;
    justify-content: center;
    align-items: center;
    margin: 20px 0;
  }
  
  .search-bar input {
    width: 500px;
    padding: 10px;
    font-size: 16px;
    border: 1px solid #ddd;
    border-radius: 5px;
    margin-right: 10px;
  }
  
  .search-bar button {
    padding: 10px 15px;
    background: #ff0000;
    color: white;
    border: none;
    cursor: pointer;
    border-radius: 5px;
  }
  
  .search-bar button:hover {
    background: #cc0000;
  }
  </style>
  