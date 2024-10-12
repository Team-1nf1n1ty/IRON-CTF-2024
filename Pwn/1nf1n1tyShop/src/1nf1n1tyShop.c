#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>

void flag(){
    printf("flag{nope_no_flag_for_you!}");
    asm(
        "sub esp, 0x30\n"
        "ret\n"
    );
}

void food(){
    char food[160];
    printf("What food would you like?\n>");
    read(0, food, 176);
    return;
}

void mystery(char *name){
    if(!strcmp(name, "hacker\n")){
        printf("Your prize: %p;)\n", &system);
    }
    else{
        printf("Your prize: %p;)\n", &flag);
    }
}

//gcc 1nf1n1tyShop.c -o 1nf1n1tyShop  -masm=intel -O0
int main()
{
    setvbuf(stdout, NULL, _IONBF, 0);
    printf("Welcome to 1nf1n1ty Shop! The shop for elite travellers\n");
    printf("Enter Your Name:\n>");
    char name[24];
    memset(name, 0, 24);
    read(0, name, 24);
    printf("Hello, %s", name);
    printf("Before, you start with your journey would you like to buy some items? :)\n");
    int option;
    while (1){
        printf("1) Water Bottle, 2) Food, 3) Pillow, 4) Mystery Prize, 5) No Thanks (leave)\n>");
        scanf("%d", &option);
        
        if(option==1){
            puts("Here Have your water bottle, Stay Hydrated!");
        }
        else if(option==2){
            food();
            printf("Got it!\n");
        }
        else if(option==3){
            puts("Shame on you, hackers dont sleep!\n");
            return 0;
        }
        else if(option==4){
            mystery(name);
        }
        else if(option==5){
            printf("Good luck :)\n");
            return 0;
        }

        printf("Would you like more items?\n");
    }
    return 0;
}
