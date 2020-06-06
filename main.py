'''Библиотека FLASK'''
from flask import Flask, render_template, redirect, request, make_response, jsonify
from flask_restful import Api
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
import requests

'''Классы для работы с таблицами Базы Данных(папка data)'''
from data import db_session
from data.categories import Category
from data.questions import Question
from data.users import User
from data.games import Game
from data.news import News

'''Библиотека для работы с элементом случайности'''
from random import choice, shuffle

'''Классы для работы с файлами json, временем, словарями'''
from secondary_functions import open_json, save_json, get_time, format_date, fill_dict

'''Библиотека для работы с ОС'''
import os
import configparser

'''Cоздаём объекта парсера. Читаем конфигурационный файл'''
config = configparser.ConfigParser()
config.read("config.ini", encoding='utf-8')

'''Классы для работы с формами для работы с польхователем'''
from forms.register import RegisterForm
from forms.login import LoginForm
from forms.add_question import AddQuestionForm
from forms.check_quests import CheckQuestionForm

'''Классы для работы с собственным API(папка api)'''
from api import questions_api, users_api

'''Библиотеки для реализации отправки писем'''
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email import encoders
from platform import python_version

"""Загрузка переменных среды из файла"""
from dotenv import load_dotenv
load_dotenv(dotenv_path=config['PATH']['SECRET_DATA'])

'''Запуск приложения FLASK'''
application = Flask(__name__)

'''Настройка приложения для того, чтобы можно было сохранять русские символы в json'''
application.config.update(
    JSON_AS_ASCII=False
)

'''Регистрация API в приложении'''
application.register_blueprint(questions_api.blueprint)
application.register_blueprint(users_api.blueprint)

'''Соединение с Базой Данных'''
db_session.global_init("db/baseDate.sqlite")

'''Инициализируем LoginManager'''
login_manager = LoginManager()
login_manager.init_app(application)


'''Функция для получения пользователя'''
@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


'''Выход из аккаунта для пользователя'''
@application.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


'''Эта настройка защитит наше приложение от межсайтовой подделки запросов'''
application.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


'''
    Функция для возвращения пользователя в игру, 
    если она была прервана по каким-либо причинам
    1. Открытие файла с сохранёнными играми для пользователей
    2. Проверка пользователь зашёл в аккаунт или нет & Проверка была ли не закончена игра у текущего пользователя 
'''
def return_to_game():
    data = open_json('static/json/games.json')                          # 1
    if current_user.is_authenticated and \
            str(current_user.id) in data['current_games'] and \
            data['current_games'][str(current_user.id)] is not None:    # 2
        return 1
    return 0


@application.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


'''
    Страница для выбора категории для следующей игры.
    1. Проверка была ли начата игра текущим пользователем
    2. Если у текущего пользователя есть незаконченная игра, то он будет должен ее доиграть
    3. Подключение к базе данных
    4. Создание словаря для работы с переменными в html коде
        'title'            - Заголовок страницы
        'style'            - Названия файлов, в которых храняться стили для данной страницы
        'path_for_style'   - Путь к папке со стилями
        'style_for_mobile' - Путь к файлу с css стилями для мобильного устройства
        'categories'       - Все элементы Category из БД
    5. Рендеринг
'''
@application.route('/categories')
def categories():
    if return_to_game():                          # 1
        return redirect('/current_game')          # 2

    session = db_session.create_session()         # 3

    registerForm = RegisterForm()
    loginForm = LoginForm()

    param = fill_dict(                            # 4
        title='Категории',
        style=os.listdir(config["PATH"]['to_css'] + 'styleForCategories/'),
        path_for_style=config["PATH"]['to_css'] + 'styleForCategories/',
        style_mobile=config["PATH"]['to_css_mobile'] + 'styleForCategoriesMobile.css',
        categories=session.query(Category).all())
    return render_template('categories.html', **param, formLogin=loginForm, formRegister=registerForm)  # 5


'''
    Главная страница сайта. Рейтинг. Новости.
    1. Проверка была ли начата игра текущим пользователем
    2. Если у текущего пользователя есть незаконченная игра, то он будет должен ее доиграть
    3. Подключение к базе данных
    4. Получение всех пользователей сайта. Сортировка по рейтингу
    5. Создание словаря для работы с переменными в html коде
        'title'            - Заголовок страницы
        'style'            - Названия файлов, в которых храняться стили для данной страницы
        'path_for_style'   - Путь к папке со стилями
        'style_for_mobile' - Путь к файлу с css стилями для мобильного устройства
        'news'             - Все элементы News из БД [ Текст новости, картинка, заголовок, id]
        'users'            - Все пользователи, отсортированные по рейтингу
    6. Рендеринг
'''
@application.route('/')
def main_page():
    if return_to_game():                   # 1
        return redirect('/current_game')   # 2

    session = db_session.create_session()  # 3

    all_users = session.query(User).all()                                                              # 4
    all_users.sort(key=lambda x: (-x.rating, x.surname.lower() + x.name.lower(), x.nickname.lower()))  # 4

    registerForm = RegisterForm()
    loginForm = LoginForm()

    param = fill_dict(                     # 5
        title='Главная страница',
        style=os.listdir(config["PATH"]['to_css'] + 'styleForMainPage/'),
        path_for_style=config["PATH"]['to_css'] + 'styleForMainPage/',
        style_mobile=config["PATH"]['to_css_mobile'] + 'styleForMainPageMobile.css',
        news=[[new.text.split('!@#$%')[1], new.image, new.caption, new.id] for new in session.query(News).all()],
        users=all_users)

    return render_template('main_page.html', **param, formLogin=loginForm, formRegister=registerForm)  # 6


