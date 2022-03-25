# py_utils
utilities to ease python development

## PoolExecutor
PoolExecutor is a ThreadPoolExecutor or ProcessPoolExecutor wrapper
utility class. It simplify tracking of future object submitted to executor
and also handles processing the results exception.

To use :
```python
  def thread(number):
        print('start : {}'.format(number))
        time.sleep(number)
        print('finish : {}'.format(number))
        return number

    with PoolExecutor(max_workers=5) as pool:
        for i in range(10):
            pool.submit(thread, i) # i here is passed as parameter to thread method
```
Alternatively:
````python
    pool = PoolExecutor(max_workers=5)
    for i in range(10):
        pool.submit(thread, i)
    pool.finish()
````
pool function could return results which is accesible through 
````python
pool.results()
````
On arguments refer to concurrent.futures module in python library
