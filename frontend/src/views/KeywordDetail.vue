<template>
  <div>
    <!-- 키워드 제목 -->
    <div class="keyword-title">키워드: {{ keyword }}</div>

    <!-- 연관 키워드 -->
    <div class="related-keywords">
      <h3>🔗 연관 키워드</h3>
      <div class="tags">
        <button
          v-for="tag in relatedKeywords"
          :key="tag"
          @click="goToKeyword(tag)"
          class="keyword-btn"
        >
          {{ tag }}
        </button>
      </div>
    </div>

    <!-- 콘텐츠 -->
    <div class="content">
      <div class="related-videos">
        <h3>연관 동영상</h3>
        <div v-for="video in videos" :key="video.id" class="video-item">
          <img
            :src="video.thumbnail"
            :alt="video.title"
            class="video-thumbnail"
          />
          <a :href="video.link" target="_blank" class="video-title">{{
            video.title
          }}</a>
        </div>
      </div>

      <!-- 인기 추이 그래프 -->
      <div class="chart-container">
        <h3>인기 추이</h3>
        <canvas ref="popularityChart"></canvas>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRoute } from "vue-router";
import Chart from "chart.js/auto";

const route = useRoute();
const keyword = ref(route.params.keyword || "알 수 없음");

// 예제 연관 키워드 데이터
const relatedKeywords = ref([
  "연관키워드1",
  "연관키워드2",
  "연관키워드3",
  "연관키워드4",
]);
// 예제 동영상 데이터
const videos = ref([
  {
    title:
      "LCK 컵 그룹배틀 전승 KDA 4️⃣9️⃣인 선수👤가 WORLDS 우승🏆 MSI 준우승🎭 리그 쓰리핏3️⃣ 있고요...",
    link: "https://www.youtube.com/watch?v=YIsOAxUbOnE",
    thumbnail: "https://img.youtube.com/vi/YIsOAxUbOnE/maxresdefault.jpg",
  },
  {
    title: "Example Video 2",
    link: "https://youtube.com/watch?v=2",
    thumbnail: "https://img.youtube.com/vi/2/hqdefault.jpg",
  },
  {
    title: "Example Video 3",
    link: "https://youtube.com/watch?v=3",
    thumbnail: "https://img.youtube.com/vi/3/hqdefault.jpg",
  },
  {
    title: "Example Video 4",
    link: "https://youtube.com/watch?v=4",
    thumbnail: "https://img.youtube.com/vi/4/hqdefault.jpg",
  },
  {
    title: "Example Video 5",
    link: "https://youtube.com/watch?v=5",
    thumbnail: "https://img.youtube.com/vi/5/hqdefault.jpg",
  },
]);

const popularityChart = ref(null);

// 그래프 생성
onMounted(() => {
  const ctx = popularityChart.value.getContext("2d");
  new Chart(ctx, {
    type: "line",
    data: {
      labels: ["1월", "2월", "3월", "4월", "5월", "6월", "7월", "8월"],
      datasets: [
        {
          label: "인기 점수",
          data: [50, 40, 60, 80, 70, 50, 90],
          borderColor: "rgba(255, 99, 132, 1)",
          backgroundColor: "rgba(255, 99, 132, 0.2)",
        },
      ],
    },
    options: {
      responsive: true,
    },
  });
});
</script>

<style scoped>
.related-videos {
  background-color: #f9f9f9;
  border-radius: 8px;
  padding: 15px;
  width: 100%;
  max-width: 400px;
}

/* 키워드 제목 */
.keyword-title {
  width: 100%;
  text-align: center;
  background-color: #f0f0f0;
  padding: 15px 0;
  margin-bottom: 20px;
  font-size: 24px;
  font-weight: bold;
}

/* 메인 콘텐츠 */
.content {
  width: 100%;
  height: calc(100vh - 60px);
  display: flex;
  gap: 20px;
  padding: 20px;
  box-sizing: border-box;
}

/* 인기 추이 그래프 */
.chart-container {
  flex: 4;
  text-align: center;
  background-color: #f9f9f9;
  border-radius: 5px;
  padding: 20px;
}

/* 연관 동영상 리스트 */
.video-list {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 20px;
  background-color: #f9f9f9;
  border-radius: 5px;
  padding: 20px;
}

.video-item {
  display: flex;
  align-items: center;
  gap: 12px;
  background: white;
  padding: 10px;
  border-radius: 5px;
  border: 1px solid #ddd;
  box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  margin-bottom: 10px;
}
.video-thumbnail {
  width: 120px;
  height: 90px;
  object-fit: cover; /* 잘림 방지 */
  border-radius: 5px;
}

.video-item img {
  width: 120px;
  height: 90px;
  object-fit: cover;
}

.video-item a {
  color: #007bff;
  text-decoration: none;
  font-size: 16px;
}

.video-item a:hover {
  text-decoration: underline;
}
</style>
