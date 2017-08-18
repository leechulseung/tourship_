/*global jQuery*/
/*global daum*/
/*global navigator*/
// $("html").niceScroll();
var $ = jQuery;
var mapContainer = $('#after_login__map')[0];
var mapOptions = {
    center: new daum.maps.LatLng(37.57484288719911, 126.93107087733638),
    level: 13
};

var map = new daum.maps.Map(mapContainer, mapOptions);
var geocoder = new daum.maps.services.Geocoder();
var ps = new daum.maps.services.Places(map);

// 지도에 확대 축소 컨트롤을 생성한다
var zoomControl = new daum.maps.ZoomControl();

// 지도의 우측에 확대 축소 컨트롤을 추가한다
map.addControl(zoomControl, daum.maps.ControlPosition.RIGHT);

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

    // 공통
    var user = userLocations;

    // 추억 마커 코드
    var markerLocationArray = [];
    var userMarkerArray = [];

    // 예약 마커 코드
    var bookingLocationArray = [];
    var bookingMarkerArray = [];
    var memoryIcon = new daum.maps.MarkerImage(
        "/static/img/memory_pin3.png",
        new daum.maps.Size(40, 42),
        {
            offset: new daum.maps.Point(16, 34),
            alt: "momoeyIcon",
            shape: "poly",
            coords: "1,20,1,9,5,2,10,0,21,0,27,3,30,9,30,20,17,33,14,33"
        }
    );

    console.log(user);
    // 추억추가 마커 코드
    for(var i = 0; i < user.locations.length; i++){
        markerLocationArray.push(user.locations[i].location.split(","));
    }

    for (var i = 0; i < user.locations.length; i++) {
        var userMarker = new daum.maps.Marker({
            map: map,
            title: user.locations[i].post_id,
            position: new daum.maps.LatLng(markerLocationArray[i][0], markerLocationArray[i][1]),
            opacity: 0
        });

        var infowindow = new daum.maps.InfoWindow({
            zIndex:1,
            content: '<div style="padding:5px;font-size:12px;"><p> '+ '제목 : ' + user.locations[i].title +' </p>' + '<p>' + '내용 : ' + user.locations[i].content + '</p></div>'
        });

        userMarkerArray.push(userMarker);

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

    $(document).on("click",".ajaxButton",function(e){
        e.submit
        e.stopPropagation(); // 같은 영역에 속해있는 중복 클릭 방지 
        e.preventDefault();  // 이벤트 진행 중지 
        
        var pk = parseInt($("area[shape=poly]")[0].title);
        var message = $('#id_message').val()

        var csrf = getCookie("csrftoken");
        if($('.message'+pk+' #id_message').val()==''){

        }else{
            $.ajax({
               type : 'post', // post방식으로 전송
               url : user.url, // 서버로 보낼 url 주소
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
    });

    $(document).on('click', '#comment-more', function(){
         var pk = parseInt($("area[shape=poly]")[0].title);
         // var url = $(this).attr('href');
         var csrf = getCookie("csrftoken");

         $.ajax({
           type: "POST",
           url: user.more_url,
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
    // 추억추가 마커 코드 끝
    
    // 예약추가 마커 코드 시작
    for(var i = 0; i < user.booking_locations.length; i++){
        bookingLocationArray.push(user.booking_locations[i].location.split(","));
    }

    for (var i = 0; i < user.booking_locations.length; i++) {
        var bookingMarker = new daum.maps.Marker({
            map: map,
            title: user.booking_locations[i].post_id,
            position: new daum.maps.LatLng(bookingLocationArray[i][0], bookingLocationArray[i][1]),
            image: memoryIcon
        });

        var bookingMarker_infowindow = new daum.maps.InfoWindow({
            zIndex:1,
            content: '<div style="padding:5px;font-size:12px;"><p> '+ '이름 : ' + user.booking_locations[i].username +' </p>' + '<p>' + '제목 : ' + user.booking_locations[i].title + '</p></div>'
        });

        bookingMarkerArray.push(bookingMarker);

        daum.maps.event.addListener(bookingMarker, 'mouseover', markerOver(map, bookingMarker, bookingMarker_infowindow));
        daum.maps.event.addListener(bookingMarker, 'mouseout', markerOutOver(bookingMarker_infowindow));
    }
        
    // 예약추가 마커 코드 끝
    

    $(document).on('click', '#all_view', function(){
        console.log("전체보기");
        for(var i = 0; i < userMarkerArray.length; i++){
            userMarkerArray[i].setMap(map);
        }
    });

    $(document).on('click', '#memory_pin_view', function(){
        console.log("추억 핀 보기");
        for(var i = 0; i < userMarkerArray.length; i++){
            userMarkerArray[i].setMap(map);
        }

    });

    $(document).on('click', '#booking_pin_view', function(){
        console.log("예약 핀 보기");
        for(var i = 0; i < userMarkerArray.length; i++){
            userMarkerArray[i].setMap(null);
        }
    });

})(window.daum, window.jQuery);

// 오제웅 Start
(function(daum, jQuery){

    var j = 0;
    var markerMake = $('#markerMake')[0], memory_booking = $('#memory_booking')[0];
    var content = '<div id="img"></div>';
    var memory_content = '<div id="memory_img"></div>'

    var markerArray = [];

    var moveMarker = new daum.maps.Marker();
    var selectMarker = null;

    var curOverlay = new daum.maps.CustomOverlay({
        map: map
    });
    var booking_curOverlay = new daum.maps.CustomOverlay({
        map: map
    });

    function callModal(){
        $('#add_memory').modal('show');
    }

    function handleMove(e){
        var latlng = e.latLng;
        map.setCursor("default");
        curOverlay.setContent(content);
        curOverlay.setPosition(latlng);
    }

    function callAddress(result, status) {
        if (status === daum.maps.services.Status.OK) {
            $('#id_address')[0].value = result[0].address.address_name;
        }
    }

    function handleClick(e) {
        var latlng = e.latLng;
        var getLatgetLng = null;

        callModal();
        getLatgetLng = latlng.getLat() + ',' + latlng.getLng();
        $('#getLatgetLng').attr("value", getLatgetLng);

        daum.maps.event.removeListener(map, 'click', handleClick);
        daum.maps.event.removeListener(map, 'mousemove', handleMove);
        geocoder.coord2Address(latlng.getLng(), latlng.getLat(), callAddress);

        map.setCursor(null);
        curOverlay.setVisible(false);
    }

    function cancelClick(e){
        daum.maps.event.removeListener(map, 'click', handleClick);
        daum.maps.event.removeListener(map, 'mousemove', handleMove);
        daum.maps.event.removeListener(map, 'rightclick', cancelClick);
        map.setCursor(null);
        curOverlay.setVisible(false);
    }

    $(document).on('click', '#markerMake', function(){
        console.log("마커생성");
        curOverlay.setVisible(true);
        daum.maps.event.addListener(map, 'click', handleClick);
        daum.maps.event.addListener(map, 'rightclick', cancelClick);
        daum.maps.event.addListener(map, 'mousemove', handleMove);
    });

    ///////////////////////////////////////////////////////////////////////

    $('[data-toggle="popover_marker"]').popover({
        html: true,
        content: function(e) {
            return $('#popover-marker-content').html();
        }
    });

    $('[data-toggle="popover_share"]').popover({
        html: true,
        content: function(e) {
            return $('#popover-share-content').html();
        }
    });

    //////////////////////////////////////////////////////////////////////
    
    function memoryAddModel(){
        $('#memoryBooking').modal('show');
    }

    function memoryHandleClick(e){
        var latlng = e.latLng;
        map.setCursor("default");
        curOverlay.setContent(memory_content);
        curOverlay.setPosition(latlng);
    }

    function memoryCallAddress(result, status){
        if (status === daum.maps.services.Status.OK) {
            $('#memoryBooking__address')[0].value = result[0].address.address_name;
        }
    }

    function memoryMarkerClick(e){
        var latlng = e.latLng;
        var booking__hidden = null;

        memoryAddModel();
        booking__hidden = latlng.getLat() + ',' + latlng.getLng();
        $('#booking__hidden').attr("value", booking__hidden);

        daum.maps.event.removeListener(map, 'click', memoryMarkerClick);
        daum.maps.event.removeListener(map, 'mousemove', memoryHandleClick);
        geocoder.coord2Address(latlng.getLng(), latlng.getLat(), memoryCallAddress);

        map.setCursor(null);
        curOverlay.setVisible(false);
    }

    function memoryCancelClick(){
        daum.maps.event.removeListener(map, 'click', memoryMarkerClick);
        daum.maps.event.removeListener(map, 'mousemove', memoryHandleClick);
        daum.maps.event.removeListener(map, 'rightclick', memoryCancelClick);
        map.setCursor(null);
        curOverlay.setVisible(false);
    }
    
    $(document).on('click', '#memory_booking', function(){
        console.log("예약 추가를 클릭했다.");
        curOverlay.setVisible(true);
        daum.maps.event.addListener(map, 'click', memoryMarkerClick);
        daum.maps.event.addListener(map, 'rightclick', memoryCancelClick);
        daum.maps.event.addListener(map, 'mousemove', memoryHandleClick);
    });

    ////////////////////////////////////////////////////////////

})(window.daum, window.jQuery);
// 오제웅 End

// 장근열 Start
(function(daum, jQuery){
    // 마커를 클릭했을 때 해당 장소의 상세한 정보를 보여줄 커스텀 오버레이입니다
    var placeOverlay = new daum.maps.CustomOverlay({zIndex:1}),
        contentNode = document.createElement('div'), // 장소의 상세한 정보를 보여줄 커스텀 오버레이의 컨텐츠 엘리먼트입니다
        markers = [], // 마커를 담을 배열입니다
        currCategory = ''; // 현재 선택된 카테고리를 가지고 있을 변수입니다

    // 마커를 마우스 오버했을 때 해당 장소의 간략한 정보를 보여줄 커스텀 오버레이입니다
    var placeTitleOverlay = new daum.maps.CustomOverlay({zIndex:1}),
        contentTitleNode = document.createElement('div'); // 장소의 간략한 정보를 커스텀 오버레이의 컨텐츠 엘리먼트입니다

    // 커스텀 오버레이들의 컨텐츠 노드에 각각 css class를 추가합니다
    contentNode.className = 'placeinfo_wrap';
    contentTitleNode.className = 'placeinfo2_wrap';

    // 장소 검색 객체를 생성합니다
    // var ps = new daum.maps.services.Places(map);

    // 커스텀 오버레이들의 컨텐츠를 설정합니다
    placeOverlay.setContent(contentNode);
    placeTitleOverlay.setContent(contentTitleNode);

    // 커스텀 오버레이들의 컨텐츠 노드에 mousedown, touchstart 이벤트가 발생했을때
    // 지도 객체에 이벤트가 전달되지 않도록 이벤트 핸들러로 daum.maps.event.preventMap 메소드를 등록합니다
    addEventHandle(contentNode, 'mousedown', daum.maps.event.preventMap);
    addEventHandle(contentNode, 'touchstart', daum.maps.event.preventMap);
    addEventHandle(contentTitleNode, 'mousedown', daum.maps.event.preventMap);
    addEventHandle(contentTitleNode, 'touchstart', daum.maps.event.preventMap);

    // 엘리먼트에 이벤트 핸들러를 등록하는 함수입니다
    // IE에서는 attachEvent만 지원하고, addEventListener는 지원하지 않습니다
    // 그래서 아래와 같이 작성하였습니다
    function addEventHandle(target, type, callback) {
        if (target.addEventListener) {
            target.addEventListener(type, callback); // 이벤트를 발생시키고 콜백함수를 호출한다.
        } else {
            target.attachEvent('on' + type, callback); // 이벤트 앞에 on을 붙여 발생시키고 콜백함수를 호출한다.
        }
    }

    // 각 카테고리에 클릭 이벤트를 등록합니다
    addCategoryClickEvent();

    // 각 카테고리에 클릭 이벤트를 등록하는 함수입니다
    function addCategoryClickEvent() {
        var category = document.getElementById('category'), // category ID를 가진 엘리먼트를 category변수에 저장합니다
            children = category.children; // category ID를 가진 엘리먼트의 자식 요소를 children에 저장합니다

        for (var i=0; i<children.length; i++) {
            // 카테고리를 클릭하면 onClickCategory()함수가 호출됩니다
            children[i].onclick = onClickCategory;
        }
    }

    // 카테고리를 클릭했을 때 호출되는 함수입니다
    function onClickCategory() {
        var id = this.id,
            className = this.className;

        placeOverlay.setMap(null); // 상세 정보 커스텀 오버레이를 제거합니다
        placeTitleOverlay.setMap(null); // 간략 정보 커스텀 오버레이를 제거합니다

        if (className === 'on') {
            currCategory = '';
            changeCategoryClass();
            removeMarker();
        } else {
            currCategory = id; // 클릭한 카테고리의 ID를 생성합니다
            changeCategoryClass(this); // 클릭한 카테고리의 class 속성을 생성합니다
            searchCategory(); // 카테고리 검색을 요청한다.
        }
    }

    // 카테고리 검색을 요청하는 함수입니다
    function searchCategory() {
        if (!currCategory) {
            return;
        }
        // 커스텀 오버레이를 숨깁니다
        placeOverlay.setMap(null);
        placeTitleOverlay.setMap(null);

        // 지도에 표시되고 있는 마커를 제거합니다
        removeMarker();

        // 생성한 장소 검색 객체에서 categorySearch 메소드를 사용하여 카테고리 코드를 검색합니다
        // useMapBounds에 true값을 주어 지도의 영역이 자동으로 관련 값에 할당되도록 합니다
        ps.categorySearch(currCategory, placesSearchCB, {useMapBounds:true});
    }

    // 클릭된 카테고리에만 클릭된 스타일을 적용하는 함수입니다
    function changeCategoryClass(el) {
        var category = document.getElementById('category'),
            children = category.children,
            i;

        for ( i=0; i<children.length; i++ ) {
            children[i].className = '';
        }

        if (el) {
            el.className = 'on';
        }
    }

    // 장소검색이 완료됐을 때 호출되는 콜백함수입니다
    function placesSearchCB(data, status, pagination) {
        if (status === daum.maps.services.Status.OK) {
            // 정상적으로 검색이 완료됐으면 지도에 마커를 표출합니다
            displayPlaces(data);
        } else if (status === daum.maps.services.Status.ZERO_RESULT) {
            // 검색결과가 없을 때, 맵을 움직일 때마다 계속 알림창이 뜨는 번거로움이 생겨 alert메소드를 적용하지 않았습니다

        } else if (status === daum.maps.services.Status.ERROR) {
            // 에러로 인해 검색결과가 나오지 않은 경우 해야할 처리가 있다면 이곳에 작성해 주세요
            alert('오류로 인해 검색을 하지 못했습니다.');
        }
    }

    // 지도에 마커를 표출하는 함수입니다
    function displayPlaces(places) {
        // 몇번째 카테고리가 선택되어 있는지 얻어옵니다
        // 이 순서는 스프라이트 이미지에서의 위치를 계산하는데 사용됩니다
        var order = document.getElementById(currCategory).getAttribute('data-order');

        for ( var i=0; i<places.length; i++ ) {
                // 마커를 생성하고 지도에 표시합니다
                var marker = addMarker(new daum.maps.LatLng(places[i].y, places[i].x), order);

                // 마커에 이벤트를 등록하는 함수 만들고 즉시 호출하여 클로저를 만듭니다
                // 클로저를 만들어 주지 않으면 마지막 마커에만 이벤트가 등록됩니다
                (function(marker, place) {
                    // 마커와 검색결과 항목을 클릭 했을 때
                    // 장소의 상세한 정보를 표출하도록,
                    // 장소의 간단한 정보만 표시되는 커스텀 오버레이는 제거되도록
                    // 클릭 이벤트를 등록합니다.
                    daum.maps.event.addListener(marker, 'click', function() {
                        var level = map.getLevel();

                        displayPlaceInfo(place);
                        displayPlaceTitleOut(place);

                        // 지도 레벨 5를 넘은 상태에서 마커 클릭 시
                        // 클릭한 마커를 중심좌표로 삼아 지도 레벨 5로 설정해 준다.
                        if(level > 5) {
                            map.setLevel(5);
                            map.setCenter(new daum.maps.LatLng(place.y, place.x));
                        }
                        // 클릭한 마커에 마우스 아웃했다가 마우스 오버했을 때
                        // 다시 뜨는 간단한 정보의 커스텀 오버레이를 제거하도록
                        // 마우스 오버 이벤트를 등록합니다.
                        daum.maps.event.removeListener(map, 'mouseover', function() {
                            displayPlaceTitle(place);
                        });
                    });
                    // 마우스 오버했을 때
                    // 장소의 간단한 정보를 표출하도록 마우스 오버 이벤트를 등록합니다
                    daum.maps.event.addListener(marker,'mouseover',function() {
                        displayPlaceTitle(place);
                    });
                    // 마우스 아웃했을 떄
                    // 장소의 간단한 정보를 제거하도록 마우스 아웃 이벤트를 등록합니다
                    daum.maps.event.addListener(marker,'mouseout',function() {
                        displayPlaceTitleOut(place);
                    });
                })(marker, places[i]);

                (function(map,place){
                    // 마커가 아닌 지도를 클릭했을 때
                    // 상세정보를 표시하는 커스텀 오버레이를 제거하도록 클릭 이벤트를 등록합니다
                    daum.maps.event.addListener(map, 'click', function(){
                        displayPlaceInfoOut(place);
                    });
                })(map, places[i]);
        }
    }

    // 마커를 생성하고 지도 위에 마커를 표시하는 함수입니다
    function addMarker(position, order) {
        var imageSrc = 'http://t1.daumcdn.net/localimg/localimages/07/mapapidoc/places_category.png', // 마커 이미지 url, 스프라이트 이미지를 씁니다
            imageSize = new daum.maps.Size(27, 28),  // 마커 이미지의 크기
            imgOptions =  {
                spriteSize : new daum.maps.Size(72, 208), // 스프라이트 이미지의 크기
                spriteOrigin : new daum.maps.Point(46, (order*36)), // 스프라이트 이미지 중 사용할 영역의 좌상단 좌표
                offset: new daum.maps.Point(11, 28) // 마커 좌표에 일치시킬 이미지 내에서의 좌표
            },
            markerImage = new daum.maps.MarkerImage(imageSrc, imageSize, imgOptions),
                marker = new daum.maps.Marker({
                position: position, // 마커의 위치
                image: markerImage
            });

        // var imageSrc = 'tpin4.png', // 마커 이미지 url
        //     imageSize = new daum.maps.Size(27, 28),  // 마커 이미지의 크기
        //     imgOptions =  {
        //         offset: new daum.maps.Point(11, 28) // 마커 좌표에 일치시킬 이미지 내에서의 좌표
        //     },
        //     markerImage = new daum.maps.MarkerImage(imageSrc, imageSize, imgOptions),
        //         marker = new daum.maps.Marker({
        //         position: position, // 마커의 위치
        //         image: markerImage
        //     });

        marker.setMap(map); // 지도 위에 마커를 표출합니다
        markers.push(marker);  // 배열에 생성된 마커를 추가합니다

        return marker;
    }

    // 지도 위에 표시되고 있는 마커를 모두 제거합니다
    function removeMarker() {
        for ( var i = 0; i < markers.length; i++ ) {
            markers[i].setMap(null);
        }
        markers = [];
    }

    // 클릭한 마커에 대한 장소의 상세정보를 커스텀 오버레이로 표시하는 함수입니다
    function displayPlaceInfo (place) {
        var content = '<div class="placeinfo">' +
                        '   <p class="title" target="_blank" title="' + place.place_name + '">' + place.place_name + '</p>';

        if (place.road_address_name) {
            content += '    <span title="' + place.road_address_name + '">' + place.road_address_name + '</span>' +
                        '  <span class="jibun" title="' + place.address_name + '">(지번 : ' + place.address_name + ')</span>';
        }  else {
            content += '    <span title="' + place.address_name + '">' + place.address_name + '</span>';
        }

        content += '    <span class="tel">' + place.phone + '</span>' +
                    '</div>' +
                    '<div class="after"></div>';
        // 상세 정보 커스텀 오버레이의 컨텐츠 노드에 컨텐츠를 출력해준다.
        contentNode.innerHTML = content;

        placeOverlay.setPosition(new daum.maps.LatLng(place.y, place.x));
        placeOverlay.setMap(map);
    }

    // 지도를 클릭하면 클릭한 마커에 대한 상세정보를 표시하는 커스텀 오버레이를 제거하는 함수입니다
    function displayPlaceInfoOut (place) {
        placeOverlay.setMap(null);
    }

    // 마우스 오버한 마커에 대한 장소의 간략한 정보를 커스텀 오버레이로 표시하는 함수입니다
    function displayPlaceTitle (place) {
        var content = '<p class="title2" target="_blank" title="' + place.place_name + '">' + place.place_name + '</p>';

        // 간략한 정보 커스텀 오버레이의 컨텐츠 노드에 컨텐츠를 출력해준다.
        contentTitleNode.innerHTML = content;

        placeTitleOverlay.setPosition(new daum.maps.LatLng(place.y, place.x));
        placeTitleOverlay.setMap(map);
    }

    // 마우스 오버한 마커에 마우스 아웃 시
    // 간략한 정보의 커스텀 오버레이를 제거하는 함수입니다
    function displayPlaceTitleOut (place) {
        placeTitleOverlay.setMap(null);
    }

})(window.daum, window.jQuery);
// 장근열 End

// 박기철 Start
(function(daum, jQuery){
// 주소-좌표 변환 객체를 생성합니다
var geocoder = new daum.maps.services.Geocoder();

function successCallback(position) {
        var lat = position.coords.latitude, // 위도
        lon = position.coords.longitude; // 경도

        var locPosition = new daum.maps.LatLng(lat, lon); // 마커가 표시될 위치를 geolocation으로 얻어온 좌표로 생성합니다

        // 지도의 중심좌표를 얻어옵니다
        var latlng = map.getCenter();

        // 현재 지도의 레벨을 얻어옵니다
        var level = map.getLevel();

        // 지도의 중심좌표를 내 현재위치로 변경합니다
        map.setCenter(locPosition);

        // 지도의 확대 레벨을 낮춥니다
        map.setLevel(level -13,  {
            // animate: {
            //     duration: 600
            // }
        });
}

function errorCallback(error) {
    alert("Error: " + error.message);
}


document.getElementById("getLocation").onclick = function () {
    navigator.geolocation.getCurrentPosition(successCallback, errorCallback);
};

})(window.daum, window.jQuery);





// 마커를 담을 배열입니다
var markers = [];

// 검색 결과 목록이나 마커를 클릭했을 때 장소명을 표출할 인포윈도우를 생성합니다
var infowindow = new daum.maps.InfoWindow({zIndex:1});

// 키워드로 장소를 검색합니다
searchPlaces();

// 키워드 검색을 요청하는 함수입니다
function searchPlaces() {

    var keyword = document.getElementById('keyword').value;

    // if (!keyword.replace(/^\s+|\s+$/g, '')) {
    //     alert('키워드를 입력해주세요!');
    //     return false;
    // }

    // 장소검색 객체를 통해 키워드로 장소검색을 요청합니다
    ps.keywordSearch(keyword, placesSearchCB);
}

// 장소검색이 완료됐을 때 호출되는 콜백함수 입니다
function placesSearchCB(data, status, pagination) {
    if (status === daum.maps.services.Status.OK) {

        // 정상적으로 검색이 완료됐으면
        // 검색 목록과 마커를 표출합니다
        displayPlaces(data);

        // 페이지 번호를 표출합니다
        displayPagination(pagination);

    } else if (status === daum.maps.services.Status.ZERO_RESULT) {
        alert('검색 결과가 존재하지 않습니다.');
        return;

    } else if (status === daum.maps.services.Status.ERROR) {
        alert('검색 결과 중 오류가 발생했습니다.');
        return;
    }
}

// 검색 결과 목록과 마커를 표출하는 함수입니다
function displayPlaces(places) {

    var listEl = document.getElementById('placesList'),
    menuEl = document.getElementById('menu_wrap'),
    fragment = document.createDocumentFragment(), // 노드 객체의 모든 프로퍼티와 메소드를 사용하여 가상의 노드 객체를 만듭니다
    bounds = new daum.maps.LatLngBounds(), // WGS84 좌표계에서 사각영역 정보를 표현하는 객체를 생성합니다 인자를 주지 않으면 빈 영역을 생성합니다
    listStr = '';

    // 검색 결과 목록에 추가된 항목들을 제거합니다
    removeAllChildNods(listEl);

    // 지도에 표시되고 있는 마커를 제거합니다
    removeMarker();

    for ( var i=0; i<places.length; i++ ) {

        // 마커를 생성하고 지도에 표시합니다
        var placePosition = new daum.maps.LatLng(places[i].y, places[i].x),
            marker = addMarker(placePosition, i),
            itemEl = getListItem(i, places[i]); // 검색 결과 항목 Element를 생성합니다

        // 검색된 장소 위치를 기준으로 지도 범위를 재설정하기위해
        // LatLngBounds 객체에 좌표를 추가합니다
        bounds.extend(placePosition);

        // 마커와 검색결과 항목에 mouseover 했을때
        // 해당 장소에 인포윈도우에 장소명을 표시합니다
        // mouseout 했을 때는 인포윈도우를 닫습니다
        (function(marker, title) {
            daum.maps.event.addListener(marker, 'mouseover', function() {
                displayInfowindow(marker, title);
            });

            daum.maps.event.addListener(marker, 'mouseout', function() {
                infowindow.close();
            });

            itemEl.onmouseover =  function () {
                displayInfowindow(marker, title);
            };

            itemEl.onmouseout =  function () {
                infowindow.close();
            };
        })(marker, places[i].place_name);

        fragment.appendChild(itemEl);
    }

    // 검색결과 항목들을 검색결과 목록 Elemnet에 추가합니다
    listEl.appendChild(fragment);
    menuEl.scrollTop = 0;

    // 검색된 장소 위치를 기준으로 지도 범위를 재설정합니다
    map.setBounds(bounds);
}

// 검색결과 항목을 Element로 반환하는 함수입니다
function getListItem(index, places) {

    var el = document.createElement('li'),
    itemStr = '<span class="markerbg marker_' + (index+1) + '"></span>' +
                '<div class="info">' +
                '   <h5>' + places.place_name + '</h5>';

    if (places.road_address_name) {
        itemStr += '    <span>' + places.road_address_name + '</span>' +
                    '   <span class="jibun gray">' +  places.address_name  + '</span>';
    } else {
        itemStr += '    <span>' +  places.address_name  + '</span>';
    }

      itemStr += '  <span class="tel">' + places.phone  + '</span>' +
                '</div>';

    el.innerHTML = itemStr;
    el.className = 'item';

    return el;
}

// 마커를 생성하고 지도 위에 마커를 표시하는 함수입니다
function addMarker(position, idx, title) {
    var imageSrc = 'https://t1.daumcdn.net/localimg/localimages/07/mapapidoc/marker_number_blue.png', // 마커 이미지 url, 스프라이트 이미지를 씁니다
        imageSize = new daum.maps.Size(36, 37),  // 마커 이미지의 크기
        imgOptions =  {
            spriteSize : new daum.maps.Size(36, 691), // 스프라이트 이미지의 크기
            spriteOrigin : new daum.maps.Point(0, (idx*46)+10), // 스프라이트 이미지 중 사용할 영역의 좌상단 좌표
            offset: new daum.maps.Point(13, 37) // 마커 좌표에 일치시킬 이미지 내에서의 좌표
        },
        markerImage = new daum.maps.MarkerImage(imageSrc, imageSize, imgOptions),
            marker = new daum.maps.Marker({
            position: position, // 마커의 위치
            image: markerImage
        });

    marker.setMap(map); // 지도 위에 마커를 표출합니다
    markers.push(marker);  // 배열에 생성된 마커를 추가합니다

    return marker;
}

// 지도 위에 표시되고 있는 마커를 모두 제거합니다
function removeMarker() {
    for ( var i = 0; i < markers.length; i++ ) {
        markers[i].setMap(null);
    }
    markers = [];
}

// 검색결과 목록 하단에 페이지번호를 표시는 함수입니다
function displayPagination(pagination) {
    var paginationEl = document.getElementById('pagination'),
        fragment = document.createDocumentFragment(),
        i;

    // 기존에 추가된 페이지번호를 삭제합니다
    while (paginationEl.hasChildNodes()) {
        paginationEl.removeChild (paginationEl.lastChild);
    }

    for (i=1; i<=pagination.last; i++) {
        var el = document.createElement('a');
        el.href = "#";
        el.innerHTML = i;

        if (i===pagination.current) {
            el.className = 'on';
        } else {
            el.onclick = (function(i) {
                return function() {
                    pagination.gotoPage(i);
                }
            })(i);
        }

        fragment.appendChild(el);
    }
    paginationEl.appendChild(fragment);
}

// 검색결과 목록 또는 마커를 클릭했을 때 호출되는 함수입니다
// 인포윈도우에 장소명을 표시합니다
function displayInfowindow(marker, title) {
    var content = '<div style="padding:5px;z-index:1;">' + title + '</div>';

    infowindow.setContent(content);
    infowindow.open(map, marker);
}

 // 검색결과 목록의 자식 Element를 제거하는 함수입니다
function removeAllChildNods(el) {
    while (el.hasChildNodes()) {
        el.removeChild (el.lastChild);
    }
}

$(document).ready(function(){
  $(".main__btn__search").click(function(){
    $("#menu_wrap").toggle();
    removeMarker();
  });
});

$(document).ready(function(){
  $(".main__btn__search").click(function(){
    $("#category_wrap").toggle();
  });
});

$(document).ready(function(){
    $(".travel").click(function(){
    $(".break").toggle();
    $(this).hide();
  });
    $(".break").click(function(){
    $(".travel").toggle();
    $(this).hide();
  });
});
// 박기철 End