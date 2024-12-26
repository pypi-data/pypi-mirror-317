PO_DEF={'what':0,'of':100,'print_value':True,'base_percent':100}
class percentOf:
    value=None
    what=None
    of=None
    def __init__(self,what=0,of=100,print_value=True,base_percent=100):
        self.base_percent=base_percent
        if True not in [isinstance(what,int),isinstance(what,float)]:
            print("What Must be a int or a float")
            return
        self.what=what
        self.of=of
        if isinstance(of,int):
            self.value=(self.what/base_percent)*of
        elif True in [isinstance(of,list),isinstance(of,tuple),isinstance(of,str),isinstance(of,bytes)]:
            size=len(of)
            percent=int((what/base_percent)*size)
            if percent not in [None,]:
                self.value=of[0:percent]
        if print_value:
            print(f"Of(what={self.what}:{type(self.what)},of={self.of}:{type(self.of)},value={self.value}:{type(self.value)})")
