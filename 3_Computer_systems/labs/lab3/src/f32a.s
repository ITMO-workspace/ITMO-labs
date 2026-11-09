    .data

input_addr:      .word  0x80               \ Input address where the number 'n' is stored
output_addr:     .word  0x84               \ Output address where the result should be stored

    .text
    .org 0x90

\ Idea (Kernighan): n & (n - 1) clears the lowest set bit of n,
\ so the number of iterations until n == 0 is the number of ones.
\ It works on the whole 32-bit word, so negative numbers are counted as unsigned
\ (-1 -> 32, -2 -> 31), and no shifts are needed.
\
\ Stack comments: the top of the stack is on the left, as in the examples.
\ Register A is used as the counter of ones, so the data stack holds only n.
\
\ Call tree:
\   _start
\   `-- count_ones
\       |-- count_ones_reset
\       |-- count_ones_clear_lowest_bit
\       |-- count_ones_increment
\       `-- count_ones_result

_start:
    @p input_addr a! @       \ n:[]

    count_ones               \ ones:[]

    @p output_addr a! !      \ []
    halt

\ ----------------------------------------------------------------------

\ n:[] => ones:[]
count_ones:
    count_ones_reset         \ n:[]; A = 0
count_ones_while:
    dup                      \ n:n:[]
    if count_ones_finish     \ n:[]; leave if n == 0

    count_ones_clear_lowest_bit \ n':[]
    count_ones_increment     \ n':[]; A = A + 1

    count_ones_while ;

count_ones_finish:
    drop                     \ []
    count_ones_result        \ ones:[]
    ;

\ ----------------------------------------------------------------------

\ => A = 0
count_ones_reset:
    0 a!
    ;

\ n:[] => n & (n - 1):[]
count_ones_clear_lowest_bit:
    dup                      \ n:n:[]
    -1 +                     \ n-1:n:[]
    and                      \ n&(n-1):[]
    ;

\ => A = A + 1
count_ones_increment:
    a 1 + a!
    ;

\ [] => A:[]
count_ones_result:
    a
    ;
