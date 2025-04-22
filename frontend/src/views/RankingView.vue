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
import { ref, computed, onMounted, watch } from "vue";
import { nextTick } from "vue";
import axios from "axios";
import { useRoute, useRouter } from "vue-router";

const route = useRoute();
const router = useRouter();
// 상태 변수
const keywordsByCategory = ref({});
const selectedCategory = ref(route.query.category || "News & Politics");
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

// selectedCategory가 변경될 때마다 URL 쿼리 갱신
watch(selectedCategory, (newCategory) => {
  router.replace({
    query: { ...route.query, category: newCategory },
  });
});

// 컴포넌트가 마운트될 때 API 호출
onMounted(async () => {
  await fetchKeywords();

  // ✅ 데이터를 다 불러오고 DOM이 렌더링된 뒤에 수동으로 스크롤 복원 요청
  await nextTick(); // DOM 업데이트 기다리기

  // savedPosition이 있는 경우에만 복원
  if ("scrollRestoration" in history) {
    // 이건 일부 브라우저가 자동으로 scrollRestoration=manual 일 때만 적용되기도 함
    window.scrollTo({
      top: history.state?.scroll?.top || 0,
      left: 0,
      behavior: "auto",
    });
  }
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
  appearance: none;
  -webkit-appearance: none;
  -moz-appearance: none;
  background: url("data:image/svg+xml;charset=US-ASCII,%3Csvg xmlns='http://www.w3.org/2000/svg' width='10' height='6'%3E%3Cpath fill='black' d='M0 0l5 6 5-6z'/%3E%3C/svg%3E")
    no-repeat right 10px center;
  background-color: white;
  background-size: 10px 6px;
  padding: 10px 30px 10px 10px; /* 오른쪽 패딩 조정 */
  font-size: 16px;
  border: 1px solid #ddd;
  border-radius: 5px;
  cursor: pointer;
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
