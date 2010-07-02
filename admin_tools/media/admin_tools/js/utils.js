var load_script = function(index, js_files) {
    if (typeof(js_files[index]) != 'undefined') {
        if (js_files[index].test()) {
            // add script element
            //console.log('Loading ' + js_files[index].src);
            var head = document.getElementsByTagName('head')[0];
            var s = document.createElement('script');
            s.src = js_files[index].src;
            s.type = 'text/javascript';
            head.appendChild(s);
            s.onload = load_script(index + 1, js_files);
        } else {
            //console.log('Skipped already loaded file ' + js_files[index].src);
            load_script(index + 1, js_files);
        }
    }
}
