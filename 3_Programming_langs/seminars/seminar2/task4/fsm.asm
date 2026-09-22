; finite state machine realisation for parse_uint

section .data
message:       db  'ab1c23x', 10

section .text
global _start

exit:
    mov rax, 60
    xor rdi, rdi
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
    mov rsi, rdi
    mov  rax, 1
    mov  rdi, 1
    syscall
    ret

; Принимает указатель на строку, пытается
; прочитать из её начала беззнаковое число.
; Возвращает в rax: число, rdx : его длину в символах
; rdx = 0 если число прочитать не удалось
parse_uint:
    xor eax, eax
    xor edx, edx

    call loop_symbol
    mov r8, rax
    call string_length
    mov rdx, rax
    mov rax, r8
    ret



loop_symbol:
    .counter:
        mov cl, byte[rdi]
        cmp cl, 0
        je .return
        sub rcx, '0'
        cmp rcx, '9' 
        inc rdi
        ja .counter

        imul rax, rax, 10
        add  rax, rcx

        inc rdx
        jmp .counter

    .return:
        ret




_start:
    mov  rdi, message
    call parse_uint
    mov rdi, rax
    call print_string