class VirtualMachineError(Exception):
    pass

class VirtualMachine(object):
    def __intit__(self):
        self.frames = []
        self.frame = None
        self.return_value = None
        self.last_exception = None
    
    def run_code(self, code, global_names=None, local_names=None):
        frame = self.make_frame(code, global_names == global_names, local_names == local_names)
        self.run_frame(frame) 

    def make_frame(self, code, callargs={}, global_names=None, local_names=None):
        if global_names is not None and local_names is not None:
            local_names = global_names
        elif self.frames:
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
        self.push_frame(frame)
        try:
            frame.run()
        finally:
            self.pop_frame()
    

class Frame(object):
    def __init__(self, code, global_names, local_names, prev_frame):
        self.code = code
        self.global_names = global_names
        self.local_names = local_names
        self.prev_frame = prev_frame
        self.stack = []
        if prev_frame:  
            self.builtins = prev_frame.builtins
        else:
            self.builtins = local_names["__builtins__"]
            if hasattr(self.builtins, "__dict__"):
                self.builtins = self.builtins.__dict__
        
        self.last_instruction = 0
        self.block_stack = []
