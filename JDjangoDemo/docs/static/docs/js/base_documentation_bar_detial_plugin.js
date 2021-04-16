((args)=>{
    "use strict";
    args.forEach((bd)=>{
        document.getElementById(bd[0]).addEventListener('click',()=>{
            let innerFunc = (x, flag)=>{
                let btn_div1 = document.getElementById(x[0]).children[0];
                let btn_div2 = document.getElementById(x[0]).children[1];
                let div = document.getElementById(x[1]);
                if ('Z' === flag) {
                    btn_div1.style.background = '#7D868C';
                    btn_div2.style.background = '#3E4A56';
                    div.style.display = 'none';
                } else {
                    btn_div1.style.background = '#54bfda';
                    btn_div2.style.background = '#363e46';
                    div.style.display = 'block';
                }
            };
            for (let i = args.length-1; i>=0; --i) {
                if (bd[0] !== args[i][0]) {
                    innerFunc(args[i], 'Z');
                } else {
                    innerFunc(args[i], 'F');
                }
            }
        });
    });
})(
    [
        ['btn-1', 'div-b-right-content1'], // 必须全部传入id，且配对传入
    ]
);
