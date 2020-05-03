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
    document.getElementById('checkbox1').style.left = String(document.getElementById('div_questions_answer1').getBoundingClientRect().x) + 'px';
    document.getElementById('checkbox2').style.left = String(document.getElementById('div_questions_answer2').getBoundingClientRect().x) + 'px';
    document.getElementById('checkbox3').style.left = String(document.getElementById('div_questions_answer3').getBoundingClientRect().x) + 'px';
    document.getElementById('checkbox4').style.left = String(document.getElementById('div_questions_answer4').getBoundingClientRect().x) + 'px';
};};

function changeRadioBox(id_) {
    chbox = document.getElementById(id_);
        if (chbox.checked) {
            if (id_ == 'checkbox1') {
                document.getElementById('div_questions_answer1').style.background = 'linear-gradient(#4c4, #8f8 50%, #4c4)';
                document.getElementById('div_questions_answer1').style.color = 'white';
                document.getElementById('div_questions_answer2').style.color = 'rgb(60, 60, 60)';
                document.getElementById('div_questions_answer3').style.color = 'rgb(60, 60, 60)';
                document.getElementById('div_questions_answer4').style.color = 'rgb(60, 60, 60)';
                document.getElementById('div_questions_answer2').style.background = 'rgb(180, 180, 180)';
                document.getElementById('div_questions_answer3').style.background = 'rgb(180, 180, 180)';
                document.getElementById('div_questions_answer4').style.background = 'rgb(180, 180, 180)';
             };
            if (id_ == 'checkbox2') {
                document.getElementById('div_questions_answer2').style.background = 'linear-gradient(#4c4, #8f8 50%, #4c4)';
                document.getElementById('div_questions_answer2').style.color = 'white';
                document.getElementById('div_questions_answer1').style.color = 'rgb(60, 60, 60)';
                document.getElementById('div_questions_answer3').style.color = 'rgb(60, 60, 60)';
                document.getElementById('div_questions_answer4').style.color = 'rgb(60, 60, 60)';
                document.getElementById('div_questions_answer1').style.background = 'rgb(200, 200, 200)';
                document.getElementById('div_questions_answer3').style.background = 'rgb(200, 200, 200)';
                document.getElementById('div_questions_answer4').style.background = 'rgb(200, 200, 200)';
             };
            if (id_ == 'checkbox3') {
                document.getElementById('div_questions_answer3').style.background = 'linear-gradient(#4c4, #8f8 50%, #4c4)';
                document.getElementById('div_questions_answer3').style.color = 'white';
                document.getElementById('div_questions_answer2').style.color = 'rgb(60, 60, 60)';
                document.getElementById('div_questions_answer1').style.color = 'rgb(60, 60, 60)';
                document.getElementById('div_questions_answer4').style.color = 'rgb(60, 60, 60)';
                document.getElementById('div_questions_answer2').style.background = 'rgb(200, 200, 200)';
                document.getElementById('div_questions_answer1').style.background = 'rgb(200, 200, 200)';
                document.getElementById('div_questions_answer4').style.background = 'rgb(200, 200, 200)';
             };
            if (id_ == 'checkbox4') {
                document.getElementById('div_questions_answer4').style.background = 'linear-gradient(#4c4, #8f8 50%, #4c4)';
                document.getElementById('div_questions_answer4').style.color = 'white';
                document.getElementById('div_questions_answer2').style.color = 'rgb(60, 60, 60)';
                document.getElementById('div_questions_answer3').style.color = 'rgb(60, 60, 60)';
                document.getElementById('div_questions_answer1').style.color = 'rgb(60, 60, 60)';
                document.getElementById('div_questions_answer2').style.background = 'rgb(200, 200, 200)';
                document.getElementById('div_questions_answer3').style.background = 'rgb(200, 200, 200)';
                document.getElementById('div_questions_answer1').style.background = 'rgb(200, 200, 200)';
             };
        }
        else {
            if (id_ == 'checkbox1') { document.getElementById('div_questions_answer1').style.background = 'rgb(200, 200, 200)'; };
            if (id_ == 'checkbox2') { document.getElementById('div_questions_answer2').style.background = 'rgb(200, 200, 200)'; };
            if (id_ == 'checkbox3') { document.getElementById('div_questions_answer3').style.background = 'rgb(200, 200, 200)'; };
            if (id_ == 'checkbox4') { document.getElementById('div_questions_answer4').style.background = 'rgb(200, 200, 200)'; };
        }
};
