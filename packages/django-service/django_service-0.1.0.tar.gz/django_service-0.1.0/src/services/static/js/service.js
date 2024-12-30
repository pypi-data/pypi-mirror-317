$(document).ready(function() {
    'use strict';
    /*-----------------------------------------------------------------------------------*/
    /*	LIGHTGALLERY
    /*-----------------------------------------------------------------------------------*/
    var $lgContainer = document.getElementById('inline-gallery-container');
    var lg = lightGallery($lgContainer, {
      container: $lgContainer,
      dynamic: true,
      hash: false,
      closable: false,
      showMaximizeIcon: true,
      download: false,
      slideShowAutoplay: true,
      slideDelay: 400,
      mode: 'lg-fade',
      appendSubHtmlTo: ".lg-item",
      plugins: [lgZoom, lgThumbnail, lgAutoplay],
      dynamicEl: $dynamicEl
    });

    setTimeout(() => {
      lg.openGallery();
    }, 500);
});