(()=>{
    "use strict";

    jQuery.ajaxSetup({
        timeout: 2000,
        cache: false
    });

    const btn_send = document.querySelector('button#send');
    const input_email = document.querySelector('input[name="email"]');

    const div_msg_back = document.querySelector('div.msg-back');
    const div_error_msg = document.querySelector('div.error-msg');

    const span_info = document.querySelector('span#info');
    const span_time = document.querySelector('span#time');

    const ERRORS = {
        0: '请输入邮箱',
        1: '邮箱格式错误',
        2: '邮箱不存在',
        6: '请求服务器失败，网络异常或邮箱地址错误',
        100: '未知错误',
    };

    let TIME = 60;

    function show_msg(i) {
        div_error_msg.innerHTML = ERRORS[i];
        div_msg_back.style.display = 'flex';
    }

    // 验证输入的合法性
    function valid() {
        let email = input_email.value;
        let reg = /^([a-zA-Z]|[0-9])(\w|\-)+@[a-zA-Z0-9]+\.([a-zA-Z]{2,4})$/;
        if (0 == email.length) {
            show_msg(0);
            return false;
        }
        if (!reg.test(email)) {
            show_msg(1);
            return false;
        }
        return true
    }

    function f() {
        span_time.innerHTML = `${TIME}秒`;
        span_time.style.display = 'inline-block';
        TIME -= 1;
    }

    function invoke(f, start, interval, end) {
        if (!start) start = 0;
        if (arguments.length <= 2) {
            setTimeout(f, start);
        } else {
            setTimeout(repeat, start);
            function repeat() {
                var h = setInterval(f, interval);
                if (end) setTimeout(()=>{ 
                    clearInterval(h);
                    TIME = 60;
                    btn_send.disabled = false;
                    btn_send.style.background = "#2ea44f";
                    span_time.style.display = 'none';
                    span_info.innerHTML = '重新发送';
                }, end);
            }
        }
    }
    
    // 发送验证码
    btn_send.addEventListener('click', ()=>{
        if (valid()) {
            jQuery.ajax({
                type: "GET",
                url: `/account/json/passwordreset/${input_email.value}`,
                data: null,
                dataType: "json",
                success: (x)=>{
                    if ('success' === x.msg) {
                        span_info.innerHTML = '验证成功，已发送，请注意查收';
                        btn_send.disabled = true;
                        btn_send.style.background = "#8cdfa4";
                        // btn_send.setAttribute('type', 'submit');
                        invoke(f, 0, 1000, 62000);
                    } else {
                        if (1 === x.code) {
                            show_msg(2);
                        } else {
                            show_msg(100);
                        }
                    }
                },
                error: ()=>{
                    show_msg(6);
                }
            })
        }
    });

    // 关闭错误提示框
    document.querySelector('button#btn-error-msg').addEventListener('click', ()=>{
        div_msg_back.style.display = 'none';
    });
})();
