# RU
<p align="center"><b>MikuPlay alpha 0.1.8 "Первый ПОИСК будущего"</b></p>
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

Смотрите в файле `requirements.txt`.

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

<summary>alpha 0.1.8 "Первый ПОИСК будущего" (15.12.2024)</summary>

Второе обновление, включающее в себя:
* Улучшена логика добавления треков.
* Изменена логика замены треков.
* Добавлена проверка на тип файла (поддерживаются только mp3) при добавлении и замене треков.
* Добавлена логика обрезки сообщения со списком полученных треков для избежания проблем с его отправкой.
* Улучшен поиск треков через инлайн-режим.
* Добавлен расширенный поиск треков через диалог с ботом (можно узнать айди трека из базы данных, его название и исполнителя, не открывая саму базу данных).
* Предварительно добавлены меню магазина и профиля в главное меню.
* Улучшено логирование.
* Функции администраторов помещены в отдельное меню.
* В меню администратора добавлена возможность получить ID своего профиля, текущего чата и файлов (фото, видео, музыка, голосовые сообщения, стикеры и т. д.).
* Изменена логика получения ответов для ИИ: теперь не обязательно указывать имя при обращении к ней, можно ответить на любое сообщение бота.
* Изменён текст отправки запроса юзера к ИИ.
* Изменён контекст ИИ.
* Изменено меню помощи: дисклеймер и DMCA помещены в отдельные меню в нём.


</details>
<details>

<summary>alpha 0.1.7 fix 2 "Первый текст будущего" (03.12.2024)</summary>

Второй фикс первого обновления, включающий в себя:
* Добавлено и убрано логирование в некоторых местах.


</details>
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
<p align="center"><b>MikuPlay alpha 0.1.8 "The first SEARCH of the future"</b></p>
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

See in the file `requirements.txt`.

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

<summary>alpha 0.1.8 "The first SEARCH of the future" (15.12.2024)</summary>

The second update, which includes:
* Improved the logic for adding tracks.
* Changed the logic of replacing tracks.
* Added file type checking (only mp3 is supported) when adding and replacing tracks.
* Added logic for cropping a message with a list of received tracks to avoid problems with sending it.
* Improved track search via inline mode.
* Added advanced track search via the bot dialog (you can find out the track ID from the database, its name and artist without opening the database itself).
* Pre-added store and profile menus to the main menu.
* Improved logging.
* Admin functions are placed in a separate menu.
* Added the ability to get the ID of your profile, current chat, and files (photos, videos, music, voice messages, stickers, etc.) in the admin menu.
* Changed the logic for getting answers for AI: now you don't have to specify a name when accessing it, you can reply to any bot message.
* Changed the text of sending a user's request to the AI.
* The AI context has been changed.
* Changed the help menu: disclaimer and DMCA are placed in separate menus in it.


</details>
<details>

<summary>alpha 0.1.7 fix 2 "The first text of the future" (03.12.2024)</summary>

The second fix of the first update, which includes:
* Added and removed logging in some places.


</details>
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
