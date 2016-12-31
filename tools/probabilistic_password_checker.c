// Adapted from http://shtrom.ssji.net/skb/getc.html
#include <stdio.h>
#include <termios.h>
#include <unistd.h>
    
// Password is aabcccq
static int code[26] = {2,1,3,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0};

int main() {

	struct termios old_tio, new_tio;
	unsigned char c;

    int counts[26];

    for(unsigned int i = 0; i < 26; ++i) {
        counts[i] = 0;
    }

    printf("Probabilistic Password Checker\n");
    printf("This program is very secure, because it's code is stored here: %p", code);

	/* get the terminal settings for stdin */
	tcgetattr(STDIN_FILENO,&old_tio);

	/* we want to keep the old setting to restore them a the end */
	new_tio=old_tio;

	/* disable canonical mode (buffered i/o) and local echo */
	new_tio.c_lflag &=(~ICANON & ~ECHO);

	/* set the new settings immediately */
	tcsetattr(STDIN_FILENO,TCSANOW,&new_tio);

    int already_failed = 0;
	do {
		 c=getchar();
		 printf("%d ",c);
         if( c >= 'a' && c <= 'z') {
             counts[c-'a']++;
             // Just to be super secure we test if we exeeded the maximum number of characters
             // For sure this makes our application more secure except if someone could monitor
             // our access of the code-array. But this is impossible!
             if(counts[c-'a'] > code[c-'a'])
                 already_failed = 1;
         }
	} while(c!='q');
	
	/* restore the former settings */
	tcsetattr(STDIN_FILENO,TCSANOW,&old_tio);

    if(already_failed == 1) {
        printf("Password is very wrong!");
        return 1;
    }
    
    for(unsigned int i = 0; i < 26; ++i) {
        if(code[i] != counts[i]) {
            printf("Password is wrong!");
            return 1;
        }
    }

    printf("Password was correct! You can continue using my super secure program");

	return 0;

}
