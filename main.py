class Interpreter:
    def __init__(self):
        self.stack = []
    
    def LOAD_VALUE(self, value):
        self.stack.append(value)

    def PRINT_ANSWER(self):
        ans = self.stack.pop()
        print(ans)

    def ADD_TWO_VAlUES(self):
        first_num = self.stack.pop()
        second_num = self.stack.pop()
        total = first_num + second_num
        self.stack.append(total)
    
    def run_code(self, what_to_run):
        instructions = what_to_run["instructions"]
        numbers = what_to_run["numbers"]
        for each_step in instructions:
            instruction, argument = each_step
            if instruction == "LOAD_VALUE":
                number = numbers[argument]
                self.LOAD_VALUE(number)
            elif instruction == "PRINT_ANSWER":
                self.PRINT_ANSWER()
            elif instruction == "ADD_TWO_VALUES":
                self.ADD_TWO_VAlUES()
interpreter = Interpreter()

what_to_run = {
    "instructions":[("LOAD_VALUE", 0),
                         ("LOAD_VALUE", 1),
                         ("ADD_TWO_VALUES", None),
                         ("LOAD_VALUE", 2),
                         ("ADD_TWO_VALUES", None),
                         ("PRINT_ANSWER", None)]
    ,"numbers": [7,5,8]

}

interpreter.run_code(what_to_run)
    



    