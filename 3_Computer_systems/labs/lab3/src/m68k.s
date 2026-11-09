    .data
.org             0x00

; Two line buffers, 0x20 bytes each (31 characters + terminator), initial value '_'
pattern_buf:     .byte  '________________________________'
text_buf:        .byte  '________________________________'

    .text
    .org     0x100

; Algorithm (recursive, with backtracking, as in the Python reference):
;   match(p, t):
;     p == ""    -> t == ""
;     p[0] == '*' -> match(p + 1, t) or (t != "" and match(p, t + 1))
;     t == ""    -> false
;     p[0] == '?' or p[0] == t[0] -> match(p + 1, t + 1)
;     otherwise  -> false
;
; Registers:
;   A4 -- output port (0x84)             global
;   A5 -- input port (0x80)              global
;   A6 -- frame pointer (link / unlk)
;   A7 -- stack pointer
; Calling convention: arguments in D0, D1; result in D0. Pointers are kept in
; data registers, an address register is loaded only when memory is accessed.
;
; Call tree:
;   _start
;   |-- read_line                  (twice)
;   `-- glob_match                 (recursive)

_start:
    movea.l  0x800, A7                       ; stack pointer
    movea.l  0x80, A5                        ; input port
    movea.l  0x84, A4                        ; output port

    move.l   pattern_buf, D0
    jsr      read_line                       ; D0 <- 1 if the line fits into the buffer
    cmp.l    0, D0
    beq      overflow

    move.l   text_buf, D0
    jsr      read_line
    cmp.l    0, D0
    beq      overflow

    move.l   pattern_buf, D0                 ; D0 <- p
    move.l   text_buf, D1                    ; D1 <- t
    jsr      glob_match                      ; D0 <- 1 or 0
    move.l   D0, (A4)                        ; output <- result
    halt

overflow:
    move.l   0xCCCCCCCC, (A4)                ; output <- overflow marker
    halt

; ----------------------------------------------------------------------

; D0 = buffer address. Reads a line from the input port into the buffer and
; terminates it with 0. D0 <- 1 on success, 0 if the line has more than 31 characters
; (the 32nd character is consumed, the rest of the line is left in the input).
read_line:
    move.l   D3, -(A7)                       ; save D3
    movea.l  D0, A2                          ; A2 <- buffer
    clr.l    D3                              ; D3 <- number of characters read

read_line_loop:
    move.l   (A5), D1                        ; D1 <- next character
    cmp.l    0x0A, D1                        ; '\n'
    beq      read_line_done                  ; end of line
    cmp.l    31, D3
    beq      read_line_overflow              ; no room for one more character
    move.b   D1, 0(A2,D3)                    ; buffer[D3] <- character
    add.l    1, D3
    jmp      read_line_loop

read_line_done:
    move.b   0, 0(A2,D3)                     ; buffer[D3] <- 0
    move.l   1, D0
    jmp      read_line_return

read_line_overflow:
    clr.l    D0

read_line_return:
    move.l   (A7)+, D3                       ; restore D3
    rts

; ----------------------------------------------------------------------

; D0 = pattern, D1 = text -> D0 = 1 if the text matches the pattern, else 0.
; Frame: -4(A6) = pattern, -8(A6) = text.
glob_match:
    link     A6, -8
    move.l   D0, -4(A6)
    move.l   D1, -8(A6)

    movea.l  D0, A0
    move.b   (A0), D2                        ; D2 <- p[0]
    cmp.b    0, D2
    beq      glob_match_pattern_end
    cmp.b    '*' , D2
    beq      glob_match_star

    movea.l  D1, A1
    move.b   (A1), D3                        ; D3 <- t[0]
    cmp.b    0, D3
    beq      glob_match_fail                 ; pattern is not over, text is
    cmp.b    '?' , D2
    beq      glob_match_next                 ; '?' matches any character
    cmp.b    D3, D2
    bne      glob_match_fail                 ; p[0] != t[0]

; return match(p + 1, t + 1)
glob_match_next:
    move.l   -4(A6), D0
    add.l    1, D0
    move.l   -8(A6), D1
    add.l    1, D1
    jsr      glob_match
    jmp      glob_match_return

; '*' matches an empty sequence
glob_match_star:
    move.l   -4(A6), D0
    add.l    1, D0
    move.l   -8(A6), D1
    jsr      glob_match                      ; match(p + 1, t)
    cmp.l    0, D0
    bne      glob_match_return               ; matched

    move.l   -8(A6), D1                      ; '*' absorbs one more character
    movea.l  D1, A1
    move.b   (A1), D3
    cmp.b    0, D3
    beq      glob_match_fail                 ; no characters left
    add.l    1, D1
    move.l   -4(A6), D0
    jsr      glob_match                      ; match(p, t + 1)
    jmp      glob_match_return

; p == "": t must be empty too
glob_match_pattern_end:
    movea.l  D1, A1
    move.b   (A1), D3
    cmp.b    0, D3
    bne      glob_match_fail

    move.l   1, D0
    jmp      glob_match_return

glob_match_fail:
    clr.l    D0

glob_match_return:
    unlk     A6
    rts
