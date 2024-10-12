#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <netinet/in.h>

#define PORT 1337
#define BUFFER_SIZE 1024

int client_socket;

void sort(int arr[], int n)
{
    for (int i = 0; i < n - 1; i++)
    {
        int min_idx = i;
        for (int j = i + 1; j < n; j++)
        {
            if (arr[j] < arr[min_idx])
                min_idx = j;
        }

        if (min_idx != i)
        {
            int temp = arr[min_idx];
            arr[min_idx] = arr[i];
            arr[i] = temp;
        }
    }
}

void setup() {
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
}

int sortingserver()
{
    write(client_socket, "Welcome to sorting server, server to sort your numbers efficiently!\n", 69);
    int length;
    write(client_socket, "Enter number of elements: ", 26);
    char buf[24];
    read(client_socket, buf, 24);
    length = atoi(buf);
    
    if ((int)length > 100)
    {
        write(client_socket, "Sorry length more than 100 are currently not supported!\n", 56);
        close(client_socket);
        exit(0);
    }

    int nums[100];
    write(client_socket, "Enter the numbers: \n", 20);
    for (short int i = 0; i < (short)length; i++)
    {
        read(client_socket, buf, 24);
        if(!strlen(buf)) continue;
        nums[i] = atoi(buf);
    }

    sort(nums, length);
    write(client_socket, "Result: ", 8);
    for (short int i = 0; i < (short)length; i++)
    {
        sprintf(buf, "%d ", nums[i]);
        write(client_socket, buf, strlen(buf));
    }

    return 0;
}

// gcc sortingserver.c -o sortingserver -fstack-protector -L. -Wl,--rpath=. -Wl,--dynamic-linker=./ld-linux-x86-64.so.2 -s 
int main() {
    setup();
    int server_fd;
    struct sockaddr_in address;
    int addrlen = sizeof(address);

    if ((server_fd = socket(AF_INET, SOCK_STREAM, 0)) == 0) {
        perror("Socket failed");
        exit(EXIT_FAILURE);
    }
    address.sin_family = AF_INET;
    address.sin_addr.s_addr = htonl(INADDR_ANY);
    address.sin_port = htons(PORT);

    if (bind(server_fd, (struct sockaddr *)&address, sizeof(address)) < 0) {
        perror("Bind failed");
        close(server_fd);
        exit(EXIT_FAILURE);
    }

    if (listen(server_fd, 3) < 0) {
        perror("Listen failed");
        close(server_fd);
        exit(EXIT_FAILURE);
    }

    printf("Server is listening on port %d...\n", PORT);

    while (1) {
        if ((client_socket = accept(server_fd, (struct sockaddr *)&address, (socklen_t *)&addrlen)) < 0) {
            perror("Accept failed");
            close(server_fd);
            exit(EXIT_FAILURE);
        }

        if (fork() == 0) break;
        
        printf("Connected to client.\n");
        close(client_socket);
    }

    sortingserver();
    write(client_socket, "\nThank you for using our service! hope to see you again soon.\n", 62);
    close(client_socket);
    return 0;
}
