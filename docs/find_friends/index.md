# **Aplikacja Find Friends**

Zapraszam do zapoznania się z moim projektem aplikacji **Find Friends**.<br>

<a href="https://find-friends-v4.streamlit.app/" class="md-button md-button--primary" target="_blank" rel="noopener noreferrer">Find Friends</a>

Ta aplikacja została stworzona w celu dopasowywania użytkownika do grupy osób o podobnych cechach i zainteresowaniach na podstawie prostego formularza ankietowego.<br>
W praktyce działa jak mini system rekomendacji znajomości wykorzystujący klasteryzację danych.

![alt text](find_friends.png)


### **Funkcjonalności aplikacji**


#### 1. Formularz użytkownika (sidebar)
Po lewej stronie aplikacji użytkownik wprowadza informacje o sobie:
        
        * wiek
        * poziom wykształcenia
        * ulubione zwierzęta
        * ulubione miejsce
        * płeć

Dane są wybierane za pomocą komponentów:
   
        * selectbox
        * radio

Następnie dane są zapisywane do obiektu `DataFrame` (`person_df`).<br>


#### 2. Wczytanie modelu ML<br>
Aplikacja ładuje wcześniej wytrenowany model klasteryzacji: `load_model(MODEL_NAME)`.<br>
Model został zapisany wcześniej przy pomocy biblioteki PyCaret.<br>

Do optymalizacji wykorzystano `@st.cache_data`.<br>
Dzięki temu model nie jest ładowany przy każdym odświeżeniu i aplikacja działa szybciej.


#### 3. Predykcja klastra użytkownika<br>
Model analizuje dane użytkownika `predict_model(model, data=person_df)` i przypisuje go do odpowiedniego klastra.<br>
Każdy klaster posiada nazwę i opis, które są pobierane z pliku JSON `welcome_survey_cluster_names_and_descriptions_v2.json`.

Te informacje zostały zapisane tam wcześniej z wykorzystaniem skryptu do automatycznego generowania nazw i opisów klastrów utworzonych przez model ML.<br>
W tym celu została użyta biblioteka `PyCaret` i wytrenowany model klasteryzacji `K-Means`.


Poniżej zamieszczam do wglądu pliki z klasteryzacji i nazywania klastrów.<br>

<a href="clustering.html" class="md-button" target="_blank" rel="noopener noreferrer">clustering</a>
<a href="clusters_naming.html" class="md-button" target="_blank" rel="noopener noreferrer">clusters_naming</a>


#### 4. Analiza osób z tego samego klastra<br>
**Aplikacja:**

        * wczytuje pełny zbiór uczestników
        * przypisuje klastry wszystkim osobom
        * filtruje osoby należące do tego samego klastra co użytkownik
    
`same_cluster_df = all_df[all_df["Cluster"] == predicted_cluster_id]`


#### 5. Statystyki grupy
Wyświetlana jest liczba osób w danym klastrze:<br>
`st.metric("Liczba Twoich znajomości w tym klastrze:", len(same_cluster_df))`

![alt text](find_friends_same_cluster.png)


#### 6. Wizualizacja danych
Aplikacja generuje histogramy pokazujące rozkład cech w grupie:<br>
    
        * wieku
        * wykształcenia
        * ulubionych zwierząt
        * ulubionych miejsc
        * płci

Wykresy są tworzone przy pomocy `Plotly`

![alt text](find_friends_age.png)
`fig = px.histogram(same_cluster_df.sort_values("age"), x="age")`

![alt text](find_friends_edu_level.png)
`fig = px.histogram(same_cluster_df.sort_values("edu_level"), x="edu_level")`

![alt text](find_friends_fav_animals.png)
`fig = px.histogram(same_cluster_df.sort_values("fav_animals"), x="fav_animals")`

![alt text](find_friends_fav_place.png)
`fig = px.histogram(same_cluster_df.sort_values("fav_place"), x="fav_place")`

![alt text](find_friends_gender.png)
`fig = px.histogram(same_cluster_df.sort_values("gender"), x="gender")`


### **Wykorzystane technologie**

1. **Streamlit**
        
        * st.sidebar
        * st.selectbox
        * st.metric
        * ...

2. **Pandas**
        
        * pd.read_csv()
        * pd.DataFrame()
        * ...

3. **PyCaret**
        
        * load_model()
        * predict_model()

4. **Plotly**
        
        * px.histogram()

5. **JSON**

5. **CSV**

### **Link GitHub**
<a href="https://github.com/kbierko/find_friends_v4" class="md-button" target="_blank" rel="noopener noreferrer">:simple-github: Find Friends</a>

<br>
Poniżej zamieszczam do wglądu plik app.py

<a href="app.py" class="md-button">Pobierz plik app.py</a>