<template>
  <div class="search-bar">
    <input
      type="text"
      :value="searchQuery"
      placeholder="키워드를 검색하세요..."
      @input="handleInput"
      @compositionstart="handleCompositionStart"
      @compositionend="handleCompositionEnd"
      @keyup.enter="emitSearch"
    />

    <ul v-if="suggestions.length" class="suggestions">
      <li
        v-for="(s, i) in suggestions"
        :key="i"
        @click="selectSuggestion(s)"
        :class="{ active: selectedIndex === i }"
      >
        {{ s }}
      </li>
    </ul>

    <button @click="emitSearch">검색</button>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from "vue";
import { useRouter } from "vue-router";
import axios from "axios";
import debounce from "lodash/debounce"; // lodash 사용 시

const searchQuery = ref("");
const suggestions = ref([]);
const selectedIndex = ref(-1); // 🔥 키보드 선택용
const router = useRouter();
const apiUrl = process.env.VUE_APP_API_URL;

const isComposing = ref(false);

const handleInput = (e) => {
  const value = e.target.value;
  searchQuery.value = value; // 직접 업데이트!
  if (!isComposing.value) {
    fetchSuggestions(value); // 바로 전달
  }
};

const handleCompositionEnd = (e) => {
  isComposing.value = false;
  searchQuery.value = e.target.value; // 조합 완료된 값 반영
  getSuggestions(e.target.value); // 즉시 실행
};

// 🔹 자동완성 함수
const getSuggestions = async (value) => {
  const query = value ?? searchQuery.value;
  if (!query) {
    suggestions.value = [];
    return;
  }

  const words = query.split(" ");

  try {
    if (words.length === 1) {
      const res = await axios.get(`${apiUrl}/api/keyword-suggest`, {
        params: { q: words[0] },
      });
      suggestions.value = res.data.slice(0, 14);
    } else if (words.length >= 2) {
      const res = await axios.get(`${apiUrl}/api/mongo-related-suggest`, {
        params: { q: words[0] },
      });
      const mapped = res.data.map((r) => `${words[0]} > ${r.split(" > ")[1]}`);
      suggestions.value = mapped.slice(0, 14);
    }
    selectedIndex.value = -1;
  } catch (e) {
    console.error("❌ 자동완성 에러:", e);
    suggestions.value = [];
  }
};

const fetchSuggestions = debounce(getSuggestions, 200);

const selectSuggestion = (s) => {
  const selected = s.includes(">") ? s.split(" > ")[1] : s;
  const words = searchQuery.value.split(" ");
  searchQuery.value = words.length > 1 ? `${words[0]} ${selected}` : selected;

  emitSearch();
};

const emitSearch = () => {
  if (searchQuery.value.trim()) {
    router.push(`/keyword/${encodeURIComponent(searchQuery.value.trim())}`);
    suggestions.value = [];
  }
};

// 🔹 키보드 이벤트 핸들링
const handleKeyDown = (e) => {
  if (!suggestions.value.length) return;

  if (e.key === "ArrowDown") {
    selectedIndex.value = (selectedIndex.value + 1) % suggestions.value.length;
  } else if (e.key === "ArrowUp") {
    selectedIndex.value =
      (selectedIndex.value - 1 + suggestions.value.length) %
      suggestions.value.length;
  } else if (e.key === "Enter" && selectedIndex.value !== -1) {
    selectSuggestion(suggestions.value[selectedIndex.value]);
  }
};

// 🔹 mount 시 이벤트 등록
onMounted(() => {
  window.addEventListener("keydown", handleKeyDown);
});
onUnmounted(() => {
  window.removeEventListener("keydown", handleKeyDown);
});
</script>

<style scoped>
.search-bar {
  position: relative;
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

.suggestions {
  position: absolute;
  top: 50px;
  left: 0;
  right: 0;
  background: white;
  border: 1px solid #ccc;
  border-radius: 4px;
  list-style: none;
  width: 100%;
  max-width: 500px;
  margin: 0 auto;
  padding: 0;
  z-index: 1000;
}

.suggestions li {
  text-align: left;
  padding: 10px 12px;
  cursor: pointer;
  transition: background 0.2s;
}

.suggestions li:hover,
.suggestions li.active {
  background-color: #e5e5e5;
  font-weight: bold;
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
