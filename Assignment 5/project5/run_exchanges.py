import argparse
from sqlalchemy.orm import sessionmaker
import time
from db_connect import get_conn
import random

## Argument parser to take the parameters from the command line
## Example on how to run: python run_exchanges.py 10 READ_COMMITTED
parser = argparse.ArgumentParser()
parser.add_argument('E', type = int, help = 'number of exchange transactions in a process')
parser.add_argument('I', help = 'isolation level')
args = parser.parse_args()


def exchange(sess):
    # generate two random account number
    account_nums = random.sample(range(1, 100000), 2)
    # print 'perform swap between '+str(account_nums[0])+'and'+str(account_nums[1])
    balance_0 = float(list(sess.execute(" \
    SELECT balance from account \
    where id = " + str(account_nums[0])))[0][0])

    balance_1 = float(list(sess.execute(" \
    SELECT balance from account \
    where id = " + str(account_nums[1])))[0][0])

    sess.execute(" UPDATE account set balance = " + str(balance_1) + " \
    where id = " + str(account_nums[0]))

    sess.execute(" UPDATE account set balance = " + str(balance_0) + " \
    where id = " + str(account_nums[1]))

    # balance_0_new = float(list(sess.execute(" \
    # SELECT balance from account \
    # where id = " + str(account_nums[0])))[0][0])
    #
    # balance_1_new = float(list(sess.execute(" \
    # SELECT balance from account \
    # where id = " + str(account_nums[1])))[0][0])
    # print balance_0_new, balance_1_new

## Create S sums operations
def E_swaps(sess, E):
    start = time.time()

    for i in xrange(0, E):
        while True:
            try:
                exchange(sess)
                time.sleep(0.0001)
            except Exception as e:
                # print e
                sess.rollback()
                continue
            break

    stop = time.time()
    return stop-start

## Create the engine and run the sums
engine = get_conn()
Session = sessionmaker(bind=engine.execution_options(isolation_level=args.I, autocommit=True))
sess = Session()
time = E_swaps(sess, args.E)
print time
