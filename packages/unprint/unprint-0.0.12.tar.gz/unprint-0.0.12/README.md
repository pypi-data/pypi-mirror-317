# Unprint

Unprint stuff in your terminal just by using unprint()

```
from unprint import unprint

print('apple')

print('this will be unprinted')
print('this will also be unprinted')
print('this too will be unprinted')

unprint(3)
# unprints 3 lines

print('this will be below apple')
```

Unprinting with a delay

```
from unprint import unprint

print('apple')

print('this will be unprinted')
print('this will also be unprinted')
print('this too will be unprinted')

unprint(3, delay=2)
# unprints 3 lines after a delay of 2 seconds

print('this will be after apple')
```