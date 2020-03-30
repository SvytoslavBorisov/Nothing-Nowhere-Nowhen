document.getElementById('top_menuDiv').style.width = String(document.documentElement.clientWidth) + 'px';
document.getElementById('top_menuDiv').style.height = '75px';

for (var i = 0; i < document.getElementsByClassName('navigator_div').length - 1; i++) {

    document.getElementsByClassName('navigator_div')[i].style.height = '47px';
    document.getElementsByClassName('navigator_div')[i].style.maxHeight = '75px';
};

document.getElementsByClassName('navigator_div')[document.getElementsByClassName('navigator_div').length - 1].style.height = '57px';
document.getElementsByClassName('navigator_div')[document.getElementsByClassName('navigator_div').length - 1].style.maxHeight = '75px';

document.getElementById('top_menuDiv').style.background = 'rgb(35, 40, 45)';

window.onresize = function () {
    document.getElementById('top_menuDiv').style.width = String(document.documentElement.clientWidth) + 'px';
};