'''
    Рейтинг.
    1. Проверка была ли начата игра текущим пользователем
    2. Если у текущего пользователя есть незаконченная игра, то он будет должен ее доиграть
    3. Подключение к базе данных
    4. Получение всех пользователей сайта. Сортировка по рейтингу
    5. Создание словаря для работы с переменными в html коде
        'title'            - Заголовок страницы
        'style'            - Названия файлов, в которых храняться стили для данной страницы
        'path_for_style'   - Путь к папке со стилями
        'style_for_mobile' - Путь к файлу с css стилями для мобильного устройства
        'users'            - Все пользователи, отсортированные по рейтингу
    6. Рендеринг
'''
@application.route('/rating')
def rating():
    if return_to_game():                   # 1
        return redirect('/current_game')   # 2

    session = db_session.create_session()  # 3

    all_users = session.query(User).all()                                                              # 4
    all_users.sort(key=lambda x: (-x.rating, x.surname.lower() + x.name.lower(), x.nickname.lower()))  # 4

    registerForm = RegisterForm()
    loginForm = LoginForm()

    param = fill_dict(                     # 5
        title='Главная страница',
        style=os.listdir(config["PATH"]['to_css'] + 'styleForRating/'),
        path_for_style=config["PATH"]['to_css'] + 'styleForRating/',
        style_mobile=config["PATH"]['to_css_mobile'] + 'styleForRatingMobile.css',
        users=all_users)

    return render_template('rating.html', **param, formLogin=loginForm, formRegister=registerForm)  # 6


'''
    Авторизации на сайте.
    1. Проверка была ли начата игра текущим пользователем
    2. Если у текущего пользователя есть незаконченная игра, то он будет должен ее доиграть
    3. Подключение к базе данных
    4. Если выполнен POST запрос
    5. Проверяем правильно ли введены данные
    6. Выводим сообщение, если непрвильно введены данные
    7. Переход на главную страницу
'''
@application.route('/login', methods=['POST', 'GET'])
def login():
    if return_to_game():                   # 1
        return redirect('/current_game')   # 2

    session = db_session.create_session()  # 3

    if request.method == 'POST':          # 4
        user = session.query(User).filter(User.email == request.form['email']).first()  # 5

        if user.check_password(request.form['psw']):
            login_user(user)
            return redirect('/')
    return redirect('/')                                                          # 7


'''
    Страница регистрации на сайте.
    1. Проверка была ли начата игра текущим пользователем
    2. Если у текущего пользователя есть незаконченная игра, то он будет должен ее доиграть
    3. Подключение к базе данных
    4. Создание словаря для работы с переменными в html коде
        'title'            - Заголовок страницы
        'style'            - Названия файлов, в которых храняться стили для данной страницы
        'path_for_style'   - Путь к папке со стилями
        'style_for_mobile' - Путь к файлу с css стилями для мобильного устройства
    5. Создание формы для авторизации пользователя
    6. Проверка, была ли отправлена форма.
    7. Проверка есть ли пользователь с таким же email
    8. Проверка есть ли пользователь с таким же ником
    9. Создание нового пользователя, коммит
об ошибке и предложено ввести данные ещё раз.
    10. Если пользователь указал аватар, то установить его, иначе стандартный
    11. Перемещаем пользователя в стартовое меню для выбора игры
    12. Рендеринг
'''
@application.route('/register', methods=['POST', 'GET'])
def register():

    session = db_session.create_session()

    if request.method == 'POST':
        user = session.query(User).filter(User.email == request.form['email']).first()
        if user.check_password(request.form['password']):
            login_user(user)
            redirect('/')
    return redirect('/')



@application.route('/edit_avatar/<int:id_>', methods=['POST'])
def edit_avatar(id_):

    if current_user.is_authenticated and current_user.id == id_:

        session = db_session.create_session()  # 3

        user = session.query(User).filter(User.id == current_user.id).first()

        if user:
            if user.avatar != '/static/img/users_avatars/no_photo.png':
                os.remove(user.avatar[1:])
            user.avatar = f'/static/img/users_avatars/{user.id}+{get_time()}.png'
            with open(user.avatar[1:], 'wb') as f1:
                f1.write(request.files['edit_avatar'].read())

            session.commit()
        return redirect('/user_info/' + current_user.nickname)
    return redirect('/')


