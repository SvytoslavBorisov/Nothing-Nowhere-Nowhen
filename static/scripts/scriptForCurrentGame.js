

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

function oninput_forgame() {
    alert(event.data);
    if (event.text.length > 1)
        event.preventDefault();
}