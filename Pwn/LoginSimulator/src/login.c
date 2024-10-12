#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>

struct user{
    char name[20];
    char password[20];
} users[5];

void setup() {
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
}

void register_user(int i)
{
    if (i >= 5){
        printf("Max users reached!\n");
        return;
    }
    printf("Enter your name: ");
    scanf("%20s", users[i].name);
    printf("Enter new password: ");
    scanf("%20s", users[i].password);
}

void view_user(int j)
{
    int i;
    printf("Enter user id: ");
    scanf("%d", &i);

    if (i >= j || i < 0){
        printf("Invalid id!\n");
        exit(1);
    }

    printf("Name: %s\n", users[i].name);
}

int login()
{
    printf("Enter your user id: ");
    int i;
    scanf("%d", &i);

    if (i >= 5 || i < 0){
        printf("Invalid id!\n");
        exit(1);
    }

    printf("Enter your password: ");
    char input[20];
    scanf("%20s", input);
    if (strcmp(input, users[i].password))
    {
        printf("Invalid password!\n");
        exit(1);
    }

    printf("Successfully logged in!\n");
    return i;
}

void change_password()
{
    char buf[100];
    int i = login();
    printf("Enter new password: ");
    scanf("%s", buf);
    if(strlen(buf) <= 20){
        strcpy(users[i].password, buf);
        printf("Password Changed Successfully!\n");
    }
    else{
        printf("Before we continue how much would you like to rate our application: ");
        scanf("%lf", (int*)(buf+strlen(buf)-4));
        printf("%s is not a valid password!\n", buf);
    }
}

void control_panel() // TODO
{
    char buf[400];
    printf("Enter command: ");
    read(0, buf, 0x400);
    asm("syscall");
}

int main()
{
    setup();
    int op;
    int i = 0;
    int user_id;
    printf("Welcome to login simulator! The most secure login system.\n");
    int changed = 0;
    while(1)
    {
        printf("=====Menu=====\n");
        printf("1) Register\n");
        printf("2) View User\n");
        printf("3) Change Password\n");
        printf("> ");
        scanf("%d", &op);

        switch (op)
        {
            case 1:
                register_user(i);
                i++;
                break;
            case 2:
                view_user(i);
                break;
            case 3:
                if(changed){
                    printf("Too many resets, try again after 2hrs\n");
                    continue;
                }
                changed = 1;
                change_password();
                break;
            case 1337:
                control_panel();
                break;
        }
    }
    return 0;
}