<template>
  <div>
    <div class="centered-content">
      <h2 class="title">🔥 유튜브 인기 키워드 랭킹 🔥</h2>

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

      <div v-else class="table-wrapper">
        <table>
          <thead>
            <tr>
              <th>순위</th>
              <th>키워드</th>
              <th>등락</th>
              <th>이전 순위</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(keyword, index) in filteredKeywords" :key="index">
              <td>{{ index + 1 }}</td>
              <td>
                <router-link
                  :to="`/keyword/${encodeURIComponent(keyword.keyword)}`"
                >
                  {{ keyword.keyword }}
                </router-link>
              </td>
              <td>
                <span
                  v-if="keyword.previous_rank === null"
                  style="color: green; font-weight: bold"
                >
                  NEW
                </span>
                <span
                  v-else-if="keyword.rank_change > 0"
                  style="color: red; font-weight: bold"
                >
                  ▲ {{ keyword.rank_change }}
                </span>
                <span
                  v-else-if="keyword.rank_change < 0"
                  style="color: blue; font-weight: bold"
                >
                  ▼ {{ -keyword.rank_change }}
                </span>
                <span
                  v-else-if="keyword.rank_change === 0"
                  style="color: gray; font-weight: bold"
                >
                  –
                </span>
              </td>
              <td>{{ keyword.previous_rank ?? "—" }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from "vue";
import axios from "axios";
import { useRoute, useRouter } from "vue-router";

const route = useRoute();
const router = useRouter();

const selectedCategory = ref(route.query.category || "News & Politics");
const selectedPeriod = ref(route.query.period || "today");
const allKeywords = ref({});
const loading = ref(true);
const apiUrl = process.env.VUE_APP_API_URL;

const categoryMap = {
  25: "News & Politics",
  10: "Music",
  17: "Sports",
  20: "Gaming",
  28: "Science & Technology",
};

const fetchKeywords = async () => {
  loading.value = true;
  try {
    const response = await axios.get(
      `${apiUrl}/api/ranking/${selectedPeriod.value}`
    );
    const result = response.data || {};

    const mapped = {};
    for (const id in result) {
      const categoryName = categoryMap[id] || id;
      mapped[categoryName] = result[id];
    }
    allKeywords.value = mapped;
  } catch (error) {
    console.error("❌ 데이터 불러오기 실패:", error);
  } finally {
    loading.value = false;
  }
};

onMounted(fetchKeywords);

watch([selectedPeriod], async () => {
  router.replace({
    query: {
      ...route.query,
      category: selectedCategory.value,
      period: selectedPeriod.value,
    },
  });
  await fetchKeywords();
});

const filteredKeywords = computed(() => {
  return allKeywords.value[selectedCategory.value] || [];
});
</script>

<style scoped>
.centered-content {
  text-align: center;
  margin-top: 60px;
  padding: 20px;
}

.title {
  color: #e60023;
  font-size: 28px;
  margin-bottom: 30px;
}

.filter-container {
  margin-bottom: 20px;
}

.filter-container select {
  padding: 8px 12px;
  font-size: 16px;
  border-radius: 8px;
  border: 1px solid #ccc;
}

.loading {
  font-size: 18px;
  color: gray;
  margin-top: 20px;
}

.table-wrapper {
  overflow-x: auto;
}

table {
  width: 70%;
  margin: 0 auto;
  border-collapse: separate;
  border-spacing: 0;
  font-size: 16px;
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

th,
td {
  padding: 12px 15px;
  border-bottom: 1px solid #eee;
  text-align: center;
}

th {
  background-color: #e60023;
  color: white;
  font-weight: 600;
}

tr:hover {
  background-color: #f9f9f9;
}
</style>
