window.onresize = function () {
    $('#content').height('100%');
    $('.header').height(38);
    if (/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)) {
    var x = $( '#content' ).height()+ 420 - Number($( '#content' ).css( "margin-bottom" ).substring(0, $( '#content' ).css( "margin-bottom" ).length - 2)) - Number($( '#content' ).css( "margin-top" ).substring(0, $( '#content' ).css( "margin-top" ).length - 2));
    if ( $( window ).height() > x + 130) {
        document.getElementById('footer').style.marginTop = String( Number($( document ).height() - x - 130)) + 'px';
    }
    else {
        document.getElementById('footer').style.marginTop = String( 30 ) + 'px';
    };

  } else {
    var x = $( '#content' ).height() + 202 - Number($( '#content' ).css( "margin-bottom" ).substring(0, $( '#content' ).css( "margin-bottom" ).length - 2)) - Number($( '#content' ).css( "margin-top" ).substring(0, $( '#content' ).css( "margin-top" ).length - 2));
    if ( $( window ).height() > x + 130) {
        document.getElementById('footer').style.marginTop = String( Number($( document ).height() - x - 130)) + 'px';
    }
    else {
        document.getElementById('footer').style.marginTop = String( 30 ) + 'px';
    };
    $( '#top_menuDiv' ).width(document.documentElement.clientWidth);
        $( '#all_navigator_div' ).width(document.documentElement.clientWidth - 400);
};
$('#navigator_div4').css('visibility', 'visible');
};

$( document ).ready(function () {

    $('#content').height('100%');
    $('.header').height(38);
    if (/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)) {
        alert($( window ).height());
        var x = $( '#content' ).height() + 420 - Number($( '#content' ).css( "margin-bottom" ).substring(0, $( '#content' ).css( "margin-bottom" ).length - 2)) - Number($( '#content' ).css( "margin-top" ).substring(0, $( '#content' ).css( "margin-top" ).length - 2));
        alert(x);
        if ( $( window ).height() > x + 125) {
            document.getElementById('footer').style.marginTop = String( Number(document.documentElement.clientHeight - x - 125)) + 'px';
        }
        else {
            document.getElementById('footer').style.marginTop = String( 30 ) + 'px';
        };
    }
    else {
        var x = $( '#content' ).height() + 202 - Number($( '#content' ).css( "margin-bottom" ).substring(0, $( '#content' ).css( "margin-bottom" ).length - 2)) - Number($( '#content' ).css( "margin-top" ).substring(0, $( '#content' ).css( "margin-top" ).length - 2)) - Number($( '#content' ).css( "border-width" ).substring(0, $( '#content' ).css( "border-width" ).length - 2));
        if ( $( window ).height() > x + 130) {
            document.getElementById('footer').style.marginTop = String( Number(document.documentElement.clientHeight - x - 125)) + 'px';
            }
        else {
            document.getElementById('footer').style.marginTop = String( 30 ) + 'px';
            };
        $( '#top_menuDiv' ).width(document.documentElement.clientWidth);
        $( '#all_navigator_div' ).width(document.documentElement.clientWidth - 400);
    };
    $('#navigator_div4').css('visibility', 'visible');}
);

if (/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)) {
    var x = $( '#content' ).height() + 408 - Number($( '#content' ).css( "margin-bottom" ).substring(0, $( '#content' ).css( "margin-bottom" ).length - 2)) - Number($( '#content' ).css( "margin-top" ).substring(0, $( '#content' ).css( "margin-top" ).length - 2));
    if ( $( window ).height() > x + 125) {
        document.getElementById('footer').style.marginTop = String( Number($( document ).height() - x - 125)) + 'px';
        }
    else {
        document.getElementById('footer').style.marginTop = String( 30 ) + 'px';
        };
}
else {
    var x = $( '#content' ).height() + 202 - Number($( '#content' ).css( "margin-bottom" ).substring(0, $( '#content' ).css( "margin-bottom" ).length - 2)) - Number($( '#content' ).css( "margin-top" ).substring(0, $( '#content' ).css( "margin-top" ).length - 2)) - Number($( '#content' ).css( "border-width" ).substring(0, $( '#content' ).css( "border-width" ).length - 2));
    if ( $( window ).height() > x + 130) {
        document.getElementById('footer').style.marginTop = String( Number(document.documentElement.clientHeight - x - 125)) + 'px';
        }
    else {
        document.getElementById('footer').style.marginTop = String( 30 ) + 'px';
        };
};