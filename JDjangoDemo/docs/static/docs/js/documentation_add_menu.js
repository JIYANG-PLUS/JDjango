(()=>{
    "use strict";

    jQuery.ajaxSetup({
        timeout: 2000,
        cache: false
    });

    const btn_ad_rootmenu = document.querySelector('button.btn-add-rootmenu');
    const btn_adds = document.querySelectorAll('button.btn-add-menu');
    const btn_dels = document.querySelectorAll('button.btn-del-menu');
    const btn_mods = document.querySelectorAll('button.btn-mod-menu');
    const btn_plug_adds = document.querySelectorAll('button.btn-add-plug');
    const btn_cancels = document.querySelectorAll('button.common-cancel');
    const btn_submit = document.querySelector('button#add-btn-submit');
    const btn_del_menu = document.querySelector('button#btn-del-menu');
    const btn_modify = document.querySelector('button#mod-btn-submit');

    // 大容器
    const aside = document.querySelector('div.aside');
    const aside_add_h1 = document.querySelector('div.aside-add-menu>h1>span');
    const aside_del_h1 = document.querySelector('div.aside-del-menu>h1>span');
    const aside_mod_h1 = document.querySelector('div.aside-mod-menu>h1>span');

    const ALL_ASIDE = [
        'div.aside-add-menu',
        'div.aside-del-menu',
        'div.aside-mod-menu',
        'div.aside-add-plug',
    ]

    // 新增、删除、修改三者只可显示一个
    function show_aside(v) {
        ALL_ASIDE.forEach(a=>{
            const t = document.querySelector(a);
            if (a !== v) { // 隐藏
                t.style.display = 'none';
            } else { // 显示
                t.style.display = 'block';
            }
        });
    }

    // 自动赋值控件
    const input_add_pk = document.querySelector('input[name="add-pk"]');
    const input_mod_pk = document.querySelector('input[name="mod-pk"]');
    const input_mod_name = document.querySelector('input[name="mod-name"]');
    const textarea_mod_describe = document.querySelector('textarea[name="mod-describe"]');
    const input_mod_order = document.querySelector('input[name="mod-order"]');
    const input_mod_isroot = document.querySelector('input[name="mod-isroot"]');
    const input_add_isroot = document.querySelector('input[name="add-isroot"]');
    const input_mod_visible = document.querySelector('input[name="mod-isvisible"]');

    const span_del_pk = document.querySelector('span#del-pk');
    // 新增根节点
    btn_ad_rootmenu.addEventListener('click', ()=>{
        aside.style.display = 'flex';
        show_aside('div.aside-add-menu');
        input_add_pk.value = '0'; // 根节点标志
        input_add_isroot.checked = true;
        input_add_isroot.disabled = true;
    });

    // 新增节点
    btn_adds.forEach(btn=>{
        btn.addEventListener('click', ()=>{
            let pk = btn.dataset.pk.slice(2);
            aside.style.display = 'flex';
            show_aside('div.aside-add-menu');
            input_add_pk.value = pk;
            input_add_isroot.checked = false;
            input_add_isroot.disabled = true;
            // 获取标题
            jQuery.ajax({
                type: "GET",
                url: `/docs/json/pk2name/${pk}/`,
                data: null,
                dataType: "json",
                success: (x)=>{
                    aside_add_h1.innerHTML = `【${x.name}...】`;
                },
                error: ()=>{
                    alert("网络问题，无法新增。");
                }
            })
        });
    });

    // 删除节点
    btn_dels.forEach(btn=>{
        btn.addEventListener('click', ()=>{
            aside.style.display = 'flex';
            show_aside('div.aside-del-menu');
            let pk = btn.dataset.pk.slice(2);
            span_del_pk.innerHTML = pk;
            jQuery.ajax({
                type: "GET",
                url: `/docs/json/pk2name/${pk}/`,
                data: null,
                dataType: "json",
                success: (x)=>{
                    aside_del_h1.innerHTML = `【${x.name}...】`;
                },
                error: ()=>{
                    alert("网络问题，无法删除。");
                }
            })
        });
    });

    // 修改节点
    btn_mods.forEach(btn=>{
        btn.addEventListener('click', ()=>{
            let pk = btn.dataset.pk.slice(2);
            aside.style.display = 'flex';
            show_aside('div.aside-mod-menu');
            input_mod_pk.value = pk;
            jQuery.ajax({
                type: "GET",
                url: `/docs/json/pk2all/${pk}/`,
                data: null,
                dataType: "json",
                success: (x)=>{
                    aside_mod_h1.innerHTML = `【${x.name}...】`;
                    input_mod_name.value = x.full_name;
                    textarea_mod_describe.value = x.description;
                    input_mod_order.value = x.order;
                    input_mod_isroot.checked = x.isroot;
                    input_mod_visible.checked = x.isvisible;
                },
                error: ()=>{
                    alert("网络问题，无法修改。");
                }
            })
        });
    });

    // 新增插件文章
    btn_plug_adds.forEach(btn=>{
        btn.addEventListener('click',()=>{
            aside.style.display = 'flex';
            show_aside('div.aside-add-plug');
            document.getElementById('menu_pk').value = btn.dataset.pk.slice(2);
        });
    });

    // 通用取消功能
    btn_cancels.forEach(btn=>{
        btn.addEventListener('click', ()=>{
            aside.style.display = 'none';
        });
    }); 

    // 新增
    btn_submit.addEventListener('click', ()=>{
        // 获取界面所有信息
        let name = document.querySelector('input[name="add-name"]').value;
        let description = document.querySelector('textarea[name="add-describe"]').value;
        let order = document.querySelector('input[name="add-order"]').value;
        let pk = input_add_pk.value;
        let isroot = input_add_isroot.checked ? 1 : 0; // 1为选中，0为未选中
        let isvisible = document.querySelector('input[name="add-isvisible"]').checked ? 1 : 0;

        jQuery.ajax({
            type: "GET",
            url: `/docs/json/menu/add/${name}/${description}/${order}/${pk}/${isroot}/${isvisible}/`,
            data: null,
            dataType: "json",
            success: (x)=>{
                if ('success' === x.msg) {
                    alert('新增节点成功');
                    aside.style.display = 'none';
                    window.location.reload();
                } else {
                    alert('新增节点失败，请联系管理员');
                }
            },
            error: ()=>{
                alert("请正确填写相关信息。");
            }
        })
    });
    // 删除
    btn_del_menu.addEventListener('click', ()=>{
        // 获取删除pk
        let pk = span_del_pk.innerHTML;
        jQuery.ajax({
            type: "GET",
            url: `/docs/json/menu/del/${pk}/`,
            data: null,
            dataType: "json",
            success: (x)=>{
                if ('success' === x.msg) {
                    alert('删除节点成功');
                    aside.style.display = 'none';
                    window.location.reload();
                } else {
                    alert('删除节点失败，请联系管理员');
                }
            },
            error: ()=>{
                alert("删除失败。");
            }
        })
    });
    // 修改
    btn_modify.addEventListener('click', ()=>{
        let name = input_mod_name.value;
        let description = textarea_mod_describe.value;
        let order = input_mod_order.value;
        let pk = input_mod_pk.value;
        let isroot = input_mod_isroot.checked ? 1 : 0;
        let isvisible = input_mod_visible.checked ? 1 : 0;
        jQuery.ajax({
            type: "GET",
            url: `/docs/json/menu/modify/${name}/${description}/${order}/${pk}/${isroot}/${isvisible}/`,
            data: null,
            dataType: "json",
            success: (x)=>{
                if ('success' === x.msg) {
                    alert('修改节点成功');
                    aside.style.display = 'none';
                    window.location.reload();
                } else {
                    alert('修改节点失败，请联系管理员');
                }
            },
            error: ()=>{
                alert("请正确填写相关信息。");
            }
        })
    });
})(); // 管理员操作
