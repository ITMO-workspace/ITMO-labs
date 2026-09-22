; print_string.asm 
section .data
message:       db  'hello, world!', 10, 0
error_message: db  'hello, errors!', 10, 0

section .text
global _start

exit:
    mov  rax, 60
    xor  rdi, rdi          
    syscall

string_length:
    xor rax, rax
    .counter:
        cmp byte[rdi + rax], 0
        je .end
        inc rax
        jmp .counter
    .end:
        ret

print_string:
    push rdi
    call string_length
    pop rdi
    mov rdx, rax
    mov rsi, rdi
    mov  rax, 1
    mov  rdi, 1
    syscall
    ret

_start:
    mov  rdi, message
    call print_string

    mov  rdi, error_message
    call print_string
    
    jmp exit