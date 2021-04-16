<template>
    <div class="whole">
        <inputCtl/>
        <showlist :datas="datas" :deleteItem="deleteItem"/>
        <buttonCtl :checked="checked"/>
    </div>
</template>

<script>
import buttonCtl from './buttonCtl.vue'
import inputCtl from './inputCtl.vue'
import showlist from './showlist.vue'
export default {
    data() {
        return {
            datas: [
                {checked: false, name: 'AAA'},
                {checked: true, name: 'BBB'},
            ],
            checked: false,
        }
    },
    components: {
        buttonCtl,
        inputCtl,
        showlist,
    },
    methods: {
        deleteItem(index) {
            this.datas.splice(index, 1)
        }
    }
}
</script>

<style>
.whole{
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    padding: 12px;
    margin: 12px;
    border: 1px solid black;
}
</style>
