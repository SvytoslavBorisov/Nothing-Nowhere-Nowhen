window.onresize = function () {
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
    document.getElementById('top_menuDiv').style.width = String(document.documentElement.clientWidth) + 'px';
    document.getElementById('all_navigator_div').style.width = String(document.documentElement.clientWidth - 400) + 'px';
};
};

if (/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)) {
    let div = document.createElement('div');
    div.id = 'footer';
    div.innerHTML = `<div id="logo_and_name">
                         <img src="/static/img/icons/footer_logo.png" alt="" height="100px" width="200px" id="footer_logo">
                         <p id="p_name"> Ничто? Нигде? Никогда?</p>
                     </div>
                     <div id="links_and_foot_p">
                         <div id="div_links">
                             <p id="footer_p_">Ничто? Нигде? Никогда? - в соцсетях</p>
                             <a id="vk_a_join" target="_blank" href="https://vk.com/nothingnowherenowhen">
                                 <img src="/static/img/icons/vk_link.png" alt="" id="vk_logo">
                             </a>
                         </div>
                         <p id="footer_p">Онлайн Викторина © 2020 NothingNowhereNowhen.com</p>
                     </div>`
    document.getElementById('main').after(div);
    var x = $( '#content' ).height() + 420 - Number($( '#content' ).css( "margin-bottom" ).substring(0, $( '#content' ).css( "margin-bottom" ).length - 2)) - Number($( '#content' ).css( "margin-top" ).substring(0, $( '#content' ).css( "margin-top" ).length - 2));
    if ( $( window ).height() > x + 130) {
        document.getElementById('footer').style.marginTop = String( Number($( document ).height() - x - 130)) + 'px';
    }
    else {
        document.getElementById('footer').style.marginTop = String( 30 ) + 'px';
    };

  } else {
    let div = document.createElement('div');
    div.id = 'footer';
    div.innerHTML = `<div id="logo_and_name">
                         <img src="/static/img/icons/footer_logo.png" alt="" height="100px" width="200px" id="footer_logo">
                         <p id="p_name"> Ничто? Нигде? Никогда?</p>
                     </div>
                     <div id="links_and_foot_p">
                         <div id="div_links">
                             <p id="footer_p_">Ничто? Нигде? Никогда? - в соцсетях</p>
                             <a id="vk_a_join" target="_blank" href="https://vk.com/nothingnowherenowhen">
                                 <img src="/static/img/icons/vk_link.png" alt="" id="vk_logo">
                             </a>
                         </div>
                         <p id="footer_p">Онлайн Викторина © 2020 NothingNowhereNowhen.com</p>
                     </div>`
    document.getElementById('main').after(div);
    var x = $( '#content' ).height() + 202 - Number($( '#content' ).css( "margin-bottom" ).substring(0, $( '#content' ).css( "margin-bottom" ).length - 2)) - Number($( '#content' ).css( "margin-top" ).substring(0, $( '#content' ).css( "margin-top" ).length - 2));
    if ( $( window ).height() > x + 130) {
        document.getElementById('footer').style.marginTop = String( Number($( document ).height() - x - 130)) + 'px';
    }
    else {
        document.getElementById('footer').style.marginTop = String( 30 ) + 'px';
    };
    document.getElementById('top_menuDiv').style.width = String(document.documentElement.clientWidth) + 'px';
    document.getElementById('all_navigator_div').style.width = String(document.documentElement.clientWidth - 400) + 'px';
};
