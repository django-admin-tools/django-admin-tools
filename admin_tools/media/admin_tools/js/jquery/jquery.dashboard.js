/* vim: set expandtab tabstop=4 shiftwidth=4 softtabstop=4: */

/**
 * Dashboard plugin.
 * This plugin is not yet released, but should be when it will be finished.
 *
 * copyright (c) 2010 David Jean Louis <izimobil@gmail.com>
 * 
 * Permission is hereby granted, free of charge, to any person obtaining a
 * copy of this software and associated documentation files (the "Software"),
 * to deal in the Software without restriction, including without limitation
 * the rights to use, copy, modify, merge, publish, distribute, sublicense,
 * and/or sell copies of the Software, and to permit persons to whom the
 * Software is furnished to do so, subject to the following conditions:
 * 
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 * 
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
 * FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER 
 * DEALINGS IN THE SOFTWARE.
 */

(function($) {

    $.fn.extend({
        //pass the options variable to the function
        dashboard: function(options) {
            //Set the default values, use comma to separate the settings, example:
            var defaults = {
                panel_id: 'dashboard-panel',
                dashboard_module_class: 'dashboard-module',
                columns: 2
            }    
            var options = $.extend(defaults, options);

            return this.each(function() {
                // set ids for dashboard modules
                _set_ids($(this), options);
                // columnize the dashboard modules
                _columnize($(this), options);
                // add draggable behaviour
                _set_draggable($(this), options);
                // add collapsible behaviour
                _set_collapsible($(this), options);
                // add deletable behaviour
                _set_deletable($(this), options);
                // add addable behaviour to dashboard panel items
                _set_addable($(this), options);
                // restore user preferences
                _restore_preferences($(this), options);
            });
        }
    });

    var json_str = $.cookie('admin-tools.dashboard');
    var preferences = json_str ? JSON.parse(json_str) : {};

    var _set_ids = function(elt, options) {
        elt.children('div[id!=' + options.panel_id +']').each(function(index) {
            if (!$(this).attr('id')) {
                $(this).attr('id', 'module_' + index);
            }
        });
    };

    var _columnize = function(elt, options) {
        var elts = elt.children('div[id!=' + options.panel_id +']');
        var size = Math.ceil(elts.length / options.columns);
        var percent = Math.floor(100 / options.columns);
        for (i = 0; i < options.columns; i++) {
            start = i * size;
            elts.slice(start, start+size).wrapAll(
                '<div class="dashboard-column" style="float:left;width:'+percent+'%;"/>'
            );
        }
    };

    var _restore_preferences = function(elt, options) {
        elt.children().children('.disabled').each(function() {
            _delete_element($(this), options);
        });
        if (preferences['disabled']) {
            $.each(preferences['disabled'], function(k, v) {
                v ? _delete_element($('#'+k), options) : _add_element($('#'+k), options);
            });
        }
        if (preferences['collapsed']) {
            $.each(preferences['collapsed'], function(k, v) {
                if (v) {
                    _toggle_element($('#'+k), options);
                }
            });
        }
    };

    var _set_draggable = function(elt, options) {
        // the dashboard column
        elt.children('.dashboard-column').sortable({
            handle: 'h2',
            items: '.draggable',
            connectWith: '.dashboard-column',
            placeholder: 'dashboard-placeholder',
            forcePlaceholderSize: true,
            cursor: 'crosshair',
            opacity: 0.7
        });
    };

    var _set_collapsible = function(elt, options) {
        elt.find('.collapsible h2').each(function() {
            $(this).append('<a href="#" class="toggle-icon">Toggle</a>').find('a.toggle-icon').click(function() {
                var prnt = $(this).parent().parent();
                _toggle_element(prnt, options, true);
            });
        });
    };

    var _toggle_element = function(elt, options, save_preference) {
        elt.find('h2 a.toggle-icon').toggleClass('collapsed');
        elt.children('div').slideToggle();
        if (save_preference) {
            _set_preference('collapsed', elt.attr('id'), elt.find('h2 a.toggle-icon').hasClass('collapsed'));
        }
    };

    var _set_deletable = function(elt, options) {
        elt.find('.deletable h2').each(function() {
            $(this).append('<a href="#" class="close-icon">Close</a>').find('a.close-icon').click(function() {
                var prnt = $(this).parent().parent();
                _delete_element(prnt, options, true);
            });
        });
    };

    var _delete_element = function(elt, options, save_preference) {
        var existing = $('#'+options.panel_id).find('li a[rel='+elt.attr('id')+']');
        if (!existing.length) {
            $('#' + options.panel_id).find('ul').append(
                '<li><a href="#" rel="' 
                + elt.attr('id') 
                + '" class="addlink dashboard-module-add">'
                + elt.find('h2').contents().first().text() 
                + '</a></li>'
            );
            _set_addable(elt, options, $('#'+options.panel_id).find('li a[rel='+elt.attr('id')+']'));
        } else {
            existing.parent().show();
        }
        elt.fadeOut('fast');
        if (save_preference) {
            _set_preference('disabled', elt.attr('id'), true);
        }
    };

    var _set_addable = function(elt, options, elts) {
        if (!elts) {
            elts = $('#'+options.panel_id).find('li a');
        }
        elts.click(function() {
            _add_element($('#'+$(this).attr('rel')), options, true);
        });
    };

    var _add_element = function(elt, options, save_preference) {
        panel_elt = $('#'+options.panel_id).find('li a[rel='+elt.attr('id')+']');
        panel_elt.parent().hide();
        elt.removeClass('disabled');
        elt.fadeIn('fast');
        if (save_preference) {
            _set_preference('disabled', elt.attr('id'), false);
        }
    };

    var _get_preference = function(cat, id, defaultval) {
        try {
            if (preferences[cat] == undefined) {
                preferences[cat] = {};
            }
            return preferences[cat][id];
        } catch (e) {
            return defaultval ? defaultval : null;
        }
    };

    var _set_preference = function(cat, id, val) {
        try {
            if (preferences[cat] == undefined) {
                preferences[cat] = {};
            }
            preferences[cat][id] = val;
        } catch (e) {
        }
        $.cookie('admin-tools.dashboard', JSON.stringify(preferences), {expires: 1825});
    };

})(jQuery);
