(()=>{
    "use strict";

    const btn_vote = document.getElementById('btn-vote');
    const btn_remark = document.getElementById('btn-remark');
    const span_num_votes = document.getElementById('num_votes');

    // 点赞功能
    btn_vote.addEventListener('click', ()=>{
        if ("0" === btn_vote.dataset.flag) {
            btn_vote.setAttribute('data-flag', '1');
            btn_vote.children[0].setAttribute('class', 'fa fa-thumbs-up');
            btn_vote.children[0].style.color = 'rgb(31, 243, 31)';
            let pk = document.querySelector('input[name="pk"]').value;
            jQuery.ajax({
                type: "GET",
                url: `/BBS/json/votes/${pk}/`,
                data: null,
                dataType: "json",
                timeout: 3000,
                success: (x)=>{
                    span_num_votes.innerHTML = x.nums;
                },
                error: ()=>{
                    
                }
            })
        }
    });
})();