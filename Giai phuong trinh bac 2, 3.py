import math
PI = 3.14
class phuong_trinh:
    """ Lop cung cap cac ham giai phuong trinh bac hai, bac ba.
        Cung cap cac tham so dau vao nhu a, b, c, d
    """
    def __init__(self, a, b, c, d = 0):
        """ Ham khoi tao, khoi gan cac gia tri """
        self.a = a
        self.b = b
        self.c = c
        self.d = d
    def bac_hai(self):
        """ Ham giai phuong trinh bac hai
            Args: a, b, c la cac gia tri can thiet cua mot phuong trinh bac hai
            Returns: Nghiem rieng biet, nghiem kep, vo nghiem
        """
        if self.a == 0:  # Neu dau vao a la 0, phuong trinh co nghiem x = -b /a
            if self.b == 0: 
                return "Phuong trinh vo nghiem"
            else:
                return float(self.c) / self.b
        else: # Truong hop dau vao a khac khong
            delta = self.b ** 2 - 4 * self.a * self.c # Tinh del-ta cho phuong trinh
            if delta < 0: # Neu del-ta nho hon khong, phuong trinh khong co nghiem
                return "Phuong trinh vo nghiem"
            elif delta == 0: # Neu del-ta bang 0, phuong trinh co nghiem kep
                return -self.b / (2 * self.a)
            else: # Neu del - ta lon hon khong, phuong trinh co hai nghiem rieng biet
                return [((-self.b - delta ** 0.5) / (2 * self.a)), ((-self.b + delta ** 0.5) / (2 * self.a))]            
    
    def bac_ba(self):
        """ Ham giai phuong trinh bac ba
            Args: a, b, c, d là cac gia tri can thiet cua mot phuong trinh bac ba
            Returns: Ba nghiem rieng biet, nghiem kep, vo nghiem
        """
        if self.a == 0: # Neu dau vao a bang 0, phuong trinh tro thanh phuong trinh bac hai
            self.a = self.b
            self.b = self.c
            self.c = self.d
            return self.bac_hai() 
        else: # Neu dau vao a khac 0 giai theo phuong trinh bac ba
            delta = float(self.b**2) - 3*self.a*self.c # Tinh del-ta cho phuong trinh
            k = float((9*self.a*self.b*self.c - 2*self.b**3 - 27*self.a**2*self.d))/ (2*math.fabs(delta**3)**0.5)         
            if delta > 0:         
                    if math.fabs(k) <= 1 : # Neu del-ta lon hon 0 nhung k nho hon hoac bang 1, phuong trinh co ba nghiem rieng biet                    
                        x1 = (2*math.sqrt(delta)*math.cos((math.acos(k)/3)) - self.b)/ float((3*self.a))
                        x2 = (2*math.sqrt(delta)*math.cos((math.acos(k)/3 - (2*PI/3))) - self.b) / float((3*self.a))
                        x3 = (2*math.sqrt(delta)*math.cos((math.acos(k)/3 + (2*PI/3))) - self.b) / float((3*self.a))
                        return [x1, x2, x3]                    
                    else: # Neu del-ta lon hon 0 nhung k lon hon 1, phuong trinh co ba nghiem rieng biet                   
                        x0 = float(((math.sqrt(delta)*math.fabs(k))/(3*self.a*k))) * (math.pow(math.fabs(k) + math.sqrt(math.pow(k,2) - 1),1/3) + math.pow(math.fabs(k) - math.sqrt(math.pow(k,2) - 1),1/3)) - (self.b/(3*self.a))
                        return x0           
            elif delta == 0: # del-ta bang khong phuong trinh co nghiem kep         
                    x = (-self.b + math.pow(math.pow(self.b,3) - 27*math.pow(self.a,2)*self.d,1/3)) / float((3*self.a))
                    return x          
            else: #del-ta be hon khong phuong trinh co nghiem don          
                    x = (math.sqrt(math.fabs(delta))/(3*self.a))*(math.pow(k + math.sqrt(math.pow(k,2) + 1), 1/3) + (k - math.sqrt(math.pow(k,2) + 1))**(1/3)) - float((self.b/(3*self.a)))
                    return x
