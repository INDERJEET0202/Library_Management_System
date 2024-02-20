import { createRouter, createWebHistory } from 'vue-router'
import HomePage from "../views/Home/HomePage.vue"
import UserLogin from "../views/Auth/UserLogin.vue"
import LibrarianLogin from "../views/Auth/LibrarianLogin.vue"
import UserSignup from "../views/Auth/UserSignup.vue"
import UserDashboard from "../views/Dashboard/UserDashboard.vue"
import NotFound from "../views/NotFound/NotFound.vue"
import AdminLogin from "../views/Admin/AdminLogin.vue"
import AdminPage from "../views/Admin/AdminPage.vue"

const routes = [
    {
        path: '/',
        name: 'Home',
        component: HomePage,
    },
    {
        path: '/userlogin',
        name: 'UserLogin',
        component: UserLogin,
        meta: {
            title: "User Login | LMS"
        },
        beforeEnter: (to, from, next) => {
            const accessToken = localStorage.getItem('accessToken');
            if (accessToken) {
                next({ name: 'UserDashboard' });
            } else {
                next();
            }
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
        },
        beforeEnter: (to, from, next) => {
            const accessToken = localStorage.getItem('accessToken');
            if (accessToken) {
                next({ name: 'UserDashboard' });
            } else {
                next();
            }
        }
    },
    {
        path: "/user/dashboard",
        name: "UserDashboard",
        component: UserDashboard,
        meta: {
            title: "User Dashboard | LMS"
        },
        beforeEnter: (to, from, next) => {
            const accessToken = localStorage.getItem('accessToken');
            if (!accessToken) {
                next({ name: 'UserLogin' });
            } else {
                next();
            }
        }
    },
    {
        path: "/:catchAll(.*)", 
        component: NotFound, 
        meta: {
            title: "Page Not Found | LMS"
        }
    },
    {
        path: "/adminlogin",
        name: "AdminLogin",
        component: AdminLogin,
        meta: {
            title: "Admin Login | LMS"
        }
    },
    {
        path: "/admin/dashboard",
        name: "AdminPage",
        component: AdminPage,
        meta: {
            title: "Admin Dashboard | LMS"
        },
        beforeEnter: (to, from, next) => {
            const accessToken = localStorage.getItem('accessToken');
            if (!accessToken) {
                next({ name: 'Home' });
            } else {
                next();
            }
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