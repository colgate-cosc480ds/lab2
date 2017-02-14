# Lab 2: Snakes on a Plane

Welcome to the *second* COSC 480 Data Science Lab!

You are encouraged to work with a partner for this lab.  If you do not have a partner, let me know and I can assign one to you.  (While you can choose your partner, you may be asked to choose *different* partners for each lab for the first couple of labs.)

The lab is due **Thursday, Feb. 16th 2017 at 11:59pm**.  Submission instructions appear the end.  *When you finish, please be sure to write a commit message!*


## Updates

**Updates to the lab will be posted here**:

- Feb. 14, 2017 6am: Correction: the number of rows in `flights.csv` may in fact be slightly less than the number of rows in the input because some rows are filtered out (those with 'NA' in `DepTime` or `ArrTime`).
- Feb. 14, 2017 1:45pm: Correction: in the test_input.csv, one of the times on the first line is `23:55` but it should be `2355`.
- Feb. 14, 2017 1:45pm: Correction: the test output provided did not match the specification in the readme.  It's now been updated to match the specification.



## Your challenge

This assignment is designed to expose you to some of the challenges of a typical task faced by a data scientist: using command-line tools and Python scripting to "wrangle" data into a format for subsequent analysis.  In addition, the dataset we will use for this lab is "large" and so you will have to design your programs so that they run efficiently *even when the amount of available memory is smaller than the dataset*.

