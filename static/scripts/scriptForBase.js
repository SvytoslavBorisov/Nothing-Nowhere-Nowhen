
$('#navigator_div4').css('visibility', 'visible');

/* КРАСОТА ДЛЯ ТЕЛЕФОНА */

if ( $( window ).width() > 980 | !(/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent))) {
    document.getElementById('top_menuDiv').style.width = String(document.documentElement.clientWidth) + 'px';
    document.getElementById('all_navigator_div').style.width = String(document.documentElement.clientWidth - 400) + 'px';
};
