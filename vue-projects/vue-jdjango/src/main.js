/**
 * 入口 JS，通常取名 main.js
 */

import Vue from 'vue' /* 导入 Vue 实例 */
import App from './App.vue' /* 程序的根组件 */
import router from './router' /* 导入路由 */
import store from './store' /* 导入组件交互 */

Vue.config.productionTip = false/* 非生产环境 */

new Vue({
 router,
 store,
 render: h => h(App) /* 渲染函数，渲染页面 */
}).$mount('#app')
