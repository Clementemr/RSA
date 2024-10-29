import math
from random import randint

def gcd(a,n): # function to calculate the gcd of two numbers
    if a>n:
        dv = n
        dn = a
    else:
        dv = a
        dn = n
    while(True):
        # print(f"{int(dn)} = {int(dv)} * {int(dn/dv)} + {int(dn%dv)}")
        q = math.floor(dn/dv)
        r = dn - dv*q
        if r==0:
            break
        dv = r
        dn = (dn - r)//q
    gcd = int(dv)
    return gcd


def rule1(symbol): # function for rule 1
    #print("rule 1")
    tup = symbol[2]
    a = tup[0]
    n = tup[1]
    if gcd(a,n)!=1:
        #print("error: gcd!=1")
        return symbol
    c=a
    while c>n:
        c = c-n
    # print((a,n)," -> ",(c,n))
    return [symbol[0],symbol[1],(c,n)]

def rule2(symbol): # function for rule 2
    #print("rule 2")
    tup = symbol[2]
    a = tup[0]
    n = tup[1]
    twos = symbol[1]
    if gcd(a,n)!=1:
        print("error: gcd!=1")
        return symbol

    result = []
    c=a
    while c%2==0:
        result.append((2,n))
        c=c//2
    result.append((c,n))
    # print((a,n)," -> ",end="")
    # for item in result:
    #     print(item,end=" ")
    # print("")
    twos = len(result)-1
    return [symbol[0],twos,result[-1]]

def rule4(symbol): # function for rule 4
    #print("rule 4")
    tup = symbol[2]
    a = tup[0]
    n = tup[1]
    twos = symbol[1]
    sign = symbol[0]
    for i in range(twos):
        if n%8==1 or n%8==7:
            sign = sign * 1
        if n%8==3 or n%8==5:
            sign = sign * -1
    return [sign,0,(a,n)]

def rule5(symbol): # function for rule 5
    #print("rule 5")
    tup = symbol[2]
    m = tup[0]
    n = tup[1]
    twos = symbol[1]
    sign = symbol[0]
    if m%2==1 and gcd(m,n)==1:
        if m%4==3 and n%4==3:
            return [sign*-1,symbol[1],(n,m)]
        else:
            return [sign,symbol[1],(n,m)]
    else:
        #print("error: m is even or gcd!=1")
        return symbol

def jacobi(symbol): # this function calculates the Jacobi symbol iteratively by applying the rules
    if gcd(symbol[2][0],symbol[2][1])!=1:
        print("GCD!=1 -jacobi")
        return None
    count=0
    s = symbol
    # if s[0]==1:
    #         print("",end="")
    # if s[0]==-1:
    #     print("-",end="")
    # print(s[2])
    while count<100000:
        count+=1
        if s[2][0]>s[2][1]:
            s = rule1(s)
        if s[2][0]%2==0:
            s=rule4(rule2(s))
            # if s[0]==1:
            #     print("",end="")
            # if s[0]==-1:
            #     print("-",end="")
            # print(s[2])
        if s[2][0]==1:
            return s[0]
        if s[2][0]==2:
            n = s[2][1]
            sign = s[0]
            if n%8==1 or n%8==7:
                sign = sign * 1
            if n%8==3 or n%8==5:
                sign = sign * -1
            return sign
        s = rule5(s)
        # if s[0]==1:
        #     print("",end="")
        # if s[0]==-1:
        #     print("-",end="")
        # print(s[2])

def squareMultiply(a,e,m): # a^e mod m
    a=a%m
    result=1
    while e>0:
        if e%2==1:
            result = (result*a)%m
        a = (a**2)%m
        e = e//2
    return result


def getKeyFromFile(fileName): #gets the key from a file
    with open(fileName) as file: 
        for line in file:
            key = int(line.strip())
            return key
    print("key not found")


def getPlaintextFromFile(fileName): #gets the plaintext from a file
    with open(fileName) as file:
        for line in file:
            text = str(line.strip())
            return text
        
def getBit(num): #converts a number to an 8 bit binary string
    result=""
    for i in range(8):
        if num>=2**(7-i):
            result+="1"
            num-=2**(7-i)
        else:
            result+="0"
    return result

def convertTextToBytes(text): #converts a string to a binary string
    theBytes=""
    for letter in text:
        theBytes+=getBit((ord(letter)))
    return theBytes

def convertIntToBytes(num): #converts a number to a binary string
    result=""
    while num>0:
        result+=str(num%2)
        num=num//2
    while len(result)%8!=0:
        result+="0"
    return result[::-1]

def convertBytesToText(theBytes): #converts a binary string to a string
    result=""
    for i in range(0,len(theBytes),8):
        result+=(chr(convertBytesToInt(theBytes[i:i+8])))
    return result

def convertBytesToInt(theBytes): #converts a binary string to a number
    num = 0
    l = len(theBytes)
    for i in range(l):
        if(theBytes[i]=="1"):
            num+=(2**(l-i-1))
    return num

def splitTextBlocks(text): #splits a string into blocks of size 214
    result=[]
    currentBlock=text[0]
    for i in range(1,len(text)):
        currentBlock+=text[i]
        if(i%214==0):
            result.append(currentBlock)
            currentBlock=""
    result.append(currentBlock)
    return result

