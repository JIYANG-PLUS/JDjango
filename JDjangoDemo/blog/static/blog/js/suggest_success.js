(()=>{
    "use script";

    const second = document.getElementById('second');
    let TIME = 10;

    function invoke(f, start, interval, end) {
        if (!start) start = 0;
        if (arguments.length <= 2) {
            setTimeout(f, start);
        } else {
            setTimeout(repeat, start);
            function repeat() {
                var h = setInterval(f, interval);
                if (end) setTimeout(()=>{ 
                    clearInterval(h);
                    window.location.replace("/BBS/");
                }, end);
            }
        }
    }

    function f() {
        second.innerHTML = `${TIME}`;
        TIME -= 1;
    }

    window.onload = ()=> {
        // 倒计时开始
        invoke(f, 0, 1000, 11000);
    }
})();