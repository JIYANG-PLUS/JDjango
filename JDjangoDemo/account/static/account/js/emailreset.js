(()=>{
    "use strict";

    let SWITCH_EYE = 0;

    const ERRORS = {
        0: '缺少数字',
        1: '缺少字母',
        2: '缺少标点符号',
        3: '密码长度不够',
    };

    const btn_send = document.querySelector('button[type="submit"]');
    const btn_eye = document.getElementById('eye');
    const input_pwd = document.querySelector('input[name="password"]');
    const msg = document.getElementById('msg');
    const error_info = document.getElementById('error-info');

    function show_msg(n) {
        msg.classList.remove('green');
        msg.classList.remove('fa-check');
        msg.classList.add('red');
        msg.classList.add('fa-times');
        error_info.innerHTML = ERRORS[n];
        btn_send.style.background = '#aef5c2';
        btn_send.disabled = true;
    }

    function valid() {
        let password = input_pwd.value;
        let reg_digit = /[0-9]/;
        let reg_char = /[a-zA-Z]/;
        let reg_other = /[-!#\$%&\(\)\*\+,\.\/:;<=>?@[\]\^_`{|}~]/;
        if (!(password.length>=8&&password.length<=12)) {
            show_msg(3);
            return false;
        }
        if (!reg_digit.test(password)) {
            show_msg(0);
            return false;
        }
        if (!reg_char.test(password)) {
            show_msg(1);
            return false;
        }
        if (!reg_other.test(password)) {
            show_msg(2);
            return false;
        }
        return true
    }

    input_pwd.addEventListener('keyup', ()=>{
        if (valid()) {
            error_info.innerHTML = "";
            msg.classList.remove('red');
            msg.classList.remove('fa-times');
            msg.classList.add('green');
            msg.classList.add('fa-check');
            btn_send.style.background = '#2ea44f';
            btn_send.disabled = false;
        }
    });

    btn_eye.addEventListener('click', ()=>{
        if (0 == SWITCH_EYE) {
            btn_eye.classList.remove('fa-eye-slash');
            btn_eye.classList.add('fa-eye');
            input_pwd.setAttribute('type', 'text');
            SWITCH_EYE = 1;
        } else {
            btn_eye.classList.remove('fa-eye');
            btn_eye.classList.add('fa-eye-slash');
            input_pwd.setAttribute('type', 'password');
            SWITCH_EYE = 0;
        }
    });
})();