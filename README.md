Расчет минимального адреса хоста подсети для IP-адресов версии IPv4.

Временная сложность стремится к O(n), информация о времени выполнения функции размещена в time.py

Запуск приложения локально:

1. Вариант
- virtualenv --python=python3.6 venv
- source venv/bin/activate
- pip install -r requirements.txt
- python run.py --file ip_list.txt --ip_version ipv4

  Запуск тестов:
 - python -m unittest -v tests.py

2. Вариант

- virtualenv --python=python3.6 venv
- source venv/bin/activate

  Установка модуля:
- pip install --editable .
- 
  Запуск модуля:
- run --file ip_list.txt --ip_version ipv4


В приложении:

- в файле run.py находятся основные функции и класс для расчетов
- в файле setup.py находятся настройки для setuptools
- в файле ip_list.txt находятся примеры IP-адресов IPv4
- в файле ip_list_test.txt находятся примеры IP-адресов IPv6 и некорректного адреса для тестирования

Приложение ведет подсчет адресов по умолчанию с маской 24. Можно передать маску сети после IP-адреса в формате /25, подсчет будет вестись по указанной маске.
