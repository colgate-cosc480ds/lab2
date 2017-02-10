import csv
import datetime
import dateutil
import dateutil.parser
import sys

def make_time(year, month, day, time):
    """Given a year, month, day, and time (hhmm format), parse and return the 
    corresponding datetime object."""
    if time == '2400':  # small hack: 2400 is equivalent to 0000, 
                        # but 2400 breaks parser
        time = '0000'
    time = time.zfill(4)  # pad left with zeros; e.g., '730' becomes '0730'
    return dateutil.parser.parse('{}-{}-{}-{}'.format(year, month, day, time))

def example_function():
    """
    This is an example of a Python function that processes a stream of data 
    from STDIN and writes a stream of data to STDOUT.

    The format of the input stream is the format of the flight data as 
    specified in the lab description.  The format of the output stream is a CSV 
    with columns TailNum, ScheduledDepTime.

    This function outputs the tail number and scheduled departure time in the
    desired format.
    """
    with sys.stdin as f, sys.stdout as f2:
        reader = csv.DictReader(f)
        writer = csv.DictWriter(f2, ['TailNum', 'ScheduledDepTime'])
        writer.writeheader()
        for row in reader:
            # skip cancelled/diverted flights
            if row['DepTime'] == 'NA' or row['ArrTime'] == 'NA':
                continue
            scheduled_time = make_time(row['Year'], 
                row['Month'], row['DayofMonth'], row['CRSDepTime'])
            writer.writerow({'TailNum': row['TailNum'], 'ScheduledDepTime': scheduled_time})
