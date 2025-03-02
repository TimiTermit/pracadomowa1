class Osoba:
    def __init__(self, imie, nazwisko):
        self.imie = imie
        self.nazwisko = nazwisko

    def przedstaw_sie(self):
        return f"Cześć, jestem {self.imie} {self.nazwisko}."


class Student(Osoba):
    def __init__(self, imie, nazwisko, kierunek):
        super().__init__(imie, nazwisko)
        self.kierunek = kierunek
        self.stan_psychiczny = "neutralny"
        self.glod = 0  

    def przedstaw_sie(self):
        return f"{super().przedstaw_sie()} Studiuję na kierunku {self.kierunek}. " \
               f"Mój stan psychiczny to: {self.stan_psychiczny}, a głód wynosi: {self.glod}."

    def jedz(self, ilosc):
        self.glod = max(0, self.glod - ilosc)
        print(f"{self.imie} zjadł(a) coś. Głód teraz wynosi: {self.glod}.")

    def zmien_stan_psychiczny(self, nowy_stan):
        self.stan_psychiczny = nowy_stan
        print(f"{self.imie} zmienił(a) stan psychiczny na: {self.stan_psychiczny}.")


class Nauczyciel(Osoba):
    def __init__(self, imie, nazwisko, przedmiot):
        super().__init__(imie, nazwisko)
        self.przedmiot = przedmiot
        self.stan_psychiczny = "neutralny"
        self.glod = 0  

    def przedstaw_sie(self):
        return f"{super().przedstaw_sie()} Uczę przedmiotu {self.przedmiot}. " \
               f"Mój stan psychiczny to: {self.stan_psychiczny}, a głód wynosi: {self.glod}."

    def jedz(self, ilosc):
        self.glod = max(0, self.glod - ilosc)
        print(f"{self.imie} zjadł(a) coś. Głód teraz wynosi: {self.glod}.")

    def zmien_stan_psychiczny(self, nowy_stan):
        self.stan_psychiczny = nowy_stan
        print(f"{self.imie} zmienił(a) stan psychiczny na: {self.stan_psychiczny}.")


if __name__ == "__main__":
    student = Student("Jan", "Kowalski", "Informatyka")
    nauczyciel = Nauczyciel("Anna", "Nowak", "Matematyka")

    print(student.przedstaw_sie())
    print(nauczyciel.przedstaw_sie())

    student.zmien_stan_psychiczny("szczęśliwy")
    student.glod = 5  
    student.jedz(3)   
    print(student.przedstaw_sie())

    nauczyciel.zmien_stan_psychiczny("zdenerwowany")
    nauczyciel.glod = 7  
    nauczyciel.jedz(4)   
    print(nauczyciel.przedstaw_sie())