'''
    Страница информации о пользователе.
    1. Проверка была ли начата игра текущим пользователем
    2. Если у текущего пользователя есть незаконченная игра, то он будет должен ее доиграть
    3. Подключение к базе данных
    4. В пути указывается никнейм пользователя, чей это профиль
    5. Получаем пользователя из БД, чей это профиль
    6. Создание словаря для работы с переменными в html коде
        'title'            - Заголовок страницы
        'style'            - Названия файлов, в которых храняться стили для данной страницы
        'path_for_style'   - Путь к папке со стилями
        'style_for_mobile' - Путь к файлу с css стилями для мобильного устройства
        'user'             - Пользователь, чей это профиль
        'games'            - Игры пользователя, чей это профиль
        'procent_win'      - Процент побед
        'procent_def'      - Процент поражений
    7. Рендеринг
'''
@application.route('/user_info/<string:user>')  # 4
def user_info(user):
    if return_to_game():                    # 1
        return redirect('/current_game')    # 2

    session = db_session.create_session()   # 3

    user = session.query(User).filter(User.nickname == user).first()  # 5
    categories = session.query(Category).all()  # 4

    registerForm = RegisterForm()
    loginForm = LoginForm()

    addQuestForm = AddQuestionForm()

    addQuestForm.category.choices = [(category.name, category.name) for category in categories[1:]]  # 8
    addQuestForm.category.default = categories[1].name  # 9
    addQuestForm.type.choices = [('change', 'С вариантами'), ('write','С вводом ответа'), ('all', 'И так и так')]
    addQuestForm.complexity.choices = [('1', 'Новичок'), ('2', 'Любитель'), ('3',  'Профи')]

    param = fill_dict(                      # 6
        title='Профиль',
        style=os.listdir(config["PATH"]['to_css'] + 'styleForUserInfo/'),
        path_for_style=config["PATH"]['to_css'] + 'styleForUserInfo/',
        style_mobile=config["PATH"]['to_css_mobile'] + 'styleForUserInfoMobile.css',
        user=user,
        games=user.games,
        procent_win=user.get_procent_win(),
        procent_def=100 - user.get_procent_win())

    return render_template('user_info.html', **param, formLogin=loginForm, formRegister=registerForm, formAddQuest=addQuestForm)  # 7


'''
    Страница информации о сайте.
    1. Проверка была ли начата игра текущим пользователем
    2. Если у текущего пользователя есть незаконченная игра, то он будет должен ее доиграть
    3. В пути указывается катнгория игры, которую выбрал пользователь
    4-5. Если пользователь выбрал сложность и тип вопроса, то переходим к старту игры
    6. Подключение к базе данных
    7. Создание словаря для работы с переменными в html коде
        'title'            - Заголовок страницы
        'style'            - Путь к файлу с css стилями
        'style_for_mobile' - Путь к файлу с css стилями для мобильного устройства
        'category'         - Выбранная пользователем категория
    8. Рендеринг
'''
@application.route('/game/<int:id_>', methods=['POST', 'GET'])  # 3
def game(id_):
    if return_to_game():                    # 1
        return redirect('/current_game')    # 2

    registerForm = RegisterForm()
    loginForm = LoginForm()

    if request.method == 'POST':             # 4
        return redirect(f'/start_game/{str(id_)}+{str(request.form["complexity"])}+{str(request.form["type"])}')  # 5

    session = db_session.create_session()   # 6

    param = fill_dict(                      # 7
        title='Начать игру',
        style=os.listdir(config["PATH"]['to_css'] + 'styleForGame/'),
        path_for_style=config["PATH"]['to_css'] + 'styleForGame/',
        style_mobile=config["PATH"]['to_css_mobile'] + 'styleForGameMobile.css',
        category=session.query(Category).filter(Category.id == id_).first())

    return render_template('game.html', **param, formLogin=loginForm, formRegister=registerForm)  # 8


'''
    Функция старта игры.
    1. Проверка была ли начата игра текущим пользователем, 
если у текущего пользователя есть незаконченная игра, то он будет должен ее доиграть
    2. Подключение к базе данных
    3. ID категории, сложность и тип вопроса
    4. Переменная для подходящих вопросов
    5. Проверка, авторизовался ли пользователь
    6. Если категория не "Общая", 
    ТО
    7-8. Добавляем вопросы, только выбранной категории, сложности, типа и те которые не создал сам игрок 
    ИНАЧЕ
    9-10. Добавляем вопросы, всех категорий, выбранной сложности, типа и те которые не создал сам игрок 
    11. Если пользователь не авторизовался, то переводим его на страницу авторизации
    12. Переменная для выбора итоговых 11 вопросов
    13. Подбираем итоговые случайные вопросы для игры
    14. Открываем файл с сохранениями
    15. Записываем в него текущую игру
        'questions'                - Вопросы
        'wins'                     - Правильно отвечено
        'category'                 - Категория игры 
        'defeats'                  - Неправильно отвечено
        'current_question'         - Текущий номер вопроса
        'time': get_time()         - Текущее время
        'quest_or_next'            - Идет игра или Показывается ответ на вопрос
        'last_result'              - Последний результат
        'type'                     - Тип вопроса
        'complexity'               - Сложность вопроса
        'last_answer'              - Последний ответ
    16. Проверяем, есть ли в данной категории хотя бы 11 вопросов, 
если нет, то выводим уведомление, что категория в разработке
    17. Создаём новую игру в сохранениях 
    18. Заполняем сохранение данными
    19. Сохраняем изменения
    20. Переходим на страницу игры
'''
@application.route('/start_game/<int:id_>+<int:comp_>+<type>', methods=['POST', 'GET'])
def start_game(id_, comp_, type):  # 3
    if return_to_game():                   # 1
        return redirect('/current_game')   # 1

    registerForm = RegisterForm()
    loginForm = LoginForm()

    quests = []                                # 4
    if current_user.is_authenticated:          # 5
        session = db_session.create_session()  # 2

        if id_ != 1:                           # 6
            for question in session.query(Question).filter(Question.category == id_,                            # 7
                                                           Question.who_add != current_user.id,                 # 7
                                                           (Question.type == type) | (Question.type == 'all'),  # 7
                                                           Question.complexity == int(comp_)):                  # 7
                quests.append(question)    # 8
        else:
            for question in session.query(Question).filter(Question.who_add != current_user.id,  # 9
                                                          (Question.type == type) | (Question.type == 'all'),
                                                           Question.complexity == int(comp_)):   # 9
                quests.append(question)    # 10
    else:
        return ''' 
                <script>
                    alert('Для того, чтобы поиграть в викторину, нужно зарегистрироваться.');
                    document.location.href = "/categories";
                </script>
                '''          # 11

    if len(quests) < 11:      # 16
        return ''' 
                <script>
                    alert('Недостаточно вопросов данной сложности или типа в этой категории. Выберите другую категорию. Извините за неудобства.');
                    document.location.href = "/categories";
                </script>
                '''
    selected = []                       # 12
    for _ in range(11):                 # 13
        k = choice(quests)              # 13
        while k in selected:            # 13
            k = choice(quests)          # 13
        selected.append(k)              # 13

    data = open_json(config['PATH']['games'])      # 14

    load = {                                       # 15
        'questions': [x.id for x in selected],
        'wins': 0,
        'category': id_,
        'defeats': 0,
        'current_question': 0,
        'time': get_time(),
        'quest_or_next': 'quest',
        'last_result': None,
        'type': type,
        'complexity': comp_,
        'last_answer': '',
        'delete': [],
        'create_map': 'yes'
    }

    data['current_games'][str(current_user.id)] = {}  # 17
    for x in load:                                                # 18
        data['current_games'][str(current_user.id)][x] = load[x]  # 18

    save_json(data, config['PATH']['games'])         # 19

    return redirect('/current_game')                  # 20


