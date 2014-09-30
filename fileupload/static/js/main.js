/*
 * jQuery File Upload Plugin JS Example 8.8.2
 * https://github.com/blueimp/jQuery-File-Upload
 *
 * Copyright 2010, Sebastian Tschan
 * https://blueimp.net
 *
 * Licensed under the MIT license:
 * http://www.opensource.org/licenses/MIT
 */

/*jslint nomen: true, regexp: true */
/*global $, window, blueimp */

$(function () {
    'use strict';

    // Initialize the jQuery File Upload widget:
    $('#fileupload').fileupload({
        // Uncomment the following to send cross-domain cookies:
        //xhrFields: {withCredentials: true},
        //url: 'server/php/'
    });

    // Enable iframe cross-domain access via redirect option:
    $('#fileupload').fileupload(
        'option',
        'redirect',
        window.location.href.replace(
            /\/[^\/]*$/,
            '/cors/result.html?%s'
        )
    );

    // Load existing files:
    $('#fileupload').addClass('fileupload-processing');
    $.get(
        '/upload/view/'
    ).done(function (result) {
            $('#fileupload').find("table").append(result);
            $('#fileupload').removeClass('fileupload-processing');
        });

});


function addItemPic(that, url) {
    var formData = new FormData($(that.form)[0]);
    $.ajax({
        type: 'POST',
        url: url,
        data: formData,
        cache: false,
        contentType: false,
        processData: false
    }).done(function (data) {
        $(data)
            .hide()
            .insertBefore($(that).closest('div'))
            .fadeIn(300);
    });
}


function deleteItemPic(that, url) {
    $.ajax({
        type: 'POST',
        url: url,
        data: {},
        cache: false,
        contentType: false,
        processData: false
    }).done(function (data) {
        $(that).closest('div.preview').fadeOut(300, function () {
            this.remove();
        });
    });
}