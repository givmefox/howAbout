<template>
  <div>
    <!-- 키워드 제목 -->
    <div class="keyword-title">키워드: {{ keyword }}</div>

    <!-- 연관 키워드 + 키워드 통계 -->
    <div class="related-keywords-and-detail">
      <div class="related-keywords">
        <h3>🔗 연관 키워드</h3>
        <v-data-table
          :headers="keywordHeaders"
          :items="relatedKeywordsTable"
          class="elevation-1"
          dense
          hide-default-footer
        >
          <template v-slot:[`item.keyword`]="{ item }">
            <span @click="goToKeyword(item.keyword)" class="clickable-keyword">
              #{{ item.keyword }}
            </span>
          </template>
        </v-data-table>
      </div>

      <!-- 키워드 트렌드 그래프 -->
      <div class="trend-chart">
        <h3>📊 키워드 트렌드</h3>
        <canvas ref="trendChart"></canvas>
      </div>
    </div>

    <!-- 콘텐츠 -->
    <div class="content">
      <div class="related-videos">
        <h3>📺 연관 동영상</h3>
        <div
          v-for="video in paginatedVideos"
          :key="video.video_id"
          class="video-item"
        >
          <!-- 썸네일 + 제목 -->
          <!-- ✅ 썸네일 -->
          <img
            :src="getThumbnailUrl(video.video_id)"
            :alt="video.title"
            class="video-thumbnail"
          />

          <!-- ✅ 제목 -->
          <div class="video-info">
            <a
              :href="getVideoUrl(video.video_id)"
              target="_blank"
              class="video-title"
            >
              {{ video.title }}
            </a>
          </div>
        </div>

        <div class="pagination-controls">
          <button @click="prevPage" :disabled="currentPage === 1">
            ⬅ 이전
          </button>
          <button
            @click="nextPage"
            :disabled="currentPage >= Math.ceil(videos.length / itemsPerPage)"
          >
            다음 ➡
          </button>
        </div>
      </div>

      <div v-if="keywordDetail" class="keyword-stats">
        <h3>📌 키워드 통계</h3>
        <ul>
          <li>조회수: {{ keywordDetail.view_count.toLocaleString() }}</li>
          <li>좋아요: {{ keywordDetail.like_count.toLocaleString() }}</li>
          <li>댓글 수: {{ keywordDetail.comment_count.toLocaleString() }}</li>
          <li>선호도: {{ keywordDetail.preference }}</li>
          <li>참여도: {{ keywordDetail.engagement }}</li>
          <li>성장 가능성: {{ keywordDetail.growth_score }}</li>
          <li>선호도 등급: {{ keywordDetail.preference_grade }}</li>
          <li>참여도 등급: {{ keywordDetail.engagement_grade }}</li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, nextTick, computed } from "vue";
import { useRoute, useRouter } from "vue-router";
import axios from "axios";
import Chart from "chart.js/auto";

const route = useRoute();
const router = useRouter();
const keyword = ref(route.params.keyword || "알 수 없음");
const apiUrl = process.env.VUE_APP_API_URL;
const relatedKeywordsTable = ref([]);
const videos = ref([]);
const keywordDetail = ref(null);
const trendChart = ref(null);
let chartInstance = null;
const currentPage = ref(1);
const itemsPerPage = 5;

const keywordHeaders = [
  { text: "순위", value: "rank" },
  { text: "연관 키워드", value: "keyword" },
  { text: "검색량", value: "search_volume" },
  { text: "관련성 점수", value: "relevance" },
];

const fetchKeywordDetails = async () => {
  try {
    const relatedResponse = await axios.get(
      `${apiUrl}/api/mongo-related-keywords`,
      {
        params: { keyword: keyword.value },
      }
    );
    const keywordData = relatedResponse.data.data.find(
      (item) => item.keyword === keyword.value
    );
    relatedKeywordsTable.value = (keywordData?.related || []).map(
      (item, index) => ({
        rank: index + 1,
        keyword: item,
      })
    );

    const videoResponse = await axios.get(
      `${apiUrl}/api/mongo-keyword-videos`,
      {
        params: { keyword: keyword.value },
      }
    );
    videos.value = videoResponse.data.data
      .filter((item) => item.keyword === keyword.value)
      .flatMap((item) =>
        item.videos.map((video) => ({
          video_id: video.video_id,
          title: video.title,
          score: video.score,
        }))
      );

    const detailResponse = await axios.get(
      `${apiUrl}/api/keyword-detail/${encodeURIComponent(keyword.value)}`
    );
    keywordDetail.value = detailResponse.data;

    generateMockChartData();
  } catch (error) {
    console.error("❌ 데이터 불러오기 실패:", error);
  }
};

const getThumbnailUrl = (videoId) =>
  `https://img.youtube.com/vi/${videoId}/hqdefault.jpg`;
const getVideoUrl = (videoId) => `https://www.youtube.com/watch?v=${videoId}`;

