import javaobj
import base64

with open("obj.ser", "rb") as fd:
    jobj = fd.read()

jobj=base64.b64decode(jobj)
print(jobj)
pobj = javaobj.loads(jobj)
print(pobj)