(()=>{
    "use strict";
    // 全局搜索 和 登录
    const btn_search = document.getElementById('btn-search');
    const btn_user = document.getElementById('btn-login');
    const btn_cancel = document.getElementById('btn-cancel');
    const btn_logoutin_cancel = document.getElementById('logoutin_cancel');
    const h_right_classify = document.querySelector('div#h-right-classify');
    const h_right_split = document.querySelector('span#h-right-split');
    const h_right_search = document.querySelector('div#h-right-search');
    const logoutin = document.querySelector('div#logoutin');
    let bar_normal_status = ()=>{
        h_right_classify.style.display = 'block';
        h_right_split.style.display = 'inline-block';
        btn_search.style.display = 'block';
        btn_cancel.style.display = 'none';
        h_right_search.style.display = 'none';
    }
    btn_search.addEventListener('click', ()=>{
        h_right_classify.style.display = 'none';
        h_right_split.style.display = 'none';
        btn_search.style.display = 'none';
        logoutin.style.display = 'none';
        btn_cancel.style.display = 'block';
        h_right_search.style.display = 'block';
    });
    btn_cancel.addEventListener('click', ()=>{
        bar_normal_status();
    });
    if (btn_user) {
        btn_user.addEventListener('click', ()=>{
            logoutin.style.display = 'block';
            bar_normal_status();
        });
    }
    btn_logoutin_cancel.addEventListener('click', ()=>{
        logoutin.style.display = 'none';
    });
})();

((args)=>{
    "use strict";
    // bar按钮点击界面切换
    const div_nav = document.querySelector('div.nav');
    const div_func = document.querySelector('div.func');
    const main = document.querySelector('main');
    const footer = document.querySelector('footer');
    const aside = document.querySelector('aside');
    const header = document.querySelector('header');

    let swits = {}
    args.forEach((x)=>{ swits[x[3]] = 0; })
    let show_main = function(button, div, swit_name, triangle, i) {
        div_nav.style.display = 'flex';
        div_func.style.display = 'flex';
        main.style.display = 'flex';
        footer.style.display = 'block';
        aside.style.display = 'block';
        init_btns(button, div, swit_name, triangle, i);
    }
    let init_btns = function(button, div, swit_name, triangle, i) {
        header.style.borderBottom = '1px solid rgba(255, 255, 255, .3)';
        button.style.color = '#ffffff';
        div.style.display = 'none';
        triangle.style.display = 'none';
        swits[swit_name] = 0;
        i.setAttribute('class', 'fa fa-angle-down');
    }
    let unshow_main = function(button, div, swit_name, triangle, i) {
        div_nav.style.display = 'none';
        div_func.style.display = 'none';
        main.style.display = 'none';
        footer.style.display = 'none';
        aside.style.display = 'none';
        div.style.display = 'block';
        triangle.style.display = 'inline-block';
        swits[swit_name] = 1;
        header.style.borderBottom = '1px solid #f7c744';
        button.style.color = '#f7c744';
        i.setAttribute('class', 'fa fa-angle-up');
    }
    let clear_other_btns_status = function(button) {
        for (let i = args.length-1; i>=0; --i) {
            if (button !== args[i][0]) {
                init_btns(
                    document.getElementById(args[i][0]), 
                    document.getElementById(args[i][1]), 
                    args[i][3], 
                    document.getElementById(args[i][2]),
                    document.getElementById(args[i][4])
                ); // 按钮状态还原
            } else {
                unshow_main(
                    document.getElementById(args[i][0]), 
                    document.getElementById(args[i][1]), 
                    args[i][3], 
                    document.getElementById(args[i][2]),
                    document.getElementById(args[i][4])
                ); // 仅触发一次
            }
        }
    }
    args.forEach((x)=>{
        document.getElementById(x[0]).addEventListener('click',()=>{
            if (0 == swits[x[3]]) {
                clear_other_btns_status(x[0]);
            } else {
                show_main(
                    document.getElementById(x[0]), 
                    document.getElementById(x[1]), 
                    x[3], 
                    document.getElementById(x[2]),
                    document.getElementById(x[4])
                );
            }
        })
    })
})(
    [
        // 按钮、覆盖内容、三角提示箭头、控制器命名
        ['btn-plugin', 'div-plugin', 'classify-triangle-plugin', 'switch_plugin', 'i-plugin'],
        ['btn-about', 'div-about', 'classify-triangle-about', 'switch_about', 'i-about'],
    ]
);
