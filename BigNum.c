// BigNum.h ... LARGE positive integer values

#include <stdlib.h>
#include <stdio.h>
#include <assert.h>
#include <string.h>
#include <ctype.h>
#include <string.h>
#include "BigNum.h"

// Initialise a BigNum to N bytes, all zero
void initBigNum(BigNum *n, int Nbytes)
{
    n->nbytes = Nbytes;
    n->bytes = calloc(Nbytes, sizeof(unsigned char));
    int i = 0;
    while(i<Nbytes){
        n->bytes[i] = '0';
        i++;
    }
}


// Add two BigNums and store result in a third BigNum
void addBigNums(BigNum n, BigNum m, BigNum *res){
    if(n.nbytes > m.nbytes){
        int temp = n.nbytes;
        n.nbytes = m.nbytes;
        m.nbytes = temp;
    }
    res->bytes = ;
    int n1 = n.nbytes;
    int n2 = m.nbytes;
    int diff = n2- n1;

}

// Set the value of a BigNum from a string of digits
// Returns 1 if it *was* a string of digits, 0 otherwise
int scanBigNum(char *s, BigNum *n)
{
    int len = strlen(s);
    assert(len != 0);
    n->nbytes = len;
    n->bytes = calloc(len, sizeof(unsigned char));
    int i = 0;
    char ch;
    while (i < len) {
        ch = s[i];
        if(ch > '9' || ch < '0'){
            return 0;
        }else{
            n->bytes[i] = ch;
        }
        i++;
    }
    return 1;
}

// Display a BigNum in decimal format
void showBigNum(BigNum n){
    int i = 0;
    while(i < n.nbytes){
        printf("%c ", n.bytes[i]);
        i++;
    }
}
