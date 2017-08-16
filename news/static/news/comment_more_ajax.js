$(document).on('click', '#comment-more', function(){
   var pk = $(this).attr('name');
 	 var url = $(this).attr('href');
 	 var csrf = getCookie("csrftoken");

     $.ajax({
       type: "POST",
       url: url,
       data: {
         'pk': pk,
         'csrfmiddlewaretoken': csrf,
       },
       dataType: "html",
 
       success: function(data, textStatus, jqXHR){
         $('#ajax-comment').append(data);
         $("#comment-more").remove()
       },
 
       error: function(request, status, error){
         alert("code:"+request.status+"\n"+"message:"+request.responseText+"\n"+"error:"+error);
         alert("문제가 발생했습니다.");
       },
     })
   })