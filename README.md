# Kackers-blockchained-notes (scores:919)
> We found a strange service with secrets that use blockchain-like technology.
Evil kackers use it to store their secrets, maybe u can find something interesting.
>> Hint:Next secret is chained to previous,
link to next secret contains current location and current secret (except first step)
---
# Solution:
```
git clone https://github.com/Slonser/Kackers-blockchained-notes.git && cd Kackers-blockchained-notes
pip install requests
sudo python3 -m pip install bs4
python3 script.py
```
## RU:
* На сайте http://tasks.open.kksctf.ru:20005/ мы должны ввести в input,такой текст,у которого последние 4 символа md5 hash такие же как и на картинке.
* Картинка с капптчей генерируеться скриптом captcha.php
* Замечаем скрытое поле `<input name="hash" value="079688177962f99daf7c0e6d83f0cf77" type="hidden">`,в нем видим md5 hash,расшифровываем его.
* Расшифровав hash мы увидим что это 4 символа с картинки.
* Напишем [скрипт](script_gen.py) на питоне,который сгенерирует все возможные четырёх символные последовательности из символов `0123456789abcdef`.
Для удобвства сохраним все последовательности в базу данных.
* Теперь когда у нас есть база данных мы можем написать скрипт который будет делать запрос на сайт и перебор будет искать такую строку x,
что md5(x)[28::]=hash
  * С помощью библиотеки requests ***создаем сессию***,если мы будем посылать все запросы к сайту без сессии,то у нас ничего не выйдет.
  * Делаем GET запрос к начальной странице,получаем значение hash,находим его в нашей базе данных,извлекаем значение последних символов
  * Пишим "глупый" перебор,он заключаеться в том,что мы берем ASCII символы с кодами от 33 до 121,и вычисляем хэши всех их последовательностей(s * 1,s * 2,...s * seed),
  где сид 5000(можно снизить до ~3000).В таком случае мы получаем 445 000 разных md5 хэшей,один из них будет точно будет оканчиваться на нашу последовательность
  * Отправляем POST запрос и получаем страницу с секретом.
  * Парсим её и вынимаем 'секрет'.
  * Страница с новой каптчей находиться по адресу md5(текущей ссылка + 'секрет')
  * Повторяем процесс до тех пор,пока в консоли не увидим `k k s lbrace d0 _ u _ r34lly _ l1k3 _ w3b _ bl0ckCh4in _ T3ch`
  * Приводим флаг к формату соревнования
 * Флаг - `kks{d0_u_r34lly_l1k3_w3b_bl0ckCh4in_T3ch}`
