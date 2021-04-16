(()=>{
    "use strict";

    const btn_merg = document.getElementById('btn-merg');
    const btn_important = document.getElementById('btn-important');
    const btn_normal = document.getElementById('btn-normal');
    const btn_allnotice = document.getElementById('btn-allnotice');
    const btn_halfyear = document.getElementById('btn-halfyear');
    const btn_month = document.getElementById('btn-month');
    const btn_halfmonth = document.getElementById('btn-halfmonth');
    const btn_week = document.getElementById('btn-week');
    const btn_allarticle = document.getElementById('btn-allarticle');

    const div_notices_items = document.getElementById('notices-items');
    const div_recent_items = document.getElementById('recent-items');

    const NOTICES = [
        btn_merg,btn_important,btn_normal,btn_allnotice
    ]

    const ARTICLES = [
        btn_halfyear,btn_month,btn_halfmonth,btn_week,btn_allarticle
    ]

    // 通知光标移动
    function moveNotice(obj) {
        NOTICES.forEach(n=>{
            if (obj === n) {
                // 变成橘红色
                n.style.color = '#f79568';
                n.style.fontWeight = '800';
            } else {
                // 变成蓝色
                n.style.color = '#40a3d1';
                n.style.fontWeight = '400'; 
            }
        });
    }
    // 最近更新光标移动
    function moveArticle(obj) {
        ARTICLES.forEach(a=>{
            if (obj === a) {
                // 变成橘红色
                a.style.color = '#f79568';
                a.style.fontWeight = '800';
            } else {
                // 变成蓝色
                a.style.color = '#40a3d1';
                a.style.fontWeight = '400';    
            }
        });
    }

    function insertNoticeItem(notice) {
        let frag = document.createDocumentFragment();
        let div = document.createElement('div');
        frag.appendChild(div);
        let div_div = document.createElement('div');
        let div_span = document.createElement('span');
        div_span.innerHTML = notice.create_time;
        div.appendChild(div_div);
        div.appendChild(div_span);
        let div_div_span = document.createElement('span');
        if ('A' === notice.level) {
            div_div_span.setAttribute('class', 'info-mormal');
            div_div_span.innerHTML = '一般';
        } else if ('B' === notice.level) {
            div_div_span.setAttribute('class', 'info-important');
            div_div_span.innerHTML = '重要';
        } else {
            div_div_span.setAttribute('class', 'info-urgent');
            div_div_span.innerHTML = '紧急';
        }
        let div_div_a = document.createElement('a');
        div_div_a.setAttribute('class', 'notice-detial');
        div_div_a.setAttribute('data-pk', notice.pk);
        div_div_a.addEventListener('click', ()=>{
            const div_notice_show = document.querySelector('div.notice-show');
            div_notice_show.style.display = 'flex';
            jQuery.ajax({
                type: "GET",
                url: `/BBS/json/notice/detial/${notice.pk}/`,
                data: null,
                dataType: "json",
                timeout: 3000,
                success: (x)=>{
                    let article = div_notice_show.children[0];
                    let level = '';
                    if ('A' === x.level) {
                        level += '一般';
                    } else if ('B' === x.level) {
                        level += '重要';
                    } else {
                        level += '紧急';
                    }
                    article.children[0].innerHTML = `公告详情【${level}】`;
                    article.children[1].innerHTML = x.content;
                    article.children[2].innerHTML = x.create_time;
                },
                error: ()=>{
                    
                }
            })
        });
        div_div_a.innerHTML = notice.title;
        div_div.appendChild(div_div_span);
        div_div.appendChild(div_div_a);
        div_notices_items.appendChild(frag);
    }

    function insertArticleItem(article) {
        let frag = document.createDocumentFragment();
        let div = document.createElement('article');
        frag.appendChild(div);
        let div_a = document.createElement('a');
        div_a.innerHTML = article.title;
        div_a.setAttribute('href', `articledetial/${article.pk}/`);
        let div_span = document.createElement('span');
        div_span.innerHTML = article.modify_time;
        div.appendChild(div_a);
        div.appendChild(div_span);
        div_recent_items.appendChild(frag);
    }

    function commonNotice(mode) {
        jQuery.ajax({
            type: "GET",
            url: `/BBS/json/notice/${mode}/`,
            data: null,
            dataType: "json",
            timeout: 3000,
            success: (x)=>{
                div_notices_items.innerHTML = '';
                [...x.notices].forEach(notice=>{
                    insertNoticeItem(notice);
                });
            },
            error: ()=>{
                
            }
        })
    }

    function commonArticle(mode) {
        jQuery.ajax({
            type: "GET",
            url: `/BBS/json/recent/${mode}/`,
            data: null,
            dataType: "json",
            timeout: 3000,
            success: (x)=>{
                div_recent_items.innerHTML = '';
                [...x.articles].forEach(article=>{
                    insertArticleItem(article);
                });
            },
            error: ()=>{
                
            }
        })
    }

    btn_merg.addEventListener('click', ()=>{
        commonNotice('C');
        moveNotice(btn_merg);
    });
    btn_important.addEventListener('click', ()=>{
        commonNotice('B');
        moveNotice(btn_important);
    });
    btn_normal.addEventListener('click', ()=>{
        commonNotice('A');
        moveNotice(btn_normal);
    });
    btn_allnotice.addEventListener('click', ()=>{
        commonNotice('D');
        moveNotice(btn_allnotice);
    });
    btn_halfyear.addEventListener('click', ()=>{
        commonArticle('A');
        moveArticle(btn_halfyear);
    });
    btn_month.addEventListener('click', ()=>{
        commonArticle('B');
        moveArticle(btn_month);
    });
    btn_halfmonth.addEventListener('click', ()=>{
        commonArticle('C');
        moveArticle(btn_halfmonth);
    });
    btn_week.addEventListener('click', ()=>{
        commonArticle('D');
        moveArticle(btn_week);
    });
    btn_allarticle.addEventListener('click', ()=>{
        commonArticle('E');
        moveArticle(btn_allarticle);
    });
})(); // 标签切换

(()=>{
    "use strict";

    const a_btn_notices = document.querySelectorAll('a.notice-detial');
    const div_notice_show = document.querySelector('div.notice-show');

    a_btn_notices.forEach(a=>{
        a.addEventListener('click', ()=>{
            div_notice_show.style.display = 'flex';
            jQuery.ajax({
                type: "GET",
                url: `/BBS/json/notice/detial/${a.dataset.pk}/`,
                data: null,
                dataType: "json",
                timeout: 3000,
                success: (x)=>{
                    let article = div_notice_show.children[0];
                    let level = '';
                    if ('A' === x.level) {
                        level += '一般';
                    } else if ('B' === x.level) {
                        level += '重要';
                    } else {
                        level += '紧急';
                    }
                    article.children[0].innerHTML = `公告详情【${level}】`;
                    article.children[1].innerHTML = x.content;
                    article.children[2].innerHTML = x.create_time;
                },
                error: ()=>{
                    
                }
            })
        });
    });

    div_notice_show.addEventListener('click', ()=>{
        div_notice_show.style.display = 'none';
    });
})(); // 通知详细