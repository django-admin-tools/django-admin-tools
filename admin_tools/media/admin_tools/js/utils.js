var loadScripts = function(js_files, onComplete){
    var len = js_files.length;
    var head = document.getElementsByTagName('head')[0];

    function loadScript(index){

        if (index >= len){
            onComplete();
            return;
        }

        if (js_files[index].test()){
//            console.log('Loading ' + js_files[index].src);

            var s = document.createElement('script');
            s.src = js_files[index].src;
            s.type = 'text/javascript';
            head.appendChild(s);

            s.onload = function(){
                loadScript(index+1);
            }
        }
        else{
            loadScript(index+1);
        }
    }

    loadScript(0);
}
