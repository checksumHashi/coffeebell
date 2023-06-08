import multiprocessing

workers = multiprocessing.cpu_count() * 2 + 1
worker-class = sync
bind = 'unix:coffeebell.sock'
umask = 0o007
reload = True

#logging
accesslog = '-'
errorlog = '-'