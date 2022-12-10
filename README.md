# Локальный запуск:
```
git clone https://github.com/qutoq/online_test.git
```
Перейти в online_test/

Установка используемых библиотек:
```
pip install -r requirements.txt
```
Запуск локального сервера:

```
python3 manage.py migrate --run-syncdb
python3 manage.py createsuperuser
python3 manage.py runserver
```
Теперь можно создавать тесты в admin панели и проходить их на главной странице.
