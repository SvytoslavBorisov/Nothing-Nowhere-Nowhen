
/* СЛАЙДЕР НА ГЛАВНОЙ СТРАНИЦЕ */

'use strict';
var multiItemSlider = (function () {
  return function (selector, config) {
    var
      _mainElement = document.querySelector(selector),
      _sliderWrapper = _mainElement.querySelector('.slider__wrapper'),
      _sliderItems = _mainElement.querySelectorAll('.slider__item'),
      _sliderControls = _mainElement.querySelectorAll('.slider__control'),
      _sliderControlsButton = _mainElement.querySelectorAll('.p_news_lenta'),
      _sliderControlLeft = _mainElement.querySelector('.slider__control_left'),
      _sliderControlRight = _mainElement.querySelector('.slider__control_right'),
      _wrapperWidth = parseFloat(getComputedStyle(_sliderWrapper).width),
      _itemWidth = parseFloat(getComputedStyle(_sliderItems[0]).width),
      _positionLeftItem = 0,
      _transform = 0,
      _step = _itemWidth / _wrapperWidth * 100,
      _items = [];
    _sliderItems.forEach(function (item, index) {
      _items.push({ item: item, position: index, transform: 0 });
    });

    var position = {
      getMin: 0,
      getMax: _items.length - 1,
    }

    var _transformItem = function (direction, _id) {
        $('#slider_news_' + '1').css('visibility', 'hidden');
        $('#slider_news_' + '2').css('visibility', 'hidden');
        $('#slider_news_' + '3').css('visibility', 'hidden');
        $('#slider_news_' + '4').css('visibility', 'hidden');
        $('#slider_news_' + '5').css('visibility', 'hidden');
      if (direction === 'right') {
        if ((_positionLeftItem + _wrapperWidth / _itemWidth - 1) >= position.getMax) {
          return;
        }
        if (!_sliderControlLeft.classList.contains('slider__control_show')) {
          _sliderControlLeft.classList.add('slider__control_show');
        }
        if (_sliderControlRight.classList.contains('slider__control_show') && (_positionLeftItem + _wrapperWidth / _itemWidth) >= position.getMax) {
          _sliderControlRight.classList.remove('slider__control_show');
        }
        _positionLeftItem++;

        for (var i = 0; i < document.getElementsByClassName('p_news_lenta').length; i++) {
            document.getElementsByClassName('p_news_lenta')[i].style.background = 'rgb(200, 200, 200)';
        }

        $('#slider_text_' + _positionLeftItem).css('background', 'rgb(186, 48, 48)');
        _transform -= _step;
        $('#slider_news_' + String(_positionLeftItem + 1)).css('visibility', 'visible');
        };
      if (direction === 'left') {
        if (_positionLeftItem <= position.getMin) {
          return;
        }
        if (!_sliderControlRight.classList.contains('slider__control_show')) {
          _sliderControlRight.classList.add('slider__control_show');
        }
        if (_sliderControlLeft.classList.contains('slider__control_show') && _positionLeftItem - 1 <= position.getMin) {
          _sliderControlLeft.classList.remove('slider__control_show');
        }
        _positionLeftItem--;
        _transform += _step;
        for (var i = 0; i < document.getElementsByClassName('p_news_lenta').length; i++) {
            document.getElementsByClassName('p_news_lenta')[i].style.background = 'rgb(200, 200, 200)';
        }

        $('#slider_text_' + _positionLeftItem).css('background', 'rgb(186, 48, 48)');
        $('#slider_news_' + String(_positionLeftItem + 1)).css('visibility', 'visible');
      };
      if (direction === 'no') {

        _sliderControlRight.classList.add('slider__control_show');
        _sliderControlLeft.classList.add('slider__control_show');

        if (Number(_id) == position.getMin) {
          _sliderControlRight.classList.add('slider__control_show');
          _sliderControlLeft.classList.remove('slider__control_show');
        }

        if (Number(_id) == position.getMax) {
          _sliderControlRight.classList.remove('slider__control_show');
          _sliderControlLeft.classList.add('slider__control_show');
        }

        _transform += (_positionLeftItem - Number(_id)) * _step;
        _positionLeftItem = Number(_id);

        for (var i = 0; i < document.getElementsByClassName('p_news_lenta').length; i++) {
            document.getElementsByClassName('p_news_lenta')[i].style.background = 'rgb(200, 200, 200)';
        }

        $('#slider_text_' + _positionLeftItem).css('background', 'rgb(186, 48, 48)');
      };
      _sliderWrapper.style.transform = 'translateX(' + _transform + '%)';
    };

    var _controlClick = function (e) {
      if (e.target.classList.contains('slider__control')) {
        e.preventDefault();
        var direction = e.target.classList.contains('slider__control_right') ? 'right' : 'left';
        _transformItem(direction);
      }
    };

    var _click_on_p_news_lenta = function (e, _id) {
      if (e.target.classList.contains('p_news_lenta')) {
        e.preventDefault();
        var i = 0;
        while (e.target.id != 'slider_text_' + String(i)) {
            i++;
        };
        var direction = i;
        _transformItem('no', direction);
      }
    };

    var _setUpListeners = function () {

      _sliderControls.forEach(function (item) {
        item.addEventListener('click', _controlClick);
      });
      _sliderControlsButton.forEach(function (item) {
        item.addEventListener('click', _click_on_p_news_lenta);
      });
      _transformItem('no', 0);
    }

    _setUpListeners();

    return {
      right: function () {
        _transformItem('right');
      },
      left: function () {
        _transformItem('left');
      }
    }

  }
}());

var slider = multiItemSlider('#div_lenta_news')
$('#slider_news_' + '1').css('visibility', 'visible');


$( window ).resize(function (){
    $('.image_news_lenta').width('100%');
    $('.slider__item').height($('.image_news_lenta').height());
});

$('.image_news_lenta').width('100%');

$(document).ready(function() {
    $('.slider__item').height($('.image_news_lenta').height());
});
/* ПОЯВЛЕНИЕ И ИСЧЕЗАНИЕ НОВОСТНОЙ ЛЕНТЫ */
/*function fadeIn(el, speed) {
  var step = 1 / speed;
  var interval = setInterval(function() {
    if (+el.style.opacity >= 1)
      clearInterval(interval);

    el.style.opacity = +div.style.opacity + step;
  }, speed / 1000);
};

function fadeOut(el, speed) {
  var step = 1 / speed;
  var interval = setInterval(function() {
    if (el.style.opacity <= 0)
      clearInterval(interval);

    el.style.opacity = +div.style.opacity - step;
  }, speed / 1000);
};

var div = document.getElementById("div_news");

 if ( $( window ).width() > 980 | !(/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent))) {
    window.addEventListener('scroll', function() {
        fadeIn(div, 250);
          if ($(window).scrollTop() == 0) {
            fadeOut(div, 50);
          };
    });}
else {
    $('#div_news').css('opacity', 100);
} */