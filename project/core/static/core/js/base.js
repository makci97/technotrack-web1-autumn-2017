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

    function setOnClickForLikes() {
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
                        alert('Need to login');
                    },
                    dataType: 'html'
                });

                function likeComment(data, textStatus, jqXHR){
                    like_span_id = '#thumb_comment_' + objectId;
                    $(like_span_id).html(data);
                    setOnClickForLikes();
                }

            });
    }

    setOnClickForLikes();
    updateComments();

    window.setInterval(updateComments, 3000);
});