'''
    Страница текущей игры
    1. Проверка зашёл ли пользователь в аккаунт
    2. Подключение к базе данных
    3. Открытие файла с сохранением игры
    4. Если игрок не начинал игру, то его перемещают в стартовое меню
    5. Данные текущей игры в удобную переменную
    6. Получаем ID текущего вопроса
    7. Получаем текущий вопрос
    8. Если в данный момент идет ожидание ответа на вопрос
    ТО
        9. Создаём рандомную расстановку вариантов ответа
        10. Получаем из вопроса ответы на него
        11. Расставляем варианты вопросов по созданной расстановке
        12. Создание словаря для работы с переменными в html коде
            'title'                - Заголовок страницы
            'style'                - Названия файлов, в которых храняться стили для данной страницы
            'path_for_style'       - Путь к папке со стилями
            'style_for_mobile'     - Путь к файлу с css стилями для мобильного устройства
            'question'             - Текущий вопрос
            'answers'              - Ответы на вопрос
            'current_number_quest' - Номер текущего вопроса
            'image_question'       - Картинка к вопросу
            'type_quest'           - Тип вопроса
            'current_time'         - Оставшееся время
            'user'                 - Создатель вопроса
            'win'                  - Количество правильных ответов на вопрос
            'defeat'               - Количество неправильных ответов на вопрос
        13. Если игрок нажал на "Отправить" или закончилось время
        ТО
            14. Меняем статус игры на "Ответ"
            15. Если игрок не оставил поле ответа пустым
            ТО
                16-17. Приравниваем вариант пользователя и правильный ответ. 
                Делаем выввод правильно ответил пользователь или нет. Если неправильно, то создателю вопроса +1 к рейтингу
            ИНАЧЕ
                18. Ответ неправильный. Создателю вопроса +1 к рейтингу
            19. Сохраняеи изменения в БД
            20. Обновляем данные игры
            21. В зависимости от результата прибавляем побед/поражений
            22. Сохраняем изменения в файле
            23. Переходим к показу правильного ответа
        ИНАЧЕ
            24. Игра начинается или продолжается 
    ИНАЧЕ
        25. (СМ.ПУНКТ 12) Создание словаря для работы с переменными в html коде
            'result'                  - Результат ответа на вопрос
        26. Показывается ответ на вопрос
        27. Если пользователь продолжил игру
        28. Меняем статус игры на "Вопрос"
        29. Увеличиваем кол-во вопросов на которые ответил игрок
        30. Устанавливаем время показа вопроса
        31-32. Если еще никто не набрал 6 баллов, то игра продолжается. Сохраняем изменения и переходим к игре
        33. Если игра закончена, то получаем из БД играющего игрока
        34. Увеличиваем ему количество сыгранных игр
        35. Увеличиваем ему количество побед или поражений
        36. Увеличиваем рейтинг по формуле
        37. Создаёи объект класса Game и сохраняем данные о игре в БД
        38. Сохранение данных
        39. Обнудение текущей игры
        40. Переходим к странице завершения игры, передавая в пути результат игры 
    41. Если игрок не зарегистрирован, то переводим его на страницу регистрации
'''
@application.route('/current_game', methods=['POST', 'GET'])
def current_game():
    if current_user.is_authenticated:                           # 1
        session = db_session.create_session()                   # 2
        data = open_json(config['PATH']['games'])               # 3

        if not data['current_games'][str(current_user.id)]:     # 4
            return redirect('/change_play')                     # 4

        this_game_data = data['current_games'][str(current_user.id)]                         # 5

        cur_quest_id = this_game_data['questions'][this_game_data['current_question']]       # 6
        this_question = session.query(Question).filter(Question.id == cur_quest_id).first()  # 7

        registerForm = RegisterForm()
        loginForm = LoginForm()

        if this_game_data['quest_or_next'] == 'quest':  # 8

            temp_shuffle_answers = [0, 1, 2, 3]  # 9
            shuffle(temp_shuffle_answers)        # 9

            answers = this_question.answers.split('!@#$%')  # 10
            shuffle_answers = []                    # 11
            for x in temp_shuffle_answers:          # 11
                shuffle_answers.append(answers[x])  # 11

            param = fill_dict(                      # 12
                title='Идёт игра',
                style=os.listdir(config["PATH"]['to_css'] + 'styleForCurrentGame/'),
                path_for_style=config["PATH"]['to_css'] + 'styleForCurrentGame/',
                style_mobile=config["PATH"]['to_css_mobile'] + 'styleForCurrentGameMobile.css',
                question=this_question,
                answers=shuffle_answers,
                current_number_quest=this_game_data['current_question'],
                image_question=this_question.images,
                type_quest=this_game_data['type'],
                current_time=get_time() - this_game_data['time'],
                user=session.query(User).filter(User.id == this_question.who_add).first(),
                win=this_game_data['wins'],
                defeat=this_game_data['defeats'])

            if request.method == 'POST' or param['current_time'] > 60:  # 13
                this_game_data['quest_or_next'] = 'next'                # 14

                if request.form.get('option'):                          # 15
                    if request.form['option'].lower().strip().replace('ё', 'е') \
                            in set([x.lower().strip().replace('ё', 'е') for x in param['question'].right_answer.split('!@#$%')]):  # 16
                        result = True
                    else:
                        result = False
                        user = session.query(User).filter(User.id == param['question'].who_add).first()  # 17
                        user.rating += 1                                                                 # 17
                else:
                    result = False                                                                       # 18
                    user = session.query(User).filter(User.id == param['question'].who_add).first()      # 18
                    user.rating += 1                                                                     # 18
                session.commit()  # 19

                this_game_data['last_result'] = result                                                             # 20
                this_game_data['last_answer'] = request.form.get('option') if request.form.get('option') else ' '  # 20
                if result:                             # 21
                    this_game_data['wins'] += 1        # 21
                else:                                  # 21
                    this_game_data['defeats'] += 1     # 21

                data['current_games'][str(current_user.id)] = this_game_data   # 22

                save_json(data, config['PATH']['games'])                       # 22
                return redirect('/current_game')       # 23
            elif request.method == 'GET':
                return render_template('current_game.html', **param, formLogin=loginForm, formRegister=registerForm)  # 24
        else:
            param = fill_dict(  # 25
                title='Ответ',
                style=os.listdir(config["PATH"]['to_css'] + 'styleForCurrentGame/'),
                path_for_style=config["PATH"]['to_css'] + 'styleForCurrentGame/',
                style_mobile=config["PATH"]['to_css_mobile'] + 'styleForCurrentGameMobile.css',
                question=this_question,
                current_number_quest=this_game_data['current_question'],
                image_question=this_question.images,
                type_quest=this_game_data['type'],
                current_time=0,
                user=session.query(User).filter(User.id == this_question.who_add).first(),
                win=this_game_data['wins'],
                defeat=this_game_data['defeats'],
                result='Вы ответили правильно' if this_game_data['last_result'] else 'Вы ответили неправильно',
                last_answer=this_game_data['last_answer'])

            if request.method == 'GET':                                 # 26
                return render_template('next_game.html', **param, formLogin=loginForm, formRegister=registerForm)       # 26
            elif request.method == 'POST':                         # 27
                this_game_data['quest_or_next'] = 'quest'          # 28
                this_game_data['current_question'] += 1            # 29
                this_game_data['time'] = get_time()                # 30
                if param['win'] != 6 and param['defeat'] != 6:                    # 31
                    data['current_games'][str(current_user.id)] = this_game_data  # 32
                    save_json(data, config['PATH']['games'])                      # 32
                    return redirect('/current_game')                              # 32
                else:
                    user = session.query(User).filter(User.id == current_user.id).first()              # 33
                    user.all_games += 1                                                                # 33
                    user.wins += param['defeat'] != 6                                                  # 34
                    user.defeats += param['win'] != 6                                                  # 34
                    add_rating = 20 * int(this_game_data['complexity']) if param['defeat'] != 6 \
                        else param['win'] * int(this_game_data['complexity'])
                    user.rating += add_rating                                                         # 35

                    game_res = Game()                                                                  # 36
                    game_res.category = int(this_game_data['category'])                                # 37
                    game_res.result = param['defeat'] != 6                                             # 37
                    game_res.who_play = current_user.id                                                # 37
                    game_res.questions = '!@$'.join([str(x) for x in this_game_data['questions']])     # 37
                    game_res.result_questions = f"{param['win']}:{param['defeat']}"                    # 37
                    session.add(game_res)                                            # 38
                    session.commit()                                                 # 38

                    data['current_games'][str(current_user.id)] = None             # 39

                    save_json(data, 'static/json/games.json')                      # 39
                if param['defeat'] != 6:                  # 40
                    return redirect('/end_game/200+' + str(add_rating))      # 40
                else:                                     # 40
                    return redirect('/end_game/201+' + str(add_rating))      # 40
    else:
        return redirect('/login')    # 41


