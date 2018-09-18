#this program calculates E(X^2)
#X:(i-j)^2-abs(2*i-j)
# i,j are ints s.t. 1<=i,j<=6
def main():
    X=0
    for i in range(1,7):
        for j in range(1,7):
            T=(i-j)**2-abs(2*i-j)
            S=T**2
            print ('(',i,',',j,'): ',T, ' ', S)
            
            X+=S

    print (X/36.0)
