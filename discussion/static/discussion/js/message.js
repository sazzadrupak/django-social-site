$(document).ready(function () {
    $('[data-toggle="popover"]').popover({
        html: true,
        content: function() {
            let post_id = $(this).data('post_id');
            isPaused = true;
            return $('#popover-content-'+post_id).html();
        },
    });

    $('body').on('click', '.edit_chat_event', function () {
        isPaused = true;
        $('[data-toggle="popover"]').popover('hide');
        let chat_id = $(this).data('chat_id');
        $.ajax({
            type: 'GET',
            url: '/discussion/get_message/'+chat_id,
            dataType: 'HTML',
            beforeSend: function(){

            },
            success: function(data, textStatus, jqXHR) {
                $('#message_area_'+chat_id).html(data);
                console.log(data)
            },
            error: function(jqXHR, textStatus, errorThrown) {
                // When AJAX call has failed
                console.log(textStatus + ': ' + errorThrown);
            },
            complete: function() {
                // When AJAX call is complete, will fire upon success or when error is thrown
                console.log('AJAX call completed');
            }
        });
    });

    $('body').on('submit', '.edit_chat', function (event) {
        isPaused = true;
        event.preventDefault();

        let chat_id = $('.edit_chat input[name="chat_id"]').val();
        console.log(chat_id);
        $.ajax({
            type: 'POST',
            url: '/discussion/chat_update',
            data: $( this ).serialize(),
            dataType: 'HTML',
            beforeSend: function(){

            },
            success: function(data, textStatus, jqXHR) {
                $('#message_area_'+chat_id).html(data);
                isPaused = false;
            },
            error: function(jqXHR, textStatus, errorThrown) {
                // When AJAX call has failed
                console.log('AJAX call failed.');
                console.log(textStatus + ': ' + errorThrown);
            },
            complete: function() {
                // When AJAX call is complete, will fire upon success or when error is thrown
                console.log('AJAX call completed');
            }
        });
    });

    $('body').on('click', '.cancel_message_edit', function () {
        let chat_id = $(this).data('chat_id');
        let head_id = $(this).data('head_id');
        $.ajax({
            type: 'GET',
            url: '/discussion/cancel_message_edit/'+chat_id+'/'+head_id,
            dataType: 'HTML',
            beforeSend: function(){

            },
            success: function(data, textStatus, jqXHR) {
                $('#message_area_'+chat_id).html(data);
                isPaused = false;
            },
            error: function(jqXHR, textStatus, errorThrown) {
                // When AJAX call has failed
                console.log('AJAX call failed.');
                console.log(textStatus + ': ' + errorThrown);
            },
            complete: function() {
                // When AJAX call is complete, will fire upon success or when error is thrown
                console.log('AJAX call completed');
            }
        });
    });
    
    $('body').on('click', '.delete_chat_event', function () {
        isPaused = true;
        $('[data-toggle="popover"]').popover('hide');
        if (confirm('Are you sure?')) {
            let chat_id = $(this).data('chat_id');

            $.ajax({
                type: 'GET',
                url: '/discussion/delete_chat/'+chat_id,
                dataType: 'JSON',
                beforeSend: function(){

                },
                success: function(data, textStatus, jqXHR) {
                    console.log(chat_id);
                    $('#message_text_'+chat_id).remove();
                    isPaused = false;
                },
                error: function(jqXHR, textStatus, errorThrown) {
                    // When AJAX call has failed
                    console.log('AJAX call failed.');
                    console.log(textStatus + ': ' + errorThrown);
                },
                complete: function() {
                    // When AJAX call is complete, will fire upon success or when error is thrown
                    console.log('AJAX call completed');
                }
            });
        } else {
            isPaused = false;
            return true;
        }
    })

});