'''
    Страница завершения игры.
    1. Проверка была ли начата игра текущим пользователем, 
если у текущего пользователя есть незаконченная игра, то он будет должен ее доиграть
    2. Создание словаря для работы с переменными в html коде
        'title'            - Заголовок страницы
        'style'            - Названия файлов, в которых храняться стили для данной страницы
        'path_for_style'   - Путь к папке со стилями
        'style_for_mobile' - Путь к файлу с css стилями для мобильного устройства
        'why'              - Результат игры
    3. Рендеринг
'''
@application.route('/end_game/<why>+<int:add_rating>')
def end_game(why, add_rating):
    if return_to_game():                  # 1
        return redirect('/current_game')  # 1

    registerForm = RegisterForm()
    loginForm = LoginForm()

    param = fill_dict(  # 2
        title='Конец игры',
        style=os.listdir(config["PATH"]['to_css'] + 'styleForEndGame/'),
        path_for_style=config["PATH"]['to_css'] + 'styleForEndGame/',
        style_mobile=config["PATH"]['to_css_mobile'] + 'styleForEndGame.css',
        add_rating=add_rating,
        why='Вы победили! Результат записан' if why == '200' else 'Вы проиграли! Результат записан')

    return render_template('end_game.html', **param, formLogin=loginForm, formRegister=registerForm)  # 3


