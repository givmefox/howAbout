<template>
        <nav class="navbar">
            <a href="#" class="logo">여기어때</a>
            <div>
                <a href="#">Home</a>
                <a href="#">Chart</a>
                <a href="#">About</a>
                <button class="login-btn">Login</button>
            </div> 
        </nav>
</template>
    
<script>
    export default{
        name: 'NavbarComponent',
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
</style>