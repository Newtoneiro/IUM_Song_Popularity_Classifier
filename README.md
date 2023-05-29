# Projekt IUM

## Preview

[ium_preview.webm](https://github.com/Newtoneiro/IUM_Song_Popularity_Classifier/assets/79006719/a8bf2cc0-dd04-4857-b16d-42f1fba1a522)

![Screenshot_2023-05-29-12:59:53](https://github.com/Newtoneiro/IUM_Song_Popularity_Classifier/assets/79006719/8fa4b759-e509-42a9-964a-cd44a43c7068)

![Screenshot_2023-05-29-12:59:40](https://github.com/Newtoneiro/IUM_Song_Popularity_Classifier/assets/79006719/3a7acdba-30df-46b7-a006-111d830c6ebe)

## Uruchomienie programu z testem AB

Aby uruchomić program należy wykonać następujące kroki:

1. Zainstalować zależności z pliku `requirements.txt` (najlepiej wirtualne środowisko)
2. Wywołać komendę `python3 rest_api.py` w katalogu głównym projektu
3. Wysłać zapytanie do endpointu `localhost:8888/predict`

## Uruchomenie programu wizualizującego modele

Aby uruchomić program należy wykonać następujące kroki:

1. Zainstalować zależności z pliku `requirements.txt` (najlepiej wirtualne środowisko)
2. Wywołać komendę `streamlit run app.py` w katalogu głównym projektu
3. W przeglądarce internetowej powinna otworzyć się strona z aplikacją

## Treść zadania

“Nasz serwis zarabia wtedy, gdy ludzie słuchają muzyki. Jeśli nie wiemy ile czasu będą słuchali jej w przyszłości, to trudno nam rozliczać się z artystami i negocjować z nimi stawki”

## Kontekst zadania

Portal "Pozytywka" opłaca artystów, których utwory są następnie udostępniane użytkownikom portalu. W zależności od tego, jak chętnie słuchane są utwory danego wykonawcy muzycznego - administratorzy portalu mogą regulować stawki z artystami. Dobrze prosperujący artyści mogą dostać premię, a ci mniej popularni - wręcz przeciwnie. "Pozytywka" zbiera dane od użytkowników portalu i przechowuje takie informacje, jak czas słuchania utworów artystów, akcję odsłuchania utworu, polubienia oraz pominięcia go.

## Zdefiniowane zadania

Zadanie polega na stworzeniu modelu, na podstawie którego klient będzie mógł ustalać warunki kontraktów z artystami oraz ocenić, którzy z nich są chętnie, a którzy mniej chętnie słuchani. Kluczowe będą danę reprezentujące szereg czasowy sumarycznych czasów słuchania wykonawcy w danym tygodniu.

Na tej podstawie klient będzie mógł we własnym zakresie ustalać stawki dla dobrze prosperujących artystów.

Na potrzeby kryteriów biznesowych i analitycznych zakładamy, że płatność dla artysty jest realizowana na kolejny interwał czasowy - czyli co tydzień.

## Dane wejściowe i wyjściowe

Dane wejściowe będą reprezentowały kolejne interwały czasowe - dane historyczne wraz ze średnim czasem słuchania wykonawcy obliczanym na podstawie długości utworu związanego z akcjami oraz rodzajem akcji. W prostej wersji, będzie to po prostu liczba akcji PLAY w danym tygodniu pomnożona przez czas trwania utworu związanego z akcją. W bardziej zaawansowanej wersji, być może lepiej będzie zachowywać się model, dla którego pod uwagę weźmiemy również akcje SKIP (np. jest to odjęcie od całego czasu słuchania połowy długości utworu związanego z akcją SKIP - ponieważ średnio tyle piosenki jest pomijane.).

Model regresji będzie przewidywać X_t+1 średni czas słuchania utworu na podstawie szeregu czasowego postaci [X_0, X_1, ... X_t],
gdzie X_n oznacza średni czas słuchania wykonawcy w okresie n.

## Model naiwny

Model naiwny, który będzie stanowił projektowy 'baseline', od którego będziemy później wychodzić to prosta regresja liniowa. Jest to słaby model, nie biorący pod uwagę okresowości ani innych ukrytych zależności między okresami, ale przez to stanowi dobry punkt odniesienia. Jeżeli nie uda nam się stworzyć modelu przebijającego model naiwny pod względem jakości - to możliwe, że dane są błędne albo zadanie należy sformułować w inny sposób.

Model naiwny, jego wizualizację i miary jakości można znaleźć w pliku naive_model.ipynb.

## Definicja celów biznesowych

Celem biznesowym jest optymalizacja kosztów opłacania artystów muzycznych. Lepiej prosperujący artyści muzyczni dostaną premię za zasługi dla portalu "Pozytywka", a koszty przeznaczane na tych mniej słuchanych zostaną ograniczone, przez co będzie je można przeznaczyć na innych, bardziej opłacalnych wykonawców. Model powinien działać na bieżąco, a jego wyniki powinny być użyte do podejmowania decyzji biznesowych.

## Kryteria sukcesu

### Kryterium biznesowe

- Optymalizacja kosztów przeznaczanych na opłacanie artystów udostępniających swoje utwory w serwisie "Pozytywka"
- Ułatwienie podejmowania decyzji dotyczących artystów na podstawie wyników modelu (promowanie dobrze prosperujących wykonawców, których średni czas słuchania wzrasta)

### Weryfikacja spełnienia kryteriów

- Testy A/B - Dzielimy wszystkich artystów na dwie podgrupy - decyzję o opłacaniu pierwszej podejmujemy na podstawie starego systemu, a drugiej na podstawie naszego modelu. Następnie analizujemy wydatki w obydwu grupach i porównujemy je ze sobą, co pozwoli nam na ocenę jakości naszego modelu.

### Opis zadań modelowania

W ramach tego zadania analitycznego zajmujemy się przewidywaniem średniego czasu słuchania artysty udostępniającego swoje dzieła dla portalu "Pozytywka" w przyszłości, na podstawie danych zebranych w pewnym okresie czasu. Naszym celem jest przewidzenie średniego czasu słuchania utworów artysty w kolejnym okresie czasu (będącym okresem wyznaczania stawek dla artysty).

Na podstawie dostępnych danych, po ich obróbce i wyekstraktowaniu cech charakterystycznych dla artystów w okresie czasu (średni czas słuchania oszacowany na podstawie akcji PLAY i SKIP w danym okresie) i z użyciem modeli regresyjnych - będziemy dokonywać przewidywania, na podstawie których portal "Pozytywka" będzie mógł zadecydować, czy dany artysta jest wart inwestycji.

### Analityczne kryteria sukcesu

Analitycznym kryterium sukcesu jest stworzenie modelu o miarach jakości lepszych od modelu naiwnego. Dla stworzonego modelu naiwnego oznacza to osiągnięcie modelu regresji o MSE <= 1669.4069131874119. Jest to miara łatwa w sprawdzaniu, w związku z czym będzie dobrym wyznacznikiem spełnienia oczekiwań analitycznych.

# Model LSTM

Do realizacji zadania zdecydowaliśmy się wykorzystać model LSTM, ze względu na to, że idealnie pasuje do naszego zadania - przewidywania szeregów czasowych. Pamięć krótkotrwała i długotrwała pozwalają w sposób precyzyjny przewidywać średni czas słuchania wykonawcy muzycznego w kolejnych interwałach czasowych.

Do stworzenia modelu wykożystaliśmy `tf.keras.Sequential()` z biblioteki tf.keras. Przed wytrenowaniem modelu przystąpiliśmy do optymalizacji hiperparametrów przy pomocy biblioteki keras_tuner. Wykorzystana została metoda siatki hiperparametrów, która na potrzeby naszego projektu - okazała się wystarczająco dobra. Po następnym wytrenowaniu modelu z hiperparametrami osiągniętymi dzięki hipersiatce, otrzymaliśmy satysfakcjonujący nas model, którego porównanie z modelem naiwnym zostało przedstawione na końcu pliku `lstm_model.ipynb`.

# Podsumowanie Projektu

Pierwszym zadaniem projektowym było zapoznanie się ze środowiskiem otaczającym zadanie, wcielenie się w role klienta i opisanie wstępnego planu działania oraz kryteriów biznesowych. Dokładniej opisane one zostały w częściach im poświęconym w tym pliku.

Odrębną częścią projektu była analiza danych - najpierw były to dane błędne, niepełne i zaszumione, które należało wymienić na inne, o wyższej jakości. Po otrzymaniu poprawnych danych wejściowych, przeprowadzona została ich analiza dostępna w pliku `data_analysys.ipynb`. Analiza danych pozwoliła nam na sformułowanie wstępnej wizji modelu - jego danych wejściowych i wyjściowych oraz stworzenie prostego modelu naiwnego stanowiącego baseline do porównywania postępu w projekcie. Poszczególne części zostały omówione dokładniej w poprzednich częściach tego pliku. Tym sposobem zakończyliśmy pierwszy etap projektu.

Drugi etap projektu rozpoczęliśmy od stworzenia modelu mającego na celu przebicie modelu naiwnego. Zadanie to wymagało stworzenia obiektu DataProvider - odpowiedzialnego za ładowanie i preprocessing danych jak i operacje dzielenia zbioru danych na treningowy i testowy. Po wytrenowaniu modelu, ustaleniu wartości hiperparametrów i wizualizacji wyników byliśmy gotowi na stworzenie mikroserwisu prezentującego postęp. Początkowo zdecydowaliśmy się na wizualizację danych w czasie rzeczywistym za pomocą biblioteki streamlit. Przedstawione działanie programu można obejrzeć przez załączony plik mp4. Następnie przeszliśmy do implementacji mikroserwisu, pozwalającego na przeprowadzenie eksperymentów A/B, który dzielił przychodzące zapytania na dwie podgrupy oraz rejestrował dane wejściowe wraz z wynikami. Po kilku drobniejszych poprawkach zakończyliśmy etap drugi, kończąc tym samym projekt IUM.
