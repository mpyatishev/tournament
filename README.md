# tournament
Tournament

* Скачать GAE SDK https://cloud.google.com/appengine/downloads
* Распаковать архив в выбранный каталог
* Рядом развернуть virtualenv и склонировать репозиторий
* Активировать виртуальное окружение
* Установить flask: pip install -r tournament/requirements.txt -t tournament/lib


Запуск тестов

* pip install webtest
* pip install mock
* tournament/run_tests.py google_appengine tournament/


Запуск

* google_appengine/dev_appserver.py --clear_datastore=yes --port=8081 tournament/
* python tournament/tournament.py
