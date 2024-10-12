section .data
msg1 db '             ,', 10
     db '            /|      __', 10
     db '           / |   ,-~ /', 10
     db '          Y :|  //  /', 10
     db '          | jj /( .^', 10
     db '          >-"~"-v"', 10
     db '         /       Y', 10
     db '        jo  o    |', 10
     db '       ( ~T~     j', 10
     db '        >._-"" _./', 10
     db '       /   "~"  |', 10
     db '      Y     _,  |', 10
     db '     /| ;-~ _  l', 10
     db '    / l/ ,-~    \', 10
     db '    \//\/      .- \', 10
     db '     Y        /    Y', 10
     db '     l       I     !', 10
     db '     ]\      _\    /"\', 10
     db '    (" ~----( ~   Y.  )', 10
len1 equ $ - msg1

msg2 db '╭╮╱╭┳━━━╮╱╱╱    ╭╮╱╭━━━╮', 10
     db '┃┃╱┃┃╭━╮┃╱╱╱    ┃┃╱┃╭━╮┃', 10
     db '┃╰━╯┃┃┃┃┣━━╮    ┃╰━┫┃╱┃┣━━╮', 10
     db '┃╭━╮┃┃┃┃┃╭╮┃    ┃╭╮┃┃╱┃┃╭╮┃', 10
     db '┃┃╱┃┃╰━╯┃╰╯┃    ┃┃┃┃╰━╯┃╰╯┃', 10
     db '╰╯╱╰┻━━━┫╭━╯    ╰╯╰┻━━━┫╭━╯', 10
     db '╱╱╱╱╱╱╱╱┃┃╱    ╱╱╱╱╱╱╱╱┃┃', 10
     db '╱╱╱╱╱╱╱╱╰╯╱    ╱╱╱╱╱╱╱╱╰╯', 10
     db '>> '
len2 equ $ - msg2

section .text
global _start

print:
    mov rax, 1
    mov rdi, 1
    syscall
    xchg r13, rax
    jmp [rsp]
    
dispatcher:
    add rbx, 8
    xor r15, r15
    jmp [rbx]

gadgets:
    pop rsi
    pop rdi
    pop rbx
    pop r13
    pop r15
    jmp r15

    xor rdx, rdx
    jmp r15

    xor rsi, rsi
    jmp r15

    xor rdi, rdi
    jmp r15


_start:
    mov rsi, msg1       
    mov rdx, len1       
    call print

    push rsp
    mov rsi, rsp
    mov rdx, 8
    call print

    mov rsi, msg2      
    mov rdx, len2       
    call print

    xor rax, rax
    xor rdi, rdi
    mov rsi, rsp
    mov rdx, 1337
    syscall
    jmp [rsp]
