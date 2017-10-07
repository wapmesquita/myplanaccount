(function($) {

	//$.wf.autoloads([ 'templates/base.html' ]);

    $(window).bind('hashchange', function() {
        var hash = $.trim(this.location.hash || '#');
        if (!hash || hash == '#') {
            this.location = '#projection';
            return;
        }
        hash = hash.substring(1).split('?')[0];
        $.wf([ 'static/page/' + hash + '.html' ], function(face) {
            face.open();
        });
    })

    $(window).trigger('hashchange');

    $.projutils = {};
    $.projutils.formatMoney = function() {
        $.each($('.money'), function(idc, item) {$(item).html(accounting.formatMoney($(item).html(), "", 2, ",", "."));})
      };

})(jQuery)
