class VirtualMachineError(Exception):
    pass

class VirtualMachine(object):
    def __init__(self):
        self.frames = []
        self.frame = None
        self.return_value = None
        self.last_exception = None
    
    def run_code(self, code, global_names=None, local_names=None):
        frame = self.make_frame(code, {}, global_names, local_names)
        self.run_frame(frame) 

    def make_frame(self, code, callargs={}, global_names=None, local_names=None):
        if global_names is None or local_names is None:
            if self.frames:
                global_names = self.frame.global_names
                local_names = {}
            else:
                global_names = local_names = {
                    '__builtins__': __builtins__,
                    '__name__': '__main__',
                    '__doc__': None,
                    '__package__': None,
                }
        local_names.update(callargs)
        frame = Frame(code, global_names, local_names, self.frame)
        return frame
    
    def push_frame(self, frame):
        self.frames.append(frame)
        self.frame = frame

    def pop_frame(self):
        self.frames.pop()
        if self.frames:
            self.frame = self.frames[-1]
        else:
            self.frame = None

    def run_frame(self, frame):
        pass
    

class Frame(object):
    def __init__(self, code, global_names, local_names, prev_frame):
        self.code = code
        self.global_names = global_names
        self.local_names = local_names
        self.prev_frame = prev_frame
        self.stack = []
        if prev_frame:  
            self.builtin_names = prev_frame.builtin_names
        else:
            self.builtin_names = local_names["__builtins__"]
            if hasattr(self.builtin_names, "__dict__"):
                self.builtin_names = self.builtin_names.__dict__
        
        self.last_instruction = 0
        self.block_stack = []
