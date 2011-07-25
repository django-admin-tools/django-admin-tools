var init_dashboard = function(id, columns, preferences, url) {
    jQuery('#'+id).dashboard({
        'columns': columns,
        'load_preferences_function': function(options) {
            return preferences;
        },
        'save_preferences_function': function(options, preferences) {
            jQuery.post(url, { data: JSON.stringify(preferences) });
        }
    });
    jQuery(".group-tabs").tabs();
    jQuery(".group-accordion").accordion({header: '.group-accordion-header'});
};
