    .data

input_addr:      .word  0x80               ; Input address where the number 'n' is stored
output_addr:     .word  0x84               ; Output address where the result should be stored

    .text
    .org     0x90

; Idea: 1 + 3 + 5 + ... + (2k - 1) = k^2, where k = number of odd numbers in 1..n = (n + 1) / 2
;
; Calling convention: argument and result in a0, return address in ra,
; every procedure that calls another one saves ra on the stack.
;
; Call tree:
;   _start
;   `-- sum_odd_n
;       |-- sum_odd_n_count
;       `-- sum_odd_n_square
;           `-- sum_odd_n_overflow

_start:
    lui      t0, %hi(input_addr)
    addi     t0, t0, %lo(input_addr)
    lw       t0, 0(t0)                       ; t0 <- 0x80
    lw       a0, 0(t0)                       ; a0 <- n

    lui      sp, %hi(0x800)                  ; set up the stack pointer
    addi     sp, sp, %lo(0x800)

    jal      ra, sum_odd_n                   ; a0 <- sum_odd_n(a0)

    lui      t0, %hi(output_addr)
    addi     t0, t0, %lo(output_addr)
    lw       t0, 0(t0)                       ; t0 <- 0x84
    sw       a0, 0(t0)                       ; output <- result

    halt

; a0 = n -> a0 = sum of odd numbers in 1..n, -1 if n <= 0, 0xCCCCCCCC on overflow
sum_odd_n:
    addi     sp, sp, -4                      ; prologue
    sw       ra, 0(sp)

    slti     t0, a0, 1                       ; t0 <- (n < 1)
    bnez     t0, sum_odd_n_not_in_domain

    jal      ra, sum_odd_n_count             ; a0 <- k
    jal      ra, sum_odd_n_square            ; a0 <- k * k
    j        sum_odd_n_return

sum_odd_n_not_in_domain:
    addi     a0, zero, -1

sum_odd_n_return:
    lw       ra, 0(sp)                       ; epilogue
    addi     sp, sp, 4
    jalr     zero, ra, 0

; a0 = n -> a0 = how many odd numbers are in 1..n
sum_odd_n_count:
    addi     a0, a0, 1                       ; logical shift, so n = 0x7FFFFFFF is fine
    srli     a0, a0, 1
    jalr     zero, ra, 0

; a0 = k -> a0 = k * k, or 0xCCCCCCCC if it does not fit into int32
sum_odd_n_square:
    addi     sp, sp, -4                      ; prologue
    sw       ra, 0(sp)

    mulh     t0, a0, a0                      ; t0 <- high 32 bits of k * k
    mul      a0, a0, a0                      ; a0 <- low 32 bits of k * k
    bnez     t0, sum_odd_n_square_overflow   ; does not fit into 32 bits
    blt      a0, zero, sum_odd_n_square_overflow ; bit 31 is set: over INT32_MAX
    j        sum_odd_n_square_return

sum_odd_n_square_overflow:
    jal      ra, sum_odd_n_overflow          ; a0 <- 0xCCCCCCCC

sum_odd_n_square_return:
    lw       ra, 0(sp)                       ; epilogue
    addi     sp, sp, 4
    jalr     zero, ra, 0

; -> a0 = 0xCCCCCCCC
sum_odd_n_overflow:
    lui      a0, %hi(0xCCCCCCCC)
    addi     a0, a0, %lo(0xCCCCCCCC)
    jalr     zero, ra, 0
