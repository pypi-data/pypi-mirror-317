if __name__ == '__main__':
    from Task import Task
else:
    from src.CalculateAndPermutations16_qjarishekka.Calc.Task import Task

def test1(comments=False):
    test = Task("1+1")
    
    assert test.compute() == 2
    if comments:
        print('first example test completed')
    test = Task("2*3")
    assert test.compute() == 6
    if comments:
        print('second example test completed')

if __name__ == '__main__':
    print('this is init of Calc module!')
    test1()
