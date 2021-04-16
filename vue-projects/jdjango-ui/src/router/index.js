// https://router.vuejs.org/
import Vue from 'vue'
import VueRouter from 'vue-router'
import HelloWorld from '@/views/Element/HelloWorld.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'HelloWorld',
    component: HelloWorld
  },
  {
    path: '/events',
    name: 'Events',
    component: () => import('../components/Normal/Events.vue')
  },
  {
    path: '/list/:name',
    name: 'List',
    component: () => import('../components/Normal/List.vue')
  },
  {
    path: '/css',
    name: 'CSS',
    component: () => import('../components/Normal/CSS.vue')
  },
  {
    path: '/vmodel',
    name: 'VModel',
    component: () => import('../components/Normal/VModel.vue')
  },
  {
    path: '/usesub',
    name: 'UseSub',
    component: () => import('../components/PropSample/UseSub.vue')
  },
  {
    path: '/checklist',
    name: 'checklist',
    component: () => import('../components/checkList/whole.vue')
  },
  // {
  //   path: '/about',
  //   name: 'About',
  //   // route level code-splitting
  //   // this generates a separate chunk (about.[hash].js) for this route
  //   // which is lazy-loaded when the route is visited.
  //   component: () => import(/* webpackChunkName: "about" */ '../views/About.vue')
  // }
]

const router = new VueRouter({
  routes // 等价于：routes: routes
})

export default router
