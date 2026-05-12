# **Aplikacja Audio Notes**

Zapraszam do zapoznania się z moim projektem aplikacji **Audio Notes**.<br>

Ta aplikacja to prosty system do tworzenia, transkrypcji, zapisywania i wyszukiwania notatek głosowych oparty o AI.

![alt text](audio_notes_home.png)

<a href="https://audionotes-karol.streamlit.app/" class="md-button md-button--primary" target="_blank" rel="noopener noreferrer">Audio Notes</a>


><span style="color:red">
WAŻNE!
</span> Do funkcjonowania aplikacji konieczny jest klucz API OpenAI.

### **Główne funkcjonalności aplikacji**
Aplikacja składa się z dwóch głównych zakładek: dodawanie notatek audio i wyszukiwanie notatek.

#### 1. Dodawanie notatek audio

**Użytkownik może:**<br>
* nagrać notatkę głosową bezpośrednio w przeglądarce,<br>
* odsłuchać nagranie,<br>
* wysłać nagranie do modelu Whisper od OpenAI,<br>
* otrzymać automatyczną transkrypcję mowy na tekst,<br>
* ręcznie edytować tekst notatki,<br>
* zapisać notatkę do bazy wektorowej.<br>

**Proces wygląda następująco:**<br>
* nagranie audio przez mikrofon<br>
* konwersja nagrania do formatu MP3<br>
* transkrypcja audio → tekst<br>
* wygenerowanie embeddingu tekstowego<br>
* zapis embeddingu i treści notatki w Qdrant Cloud<br>

![alt text](audio_notes_saving.png)

#### 2. Wyszukiwanie notatek audio

**Użytkownik może:**<br>
* wpisać dowolne zapytanie tekstowe,<br>
* wyszukać podobne semantycznie notatki,<br>
* zobaczyć trafność wyników (`score`).<br>

**Aplikacja wykorzystuje:**<br>
* embeddingi<br>
* wyszukiwanie semantyczne<br>
* similarity search<br>

Dzięki temu użytkownik może znaleźć notatkę nawet wtedy, gdy użyto innych słów o podobnym znaczeniu.

![alt text](audio_notes_search.png)

### **Wykorzystane technologie**

1. **Streamlit**
2. **OpenAI API**
    - model `whisper-1` (speech-to-text)
    - model `text-embedding-3-large`
3. **Qdrant**
4. **streamlit-audiorecorder**
5. **python-dotenv**

### **Elementy techniczne**

1. **Session state**<br>
Aplikacja wykorzystuje `st.session_state` do przechowywania audio, transkrypcji, klucza OpenAI.
2. **MD5 Hash**<br>
`current_md5 = md5(st.session_state["note_audio_bytes"]).hexdigest()`<br>
Służy do wykrywania zmiany nagrania i uniknięcia ponownej transkrypcji tego samego audio.
3. **Cache resource**<br>
`@st.cache_resource`<br>
Wykorzystywane dla klienta Qdrant.<br>
Dzięki temu połączenie z bazą nie jest tworzone wielokrotnie i aplikacja działa szybciej.

### **Link GitHub**
<a href="https://github.com/kbierko/audio_notes_v6_wdrozenie" class="md-button" target="_blank" rel="noopener noreferrer">:simple-github: Audio Notes</a>

<br>
Poniżej zamieszczam do wglądu plik app.py

<a href="app.py" class="md-button" target="_blank" rel="noopener noreferrer">Pobierz plik app.py</a>