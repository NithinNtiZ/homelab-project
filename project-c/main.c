#include <stdio.h>
#include <string.h>  // For strcspn()

int main(int argc, char const *argv[])
{
    char str[100];  // Buffer to store the string

    printf("Enter your name:\n");
    fgets(str, sizeof(str), stdin);  // Use fgets to read the entire line including spaces

    // Remove the newline character if it's present
    str[strcspn(str, "\n")] = '\0';

    printf("My name is %s\n", str);  // Print the string

    return 0;
}
