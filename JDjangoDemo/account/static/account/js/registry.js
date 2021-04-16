(()=>{
    "use strict";

    // <object data="{% static 'account/svg/eye.svg' %}"></object>

    jQuery.ajaxSetup({
        timeout: 2000,
        cache: false
    });

    const ERRORS = {
        0: '密码长度必须大于等于8，且小于等于12',
        1: '邮箱格式错误',
        2: '密码格式错误，必须由数字+字母+英文标点符号组成',
        3: '用户名不能为空',
        4: '账号长度不超过6位。',
        5: '请正确填写8位验证码',
        6: '请求服务器失败，网络异常或邮箱地址错误',
        7: '验证码无效',
        8: '检测到违规操作，请按顺序操作',
        9: '仅支持@qq.com、@foxmail.com、@163.com',
        10: '网络错误或邮箱不存在',
        11: '发送信息失败，请稍后再试',
        12: '该邮箱已被注册',
        13: '用户名已存在',
        100: '未知错误',
    };
    const SUCCESS = {
        0: '注册成功！',
    };

    let FLAG_SEE = 0;

    const input_username = document.querySelector("input[name='username']");
    const input_email = document.querySelector("input[name='email']");
    const input_password = document.querySelector("input[name='password']");
    const input_code = document.querySelector("input[name='code']");

    const div_msg_back = document.querySelector('div.msg-back');
    const div_error_msg = document.querySelector('div.error-msg');
    const div_success = document.querySelector('div.success');
    const div_success_msg = document.querySelector('div.success-msg');

    const btn_send_code = document.querySelector('button#send-code');
    const btn_create = document.querySelector('button#create');
    const btn_see = document.getElementById('btn-see');
 
    function show_msg(i) {
        div_error_msg.innerHTML = ERRORS[i];
        div_msg_back.style.display = 'flex';
    }
    function show_success(i) {
        div_success_msg.innerHTML = SUCCESS[i];
        div_success.style.display = 'flex';
    }

    // 验证输入的合法性
    function valid() {
        let username = input_username.value;
        let email = input_email.value;
        let password = input_password.value;
        let reg = /^([a-zA-Z]|[0-9])(\w|\-)+@[a-zA-Z0-9]+\.([a-zA-Z]{2,4})$/;
        let reg_digit = /[0-9]/;
        let reg_char = /[a-zA-Z]/;
        let reg_other = /[-!#\$%&\(\)\*\+,\.\/:;<=>?@[\]\^_`{|}~]/;
        let reg_all = /^([-!#\$%&\(\)\*\+,\.\/:;<=>?@[\]\^_`{|}~]|[0-9]|[a-zA-Z])*$/
        if (0 == username.length) {
            show_msg(3);
            return false;
        }
        if (username.length > 6) {
            show_msg(4);
            return false;
        }
        if (!reg.test(email)) {
            show_msg(1);
            return false;
        }
        if (!(password.length>=8&&password.length<=12)) {
            show_msg(0);
            return false;
        }
        if (!(reg_digit.test(password)&&reg_char.test(password)&&reg_other.test(password))) {
            show_msg(2);
            return false;
        } else {
            if (!(reg_all.test(password))) {
                show_msg(2);
                return false;
            }
        }
        return true
    }

    // 获取邮箱验证码
    btn_send_code.addEventListener('click', ()=>{
        if (valid()) {
            jQuery.ajax({
                type: "GET",
                url: `/account/json/code/${input_username.value}/${input_email.value}`,
                data: null,
                dataType: "json",
                success: (x)=>{
                    if ('success' === x.msg) {
                        btn_create.style.display = 'block';
                        input_username.disabled = true;
                        input_email.disabled = true;
                        input_password.disabled = true;
                        input_code.disabled = false;
                        btn_send_code.disabled = true;
                        btn_send_code.style.background = '#555555';
                        btn_send_code.innerHTML = '已发送';
                    } else {
                        if (1 === x.code) {
                            show_msg(9);
                        } else if (2 === x.code) {
                            show_msg(10);
                        } else if (3 === x.code) {
                            show_msg(11);
                        } else if (4 === x.code) {
                            show_msg(12);
                        } else if (5 === x.code) {
                            show_msg(13);
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
    // 创建用户
    btn_create.addEventListener('click', ()=>{
        let code = input_code.value;
        if (8 != code.length) {
            show_msg(5);
            return;
        }
        jQuery.ajax({
            type: "GET",
            url: `/account/json/registry/${input_username.value}/${input_email.value}/${input_password.value}/${code}`,
            data: null,
            dataType: "json",
            success: (x)=>{
                if ('success' == x.msg) {
                    show_success(0);
                } else {
                    if (2 === x.code) {
                        show_msg(7);
                    } else if (1 === x.code) {
                        show_msg(8);
                    } else if (3 === x.code) {
                        show_msg(13);
                    }else {
                        show_msg(100);
                    }
                }
            },
            error: ()=>{
                show_msg(6);
            }
        })
    });

    // 密码可见
    btn_see.addEventListener('click', ()=>{
        if (0 === FLAG_SEE) {
            input_password.setAttribute('type', 'text');
            btn_see.children[0].classList.remove('fa-eye-slash');
            btn_see.children[0].classList.add('fa-eye');
            FLAG_SEE = 1;
        } else {
            input_password.setAttribute('type', 'password');
            btn_see.children[0].classList.remove('fa-eye');
            btn_see.children[0].classList.add('fa-eye-slash');
            FLAG_SEE = 0;
        }
    });

    // 关闭错误提示框
    div_msg_back.addEventListener('click', ()=>{
        div_msg_back.style.display = 'none';
    });
})();
