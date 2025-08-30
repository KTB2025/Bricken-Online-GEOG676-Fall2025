# Arithmatic in Python
##Part 1 - Take the following list and multiply all list items together.
part1 = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096]

product_list = 1
for num in part1:
    product_list *=num
print("Product of all list items:",product_list)

##Part 2 - Take the following list and add all list items together.
part2 = [-1, 23, 483, 8573, -13847, -381569, 1652337, 718522177]

total_list = 0
for num in part2:
    total_list+= num
print("Sum of all list items:",total_list)

##Part 3 - Take the following list and only add together those list items which are even. 
##You can use the following snippet of code to see if a number is even or odd. 
##The % operation is called Modulo and is used to find the remainder after division of one number by another. 
##We divide by 2 and look at the remainder; if there is no remainder the number is even, if there is a remainder the number is odd.
part3 = [146, 875, 911, 83, 81, 439, 44, 5, 46, 76, 61, 68, 1, 14, 38, 26, 21] 

even_sum = 0
for num in part3:
    if num % 2 == 0: 
        even_sum += num
print("Sum of all even numbers:", even_sum)