def coroutine(func):
    def start(*args, **kwargs):
        cr = func(*args, **kwargs)
        cr.next()
        return cr
    return start

@coroutine
def f():
    i = 0
    yield None
    while True:
        print "Iterating"
        yield i
        print "In between"
        j = (yield)
        print "Got: " + str(j)
        i += 1

