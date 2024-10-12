#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>

char *notes[50];

void add_note()
{
    int i, n;
    printf("Enter the id of note: ");
    scanf("%d", &i);
    if (i < 0 || i >= 50)
    {
        printf("Invalid Id!\n");
        return;
    }
    printf("Enter the size of note: ");
    scanf("%d", &n);
    char *data = (char*)malloc(sizeof(char)*n);
    notes[i] = data;
    printf("Enter the note: ");
    read(0, notes[i], n);
}

void delete_note()
{
    int i;
    printf("Enter the id of note: ");
    scanf("%d", &i);
    if (i < 0 || i >= 50)
    {
        printf("Invalid Id!\n");
        return;
    }
    free(notes[i]);
}

void edit_note()
{
    int i, n;
    printf("Enter the id of note: ");
    scanf("%d", &i);
    if (i < 0 || i >= 50)
    {
        printf("Invalid Id!\n");
        return;
    }
    printf("Enter the size of note: ");
    scanf("%d", &n);
    printf("Enter the note: ");
    read(0, notes[i], n);
}

void read_note()
{
    int i;
    printf("Enter the id of note: ");
    scanf("%d", &i);
    if (i < 0 || i >= 50)
    {
        printf("Invalid Id!\n");
        return;
    }
    printf("%s\n", notes[i]);
}

void setup() {
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
}

int main()
{
    setup();
    memset(notes, 0, sizeof(notes));
    printf("1) Create Note\n2) Edit Note\n3) Delete Note\n4) Read Note\n5) Exit\n");
    while(1)
    {
        printf(">> ");
        int option;
        scanf("%d", &option);
        if (option == 1)
        {
            add_note();
        }
        else if(option == 2)
        {
            edit_note();
        }
        else if(option == 3)
        {
            delete_note();
        }
        else if(option == 4)
        {
            read_note();
        }
        else if(option == 5)
        {
            exit(0);
        }
        else{
            printf("Invalid Option!\n");
        }
    }
}
