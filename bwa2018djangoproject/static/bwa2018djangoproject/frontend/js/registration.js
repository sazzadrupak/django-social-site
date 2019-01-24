$(document).ready(function () {
    $('body').on('blur', '#id_email_test', function (e) {
        $.ajax({
            type: 'GET',
            url: '/ajax/check_uniqe_email_id',
            data: {'email_id' : $('#id_email').val()},
            dataType: 'JSON',
            success: function(data, textStatus, jqXHR) {
                // When AJAX call is successfuly
                $('.inputDisabled').prop("disabled", false); // Element(s) are now enabled.

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
});