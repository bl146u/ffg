# Finstar Financial Group: тестовая работа


## Версии используемого ПО

`Python 3.9.13`  
`Django 4.0.5`  
`Docker version 20.10.17, build 100c70180f`  
`Docker Compose version 2.6.0`  
`Manjaro Linux; Build ID: rolling`


## Запуск

Для упрощения запуска был создан `Makefile`
```
make containers_restart
```

После запуска веб-приложение будет доступно по ссылке http://localhost/. Так же доступна документация http://localhost/docs/ (она вообще не описана, только для того, чтобы посмотреть, какие API-методы существуют).


## Админка

Доступна по ссылке http://localhost/.  

Суперпользователь:  
`login`: admin  
`password`: admin

Тестовый пользователь:  
`login`: test  
`password`: admin

API реализован следующим образом: суперпользователю отдаются все данные, остальным только свои. Некоторые методы требуют GET-параметры: `date`, `from` и `to`.
