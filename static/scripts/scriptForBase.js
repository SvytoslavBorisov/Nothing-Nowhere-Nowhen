
$('#navigator_div4').css('visibility', 'visible');

/* КРАСОТА ДЛЯ ТЕЛЕФОНА */

if ( $( window ).width() > 980 | !(/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent))) {
    document.getElementById('top_menuDiv').style.width = String(document.documentElement.clientWidth) + 'px';
    document.getElementById('all_navigator_div').style.width = String(document.documentElement.clientWidth - 400) + 'px';
};

$('#navigator_div3').on('click', function() {
  if (document.location.pathname == '/') {
     $('html, body').animate({scrollTop:$('#div_rating').offset().top - 75 + "px"},{duration:1E3});
  }
  else {
     document.location.href = '/rating';
  };
});

$('#navigator_div1').on('click', function() {
  if (document.location.pathname == '/') {
     $('html, body').animate({scrollTop:$('#div_about_site').offset().top - 75 + "px"},{duration:1E3});
  }
  else {
     document.location.href = '/about_site';
  };
});