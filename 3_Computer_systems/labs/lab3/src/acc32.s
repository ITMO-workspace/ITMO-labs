    .data
.org             0x00

; Result buffer: 0x20 bytes at 0x00, initial value '_'. Layout: [length][reversed characters]
buf:             .byte  '________________________________'
; Padding: a word store at buf[31] spills over 3 bytes after the buffer.
buf_pad:         .word  0

; Constants
const_1:         .word  1
const_2:         .word  2
const_4:         .word  4
const_newline:   .word  0x0A               ; End of input
const_fill:      .word  0x5F5F5F00         ; "___" in the three upper bytes, see 'store_ind buf_wptr'
const_overflow:  .word  0xCCCCCCCC

; Scratch stack for the characters: one word per character, grows up from 0x300.
; Max 31 characters, so the limit is 0x300 + 31 * 4 = 0x37C.
stack_base:      .word  0x300
stack_limit:     .word  0x37C

; Variables
char:            .word  0                  ; The last read character
sp:              .word  0                  ; Address of the first free word in the scratch stack
buf_wptr:        .word  0                  ; Address in buf where the next character will be written

    .text
    .org         0x90

; Algorithm:
;   1. Read characters from 0x80 and push each of them to the scratch stack.
;      Stop at '\n'. If the 32nd character is not '\n' -- overflow.
;   2. length <- (sp - stack_base) / 4, write it as the first byte of buf.
;   3. Pop characters (they come in reverse order), print each to 0x84
;      and write it to buf.
;
; Each character is written to buf with a word store (acc32 has no byte store).
; A word store writes 4 bytes: <char> + 3 bytes of const_fill ("___").
; Characters go in ascending order, so every next store overwrites the spill of
; the previous one, and after the last character the tail is exactly '_'.
;
; load_addr/store_addr are used everywhere, because the data is further than
; 127 bytes from some instructions, which is the limit of load/store.

_start:
    load_addr    stack_base
    store_addr   sp                          ; sp <- stack_base

; do {
read_loop:
    load_addr    0x80                        ;     acc <- next input character
    store_addr   char
    sub          const_newline
    beqz         read_done                   ;     if (char == '\n') break

    load_addr    sp
    sub          stack_limit
    beqz         overflow                    ;     if (stack is full) goto overflow

    load_addr    char
    store_ind    sp                          ;     *sp <- char
    load_addr    sp
    add          const_4
    store_addr   sp                          ;     sp += 4
    jmp          read_loop                   ; }

read_done:
    load_addr    sp
    sub          stack_base
    shiftr       const_2                     ; acc <- length
    or           const_fill
    store_addr   buf                         ; buf[0] <- length, buf[1..3] <- '_'

    load_imm     buf
    add          const_1
    store_addr   buf_wptr                    ; buf_wptr <- buf + 1

    load_addr    sp
    sub          const_4
    store_addr   sp                          ; sp <- address of the last pushed character

; while (sp >= stack_base) {
write_loop:
    load_addr    sp
    sub          stack_base
    bltz         write_done

    load_addr    sp
    load_acc                                 ;     acc <- *sp
    store_addr   0x84                        ;     print the character
    or           const_fill
    store_ind    buf_wptr                    ;     *buf_wptr <- char, spill '___'

    load_addr    buf_wptr
    add          const_1
    store_addr   buf_wptr                    ;     buf_wptr += 1

    load_addr    sp
    sub          const_4
    store_addr   sp                          ;     sp -= 4
    jmp          write_loop                  ; }

write_done:
    halt

overflow:
    load_addr    const_overflow
    store_addr   0x84                        ; output <- 0xCCCCCCCC
    halt
