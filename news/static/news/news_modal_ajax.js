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

$(document).on('click','.modalStart', function(e) {
    e.stopPropagation(); // 같은 영역에 속해있는 중복 클릭 방지 
    e.preventDefault();  // 이벤트 진행 중지 
    

	var pk = $(this).attr('name');

    var url = $(this).attr('href');
    var csrf=getCookie("csrftoken");
    $.ajax({
        type: 'post',
        url: url,
        data: {
        	'pk':pk,
            'page':'gogo',
        	'csrfmiddlewaretoken': csrf
        },
    	success: function (data, textStatus, jqXHR) {
            $('#post-modal').find('.post-modal-content').html(data);
            $('#post-modal').modal('show');
        },
    });
});