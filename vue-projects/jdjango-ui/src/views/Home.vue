<template>
  <div class="app">
    <List :todos="todos"></List>
    <CSS />
    <Events />
    <VModel />
  </div>
</template>

<script>
// @ 是 /src 的 别名
import axios from "axios";
import List from "@/components/Normal/List.vue";
import CSS from "@/components/Normal/CSS.vue";
import Events from "@/components/Normal/Events.vue";
import VModel from "@/components/Normal/VModel.vue"

export default {
  components: {
    List,
    CSS,
    Events,
    VModel,
  },
  data() {
    return {
      todos: [], // 只有在 data 中显式申明的变量才是可使用的变量
    };
  },
  async created() {
    const res = await axios.get("https://jsonplaceholder.typicode.com/todos");
    this.todos = res.data;
  },
};
</script>
