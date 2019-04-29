import BitFill.generate as bg
import BitFill.decode as bd


initframe = '101110111111101011'
print("Init:", initframe)
frame = bg.generate(initframe)
print("Frame:", frame)
frame = bd.decode(frame)
print("Final:", frame)

l = bd.decode(
    '010111010111111010111011111011010110111111010000101101111110101110111110110101101111110')
for x in l:
    print(x)