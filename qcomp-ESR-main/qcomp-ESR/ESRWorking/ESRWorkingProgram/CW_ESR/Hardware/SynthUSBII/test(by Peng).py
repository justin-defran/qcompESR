import visa,sys,traceback, time

rm = visa.ResourceManager()
syn = rm.open_resource("COM3")
amp = rm.open_resource("COM7")

amp.write("a50")
syn.write("f3000")


print syn.query("?")
print amp.query("?")

