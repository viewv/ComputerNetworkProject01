import ByteFill.decode as bd
import ByteFill.generate as bg

message = '1b7d7d7e7d7d7e23'
print("Init Message", message)
message = bg.fill(message)
print("Encode", message)
message = bd.decode(message)
print("After Decode", message)

