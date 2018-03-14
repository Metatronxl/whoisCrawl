import datetime
import time


def date_cmp(first_date,sec_date):
    strftime = datetime.datetime.strptime(first_date, "%Y-%m-%d")
    strftime2 = datetime.datetime.strptime(sec_date, "%Y-%m-%d")
    result = strftime>strftime2
    # print("first_date > sec_date:",strftime>strftime2)
    return result


if __name__ == '__main__':
    date_cmp('2017-11-02','2017-01-04')