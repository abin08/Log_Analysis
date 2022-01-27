# Log Analysis

Requires Python 3.7.1

Use the following steps to run

1. Create Python virtual environment
    python3 -m venv venv

2. Activate virtual environment
    . venv/bin/Activate

3. Install requirements by
    pip install -r requirements.txt

4. Run the following command to get all the use cases
    python analyze.py


The above command will print results for all the insights given below,
    1) Top 10 requested pages and the number of requests made for each
    2) Percentage of successful requests (anything in the 200s and 300s range)
    3) Percentage of unsuccessful requests (anything that is not in the 200s or 300s range)
    4) Top 10 unsuccessful page requests
    5) The top 10 hosts making the most requests, displaying the IP address and number of requests made.
    6) For each of the top 10 hosts, show the top 5 pages requested and the number of requests for each

To get only one insight use the following command with option number
    python analyze.py -o <option number>

For example,
    python analyze.py -o 4
the above command will give result for 4th use case ie, 4) Top 10 unsuccessful page requests


Run Unit test cases,

    pyhthon -m unittest test.py


NOTE: Before writing the script analyze.py, I performed an exploratory analysis on the log file 
using jupyter notebook to understand the logs. It can be viewed by running following commands,

    pip install notebook
    jupyter notebook exploratory_analysis.ipynb
