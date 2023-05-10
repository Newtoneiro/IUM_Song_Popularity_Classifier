# Projekt IUM

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
