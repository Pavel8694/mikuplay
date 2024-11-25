# RU
<p align="center"><b>MikuPlay alpha 0.1.7 fix 1 "Первый текст будущего"</b></p>
<p align="center">Исходный код бота для быстрого поиска и скачивания музыки в TG с ИИ.</p>
<p align="center">API токен должен храниться в <tt>.env</tt> файле.</p>

<p align="center">
    <img src="/assets/ava.jpeg" width="300px" height="300px"/>
</p>

<p align="center">Создано при помощи:</p>
<p align="center"><img src="https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white"/> <tt>Bot API 7.10</tt></p> 
<p align="center"><img src="https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54"/> <tt>Aiogram 3.x</tt></p>
<p align="center"><img src="https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white"/> <tt>Aiosqlite 0.20.0</tt></p>
<p align="center"><img src="https://img.shields.io/badge/Visual%20Studio%20Code-0078d7.svg?style=for-the-badge&logo=visual-studio-code&logoColor=white"/> <tt>Последняя версия</tt></p>
<p align="center"><img src="https://img.shields.io/badge/chatGPT-74aa9c?style=for-the-badge&logo=openai&logoColor=white"/> <tt>GPT-4o</tt></p>
<p align="center"><img src="https://img.shields.io/badge/google-4285F4?style=for-the-badge&logo=google&logoColor=white"/> <tt>Gemini API</tt></p>

## Информация
<details>

<summary>Функции (реализованные и планируемые, может пополняться)</summary>

- [x] Inline-поиск треков;
- [x] Добавление аудио-файлов (вплоть до нескольких десятков или 100 штук за раз);
- [x] Замена аудио-файлов и их информации;
- [x] Редактирование сведений добавленного аудио-файла в БД (Исполнителя, название. Не меняет информацию в самом MP3 файле.);
- [x] Удаление трека из поисковой выдачи;
- [x] Добавление администраторов;
- [x] Разжалование администраторов;
- [ ] Создание личных плейлистов;
- [x] Нейросеть с личностью Мику.

</details>
<details>

<summary>Необходимые либы для работы</summary>

1. `aiofiles==24.1.0`
2. `aiogram==3.13.1`
3. `aiohappyeyeballs==2.4.3`
4. `aiohttp==3.10.10`
5. `aiosignal==1.3.1`
6. `aiosqlite==0.20.0`
7. `annotated-types==0.7.0`
8. `attrs==24.2.0`
9. `cachetools==5.5.0`
10. `certifi==2024.8.30`
11. `charset-normalizer==3.4.0`
12. `colorama==0.4.6`
13. `frozenlist==1.4.1`
14. `fuzzywuzzy==0.18.0`
15. `google-ai-generativelanguage==0.6.10`
16. `google-api-core==2.21.0`
17. `google-api-python-client==2.149.0`
18. `google-auth==2.35.0`
19. `google-auth-httplib2==0.2.0`
20. `google-generativeai==0.8.3`
21. `googleapis-common-protos==1.65.0`
22. `greenlet==3.1.1`
23. `grpcio==1.67.0`
24. `grpcio-status==1.67.0`
25. `httplib2==0.22.0`
26. `idna==3.10`
27. `Levenshtein==0.26.0`
28. `magic-filter==1.0.12`
29. `multidict==6.1.0`
30. `propcache==0.2.0`
31. `proto-plus==1.25.0`
32. `protobuf==5.28.3`
33. `pyasn1==0.6.1`
34. `pyasn1_modules==0.4.1`
35. `pydantic==2.9.2`
36. `pydantic_core==2.23.4`
37. `pyparsing==3.2.0`
38. `python-dotenv==1.0.1`
39. `python-Levenshtein==0.26.0`
40. `RapidFuzz==3.10.0`
41. `requests==2.32.3`
42. `rsa==4.9`
43. `SQLAlchemy==2.0.36`
44. `tqdm==4.66.5`
45. `typing_extensions==4.12.2`
46. `uritemplate==4.1.1`
47. `urllib3==2.2.3`
48. `yarl==1.15.5`

</details>
<details>

<summary>Лицензия</summary>

MIT License

Copyright (c) 2024 Meme Corp

