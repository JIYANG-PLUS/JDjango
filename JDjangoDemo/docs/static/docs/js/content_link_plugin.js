(()=>{
    "use strict";

    const btn_insert_cancel = document.getElementById('btn-insert-cancel');
    const btn_insert_plugin = document.getElementById('btn-insert-plugin');
    const div_insert_plugin = document.querySelector('div.div-insert-plugin');
    if (btn_insert_cancel) {
        btn_insert_cancel.addEventListener('click', ()=>{
            div_insert_plugin.style.display = 'none';
        });
    }
    if (btn_insert_plugin) {
        btn_insert_plugin.addEventListener('click', ()=>{
            div_insert_plugin.style.display = 'flex';
            const url = document.getElementById('copy-content').innerHTML;
            document.querySelector('input[name="link_use_linke"]').value = url;
        });
    }
    
})();