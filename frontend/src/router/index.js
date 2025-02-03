import { createRouter, createWebHistory } from "vue-router";
import RegisterView from "@/views/RegisterView.vue";

const router = createRouter({
    history: createWebHistory(),
    routes: [
        {
            path: "/register",
            name: "Register",
            component: RegisterView,
        },
    ],
});

export default router;