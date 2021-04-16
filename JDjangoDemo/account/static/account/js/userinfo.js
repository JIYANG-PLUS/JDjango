const RURL = 'http://127.0.0.1:8000';

(()=>{
    "use strict";

    const btn_generate_only_code = document.getElementById('show_generate_only_code');
    const btn_get_code = document.getElementById('get_code');
    const btn_generate_code = document.getElementById('generate_code');
    const div_send_and_back = document.querySelector('div.send_and_back');
    // const div_send_code = document.querySelector('div.div-send-code');
    const div_generate_code = document.querySelector('div.div-generate-code');

    if (btn_generate_only_code) {
        btn_generate_only_code.addEventListener('click', ()=>{
            div_send_and_back.style.display = 'block';
        });
    }
    

    if (btn_get_code) {
        btn_get_code.addEventListener('click', ()=>{
            // 发送验证码
            jQuery.ajax({
                type: "GET",
                url: `${RURL}/account/json/onlycodesendemail/`,
                data: null,
                dataType: "json",
                timeout: 3000,
                success: (x)=>{
                    btn_get_code.disabled = true;
                    div_send_and_back.children[1].innerHTML = '# 邮件发送成功，请耐心等待接收。若长时间未收到邮件，请刷新本界面后重新发送';
                    div_generate_code.style.display = 'flex';
                },
                error: ()=>{
                    alert("网络问题，无法获取验证码。");
                }
            })
        });
    }
    
    if (btn_generate_code) {
        btn_generate_code.addEventListener('click', ()=>{
            const code = div_generate_code.children[0].value;
            if (8 !== code.trim().length) {
                alert("请正确填写8位验证码。");
            } else {
                jQuery.ajax({
                    type: "GET",
                    url: `${RURL}/account/json/generateonlycode/${code}/`,
                    data: null,
                    dataType: "json",
                    timeout: 3000,
                    success: (x)=>{
                        if ('success' === x.msg) {
                            alert('生成成功，即将刷新页面。');
                            window.location.reload();
                        } else {
                            alert('验证码填写错误或已失效。');
                        }
                    },
                    error: ()=>{
                        alert("网络问题，无法生成。");
                    }
                })
            }
        })
    }
})(); // 验证和生成唯一码

(()=>{
    "use strict";

    const btn_only_code_copy = document.getElementById('copy-only-code');
    const token_code = document.getElementById('token-code');

    if (btn_only_code_copy) {
        btn_only_code_copy.addEventListener('click', ()=>{
            window.getSelection().selectAllChildren(token_code);
            let bool = document.execCommand("copy");
            if (bool) {
                alert('拷贝成功');
            } else {
                alert('拷贝失败');
            }
        });
    }
})(); // 复制

((args)=>{
    "use strict";

    let swits = {}
    args.forEach((x)=>{ swits[x[2]] = 0; })

    let init_btns = function(button, div, swit_name) {
        button.style.color = 'rgb(4,124,161)';
        div.style.display = 'none';
        swits[swit_name] = 0;
    }

    let active_btns = function(button, div, swit_name) {
        button.style.color = 'rgb(233, 18, 197)';
        div.style.display = 'block';
        swits[swit_name] = 1;
    }

    let clear_other_btns_status = function(button) {
        for (let i = args.length-1; i>=0; --i) {
            if (button !== args[i][0]) {
                init_btns(
                    document.getElementById(args[i][0]), 
                    document.getElementById(args[i][1]), 
                    args[i][2]
                ); // 按钮状态还原
            } else {
                active_btns(
                    document.getElementById(args[i][0]), 
                    document.getElementById(args[i][1]), 
                    args[i][2]
                );// 仅触发一次
            }
        }
    }

    args.forEach((x)=>{
        document.getElementById(x[0]).addEventListener('click',()=>{
            clear_other_btns_status(x[0]);
        })
    })
})(
    [
        ['btn-base-info','right-base-info','swit_base_info'],
        ['btn-only-code','right-only-code','swit_only_code'],
        ['btn-valid-code','right-valid-code','swit_valid_code'],
        ['btn-modify-info','right-modify-info','swit_modify_info'],
        ['btn-continue','right-vaild-continue','swit_continue'],
    ]
); // 页面切换

