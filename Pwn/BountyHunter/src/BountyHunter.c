#include <stdio.h>
#include <fcntl.h> 
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/mman.h>
#include <seccomp.h>
#include <errno.h>
#include <sys/time.h>

void* generate_random_address() {
    struct timeval time;
    gettimeofday(&time, NULL);
    srandom((unsigned int)(time.tv_sec ^ time.tv_usec));
    uintptr_t random_addr = (random() % 0x0000500000000000);
    return (void*)random_addr;
}

void setup_seccomp() {
    scmp_filter_ctx ctx;
    ctx = seccomp_init(SCMP_ACT_KILL); 
    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(read), 0);
    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(write), 0);
    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(access), 0);
    seccomp_load(ctx);
    seccomp_release(ctx);
}

void* create_mmap_and_input(size_t size) {
    void* addr = mmap(NULL, size, PROT_READ | PROT_WRITE, MAP_ANONYMOUS | MAP_PRIVATE, -1, 0);
    printf("Unleash your hunter>> ");
    read(STDIN_FILENO, addr, size - 1);
    mprotect(addr, size, PROT_READ | PROT_EXEC);
    return addr;
}

void* create_flag_segment(size_t size, const char* flag) {
    void* random_addr = generate_random_address();
    void* addr = mmap(random_addr, size, PROT_READ | PROT_WRITE, MAP_ANONYMOUS | MAP_PRIVATE, -1, 0);
    memcpy(addr, flag, strlen(flag));
    return addr;
}


void setup() {
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
}

int main() {
    setup();
    size_t size = 4096;

    int fd = open("flag.txt", O_RDONLY);
    char flag[50];
    read(fd, flag, sizeof(flag) - 1);
    close(fd);
    
    create_flag_segment(size, flag);
    memset(flag, 0, strlen(flag));
    void* input_segment = create_mmap_and_input(size);
    setup_seccomp();
    void (*user_code)() = (void (*)())input_segment;
    user_code();
    return 0;
}
