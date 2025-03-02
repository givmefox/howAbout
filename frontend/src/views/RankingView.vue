<template>
  <div>
    <!-- 메인 콘텐츠 -->
    <div class="centered-content">
      <h2 style="color: #ff0000">🔥 유튜브 인기 키워드 랭킹 🔥</h2>

      <!-- 필터 섹션 -->
      <div class="filter-container">
        <label for="category-filter">카테고리 : </label>
        <select id="category-filter" v-model="selectedCategory">
          <option value="News & Politics">뉴스 및 정치</option>
          <option value="Music">음악</option>
          <option value="Sports">스포츠</option>
          <option value="Gaming">게임</option>
          <option value="Science & Technology">과학 및 기술</option>
        </select>
      </div>

      <!-- 로딩 표시 -->
      <div v-if="loading" class="loading">데이터 불러오는 중...</div>

      <!-- 랭킹 테이블 -->
      <div v-else class="hashtags">
        <table>
          <thead>
            <tr>
              <th>순위</th>
              <th>키워드</th>
              <th>카테고리</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="(keyword, index) in filteredKeywords.slice(0, 50)"
              :key="index"
            >
              <td>{{ keyword.rank }}</td>
              <td>
                <router-link
                  :to="`/keyword/${encodeURIComponent(keyword.name)}`"
                >
                  {{ keyword.name }}
                </router-link>
              </td>
              <td>{{ keyword.category }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import axios from "axios";

// 상태 변수
const keywordsByCategory = ref({});
const selectedCategory = ref("News & Politics");
const loading = ref(true); // 데이터 로딩 여부
const apiUrl = process.env.VUE_APP_API_URL;

// API에서 데이터 가져오기
const fetchKeywords = async () => {
  try {
    const response = await axios.get(`${apiUrl}/api/mongo-category-keywords`);
    if (response.data && response.data.data) {
      // 데이터를 카테고리별로 변환
      keywordsByCategory.value = response.data.data.reduce((acc, item) => {
        acc[item.category] = item.ranked_keywords.map((keyword) => ({
          rank: keyword.순위,
          name: keyword.키워드,
          category: item.category,
        }));
        return acc;
      }, {});
    }
  } catch (error) {
    console.error("❌ 데이터 불러오기 실패:", error);
  } finally {
    loading.value = false;
  }
};

// 컴포넌트가 마운트될 때 API 호출
onMounted(fetchKeywords);

// 카테고리 필터링
const filteredKeywords = computed(() => {
  return keywordsByCategory.value[selectedCategory.value]?.slice(0, 50) || [];
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

.loading {
  text-align: center;
  font-size: 18px;
  color: gray;
  margin-top: 20px;
}

.hashtags {
  display: flex;
  justify-content: center;
}

table {
  width: 80%;
  margin: auto;
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
