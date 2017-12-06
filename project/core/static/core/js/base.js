$(document).ready(function() {
    function updateComments() {
        if ($('.comments').length > 0) {
            $.get($('.comments').data('comments-url'), function (data) {
                $('.comments').html(data);
            });
        }
    }

    function openDialog() {
        $('.modal').modal('show');
    }

    $(document).on('click', '.open_dialog', function (event) {
        openDialog();
        $.get(this.href, function (data) {
            $('.modal').html(data);
        });
        event.preventDefault();
    });

    $(document).on('submit', '[data-formtype="ajaxForm"]', function (event) {
        $.post(this.action, $(this).serialize(), function (data) {
            console.log(data);
            if (data == 'OK') {
                document.location.reload();
            } else {
                $('.modal').html(data);
            }
        });
        event.preventDefault();
    });

    $('.thumb_comment').click(function() {
        var indx = $('.thumb_comment').index(this);
        var objectId = $('.comment-content:eq('+indx+')').data('comment-id');
        $.ajax({
            type: 'POST',
            url: '/likes/',
            data: {
                'content_type': 'Comment',
                'object_id': objectId,
                'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
            },
            success: likeComment,
            error: function () {
                alert('error');
            },
            dataType: 'html'
        });

        function likeComment(data, textStatus, jqXHR){
            console.log($.parseHTML(data));
            // alert($(data)[0].outerHTML.find(".okey"));
            // alert($(data).find(".okey").text());
            var okey = $(data).find(".okey").text();
            var likes_count = $(data).find(".likes_count").text();
            // alert(okey);
            // alert(likes_count);
            if($.trim(data) == 'new' || $.trim(data) == 'true') {
                $('.thumb_comment:eq('+indx+')').addClass( "liked" );
                $('.thumb_comment_count:eq('+indx+')').addClass( "liked" );
            } else if($.trim(data) == 'false') {
                $('.thumb_comment:eq('+indx+')').removeClass( "liked" );
            }
        }

    });
    // updateComments();
    //window.setInterval(updateComments, 3000);


});