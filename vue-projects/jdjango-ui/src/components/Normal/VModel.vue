<template>
    <div id="vmodel">
        <h1>v-model 用法大全</h1>
        <p>可以用 v-model 在【input】、【text】、【textarea】、【select】、【checkbox】、【radio】标签上创建数据的双向绑定。</p>
        <p>v-model 会忽略所有表单元素的初始值，应该在 data 中声明初始值。</p>
        <p>修饰符：.lazy 表示触发change事件后同步；.number 表示将值转为数值类型；.trim 表示忽略首尾空白字符。</p>

        <!-- 文本 -->
        <div>
            <h2>input['text'] 文本【字符串】</h2>
            <input type="text" v-model="inputValue" placeholder="此处输入，右侧虚线框显示"><span>{{ inputValue }}</span>
        </div>

        <!-- 多行文本 -->
        <div>
            <h2>textarea 多行文本【字符串】</h2>
            <textarea v-model="textareaValue" placeholder="此处输入多行文本，下侧实时显示输入内容" rows="3" style="width: 100%;"></textarea>
            <p>{{ textareaValue }}</p>
        </div>

        <!-- 单复选框 -->
        <div>
            <h2>input['checkbox'] 单复选框【布尔值】</h2>
            <!-- 模式一 -->
            <input type="checkbox" v-model="checkboxValue" id="checkbox"><label for="checkbox">{{ checkboxValue ? '选中' : '未选中' }}</label>
            <!-- 模式二 -->
            <br>
            <input type="checkbox" v-model="checkboxValueBind" true-value="yes" false-value="no" id="checkboxValueBind"><label for="checkboxValueBind">{{ checkboxValueBind }}</label>
        </div>

        <!-- 多复选框 -->
        <div>
            <h2>input['checkbox'] 多复选框【列表】</h2>
            <p>除了绑定 v-model 外，多复选框必须要设置 value 属性值。</p>
            <span>第一组：</span>
            <input type="checkbox" v-model="checkboxsValue" id="A" value="A"><label for="A">A</label> |
            <input type="checkbox" v-model="checkboxsValue" id="B" value="B"><label for="B">B</label> |
            <input type="checkbox" v-model="checkboxsValue" id="C" value="C"><label for="C">C</label>
            <br>
            <span>第二组：</span>
            <input type="checkbox" v-model="checkboxs2Value" id="D" value="D"><label for="D">D</label> |
            <input type="checkbox" v-model="checkboxs2Value" id="E" value="E"><label for="E">E</label> |
            <input type="checkbox" v-model="checkboxs2Value" id="F" value="F"><label for="F">F</label>
            <p>组1已选中的值：{{ checkboxsValue }}</p>
            <p>组2已选中的值：{{ checkboxs2Value }}</p>
        </div>

        <!-- 单选按钮 -->
        <div>
            <h2>input['radio'] 单选按钮【字符串】</h2>
            <p>同样的，必须要指定属性 value 的值。</p>
            <!-- 模式一 -->
            <input type="radio" id="G" value="A" v-model="radioValue"><label for="G">A</label>
            <input type="radio" id="H" value="B" v-model="radioValue"><label for="H">B</label>
            <input type="radio" id="I" value="C" v-model="radioValue"><label for="I">C</label>
            <input type="radio" id="J" value="D" v-model="radioValue"><label for="J">D</label>
            <p>单选值：{{ radioValue }}</p>
            <!-- 模式二 -->
            <input type="radio" id="K" v-model="radioValueK" :value="a"><label for="K">{{ a }}-{{ radioValueK }}</label>
            <input type="radio" id="L" v-model="radioValueK" :value="b"><label for="L">{{ b }}-{{ radioValueK }}</label>
        </div>

        <!-- 下拉选择框 -->
        <div>
            <h2>select-option 选择框【字符串】</h2>
            <!-- 模式一 （若提供value，则value是selectValue的首选项） -->
            <select v-model="selectValue">
                <option disabled>请选择</option>
                <option value="A">A选项</option>
                <option>B</option>
                <option>C</option>
            </select>
            <p>选择框值：{{ selectValue }}</p>
            <!-- 模式二 -->
            <select v-model="selected">
                <option :value="{ number: 123 }">123</option>
            </select>
            <p>选项为对象：{{ selected }}</p>
        </div>

        <!-- 多选-下拉选择框 -->
        <div>
            <h2>select-option 多选-选择框【列表】</h2>
            <select v-model="selectsValue" multiple>
                <option value="A">A选项</option>
                <option>B</option>
                <option>C</option>
            </select>
            <p>多选-选择框值：{{ selectsValue }}</p>
        </div>
    </div>
</template>


<script>
export default {
    name: 'VModel',
    data() {
        return {
            inputValue: '',
            textareaValue: '',
            checkboxValue: true,
            checkboxValueBind: 'yes',
            checkboxsValue: [], // 默认都不选中
            checkboxs2Value: [],
            radioValue: '',
            selectValue: '', // 默认为禁用选项
            selectsValue: [],
            radioValueK: '',
            a: 'a',
            b: 'b',
            selected: '',
        }
    },
    methods: {

    },
}
</script>


<style>
div#vmodel { border: 6px solid rgb(28, 197, 57); border-radius: 10px; padding: 3px 6px; margin: 6px 0; }
div#vmodel > h1 { text-align: center; border-bottom: 3px solid black; }
div#vmodel > div { border: 1px solid rgb(33, 12, 226); padding: 6px 12px; margin: 6px 0;}
p {color: rgb(106, 107, 199);}
</style>