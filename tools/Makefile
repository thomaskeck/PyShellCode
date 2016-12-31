all:
	gcc probabilistic_password_checker.c -o probabilistic_password_checker
	nasm -f elf64 simple_cache_leak_test.asm -o simple_cache_leak_test.o
	ld simple_cache_leak_test.o -o simple_cache_leak_test -s --build-id=none
	# gcc simple_cache_leak_test.c -o simple_cache_leak_test -Os  -fno-unwind-tables -fno-asynchronous-unwind-tables -s -fno-ident -Wl,--build-id=none