'''
    Страница модерации вопросов(admin).
    1. Проверка была ли начата игра текущим пользователем, 
если у текущего пользователя есть незаконченная игра, то он будет должен ее доиграть
    2. Создание формы для редактирования вопроса
    3. Если игрок вошел в аккаунт и имеет статус ADMIN
    ТО
        4. Подключение к базе данных
        5. Если админ посылает POST запрос 
        6. Если он нажал кнопку Добавить
        ТО
            7. Берем из БД первый непроверенный вопрос
            8. Изменияем вопрос и делаем его проверенным
            9. Сохраняем изменения, коммит
        ИНАЧЕ
            10. Удаляем вопрос из БД
        11. Создание словаря для работы с переменными в html коде
            'title'            - Заголовок страницы
            'style'            - Названия файлов, в которых храняться стили для данной страницы
            'path_for_style'   - Путь к папке со стилями
            'style_for_mobile' - Путь к файлу с css стилями для мобильного устройства
            'categories'       - Все категории вопросов из БД
            'quest'            - Первый непроверенный вопрос
        12. Если есть непроверенный вопрос, то тогда заполняем форму вопроса стандартными данными
        13. Переходим к html
        14. Если нет непроверенных вопросов, то тогда переходим в профиль
    ИНАЧЕ
        15. Предлагаем игроку войти
'''
@application.route('/check_quests', methods=['POST', 'GET'])
def check_quests():
    if return_to_game():                      # 1
        return redirect('/current_game')      # 1

    registerForm = RegisterForm()
    loginForm = LoginForm()

    form = CheckQuestionForm()                                            # 2
    if current_user.is_authenticated and current_user.state == 'admin':   # 3

        session = db_session.create_session()       # 4

        if request.method == 'POST':    # 5
            if request.form.get('submit'):                                                      # 6
                question = session.query(Question).filter(Question.is_promoted == 0).first()    # 7

                question.text = request.form['text']                                            # 8
                question.category = session.query(Category).filter(Category.name ==
                                                                   request.form['category']).first().id  # 8
                question.answers = "!@#$%".join(
                    [request.form['answer'], request.form['wrong_answer1'], request.form['wrong_answer2'],
                     request.form['wrong_answer3']])            # 8
                question.right_answer = request.form['answer']  # 8
                question.is_promoted = True                     # 8
                question.comment = request.form['comment']      # 8
                question.type = request.form['type']            # 8
                question.comp = request.form['comp']            # 8

                session.add(question)                           # 9
                session.commit()                                # 9
            else:
                question = session.query(Question).filter(Question.is_promoted == 0).first()  # 10
                session.delete(question)                                                      # 10
                session.commit()                                                              # 10

        param = fill_dict(       # 11
            title='Просмотр вопросов',
            style=os.listdir(config["PATH"]['to_css'] + 'styleForCheckQuests/'),
            path_for_style=config["PATH"]['to_css'] + 'styleForCheckQuests/',
            style_mobile=config["PATH"]['to_css_mobile'] + 'styleForCheckQuests.css',
            categories=session.query(Category).all(),
            quest=session.query(Question).filter(Question.is_promoted == 0).first())

        if param['quest']:                                                                   # 12
            temp = param['quest'].answers.split('!@#$%')                                     # 12
            form.text.default = param['quest'].text                                          # 12
            form.answer.default = temp[0]                                                    # 12
            form.comment.default = param['quest'].comment                                    # 12
            form.category.choices = [(x.name, x.name) for x in param['categories'][1:]]      # 12
            form.category.default = param['quest'].orm_with_category.name                    # 12
            form.wrong_answer1.default = temp[1]                                             # 12
            form.wrong_answer2.default = temp[2]                                             # 12
            form.wrong_answer3.default = temp[3]                                             # 12
            return render_template('check_quests.html', form=form, **param, formLogin=loginForm, formRegister=registerForm)    # 13
        else:
            return ''' 
                <script>
                    alert('Нет вопросов для модерации!');
                    document.location.href = "/adminka";
                </script>
                '''        # 14
    else:
        return redirect('/login')      # 15


'''
    Страница выбора игры.
    1. Проверка была ли начата игра текущим пользователем, 
если у текущего пользователя есть незаконченная игра, то он будет должен ее доиграть
    2. Создание словаря для работы с переменными в html коде
        'title'            - Заголовок страницы
        'style'            - Названия файлов, в которых храняться стили для данной страницы
        'path_for_style'   - Путь к папке со стилямии
        'style_for_mobile' - Путь к файлу с css стилями для мобильного устройства
    3. Рендеринг
'''
@application.route('/change_play/')
def change_play():
    if return_to_game():                  # 1
        return redirect('/current_game')  # 1

    registerForm = RegisterForm()
    loginForm = LoginForm()

    param = fill_dict(  # 2
        title='Выбор игры',
        style=os.listdir(config["PATH"]['to_css'] + 'styleForChangePlay/'),
        path_for_style=config["PATH"]['to_css'] + 'styleForChangePlay/',
        style_mobile=config["PATH"]['to_css_mobile'] + 'styleForChangePlayMobile.css')

    return render_template('change_play.html', **param, formLogin=loginForm, formRegister=registerForm)   # 3


