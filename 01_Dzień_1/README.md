![Coders-Lab-1920px-no-background](https://user-images.githubusercontent.com/152855/73064373-5ed69780-3ea1-11ea-8a71-3d370a5e7dd8.png)


## Zadanie 1 &ndash; przygotowanie projektu &ndash; rozwiązywane z wykładowcą.

1. Zapoznaj się z projektem `project`. Zajrzyj do pliku **settings.py**:
* sprawdź, nazwę bazy danych, której używa ten projekt,
* załóż bazę o odpowiedniej nazwie w PostgreSQL,
* wykonaj pierwszą migrację.

2. Skonfiguruj system szablonów. Skorzystaj z wiedzy z prezentacji i ustaw:
* BACKEND na `django.template.backends.django.DjangoTemplates`
* DIRS ustaw tak, aby wszystkie szablony znajdowały się w katalogu **/templates** w folderze aplikacji (nie projektu).

3. Wykonaj komendę: `python manage.py populateschool` i zapoznaj się z zawartością bazy danych wykorzystywanej podczas 
ćwiczeń.

## Zadanie 2 &ndash; szablon bazowy &ndash; rozwiązywane z wykładowcą.

1. Zapoznaj się z widokiem `SchoolView` w pliku **views.py**. Znajdziesz tam zmienną HTML, 
która przechowuje wygląd strony. Utwórz na jej podstawie szablon bazowy dla całej aplikacji. 
Od teraz, ilekroć będziesz tworzył nowy szablon dla zadań ze "szkoły", powinieneś dziedziczyć z tego szablonu bazowego.

2. Zmodyfikuj widok `SchoolView` tak, aby HTML z wyglądem strony był ładowany z szablonu. 
Szablon ten powinien dziedziczyć po szablonie bazowym.

## Zadanie 3 &ndash; lista uczniów

Zapoznaj się z widokiem `SchoolClassView`. Sprawdź w pliku **urls.py**, w jaki sposób ten widok jest udostępniany 
w aplikacji.  Napisz szablon, który zaprezentuje listę uczniów w pokazywanej klasie.

W kodzie widoku znajduje się mały błąd. Czy potrafisz go znaleźć?

**Podpowiedź:** do renderowania danych kontekstowych użyj komend szablonów 
`{% for ... in ... %} ... {% endfor %}` i `{% if ... %} ... {% endif %}`

## Zadanie 4 &ndash; metryczka ucznia

Napisz widok, który udostępnisz pod URL-em `/student/{student_id}`, gdzie {student\_id} to identyfikator (klucz główny) 
ucznia. Widok powinien pokazywać metryczkę ucznia:

* imię,
* nazwisko,
* klasę.

Na dole strony dodaj listę wszystkich przedmiotów. Każdy przedmiot powinien być osobnym linkiem, 
który będzie przekierowywał użytkownika, do (nieistniejącego jeszcze) widoku `/grades/{student_id}/{subject_id}`, 
gdzie {student\_id} to identyfikator (klucz główny) ucznia, a {subject\_id} to identyfikator przedmiotu.

Napisaniem widoku `/grades...` zajmiemy się w następnym zadaniu.

## Zadanie 5 &ndash; oceny cznia

Napisz widok, który udostępnisz pod URL-em `/grades/{student_id}/{subject_id}`, gdzie `{student\_id}` to identyfikator
(klucz główny) ucznia, a `{subject\_id}` to identyfikator przedmiotu.

Widok powinien pokazać:
* nazwisko ucznia i jego klasę,
* nazwę przedmiotu i nazwisko nauczyciela,
* wszystkie oceny ucznia z danego przedmiotu,
* średnią ocen z danego przedmiotu.
