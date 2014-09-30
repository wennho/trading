function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function sameOrigin(url) {
    // test that a given url is a same-origin URL
    // url could be relative or scheme relative or absolute
    var host = document.location.host; // host + port
    var protocol = document.location.protocol;
    var sr_origin = '//' + host;
    var origin = protocol + sr_origin;
    // Allow absolute or scheme relative URLs to same origin
    return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
        (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
        // or any other URL that isn't scheme relative or absolute i.e relative.
        !(/^(\/\/|http:|https:).*/.test(url));
}

$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
            // Send the token to same-origin, relative URLs only.
            // Send the token only if the method warrants CSRF protection
            // Using the CSRFToken value acquired earlier
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

function avoidEnter(e) {
    e.preventDefault(); //prevent default form submit
    $(this).find('button').click();
}

function update(data, id) {
    $(id).hide().empty().append(data).fadeIn();
    $(id).find('form').submit(avoidEnter);
}

function createBid(itemId) {
    var itemIdBidForm = '#' + itemId + '-form';

    $.post(
            getUrl('peerShop:bid-new'),
            $(itemIdBidForm).serialize()
        ).done(
        function (data) {
            update(data, '#' + itemId);
        });
}

function updateBid(bid, callbackFun) {
    var bidId = '#' + bid + '-update-form';
    $.post(
            getUrl('peerShop:bid-update', bid),
            $(bidId).serialize()
        ).done(
        function (data) {
            update(data, '#' + bid + '-bid');
        });
}

function changeBidStatus(bid, status) {

    $.post(
            getUrl('peerShop:bid-update', bid),
            $('#' + bid + '-status-form').serialize() + '&status=' + status
        ).done(
        function (data) {
            $('#' + bid + '-status').hide().empty().append(status).fadeIn();
            $('#'+bid+'-Accepted').toggleClass("hide");
            $('#'+bid+'-Declined').toggleClass("hide");
            $('#'+bid+'--').toggleClass("hide");
        });
}

function deleteBid(bid) {
    $.post(
        getUrl('peerShop:bid-delete', bid),
        {}
    ).done(
        function (data) {
            update(data, '#' + bid + '-bid');
        });
}


$(document).ready(function () {
    $(".bid-container").find("form").submit(avoidEnter);
});