'''
    Страница выбора игры.
    1. Проверка была ли начата игра текущим пользователем, 
если у текущего пользователя есть незаконченная игра, то он будет должен ее доиграть
    2. Подключение к базе данных
    3. Создание словаря для работы с переменными в html коде
        'title'            - Заголовок страницы
        'style'            - Названия файлов, в которых храняться стили для данной страницы
        'path_for_style'   - Путь к папке со стилями
        'style_for_mobile' - Путь к файлу с css стилями для мобильного устройства
        'new'              - Новость
    4. Рендеринг
'''
@application.route('/news/<int:id_>')
def one_new(id_):
    if return_to_game():                   # 1
        return redirect('/current_game')   # 1

    session = db_session.create_session()  # 2

    registerForm = RegisterForm()
    loginForm = LoginForm()

    new = session.query(News).filter(News.id == id_).first()

    param = fill_dict(                     # 3
        title='Новость',
        style=os.listdir(config["PATH"]['to_css'] + 'styleForOneNew/'),
        path_for_style=config["PATH"]['to_css'] + 'styleForOneNew/',
        style_mobile=config["PATH"]['to_css_mobile'] + 'styleForOneNewMobile.css',
        new={'caption': new.caption,
             'text': new.text.split('!@#$%')[1],
             'small_caption': new.text.split('!@#$%')[0],
             'image': new.image})

    return render_template('one_new.html', **param, formLogin=loginForm, formRegister=registerForm)  # 4


@application.route('/send_message', methods=['POST', 'GET'])
def send_message():

    if current_user.is_authenticated and current_user.state == 'admin':

        registerForm = RegisterForm()
        loginForm = LoginForm()

        param = fill_dict(  # 3
            title='Рассылка',
            style=os.listdir(config["PATH"]['to_css'] + 'styleForSendMessage/'),
            path_for_style=config["PATH"]['to_css'] + 'styleForSendMessage/',
            style_mobile=config["PATH"]['to_css_mobile'] + 'styleForsendMessageMobile.css')

        session = db_session.create_session()

        if request.method == 'POST':
            recipients = [[user.nickname, user.email] for user in session.query(User).filter(User.agree_newsletter == 1).all()]

            server = 'smtp.mail.ru'

            user = os.getenv("EMAIL")
            password = os.getenv("PASSWORD")

            text_message = request.form['text_message']
            text = ''
            sender = user
            subject = 'Откройте письмо! У нас для вас новость!'

            for recipient in recipients:

                with open(config['INFO']['message'], 'r', encoding='utf-8') as f:
                    html = f.read()

                html = html.replace('/n', '')
                html = html.replace('!@#$%name!@#$%', recipient[0])
                html = html.replace('!@#$%text!@#$%', text_message)

                msg = MIMEMultipart('alternative')
                msg['Subject'] = subject
                msg['From'] = 'NothingNowhereNowhen <' + sender + '>'
                msg['To'] = recipient[1]
                msg['Reply-To'] = sender
                msg['Return-Path'] = sender
                msg['X-Mailer'] = 'Python/' + (python_version())

                part_text = MIMEText(text, 'plain')
                part_html = MIMEText(html, 'html')

                if request.files.get('file_message'):
                    img = MIMEImage(request.files['file_message'].read())
                    msg.attach(img)

                msg.attach(part_text)
                msg.attach(part_html)

                mail = smtplib.SMTP_SSL(server)
                mail.login(user, password)
                mail.sendmail(sender,  recipient[1], msg.as_string())
                mail.quit()
            return redirect('/adminka')

        return render_template('send_message.html', **param, formLogin=loginForm, formRegister=registerForm)
    else:
        return redirect('/login')


'''
    Админка.
    1. Проверка зашёл ли админ
    2. Создание словаря для работы с переменными в html коде
        'title'            - Заголовок страницы
        'style'            - Названия файлов, в которых храняться стили для данной страницы
        'path_for_style'   - Путь к папке со стилямии
        'style_for_mobile' - Путь к файлу с css стилями для мобильного устройства
    3. Рендеринг
'''
@application.route('/adminka/')
def adminka():
    if current_user.is_authenticated and current_user.state == 'admin':  # 1
        registerForm = RegisterForm()
        loginForm = LoginForm()

        param = fill_dict(  # 2
            title='Админка',
            style=os.listdir(config["PATH"]['to_css'] + 'styleForAdminka/'),
            path_for_style=config["PATH"]['to_css'] + 'styleForAdminka/',
            style_mobile=config["PATH"]['to_css_mobile'] + 'styleForChangePlayMobile.css')

        return render_template('adminka.html', **param, formLogin=loginForm, formRegister=registerForm)   # 3
    return redirect('/')


