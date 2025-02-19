<template>
  <div>
    <!-- 메인 콘텐츠 -->
    <div class="centered-content">
      <h2 style="color: #ff0000">🔥 유튜브 인기 키워드 랭킹 🔥</h2>

      <!-- 필터 섹션 -->
      <div class="filter-container">
        <label for="category-filter">카테고리 : </label>
        <select id="category-filter" v-model="selectedCategory">
          <option value="all">전체</option>
          <option value="music">음악</option>
          <option value="sports">스포츠</option>
          <option value="movies">영화 및 애니메이션</option>
          <option value="gaming">게임</option>
          <option value="news">뉴스 및 정치</option>
        </select>
      </div>

      <!-- 랭킹 테이블 -->
      <div class="hashtags">
        <table>
          <thead>
            <tr>
              <th>순위</th>
              <th>키워드</th>
              <th>카테고리</th>
              <th>인기도 점수</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(keyword, index) in filteredKeywords" :key="index">
              <td>{{ index + 1 }}</td>
              <td>
                <router-link
                  :to="`/keyword/${encodeURIComponent(keyword.name)}`"
                >
                  {{ keyword.name }}
                </router-link>
              </td>
              <td>{{ keyword.category }}</td>
              <td>{{ keyword.score }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from "vue";

const searchQuery = ref("");
const selectedCategory = ref("all");
const keywords = ref([
  { name: "#뮤직히트", category: "music", score: 98 },
  { name: "#스포츠업데이트", category: "sports", score: 92 },
  { name: "#영화예고편", category: "movies", score: 88 },
  { name: "#게임트렌드", category: "gaming", score: 85 },
  { name: "#속보", category: "news", score: 83 },
  { name: "#팝히트", category: "music", score: 81 },
  { name: "#축구열기", category: "sports", score: 79 },
  { name: "#애니메이션버즈", category: "movies", score: 76 },
  { name: "#이스포츠월드", category: "gaming", score: 74 },
  { name: "#데일리정치", category: "news", score: 72 },
  { name: "#데일리정치", category: "news", score: 72 },
  { name: "#데일리정치", category: "news", score: 72 },
  { name: "#데일리정치", category: "news", score: 72 },
  { name: "#데일리정치", category: "news", score: 72 },
  { name: "#데일리정치", category: "news", score: 72 },
  { name: "#데일리정치", category: "news", score: 72 },
  { name: "#데일리정치", category: "news", score: 72 },
  { name: "#데일리정치", category: "news", score: 72 },
  { name: "#데일리정치", category: "news", score: 72 },
  { name: "#데일리정치", category: "news", score: 72 },
  { name: "#데일리정치", category: "news", score: 72 },
  { name: "#데일리정치", category: "news", score: 72 },
  { name: "#데일리정치", category: "news", score: 72 },
  { name: "#데일리정치", category: "news", score: 72 },
  { name: "#데일리정치", category: "news", score: 72 },
  { name: "#데일리정치", category: "news", score: 72 },
  { name: "#데일리정치", category: "news", score: 72 },
]);

// 카테고리 및 검색 필터링
const filteredKeywords = computed(() => {
  return keywords.value.filter((keyword) => {
    return (
      (selectedCategory.value === "all" ||
        keyword.category === selectedCategory.value) &&
      keyword.name.includes(searchQuery.value)
    );
  });
});
</script>

<style scoped>
.centered-content {
  text-align: center;
  margin-top: 60px;
}

.filter-container {
  margin: 30px auto;
  text-align: center;
}

.filter-container select {
  padding: 10px;
  font-size: 16px;
  border: 1px solid #ddd;
  border-radius: 5px;
}

.hashtags {
  display: flex;
  justify-content: center;
}

table {
  width: 80%;
  margin: auto; /* 테이블을 가운데 정렬 */
  border-collapse: collapse;
  font-size: 16px;
}

th,
td {
  padding: 10px;
  border: 1px solid #ddd;
}

th {
  background-color: #ff0000;
  color: white;
}
</style>
