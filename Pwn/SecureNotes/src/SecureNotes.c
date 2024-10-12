#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>

char *notes[50];
int size[50];

void add_note()
{
    int i;
    printf("Enter the id of note: ");
    scanf("%d", &i);
    if (i < 0 || i >= 50)
    {
        printf("Invalid Id!\n");
        return;
    }
    char buf[1024];
    printf("Enter the note: ");
    int length = read(0, buf, 1023);
    size[i] = length;
    buf[length] = 0;
    notes[i] = (char*)malloc(length);
    strcpy(notes[i], buf); 
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
    if (notes[i]){
        free(notes[i]);
        notes[i] = NULL;
        size[i] = 0;
    }
    else{
        printf("The note of given id doesn't exist!\n");
    }
}

void edit_note()
{
    int i;
    printf("Enter the id of note: ");
    scanf("%d", &i);
    if (i < 0 || i >= 50)
    {
        printf("Invalid Id!\n");
        return;
    }
    if(notes[i] == NULL)
    {
        printf("The note of given id doesn't exist!\n");
        return;
    }
    printf("Enter the note: ");
    int length = read(0, notes[i], size[i]);
    *(notes[i]+length) = 0;
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
    if(notes[i] != NULL)
    {
        printf("%s\n", notes[i]);
    }
    else{
         printf("The note of given id doesn't exist!\n");
    }
}

void setup() {
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
}

int main()
{
    setup();
    memset(notes, 0, sizeof(notes));
    memset(size, 0, sizeof(size));
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
