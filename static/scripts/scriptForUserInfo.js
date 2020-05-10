function showDiagramm(procent_def, procent_win) {var dataset = [
  {
    value: procent_def,
    color: 'white'
  },
  {
    value: procent_win,
    color: 'rgb(255, 70, 0)'
  }
];

var maxValue = 25;
var container = $('.container1');

var addSector = function(data, startAngle, collapse) {
  var sectorDeg = 3.6 * data.value;
  var skewDeg = 90 + sectorDeg;
  var rotateDeg = startAngle;
  if (collapse) {
    skewDeg++;
  }

  var sector = $('<div>', {
    'class': 'sector'
  }).css({
    'background': data.color,
    'transform': 'rotate(' + rotateDeg + 'deg) skewY(' + skewDeg + 'deg)'
  });
  container.append(sector);

  return startAngle + sectorDeg;
};

dataset.reduce(function (prev, curr) {
  return (function addPart(data, angle) {
    if (data.value <= maxValue) {
      return addSector(data, angle, false);
    }

    return addPart({
      value: data.value - maxValue,
      color: data.color
    }, addSector({
      value: maxValue,
      color: data.color,
    }, angle, true));
  })(curr, prev);
}, 0);}

function showDiagramm1(procent_win, procent_def) {var dataset = [
  {
    value: procent_def,
    color: 'white'
  },
  {
    value: procent_win,
    color: 'rgb(137, 200, 211)'
  }
];

var maxValue = 25;
var container = $('.container');

var addSector = function(data, startAngle, collapse) {
  var sectorDeg = 3.6 * data.value;
  var skewDeg = 90 + sectorDeg;
  var rotateDeg = startAngle;
  if (collapse) {
    skewDeg++;
  }

  var sector = $('<div>', {
    'class': 'sector'
  }).css({
    'background': data.color,
    'transform': 'rotate(' + rotateDeg + 'deg) skewY(' + skewDeg + 'deg)'
  });
  container.append(sector);

  return startAngle + sectorDeg;
};

dataset.reduce(function (prev, curr) {
  return (function addPart(data, angle) {
    if (data.value <= maxValue) {
      return addSector(data, angle, false);
    }

    return addPart({
      value: data.value - maxValue,
      color: data.color
    }, addSector({
      value: maxValue,
      color: data.color,
    }, angle, true));
  })(curr, prev);
}, 0);};

$(document).ready(function() {
    if ( $( window ).width() > 980 | !(/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent))) {
        $('#main_div_user_info').height( $('#div_user_games_and_info').height() + 40);
    }
    else {
        $('#user_avatar_and_root').height( 600 );
    }
});

function copyToClipboard() {
     var copytext = document.createElement('input');
     copytext.value = window.location.href;
     document.body.appendChild(copytext);
     copytext.select();
     document.execCommand('copy');
     document.body.removeChild(copytext);
}

