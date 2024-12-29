class Task:
    def __init__(self,f):
        self.formula = f
    # 1 + 2*3 - 5/4
    def compute(self):
        operators = ['+', '-' , '*' , '/']
        for op in operators:
            if op in self.formula:
                index = self.formula.index(op)
                
                left = Task(self.formula[:index])
                right = Task(self.formula[index+1:])
                
                match op:
                    case '+':
                        return left.compute() + right.compute()
                    case '-':
                        return left.compute() - right.compute()
                    case '/':
                        return left.compute() / right.compute()
                    case '*':
                        return left.compute() * right.compute()
        return float(self.formula)

