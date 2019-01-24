let global_discussion_head_id = 0;
let isPaused = false;
if(document.title === 'All discussions' || document.title === 'Chat history'){
    console.log(document.title);
    let timer = window.setInterval(function() {
        if(!isPaused){
            add_chat_after_view(global_discussion_head_id);
        }
     }, 5000);
}
$(document).ready(function () {
    $('.discussion_dropdown').find('form').click(function (e) {
        e.stopPropagation();
    });

    if(document.title === 'All discussions' || document.title === 'Chat history') {
        $(".head_msg_history").stop().animate({scrollTop: $(".head_msg_history")[0].scrollHeight}, 1000);
    }
    global_discussion_head_id = $("input[name=discussion_head_id]").val();

    $('body').on('focus', '#id_head_name', function (e) {
        isPaused = true;
        console.log('paused');
    });

    $('body').on('blur', '#id_head_name', function (e) {
        isPaused = false;
        console.log('not paused');
    });

    $('body').on('submit', '#discussion_head_form', function (e) {
        e.preventDefault();
        let form = $(this);
        $.ajax({
            type: 'POST',
            url: '/discussion/create_new_discussion',
            data: form.serialize(),
            cache: false,
            beforeSend: function(){

            },
            success: function(response, textStatus, jqXHR) {
                $(".discussion_dropdown").html(response);

            },
            error: function(jqXHR, textStatus, errorThrown) {
                // When AJAX call has failed
                console.log('AJAX call failed.');
                console.log(textStatus + ': ' + errorThrown);
            },
            complete: function() {
                // When AJAX call is complete, will fire upon success or when error is thrown
                console.log('AJAX call completed');
                if(document.title === 'All discussions') {
                    discussion_head_view_update();
                    global_discussion_head_id = $("input[name=discussion_head_id]").val();
                }
            }
        });
    });

    $('body').on('click', '.chat_head', function () {
        let discussion_head_id = $(this).data('discussion_head_id');
        $.ajax({
            type: 'GET',
            url: '/discussion/get_discussion_head_texts/'+discussion_head_id,
            cache: false,
            beforeSend: function(){
                $('.loader').css("display", "block");
            },
            success: function(response, textStatus, jqXHR) {
                // When AJAX call is successfuly
                // console.log(response); // Element(s) are now enabled.
                $('.head_messages').html(response);
            },
            error: function(jqXHR, textStatus, errorThrown) {
                // When AJAX call has failed
                console.log('AJAX call failed.');
                console.log(textStatus + ': ' + errorThrown);
            },
            complete: function() {
                // When AJAX call is complete, will fire upon success or when error is thrown
                console.log('AJAX call completed');
                $(".chat_list").removeClass("active_chat");
                $(".head_msg_history").stop().animate({ scrollTop: $(".head_msg_history")[0].scrollHeight}, 1000);
                $("#chat_head_"+discussion_head_id).addClass("active_chat");
                global_discussion_head_id = discussion_head_id;
                $('.loader').css("display", "none");
            }
        });
    });

    $('body').on('submit', '.add_chat', function (e) {
        e.preventDefault();
        let form = $(this);
        let form_data = form.serializeArray();
        $.ajax({
            type: 'POST',
            url: '/discussion/save_chat',
            cache: false,
            data: form_data,
            beforeSend: function(){
                $('.loader').css("display", "block");
            },
            success: function(response, textStatus, jqXHR) {
                // When AJAX call is successfuly
                // Element(s) are now enabled.
                // console.log(document.forms['add_chat']['discussion_head_id'].value);
                console.log(response);
                document.forms['add_chat']['message'].value = '';
                if (response === '1'){
                    add_chat_after_view(document.forms['add_chat']['discussion_head_id'].value);
                }
                else{

                }
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

    $('body').on('keyup', '.search_value', function (e) {
        if($(this).val().length > 2){
            isPaused = true;
            let csrfmiddlewaretoken = $('.all_discussion_search').find('input[name="csrfmiddlewaretoken"]').val();
            $.ajax({
                type: 'POST',
                url: '/discussion/all_discussion_search_result',
                data: {'search_value': $(this).val(), 'csrfmiddlewaretoken': csrfmiddlewaretoken},
                cache: false,
                beforeSend: function(){
                    $(".all_discussion_search .fa").removeClass("fa-search");
                    $(".all_discussion_search .fa").addClass("fa-spinner fa-spin");
                },
                success: function(response, textStatus, jqXHR) {
                    // When AJAX call is successfuly
                    // Element(s) are now enabled.
                    $('.head-list-items').html(response);
                },
                error: function(jqXHR, textStatus, errorThrown) {
                    // When AJAX call has failed
                    console.log('AJAX call failed.');
                    console.log(textStatus + ': ' + errorThrown);
                },
                complete: function() {
                    // When AJAX call is complete, will fire upon success or when error is thrown
                    console.log('AJAX call completed');
                    //$(".head_msg_history").stop().animate({ scrollTop: $(".head_msg_history")[0].scrollHeight}, 1000);
                    //$('.loader').css("display", "none");
                    $(".all_discussion_search .fa").removeClass("fa-spinner fa-spin");
                    $(".all_discussion_search .fa").addClass("fa-close");
                }
            });
        }
    });

    $('body').on('click', '.fa-close', function () {
        $(".all_discussion_search .fa").removeClass("fa-close");
        $(".all_discussion_search .fa").addClass("fa-search");
        isPaused = false;
        $('.all_discussion_search').find('input[name="search_value"]').val('');
        add_chat_after_view(global_discussion_head_id);
    });

    $('body').on('keyup', '.text_search_value', function (e) {
        if($(this).val().length > 2){
            isPaused = true;
            let csrfmiddlewaretoken = $('.single_discussion_search').find('input[name="csrfmiddlewaretoken"]').val();
            $.ajax({
                type: 'POST',
                url: '/discussion/single_discussion_search_result',
                data: {'search_value': $(this).val(), 'csrfmiddlewaretoken': csrfmiddlewaretoken, 'discussion_head_id': global_discussion_head_id},
                cache: false,
                beforeSend: function(){
                    $(".single_discussion_search .fa").removeClass("fa-search");
                    $(".single_discussion_search .fa").addClass("fa-spinner fa-spin");
                },
                success: function(response, textStatus, jqXHR) {
                    // When AJAX call is successfuly
                    // Element(s) are now enabled.
                    $('#head_msg_history_'+global_discussion_head_id).html(response);
                },
                error: function(jqXHR, textStatus, errorThrown) {
                    // When AJAX call has failed
                    console.log('AJAX call failed.');
                    console.log(textStatus + ': ' + errorThrown);
                },
                complete: function() {
                    // When AJAX call is complete, will fire upon success or when error is thrown
                    console.log('AJAX call completed');
                    //$(".head_msg_history").stop().animate({ scrollTop: $(".head_msg_history")[0].scrollHeight}, 1000);
                    //$('.loader').css("display", "none");
                    $(".single_discussion_search .fa").removeClass("fa-spinner fa-spin");
                    $(".single_discussion_search .fa").addClass("fa-close");
                }
            });
        }
    });
});

function discussion_head_view_update() {
    $.ajax({
        type: 'GET',
        url: '/discussion/discussion_head_view_update',
        cache: false,
        beforeSend: function(){
            $('.loader').css("display", "block");
        },
        success: function(response, textStatus, jqXHR) {
            // When AJAX call is successfuly
            // Element(s) are now enabled.
            $('.discussion_div').html(response);
        },
        error: function(jqXHR, textStatus, errorThrown) {
            // When AJAX call has failed
            console.log('AJAX call failed.');
            console.log(textStatus + ': ' + errorThrown);
        },
        complete: function() {
            // When AJAX call is complete, will fire upon success or when error is thrown
            console.log('AJAX call completed');
            $(".head_msg_history").stop().animate({ scrollTop: $(".head_msg_history")[0].scrollHeight}, 1000);
            $('.loader').css("display", "none");
        }
    });
}

function add_chat_after_view(discussion_head_id) {
    $.ajax({
        type: 'GET',
        url: '/discussion/add_chat_after_view/'+discussion_head_id,
        cache: false,
        beforeSend: function(){
            //$('.loader').css("display", "block");
        },
        success: function(response, textStatus, jqXHR) {
            // When AJAX call is successfuly
            // Element(s) are now enabled.
            $('#head_msg_history_'+discussion_head_id).html(response);
        },
        error: function(jqXHR, textStatus, errorThrown) {
            // When AJAX call has failed
            console.log('AJAX call failed.');
            console.log(textStatus + ': ' + errorThrown);
        },
        complete: function() {
            // When AJAX call is complete, will fire upon success or when error is thrown
            console.log('AJAX call completed');
            $(".chat_list").removeClass("active_chat");
            $(".head_msg_history").stop().animate({ scrollTop: $(".head_msg_history")[0].scrollHeight}, 1000);
            $("#chat_head_"+discussion_head_id).addClass("active_chat");
            $('[data-toggle="popover"]').popover({
                html: true,
                content: function() {
                    let post_id = $(this).data('post_id');
                    isPaused = true;
                    return $('#popover-content-'+post_id).html();
                },
            });
            global_discussion_head_id = discussion_head_id;
            if(document.title === 'All discussions') {
                discussion_head_lists_update(global_discussion_head_id);
            }else{
                $('.loader').css("display", "none");
            }
        }
    });
}

function discussion_head_lists_update(global_discussion_head_id){
    $.ajax({
        type: 'GET',
        url: '/discussion/discussion_head_lists_update/'+global_discussion_head_id,
        cache: false,
        beforeSend: function(){
            // $('.loader').css("display", "block");
        },
        success: function(response, textStatus, jqXHR) {
            // When AJAX call is successfuly
            // Element(s) are now enabled.
            $('.head-list-items').html(response);
        },
        error: function(jqXHR, textStatus, errorThrown) {
            // When AJAX call has failed
            console.log('AJAX call failed.');
            console.log(textStatus + ': ' + errorThrown);
        },
        complete: function() {
            // When AJAX call is complete, will fire upon success or when error is thrown
            console.log('AJAX call completed');
            $(".chat_list").removeClass("active_chat");
            $(".head_msg_history").stop().animate({ scrollTop: $(".head_msg_history")[0].scrollHeight}, 1000);
            $("#chat_head_"+global_discussion_head_id).addClass("active_chat");
            global_discussion_head_id = global_discussion_head_id;
            $('.loader').css("display", "none");
        }
    });
}