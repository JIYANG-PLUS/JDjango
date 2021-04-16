<template>
  <div id="app">
    <div id="nav">
      <router-link to="/">HelloWorld</router-link> | 
      <router-link to="/list/HHH">列表演示</router-link> | 
      <router-link to="/css">CSS 样式控制</router-link> | 
      <router-link to="/events">界面事件处理</router-link> | 
      <router-link to="/vmodel">v-model 演示大全</router-link> | 
      <router-link to="/usesub">组件复用演示</router-link> | 
      <router-link to="/checklist">复选框组件交互示范列表</router-link>
    </div>
    <router-view/>
  </div>
</template>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}

#nav {
  padding: 30px;
  color: #a38c9a;
}

#nav a {
  font-weight: bold;
  color: #2c3e50;
}

#nav a.router-link-exact-active {
  color: #42b983;
}
</style>
