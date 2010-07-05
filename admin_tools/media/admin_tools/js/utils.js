var loadScripts = function(js_files, onComplete){
    var len = js_files.length;
    var head = document.getElementsByTagName('head')[0];

    function loadScript(index){
        if (index >= len){
            onComplete();
            return;
        }

        try {
            testOk = js_files[index].test();
        } catch (e) {
            // with certain browsers like opera the above test can fail 
            // because of undefined variables...
            testOk = true;
        }

        if (testOk) {
            var s = document.createElement('script');
            s.src = js_files[index].src;
            s.type = 'text/javascript';
            head.appendChild(s);

            s.onload = function(){
                loadScript(index+1);
            }
        } else {
            loadScript(index+1);
        }
    }

    loadScript(0);
}