Данная лицензия разрешает лицам, получившим копию данного программного обеспечения и сопутствующей документации (далее — Программное обеспечение), безвозмездно использовать Программное обеспечение без ограничений, включая неограниченное право на использование, копирование, изменение, слияние, публикацию, распространение, сублицензирование и/или продажу копий Программного обеспечения, а также лицам, которым предоставляется данное Программное обеспечение, при соблюдении следующих условий:

Указанное выше уведомление об авторском праве и данные условия должны быть включены во все копии или значимые части данного Программного обеспечения.

ДАННОЕ ПРОГРАММНОЕ ОБЕСПЕЧЕНИЕ ПРЕДОСТАВЛЯЕТСЯ «КАК ЕСТЬ», БЕЗ КАКИХ-ЛИБО ГАРАНТИЙ, ЯВНО ВЫРАЖЕННЫХ ИЛИ ПОДРАЗУМЕВАЕМЫХ, ВКЛЮЧАЯ ГАРАНТИИ ТОВАРНОЙ ПРИГОДНОСТИ, СООТВЕТСТВИЯ ПО ЕГО КОНКРЕТНОМУ НАЗНАЧЕНИЮ И ОТСУТСТВИЯ НАРУШЕНИЙ, НО НЕ ОГРАНИЧИВАЯСЬ ИМИ. НИ В КАКОМ СЛУЧАЕ АВТОРЫ ИЛИ ПРАВООБЛАДАТЕЛИ НЕ НЕСУТ ОТВЕТСТВЕННОСТИ ПО КАКИМ-ЛИБО ИСКАМ, ЗА УЩЕРБ ИЛИ ПО ИНЫМ ТРЕБОВАНИЯМ, В ТОМ ЧИСЛЕ, ПРИ ДЕЙСТВИИ КОНТРАКТА, ДЕЛИКТЕ ИЛИ ИНОЙ СИТУАЦИИ, ВОЗНИКШИМ ИЗ-ЗА ИСПОЛЬЗОВАНИЯ ПРОГРАММНОГО ОБЕСПЕЧЕНИЯ ИЛИ ИНЫХ ДЕЙСТВИЙ С ПРОГРАММНЫМ ОБЕСПЕЧЕНИЕМ.

</details>

## История версий
<details>

<summary>alpha 0.1.7 fix 1 "Первый текст будущего" (25.11.2024)</summary>

Первый фикс первого обновления, включающий в себя:
* Немного изменён контекст ИИ и данные отправки запроса к Gemini API;
* Добавлена ссылка на GitHub проекта в меню.


</details>
<details>

<summary>alpha 0.1.7 "Первый текст будущего" (29.10.2024)</summary>

Первое обновление, включающее в себя:
* ИИ с личностью Мику на основе Gemini API;
* Возможность сбросить историю диалога с ИИ;
* Улучшенный поиск с помощью либы `re`;
* Прочие правки и улучшения взаимодействия пользователя с меню и текстом.


</details>
<details>

<summary>alpha 0.1.6 "Первый звук будущего" (24.10.2024)</summary>

Самая первая публично выпущенная версия с базовым функционалом:
* Inline-поиск треков;
* Добавление аудио-файлов (вплоть до нескольких десятков или 100 штук за раз);
* Замена аудио-файлов и их информации;
* Редактирование сведений добавленного аудио-файла в БД (Исполнителя, название. Не меняет информацию в самом MP3 файле.);
* Удаление трека из поисковой выдачи;
* Добавление администраторов;
* Разжалование администраторов.

</details>

# EN
<p align="center"><b>MikuPlay alpha 0.1.7 fix 1 "The first text of the future"</b></p>
<p align="center">Source code of the bot for quick search and download of music in TG with AI.</p>
<p align="center">The API token must be stored in the <tt>.env</tt> file.</p>
<p align="center">All functions in the bot are written in Russian.</p>

<p align="center">
    <img src="/assets/ava.jpeg" width="300px" height="300px"/>
</p>

