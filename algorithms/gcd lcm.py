'''
Euclidean algorithm:
GCD(A,0) = A
GCD(0,B) = B
If A = B⋅Q + R and B≠0 then GCD(A,B) = GCD(B,R) where Q is an integer, R is an integer between 0 and B-1
'''
def gcd(a, b):
    while b > 0:
        a, b = b, a % b
    return a

'''
doesnt matter if a < b or a > b

because if a < b => a % b => a therefore the next recursive call becomes gcd(b, a)

so in this formulation we should think that the 1st param > 2nd param
'''
def gcd_recursive(a, b):
    if b == 0:
        return a

    return gcd_recursive(b, a % b)

def lcm(a, b):
    return (a * b) // gcd(a, b)

'''
GCD and LCM are associative..

which means for getting gcd(a,b,c)=gcd(a,gcd(b,c))
and 

lcm(a, b, c) = a * b * c / gcd(a * b * c)
'''