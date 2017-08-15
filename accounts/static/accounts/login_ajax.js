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
// unbind().bind() 더블클릭 방지
$('#login').on("click", addAnswer);

        function addAnswer(e){

        e.submit;
        e.stopPropagation(); // 같은 영역에 속해있는 중복 클릭 방지
        e.preventDefault();  // 이벤트 진행 중지
        console.log(e);

        username = $("#id_username").val();
        console.log(username);
        password = $("#id_password").val();
        console.log(password);
        var csrf = getCookie("csrftoken");


        $.ajax({
               type : 'post', // post방식으로 전송
               url : "", // 서버로 보낼 url 주소
               data : {  // 서버로 보낼 데이터들 dict형식
                'username':username,
                'password':password,
                'csrfmiddlewaretoken': csrf,
                },
                // dataType : 'html',
                // 서버에서 리턴받아올 데이터 형식

               //서버에서 무사히 html을 리턴하였다면 실행
               success : function(response){
                console.log(e);
                //append(data);
                if(response["result"] == "success"){
                  console.log(" 아이디 비번 맞늠 success");
                  location.reload();
                }else{
                  console.log("틀림ㅐㅇㅇㅇㅇㅇㅇㅇㅇ");
                  $('#id_username').val("");
                  $('#id_password').val("");
                  $('#loginerror').html(response);
                  console.log(response);
                }

               },

               //서버에서 html을 리턴해주지 못했다면
               error : function(response){

                // console.log(response);
                e.preventDefault();
                alert("실패 하였다.");

               },

           });
       }

