z<template>
        <nav class="navbar">
            <a href="#" class="logo">여기어때</a>
            <div>
                <a href="#">Home</a>
                <a href="#">Chart</a>
                <a href="#">About</a>
                <button class="login-btn" @click="openModal">Login</button>
            </div> 
        </nav>

        <!-- 로그인 모달 -->
        <div v-if="isModalOpen" class="modal-overlay" @click="closeModal">
            <div class="modal-content" @click.stop>
                <h2>로그인</h2>
                <div class="form-group">
                    <label>아이디</label>
                    <input type="text" v-model="username" placeholder="아이디를 입력하세요">
                </div>
                <div class="form-group">
                    <label>비밀번호</label>
                    <input type="password" v-model="password" placeholder="비밀번호를 입력하세요">
                </div>
                <p class="error" v-if="errorMessage">{{ errorMessage }}</p>
                <button class="modal-btn" @click="login">로그인</button>
                <button class="close-btn" @click="closeModal">닫기</button>
            </div>
        </div>
</template>
    
<script>
    export default {
        name: 'NavbarComponent',
        data() {
            return {
                isModalOpen: false,
                username: "",
                password: "",
                errorMessage: ""
            };
        },
        methods: {
            openModal() {
                this.isModalOpen = true;
                window.addEventListener("keydown", this.escClose);
            },
            closeModal() {
                this.isModalOpen = false;
                window.removeEventListener("keydown", this.escClose);
            },
            escClose(event){
                if (event.key === "Escape") {
                    this.closeModal();
                }
            },
            login(){
                if (!this.username || !this.password) {
                    this.errorMessage = "아이디와 비밀번호를 입력하세요!";
                } else {
                    alert("로그인 시도: "+ this.username);
                    this.errorMessage = "";
                    this.closeModal();
                }
            }
        }
    }
</script>
    
<style>
    .navbar{
        display: flex;
        background: #dd3333;
        padding: 20px;
        justify-content: space-between; 
        align-items: center;
    }

    .navbar a{
        color:  #fff;
        text-decoration: none;
        padding: 1em;
    }

    .logo {
        font-size: 22px;
        font-weight: bold;
        color: white;
        text-decoration: none;
    }

    .login-btn {
        background-color: white;
        color: #dd3333;
        border: none;
        padding: 10px 15px;
        font-size: 16px;
        font-weight: bold;
        cursor: pointer;
        border-radius: 5px;
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