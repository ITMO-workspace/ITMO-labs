%macro alloc_string 1-* "Hello, world!", 10, 0
  %1:
  %rep %0 - 1
    db %2
    %rotate 1
  %endrep
%endmacro

alloc_string msg1
alloc_string msg2, "hello", "!"