<p align="center">Created using:</p>
<p align="center"><img src="https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white"/> <tt>Bot API 7.10</tt></p> 
<p align="center"><img src="https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54"/> <tt>Aiogram 3.x</tt></p>
<p align="center"><img src="https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white"/> <tt>Aiosqlite 0.20.0</tt></p>
<p align="center"><img src="https://img.shields.io/badge/Visual%20Studio%20Code-0078d7.svg?style=for-the-badge&logo=visual-studio-code&logoColor=white"/> <tt>Latest version</tt></p>
<p align="center"><img src="https://img.shields.io/badge/chatGPT-74aa9c?style=for-the-badge&logo=openai&logoColor=white"/> <tt>GPT-4o</tt></p>
<p align="center"><img src="https://img.shields.io/badge/google-4285F4?style=for-the-badge&logo=google&logoColor=white"/> <tt>Gemini API</tt></p>

## Information
<details>

<summary>Functions (implemented and planned, can be updated)</summary>

- [x] Inline-search tracks;
- [x] Adding audio files (up to several dozen or 100 pieces at a time);
- [x] Replacing audio files and their information;
- [x] Edit information about the added audio file in the database (Artist, name. Doesn't change the information in the MP3 file itself.);
- [x] Deleting a track from the search results;
- [x] Adding administrators;
- [x] Deleting administrators;
- [ ] Creating personal playlists;
- [x] AI with the Miku identity.

</details>
<details>

<summary>Required libs for operation</summary>

1. `aiofiles==24.1.0`
2. `aiogram==3.13.1`
3. `aiohappyeyeballs==2.4.3`
4. `aiohttp==3.10.10`
5. `aiosignal==1.3.1`
6. `aiosqlite==0.20.0`
7. `annotated-types==0.7.0`
8. `attrs==24.2.0`
9. `cachetools==5.5.0`
10. `certifi==2024.8.30`
11. `charset-normalizer==3.4.0`
12. `colorama==0.4.6`
13. `frozenlist==1.4.1`
14. `fuzzywuzzy==0.18.0`
15. `google-ai-generativelanguage==0.6.10`
16. `google-api-core==2.21.0`
17. `google-api-python-client==2.149.0`
18. `google-auth==2.35.0`
19. `google-auth-httplib2==0.2.0`
20. `google-generativeai==0.8.3`
21. `googleapis-common-protos==1.65.0`
22. `greenlet==3.1.1`
23. `grpcio==1.67.0`
24. `grpcio-status==1.67.0`
25. `httplib2==0.22.0`
26. `idna==3.10`
27. `Levenshtein==0.26.0`
28. `magic-filter==1.0.12`
29. `multidict==6.1.0`
30. `propcache==0.2.0`
31. `proto-plus==1.25.0`
32. `protobuf==5.28.3`
33. `pyasn1==0.6.1`
34. `pyasn1_modules==0.4.1`
35. `pydantic==2.9.2`
36. `pydantic_core==2.23.4`
37. `pyparsing==3.2.0`
38. `python-dotenv==1.0.1`
39. `python-Levenshtein==0.26.0`
40. `RapidFuzz==3.10.0`
41. `requests==2.32.3`
42. `rsa==4.9`
43. `SQLAlchemy==2.0.36`
44. `tqdm==4.66.5`
45. `typing_extensions==4.12.2`
46. `uritemplate==4.1.1`
47. `urllib3==2.2.3`
48. `yarl==1.15.5`

</details>
<details>

<summary>License</summary>

MIT License

Copyright (c) 2024 Meme Corp

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

</details>

## Version history
<details>

<summary>alpha 0.1.7 fix 1 "The first text of the future" (25.11.2024)</summary>

First fix of the first update, including:
* Slightly changed the AI context and data for sending a request to the Gemini API;
* Added a link to the project's GitHub in the menu.


</details>
<details>

<summary>alpha 0.1.7 "The first text of the future" (29.10.2024)</summary>

The first update that includes:
* AI with Miku's identity based on the Gemini API;
* Ability to reset the dialog history with AI;
* Improved search with the `re`library;
* Other edits and improvements to the user's interaction with the menu and text.


</details>
<details>

<summary>alpha 0.1.6 "The first sound of the future" (24.10.2024)</summary>

The very first publicly released version with basic functionality:
* Inline-search tracks;
* Adding audio files (up to several dozen or 100 pieces at a time);
* Replacing audio files and their information;
* Edit information about the added audio file in the database (Artist, name. Doesn't change the information in the MP3 file itself.);
* Deleting a track from the search results;
* Adding administrators;
* Deleting administrators.

</details>
