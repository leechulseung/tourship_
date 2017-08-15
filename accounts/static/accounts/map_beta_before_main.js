// $("html").niceScroll();
(function(daum, jQuery){
  var $ = jQuery;
  var mapContainer = $('#map')[0];
  var mapOptions = {
  	center: new daum.maps.LatLng(37.57484288719911, 126.93107087733638),
  	level: 12
  };
  
  var map = new daum.maps.Map(mapContainer, mapOptions);
  
  var positions = [
      {
          title: '서울특별시청', 
          latlng: new daum.maps.LatLng(37.5666103, 126.9783882)
      },
      {
          title: '인천광역시청', 
          latlng: new daum.maps.LatLng(37.4560537, 126.7051511)
      },
      {
          title: '인제군청', 
          latlng: new daum.maps.LatLng(38.0697320, 128.1703520)
      },
      {
          title: '원주시청',
          latlng: new daum.maps.LatLng(37.3419480, 127.9199210)
      },
      {
          title: '대전광역시청',
          latlng: new daum.maps.LatLng(36.3504669, 127.3846583)
      },
      {
          title: '강화군청',
          latlng: new daum.maps.LatLng(37.7464980, 126.4880520)
      },
      {
          title: '대구광역시청',
          latlng: new daum.maps.LatLng(35.8713900, 128.6017630)
      },
      {
          title: '세종특별자치시청',
          latlng: new daum.maps.LatLng(36.4800721, 127.2890845)
      },
      {
          title: '제천시청',
          latlng: new daum.maps.LatLng(37.1326460, 128.1910370)
      },
      {
          title: '51사단',
          latlng: new daum.maps.LatLng(37.2485000, 126.9248000)
      }
  ];
  
  var imageSrc = "assets/img/pinkPin.png"
  
  for (var i = 0; i < positions.length; i ++) {
      var imageSize = new daum.maps.Size(50, 50); 
      var markerImage = new daum.maps.MarkerImage(imageSrc, imageSize); 
      
      var marker = new daum.maps.Marker({
          map: map,
          position: positions[i].latlng,
          title : positions[i].title,
          image : markerImage
      });
  }
})(window.daum, window.jQuery);