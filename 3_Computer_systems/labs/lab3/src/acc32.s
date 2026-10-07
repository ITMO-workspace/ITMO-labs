; reverse_string_pstr

    .data
    .org 0x0

input_addr:      .word 0x80
output_addr:     .word 0x84
const_newline:   .word 0x0A
const_max:       .word 0x1F
const_space:     .word 0x20
const_one:       .word 0x01
const_two:       .word 0x02
const_four:      .word 0x04
const_40:        .word 0x40
const_pad:       .word 0x5F5F5F00
const_fill:      .word 0x5F5F5F5F
const_error:     .word 0xFFFFFFFF
const_overflow:  .word 0xCCCCCCCC
mask:            .word 0x000000FF

index:           .word 0
cur_char:        .word 0
ptr:             .word 0
left:            .word 0
temp:            .word 0

    .text
    .org 0x88
_start:
    ; fill mem[0x00..0x1F] with 0x5F
    load_addr const_fill
    store_addr 0x00
    store_addr 0x04
    store_addr 0x08
    store_addr 0x0C
    store_addr 0x10
    store_addr 0x14
    store_addr 0x18
    store_addr 0x1C

    load_imm 0
    store_addr index
    load_addr const_40
    store_addr ptr

read_loop:
    load_addr input_addr
    load_acc
    store_addr cur_char

    sub const_newline
    beqz end_read

    load_addr index
    sub const_max
    bgez overflow

    load_addr cur_char
    sub const_space
    bltz domain_err

    ; scratch[index] = 0x5F5F5F00 | char
    load_addr cur_char
    add const_pad
    store_ind ptr

    load_addr ptr
    add const_four
    store_addr ptr

    load_addr index
    add const_one
    store_addr index
    jmp read_loop

end_read:
    ; mem[0] = length
    load_imm 0
    store_addr ptr
    load_addr index
    store_ind ptr

    ; copy reversed: for left = 1..N: mem[left] = scratch[N-left]
    load_addr const_one
    store_addr left

copy_loop:
    load_addr left
    sub index
    bgtz emit_start

    ; ptr = 0x40 + (index - left) * 4
    load_addr index
    sub left
    store_addr temp
    load_addr temp
    shiftl const_two
    add const_40
    store_addr ptr

    load_addr ptr
    load_acc
    store_addr temp

    load_addr left
    store_addr ptr
    load_addr temp
    store_ind ptr

    load_addr left
    add const_one
    store_addr left
    jmp copy_loop

emit_start:
    load_addr const_one
    store_addr left

emit_loop:
    load_addr left
    sub index
    bgtz done

    load_addr left
    load_acc
    and mask
    store_ind output_addr

    load_addr left
    add const_one
    store_addr left
    jmp emit_loop

done:
    halt

overflow:
    load_addr const_overflow
    store_ind output_addr
    halt

domain_err:
    load_addr const_error
    store_ind output_addr
    halt