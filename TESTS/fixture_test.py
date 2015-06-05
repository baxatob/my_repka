


class A(object):
    
    def fixik1(self):
        print "FIXIK 1"
        
    @fixik1
    def fixik2(self):
        print "FIXIK 2"
        
 
if __name__ == "__main__":
    a = A()
    a.fixik1()
        
    