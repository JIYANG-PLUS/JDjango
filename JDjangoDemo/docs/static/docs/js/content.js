(()=>{
    "use strict";

    // 接口链接复制
    const btn_copy = document.querySelector('button.copy');
    const span_copy_content = document.querySelector('span#copy-content');
    const span_ph_success = document.querySelector('span#copy-success');
    // 无序调用拷贝
    const btn_disorder_copy = document.querySelector('button#copy-disorder');
    const span_disorder = document.querySelector('span#span-disorder');
    const span_disorder_success = document.querySelector('span#disorder-ok');
    // 有序调用拷贝
    const btn_order_copy = document.querySelector('button#copy-order');
    const span_order = document.querySelector('span#span-order');
    const span_order_success = document.querySelector('span#order-ok');
    // 提示信息互斥
    const SUCCESS = [
        span_ph_success,
        span_disorder_success,
        span_order_success
    ]
    function span_success_none() {
        SUCCESS.forEach(x=>{
            x.style.display = 'none';
        });
    }

    btn_copy.addEventListener('click', ()=>{
        window.getSelection().selectAllChildren(span_copy_content); // 获取选中的内容
        let bool = document.execCommand("copy");
        if (bool) {
            span_success_none();
            span_ph_success.style.display = 'block';
        } else {
            alert('未知错误');
        }
    });
    btn_disorder_copy.addEventListener('click', ()=>{
        window.getSelection().selectAllChildren(span_disorder); // 获取选中的内容
        let bool = document.execCommand("copy");
        if (bool) {
            span_success_none();
            span_disorder_success.style.display = 'block';
        } else {
            alert('未知错误');
        }
    });
    btn_order_copy.addEventListener('click', ()=>{
        window.getSelection().selectAllChildren(span_order); // 获取选中的内容
        let bool = document.execCommand("copy");
        if (bool) {
            span_success_none();
            span_order_success.style.display = 'block';
        } else {
            alert('未知错误');
        }
    });

})();