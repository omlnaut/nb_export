# nb_export
> Export marked cells to script files


```python
# exp common
import math
```

This file will become your README and also the index of your documentation.

## Exporting

Exporting cells is done by adding a comment at the top like this:

```python
# exp common
def sum_up_to(n):
    return int(n*(n+1)/2)
```

```python
sum_up_to(10)
```




    55



```python
# exp common
def product_up_to(n):
    return math.factorial(n)
```

```python
product_up_to(6)
```




    720


