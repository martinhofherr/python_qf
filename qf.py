# Simple library to deal with numbers in QFormat

import math as m

class QNumber:
    def __init__(self, m_bits, n_bits):
        self.m_bits = m_bits
        self.n_bits = n_bits

        self.max_f = m.pow(2, m_bits-1) - m.pow(2, -n_bits)
        self.min_f = -m.pow(2, m_bits-1)
        self.max_i = int(m.pow(2, m_bits+n_bits)//2 - 1)
        self.min_i = int(-self.max_i - 1)
        
        self.k = int(m.pow(2, n_bits-1));

        self._val = 0

    def _saturate(self, value):
        if value > self.max_i:
            return self.max_i
        elif value < self.min_i:
            return self.min_i
        else:
            return value

    def _check_operand(self, op):
        if self.m_bits != op.m_bits or self.n_bits != op.n_bits:
            raise ArithmeticError("Operand formats do not match!")
    
    def info(self):
        print("m = {}, n = {}, [{}, {}] == [{},{}]".format(self.m_bits, self.n_bits,
            self.min_f, self.max_f, self.min_i, self.max_i))
    
    def to_float(self):
        return self._val * m.pow(2, -self.n_bits)

    
    def from_float(self, fval):
        val = int(fval * m.pow(2, self.n_bits))
        self._val = self._saturate(val)
    
    
    def __add__(self, qnum):
        self._check_operand(qnum)

        val = self._val + qnum._val
        val = self._saturate(val)

        qn = QNumber(self.m_bits, self.n_bits)
        qn._val = val

        return qn

    def __sub__(self, qnum):
        self._check_operand(qnum)

        val = self._val - qnum._val
        val = self._saturate(val)

        qn = QNumber(self.m_bits, self.n_bits)
        qn._val = val

        return qn

    def __mul__(self, qnum):
        self._check_operand(qnum)
        
        val = self._val * qnum._val
        val = val + self.k
        val = val >>  self.n_bits
        val = self._saturate(val)

        qn = QNumber(self.m_bits, self.n_bits)
        qn._val = val

        return qn

    def __truediv__(self, qnum):
        self._check_operand(qnum)
        
        val = self._val << self.n_bits
        if (val >= 0 and qnum._val >=0) or (val < 0 and qnum._val < 0):
            val = val + qnum._val // 2
        else:
            val = val - qnum._val // 2

        val = val // qnum._val
            
        qn = QNumber(self.m_bits, self.n_bits)
        qn._val = val

        return qn

  

def disp(op, a, b, c):
    print("a {} b = c".format(op))
    print("a == {} = {}".format(a._val, a.to_float()))
    print("b == {} = {}".format(b._val, b.to_float()))
    print("c == {} = {}".format(c._val, c.to_float()))
    

def main():
    a = QNumber(3, 20)
    b = QNumber(3, 20)

    a.from_float(0.45)
    b.from_float(0.25)

    a.info()
    b.info()

    c = a + b
    disp('+', a, b, c)

    c = a - b
    disp('-',a, b, c)

    c = a * b
    disp('*', a, b, c)

    c = a / b
    disp('/', a, b, c)
   

if __name__ == "__main__":
    main()
