# tournament
Tournament

* Скачать GAE SDK https://cloud.google.com/appengine/downloads
* Распаковать архив в выбранные каталог
* Рядом развернуть virtualenv и склонировать репозиторий
* Активировать виртуальное окружение
* Установить flask: pip install -r tournament/requirements.txt -t tournament/lib


Запуск тестов

* pip install webtest
* pip install mock
* tournament/run_tests.py google_appengine tournament/application/tests
