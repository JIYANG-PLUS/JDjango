/**
 * 专门的路由管理模块
 */

import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue' /* 立即加载 */

Vue.use(VueRouter) /* 注册路由组件 */

const routes = [ /* 路由集合 */
    {
        path: '/',
        name: 'Home', /* 命名路由：方便代码调用 */
        component: Home,
        alias: '/alias', /* alias 属性标识别名，当匹配路径 '/alias' 时 等同于匹配 '/' */
        /* 如果 props 被设置为 true，route.params 将会被设置为组件属性。 */
        props: true, /* 与当前的路由解耦，方便该组件能在任意地方使用 */
        /* props: route => ({ query: route.query.q }) */
    },
    {
        path: '/about', /* 可用 '/about/:id' 传递 id 参数值，通过 this.$route.params.id 获取传递的值 */
        // redirect: '/', // 路由重定向（只需指定path和redirect这两个属性）
        // redirect: {name: Home},
        name: 'About',
        component: () => import('../views/About.vue'), /* 延迟加载 */
        children: [
            /* 嵌套路由，无需加前缀 '/' 用法类似父路由写法 */
        ]
    },
    {
        path: '*' /* 通配符匹配所有路径，通常用于捕获 404 错误路径。 */
    },
    {
        path: '/combine',
        components: {
            default: Home, /* 默认显示的组件 */
            about: import('../views/About.vue'), /* 标签中使用 name = "about" 显示使用组件 */
        },
        props: {
            default: true,
            about: false
        }
    }
]

const router = new VueRouter({
    // mode: 'history', /* 去掉 很丑的 hash */
    routes
})

router.beforeEach((to, from, next) => {
    /* 导航路由切换时自动触发 */
    console.log(to, from)
    next() /* 跳转到 to 路由 */
    // next(false) /* 禁止跳转，回退到 from 路由 */
    // next('/') /* 或者 next({name: 'Home'}) */
})

export default router /* 让 main.js 访问到总路由 */
