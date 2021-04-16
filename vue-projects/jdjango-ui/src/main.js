import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import ElementUI from 'element-ui';
// import './assets/styles/styles.scss'
import 'element-ui/lib/theme-chalk/index.css';
import 'normalize.css/normalize.css'
import 'nprogress/nprogress.css'

Vue.config.productionTip = false

Vue.use(ElementUI);

new Vue({
  router, // 挂载路由之后，所有组件可以用 this.$router 访问全局路由器；可以用 this.$route 访问当前组件的路由
  store,
  render: h => h(App)
}).$mount('#app')
