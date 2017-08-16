$(document).on("click",".ajaxButton",addAnswer);

        function addAnswer(e){
        e.submit
        e.stopPropagation(); // 같은 영역에 속해있는 중복 클릭 방지 
        e.preventDefault();  // 이벤트 진행 중지 
        
        var pk = $(this).parent().attr('name'); //선택된 요소의 부모의 name속성 캐치
        var message = $('#id_message').val()

        var csrf = getCookie("csrftoken");
        if($('.message'+pk+' #id_message').val()==''){

        }else{
        $.ajax({
               type : 'post', // post방식으로 전송
               url : "modal/", // 서버로 보낼 url 주소
               data : {  // 서버로 보낼 데이터들 dict형식 
                'pk':pk,
                'message': message,
                'csrfmiddlewaretoken': csrf,
                },
                // 서버에서 리턴받아올 데이터 형식
               dataType : 'html',  

               //서버에서 무사히 html을 리턴하였다면 실행 
               success : function(data, textStatus, jqXHR){ 
                $('#id_message').val("")
                $('#ajax-comment').append(data);
                //append(data);
               },

               //서버에서 html을 리턴해주지 못했다면 
               error : function(data, textStatus, jqXHR){
                alert("실패 하였다.");
               },
               
           });}
       }

