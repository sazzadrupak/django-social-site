$(document).ready(function () {

    $('body').on('submit', '.comment_submit', function (event) {
        event.preventDefault();
        var post_id = $("[name='post_id']", this).val();
        // console.log(status_id);
        $.ajax({
            type: 'POST',
            url: '/comment_add/',
            data: $( this ).serialize(),
            dataType: 'HTML',
            beforeSend: function(){
                $('#comment_add_'+post_id)[0].reset();
            },
            success: function(data, textStatus, jqXHR) {
                $('#comment_of_status_'+post_id).html(data);
            },
            error: function(jqXHR, textStatus, errorThrown) {
                // When AJAX call has failed
                console.log('AJAX call failed.');
                console.log(textStatus + ': ' + errorThrown);
            },
            complete: function() {
                // When AJAX call is complete, will fire upon success or when error is thrown
                console.log('AJAX call completed');
                $('[data-toggle="popover"]').popover({
                    html: true,
                    content: function() {
                        let post_id = $(this).data('post_id');
                        return $('#popover-content-'+post_id).html();
                    },
                });

                $('[data-toggle="popover-comment"]').popover({
                    html: true,
                    content: function() {
                        let post_id = $(this).data('post_id');
                        return $('#popover-comment-content-'+post_id).html();
                    },
                });
            }
        });
    });

    $('[data-toggle="popover"]').popover({
        html: true,
        content: function() {
            let post_id = $(this).data('post_id');
            return $('#popover-content-'+post_id).html();
        },
    });

    $('[data-toggle="popover-comment"]').popover({
        html: true,
        content: function() {
            let post_id = $(this).data('post_id');
            return $('#popover-comment-content-'+post_id).html();
        },
    });

    $('body').on('click', '.popover-content', function(e) {
        if(document.title === 'Chat history'){
            isPaused = true;
            console.log("clicked won't work");
        }else{
            $('[data-toggle="popover"]').popover('hide');
            $('[data-toggle="popover-comment"]').popover('hide');
            console.log("clicked inside ppppopover");
        }
    });

    
    $('body').on('click', '.edit_comment_event', function () {
        let comment_id = $(this).data('comment_id');
        $.ajax({
            type: 'GET',
            url: '/get_comment/'+comment_id,
            dataType: 'HTML',
            beforeSend: function(){

            },
            success: function(data, textStatus, jqXHR) {
                $('#comment_area_'+comment_id).html(data);
                console.log(data)
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

    $('body').on('click', '.cancel_comment_edit', function () {
        let comment_id = $(this).data('comment_id');
        let post_id = $(this).data('post_id');
        $.ajax({
            type: 'GET',
            url: '/cancel_comment_edit/'+comment_id+'/'+post_id,
            dataType: 'HTML',
            beforeSend: function(){

            },
            success: function(data, textStatus, jqXHR) {
                $('#comment_area_'+comment_id).html(data);
                console.log(data)
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

    $('body').on('submit', '.comment_edit', function (event) {
        event.preventDefault();

        let comment_id = $('.comment_edit input[name="comment_id"]').val();
        console.log(comment_id);
        $.ajax({
            type: 'POST',
            url: '/comment_update',
            data: $( this ).serialize(),
            dataType: 'HTML',
            beforeSend: function(){

            },
            success: function(data, textStatus, jqXHR) {
                $('#comment_area_'+comment_id).html(data);
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
    
    $('body').on('click', '.delete_comment', function (e) {
        if (confirm('Are you sure?')) {
            let comment_id = $(this).data('comment_id');
            let post_id = $(this).data('post_id');

            $.ajax({
            type: 'GET',
            url: '/delete_comment/'+comment_id+'/'+post_id,
            dataType: 'JSON',
            beforeSend: function(){

            },
            success: function(data, textStatus, jqXHR) {
                console.log(comment_id);
                $('#comment_li_'+comment_id).remove();
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

        }
    })
});