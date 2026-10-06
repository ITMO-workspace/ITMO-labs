ASM=nasm
ASMFLAGS=-f elf64

%.o: %.asm
	$(ASM) $(ASMFLAGS) $< -o $@


build: lib.o main.o
	@echo "PERFORMING: $@"
	ld -o main main.o lib.o
	chmod a+x ./main

run:
	@echo "PERFORMING: $@"
	./main

clean:
	@echo "PERFORMING: $@"
	rm *.o
