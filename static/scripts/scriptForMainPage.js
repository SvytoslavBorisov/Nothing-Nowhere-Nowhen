'use strict';
var multiItemSlider = (function () {
  return function (selector, config) {
    var
      _mainElement = document.querySelector(selector), // основный элемент блока
      _sliderWrapper = _mainElement.querySelector('.slider__wrapper'), // обертка для .slider-item
      _sliderItems = _mainElement.querySelectorAll('.slider__item'), // элементы (.slider-item)
      _sliderControls = _mainElement.querySelectorAll('.slider__control'), // элементы управления
      _sliderControlsButton = _mainElement.querySelectorAll('.p_news_lenta'), // элементы управления
      _sliderControlLeft = _mainElement.querySelector('.slider__control_left'), // кнопка "LEFT"
      _sliderControlRight = _mainElement.querySelector('.slider__control_right'), // кнопка "RIGHT"
      _wrapperWidth = parseFloat(getComputedStyle(_sliderWrapper).width), // ширина обёртки
      _itemWidth = parseFloat(getComputedStyle(_sliderItems[0]).width), // ширина одного элемента
      _positionLeftItem = 0, // позиция левого активного элемента
      _transform = 0, // значение транфсофрмации .slider_wrapper
      _step = _itemWidth / _wrapperWidth * 100, // величина шага (для трансформации)
      _items = []; // массив элементов
    // наполнение массива _items
    _sliderItems.forEach(function (item, index) {
      _items.push({ item: item, position: index, transform: 0 });
    });

    var position = {
      getMin: 0,
      getMax: _items.length - 1,
    }

    var _transformItem = function (direction, _id) {
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

    // обработчик события click для кнопок "назад" и "вперед"
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
      // добавление к кнопкам "назад" и "вперед" обрботчика _controlClick для событя click
      _sliderControls.forEach(function (item) {
        item.addEventListener('click', _controlClick);
      });
      _sliderControlsButton.forEach(function (item) {
        item.addEventListener('click', _click_on_p_news_lenta);
      });
      _transformItem('no', 0);
    }

    // инициализация
    _setUpListeners();

    return {
      right: function () { // метод right
        _transformItem('right');
      },
      left: function () { // метод left
        _transformItem('left');
      }
    }

  }
}());

var slider = multiItemSlider('#div_lenta_news')

$('#main_div').height($('#main_div').height() + 1);

document.getElementById('div_news').style.visibility = 'hidden';

window.addEventListener('scroll', function() {
  document.getElementById('footer').style.visibility = 'visible';
  document.getElementById('div_news').style.visibility = 'visible';
  if ($(window).scrollTop() == 0) {
    document.getElementById('div_news').style.visibility = 'hidden';
  };
});