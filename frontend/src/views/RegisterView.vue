<template>
    <div>
      <div class="container">
        <h2>회원가입</h2>
        <div class="form-group">
          <label>아이디</label>
          <input type="text" v-model="username" placeholder="아이디를 입력하세요">
        </div>
        <div class="form-group">
          <label>비밀번호</label>
          <input type="password" v-model="password" placeholder="비밀번호를 입력하세요">
        </div>
        <div class="form-group">
          <label>이메일</label>
          <input type="email" v-model="email" placeholder="이메일을 입력하세요">
        </div>
        <p class="error" v-if="errorMessage">{{ errorMessage }}</p>
        <button @click="register">회원가입</button>
      </div>
    </div>
  </template>
  
<script>
  
export default {
    name: "RegisterView",
    data() {
      return {
        username: "",
        password: "",
        email: "",
        errorMessage: ""
      };
    },
    methods: {
      async register() {
        try {
          alert("회원가입 기능 추가 예정!");
        } catch (error) {
          this.errorMessage = "회원가입 실패!";
        }
      }
    }
};
</script>

  <style>

</style>