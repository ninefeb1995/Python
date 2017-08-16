# selection sort
def selection_sort(list_):
  
  for x in range(len(list_)-1,0,-1):
    maxpos=0
    for location in range(1, x+1):
      if list_[location]>list_[maxpos]:
        maxpos = location
    
    temp = list_[x]
    list_[x] = list_[maxpos]
    list_[maxpos] = temp
  