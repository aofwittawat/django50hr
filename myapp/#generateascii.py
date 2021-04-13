#generateascii.py
import random

def GenerateToken(domain='http://127.0.0.1:8000/confirm/'):
	allchar = [chr(i) for i in range(65,91)]
	allchar.extend([chr(i) for i in range(97,123)])
	allchar.extend([str(i) for i in range(10)])
	emailtoken = ''
	for i in range(40):
		emailtoken += random.choice(allchar)

	url = domain + emailtoken
	#print(url)
	return url

GenerateToken()






'''allchar = []
for i in range(65,91):
	allchar.append(chr(i))
for i in range(97,123):
	allchar.append(chr(i))
for i in range(10):
	allchar.append(str(i))
print(allchar)

print('------')
allchar = [chr(i) for i in range(65,91)]
allchar.extend([chr(i) for i in range(97,123)])
allchar.extend([str(i) for i in range(10)])
print(allchar)
import string
print(list(string.ascii_lowercase))'''