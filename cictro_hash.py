import math
from Crypto.Util.number import bytes_to_long,long_to_bytes
from base64 import b64encode as encode
class Keccak:
    def __init__(self, data=None):
        # Initialize the constants used throughout Keccak

        self.data = data

        # self.S = [31,56,156,167,38,240,174,248]
        self.r = [31,56,156,167]
        self.c = [38,240,174,248]
        # self.w = [[31,56,156,167],[38,240,174,248]]
    @staticmethod
    def rotr(n):
        bit_n = bin(n)[2:].zfill(8)
        lsb = bit_n[-1]
        return int(lsb+bit_n[:-1],2)
    @staticmethod
    def rotl(n):
        bit_n = bin(n)[2:].zfill(8)
        msb = bit_n[0]
        return int(bit_n[1:]+msb,2)
    @staticmethod
    def Round(w):
        # alpha step
        # print 'before alpha step',w
        w.reverse()
        # print 'after alpha step',w
        # beta step
        # print 'before beta step',w
        w[0][0] = w[1][3] ^ w[0][0]
        w[0][1] = w[1][2] ^ w[0][1]
        w[0][2] = w[1][1] ^ w[0][2]
        w[0][3] = w[1][0] ^ w[0][3]

        # print 'after beta step' ,w
        # gamma step
        x1,x2,x3,x4 = w[0][0],w[0][1],w[0][2],w[0][3]
        x5,x6,x7,x8 = w[1][0],w[1][1],w[1][2],w[1][3]
        # w[0][3] = w[0][0]
        # w[1][2] = w[0][1]
        # w[1][3] = w[0][2]
        # w[1][1] = w[0][3]
        # w[0][1] = w[1][0]
        # w[1][0] = w[1][1]
        # w[0][2] = w[1][2]
        # w[0][0] = w[1][3]
        w[0][3] = x1
        w[1][2] = x2
        w[1][3] = x3
        w[1][1] = x4
        w[0][1] = x5
        w[1][0] = x6
        w[0][2] = x7
        w[0][0] = x8
        # print 'after gamma step',w
        # iota step
        w[0][0] = Keccak.rotl(w[0][0])
        w[1][0] = Keccak.rotl(w[1][0])
        w[0][2] = Keccak.rotl(w[0][2])
        w[1][2] = Keccak.rotl(w[1][2])

        w[0][1] = Keccak.rotr(w[0][1])
        w[1][1] = Keccak.rotr(w[1][1])
        w[0][3] = Keccak.rotr(w[0][3])
        w[1][3] = Keccak.rotr(w[1][3])
        # print 'after iota step',w
    @staticmethod
    def delta(w):
        for _ in xrange(50):
            Keccak.Round(w)

    def absorbing(self):
        r = self.r
        c = self.c
        data = [ord(i) for i in self.data]
        while len(data) % 4 != 0:
            data.append(0)
        # print data
        mid = []
        for idx in xrange(0,len(data),4):
            mid.append([data[idx+i] for i in xrange(4)])
        #print 'mid: ',mid
        #print 'r,c: ',r,c

        for j in xrange(len(mid)):
            r = [(a^b)%256 for a,b in zip(r,mid[j])]
            w = [r,c]
            #print 'r before delta',r
            #print 'c before delta',c
            Keccak.delta(w)
            r = w[0]
            c = w[1]
            #print 'r after delta',r
            #print 'c after delta',c


        self.r = r
        self.c = c
        #print self.r
        #print self.c

    def squeezing(self):
        r = self.r
        c = self.c

        for i in xrange(2):
            w = [r,c]
            Keccak.delta(w)
            r = w[0]
            c = w[1]
            print ('z'+str(i+1)+': 0x'+ ''.join([hex(i)[2:].zfill(2) for i in r]))
    def hex(self):
        self.absorbing()
        return '0x'+ ''.join([hex(i)[2:].zfill(2) for i in self.r])
        # self.squeezing()

if __name__ == '__main__':
    test1 = Keccak('HELLOWORLD')
    test1.hex()
    test2 = Keccak('GOODBYEWORLD')
    test2.hex()
    h = []
    def test(t):
        new_test = Keccak(t)
        return new_test.hex()
    #for n in xrange(1,1000000):
    #    m = encode(long_to_bytes(n))
    #    c_hash = test(m)
    #    if c_hash in h:
    #        print "[+] hit",c_hash
    #        print str(n)+":"+m
    #        print str(h.index(c_hash)+1) + ":" + encode(long_to_bytes(h.index(c_hash)))
    #        break
    #    else:
    #        h.append(c_hash)
