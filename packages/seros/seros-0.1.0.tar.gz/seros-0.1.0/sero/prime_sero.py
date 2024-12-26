def soe(n):
    prime = [True for _ in range(n+1)]
    p = 2

    while p*p <= n:

        if prime[p] == True:

            for i in range(p*p,n+1,p):
                prime[i] = False
        p+=1
    return [p for p in range(2, n + 1) if prime[p]]

            