The dataset we will use consists of flight arrival and departure details for commercial flights in the U.S.  The data original comes from the [U.S. Department of Transportation's Bureau of Transportation Statistics](http://www.transtats.bts.gov/OT_Delay/OT_DelayCause1.asp).  This dataset was used in a past [data competition](http://stat-computing.org/dataexpo/2009/).

## Your tools

For this assignment, you can use Python 2, [standard UNIX utilities](http://en.wikipedia.org/wiki/List_of_Unix_utilities), and some basic [bash shell](https://en.wikipedia.org/wiki/Bourne_shell) scripting.

For this lab, you can work in a combination of PyCharm (for editing code) and the command line.  You will likely not need to use Jupyter notebook for this lab.

In short, you will use your Python skills to analyze data about flights.  Snakes on a plane! 

## Your constraints

You need to be able to handle an input file that is larger than the memory of the computer that runs the script. To do so, you should:

1. write *streaming* Python and bash code that only requires a constant amount of the data to be in memory at a time, and
2. leverage UNIX utilities like `sort` that provide "out-of-core" algorithms.

You should not need to write very complicated code in either Python or bash. **Take advantage of UNIX utilities as much as you can.** In particular, note that there is no need for you to write an out-of-core algorithm to complete this homework: UNIX utilities like `sort` can do the heavy lifting if you orchestrate them properly.

Hint: if you do regular `sort` it treats numbers as text (so 110 comes before 21) but if you do `sort -n` it will treat text data numerically.  You may find this useful at some point in the lab.

## High-Level Task

The data wrangling you will do in this lab will serve two primary analysis tasks:

1. **Find "ghost flights."**  The original dataset records only registered commercial flights.  For various reasons, however, an airline sometimes needs to fly an empty plane from one airport to another.  Such flights are not recorded in this dataset.  However, we can still detect such "ghost" flights by looking for planes that land in one airport and then are next seen taking off from a different airport.  (Ghost flights were part of a [winning entry](http://stat-computing.org/dataexpo/2009/posters/hofmann-cook.pdf) in the aforementioned data competition.)

2. **Measure how long, on average, planes spend at the gate between flights.**  Airlines can maximize profits by keeping their planes in the air for as much of the day as possible.  How quickly do airlines get planes back up in the air?  Figuring out a useful statistic for this is a little tricky, because we want to avoid counting the inevitable down time for planes that occurs at the end of the day (there isn't a high consumer demand for flights that depart at 2am!). Details of how we will calculate this statistic are given below.


## Specification

First, obtain the data.  These datasets represent flights taken in 2007.  The name of the file indicates which subset of 2007 flights are included in the data.  For a description of the columns, see [here](http://stat-computing.org/dataexpo/2009/the-data.html).  You can download the input datasets like this:

    vagrant@ubuntu:~$ cd /vagrant/lab2/
    vagrant@ubuntu:/vagrant/lab2$ curl -O http://cs.colgate.edu/~mhay/cosc480ds/januaryhalf2007.csv.bz2
    vagrant@ubuntu:/vagrant/lab2$ curl -O http://cs.colgate.edu/~mhay/cosc480ds/january2007.csv.bz2
    vagrant@ubuntu:/vagrant/lab2$ curl -O http://cs.colgate.edu/~mhay/cosc480ds/2007.csv.bz2

Then decompress them.  Actually, let's just decompress the smallest one for now (you can decompress the others later when you want to try out your code on larger datasets; be warned `2007.csv` is 671M uncompressed!  You don't need to run on this one but may find it useful for the challenge problems.).

    vagrant@ubuntu:/vagrant/lab2$ bunzip2 januaryhalf2007.csv.bz2

Please **do NOT commit** the input data or your output data to your GitHub repository.  (Use `git add -u` to avoid adding new files to the repo.)

This file includes two source code files `lab2.sh` and `lab2.py`.  Go ahead and run `lab2.sh` like this:

      vagrant@ubuntu:/vagrant/lab2$ ./lab2.sh test_input.csv 

And you should see something like this:

      Running ./lab2.sh on test_input.csv
      Here is an example of streaming data into a python function:
      ...

Your task is to edit `lab2.sh` and `lab2.py` such that when `lab2.sh` is executed on an input file (as shown above), it will produce **four csv output files**, as follows:

1. `flights.csv` should be a csv file with the header `TailNum, ActualDepTime, ActualArrTime, Origin, Dest`.
    + Each row corresponds to a row from the input.  Since some rows from the input may be filtered out (see below), `flights.csv` may be slightly smaller than the original input.  (You can use UNIX utilities, such as `wc` and perhaps others, to check that the number of lines in the output is correct.)
    + Fields `TailNum`, `Origin`, and `Dest` are directly from the input.
    + Flights that have 'NA' for `DepTime` or `ArrTime` should be filtered out (see the example code). 
    + `ActualDepTime` and `ActualArrTime` should be formatted as `YYYY-MM-DD hh:mm:ss`  (see the example code).
    + Computing the time values is *not* straightforward.  This is primarily because  the original source data breaks up time in weird ways.  Specifically, there is a single year, month, day but then different time fields (scheduled departure, departure, arrival, etc.) but these events can actually happen on different days!  The problem is further compounded by the fact that planes can change time zones (in some cases causing the arrival time to be earlier than the departure time).
    + `ActualDepTime` should be computed as follows.   Start by figuring out the scheduled departure time.  This is determined by combining the `Year`, `Month`, `DayofMonth`, and `CRSDepTime` fields into a single [datetime](https://docs.python.org/2/library/datetime.html#datetime-objects) object.  Then add to this the `DepDelay` field, which reports the number of minutes the flight departure was delayed (which can be negative if it departed ahead of schedule).  You will find [timedelta](https://docs.python.org/2/library/datetime.html#timedelta-objects) objects useful here.  This new time is the `ActualDepTime`.  (You can double check that the `hhmm` component of this time matches `DepTime` field in the original data.)
    + `ActualArrTime` should be computed as follows.  Start by combining the `Year`, `Month`, `DayofMonth`, and `CRSArrTime` fields into a single datetime object.  In most cases, this is the scheduled arrival time.  However, when a flight arrives after midnight, this time is off by a day (because we used the departure day rather than the arrival day).  We will use the following heuristic: if the time is *more than two hours earlier* than `ActualDepTime`, then assume the flight landed after midnight and add 1 day to the time (again, use [timedelta](https://docs.python.org/2/library/datetime.html#timedelta-objects) objects).  But if the time is less than two hours earlier, we will assume that the flight flew west and crossed a timezone.  In this case, do not adjust it.  Finally, add to this the `ArrDelay` field, which reports the number of minutes the flight arrival was delayed (which can be negative if it arrived ahead of schedule). (You can double check that the `hhmm` component of this time matches `ArrTime` field in the original data.)
2. `ghosts.csv` should be a csv file with the header `TailNum, EarliestDepTime, LatestArrTime, Origin, Dest`.
    + Each row corresponds to a "ghost flight"---a flight that *must* have taken place, but which is not in the original data.  *You need to infer the existence of these missing flights by analyzing the data that is available to you.*
    + `TailNum` is the tail number of the plane, from the original data.
    + `EarliestDepTime` is the earliest that the ghost flight could have taken off.  We will set this equal to the `ActualArrTime` of the recorded flight immediately *preceding* the ghost flight.
    + `LatestArrTime` is the latest that the ghost flight could have taken arrived.  We will set this equal to the `ActualDepTime` of the recorded flight immediately *following* the ghost flight.
    + `Origin` should be the airport from which the ghost flight originated (and therefore equal to the `Dest` of the recorded flight immediately preceding the ghost flight).  
    + `Dest` should be the airport into which the ghost flight arrived (and therefore equal to the `Origin` of the recorded flight immediately following the ghost flight).
3. `avg_gate_wait.csv` should be a csv file with the header `AvgGateWait, TailNum`.
    + `TailNum` is the tail number of the plane, from the original data.  You should have at most one row per tail number in the original data (though planes that only fly once/day  won't appear -- see details next).
    + `AvgGateWait` is computed as follows.  A "gate wait" event is formally defined as the time difference between the arrival and departure of *consecutive* flights that occur *on the same day*.  Intuitively, it captures time that a plan is sitting at the gate between flights.  For example, if a flight arrives at 8:15pm at LGA and departs at 10:00pm from LGA, it experiences a gate wait of 1 hour and 45 minutes.  On the other hand, if a flight arrives at 11:00pm and then departs at 6:00am the next day, this will **not** count as a gate wait because the departure occurs on the following day.  Finally, it is **not** considered a "gate wait" event if a ghost flight occurs -- i.e., if the flight arrives at one airport and is then next seen taking off from a *different* airport. The `AvgGateWait` is the average of gate wait events for a given plane.  If a plane has no gate wait events, then it should **not** appear in this file.
4. `avg_gate_wait_hist.csv` should be a csv file with the header `MinutesLow, Count`.
    + This file describes a histogram of average gate waits.  
    + Each row corresponds to a bin in the histogram: the first column, `MinutesLow`, specifies the lower bound of the bin.  The value of `MinutesLow` should start at 0 and increase by 15 (minutes) with each row.  (Planes with an average gate wait less than zero -- which may happen -- can be discarded.)  
    + The value of `Count` is the number of planes that have an average gate wait falling in the range [`MinutesLow`, `MinutesLow` + 15).  Empty interval should appear with a count of zero.
    + The number of rows depends on the data: the last row should correspond to the last non-empty interval.


## Example Input

The file `test_input.csv` has been provided.  This is partially fabricated data that I wrote to illustrate the various corner cases described above.  The correct outputs for the test example have also been provided (`test_flights.csv`, `test_ghosts.csv`, `test_avg_gate_wait.csv` and `test_avg_gate_wait_hist.csv`).  

The first flight taken by 85069E arrives in DTW but then is next seen departing from MSP.  Thus a ghost flight occurred from DTW to MSP.  The other plane, 85439E, also has one ghost flight (it lands in MSN and then is next seen taking off from CAK).

For 85069E, the average gate wait is as follows:

- The 04:07 (arrival) - 16:16 (next departure) period is *not* counted because a ghost flight occurred these times (the arrival destination DTW does not match the subsequent departure origin MSP).
- 19:05-19:33 (28 min)
- 20:31-21:48 (77 min)
- 00:06-07:10 (424 min) -- This one probably shouldn't be counted since the flight probably didn't sit at the gate all night long. However, because the flight arrived after midnight on Jan. 2 and then departed later that same day, we must count it according to the definition of a gate wait
- Average gate wait is (28 + 77 + 424) / 3 = 176.33 minutes

For 85439E, the gate waits are:

- 10:38-11:55 (77 min)
- 12:46-13:36 (50 min)
- 14:50-15:25 (35 min)
- 16:28-16:53 (25 min)
- The 11:57-16:00 period is *not* counted because a ghost flight occurred these times (the arrival destination MSN does not match the subsequent departure origin CAK).
- Average gate wait is (77 + 50 + 35 + 25) / 4 = 46.75 minutes

## Challenge problems

Here are two challenge problems:

1. Try to make your code as efficient as possible.  A prize will go to the fastest submission.  For your own reference, you can time your program like this:

        vagrant@ubuntu:/vagrant/lab2$ time ./lab2.sh test_input.csv 

2. Do some additional data analysis!  There are many interesting things to explore in this dataset.  Formulate a question and use your data wrangling skills to answer it!


## Submission instructions

To submit your work, you must *commit* your changes, and then *push* those changes to GitHub. 

1. Check the status to see what changes have been made.

        vagrant@ubuntu:~$ cd /vagrant/lab1/
        vagrant@ubuntu:~$ git status 
        ...

2. Use `git add` to move these changes to the "staging area."  By using the `-u` flag you will only add files that already exist in the repository.  This is probably what you want to do in general.  Please **never** do `git add -A` because it will add all sorts of junk files (such as hidden files left by applications like PyCharm).  First, do a dry run with the `-n` flag:

        vagrant@ubuntu:~$ git add -un .           
        ... 

  If everything looks good, add them for real:

        vagrant@ubuntu:~$ git add -u .            
        ... 

3. *Commit* the changes to your local repository.  Please write a commit message having the following form.  Please fill in the blank with a word or phrase that captures your sentiments (e.g., "fun", "terrifying", "invigorating", "never-ending", "delightful", etc.).

        vagrant@ubuntu:~$ git commit -m 'completed lab1: this lab was _____'

4. *Push* these changes to GitHub.  

        vagrant@ubuntu:~$ git push origin master


##### Acknowledgments

This lab assignment has been adapted from a data wrangling assignment from the Berkeley CS 186 course.  The idea of shell scripts and python streaming and some of the text above is from the CS 186 assignment.  However, the dataset, analysis tasks, and assignment specifics are new.


