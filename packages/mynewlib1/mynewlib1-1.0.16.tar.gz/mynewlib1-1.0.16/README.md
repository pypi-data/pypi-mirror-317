# mynewlib1

Эта библиотека написана для реалшизации любых действий с факториалами и для вычислений формул, записанных в формате str.

```


from mynewlib1 import factorial, permutation, compination, binkof, gamma, summaf

n=int(input())
def main():
    # Пример использования функции factorial
    n = 5
    print(f"Факториал {n}! = {factorial(n)}")

    # Пример использования функции permutation
    print(f"Перестановка {n}! = {permutation(n)}")

    # Пример использования функции combination
    k = 3
    print(f"Комбинация C({n}, {k}) = {compination(n, k)}")

    # Пример используя функции binkof
    print(f"Биномиальный коэффициент B({n}, {k}) = {binkof(n, k)}")

    # Пример использования функции gamma
    print(f"Гамма ({n}) = {gamma(n)}")

    # Пример использования функции summaf
print(f"Сумма факториалов от 0 до = {summaf(n)}")

if __name__ == '__main__':
    main()

```
## Installation

Install it using pip:
```bash
pip install mynewlib1