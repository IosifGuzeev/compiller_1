from dataclasses import dataclass
from typing import List
from copy import copy
from collections import deque


@dataclass(init=True, repr=True)
class infNet:  # информация о нетерменале.
    Net: str  # сам нетерминал
    countAlt: int   # количество альернатив
    firstN: int  # номер первой альтерантивы в списке правил


# задали грамматику
LR: str = "ABBTTMMM"  # левые части правил
RR: List[str] = ["!B!", "T+B", "T", "M", "M*T", "a", "b", "(B)"]  #правые части правил
m: int = 4
inf: List[infNet] = [infNet('A',1,0), infNet('B',2,1), infNet('T',2,3),infNet('M',3,5)]
T: str = "!+*ab()"  # знаки которыми можно пользоваться


@dataclass
class elemL1:
    term: str = ''  # флаг терминальный или нет
    symv: str = ''  # символ
    nAlt: int = 0   # номер альтернатив
    countAlt: int = 0  # количество альтерантив

@dataclass
class elemL2:
    term: str = ''
    symv: str = ''


# зададим стеки
L1: List[elemL1] = []
x: elemL1 = elemL1()
L2: List[elemL2] = []
y: elemL2 = elemL2()
result: List[int] = []
sos: str = ''  # состояния  t,q,b
S: str = 'A'
h: str = ' ' * 20


def findNet(s: str) -> int:  # поиск нетерминала
    global m
    for i in range(m):
        if inf[i].Net == s:
            return i
    return -1


def findTerm(s: str) -> int:  # поиск терминала
    global T
    n: int = len(T)
    for i in range(n):
        if T[i] == s:
            return i
    return -1


def deleteToRRL2(number_rule: int) -> None:  # Применение альтерантивы. Удаление элементов из стека L2
    global RR
    n: int = len(RR[number_rule])
    for i in range(n):
        L2.pop()  # команда вытаскивания элементы из стека


def pushToRRL2(number_rule: int) -> None:  # Заполнение стека L2 по правым частям правил
    global RR, y
    n: int = len(RR[number_rule])
    for i in range(n):
        y.symv = copy(RR[number_rule][n - i - 1])
        if findNet(y.symv) != -1:
            y.term = 0
        else:
            y.term = 1
        L2.append(copy(y))


def pushToLRL2(number_rule: int) -> None:  # Заполнение стека L2 по левым частям правил
    global LR, y
    y.symv = copy(LR[number_rule])
    if findNet(y.symv) != -1:
        y.term = 0
    else:
        y.term = 1
    L2.append(copy(y))


def stepOne() -> None:  # Применяем 1 альтенативу у правила А
    global x, y, inf, L1, L2
    net: int = findNet(y.symv)
    x.term = 0
    x.symv = copy(y.symv)
    x.nAlt = 1
    x.countAlt = inf[net].countAlt
    L1.append(copy(x))
    L2.pop()
    number_rule: int = inf[net].firstN + x.nAlt - 1
    pushToRRL2(number_rule)


def stepTwo() -> None:  # Перенос терминального символа из L2 в L1
    global L1, L2, x, y
    L2.pop()
    x.term = 1
    x.symv = copy(y.symv)
    x.countAlt = 0
    x.nAlt = 0
    L1.append(copy(x))


def stepThree() -> None:  # Завешение алгоритма и формирование цепочки
    global x, L1, inf
    x = copy(L1[-1])  # из стека верхний элемент читаем
    L1.pop()
    net: int = findNet(x.symv)
    if net != -1:
        result.append(copy(inf[net].firstN + x.nAlt))

    while len(L1) > 0:
        x = copy(L1[-1])  # из стека верхний элемент читаем
        L1.pop()
        net = findNet(x.symv)
        if net != -1:
            result.append(inf[net].firstN + x.nAlt)


def stepFive() -> None:  # Возврат. Перенос элемента из L1 в L2
    global L1, L2, y
    L1.pop()
    y.symv = copy(x.symv)
    y.term = 1
    L2.append(copy(y))


def stepSixA() -> None:  # Пытаемся применить новую альтернативую Из L2 вытаскиваем старую.
    global L1, x, inf
    L1.pop()
    x.nAlt += 1
    L1.append(copy(x))
    net: int = findNet(x.symv)
    number_rule: int = inf[net].firstN + x.nAlt - 1
    deleteToRRL2(number_rule - 1)
    pushToRRL2(number_rule)


def stepSixV() -> None:  # Возврат отмена текущей альтернативы.
    global x, inf, L1
    net: int = findNet(x.symv)
    number_rule: int = inf[net].firstN + x.nAlt - 1
    deleteToRRL2(number_rule)
    pushToLRL2(number_rule)
    L1.pop()


def main():
    global x, y, LR, RR, L1, L2
    end: bool = False
    # вывод грамматики
    for i in range(8):
        print(f'{i + 1}: {LR[i]} -> {RR[i]}')
    str_: str = ' ' * 100
    print("Input your line: ")
    str_ = "!a*(a+b)!"
    print(str_)
    n: int = len(str_)
    i: int = 0
    j: int = 0
    k: int = 0
    sos: str = 'q'
    y.term = 0
    y.symv = copy(S)
    L2.append(copy(y))
    k += 1
    while True:
        print(L2)
        if sos == 't':  # конец алгоритма сформировать результат
            print(f"Excellent: {result[::-1]}")
            end = True
        elif sos == 'q':  # в процессе
            y = copy(L2[-1])
            if findNet(y.symv) != -1:
                stepOne()
            else:
                if y.symv == str_[i]:
                    stepTwo()
                    i += 1
                    if i == n:
                        if len(L2) == 0:
                            stepThree()
                            sos = 't'
                        else:
                            sos = 'b'  # Якобы шаг 3'
                    else:
                        if len(L2) == 0:
                            sos = 'b'  # Якобы шаг 3'
                else:
                    sos = 'b'  # Якобы шаг 4
        elif sos == 'b':  # возврат
            x = copy(L1[-1])
            print(x)
            if findTerm(x.symv) != -1:
                stepFive()
                i -= 1
            else:
                if x.nAlt < x.countAlt:  # смотрим не все ли альтернативы применены
                    stepSixA()
                    sos = 'q'
                else:
                    if x.symv == S and i == 0:
                        print("Error")  # якобы шаг 6б
                        end = True
                    else:
                        stepSixV()
        if end == True:
            break
    return None


if __name__ == '__main__':
    main()
