import { createRouter, createWebHistory } from 'vue-router'
import UserLogin from "../views/Auth/UserLogin.vue"
import LibrarianLogin from "../views/Auth/LibrarianLogin.vue"
import UserSignup from "../views/Auth/UserSignup.vue"

const routes = [
    {
        path: '/userlogin',
        name: 'UserLogin',
        component: UserLogin,
        meta: {
            title: "User Login | LMS"
        }
    },
    {
        path: '/librarianlogin',
        name: 'LibrarianLogin',
        component: LibrarianLogin,
        meta: {
            title: "Librarian Login | LMS"
        }
    },
    {
        path: '/usersignup',
        name: 'UserSignup',
        component: UserSignup,
        meta: {
            title: "User Signup | LMS"
        }
    }
]

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes
})

router.beforeEach((to, from, next) => {
    document.title = to.meta.title || 'Library Management System';
    next();
});

export default router