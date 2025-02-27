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
import { ref } from "vue"; // 'vue'에서 가져와야 합니다.
import { useRouter } from "vue-router";

const searchQuery = ref("");
const router = useRouter();

const emitSearch = () => {
  if (searchQuery.value.trim()) {
    router.push(`/keyword/${encodeURIComponent(searchQuery.value)}`);
  }
};
</script>

<style scoped>
.search-bar {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-wrap: wrap; /* 화면이 좁을 때 버튼이 자동으로 아래로 내려감 */
  gap: 10px;
  margin: 20px auto;
  width: 100%;
  max-width: 600px;
}

.search-bar input {
  flex: 1; /* 남는 공간을 채움 */
  min-width: 250px; /* 최소 크기 설정 */
  max-width: 500px; /* 최대 크기 제한 */
  padding: 12px;
  font-size: 16px;
  border: 1px solid #ddd;
  border-radius: 5px;
  outline: none;
}

.search-bar button {
  padding: 12px 15px;
  background: #ff0000;
  color: white;
  border: none;
  cursor: pointer;
  border-radius: 5px;
  font-size: 16px;
  transition: background 0.3s;
}

.search-bar button:hover {
  background: #cc0000;
}

/* 🔹 모바일 환경에서 최적화 */
@media screen and (max-width: 768px) {
  .search-bar {
    flex-direction: column;
    width: 100%;
  }

  .search-bar input {
    width: 90%;
  }

  .search-bar button {
    width: 90%;
  }
}
</style>
