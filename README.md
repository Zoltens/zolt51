Инструкция для связки Gunicorn + Nginx + Django:

1. Установка Nginx:  


    sudo apt install nginx

2. Установка Gunicorn:  


    pip install gunicorn
3. Создание файлa сокета Gunicorn:


    sudo nano /etc/systemd/system/gunicorn.socket  

Внутри файла прописываем:  


    [Unit]  
    Description=gunicorn socket

    [Socket]  
    ListenStream=/run/gunicorn.sock

    [Install]  
    WantedBy=sockets.target
4. Создание служебного файлв gunicorn.service:  


    sudo nano /etc/systemd/system/gunicorn.service  

Внутри прописываем:  
    

    [Unit]  
    Description=gunicorn daemon
    Requires=gunicorn.socket
    After=network.target


    [Service]  
    User=sammy # указывается имя пользователя
    WorkingDirectory=/home/sammy/myprojectdir # путь до директории с файлом manage.py
    ExecStart=/home/sammy/myprojectdir/myprojectenv/bin/gunicorn \ # путь до файла gunicorn в виртуальном окружении
          --access-logfile - \
          --workers 3 \
          --bind unix:/run/gunicorn.sock \
          myproject.wsgi:application

    [Install]  
    WantedBy=multi-user.target

5. Запуск и активация сокета Gunicorn:  


    sudo systemctl start gunicorn.socket  
    sudo systemctl enable gunicorn.socket

6. Проверка состояния процесса:  


    sudo systemctl status gunicorn.socket

В случае ошибок проверьте журнал:  


    sudo journalctl -u gunicorn.socket

7. Тест механизма активации сокета:  


    curl --unix-socket /run/gunicorn.sock localhost

Выводимые данные приложения должны отобразиться в терминале в формате HTML. Это показывает, что Gunicorn запущен и 
может обслуживать ваше приложение Django. Вы можете убедиться, что служба Gunicorn работает, с помощью следующей 
команды:  

    sudo systemctl status gunicorn
Если есть проблемы проверьте журнал:  

    sudo journalctl -u gunicorn

8. Настройка Nginx как прокси для Gunicorn:  

Для начала создаем серверный блок:  

    sudo nano /etc/nginx/sites-available/myproject # вместо myproject указываем название проекта
Внутри файла прописываем:  

    server {
        listen 80;
        server_name server_domain_or_IP; # указываем имя домена или IP
    
        location = /favicon.ico { access_log off; log_not_found off; }
        location /static/ {
            root /home/sammy/myprojectdir; # путь до папки static в проекте
        }
    
        location / {
            include proxy_params;
            proxy_pass http://unix:/run/gunicorn.sock;
        }
    }

Сохраняем и закрываем файл, после чего привязываем его к каталогу sites-enabled:  

    sudo ln -s /etc/nginx/sites-available/myproject /etc/nginx/sites-enabled

Тестируем конфигурацию Nginx на ошибки синтаксиса:

    sudo nginx -t

Если ошибок не будет найдено, перезапускаем Nginx с помощью следующей команды:  

    sudo systemctl restart nginx
Нам нужна возможность открыть брандмауэр для обычного трафика через порт 80. Поскольку нам больше не потребуется 
доступ к серверу разработки, мы можем удалить правило для 8000:  

    sudo ufw delete allow 8000
    sudo ufw allow 'Nginx Full'
Теперь есть возможность перейти к домену или IP-адресу нашего сервера для просмотра нашего приложения.