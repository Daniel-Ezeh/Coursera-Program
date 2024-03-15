#!/bin/bash

echo -n "Enter an integer: "
read n1

echo -n "Enter another integer: "
read n2

sum=$(($n1+$n2))
product=$(($n1*$n2))

echo "The sum of $n1 and $n2 is $sum"
echo "The product of $n1 and $n2 is $product"

if [ $sum -gt $product ]
then
    echo "The sum, which is $sum, is greater than the product, which is $product."
elif [ $product -gt $sum ]
then
    echo "The product $product, is greater than the sum $sum"
else
    echo "$sum is equal to $product."
fi