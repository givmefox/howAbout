<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import axios from "axios";

const router = useRouter();
const isModalOpen = ref(false);
const userid = ref("");
const password = ref("");
const errorMessage = ref("");
const isLoggedIn = ref(false);
const username = ref("");

// ✅ 로그인 모달 열기
const openModal = () => {
  isModalOpen.value = true;
  window.addEventListener("keydown", escClose);
};

// ✅ 로그인 모달 닫기
const closeModal = () => {
  isModalOpen.value = false;
  userid.value = "";
  password.value = "";
  window.removeEventListener("keydown", escClose);
};

// ✅ ESC 키로 모달 닫기
const escClose = (event) => {
  if (event.key === "Escape") {
    closeModal();
  }
};

// ✅ 회원가입 페이지 이동
const goToRegister = () => {
  router.push("/register");
  isModalOpen.value = false;
};

// ✅ 로그인 요청
const login = async () => {
  if (!userid.value || !password.value) {
    errorMessage.value = "아이디와 비밀번호를 입력하세요!";
    return;
  }

  try {
    console.log("로그인 요청:", userid.value, password.value);

    const response = await axios.post("/api/auth/login", {
      userid: userid.value,
      password: password.value,
    });

    if (response.data.access_token) {
      // ✅ JWT 토큰 저장
      localStorage.setItem("token", response.data.access_token);
      isLoggedIn.value = true;
      username.value = response.data.username; // ✅ 사용자명 저장
      alert("로그인 성공! 🎉");
      closeModal();
      router.push("/");
    } else {
      errorMessage.value = "로그인 실패! 다시 확인해주세요.";
    }
  } catch (error) {
    console.error("로그인 오류:", error);
    errorMessage.value = error.response?.data?.message || "로그인 중 오류 발생";
  }
};

// ✅ 로그아웃 처리
const logout = () => {
  localStorage.removeItem("token");
  isLoggedIn.value = false;
  username.value = "";
  router.push("/");
};

// ✅ 페이지 로드시 로그인 상태 유지
onMounted(() => {
  const token = localStorage.getItem("token");
  if (token) {
    isLoggedIn.value = true;

    // ✅ 토큰을 이용해 사용자 정보 가져오기
    axios
      .get("http://localhost:3000/auth/me", {
        headers: { Authorization: `Bearer ${token}` },
      })
      .then((response) => {
        username.value = response.data.username;
      })
      .catch(() => {
        logout(); // 토큰이 유효하지 않으면 로그아웃
      });
  }
});
</script>

<template>
  <nav class="navbar">
    <a href="#" class="logo">이거어때</a>
    <div>
      <a href="/">Home</a>
      <router-link to="/Ranking">Ranking</router-link>
      <a href="#">About</a>
      <template v-if="isLoggedIn">
        <span class="welcome-message">환영합니다, {{ username }}님!</span>
        <button class="logout-btn" @click="logout">Logout</button>
      </template>
      <button v-else class="login-btn" @click="openModal">Login</button>
    </div>
  </nav>

  <!-- 로그인 모달 -->
  <div v-if="isModalOpen" class="modal-overlay" @click="closeModal">
    <div class="modal-content" @click.stop>
      <h2>로그인</h2>
      <div class="form-group">
        <label>아이디</label>
        <input type="text" v-model="userid" placeholder="아이디를 입력하세요" />
      </div>
      <div class="form-group">
        <label>비밀번호</label>
        <input
          type="password"
          v-model="password"
          placeholder="비밀번호를 입력하세요"
        />
      </div>
      <p class="error" v-if="errorMessage">{{ errorMessage }}</p>
      <button class="modal-btn" @click="login">로그인</button>
      <button class="register-btn" @click="goToRegister">회원가입</button>
      <button class="close-btn" @click="closeModal">닫기</button>
    </div>
  </div>
</template>

<style scoped>
.navbar {
  display: flex;
  background: #dd3333;
  padding: 20px;
  justify-content: space-between;
  align-items: center;
}

.navbar a {
  color: #fff;
  text-decoration: none;
  padding: 1em;
  margin-right: 13px;
}

.logo {
  font-size: 22px;
  font-weight: bold;
  color: white;
  text-decoration: none;
}

.welcome-message {
  color: white;
  margin-right: 10px;
}

.login-btn,
.logout-btn {
  background-color: white;
  color: #dd3333;
  border: none;
  padding: 10px 15px;
  font-size: 16px;
  font-weight: bold;
  cursor: pointer;
  border-radius: 10px;
}

.login-btn:hover {
  transform: scale(1.1);
}

.logout-btn {
  background-color: #444;
  color: white;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 999;
}

.modal-content {
  background: white;
  padding: 20px;
  border-radius: 10px;
  width: 350px;
  text-align: center;
  box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.3);
}

.form-group {
  margin: 15px 0;
  text-align: left;
}

input {
  width: 93%;
  padding: 10px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 5px;
  outline: none;
}

.modal-btn {
  padding: 10px;
  width: 100%;
  background-color: red;
  color: white;
  border: none;
  cursor: pointer;
  border-radius: 5px;
  margin-top: 15px;
}

.register-btn {
  padding: 10px;
  width: 100%;
  background-color: rgb(232, 66, 20);
  color: white;
  border: none;
  cursor: pointer;
  border-radius: 5px;
  margin-top: 15px;
}

.close-btn {
  padding: 10px;
  width: 100%;
  background-color: gray;
  color: white;
  border: none;
  cursor: pointer;
  border-radius: 5px;
  margin-top: 15px;
}
</style>
