# Projekt IUM

## Treść zadania

“Nasz serwis zarabia wtedy, gdy ludzie słuchają muzyki. Jeśli nie wiemy ile czasu będą słuchali jej w przyszłości, to trudno nam rozliczać się z artystami i negocjować z nimi stawki”

## Kontekst zadania

Portal "Pozytywka" opłaca artystów, których utwory są następnie udostępniane użytkownikom portalu. W zależności od tego, jak chętnie słuchane są utwory danego wykonawcy muzycznego - administratorzy portalu mogą regulować stawki z artystami. Dobrze prosperujący artyści mogą dostać premię, a ci mniej popularni - wręcz przeciwnie. "Pozytywka" zbiera dane od użytkowników portalu i przechowuje takie zdarzenia jak odtworzenie utworu, polubienie utworu oraz pominięcie go. Na podstawie tych akcji można wyznaczyć model przewidujący rokowania artysty muzycznego w przyszłości i odpowiednie regulowanie stawki.

## Zdefiniowane zadania

Zadanie polega na stworzeniu modelu służącego do sklasyfikowania artysty / zespołu na podstawie interakcji użytkowników z jego utworami. Kluczowe będą akcje pominięcia, polubienia jak i samego odtworzenia utworu. Ważną rolę odegra także średni czas słuchania wykonawcy. Model będzie klasyfikować artystę na jedną z 3 kategorii:

- dobrze prosperujący
- średnio prosperujący
- słabo prosperujący
  które pozwolą następnie administratorom serwisu "Pozytywka" określić stawki dla tak sklasyfikowanych grup artystów.

## Model naiwny

Model naiwny w przypadku naszego zadania to model, który dla każdego artysty zwraca taką samą wartość - będzie to wartość "średnio prosperujący". Taki model uśrednia wydatki na artystów i nie faworyzuje dobrych zespołów, ale też nie odcina tych słabszych.

## Definicja celów biznesowych

Celem biznesowym jest optymalizacja kosztów opłacania artystów muzycznych. Lepiej prosperujący artyści muzyczni dostaną premię za zasługi dla portalu "Pozytywka", a koszty przeznaczane na tych mniej słuchanych zostaną ograniczone, przez co będzie je można przeznaczyć na innych, bardziej opłacalnych wykonawców. Model powinien działać na bieżąco, a jego wyniki powinny być użyte do podejmowania decyzji biznesowych.

## Kryteria sukcesu

### Kryterium biznesowe

- Optymalizacja kosztów przeznaczanych na opłacanie artystów udostępniających swoje utwory w serwisie "Pozytywka"
- Ułatwienie podejmowania decyzji dotyczących artystów na podstawie wyników modelu (promowanie dobrze prosperujących wykonawców)

### Weryfikacja spełnienia kryteriów

- Testy A/B - Dzielimy wszystkich artystów na dwie podgrupy - decyzję o opłacaniu pierwszej podejmujemy na podstawie starego systemu, a drugiej na podstawie naszego modelu. Następnie analizujemy wydatki w obydwu grupach i porównujemy je ze sobą, co pozwoli nam na ocenę jakości naszego modelu.

### Opis zadań modelowania

W ramach tego zadania analitycznego zajmujemy się klasyfikacją artystów udostępniających swoje dzieła dla portalu "Pozytywka" na podstawie danych zebranych w pewnym okresie czasu. Naszym celem jest określenie, czy artysta jest warty inwestycji, czy raczej powinniśmy obciąć koszty z nim związane.
Na podstawie dostępnych danych, po ich obróbce i wyekstraktowaniu cech charakterystycznych dla artystów w okresie czasu (liczba akcji PLAY, LIKE, SKIP związanych z ich utworami) i z użyciem modeli klasyfikacyjnych - będziemy dokonywać przewidywania, czy dany artysta jest wart inwestycji.

### Analityczne kryteria sukcesu

Analityczne kryterium sukcesu jest silnie związane z danymi offline dostarczonymi przez klienta. Jest określone grono zespołów, które zawsze warto opłacać, bo ich muzyka jest ponadczasowa i chętnie słuchana przez większość użytkowników serwisu. Z drugiej strony, jest masa artystów, którzy dopiero zaczynają swoją przygodę muzyczną lub mają bardzo wąskie grono fanów i jest bardzo mało prawdopodobne, że kiedyś zyskają na popularności.
Proponowany przez nas model naiwny każdemu artyście przyporządkowuje te samą klasę, a co za tym idzie - każdy z nich dostaje tę samą wypłatę i jest tak samo promowany. Naszym analitycznym kryterium sukcesu będzie stworzenie modelu, który optymalizuje koszty lepiej niż model naiwny. Dla uproszczenia można przyjąć, że zależy nam na otrzymaniu predykcji z błędem nie przekraczającym arbitralnie dobranym parametrem alfa (Przyjmijmy alfa = 80%).

Skuteczność modelu można obliczać w sposób następujący:

- Pomijamy ostatni interwał danych dla wybranego artysty
- Wrzucamy w model n - 1 danych dotyczących kolejnych interwałów czasowych i otrzymujemy predykcję
- Na podstawie odrzuconego w predykcji interwału czasowego (reprezentującego przyszłość, a co za tym idzie - faktyczne prosperowania artysty) porównujemy otrzymaną predykcję z rzeczywistością w następujący sposób:
- Bierzemy ostatni interwał zawarty w danych wrzuconych w model - nazwijmy go t0, oraz odrzucony interwał reprezentujący przyszłość - t+1.
  Na podstawie akcji dotyczących artysty w interwale t0 i t+1 wyznaczamy score na podstawie wzoru (1 \* count(PLAY) + 3 \* count(LIKE) - 1 \* count(SKIP)). Od score t+1 odejmujemy t0 i dostajemy ostateczny score reprezentujący faktyczne prosperowania artysty.
- Następnie na podstawie wyliczonego score wyznaczamy faktyczną klasę artysty w sposób następujący:
- Jeżeli score <= - (liczba użytkowników powiązanych z akcjami) - słabo prosperujący (zanik słuchaczy)
- Jeżeli score <= (liczba użytkowników powiązanych z akcjami) - średnio prosperujący (stabilni słuchacze)
- Jeżeli score > (liczba użytkowników powiązanych z akcjami) - dobrze prosperujący (wzrost słuchaczy)

Takie zdefiniowanie obliczania skuteczności modelu pozwala nam na precyzyjne wyznaczanie jakości modelu na podstawie dostarczonych danych offline i porównywanie ich z modelem naiwnym.
