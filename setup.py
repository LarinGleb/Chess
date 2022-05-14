def digital_root(n):
    result = 0
    for i in str(n):
        result += int(i)
        
      
    if len(str(result)) == 1: 
         return result
        
    else: 
        return digital_root(result)

print(len(str(6)) > 1)
print(digital_root(942))