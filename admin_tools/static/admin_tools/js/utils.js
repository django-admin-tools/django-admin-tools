function isCsrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
function useCsrfTokens(){
    // set CSRFToken header on POST requests (and remove the need for @csrf_exempt)
    jQuery.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            }
        }
    });
}
var loadScripts = function(js_files, onComplete){
    var len = js_files.length;
    var head = document.getElementsByTagName('head')[0];

    function loadScript(index){
        var testOk;

        if (index >= len){
            useCsrfTokens();
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
            if (/MSIE/.test(navigator.userAgent)) {
                // Internet Explorer
                s.onreadystatechange = function () {
                    if (s.readyState == 'loaded' || s.readyState == 'complete') {
                        loadScript(index+1);
                    }
                };
            } else {
                s.onload = function() { loadScript(index+1); };
            }
        } else {
            loadScript(index+1);
        }
    }

    loadScript(0);
}
