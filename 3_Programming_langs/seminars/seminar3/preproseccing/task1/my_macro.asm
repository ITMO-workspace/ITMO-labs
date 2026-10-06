%macro pushn 2-*
    push %1
    %rep %0 - 1
        push %2
        %rotate 1
    %endrep
%endmacro

%macro popn 2-*
    pop %1
    %rep %0 - 1
        pop %2
        %rotate 1
    %endrep
%endmacro

pushn rax, rdx

popn rdi, rax
