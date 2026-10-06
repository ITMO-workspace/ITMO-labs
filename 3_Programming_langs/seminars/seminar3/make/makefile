ASM=nasm
ASMFLAGS=-f elf64
LD=ld

a.o: a.asm
    $(ASM) $(ASMFLAGS) -o a.o a.asm

b.o: b.asm a.o
    $(ASM) $(ASMFLAGS) -o b.o b.asm

c.o: c.asm a.o
    $(ASM) $(ASMFLAGS) -o c.o c.asm

program: a.o b.o c.o
    $(LD) -o program a.o b.o c.o