# Домашнее задание к лекции 7. «Подготовка к собеседованию»
# Задачи 1, 2

class Stack:
    
    def __init__(self, s_input) -> None:
        self.s_input = s_input
        self.s_stack = self.s_input[::-1]
            
    def print_stack(self) -> str:
        print('Вызван метод: print_stack')
        print(f'Входящая строка: {self.s_input}')
        print(f'Стек: {self.s_stack}')
        
    def is_empty(self) -> bool:
        print('Вызван метод: is_empty')
        if len(self.s_stack) == 0:
            return True
        else:
            return False
        
    def push(self, s_push) -> None:  # Добавляем в стек элемент
        print('Вызван метод: push')
        self.s_push = s_push
        self.s_push += self.s_stack
        self.s_stack = self.s_push

    def pop(self) -> str:  # Удаляем первый элемент стека
        print('Вызван метод: pop')
        elem = self.s_stack[0]
        self.s_stack = self.s_stack[1:]
        return elem
    
    def peek(self) -> str:  # Возврат первого элемента стека
        print('Вызван метод: peek')
        return self.s_stack[0]
    
    def size(self) -> int:
        print('Вызван метод: size')
        return len(self.s_stack)
    
    '''
    Есть элемент открывающий и закрывающий, идём слева направо по открывающим и вслучае встречи
    открывающих i++, встречая закрывающие i--, при балансе i должен быть = 0
    И открывающий элемент не должен быть закрыт другим типом элемента: {]
    '''
    
    def between_balance(self) -> bool:
        l_form = ['(', ')', '[', ']', '{', '}']
        cnt_0 = 0
        cnt_1 = 0
        cnt_2 = 0
        cnt_error = 0
        elem_tmp = ''
        for elem in self.s_stack:
            
            # Счётчик на тип откр.скобки закрытую другим типом скобки
            # (стек имеет LIFO, поэтому начинаем с элементов: 1,3,5, *просто со строкой, без LIFO: 0,2,4)
            if elem_tmp == l_form[1] and elem == l_form[2] or elem_tmp == l_form[1] and elem == l_form[4]:
                cnt_error += 1
            if elem_tmp == l_form[3] and elem == l_form[0] or elem_tmp == l_form[3] and elem == l_form[4]:
                cnt_error += 1
            if elem_tmp == l_form[5] and elem == l_form[0] or elem_tmp == l_form[5] and elem == l_form[2]:
                cnt_error += 1
            elem_tmp = elem  # Сохраняем элемент для сравнения со следующим
            
            # Счётчики открытых и закрытых скобок, проверка на равное кол.
            if elem == l_form[0]: cnt_0 += 1
            if elem == l_form[1]: cnt_0 -= 1
            if elem == l_form[2]: cnt_1 += 1
            if elem == l_form[3]: cnt_1 -= 1
            if elem == l_form[4]: cnt_2 += 1
            if elem == l_form[5]: cnt_2 -= 1
        
        print(f'Значения баланса типов скобок: (={cnt_0} [={cnt_1} {chr(123)}={cnt_2}, Закрытых другим типом: {cnt_error}')
        
        if cnt_0 or cnt_1 or cnt_2 or cnt_error != 0: return False
        else: return True
        

if __name__=='__main__':
    
    # Пример сбалансированных последовательностей скобок:
    s_str_01 = '(((([{}]))))'
    s_str_02 = '[([])((([[[]]])))]{()}'
    s_str_03 = '{{[()]}}'
    
    # Несбалансированные последовательности:
    s_str_04 = '}{}'
    s_str_05 = '{{[(])]}}'
    s_str_06 = '[[{())}]'
    s_str_07 = '[({])}'  # равное кол. но открывающая скобка закрыта другим типом

    l_input_list = ['(((([{}]))))', '[([])((([[[]]])))]{()}', '{{[()]}}', '}{}', '{{[(])]}}', '[[{())}]', '[({])}']

    for elem in l_input_list: 
        s_str_obj_01 = Stack(elem)
        s_str_obj_01.print_stack()
        print(s_str_obj_01.between_balance())
        print()

    s_str_obj_01.push('bb')
    s_str_obj_01.print_stack()
    print()
    print(s_str_obj_01.pop())
    s_str_obj_01.print_stack()
    print()
    print(s_str_obj_01.peek())
    s_str_obj_01.print_stack()
    print()
    print(s_str_obj_01.size())
