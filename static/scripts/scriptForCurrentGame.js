window.onresize = function () {
    document.getElementById('top_menuDiv').style.width = String(document.documentElement.clientWidth) + 'px';
    document.getElementById('all_navigator_div').style.width = String(document.documentElement.clientWidth - 400) + 'px';
    document.getElementById('checkbox1').style.left = String(document.getElementById('div_questions_answer1').getBoundingClientRect().x) + 'px';
    document.getElementById('checkbox2').style.left = String(document.getElementById('div_questions_answer2').getBoundingClientRect().x) + 'px';
    document.getElementById('checkbox3').style.left = String(document.getElementById('div_questions_answer3').getBoundingClientRect().x) + 'px';
    document.getElementById('checkbox4').style.left = String(document.getElementById('div_questions_answer4').getBoundingClientRect().x) + 'px';
};

document.getElementById('top_menuDiv').style.width = String(document.documentElement.clientWidth) + 'px';
document.getElementById('all_navigator_div').style.width = String(document.documentElement.clientWidth - 400) + 'px';
document.getElementById('checkbox1').style.left = String(document.getElementById('div_questions_answer1').getBoundingClientRect().x) + 'px';
document.getElementById('checkbox2').style.left = String(document.getElementById('div_questions_answer2').getBoundingClientRect().x) + 'px';
document.getElementById('checkbox3').style.left = String(document.getElementById('div_questions_answer3').getBoundingClientRect().x) + 'px';
document.getElementById('checkbox4').style.left = String(document.getElementById('div_questions_answer4').getBoundingClientRect().x) + 'px';
document.getElementById('checkbox1').style.width = String(document.getElementById('div_questions_answer1').style.width) + 'px';
document.getElementById('checkbox2').style.width = String(document.getElementById('div_questions_answer2').style.width) + 'px';
document.getElementById('checkbox3').style.width = String(document.getElementById('div_questions_answer3').style.width) + 'px';
document.getElementById('checkbox4').style.width = String(document.getElementById('div_questions_answer4').style.width) + 'px';


function changeRadioBox(id_) {
    chbox = document.getElementById(id_);
        if (chbox.checked) {
            if (id_ == 'checkbox1') {
                document.getElementById('div_questions_answer1').style.background = 'linear-gradient(to top, #fefc0a, rgb(247, 150, 62))';
                document.getElementById('div_questions_answer1').style.color = 'white';
                document.getElementById('div_questions_answer2').style.color = 'rgb(60, 60, 60)';
                document.getElementById('div_questions_answer3').style.color = 'rgb(60, 60, 60)';
                document.getElementById('div_questions_answer4').style.color = 'rgb(60, 60, 60)';
                document.getElementById('div_questions_answer2').style.background = 'rgb(200, 200, 200)';
                document.getElementById('div_questions_answer3').style.background = 'rgb(200, 200, 200)';
                document.getElementById('div_questions_answer4').style.background = 'rgb(200, 200, 200)';
             };
            if (id_ == 'checkbox2') {
                document.getElementById('div_questions_answer2').style.background = 'green';
                document.getElementById('div_questions_answer2').style.color = 'white';
                document.getElementById('div_questions_answer1').style.color = 'rgb(60, 60, 60)';
                document.getElementById('div_questions_answer3').style.color = 'rgb(60, 60, 60)';
                document.getElementById('div_questions_answer4').style.color = 'rgb(60, 60, 60)';
                document.getElementById('div_questions_answer1').style.background = 'rgb(200, 200, 200)';
                document.getElementById('div_questions_answer3').style.background = 'rgb(200, 200, 200)';
                document.getElementById('div_questions_answer4').style.background = 'rgb(200, 200, 200)';
             };
            if (id_ == 'checkbox3') {
                document.getElementById('div_questions_answer3').style.background = 'green';
                document.getElementById('div_questions_answer3').style.color = 'white';
                document.getElementById('div_questions_answer2').style.color = 'rgb(60, 60, 60)';
                document.getElementById('div_questions_answer1').style.color = 'rgb(60, 60, 60)';
                document.getElementById('div_questions_answer4').style.color = 'rgb(60, 60, 60)';
                document.getElementById('div_questions_answer2').style.background = 'rgb(200, 200, 200)';
                document.getElementById('div_questions_answer1').style.background = 'rgb(200, 200, 200)';
                document.getElementById('div_questions_answer4').style.background = 'rgb(200, 200, 200)';
             };
            if (id_ == 'checkbox4') {
                document.getElementById('div_questions_answer4').style.background = 'green';
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
}