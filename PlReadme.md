<p align="center"><b>MikuPlay alpha 0.1.8 "Pierwsze WYSZUKIWANIE przyszłości"</b></p>
<p align="center">Kod źródłowy bota do szybkiego wyszukiwania i pobierania muzyki w TG z AI.</p>
<p align="center">Token API musi być przechowywany w pliku <tt>.env</tt>.</p>
<p align="center">Wszystkie funkcje bota są napisane po rosyjsku.</p>

<p align="center">
    <img src="/assets/ava.jpeg" width="300px" height="300px"/>
</p>

<p align="center">
    <a href="EngReadme.md"><img src="/assets/eng.png" width="30px" height="30px"/></a>
    <a href="README.md"><img src="/assets/ru.png" width="30px" height="30px"/></a>
    <a href="PlReadme.md"><img src="/assets/pl.png" width="30px" height="30px"/></a>
</p>

<p align="center">Utworzono przy użyciu:</p>
<p align="center"><img src="https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white"/> <tt>Bot API 7.10</tt></p> 
<p align="center"><img src="https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54"/> <tt>Aiogram 3.x</tt></p>
<p align="center"><img src="https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white"/> <tt>Aiosqlite 0.20.0</tt></p>
<p align="center"><img src="https://img.shields.io/badge/Visual%20Studio%20Code-0078d7.svg?style=for-the-badge&logo=visual-studio-code&logoColor=white"/> <tt>Najnowsza wersja</tt></p>
<p align="center"><img src="https://img.shields.io/badge/chatGPT-74aa9c?style=for-the-badge&logo=openai&logoColor=white"/> <tt>GPT-4o</tt></p>
<p align="center"><img src="https://img.shields.io/badge/google-4285F4?style=for-the-badge&logo=google&logoColor=white"/> <tt>Gemini API</tt></p>

## Informacje
<details>

<summary>Funkcje (zaimplementowane i planowane, mogą ulec zmianie)</summary>

- [x] Wyszukiwanie utworów inline;
- [x] Dodawanie plików audio (do kilkudziesięciu lub 100 sztuk jednocześnie);
- [x] Zastępowanie plików audio oraz ich informacji;
- [x] Edytowanie informacji o dodanym pliku audio w bazie danych (Artysta, tytuł. Nie zmienia informacji w samym pliku MP3.);
- [x] Usuwanie utworu z wyników wyszukiwania;
- [x] Dodawanie administratorów;
- [x] Usuwanie administratorów;
- [ ] Tworzenie osobistych playlist;
- [x] AI z tożsamością Miku.

</details>
<details>

<summary>Wymagane biblioteki do działania</summary>

Zobacz w pliku `requirements.txt`.

</details>
<details>

<summary>Licencja</summary>

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

## Historia wersji
<details>

<summary>alpha 0.1.8 "Pierwsze WYSZUKIWANIE przyszłości" (15.12.2024)</summary>

Druga aktualizacja, która zawiera:
* Ulepszono logikę dodawania utworów.
* Zmieniono logikę zastępowania utworów.
* Dodano sprawdzanie typu plików (tylko mp3 są obsługiwane) przy dodawaniu i zastępowaniu utworów.
* Dodano logikę skracania wiadomości z listą otrzymanych utworów, aby uniknąć problemów z jej wysyłaniem.
* Ulepszono wyszukiwanie utworów poprzez tryb inline.
* Dodano zaawansowane wyszukiwanie utworów przez dialog bota (możesz poznać ID utworu z bazy danych, jego tytuł oraz artystę bez otwierania bazy danych).
* Wstępnie dodano menu sklepu i profilu do głównego menu.
* Ulepszono logowanie.
* Funkcje administratora umieszczono w osobnym menu.
* Dodano możliwość uzyskania ID twojego profilu, bieżącego czatu oraz plików (zdjęcia, filmy, muzyka, wiadomości głosowe, naklejki itd.) w menu administratora.
* Zmieniono logikę uzyskiwania odpowiedzi od AI: teraz nie trzeba podawać imienia przy dostępie, można odpowiedzieć na dowolną wiadomość bota.
* Zmieniono tekst wysyłania zapytania użytkownika do AI.
* Zmieniono kontekst AI.
* Zmieniono menu pomocy: klauzula zrzeczenia się odpowiedzialności oraz DMCA zostały umieszczone w osobnych menu.


</details>
<details>

<summary>alpha 0.1.7 fix 2 "Pierwszy tekst przyszłości" (03.12.2024)</summary>

Druga poprawka pierwszej aktualizacji, która zawiera:
* Dodano i usunięto logowanie w niektórych miejscach.


</details>
<details>

<summary>alpha 0.1.7 fix 1 "Pierwszy tekst przyszłości" (25.11.2024)</summary>

Pierwsza poprawka pierwszej aktualizacji, w tym:
* Nieznacznie zmieniono kontekst AI oraz dane wysyłania zapytania do Gemini API;
* Dodano link do GitHub projektu w menu.


</details>
<details>

<summary>alpha 0.1.7 "Pierwszy tekst przyszłości" (29.10.2024)</summary>

Pierwsza aktualizacja, która zawiera:
* AI z tożsamością Miku oparte na Gemini API;
* Możliwość resetowania historii dialogu z AI;
* Ulepszono wyszukiwanie za pomocą biblioteki <code>re</code>;
* Inne zmiany i usprawnienia interakcji użytkownika z menu oraz tekstem.


</details>
<details>

<summary>alpha 0.1.6 "Pierwszy dźwięk przyszłości" (24.10.2024)</summary>

Pierwsza publicznie wydana wersja z podstawową funkcjonalnością:
* Wyszukiwanie utworów inline;
* Dodawanie plików audio (do kilkudziesięciu lub 100 sztuk jednocześnie);
* Zastępowanie plików audio oraz ich informacji;
* Edytowanie informacji o dodanym pliku audio w bazie danych (Artysta, tytuł. Nie zmienia informacji w samym pliku MP3.);
* Usuwanie utworu z wyników wyszukiwania;
* Dodawanie administratorów;
* Usuwanie administratorów.
