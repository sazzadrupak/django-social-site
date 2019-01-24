
let notification_timer = window.setInterval(function() {
    if(!isPaused){
        get_all_notification();
    }
 }, 15000);

$(document).ready(function () {
    $('body').on('click', '.notification_icon', function (e) {
        $.ajax({
            type: 'GET',
            url: '/notification/ajax/notification_status_change', // change the status of users all notification
            dataType: 'JSON',
            success: function (data, textStatus, jqXHR) {
                // When AJAX call is successfuly
                console.log(data['post_status']);
                $('.badge-notify').html("0"); // Element(s) are now enabled.

            },
            error: function (jqXHR, textStatus, errorThrown) {
                // When AJAX call has failed
                console.log('AJAX call failed.');
                console.log(textStatus + ': ' + errorThrown);
            },
            complete: function () {
                // When AJAX call is complete, will fire upon success or when error is thrown
                console.log('AJAX call completed');
            }
        });
    });

    $("#all_search").autocomplete({
        source: '/profile/user_search/',
        minLength: 2,
        select: function (event, ui) {
            console.log(ui.item.label);
            let url = ui.item.url
            window.open(url, '_blank ');
        }
    });
});

function get_all_notification() {
    $.ajax({
        type: 'GET',
        url: '/notification/get_all_notification_info', // change the status of users all notification
        dataType: 'HTML',
        success: function (data, textStatus, jqXHR) {
            // When AJAX call is successfuly
            $('#notification_li').html(data);
             // Element(s) are now enabled.

        },
        error: function (jqXHR, textStatus, errorThrown) {
            // When AJAX call has failed
            console.log('AJAX call failed.');
            console.log(textStatus + ': ' + errorThrown);
        },
        complete: function () {
            // When AJAX call is complete, will fire upon success or when error is thrown
            get_discussion_notification();
        }
    });
}

function get_discussion_notification() {
    $.ajax({
        type: 'GET',
        url: '/discussion/get_discussion_info', // change the status of users all notification
        dataType: 'HTML',
        success: function (data, textStatus, jqXHR) {
            // When AJAX call is successfuly
            $('#discussion_li').html(data);
             // Element(s) are now enabled.

        },
        error: function (jqXHR, textStatus, errorThrown) {
            // When AJAX call has failed
            console.log('AJAX call failed.');
            console.log(textStatus + ': ' + errorThrown);
        },
        complete: function () {
            // When AJAX call is complete, will fire upon success or when error is thrown
        }
    });
}