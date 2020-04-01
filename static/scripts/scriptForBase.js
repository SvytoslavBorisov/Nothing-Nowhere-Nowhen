window.onresize = function () {
    document.getElementById('top_menuDiv').style.width = String(document.documentElement.clientWidth) + 'px';
    document.getElementById('all_navigator_div').style.width = String(document.documentElement.clientWidth - 400) + 'px';
};

document.getElementById('top_menuDiv').style.width = String(document.documentElement.clientWidth) + 'px';
document.getElementById('all_navigator_div').style.width = String(document.documentElement.clientWidth - 400) + 'px';