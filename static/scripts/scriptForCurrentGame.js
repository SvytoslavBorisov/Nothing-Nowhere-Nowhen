function changeRadioBox(id_) {
    chbox = document.getElementById(id_);
        if (chbox.checked) {
            document.getElementById("b_answer_question").disabled = false;
            document.getElementById("b_answer_question").style.background = 'linear-gradient(to top, rgb(200, 50, 50), rgb(255, 0, 0))';
            document.getElementById("b_answer_question").style.boxShadow = '0 3px 0 rgb(190, 0, 0)';
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

function oninput_forgame() {
    if (event.text.length > 1)
        event.preventDefault();
};

if (!( $( window ).width() > 980 | !(/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)))) {
    $('#p_vs').css('visibility', 'hidden');
    $('#p_vs').height(0);
};

$("#question_image").click(function(){	// Событие клика на маленькое изображение
    var img = $(this);	// Получаем изображение, на которое кликнули
    var src = img.attr('src'); // Достаем из этого изображения путь до картинки
    $("body").append("<div class='popup'>"+ //Добавляем в тело документа разметку всплывающего окна
                     "<div class='popup_bg'></div>"+ // Блок, который будет служить фоном затемненным
                     "<img src='"+src+"' class='popup_img' />"+ // Само увеличенное фото
                     "</div>");
    $(".popup").fadeIn(800); // Медленно выводим изображение
    $(".popup_bg").click(function(){	// Событие клика на затемненный фон
        $(".popup").fadeOut(800);	// Медленно убираем всплывающее окно
        setTimeout(function() {	// Выставляем таймер
          $(".popup").remove(); // Удаляем разметку всплывающего окна
        }, 800);
    });
});

$("#question_image_map").click(function(){	// Событие клика на маленькое изображение
    var img = $(this);	// Получаем изображение, на которое кликнули
    var src = img.attr('src'); // Достаем из этого изображения путь до картинки
    $("body").append("<div class='popup'>"+ //Добавляем в тело документа разметку всплывающего окна
                     "<div class='popup_bg'></div>"+ // Блок, который будет служить фоном затемненным
                     "<img src='"+src+"' class='popup_img' />"+ // Само увеличенное фото
                     "</div>");
    $(".popup").fadeIn(800); // Медленно выводим изображение
    $(".popup_bg").click(function(){	// Событие клика на затемненный фон
        $(".popup").fadeOut(800);	// Медленно убираем всплывающее окно
        setTimeout(function() {	// Выставляем таймер
          $(".popup").remove(); // Удаляем разметку всплывающего окна
        }, 800);
    });
});
