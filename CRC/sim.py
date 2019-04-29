import CRC.generate as cg
import CRC.verify as cf

binmessage = 0b010011011101010
hexmessage = hex(binmessage)[2:]

print(cg.generate((hexmessage)))
sendmessage = hexmessage + cg.generate(hexmessage)
print('Send Message:',sendmessage)
print('Verify:',cf.verify(sendmessage))
print('Error Message')

errormessage = list(sendmessage)
errormessage[0] = 'b'
errormessage[3] = 'c'
errormessage = ''.join(errormessage)
print('errormessage:',errormessage)
print('Test Verify:',cf.verify(errormessage))

