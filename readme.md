python -m venv /path/to/new/virtual/environment
pip install django
django-admin startproject mysite
python manage.py startapp myapp

pip freeze > requirements.txt  
pip install -r requirements.txt
python manage.py createsuperuser

VSCode Django https://code.visualstudio.com/docs/python/tutorial-django

Вопросы для собесов:
Паттерн
ООП
ACID SOLID Нормализация БД
SOLID https://medium.com/webbdev/solid-4ffc018077da
https://habr.com/ru/companies/productivity_inside/articles/505430/
МэжикМетоды
СинглТон
ЧериПик
Каталог паттернов проектирования https://refactoring.guru/ru/design-patterns/catalog

34 урок
Нормализация БД
Декоратор классом 34 методы инит , колл
Полиморфизм

пример сайта для уроков
https://edu-python-course.github.io/blog-bootstrap/templates/blogpost.html
https://edu-python-course.github.io/_build/html/uk/appx/blog.html#challenge-templates

Урок 1
https://github.com/PonomaryovVladyslav/PythonCources/blob/master/lesson28.md
https://www.exlab.net/tools/sheets/regexp.html
https://regex101.com/
./pic/regexp.png

https://bool.dev/blog/detail/vizualizatsiya-poleznykh-git-komand
https://learngitbranching.js.org/?locale=ru_RU

Урок 2
https://github.com/PonomaryovVladyslav/PythonCources/blob/master/lesson29.md
https://docs.djangoproject.com/en/2.2/ref/templates/builtins/
Домашнее задание / Практика
Создать базовую html от которой будут наследоваться все остальные
Для статических урлов сделать html файлы наследующиеся от базового, но с разным текстом (можно и оформлением)

Для
урлов http://127.0.0.1:8000/article/<int:article_number>, http://127.0.0.1:8000/article/<int:article_number>/<slug:slug_text>,
Сделать html файлы в которых выводить текст о том чётный введен или нечётный article_number (логику прописать в
темплейтах),
если введён slug_text, выводить этот текст при помощи include в добавочной html (добавленной из отдельного файла).

На главной странице (http://127.0.0.1:8000/) сделать две ссылки, перейти на случайную статью (id), и перейти
на случайную статью со случайным слагом (5-10 случайных символов)

На всех страницах внизу должна быть ссылка на главную.

https://www.educative.io/answers/how-to-generate-a-random-string-in-python

How to manage static files (e.g. images, JavaScript, CSS)¶
https://docs.djangoproject.com/en/4.1/howto/static-files/

Урок 3 ОРМ
Создать два пользователя через createsuperuser
При помощи shell создать две категории постов, 5 постов в разных категориях (2 и 3, например), создать 5-7 комментариев
к постам, хотя бы один пост оставить без коментариев
Реализовать такие страницы как: '/', /<slug:slug>/
На главной странице, должен отображаться список всех блогов, название каждого должно быть ссылкой на страницу с
подробностями о блоге
На странице с подробностями, должны отображаться детали поста, и все комментарии написанные к этому посту
Дополнительная информация:
Если сложно разобраться со слагами, то реализуйте сначала урл который будет принимать id вместо слага, а только потом
добавте еще один уже для слага
Генерацию слага удобнее всего разместить в методе save.

Урок 4 Формы и юзер

    Пишем страницы для логина и для регистрации (на каждой из них должна быть ссылка на другую)
    Если пользователь не залогинен, то его должно перебрасывать на страницу с логином
    Добавляем в верхнюю часть главной страницы перечисление существующих топиков. При нажатии на которые мы должны видеть отфильтрованый список блогов, только относящихся к выбранному топику (гет запрос)
    Добавляем строку для поиска по блогам. После поиска должны отображаться посты в названии которых есть частичное совпадение без учета регистра с искомыми данными.(гет форма)
    Добавляем возможность создания поста.
    На странице с деталями поста добавляем возможность писать комментарии.

Урок 5
классы https://ccbv.co.uk/

