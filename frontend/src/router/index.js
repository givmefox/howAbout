import { createRouter, createWebHistory } from "vue-router";
import RegisterView from "@/views/RegisterView.vue";
import RankingView from "@/views/RankingView.vue";
import KeywordDetail from "@/views/KeywordDetail.vue";

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

        { 
            path: '/keyword/:keyword', 
            component: KeywordDetail, 
            props: true 
        },
    ],
});

export default router;