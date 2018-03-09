// BigNum.h ... LARGE positive integer values

#include <stdlib.h>
#include <stdio.h>
#include <assert.h>
#include <string.h>
#include <ctype.h>
#include "BigNum.h"

void addition(BigNum n, BigNum m, BigNum *res){
    int mnum = m.nbytes;
    int carry = 0;
    int i = 0;
    res->nbytes = 0;
    res->bytes = realloc(res->bytes, sizeof(Byte)*(mnum+1));
    while(i < mnum){
        int intn = n.bytes[i] - '0';
        int intm = m.bytes[i] - '0';
        int sum = intn + intm;
        if(sum >= 10){
            if(carry != 0){
                res->bytes[i] = (sum%10) + 1 + '0';
                res->nbytes++;
            }else{
                res->bytes[i] = (sum%10) + '0';
                res->nbytes++;
                carry++;
            }
            if(i == mnum-1){
                res->bytes[i+1] = 1  + '0';
                res->nbytes++;
            }
        }else{
            if(carry != 0){
                sum = sum + 1;
                res->bytes[i] = sum   + '0';
                carry = 0;
            }else{
                res->bytes[i] = sum  + '0';
            }
            res->nbytes++;
        }
        i++;
    }
}

void addition_n(BigNum n, BigNum m, BigNum *res){
    int nnum = n.nbytes;
    int mnum = m.nbytes;
    res->nbytes =0;
    int sum = 0;
    int carry = 0;
    int i = 0;
    res->bytes = realloc(res->bytes, sizeof(Byte)*(nnum+1));
    while(i < nnum){
        if(i < mnum){
            int intn = n.bytes[i] - '0';
            int intm = m.bytes[i] - '0';
            sum = intn + intm;
        }else{
            int intn = n.bytes[i] - '0';
            sum = intn;
        }
        if(carry > 0){
            sum++;
            carry = 0;
        }
        if(sum >= 10){
            if(carry != 0){
                res->bytes[i] = (sum%10) + 1 + '0';
                res->nbytes++;
            }else{
                res->bytes[i] = (sum%10) + '0';
                res->nbytes++;
                carry++;
            }
            if(i == nnum-1){
                res->bytes[i+1] = 1  + '0';
                res->nbytes++;
            }
        }else{
            if(carry != 0){
                sum = sum + 1;
                res->bytes[i] = sum   + '0';
                carry = 0;
            }else{
                res->bytes[i] = sum  + '0';
            }
            res->nbytes++;
        }
        i++;
    }
}

void addition_m(BigNum n, BigNum m, BigNum *res){
    int nnum = n.nbytes;
    int mnum = m.nbytes;
    res->nbytes = 0;
    int sum = 0;
    int carry = 0;
    int i = 0;
    res->bytes = realloc(res->bytes, sizeof(Byte)*(mnum+1));
    while(i < mnum){
        if(i < nnum){
            int intn = n.bytes[i] - '0';
            int intm = m.bytes[i] - '0';
            sum = intn + intm;
        }else{
            int intm = m.bytes[i] - '0';
            sum = intm;
        }
        if(carry > 0){
            sum++;
            carry = 0;
        }
        if(sum >= 10){
            if(carry != 0){
                res->bytes[i] = (sum%10) + 1 + '0';
                res->nbytes++;
            }else{
                res->bytes[i] = (sum%10) + '0';
                res->nbytes++;
                carry++;
            }
            if(i == mnum-1){
                res->bytes[i+1] = 1  + '0';
                res->nbytes++;
            }
        }else{
            if(carry != 0){
                sum = sum + 1;
                res->bytes[i] = sum   + '0';
                carry = 0;
            }else{
                res->bytes[i] = sum  + '0';
            }
            res->nbytes++;
        }
        i++;
    }
}


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
    int nnum = n.nbytes;
    int mnum = m.nbytes;
    if(nnum == mnum){
        addition(n, m, res);
    }else if(nnum > mnum){
        addition_n(n, m, res);
    }else if (nnum < mnum){
        addition_m(n, m, res);
    }
}

// Set the value of a BigNum from a string of digits
// Returns 1 if it *was* a string of digits, 0 otherwise
int scanBigNum(char *s, BigNum *n)
{   
    int len = strlen(s);
    if(len > n->nbytes){
        int i = 0;
        n->bytes = calloc(len, sizeof(unsigned char));
        n->nbytes = len;
        while(i != len){
            n->bytes[i] = '0';
            i++;
        }
    }else{
        n->nbytes = 0;
    }
    n->nbytes = 0;
    int i;
    int a = 0;
    for(i = len -1; i>= 0; i--){
        if(s[i] == ' '){
            continue;
        } else {
            if((s[i] - '0'> 9) ||( s[i] - '0' < 0)){
                return 0;
            }else{
               n->bytes[a] = s[i];
               n->nbytes++;
               a++;
            }
        }
    }
    return 1;
}

// Display a BigNum in decimal format
void showBigNum(BigNum n){
    int i = n.nbytes-1;
    int flag = 0;
    for(i = n.nbytes-1; i>=0; i--) {
        if(flag == 0 && n.bytes[i]-'0'==0) {
            continue;   
        } else {
            flag ++;
            printf("%d",n.bytes[i]-'0');
        
        }
    }
}
