<template>
  <div>
    <div class="centered-content">
      <h2 style="color: #ff0000">🔥 유튜브 인기 키워드 랭킹 🔥</h2>

      <div class="filter-container">
        <label for="category-filter">카테고리 : </label>
        <select id="category-filter" v-model="selectedCategory">
          <option value="News & Politics">뉴스 및 정치</option>
          <option value="Music">음악</option>
          <option value="Sports">스포츠</option>
          <option value="Gaming">게임</option>
          <option value="Science & Technology">과학 및 기술</option>
        </select>

        <label for="period-filter" style="margin-left: 20px">기간 : </label>
        <select id="period-filter" v-model="selectedPeriod">
          <option value="today">오늘</option>
          <option value="week">이번 주</option>
          <option value="month">이번 달</option>
        </select>
      </div>

      <div v-if="loading" class="loading">데이터 불러오는 중...</div>

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
const keywordsByCategory = ref({});
const selectedCategory = ref(route.query.category || "News & Politics");
const selectedPeriod = ref(route.query.period || "today");
const loading = ref(true);
const apiUrl = process.env.VUE_APP_API_URL;

// ✅ 카테고리 ID → 이름 매핑
const categoryMap = {
  25: "News & Politics",
  10: "Music",
  17: "Sports",
  20: "Gaming",
  28: "Science & Technology",
};

const mapCategoryIdToName = (id) => {
  return categoryMap[id] || "기타";
};

const fetchKeywords = async () => {
  loading.value = true;
  try {
    const response = await axios.get(
      `${apiUrl}/api/ranking/${selectedPeriod.value}`
    );
    if (response.data) {
      const result = response.data;
      keywordsByCategory.value = {};

      for (const categoryId in result) {
        const categoryName = mapCategoryIdToName(categoryId);
        keywordsByCategory.value[categoryName] = result[categoryId].map(
          (item, index) => ({
            rank: index + 1,
            name: item.keyword,
            category: categoryName,
          })
        );
      }
    }
  } catch (error) {
    console.error("❌ 데이터 불러오기 실패:", error);
  } finally {
    loading.value = false;
  }
};

onMounted(fetchKeywords);

// ✅ 카테고리 또는 기간이 바뀌면 다시 fetch
watch(selectedPeriod, async (newPeriod) => {
  router.replace({
    query: {
      ...route.query,
      category: selectedCategory.value,
      period: newPeriod,
    },
  });
  await fetchKeywords();
  await nextTick(); // ✅ 데이터 갱신 후 DOM 업데이트 기다리기
  if ("scrollRestoration" in history) {
    window.scrollTo({
      top: history.state?.scroll?.top || 0,
      left: 0,
      behavior: "auto",
    });
  }
});

const filteredKeywords = computed(() => {
  return keywordsByCategory.value[selectedCategory.value]?.slice(0, 50) || [];
});

onMounted(async () => {
  await fetchKeywords();
  await nextTick();
  if ("scrollRestoration" in history) {
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
  padding: 10px 30px 10px 10px;
  font-size: 16px;
  border: 1px solid #ddd;
  border-radius: 5px;
  cursor: pointer;
  margin-right: 10px;
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
