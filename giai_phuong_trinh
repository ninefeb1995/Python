import math

PI = 3.14

class PhuongTrinh:
    
    """ Lop cung cap cac ham giai phuong trinh bac hai, bac ba.
    """
    
    def bac_mot(self, a, b):
        
        """ Ham giai phuong trinh bac mot
            Args: a, b, la cac gia tri can thiet cua mot phuong trinh bac mot
            Returns: Nghiem rieng biet, nghiem kep, vo nghiem
        """      
        
        if a == 0:  # Neu dau vao a la 0, phuong trinh vo nghiem
             return "Phuong trinh vo nghiem"
        
        else: # Neu dau vao a khac 0, phuong trinh co nghiem x = -b / a
            return -b / a
    
    def bac_hai(self, a, b, c):
        
        """ Ham giai phuong trinh bac hai
            Args: a, b, c la cac gia tri can thiet cua mot phuong trinh bac hai
            Returns: Nghiem rieng biet, nghiem kep, vo nghiem
        """
        
        if a == 0:  # Neu dau vao a la 0, tro lai phuong trinh bac mot
           return self.bac_mot(b, c)
        
        else: # Truong hop dau vao a khac khong            
            delta = b ** 2 - 4 * a * c # Tinh del-ta cho phuong trinh
            
            if delta < 0: # Neu del-ta nho hon khong, phuong trinh khong co nghiem
                return "Phuong trinh vo nghiem"
            
            elif delta == 0: # Neu del-ta bang 0, phuong trinh co nghiem kep
                return -b / (2 * a)
            
            else: # Neu del - ta lon hon khong, phuong trinh co hai nghiem rieng biet
                return [((-b - delta ** 0.5) / (2 * a)), ((-b + delta ** 0.5) / (2 * a))]            
    
    def bac_ba(self, a, b, c, d):
        
        """ Ham giai phuong trinh bac ba
            Args: a, b, c, d là cac gia tri can thiet cua mot phuong trinh bac ba
            Returns: Ba nghiem rieng biet, nghiem kep, vo nghiem
        """
        
        if a == 0: # Neu dau vao a bang 0, phuong trinh tro thanh phuong trinh bac hai
            return bac_hai(a, b, c) 
        
        else: # Neu dau vao a khac 0 giai theo phuong trinh bac ba
            delta = float(b ** 2) - 3 * a * c # Tinh del-ta cho phuong trinh
            
            k = float((9 * a * b * c - 2 * b ** 3 - 27 * a ** 2 * self.d)) / (2 * math.fabs(delta ** 3) ** 0.5)                     
            
            if delta > 0:                             
                    if math.fabs(k) <= 1 : # Neu del-ta lon hon 0 nhung k nho hon hoac bang 1, phuong trinh co ba nghiem rieng biet                    
                        x1 = (2 * math.sqrt(delta) * math.cos((math.acos(k) / 3)) - b)/ float((3 * a))
                        
                        x2 = (2 * math.sqrt(delta) * math.cos((math.acos(k) / 3 - (2 * PI / 3))) - b) / float((3 * a))
                        
                        x3 = (2 * math.sqrt(delta) * math.cos((math.acos(k) / 3 + (2 * PI / 3))) - b) / float((3 * a))
                        
                        return [x1, x2, x3]                    
                    
                    else: # Neu del-ta lon hon 0 nhung k lon hon 1, phuong trinh co ba nghiem rieng biet                   
                        x0 = float(((math.sqrt(delta) * math.fabs(k)) / (3 * a * k))) * \
                             (math.pow(math.fabs(k) + math.sqrt(math.pow(k, 2) - 1), 1 / 3) + math.pow(math.fabs(k) - math.sqrt(math.pow(k, 2) - 1), 1 / 3)) - \
                                                                                                                                                (b / (3 * a))
                        return x0           
            
            elif delta == 0: # del-ta bang khong phuong trinh co nghiem kep         
                    x = (-b + math.pow(math.pow(b, 3) -
                                                      27 * math.pow(a, 2) * self.d, 1 / 3)) / \
                                                                                             float((3 * a))
                    return x          
            
            else: #del-ta be hon khong phuong trinh co nghiem don          
                    x = (math.sqrt(math.fabs(delta)) / (3 * a)) * \
                                (math.pow(k + math.sqrt(math.pow(k, 2) + 1), 1 / 3) + (k - math.sqrt(math.pow(k, 2) + 1)) ** (1 / 3)) - \
                                                                                                                    float((b / (3 * a)))
                    return x


