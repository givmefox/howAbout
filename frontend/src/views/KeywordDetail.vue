<template>
  <div>
    <!-- 키워드 제목 -->
    <div class="keyword-title">키워드: {{ keyword }}</div>

    <!-- 연관 키워드 -->
    <div class="related-keywords">
      <h3>🔗 연관 키워드</h3>
      <div class="tags">
        <span
          v-for="tag in relatedKeywords"
          :key="tag"
          @click="goToKeyword(tag)"
          class="keyword-tag"
        >
          #{{ tag }}
        </span>
      </div>
    </div>

    <!-- 콘텐츠 -->
    <div class="content">
      <div class="related-videos">
        <h3>연관 동영상</h3>
        <div v-for="video in videos" :key="video.video_id" class="video-item">
          <img
            :src="getThumbnailUrl(video.video_id)"
            :alt="video.title"
            class="video-thumbnail"
          />
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
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from "vue";
import { useRoute, useRouter } from "vue-router";
import axios from "axios";

const route = useRoute();
const router = useRouter();
const keyword = ref(route.params.keyword || "알 수 없음");
const apiUrl = process.env.VUE_APP_API_URL;
const relatedKeywords = ref([]);
const videos = ref([]);

// 특정 키워드의 연관 키워드 및 관련 동영상 데이터를 가져오는 함수
const fetchKeywordDetails = async () => {
  try {
    console.log(`Fetching details for keyword: ${keyword.value}`);

    // 연관 키워드 가져오기
    const relatedResponse = await axios.get(
      `${apiUrl}/api/mongo-related-keywords`,
      {
        params: { keyword: keyword.value },
      }
    );
    const keywordData = relatedResponse.data.data.find(
      (item) => item.keyword === keyword.value
    );
    relatedKeywords.value = keywordData?.related || [];

    // 인기 영상 데이터 가져오기
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
  } catch (error) {
    console.error("❌ 데이터 불러오기 실패:", error);
  }
};

// 유튜브 썸네일 URL 생성 함수
const getThumbnailUrl = (videoId) => {
  return `https://img.youtube.com/vi/${videoId}/hqdefault.jpg`;
};

// 유튜브 동영상 URL 생성 함수
const getVideoUrl = (videoId) => {
  return `https://www.youtube.com/watch?v=${videoId}`;
};

// 연관 키워드 클릭 시 해당 키워드 페이지로 이동
const goToKeyword = (newKeyword) => {
  if (newKeyword !== keyword.value) {
    router.push(`/keyword/${encodeURIComponent(newKeyword)}`);
  }
};

onMounted(() => {
  fetchKeywordDetails();
});

// 키워드가 변경될 때마다 데이터를 다시 가져옴
watch(
  () => route.params.keyword,
  (newKeyword) => {
    keyword.value = newKeyword;
    fetchKeywordDetails();
  },
  { immediate: true }
);
</script>

<style scoped>
.related-keywords {
  margin: 15px 0;
  padding: 10px;
  background-color: #f5f5f5;
  border-radius: 8px;
}

.keyword-tag {
  display: inline-block;
  background-color: #e0f7fa;
  color: #007bff;
  padding: 8px 12px;
  margin: 5px;
  border-radius: 16px;
  cursor: pointer;
  font-weight: bold;
  font-size: 14px;
  transition: background-color 0.3s;
}

.keyword-tag:hover {
  background-color: #b2ebf2;
}

.related-videos {
  background-color: #f9f9f9;
  border-radius: 8px;
  padding: 15px;
  width: 100%;
  max-width: 600px;
}

.keyword-title {
  width: 100%;
  text-align: center;
  background-color: #f0f0f0;
  padding: 15px 0;
  margin-bottom: 20px;
  font-size: 24px;
  font-weight: bold;
}

.content {
  width: 100%;
  display: flex;
  gap: 20px;
  padding: 20px;
  box-sizing: border-box;
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
  object-fit: cover;
  border-radius: 5px;
}

.video-info {
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.video-title {
  font-size: 16px;
  color: #007bff;
  text-decoration: none;
}

.video-title:hover {
  text-decoration: underline;
}
</style>
