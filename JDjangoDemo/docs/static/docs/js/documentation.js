(()=>{
    "use strict";
    // 全局开关
    let switch_light = 0;
    // 获取全局元素
    const btn_light = document.getElementById('btn-light'); // 灯光按钮
    const btn_light_info = document.querySelector('#btn-light>span'); // 灯光按钮配套提示信息
    const bg_main = document.querySelector('main'); // main标签
    const btn_menu = document.querySelector('#btn-menu-s'); // 收起+展开
    const btn_menu_z = document.querySelector('#btn-menu-z'); // 收起+展开
    const menu_all = document.querySelector('.main-left');
    const menu_some = document.querySelector('.main-left-small');
    // 灯光按钮点击事件
    btn_light.addEventListener('click', ()=>{
        const main_left = document.querySelector('main>div.main-left');
        const main_right = document.querySelector('main>div.main-right');
        const main_left_menu = document.querySelector('div.main-left-menu');
        const main_left_menu_span = document.querySelector('div.main-left-menu>span');
        const main_left_menu_button = document.querySelector('div.main-left-menu>button');
        const main_left_small_button = document.querySelector('div.main-left-small>div>button');
        const main_left_small_div = document.querySelector('div.main-left-small>div>div');
        const main_left_small_button_span = document.querySelectorAll('div.main-left-small>div>button>span');
        const main_left_small_div_span = document.querySelectorAll('div.main-left-small>div>div>span');
        const main_left_home_a = document.querySelector('a.main-left-home');
        const main_left_home_a_span = document.querySelector('a.main-left-home>span');
        const menu_items_a = document.querySelectorAll('.main-left>div.menu-items>div'); // 这里的a标签换成了div标签
        const menu_items_a_span = document.querySelectorAll('.main-left>div.menu-items>div>span'); // 这里的a标签换成了div标签
        const main_right_search_div1 = document.querySelector('div.main-right-search>div:nth-of-type(1)');
        const main_right_search_h2 = document.querySelector('div.main-right-search>h2');
        const main_right_subMenu_div = document.querySelectorAll('div.main-right-subMenu>div');
        const main_right_subMenu_a = document.querySelectorAll('div.main-right-subMenu>a');
        const content = document.querySelector('div.content');
        const content_item = document.querySelectorAll('div.content-item');
        const content_item_div1 = document.querySelectorAll('div.content-item>div:nth-of-type(1)');
        const content_item_detail_h4 = document.querySelectorAll('div.content-item-detial>h4>a');
        const content_item_detail_div1 = document.querySelectorAll('div.content-item-detial>.s1>span:nth-of-type(2)');
        const content_item_detail_div2 = document.querySelectorAll('div.content-item-detial>.s2');
        const pages = document.querySelector('div.pages');
        const btn_pages = document.querySelectorAll('div.pages>button');

        if (0 == switch_light) { // 暗夜模式
            bg_main.style.background = '#1f2023';
            btn_light_info.innerHTML = '切换到白昼模式';
            btn_light.setAttribute('title', '当前为暗夜模式');
            // main暗操作开始
            main_left.style.background = '#2d2f34';
            main_right.style.background = '#1f2023';
            main_left_home_a.style.background = '#383b40';
            main_left_home_a_span.style.color = '#ffffff';
            menu_items_a.forEach((x)=>{
                x.style.backgroundColor = '#383b40';
                x.style.borderTop = '1px solid rgba(255, 255, 255, .1)';
            });
            menu_items_a_span.forEach((x)=>{
                x.style.color = '#ffffff';
            });
            main_right_search_div1.style.color = '#ffffff';
            main_right_search_h2.style.color = '#ffffff';
            main_right_subMenu_div.forEach((x)=>{
                x.style.background = '#383b40';
                x.style.color = '#FFFFFF';
            });
            main_right_subMenu_a.forEach((x)=>{
                x.style.backgroundColor = '#2d2f34';
                x.style.color = '#FFFFFF';
            });
            content.style.background = '#383b40';
            content_item_div1.forEach((x)=>{
                x.style.background = '#000000';
            });
            content_item.forEach((x)=>{
                x.style.background = '#27292d';
            });
            content_item_detail_h4.forEach((x)=>{
                x.style.color = '#15abcd';
            });
            content_item_detail_div1.forEach((x)=>{
                x.style.color = '#FFFFFF';
            });
            content_item_detail_div2.forEach((x)=>{
                x.style.color = '#FFFFFF';
            });
            pages.style.color = '#FFFFFF';
            btn_pages.forEach((x)=>{
                x.style.color = '#FFFFFF';
            });
            main_left_menu.style.background = '#5abfd9';
            main_left_menu_span.style.color = '#353e47';
            main_left_menu_button.style.color = '#353e47';
            main_left_small_button.style.background = '#047ca1';
            main_left_small_div.style.background = '#2d2f34';
            main_left_small_button_span.forEach((x=>{
                x.style.color = '#eaebeb';
            }));
            main_left_small_div_span.forEach((x)=>{
                x.style.color = '#eaebeb';
            });
            // main暗操作结束
            switch_light = 1;
        } else { // 白昼模式
            bg_main.style.background = '#ffffff';
            btn_light_info.innerHTML = '切换到暗夜模式';
            btn_light.setAttribute('title', '当前为白昼模式');
            // main亮操作开始
            main_left.style.background = '#E5ECEB';
            main_right.style.background = '#ffffff';
            main_left_home_a.style.background = '#ffffff';
            main_left_home_a_span.style.color = '#333E48';
            menu_items_a.forEach((x)=>{
                x.style.backgroundColor = '#ffffff';
                x.style.borderTop = '1px solid rgba(0, 0, 0, .1)';
            });
            menu_items_a_span.forEach((x)=>{
                x.style.color = '#333E48';
            });
            main_right_search_div1.style.color = '#333E48';
            main_right_search_h2.style.color = '#333E48';
            main_right_subMenu_div.forEach((x)=>{
                x.style.background = '#E5ECEB';
                x.style.color = 'black';
            });
            main_right_subMenu_a.forEach((x)=>{
                x.style.backgroundColor = 'inherit';
                x.style.color = '#000000';
            });
            content.style.background = '#E5ECEB';
            content_item_div1.forEach((x)=>{
                x.style.background = '#333E48';
            });
            content_item.forEach((x)=>{
                x.style.background = '#f7f7f7';
            });
            content_item_detail_h4.forEach((x)=>{
                x.style.color = '#333E48';
            });
            content_item_detail_div1.forEach((x)=>{
                x.style.color = '#333E48';
            });
            content_item_detail_div2.forEach((x)=>{
                x.style.color = '#333E48';
            });
            pages.style.color = 'inherit';
            btn_pages.forEach((x)=>{
                x.style.color = 'inherit';
            });
            main_left_menu.style.background = '#347b9d';
            main_left_menu_span.style.color = '#e4f1f5';
            main_left_menu_button.style.color = '#e4f1f5';
            main_left_small_button.style.background = '#347b9d';
            main_left_small_div.style.background = '#e6eceb';
            main_left_small_button_span.forEach((x=>{
                x.style.color = '#ffffff';
            }));
            main_left_small_div_span.forEach((x)=>{
                x.style.color = '#353e47';
            });
            // main亮操作结束
            switch_light = 0;
        }
    });
    // 收起按钮事件
    btn_menu.addEventListener('click', ()=>{
        menu_all.style.display = 'none';
        menu_some.style.display = 'block';
    });
    // 展开按钮事件
    btn_menu_z.addEventListener('click', ()=>{
        menu_all.style.display = 'block';
        menu_some.style.display = 'none';
    });
})(); // 开关

