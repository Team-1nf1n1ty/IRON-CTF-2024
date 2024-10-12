#include <stdio.h>
#include <unistd.h>
#include <string.h>

void setup() {
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
}
// gcc blind.c -o blind -no-pie -Wl,-z,relro,-z,now
int main()
{
    setup();
    printf("Its too dark here...\n");
    char buf[1000];
    memset(buf, 0, 1000);
    while(1)
    {
        printf(">>> ");
        read(0, buf, 1000);
        printf(buf);
    }
}
