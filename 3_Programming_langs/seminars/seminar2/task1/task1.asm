; task1.asm

section .text
global _start

exit:
    mov rax, 60
    xor rdi, rdi
    syscall

g:
    ret

f:
    call g
    ret


_start:
    call f
    call exit