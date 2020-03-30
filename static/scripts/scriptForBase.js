document.getElementById('top_menuDiv').style.width = String(document.documentElement.clientWidth) + 'px';
document.getElementById('top_menuDiv').style.height = '75px';
document.getElementById('top_menuDiv').style.background = 'rgb(35, 40, 45)';

window.onresize = function () {
    document.getElementById('top_menuDiv').style.width = String(document.documentElement.clientWidth) + 'px';
};