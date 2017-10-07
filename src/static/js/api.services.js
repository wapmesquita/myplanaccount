(function($){
    $.projcore = $.projcore || {};
    $.projcore.services = $.projcore.services || {};


    function multiple(reqs, callback) {
		$.when.apply($, reqs).done(function() {
			var resps = [];
            if(reqs.length == 1) {
                resps.push(arguments[0]);
            } else {
                for (var i = 0; i < arguments.length; i++) {
                    resps.push(arguments[i][0]);
                }
            }
			if (callback) {
				callback.apply(window, resps);
			}
		});
	}

	$.projcore.mult = function() {
		var reqs = $.makeArray(arguments);
		var callback = null;
		if (reqs && reqs.length && typeof (reqs[reqs.length - 1]) == 'function') {
			callback = reqs.pop();
		}
		multiple(reqs, callback);
	}

    var mount = function(base, type, url, name, push_load){
        $.projcore.services[base] = $.projcore.services[base] || {};
        $.projcore.services[base][name] = ajax(type, url, push_load);
    }

    var mountUpload = function(base,type, url, name){
        $.projcore.services[base] = $.projcore.services[base] || {};
        $.projcore.services[base][name] = ajaxFile(type, url);
    }

    function convertToFormData(obj){
      var formData = new FormData();
      for (var i in obj){
        if (typeof(obj[i]) == 'object'){
          formData.append(i, obj[i].blob, obj[i].filename);
        } else{
          formData.append(i, obj[i]);
        }
      }
      return formData;
    }

    function ajaxFile(type, url){
        return function(obj, success, error){
            var opt = {
                type: type,
                url: url,
            };
            opt.contentType= false;
            opt.cache= false;
            opt.processData = false;
            opt.data= convertToFormData(obj);
            return $.ajax(opt);
        }
    }

    var ajax = function(type, url, push_loading){
        return function(data, success, error){
            var opt = {
                type: type,
                url: url
            };


            if (typeof(data) == 'function'){
                error = success;
                success = data;
            }

            opt.success = mountSuccess(success);

            if(type == 'POST' || type == 'PUT'){
                opt.contentType = "application/json;charset=UTF-8";
                opt.dataType = "json";
                opt.data = JSON.stringify(data);
            } else {
                if(data){
                  opt.url += '?' + $.param(data);
                }
                opt.contentType = "application/x-www-form-urlencoded;charset=UTF-8"

            }
            if(typeof(push_loading) == 'undefined'){
                push_loading = true;
            }

            opt.complete = function(){
                if(push_loading){
                    $.loading.hide();
                }
            }
            if(push_loading){
                $.loading.show();
            }

            return $.ajax(opt);
        }
    }

    var mountSuccess = function(success){
        return function(args){
            var suc = success || function(){};
            var result = $.makeArray(arguments);
            if (result[0] && result[0].auth_uri) window.location.href = result[0].auth_uri;
            suc.apply(this, result);
        }
    }

    var mountError = function(error) {
        return function(args) {
          console.warn(args);
            if (args.status == 401 || args.status == 403) {
                $.wf(['/index.html'], function(page){ page.open(); });
                return;
            }
            error = error || $.noop;
            error.apply(this, $.makeArray(arguments));
        }
    }

    mount('projection', 'GET', '/g/projection/ProjectionFromTodayToMonth', 'getLimitedProjection');
    mount('projection', 'GET', '/s/projection/LastProjectionRequested', 'getLastRequested');
    mount('database', 'GET', '/g/spreadsheet/Storage', 'list');
    mount('database', 'PUT', '/s/spreadsheet/Storage', 'add');
    mount('database', 'POST', '/g/spreadsheet/Storage', 'create');

})(jQuery);
