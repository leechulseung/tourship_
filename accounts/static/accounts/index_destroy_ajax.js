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

  $('#destroy').on("click", addAnswer);
  function addAnswer(e){
    e.submit
    e.stopPropagation(); // 같은 영역에 속해있는 중복 클릭 방지
    e.preventDefault();  // 이벤트 진행 중지

    var pk = [];
    $("input[class='check_destroy']:checked").each(function(i){
      pk.push($(this).attr('name'));
    });
    // var pk = $('.check_destroy').attr('name'); //선택된 요소의 부모의 name속성 캐치

    var url = $(this).attr('value');

    var csrf = getCookie("csrftoken");
    if(pk==0){

    }else{
      var destroy = confirm('정말로 삭제하시겠 습니까?');
    }

    if(destroy){
      $.ajax({
           type : 'post', // post방식으로 전송
           url : url, // 서버로 보낼 url 주소
           data : {  // 서버로 보낼 데이터들 dict형식
            pk,
            'csrfmiddlewaretoken': csrf,
            },
            // 서버에서 리턴받아올 데이터 형식
           // dataType : 'json',
           //서버에서 무사히 html을 리턴하였다면 실행
           success : function(response){
            // location.reload();
            if(response["message"] == "success"){
              alert("삭제 되었습니다.")
              location.reload();
            }else{

            }
            //append(data);
           },

           //서버에서 html을 리턴해주지 못했다면
           error : function(response){
            alert("실패 하였다.");
           },

       });
    }else{

    }

  }

  $(document).ready(function(){
    $('#del_memory').on('hidden.bs.modal', function(e){
      $(this).find(".check_destroy").prop('checked', false);
      $(this).find("li").removeClass("active");
    });
  });


  $(document).on("click",'#searchs', function(e){

          e.submit;
          e.stopPropagation(); // 같은 영역에 속해있는 중복 클릭 방지
          e.preventDefault();  // 이벤트 진행 중지
          var url = $('.pagination_page').attr('href')
          searchs = $("#search_content").val();


          $.ajax({
            type: 'get',
            url: url,
            data:{
              'search':searchs,

            },
            success : function(data, states, J){
                  $('#pagination_index').remove();
                  $('#check_destroys').html(data);
            },
                 //서버에서 html을 리턴해주지 못했다면
           error : function(response){


              e.preventDefault();
              alert("실패 하였다.");

             },
          });
  });

$(document).on('click','.pagination_page', function(e){
  e.stopPropagation(); // 같은 영역에 속해있는 중복 클릭 방지
  e.preventDefault();  // 이벤트 진행 중지
  var search = $('#search-flag').val()
  var url = $(this).attr('href')
  var page = $(this).text()
  if(search){
    $.ajax({
      type: "get",
      url: url,
      data : {  // 서버로 보낼 데이터들 dict형식
        'page':page,
        'search':search,
      },

      dataType: "html",
      success: function(data){
          $('#pagination_index').remove();
          $('#check_destroys').html(data);
      },
      error: function(){
          alert("error");
      }
    });
  }else{
    $.ajax({
      type: "get",
      url: url,
      data : {  // 서버로 보낼 데이터들 dict형식
        'search': search,
        'page': page,
      },
      dataType: "html",
      success: function(data){
          $('#pagination_index').remove();
          $('#check_destroys').html(data);
      },
      error: function(){
          alert("error");
      }
    });
  }

});

$(document).on('click','#booking-sent',function(e){
  e.submit
  e.stopPropagation(); // 같은 영역에 속해있는 중복 클릭 방지
  e.preventDefault();  // 이벤트 진행 중지

  var title = $('#id_title').val()
  var content = $('#id_content').val()
  var location = $('#booking__hidden').val()
  var address = $('#memoryBooking__address').val()
  var to_user = $('#id_to_user').val()
  var csrf = getCookie("csrftoken");

  $.ajax({
    type : 'post',
    url : '',
    data : {
      'title':title,
      'content':content,
      'location':location,
      'address':address,
      'to_user':to_user,
      'csrfmiddlewaretoken': csrf,
    },
    
    success : function(data, states, J){
      $('#memoryBooking').modal('hide')
    },
                 //서버에서 html을 리턴해주지 못했다면
    error : function(response){
      alert("실패 하였다.");
    },
  });
})