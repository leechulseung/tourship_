var container = document.getElementById('map'); //지도를 담을 영역의 DOM 레퍼런스
var options = { //지도를 생성할 때 필요한 기본 옵션
	center: new daum.maps.LatLng(37.57484288719911, 126.93107087733638), //지도의 중심좌표.
	level: 13 //지도의 레벨(확대, 축소 정도)
};

var map = new daum.maps.Map(container, options); //지도 생성 및 객체 리턴

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

(function(daum, jQuery){

    var user = userLocations;
    var markerArray = [];

    console.log(user);

    for(var i = 0; i < user.locations.length; i++){
        markerArray.push(user.locations[i].location.split(","));
    }

    for (var i = 0; i < user.locations.length; i++) {
        var userMarker = new daum.maps.Marker({
            map: map,
            title: user.locations[i].post_id,
            position: new daum.maps.LatLng(markerArray[i][0], markerArray[i][1])
        });

        var infowindow = new daum.maps.InfoWindow({
            zIndex:1,
            content: '<div style="padding:5px;font-size:12px;margin-bottom:0px;"><p> '+ '제목 : ' + user.locations[i].title +' </p>' + '<p>' + '내용 : ' + user.locations[i].content + '</p></div>'
        });

        daum.maps.event.addListener(userMarker, 'mouseover', markerOver(map, userMarker, infowindow));
        daum.maps.event.addListener(userMarker, 'mouseout', markerOutOver(infowindow));
    }

    $(document).on('click','area[shape=poly]', function(e) {
        e.stopPropagation(); // 같은 영역에 속해있는 중복 클릭 방지 
        e.preventDefault();  // 이벤트 진행 중지 

        var pk = parseInt($(this)[0].title);
        var csrf=getCookie("csrftoken");
        
        $.ajax({
            type: 'post',
            url: user.url,
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

    function markerOver(map, userMarker, infowindow){
        return function(){
            infowindow.open(map, userMarker);
        };
    }

    function markerOutOver(infowindow){
        return function(){
            infowindow.close();
        };
    }

})(window.daum, window.jQuery);