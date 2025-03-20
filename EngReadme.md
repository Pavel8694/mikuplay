<p align="center"><b>MikuPlay alpha 0.1.8 "The first SEARCH of the future"</b></p>
<p align="center">Source code of the bot for quick search and download of music in TG with AI.</p>
<p align="center">The API token must be stored in the <tt>.env</tt> file.</p>
<p align="center">All functions in the bot are written in Russian.</p>

<p align="center">
    <img src="/assets/ava.jpeg" width="300px" height="300px"/>
</p>

<p align="center">
    <a href="EngReadme.md"><img src="/assets/eng.png" width="30px" height="30px"/></a>
    <a href="README.md"><img src="/assets/ru.png" width="30px" height="30px"/></a>
    <a href="PlReadme.md"><img src="/assets/pl.png" width="30px" height="30px"/></a>
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
