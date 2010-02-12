/**
 * Save/remove bookmarks to/from the bookmark menu item and the cookie.
 *
 * @param string url        The current page url path (request.get_full_path)
 * @param string title      The current page title
 * @param string prompt_msg The message to ask for prompting
 * @return void
 */
var process_bookmarks = function(url, title, prompt_msg) {
    var json_str = jQuery.cookie('menu.bookmarks');
    var bookmarks = json_str ? JSON.parse(json_str) : [];
    jQuery('#bookmark-button').click(function() {
        if (jQuery(this).hasClass('bookmarked')) {
            jQuery(this).removeClass('bookmarked');
            jQuery('#navigation-menu li.bookmark ul li a[href="' + url + '"]').parent().remove();
            if (!jQuery('#navigation-menu li.bookmark ul li').length) {
                jQuery('#navigation-menu li.bookmark ul').remove();
                jQuery('#navigation-menu li.bookmark a span').remove();
                jQuery('#navigation-menu li.bookmark').addClass('disabled');
            }
            for (var i=0; i < bookmarks.length; i++) {
                if (bookmarks[i].url == url) {
                    bookmarks.splice(i, 1);
                    jQuery.cookie('menu.bookmarks', JSON.stringify(bookmarks), {
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
            jQuery(this).addClass('bookmarked');
            if (!jQuery('#navigation-menu li.bookmark ul').length) {
                jQuery('#navigation-menu li.bookmark a').prepend('<span class="icon"/>');
                jQuery('#navigation-menu li.bookmark').append('<ul/>');
            }
            jQuery('#navigation-menu li.bookmark ul').append(
                '<li><a href="' + url + '">' + title + '</a></li>'
            );
            jQuery('#navigation-menu li.bookmark').removeClass('disabled');
            var already_bookmarked = false;
            for (var i=0; i < bookmarks.length; i++) {
                if (bookmarks[i].url == url) {
                    already_bookmarked = true;
                }
            }
            if (!already_bookmarked) {
                bookmarks.push({url: url, title: title});
                jQuery.cookie('menu.bookmarks', JSON.stringify(bookmarks), {
                    expires: 1825,
                    path: '/admin/' // harcode path to have a unique cookie across pages
                });
            }
        }
    });
};