(()=>{
    "use strict";

    const btn_plugin_32only = document.getElementById('btn-plugin-32only');
    const btn_sure_sq = document.getElementById('btn-sure-sq');
    const input_plugin_32only = document.getElementById('input-plugin-32only');

    if (btn_plugin_32only) {
        btn_plugin_32only.addEventListener('click', ()=>{
            const p32 = input_plugin_32only.value;
            if (32 !== p32.length) {
                alert("请检查32位接口唯一码的正确性。");
                return;
            }
            jQuery.ajax({
                type: "GET",
                url: `${RURL}/docs/json/checkpluginactive/${p32}/`,
                data: null,
                dataType: "json",
                timeout: 3000,
                success: (x)=>{
                    if ('success' === x.msg) {
                        input_plugin_32only.setAttribute('readonly', true);
                        btn_plugin_32only.disabled = true;
                        // 验证成功后，显示生成按钮
                        document.getElementById('second-name').innerHTML = x.title;
                        document.getElementById('second-link').innerHTML = x.url;
                        document.getElementById('second-valid').innerHTML = x.isvalid;
                        document.querySelector('div.second').style.display = 'block';
                    } else {
                        alert("接口不存在或未激活，请联系管理员激活。");
                    }
                },
                error: ()=>{
                    alert("网络问题，无法验证接口是否已激活。");
                }
            })
        });
    }
    
    if (btn_sure_sq) {
        btn_sure_sq.addEventListener('click', ()=>{
            const p32 = input_plugin_32only.value;
            jQuery.ajax({
                type: "GET",
                url: `${RURL}/docs/json/authorizationcode/${p32}/`,
                data: null,
                dataType: "json",
                timeout: 3000,
                success: (x)=>{
                    if ('success' === x.msg) {
                        alert("申请成功，即将刷新界面。");
                        window.location.reload();
                    } else {
                        alert("您已申请，若想继续使用，请前往续约模块操作。");
                    }
                },
                error: ()=>{
                    alert("网络问题，无法继续操作。");
                }
            })
        });
    }
})(); // 授权码操作【新增等】

(()=>{
    "use strict";

    const btn_continue_valid = document.getElementById('continue-valid');
    const btn_continue_do = document.getElementById('continue-do');
    const input_continue_plugin_32only = document.getElementById('continue-plugin-32only');

    if (btn_continue_valid) {
        btn_continue_valid.addEventListener('click', ()=>{
            const p32 = input_continue_plugin_32only.value;
            if (32 !== p32.length) {
                alert("请检查32位接口唯一码的正确性。");
                return;
            }
            jQuery.ajax({
                type: "GET",
                url: `${RURL}/docs/json/checkpluginactivecontinue/${p32}/`,
                data: null,
                dataType: "json",
                timeout: 3000,
                success: (x)=>{
                    if ('success' === x.msg) {
                        input_continue_plugin_32only.setAttribute('readonly', true);
                        btn_continue_valid.disabled = true;
                        // 验证成功后，显示生成按钮
                        document.getElementById('con-second-name').innerHTML = x.title;
                        document.getElementById('con-second-link').innerHTML = x.url;
                        document.querySelector('div.right-vaild-continue-2').style.display = 'block';
                    } else {
                        alert("不符合续约条件。");
                    }
                },
                error: ()=>{
                    alert("网络问题，无法进行续约操作。");
                }
            })
        });
    }
    
    if (btn_continue_do) {
        btn_continue_do.addEventListener('click', ()=>{
            const p32 = input_continue_plugin_32only.value;
            jQuery.ajax({
                type: "GET",
                url: `${RURL}/docs/json/continueplugin/${p32}/`,
                data: null,
                dataType: "json",
                timeout: 3000,
                success: (x)=>{
                    if ('success' === x.msg) {
                        alert("续约成功，即将刷新界面。");
                        window.location.reload();
                    } else {
                        alert("不符合续约条件。");
                    }
                },
                error: ()=>{
                    alert("网络问题，无法进行续约操作。");
                }
            })
        });
    }
})(); // 续约
