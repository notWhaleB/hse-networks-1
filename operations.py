import os
import sqlite3
from multiprocessing import Process, Pipe
from subprocess import Popen
from time import sleep

conn = sqlite3.connect(os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    'cities.sqlite3'
))

def cities(region_id):
    cur = conn.cursor()
    cur.execute('SELECT name FROM cities WHERE state_id=? ORDER BY name', (region_id,))
    res = cur.fetchall()
    if res is None or len(res) == 0:
        return 'No cities found'
    return '<br>'.join([x[0] for x in res])

def factorize(number):
    cur_factor = 2
    number_sq = int(number ** 0.5)
    while cur_factor <= number_sq:
        if number % cur_factor == 0:
            return '%s * %s' % (number / cur_factor, cur_factor)
        cur_factor += 1
    return '%s is prime' % number

def do_ping(session, ip):
    p = Popen(['ping -c 10 %s' % ip], stdout=session['ping']['pipe']['in'],
              shell=True, close_fds=True)
    p.wait()
    sleep(1)
    os.write(session['ping']['pipe']['in'], '\n')

def ping(session, ip):
    (fd_out, fd_in) = os.pipe()

    session['ping'] = {'pipe': {
        'in': fd_in,
        'out': fd_out
    }}
    Process(target=do_ping, args=(session, ip)).start()
    return 'Ping started'


def ping_poll(session):
    ping_log = os.read(session['ping']['pipe']['out'], 1024)
    if ping_log[-2:] == '\n\n' or ping_log == '\n':
        session.pop('ping')
    return ping_log.replace('\n', '<br>')
