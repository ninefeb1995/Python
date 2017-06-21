import math
PI = 3.14
class phuong_trinh:
    def __init__(self, a, b, c, d = 0):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
    def bac_hai(self):
        if self.a == 0:
            if self.b == 0:
                return "Phuong trinh vo nghiem"
            else:
                return float(self.c) / self.b
        else:
            delta = self.b ** 2 - 4 * self.a * self.c
            if delta < 0:
                return "Phuong trinh vo nghiem"
            elif delta == 0:
                return -self.b / (2 * self.a)
            else:
                return [((-self.b - delta ** 0.5) / (2 * self.a)), ((-self.b + delta ** 0.5) / (2 * self.a))]            
    
    def bac_ba(self):
        if self.a == 0:
            self.a = self.b
            self.b = self.c
            self.c = self.d
            return self.bac_hai()
        else:
            delta = float(self.b**2) - 3*self.a*self.c
            k = float((9*self.a*self.b*self.c - 2*self.b**3 - 27*self.a**2*self.d))/ (2*math.fabs(delta**3)**0.5)         
            if delta > 0:           
                    if math.fabs(k) <= 1 :                  
                        x1 = (2*math.sqrt(delta)*math.cos((math.acos(k)/3)) - self.b)/ float((3*self.a))
                        x2 = (2*math.sqrt(delta)*math.cos((math.acos(k)/3 - (2*PI/3))) - self.b) / float((3*self.a))
                        x3 = (2*math.sqrt(delta)*math.cos((math.acos(k)/3 + (2*PI/3))) - self.b) / float((3*self.a))
                        return [x1, x2, x3]                    
                    else:                   
                        x0 = float(((math.sqrt(delta)*math.fabs(k))/(3*self.a*k))) * (math.pow(math.fabs(k) + math.sqrt(math.pow(k,2) - 1),1/3) + math.pow(math.fabs(k) - math.sqrt(math.pow(k,2) - 1),1/3)) - (self.b/(3*self.a))
                        return x0           
            elif delta == 0:           
                    x = (-self.b + math.pow(math.pow(self.b,3) - 27*math.pow(self.a,2)*self.d,1/3)) / float((3*self.a))
                    return x          
            else:          
                    x = (math.sqrt(math.fabs(delta))/(3*self.a))*(math.pow(k + math.sqrt(math.pow(k,2) + 1), 1/3) + (k - math.sqrt(math.pow(k,2) + 1))**(1/3)) - float((self.b/(3*self.a)))
                    return x

try_ = phuong_trinh(1,3,2,-3)
kq = try_.bac_ba()
print(kq)
            