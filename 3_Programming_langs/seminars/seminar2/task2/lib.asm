; lib.asm

string_length:
    xor rax, rax
    .counter:
        cmp byte[rdi + rax], 0
        je .end
        inc rax
        je .counter
    .end:
        ret

print_string:
    call string_length
    mov rdx, rax
    mov rsi, rdi
    
    mov  rax, 1
    mov  rdi, 1
    syscall
    ret