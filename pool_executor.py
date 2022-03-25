from concurrent import futures

class PoolExecutor:  # pragma: no cover
    """
    PoolExecutor is a ThreadPoolExecutor or ProcessPoolExecutor wrapper
    utility class. It simplify tracking of future object submitted to executor
    and also handles processing the results exception.

    To use :
        def thread(number):
            print('start : {}'.format(number))
            time.sleep(number)
            print('finish : {}'.format(number))
            return number

        with PoolExecutor(max_workers=5) as pool:
            for i in range(10):
                pool.submit(thread, i) # i here is passed as parameter to thread method

    Alternatively:
        pool = PoolExecutor(max_workers=5)
        for i in range(10):
            pool.submit(thread, i)
        pool.finish()

    On arguments refer to concurrent.futures module in python library

    """

    def __init__(self, max_workers,
                 return_when=futures.FIRST_EXCEPTION,
                 timeout=None,
                 executor=futures.ThreadPoolExecutor):
        self.futures = []
        self._results = []
        self.pool = executor(max_workers=max_workers)
        self.return_when = return_when
        self.timeout = timeout
        self.finished = False

    def submit(self, handler: Callable, *args, **kwargs) -> None:
        """ submit function call to pool to be executed by worker thread """
        future = self.pool.submit(handler, *args, **kwargs)
        self.futures.append(future)
        return future

    def results(self):
        self.finish()
        return self._results
   
    def finish(self):
        if self.finished:
            return
        """
        Here PoolExecutor will wait for condition set in initialization
        It will then go through each tracked futures and collect the result
        which will also trigger exception of any submitted future raise an
        exception
        """
        try:
            done, _ = futures.wait(self.futures,
                                   timeout=self.timeout,
                                   return_when=self.return_when)
            for future in done:
                self._results.append(future.result())
        finally:
            self.pool.shutdown()
            self.finished = True

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.finish()
