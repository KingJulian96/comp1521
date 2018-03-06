// COMP1521 18s1 Week 02 Lab
// Add two numbers (numbers can be LARGE)

#include <stdio.h>
#include "BigNum.h"
#include <assert.h>

int main(int argc, char **argv)
{
    BigNum num1;  // first input number
    BigNum num2;  // second input number
    BigNum sum;   // num1 + num2

    if (argc < 3) {
      printf("Usage: %s Num1 Num2\n", argv[0]);
      return 1;
    }

    // Initialise BigNum objects
    initBigNum(&num1, 20);
    assert(num1.nbytes == 20);
    assert(num1.bytes[1] == '0');
    assert(num1.bytes[19] == '0');
    initBigNum(&num2, 20);
    assert(num2.nbytes == 20);
    assert(num2.bytes[1] == '0');
    assert(num2.bytes[19] == '0');
    initBigNum(&sum,  20);
    assert(sum.nbytes == 20);
    assert(sum.bytes[1] == '0');
    assert(sum.bytes[19] == '0');

    // Extract values from cmd line args
    if (!scanBigNum(argv[1], &num1)) {
      printf("First number invalid\n");
      return 1;
    }
    if (!scanBigNum(argv[2], &num2)) {
      printf("Second number invalid\n");
      return 1;
    }
    //assert(num1.bytes[0] == '2');

    // Add num1+num2, store result in sum
    addBigNums(num1, num2, &sum);

    printf("Sum of "); showBigNum(num1);
    printf("\nand "); showBigNum(num2);
    printf("\nis "); showBigNum(sum);
    printf("\n");

    return 0;

}