const goToKeyword = (newKeyword) => {
  if (newKeyword !== keyword.value) {
    router.push(`/keyword/${encodeURIComponent(newKeyword)}`);
  }
};

const generateMockChartData = async () => {
  await nextTick();
  if (chartInstance) chartInstance.destroy();

  const ctx = trendChart.value.getContext("2d");
  const mockDates = [
    "1월",
    "2월",
    "3월",
    "4월",
    "5월",
    "6월",
    "7월",
    "8월",
    "9월",
    "10월",
  ];
  const mockValues = Array.from({ length: mockDates.length }, () =>
    Math.floor(Math.random() * 100)
  );

  chartInstance = new Chart(ctx, {
    type: "line",
    data: {
      labels: mockDates,
      datasets: [
        {
          label: "검색량",
          data: mockValues,
          borderColor: "#007bff",
          backgroundColor: "rgba(0, 123, 255, 0.2)",
          fill: true,
          tension: 0.4,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        x: { title: { display: true, text: "월별" } },
        y: { title: { display: true, text: "검색량" } },
      },
    },
  });
};

onMounted(fetchKeywordDetails);

watch(
  () => route.params.keyword,
  (newKeyword) => {
    keyword.value = newKeyword;
    fetchKeywordDetails();
  },
  { immediate: true }
);

const paginatedVideos = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage;
  const end = start + itemsPerPage;
  return videos.value.slice(start, end);
});

const nextPage = () => {
  if (currentPage.value < Math.ceil(videos.value.length / itemsPerPage)) {
    currentPage.value++;
  }
};

const prevPage = () => {
  if (currentPage.value > 1) {
    currentPage.value--;
  }
};
</script>

<style scoped>
/* 상단: 연관 키워드 + 키워드 통계 */
.related-keywords-and-detail {
  display: flex;
  justify-content: space-between;
  gap: 20px;
  padding: 10px 20px;
  flex-wrap: wrap;
}

.related-videos {
  flex: 0.4; /* 40% */
  min-width: 280px;
  max-width: 500px;
}

.keyword-stats {
  flex: 0.6; /* 60% */
  min-width: 320px;
  max-width: 700px;
}

/* 키워드 통계 */
.keyword-stats {
  background-color: #ffffff;
  border: 1px solid #ddd;
  padding: 15px;
  border-radius: 8px;
  font-size: 15px;
  line-height: 1.8;
}
.keyword-stats ul {
  list-style-type: none;
  padding: 0;
}
.keyword-stats li {
  margin-bottom: 4px;
}

/* 연관 키워드 테이블 */
.related-keywords {
  padding: 8px;
  background-color: #f5f5f5;
  border-radius: 8px;
}

/* 연관 키워드 항목 클릭 */
.clickable-keyword {
  color: #007bff;
  cursor: pointer;
  font-weight: bold;
  text-decoration: none;
}
.clickable-keyword:hover {
  text-decoration: underline;
}

/* 콘텐츠: 연관 동영상 + 트렌드 그래프 */
.content {
  width: 100%;
  display: flex;
  gap: 20px;
  padding: 20px;
  box-sizing: border-box;
  flex-wrap: wrap;
}

.related-keywords,
.trend-chart {
  flex: 1;
  min-width: 300px;
  max-width: 600px;
}

/* 키워드 트렌드 차트 */
.trend-chart {
  background-color: white;
  padding: 15px;
  border-radius: 8px;
  border: 1px solid #ddd;
  height: 320px; /* ✅ 고정 높이 필수 */
  overflow: hidden;
  position: relative;
  flex: 1;
  min-width: 300px;
  max-width: 600px;
}

/* 연관 동영상 카드 */
.related-videos {
  background-color: #f9f9f9;
  border-radius: 8px;
  padding: 15px;
}

.trend-chart canvas {
  display: block;
  width: 100% !important;
  height: 100% !important;
}

.video-item {
  display: flex; /* ✅ 가로 정렬로 변경 */
  align-items: center;
  border: 1px solid #ddd;
  padding: 10px;
  border-radius: 5px;
  background-color: #fff;
  margin-bottom: 15px;
  gap: 12px; /* 썸네일과 제목 사이 간격 */
}

.pagination-controls {
  display: flex;
  justify-content: space-between;
  margin-top: 10px;
}

.video-thumbnail {
  width: 120px;
  height: 90px;
  object-fit: cover;
  border-radius: 5px;
}

.video-info {
  flex: 1;
}

.video-title {
  font-size: 16px;
  color: #007bff;
  text-decoration: none;
}

.video-title:hover {
  text-decoration: underline;
}

/* 키워드 타이틀 */
.keyword-title {
  width: 100%;
  text-align: center;
  background-color: #f0f0f0;
  padding: 15px 0;
  margin-bottom: 20px;
  font-size: 24px;
  font-weight: bold;
}
</style>
