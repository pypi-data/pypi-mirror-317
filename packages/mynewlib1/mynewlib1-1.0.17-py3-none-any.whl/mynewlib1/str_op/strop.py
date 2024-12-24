class Task:
    def __init__(self, formula):
        self.formula = formula

    def compute(self):
        operators = ['+', '-', '*', '/']

        # Пробуем получить наиболее приоритетный оператор
        for op in operators:
            if op in self.formula:
                index = self.formula.index(op)

                # Разделяем на левую и правую часть
                left = Task(self.formula[:index].strip())  # Убираем лишние пробелы
                right = Task(self.formula[index + 1:].strip())

                match op:
                    case '+':
                        return left.compute() + right.compute()
                    case '-':
                        return left.compute() - right.compute()
                    case '*':
                        return left.compute() * right.compute()
                    case '/':
                        return left.compute() / right.compute()

        # Если нет операторов, просто возвращаем число
        return float(self.formula)

