import { createRouter, createWebHistory } from "vue-router";
import RegisterView from "@/views/RegisterView.vue";
import RankingView from "@/views/RankingView.vue";

const router = createRouter({
    history: createWebHistory(),
    routes: [
        {
            path: "/register",
            name: "Register",
            component: RegisterView,
        },

        {
            path: "/ranking",
            name: "Ranking",
            component: RankingView,
        },
    ],
});

export default router;