def splitBytesBlocks(theBytes): #splits a binary string into blocks of size 1712
    result=[]
    currentBlock=theBytes[0]
    for i in range(1,len(theBytes)):
        currentBlock+=theBytes[i]
        if(i%1712==0):
            result.append(currentBlock)
            currentBlock=""
    result.append(currentBlock)
    return result

def combineBlocks(blockList): #combines a list of blocks into a single string
    result=""
    for block in blockList:
        result+=block
    return result


def encryptRSA(plaintext): #encrypts a string using RSA

    e=getKeyFromFile("Clemente_RSA/RSA_e")

    n=getKeyFromFile("Clemente_RSA/RSA_n")

    blockText = splitTextBlocks(plaintext)

    blocks=[]

    for i in range(len(blockText)):

        block1 = blockText[i]

        block2 = convertTextToBytes(block1)

        block3 = convertBytesToInt(block2)
        

        block4 = squareMultiply(block3,e,n)
        #print(block4)

        blocks.append(block4)

    return blocks



def decryptRSA(blocks): #decrypts a list of blocks using RSA

    d=getKeyFromFile("Clemente_RSA/RSA_d")

    n=getKeyFromFile("Clemente_RSA/RSA_n")

    result = []

    for i in range(len(blocks)):
        block1 = blocks[i]

        block2 = squareMultiply(block1,d,n)

        block3 = convertIntToBytes(block2)

        block4 = convertBytesToText(block3)

        result.append(block4)
    
    result = combineBlocks(result)

    return result

def getEuler(a,n):
    x = squareMultiply(a,((n-1)//2),n)
    if x==n-1:
        return -1
    else:
        return x
    

def getJacobi(a,n):
    return jacobi([1,0,(a,n)])

def solovayStrassen(a,n):
    g = gcd(a,n)
    #print("gcd:",g)
    if g!=1:
        #print("gcd!=1")
        return 0
    
    e=getEuler(a,n)
    #print("euler:",e)
    if e>1:
        #print("error: euler>1")
        return 0
    j = getJacobi(a,n)
    #print("jacobi:",j)
    if j==None:
        #print("error: jacobi==None")
        return 0
    if j==e:
        return 1
    return 0

def getPrime(t):
    count=0
    while True:
        count+=1
        n = randint(2**1023,2**1024)
        if n%2==0:
            n+=1
        a = randint(2,n-1)
        #print(f"n:",n)
        if testN(n,t)==1:
            #print("n is prime")
            break
        else:
            #print("n is not prime")
            continue
    return [n,count]
    

def testN(n,t):
    for i in range(t):
        a = randint(2,n-1)
        if solovayStrassen(a,n)==0:
            return 0
        #print(i+1)
    return 1

def generateE(phi):
    while True:
        e = randint(2,phi-1)
        if gcd(e,phi)==1:
            return e

def extendedGCD(n1,n2):

    nums = []
    sums = {}

    dv = n1
    dn = n2
    while(True):
        q = math.floor(dn/dv)
        r = dn - dv*q
        #print(f"{int(dn)} = {int(dv)} * {int(q)} + {int(r)}")
        if r!=0:
            sums[r] = [int(dn),int(dv),int(q)]

        nums.append(int(dn))

        if r==0:
            break
        dv = r
        dn = (dn - r)//q

    s={}

    for i in range(len(nums)):
        s[nums[i]]=0

    s[nums[-1]]=sums[1][2]
    s[nums[-2]]=1

    count=0
    tempNum=nums[-1]
    while(len(nums)>2):
        

        tempNum = nums.pop()
        tempList = sums[tempNum]

 
        s[tempList[0]]+=s[tempNum]
        s[tempList[1]]+=(s[tempNum]*tempList[2])

        s[tempNum]=0



    return list(s.values())[1]

def generateKey():
    t=100
    while True:
        l1 = getPrime(t)
        p=l1[0]
        pCount=l1[1]
        # print("p:",p)

        l2 = getPrime(t)
        q=l2[0]
        qCount=l2[1]
        # print("q:",q)

        n = p*q
        

        phi = (p-1)*(q-1)

        # print("phi:",phi)

        tries = 0
        while tries<1000:
            tries+=1
            e = generateE(phi)
            
            d = extendedGCD(e,phi)

            if (e*d)%phi==1:
                break
        if tries==1000:
            continue
        else:
            break

    print("n:",n)
        
    print("e:",e)
        
            

    with open("Clemente_RSA/RSA_e","w") as file:
        file.write(str(e))

    with open("Clemente_RSA/RSA_d","w") as file:
        file.write(str(d))

    with open("Clemente_RSA/RSA_n","w") as file:
        file.write(str(n))

    print("random numbers tried before p was found:",pCount)

    print("random numbers tried before q was found:",qCount)

    print("number of Solovay-Strassen tests per prime:",t)

    print("probability that p is composite:",calcProbability(t))
    print("probability that q is composite:",calcProbability(t))

    print("keys written to files")
    print("")

    return phi

def calcProbability(n):
    return ((1024*math.log(2)-2)/((1024*math.log(2))-2+(2**(n+1))))



phi = generateKey()

plaintext = getPlaintextFromFile("Clemente_RSA/RSA_plaintext")

encrypted = encryptRSA(plaintext)

print("")
for block in encrypted:
    print(block)
    print("")

decrypted = decryptRSA(encrypted)

print(decrypted)













