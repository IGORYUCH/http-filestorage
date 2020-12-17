# http-filestorage

# Установка и запуск
Скачайте файлы приложения
```
git clone https://github.com/IGORYUCH/http-filestorage.git
```
Перейдите в папку приложения
```
cd http-filestorage
```
Создайте виртуальную среду
```
python3 -m venv filestorageenv
```
Активируйте виртуальную среду
```
source /filestorageenv/bin/activate
```
Установите flask и gunicorn
```
pip3 install flask gunicorn
```
Скопируйте filestorage.services в каталог системы служб linux
```
sudo cp filestorage.services /etc/systemd/system/filestorage.servise
```
Откройте файл /etc/systemd/system/filestorage.servise
```
sudo vim /etc/systemd/system/filestorage.servise
```
В нем будет содержимое:
```
[Service]
user=username
Group=www-data
WorkingDirectory=/home/username/filestorage
Environment="PATH=/home/username/filestorage/filestorageenv/bin"
ExecStart=/home/username/filestorage/filestorageenv/bin/gunicorn -w 2 -b 0.0.0.0:8080 wsgi:app
```
* user поменяйте имя пользователя на своего
* WorkingDirectory поменяйте на путь, в который скачано приложение
* Environment поменяйте на путь вашей виртуальной среды
* ExecStart поменяйте на путь в который установился gunicorn в виртуальной среде

Запустите службу 
```
sudo systemctl start filestorage
```
Активируйте запуск службы при старте системы
```
sudo systemctl enable filestorage
```
Проверте состояние запущенной службы
```
sudo systemctl status filestorage
```
Вывод команды при успешном запуске
```
● filestorage2.service - Gunicorn instance to server filestorage
   Loaded: loaded (/etc/systemd/system/filestorage2.service; enabled; vendor preset: enabled)
   Active: active (running) since Thu 2020-12-17 23:15:56 CST; 50min ago
 Main PID: 481 (gunicorn)
 ```
# Использование

Загрузить файл
```
files = {filename: (filename, file_stream, 'multipart/form-data')}
result = requests.post('http://{0}/api/file/upload'.format(HOSTNAME), files=files)
```
Скачать файл
```
headers = {'Hash': 'file hash'}
result = requests.delete('http://{0}/api/file/delete'.format(HOSTNAME), headers=headers)
```
Удалить файл
```
headers = {'Hash':'file hash'}
result = requests.get('http://{0}/api/file/download'.format(HOSTNAME), headers=headers)
```
# Тесты
Установите pytest для запуска тестов
 ```
 pip3 install pytest
  ```
Выполните тесты командой
 ```
 pytest -v test_filestorage.py
 ```
 Результат выполнения тестов
 ```
test_filestorage.py::test_upload_hash_returned PASSED                                                                                       [ 16%]
test_filestorage.py::test_download_file_returned PASSED                                                                                     [ 33%]
test_filestorage.py::test_delete_deleted_file_hash_returned PASSED                                                                          [ 50%]
test_filestorage.py::test_download_not_exists_returned PASSED                                                                               [ 66%]
test_filestorage.py::test_upload_exists_returned PASSED                                                                                     [ 83%]
test_filestorage.py::test_delete_not_exists_returned PASSED                                                                                 [100%]
```
