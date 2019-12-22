# Проект "Simple votings"

### Цель
Предоставить пользователю сервис, на котором можно быстро создать голосование и собрать мнения пользователей касательно какого-либо вопроса

### Технологический стек:
- python 3.6
- django 3.0+
- sqlite 3.22+

### Инструкция по настройке проекта:
1. Склонировать проект
2. Открыть проект в PyCharm с наcтройками по умолчанию
3. Создать виртуальное окружение (через settings -> project "simple votings" -> project interpreter)
4. Открыть терминал в PyCharm, проверить, что виртуальное окружение активировано.
5. Обновить pip:
```bash
pip install --upgrade pip
```
6. Установить в виртуальное окружение необходимые пакеты: 
```bash
pip install -r requirements.txt
```
7. Синхронизировать структуру базы данных с моделями: 
```bash
python manage.py migrate
```
8. Создать суперпользователя
```bash
$ python manage.py createsuperuser                                                                                                                                                                                                                                
Username (leave blank to use 'prom'):
Email: 1@abc.net
Password: promprog
Password (repeat): promprog
```
9. Создать конфигурацию запуска в PyCharm (файл `manage.py`, опция `runserver`)
