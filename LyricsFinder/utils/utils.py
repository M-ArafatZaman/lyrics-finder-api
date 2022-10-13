'''
Some common utility functions used throughout the application
'''
import datetime

def print_DT(*args, **kwargs):
    '''
    Print with datetime
    '''
    print(f"[{datetime.datetime.now()}]", *args, **kwargs)