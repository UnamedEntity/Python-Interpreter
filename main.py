class Interpreter:
    def __init__(self):
        self.stack = []
        self.enviorment = {}
    
    def LOAD_VALUE(self, value):
        self.stack.append(value)
    
    def STORE_NAME(self, name):
        val = self.stack.pop()
        self.enviorment[name] = val

    def LOAD_NAME(self, name):
        val = self.enviorment[name]
        self.stack.append(val)
    
    def parse_argument(self, instruction, argument, what_to_run):
        numbers = ["LOAD_VALUE"]
        names = ["LOAD_VALUE","STORE_NAME"]
        if instruction in numbers:
            argument = what_to_run["numbers"][argument]
        elif instruction in names:
            argument = what_to_run["names"][argument]
        return argument

    def PRINT_ANSWER(self):
        ans = self.stack.pop()
        print(ans)

    def ADD_TWO_VALUES(self):
        first_num = self.stack.pop()
        second_num = self.stack.pop()
        total = first_num + second_num
        self.stack.append(total)

    def execute(self, what_to_run):
            instructions = what_to_run["instructions"]
            for each_step in instructions:
                instruction, argument = each_step
                argument = self.parse_argument(instructions,argument,what_to_run)
                bytecode_method = getattr(self,instruction)
                if argument is None:
                    bytecode_method()
                else:
                    bytecode_method(argument)
    """
    def run_code(self, what_to_run):
        instructions = what_to_run["instructions"]
        numbers = what_to_run["numbers"]
        for each_step in instructions:
            instruction, argument = each_step
            argument = self.parse_argument(instruction, argument, what_to_run)
            if instruction == "LOAD_VALUE":
                self.LOAD_VALUE(argument)
            elif instruction == "PRINT_ANSWER":
                self.PRINT_ANSWER()
            elif instruction == "ADD_TWO_VALUES":
                self.ADD_TWO_VAlUES()
            elif instruction == "STORE_NAME":
                self.STORE_NAME(argument)
            elif instruction == "LOAD_NAME":
                self.LOAD_NAME(argument)
    """


        
        
interpreter = Interpreter()

what_to_run = {
    "instructions": [("LOAD_VALUE", 0),
                         ("STORE_NAME", 0),
                         ("LOAD_VALUE", 1),
                         ("STORE_NAME", 1),
                         ("LOAD_NAME", 0),
                         ("LOAD_NAME", 1),
                         ("ADD_TWO_VALUES", None),
                         ("PRINT_ANSWER", None)],
        "numbers": [1, 2],
        "names":   ["a", "b"]

}

interpreter.execute(what_to_run)
    



    