@application.route('/admin_quests/')
def admin_quests():
    if current_user.is_authenticated and current_user.state == 'admin':  # 1

        registerForm = RegisterForm()
        loginForm = LoginForm()

        session = db_session.create_session()
        categories = session.query(Category).all()
        quests = session.query(Question).all()
        param = fill_dict(  # 2
            title='Редактировать вопросы',
            style=os.listdir(config["PATH"]['to_css'] + 'styleForAdminQuests/'),
            path_for_style=config["PATH"]['to_css'] + 'styleForAdminQuests/',
            style_mobile=config["PATH"]['to_css_mobile'] + 'styleForAdminQuestsMobile.css',
            categories=categories[1:],
            quests=[{'id': x.id,
                     'text': x.text,
                     'comment': x.comment,
                     'category': x.orm_with_category.name,
                     'images': x.images,
                     'answer': x.right_answer,
                     'wrong_answer1': x.answers.split('!@#$%')[1],
                     'wrong_answer2': x.answers.split('!@#$%')[2],
                     'wrong_answer3': x.answers.split('!@#$%')[3],
                     'type': config['TYPE_QUESTION'][str(x.type)],
                     'comp': config['COMP_QUESTION'][str(x.complexity)]} for x in quests])

        return render_template('admin_quests.html', **param, formLogin=loginForm, formRegister=registerForm)   # 3
    return redirect('/')


@application.route('/admin_users/')
def admin_users():
    if current_user.is_authenticated and current_user.state == 'admin':  # 1

        session = db_session.create_session()

        registerForm = RegisterForm()
        loginForm = LoginForm()

        users = session.query(User).all()
        param = fill_dict(  # 2
            title='Редактировать пользователей',
            style=os.listdir(config["PATH"]['to_css'] + 'styleForAdminUsers/'),
            path_for_style=config["PATH"]['to_css'] + 'styleForAdminUsers/',
            style_mobile=config["PATH"]['to_css_mobile'] + 'styleForAdminUsersMobile.css',
            users=[{'id': x.id,
                    'nickname': x.nickname,
                    'name': x.name,
                    'surname': x.surname,
                    'email': x.email,
                    'rating': x.rating,
                    'start_date': x.start_date,
                    'state': config['ADMIN_STATE'][x.state],
                    'all_games': x.all_games,
                    'wins': x.wins,
                    'defeats': x.defeats,
                    'link_vk': x.link_vk,
                    'avatar': x.avatar,
                    'agree_newsletter': x.agree_newsletter} for x in users])

        return render_template('admin_users.html', **param, formLogin=loginForm, formRegister=registerForm)   # 3
    return redirect('/')


@application.route('/admin_add_news/', methods=['POST', 'GET'])
def admin_add_news():
    if current_user.is_authenticated and current_user.state == 'admin':  # 1

        session = db_session.create_session()

        registerForm = RegisterForm()
        loginForm = LoginForm()

        param = fill_dict(  # 2
            title='Добавить новость',
            style=os.listdir(config["PATH"]['to_css'] + 'styleForAdminAddNews/'),
            path_for_style=config["PATH"]['to_css'] + 'styleForAdminAddNews/',
            style_mobile=config["PATH"]['to_css_mobile'] + 'styleForAdminNewMobile.css')

        if request.method == 'POST':
            new = News()
            new.caption = request.form['main_input_header_admin_add_news']
            new.text = request.form['input_header_admin_add_news'] + '!@#$%' + request.form['input_admin_add_news']

            session.add(new)
            session.commit()

            if request.files.get('file'):
                f = request.files['file']
                new.image = f'/static/img/news/{new.id}.png'
                with open(new.image[1:], 'wb') as f1:
                    f1.write(f.read())
            else:
                new.image = ''
            session.commit()

        return render_template('admin_add_news.html', **param, formLogin=loginForm, formRegister=registerForm)
    return redirect('/')


@application.route('/check_edit_or_show_quest/<id_>', methods=['POST', 'PUT', 'GET', 'DELETE'])
@login_required
def check_edit_or_show_quest(id_):
    if current_user.state == 'admin':
        if request.method == 'PUT':
            return requests.put(config['PATH']['href'] + f'/api/{ os.getenv("TOKEN") }/quests/' + id_, data=request.form, files=request.files).json()
        elif request.method == 'DELETE':
            return requests.delete(config['PATH']['href'] + f'/api/{ os.getenv("TOKEN") }/quests/' + id_).json()
        elif request.method == 'GET':
            return requests.get(config['PATH']['href'] + f'/api/{ os.getenv("TOKEN") }/questions').json()
    if request.method == 'POST':
         return requests.post(config['PATH']['href'] + f'/api/{ os.getenv("TOKEN") }/add_quest', data=request.form, files=request.files).json()


@application.route('/check_edit_or_show_users/<id_>', methods=['POST', 'PUT', 'GET', 'DELETE'])
def check_edit_or_show_users(id_):
    if current_user.is_authenticated and current_user.state == 'admin':
        if request.method == 'PUT':
            return requests.put(config['PATH']['href'] + f'/api/{ os.getenv("TOKEN") }/put_user/' + id_, data=request.form, files=request.files).json()
        elif request.method == 'DELETE':
            return requests.delete(config['PATH']['href'] + f'/api/{ os.getenv("TOKEN") }/delete_user/' + id_).json()
        elif request.method == 'GET':
            return requests.get(config['PATH']['href'] + f'/api/{ os.getenv("TOKEN") }/users').json()
    if request.method == 'POST':
        return requests.post(config['PATH']['href'] + f'/api/{ os.getenv("TOKEN") }/add_user', data=request.form, files=request.files).json()

''' 
    Запуск приложения. Сайт открывается на http://127.0.0.1:5000/ 
    ИЛИ на сайте https://nothing-nowhere-nowhen.ru
'''

#application.run()
