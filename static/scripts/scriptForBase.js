window.onresize = function () {
    document.getElementById('top_menuDiv').style.width = String(document.documentElement.clientWidth) + 'px';
    document.getElementById('all_navigator_div').style.width = String(document.documentElement.clientWidth - 400) + 'px';
    var x = $( '#content' ).height() + 100 - Number($( '#content' ).css( "margin-bottom" ).substring(0, $( '#content' ).css( "margin-bottom" ).length - 2)) - Number($( '#content' ).css( "margin-top" ).substring(0, $( '#content' ).css( "margin-top" ).length - 2));
    if ( $( window ).height() > x + 125) {
        document.getElementById('footer').style.marginTop = String( $( document ).height() - x - 125) + 'px';
    }
    else {
        document.getElementById('footer').style.marginTop = String( 15 ) + 'px';
    };
    $( '#footer' ).show();
};

document.getElementById('top_menuDiv').style.width = String(document.documentElement.clientWidth) + 'px';
document.getElementById('all_navigator_div').style.width = String(document.documentElement.clientWidth - 400) + 'px';

$('#footer').hide();

$( document ).ready(function(){
    var x = $( '#content' ).height() + 100 - Number($( '#content' ).css( "margin-bottom" ).substring(0, $( '#content' ).css( "margin-bottom" ).length - 2)) - Number($( '#content' ).css( "margin-top" ).substring(0, $( '#content' ).css( "margin-top" ).length - 2));
    if ( $( window ).height() > x + 125) {
        document.getElementById('footer').style.marginTop = String( $( document ).height() - x - 125) + 'px';
    }
    else {
        document.getElementById('footer').style.marginTop = String( 15 ) + 'px';
    };
    $( '#footer' ).show();
});