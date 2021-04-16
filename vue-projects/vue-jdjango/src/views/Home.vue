<template>
  <div class="home">
    <HelloWorld msg="Welcome to Your Vue.js App"/>
  </div>
</template>

<script>
import HelloWorld from '@/components/HelloWorld.vue' /* @ 是 /src 的别名 */

export default {
  name: 'Home',
  components: {
    HelloWorld,
  }
}
</script>
