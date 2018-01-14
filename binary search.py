# binary seatch 
def binary_search(list_, value):
  left = 0
  right = len(list_) - 1
  while left <= right:
    mid = (left + right) // 2
    if list_[mid] == value:
      return True
    else:
      if list_[mid] > value:
        right = mid - 1
      else:
        left = mid + 1
  return False