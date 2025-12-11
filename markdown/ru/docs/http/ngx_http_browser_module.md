# Модуль ngx_http_browser_module

**Revision:** 2  
**Language:** ru


Модуль `ngx_http_browser_module` создаёт переменные,
значения которых зависят от значения поля **User-Agent**
в заголовке запроса:

***$modern_browser***  
  равна значению, заданному директивой ,
если браузер опознан как современный;
***$ancient_browser***  
  равна значению, заданному директивой ,
если браузер опознан как устаревший;
***$msie***  
  равна “1”, если браузер опознан как MSIE любой версии.

## Пример конфигурации {#example}

Выбор индексного файла:

```
modern_browser_value "modern.";

modern_browser msie      5.5;
modern_browser gecko     1.0.0;
modern_browser opera     9.0;
modern_browser safari    413;
modern_browser konqueror 3.0;

index index.${modern_browser}html index.html;
```

Перенаправление для старых браузеров:

```
modern_browser msie      5.0;
modern_browser gecko     0.9.1;
modern_browser opera     8.0;
modern_browser safari    413;
modern_browser konqueror 3.0;

modern_browser unlisted;

ancient_browser Links Lynx netscape4;

if ($ancient_browser) {
    rewrite ^ /ancient.html;
}
```

## Директивы {#directives}


строка ...

http
server
location


Задаёт подстроки, при нахождении которых в поле User-Agent
заголовка запроса браузер считается устаревшим.
Специальная строка “netscape4” соответствует
регулярному выражению “^Mozilla/[1-4]”.




строка
1
http
server
location


Задаёт значение для переменных $ancient_browser.




браузер версия
unlisted

http
server
location


Задаёт версию браузера, начиная с которой он считается современным.
В качестве браузера можно задать msie,
gecko (браузеры, созданные на основе Mozilla),
opera, safari
или konqueror.



Версии можно задать в форматах X, X.X, X.X.X или X.X.X.X.
Максимальные значения для каждого из форматов соответственно —
4000, 4000.99, 4000.99.99 и 4000.99.99.99.



Специальное значение unlisted указывает считать
современным браузер, не описанный директивами modern_browser
и .
В противном случае неперечисленный браузер будет считаться устаревшим.
Если в заголовке запроса нет поля User-Agent, то браузер
считается неперечисленным.




строка
1
http
server
location


Задаёт значение для переменных $modern_browser.


