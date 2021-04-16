((args)=>{
    "use strict";

    let swits = {}
    args.forEach((x)=>{ swits[x[2]] = 0; })

    let init_btns = function(button, div, swit_name) {
        button.style.color = '#ffffff';
        button.style.background = 'inherit';
        div.style.display = 'none';
        swits[swit_name] = 0;
    }

    let active_btns = function(button, div, swit_name) {
        button.style.color = 'black';
        button.style.background = 'rgb(239, 243, 2)';
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
            if (0 == swits[x[2]]) {
                clear_other_btns_status(x[0]);
            } else {
                init_btns(
                    document.getElementById(x[0]), 
                    document.getElementById(x[1]), 
                    x[2]
                );
            }
        })
    })
})(
    [
        ['btn-suggesstion','bar-suggestion','swit_suggestion'],
        ['btn-change','bar-change','swit_change'],
        ['btn-about','bar-about','swit_about'],
        ['btn-plan','bar-plan','swit_plan'],
    ]
); // bar切换

(()=>{
    "use strict";

    const btn_stars = document.querySelectorAll('#btn-star');
    btn_stars.forEach(btn_star=>{
        btn_star.addEventListener('click', ()=>{
            const pk = btn_star.dataset.spk
            jQuery.ajax({
                type: "GET",
                url: `/BBS/json/svotes/${pk}/`,
                data: null,
                dataType: "json",
                timeout: 3000,
                success: (x)=>{
                    if ("success" === x.msg) {
                        btn_star.children[0].setAttribute('class', 'fa fa-star');
                        btn_star.children[0].innerHTML = x.votes;
                        alert('投票成功，感谢您的参与。');
                    } else {
                        alert('您已投票，请勿重复投票。');
                    }
                },
                error: ()=>{
                    
                }
            })
        });
    });
})(); // 投票功能实现
