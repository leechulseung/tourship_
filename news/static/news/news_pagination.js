$(document).on('click', '#callmorepost', function(){
    var page = $("#page").val();
    var end_page = endpage;

    if(page > end_page){
      return;
    }
    callMorePostAjax(page);
    $("#page").val(parseInt(page)+1);
  });

  $(window).scroll(function(){
    var scrollHeight = $(window).scrollTop() + $(window).height();
    var documentHeight = $(document).height();
    
    // console.log("documentHeight:" + documentHeight);
    // console.log("windowHeight:" + $(window).height());
    // console.log("scrollHeight:" + scrollHeight);
    if (scrollHeight  >= documentHeight){
      var page = $("#page").val();
      var end_page = endpage
      if(page > end_page){
        return;
      }
      callMorePostAjax(page);
      $("#page").val(parseInt(page)+1);
    }
  });

  function callMorePostAjax(page) {
    var end_page = endpage
    var csrf = getCookie("csrftoken");
    if(page > end_page){
      return;
    }

    $.ajax({
      type : 'POST',
      url: "",
      data: {
        'page': page,
        'csrfmiddlewaretoken': csrf
      },
      success: addMorePostAjax,
      dataType: 'html',
      error: function(request, status, error){
        alert('스크롤에러 관리자에게 문의')
        // alert("code:"+request.status+"\n"+"message:"+request.responseText+"\n"+"error:"+error);
      },
    });
  }

  function addMorePostAjax(data, textStatus, jqXHR) {
    $('#post_list_ajax').append(data).trigger("create");
  }