/**
 * Save/remove bookmarks to/from the bookmark menu item and the cookie.
 *
 * @param string url        The current page url path (request.get_full_path)
 * @param string title      The current page title
 * @param string prompt_msg The message to ask for prompting
 * @return void
 */
var process_bookmarks = function(url, title, prompt_msg) {
    var json_str = $.cookie('menu.bookmarks');
    var bookmarks = json_str ? JSON.parse(json_str) : [];
    $('#bookmark-button').click(function() {
        if ($(this).hasClass('bookmarked')) {
            $(this).removeClass('bookmarked');
            $('#navigation-menu li.bookmark ul li a[href="' + url + '"]').parent().remove();
            if (!$('#navigation-menu li.bookmark ul li').length) {
                $('#navigation-menu li.bookmark ul').remove();
                $('#navigation-menu li.bookmark a span').remove();
                $('#navigation-menu li.bookmark').addClass('disabled');
            }
            for (var i=0; i < bookmarks.length; i++) {
                if (bookmarks[i].url == url) {
                    bookmarks.splice(i, 1);
                    $.cookie('menu.bookmarks', JSON.stringify(bookmarks), {
                        expires: 1825,
                        path: '/admin/' // harcode path to have a unique cookie across pages
                    });
                    break;
                }
            }
        } else {
            title = prompt(prompt_msg, title);
            if (!title) {
                return;
            }
            $(this).addClass('bookmarked');
            if (!$('#navigation-menu li.bookmark ul').length) {
                $('#navigation-menu li.bookmark a').prepend('<span class="icon"/>');
                $('#navigation-menu li.bookmark').append('<ul/>');
            }
            $('#navigation-menu li.bookmark ul').append(
                '<li><a href="' + url + '">' + title + '</a></li>'
            );
            $('#navigation-menu li.bookmark').removeClass('disabled');
            var already_bookmarked = false;
            for (var i=0; i < bookmarks.length; i++) {
                if (bookmarks[i].url == url) {
                    already_bookmarked = true;
                }
            }
            if (!already_bookmarked) {
                bookmarks.push({url: url, title: title});
                $.cookie('menu.bookmarks', JSON.stringify(bookmarks), {
                    expires: 1825,
                    path: '/admin/' // harcode path to have a unique cookie across pages
                });
            }
        }
    });
};
