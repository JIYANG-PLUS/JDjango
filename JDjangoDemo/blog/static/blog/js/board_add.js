(()=>{
    "use strict";
    // 新增
    const btn_add_board = document.querySelector('#add-board');
    const btn_cancels = document.querySelectorAll('.cancel');
    const section_add_board = document.querySelector('section.section-add-board');
    const section_modify_board = document.querySelector('section.section-modify-board');

    btn_add_board.addEventListener('click', ()=>{
        section_add_board.style.display = 'flex';
    });

    btn_cancels.forEach(btn_cancel=>{
        btn_cancel.addEventListener('click', ()=>{
            section_add_board.style.display = 'none';
            section_modify_board.style.display = 'none';
        });
    });

    // 修改
    const btn_modify_boards = document.querySelectorAll('button.modify-board');
    btn_modify_boards.forEach(btn_modify_board=>{
        btn_modify_board.addEventListener('click', ()=>{
            section_modify_board.style.display = 'flex';
            const pk = btn_modify_board.dataset.pk;
            document.querySelector('input[name="modify_board_pk"]').value = pk;
            jQuery.ajax({
                type: "GET",
                url: `json/${pk}/`,
                data: null,
                dataType: "json",
                timeout: 3000,
                success: (x)=>{
                    document.querySelector('input[name="modify_name"]').value = x.name;
                    document.querySelector('textarea[name="modify_description"]').value = x.description;
                },
                error: ()=>{
                    alert("网络问题，无法获取旧板块内容。");
                }
            })
        });
    });

})(); // 板块的新增和修改