#!/usr/bin/env python

# ip = "192.168.1.2"
# 
# def reverse(ip):
#     
#     a = ip.split(".")
#     new = reversed(a)      
#     return new
# 
# b =  reverse(ip)
# 
# x = (".").join(b)
# print (x)
    
s = [1,2,3,4,5]
print (s[::-1])
k = []
for n in range(len(s)):
    k.append(str(s[len(s)-n-1]))
print(k)
print (",".join(k))