(()=>{
    "use strict";
    function Queue() {
        let items = [];
        this.push = function(ele){
            items.push(ele);
        }
        this.pop = function(){
            return items.shift();
        }
        this.isEmpty = function(){
            return items.length == 0;
        }
        this.all = function() {
            return items;
        }
    } // 队列，用于顺序处理子菜单
    let lis = document.querySelectorAll('div.menu-items>div>a'); // 获取所有的菜单项
    function filterli(datas, open) {
        return [...lis].filter(function(x){
            return x.dataset.fath===datas.self // 以本节点为父节点的所有子节点
            && x.dataset.fath !== x.dataset.self // 不是根节点（排除自身）
            && x.dataset.open===open; // 标签状态
        })
    }
    lis.forEach(li => {
        li.addEventListener('click', ()=>{
            let sub_lis = null; // 存储当下的所有节点
            let flag_open = null; // 是否展开，0表示展开，1表示收起【0可见，1不可见】
            if ('0' === li.dataset.flag) { // 本标签已展开
                sub_lis = filterli(li.dataset, '0'); // 找到所有可见的子标签
                flag_open = '0'; // 继续往下搜索
            } else { // 本标签收起
                sub_lis = filterli(li.dataset, '1'); // 找到所有不可见的子标签
                flag_open = '1'; // 停止往下搜索
            }
            let all = []
            if ('0' === flag_open) { // 如果本标签可见
                let queue = new Queue();
                sub_lis.forEach(x => {
                    queue.push(x);
                });
                while (!queue.isEmpty()) {
                    let popItem = queue.pop();
                    all.push(popItem);
                    filterli(popItem.dataset, flag_open).forEach(x => {
                        queue.push(x); // 继续寻找所有可见的孩子标签
                    });
                }
            } else { // 本标签不可见
                all = sub_lis; 
            }
            // 上面是筛选，下面是状态的改变
            if ('0' === li.dataset.flag) { // 本标签是展开状态
                all.forEach(sub_li => {
                    // 配对获取
                    const contact_lis = document.querySelectorAll(`a[data-self="${sub_li.dataset.self}"]`);
                    contact_lis.forEach(x=>{
                        x.setAttribute('data-open', '1'); // 隐藏孩子节点
                        x.setAttribute('data-flag', '1'); // 状态统一变成收起
                        // 对应的父节点也改变
                        x.parentNode.setAttribute('data-open', '1');
                        x.parentNode.setAttribute('data-flag', '1');
                        // 图标改变
                        x.children[0].classList.remove('fa-chevron-right');
                        x.children[0].classList.add('fa-chevron-down');
                    });
                })
                const contact_liss = document.querySelectorAll(`a[data-self="${li.dataset.self}"]`);
                contact_liss.forEach(x=>{
                    x.setAttribute('data-flag', '1'); // 当前标签状态变成收起
                    x.children[0].classList.remove('fa-chevron-down');
                    x.children[0].classList.add('fa-chevron-right');
                });
            } else { // 本标签是收起状态
                all.forEach(sub_li => {
                    const contact_lis = document.querySelectorAll(`a[data-self="${sub_li.dataset.self}"]`);
                    contact_lis.forEach(x=>{
                        x.setAttribute('data-open', '0');
                        // 对应的父节点也改变
                        x.parentNode.setAttribute('data-open', '0');
                        // 图标改变
                        x.children[0].classList.remove('fa-chevron-down');
                        x.children[0].classList.add('fa-chevron-right');
                    });
                })
                const contact_liss = document.querySelectorAll(`a[data-self="${li.dataset.self}"]`);
                contact_liss.forEach(x=>{
                    x.setAttribute('data-flag', '0'); // 当前标签状态变成展开
                    x.children[0].classList.remove('fa-chevron-right');
                    x.children[0].classList.add('fa-chevron-down');
                });
            }
        });
    });
})(); // 动态导航栏

