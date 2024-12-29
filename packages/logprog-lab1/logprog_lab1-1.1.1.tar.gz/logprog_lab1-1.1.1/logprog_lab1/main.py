import abc

class Value(abc.ABC):
    @abc.abstractmethod
    def out(self):
        pass

    @abc.abstractmethod
    def sum(self):
        pass

    @abc.abstractmethod
    def all(self):
        pass

    @staticmethod
    def parse(string: str):
        string = string.strip()
        if string.startswith("(") and string.endswith(")"):
            string = string[1:-1]
        balance = 0
        coma = -1
        for i in range(len(string)):
            if string[i] == "(":
                balance += 1
            elif string[i] == ")":
                balance -= 1
            elif balance == 0 and string[i] == ",":
                coma = i
                break
        if coma == -1:
            try:
                return Atom(float(string))
            except:
                print("Ошибка: недопустимое число")
                return None
        else:
            left = Value.parse(string[:coma].strip())
            right = Value.parse(string[coma + 1:].strip())
            if left is None or right is None:
                return None
            return Pair(left, right)

class Atom(Value):
    def __init__(self, number):
        self.number = number

    def out(self):
        print(self.number, end="")

    def sum(self):
        return self.number

    def all(self):
        return [self.number]

class Pair(Value):
    def __init__(self, left: Value, right: Value):
        self.left = left
        self.right = right

    def out(self):
        print('(', end='')
        self.left.out()
        print(", ", end='')
        self.right.out()
        print(')', end='')

    def sum(self):
        return self.left.sum() + self.right.sum()

    def all(self):
        return self.left.all() + self.right.all()

def average(value):
    atoms = value.all()
    if len(atoms) == 0:
        return 0
    return sum(atoms) / len(atoms)

def getDeviation(value):
    atoms = value.all()
    avg = average(value)
    deviations = [abs(atom - avg) for atom in atoms]
    return min(deviations), max(deviations)

def run(string):
    parsedValue = Value.parse(string)

    if parsedValue is None:
        print("Парсинг не удался.")
        return

    print("Распарсенное значение: ", end='')
    parsedValue.out()
    print()

    print(f"Сумма всех атомов: {parsedValue.sum()}")
    avg = average(parsedValue)
    print(f"Среднее значение атомов: {avg}")
    minDev, maxDev = getDeviation(parsedValue)
    print(f"Минимальное отклонение: {minDev}")
    print(f"Максимальное отклонение: {maxDev}")

def main():
    number = 1
    tests = [
        "(2.5, (3.5, 4.5))",
        "(1.0, (2.0, (3.0, 4.0)))",
        "((1.5, 2.5), (3.5, 4.5))",
        "(10.0, 20.0)",
        "5.0",
        # Ошибочные сценарии
        "(2.35, (6.5, 1.5",
        "(2.5, (семь, 4.5))",
        "",
        "(2.5, , 4.5)"
    ]

    for test in tests:
        print(f"Тест №{number}")
        print(f"Строка ввода: {test}")
        run(test)
        number += 1
        print()

main()
