import pyasn1.codec.der.encoder
import pyasn1.type.univ
import base64

e = 0x010001
n = 0x0e5b138de1554e0a38040b3dfc4c79c5453a89636804363c27bb6ebafec834c98c3a06282055
p = 1332830227949273521465367319234277279439624789
q = 1371293089587387292180481293784036793076837889
template = '-----BEGIN RSA PRIVATE KEY-----\n{}-----END RSA PRIVATE KEY-----\n'

def egcd(a, b):
	x,y, u,v=0,1, 1,0
	while a != 0:
		q,r = b//a, b%a
		m,n = x-u*q, y-v*q
		b,a, x,y, u,v=a,r, u,v, m,n
	gcd=b
	return gcd,x,y
 
def modinv(a, m):
	gcd, x, y = egcd(a, m)
	if gcd != 1:
		return None  
	else:
		return x % m
		
def main():
	phi = (p -1)*(q-1)
	d = modinv(e,phi)
	dp = modinv(e,(p-1))
	dq = modinv(e,(q-1))
	qi = modinv(q,p)
	seq = pyasn1.type.univ.Sequence()
	for i,x in enumerate((0, n, e, d, p, q, dp, dq, qi)):
		seq.setComponentByPosition(i, pyasn1.type.univ.Integer(x))
	der = pyasn1.codec.der.encoder.encode(seq)
	key = template.format(base64.encodebytes(der).decode('ascii'))
	print(key)
	f = open("private.key","w")
	f.write(key)
	f.close()

main()



