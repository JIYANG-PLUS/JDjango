const RURL = 'http://127.0.0.1:8000/';

(()=>{
    "use strict";

    const div_link_nlog = document.querySelector('div.div-link-blog');
    const btn_touch_add = document.getElementById('btn_touch_add');
    const btn_touch_modify = document.getElementById('btn_touch_modify');
    const btn_cancels = document.querySelectorAll('button.form-cancel');

    if (btn_touch_add) {
        btn_touch_add.addEventListener('click', ()=>{
            div_link_nlog.style.display = 'flex';
            div_link_nlog.children[0].style.display = 'flex';
            div_link_nlog.children[1].style.display = 'none';
        });
    }
    if (btn_cancels.length > 0) {
        btn_cancels.forEach(btn_cancel=>{
            btn_cancel.addEventListener('click', ()=>{
                div_link_nlog.style.display = 'none';
            });
        });
    }
    if (btn_touch_modify) {
        btn_touch_modify.addEventListener('click', ()=>{
            div_link_nlog.style.display = 'flex';
            div_link_nlog.children[0].style.display = 'none';
            div_link_nlog.children[1].style.display = 'flex';
            const id = document.querySelector('input[name="id"]').value;
            // 从服务器获取旧数据
            jQuery.ajax({
                type: "GET",
                url: `${RURL}docs/json/modify/sample/${id}/`,
                data: null,
                dataType: "json",
                timeout: 3000,
                success: (x)=>{
                    document.querySelector('textarea[name="content-modify"]').value = x.content;
                },
                error: ()=>{
                    alert("网络问题，无法获取旧代码样例。");
                }
            })
        });
    }
})(); // 新增和修改代码样例

(()=>{
    "use strict";

    const btn_cancel_modify_article = document.querySelector('button.common-cancel');
    const btn_modify_article = document.querySelector('button#btn-modify-article');
    const aside_add_plug = document.querySelector('div.aside-add-plug');

    btn_cancel_modify_article.addEventListener('click', ()=>{
        aside_add_plug.style.display = 'none';
    });

    btn_modify_article.addEventListener('click', ()=>{
        aside_add_plug.style.display = 'flex';
        const pk = document.getElementById('menu_pk').value;
        jQuery.ajax({
            type: "GET",
            url: `${RURL}docs/json/modify/article/${pk}/`,
            data: null,
            dataType: "json",
            timeout: 3000,
            success: (x)=>{
                document.querySelector('input[name="plugin_name"]').value = x.name;
                document.querySelector('input[name="plugin_label"]').value = x.label;
                document.querySelector('input[name="plugin_abstract"]').value = x.abstract;
                document.querySelector('input[name="plugin_version"]').value = x.version;
                document.querySelector('textarea[name="plugin_content"]').value = x.content;
                if (x.isvisible) {
                    document.querySelector('input[name="plugin_isvisible"]').checked = true;
                } else {
                    document.querySelector('input[name="plugin_isvisible"]').checked = false;
                }
            },
            error: ()=>{
                alert("网络问题，无法获取旧代码样例。");
            }
        })
    });
})(); // 文章内容修改
