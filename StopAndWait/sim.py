import multiprocessing
import StopAndWait.send as ss
import StopAndWait.receive as sr

alldata = ['7f7d7e1d1456778167', '7f7d7e1d1456778167',
           '7f7d7e1d1456778167', '7f7d7e1d1456765444',
           '7f7d7e1d1456778166', '7f7d7e1d1456778165',
           '7f7d7e1d1456778164', '7f7d7e1d1456778166',
           '7f7d7e1d1456778163', '7f7d7e1d145677816d',
           '7f7d7e1d145677816f', '7f7d7e1d145677816e',
           '7f7d7e1d145677816e', '7f7d7e1d1456778166',
           '7f7d7e1d145677816d', '7f7d7e1d1456778165',
           '7f7d7e1d1456778164', '7f7d7e1d1456778166',
           '7f7d7e1d145677816e', '7f7d7e1d145677816f',
           '7f7d7e1d1456778164', '7f7d7e1d1456778161',
           '7f7d7e1d1456778165', '7f7d7e1d1456778166',
           '7f7d7e1d145677816d', '7f7d7e1d145677816d']


def sendandreceive(data):
    n = len(data)
    p2 = multiprocessing.Process(target=sr.main, args=(n,))
    p1 = multiprocessing.Process(target=ss.main, args=[data])

    # sr.main(n)
    p2.start()
    p1.start()

    p2.join()
    p1.join()


try:
    sendandreceive(alldata)
except Exception as e:
    print("Wrong",e)