(()=>{
    "use strict";

    const span_items = document.querySelectorAll('div.menu-items>div>span');
    const js_content = document.querySelector('div.js-content');

    // 页码相关
    const div_pages = document.querySelector('div.pages');
    const main_right_search_h2 = document.querySelector('div.main-right-search>h2');
    const main_right_search_div_form_input = document.querySelector('input[name="main-right-search"]');
    const btn_light = document.getElementById('btn-light');

    function insert_dom(article) {
        let frag = document.createDocumentFragment();
        let content_item = document.createElement('div');
        content_item.classList.add('content-item');
        frag.appendChild(content_item);
        let div = document.createElement('div');
        div.innerHTML = '<i class="fa fa-unlock-alt" aria-hidden="true"></i>'; // 文章等级
        let div_item_detial = document.createElement('div');
        div_item_detial.classList.add('content-item-detial');
        content_item.appendChild(div);
        content_item.appendChild(div_item_detial);
        // 细节
        let h4 = document.createElement('h4');
        let h4_a = document.createElement('a');
        h4_a.innerHTML = article.title; // 文章标题
        h4_a.setAttribute('href', `content/${article.pk}/${article.id}/`); // 文章pk和ID
        // h4_a.setAttribute('target', '_blank'); // 新窗口打开
        h4.appendChild(h4_a);
        let iii = document.createElement('i');
        iii.style.marginLeft = '12px';
        iii.setAttribute('class', 'fa fa-hand-o-left');
        iii.setAttribute('aria-hidden', 'true');
        h4.appendChild(iii);
        div_item_detial.appendChild(h4);
        // 三个div添加
        let div_s1 = document.createElement('div');
        div_s1.classList.add('s1');
        let div_s2 = document.createElement('div');
        div_s2.classList.add('s2');
        let div_s3 = document.createElement('div');
        div_s3.classList.add('s3');
        div_s1.innerHTML = `<span>Version: 1.0</span> - <span>${article.modify_time}</span>`; // 时间和版本
        div_s2.innerHTML = `${article.abstract}`; // 摘要
        let str_a = '';
        article.label.split("/").forEach(l=>{
            str_a += `<a>${l}</a> `;
        });
        div_s3.innerHTML = `<i class="fa fa-tags" aria-hidden="true" style="color: rgb(199,83,0);margin-right:6px;"></i>${str_a}`; // 标签
        div_item_detial.appendChild(div_s1);
        div_item_detial.appendChild(div_s2);
        div_item_detial.appendChild(div_s3);
        // 新增容器，适应背景颜色
        // 获取当前背景主题
        const color = btn_light.getAttribute('title');
        if ('当前为暗夜模式' === color) {
            // 色调改为暗色
            content_item.style.background = '#27292d';
            div.style.background = '#000000';
            h4_a.style.color = '#15abcd';
            div_s1.style.color = '#ffffff';
            div_s1.children[1].style.color = '#ffffff';
            div_s2.style.color = '#ffffff';
        }
        js_content.appendChild(frag);
    }

    span_items.forEach(span=>{
        span.addEventListener('click', ()=>{
            js_content.innerHTML = ""; // 构建之前，删除所有的子节点
            div_pages.innerHTML = ""; // 页码消除，细节不划分页面
            let pk = span.dataset.pk.slice(2);
            jQuery.ajax({
                type: "GET",
                url: `/docs/json/articles/${pk}/`,
                data: null,
                dataType: "json",
                timeout: 3000,
                success: (x)=>{
                    // 构建节点
                    x.articles.forEach(article=>{
                        insert_dom(article);
                    });
                    // 将标题和提示信息进行修改
                    main_right_search_h2.innerHTML = x.menu_name;
                    main_right_search_div_form_input.setAttribute('placeholder', x.menu_name);
                },
                error: ()=>{
                    alert("网络问题，无法获取详情页。");
                }
            })
        });
    });
})(); // 文章获取

(()=>{
    "use strict";
    const div_mini_menu = document.getElementById('div-mini-menu');
    const btn_mini_menu = document.querySelector('i[class~="fa-list"]');
    const btn_mini_menu_cancel = document.querySelector('i[class~="fa-times"]');

    btn_mini_menu.addEventListener('click', ()=>{
        div_mini_menu.style.display = 'block';
        btn_mini_menu.style.display = 'none';
        btn_mini_menu_cancel.style.display = 'inline';
    });

    btn_mini_menu_cancel.addEventListener('click', ()=>{
        div_mini_menu.style.display = 'none';
        btn_mini_menu.style.display = 'inline';
        btn_mini_menu_cancel.style.display = 'none';
    });
})(); // 迷你菜单