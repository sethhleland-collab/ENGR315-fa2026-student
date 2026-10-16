import sys

"""
Create a program which will provide answers to the questions posed in the assignment description.
We've provided a function which will parse the NYT covid database file (named "us-counties.csv"); 
however, its correct implementation will be up to you. DO NOT MODIFY THIS FUNCTION.
Your code needs to be successful as well as sufficiently commented/documented to receive full credit.
"""


def parse_nyt_data(file_path=''):
    """
    Parse the NYT covid database and return a list of tuples. Each tuple describes one entry in the source data set.
    Date: the day on which the record was taken in YYYY-MM-DD format
    County: the county name within the State
    State: the US state for the entry
    Cases: the cumulative number of COVID-19 cases reported in that locality
    Deaths: the cumulative number of COVID-19 death in the locality

    :param file_path: Path to data file
    :return: A List of tuples containing (date,county, state, fips, cases, deaths) information

    ____________________ DO NOT MODIFY THIS FUNCTION ___________________
    """
    # data point list
    data=[]

    # open the NYT file path
    try:
        fin = open(file_path)
    except FileNotFoundError:
        print('File ', file_path, ' not found. Exiting!')
        sys.exit(-1)

    # get rid of the headers
    fin.readline()

    # while not done parsing file
    done = False

    # loop and read file
    while not done:
        line = fin.readline()

        if line == '':
            done = True
            continue

        # format is date,county,state,fips,cases,deaths
        (date,county, state, fips, cases, deaths) = line.rstrip().split(",")

        # clean up the data to remove empty entries
        if cases=='':
            cases=0
        if deaths=='':
            deaths=0

        # convert elements into ints
        try:
            entry = (date,county,state, fips, int(cases), int(deaths))
        except ValueError:
            print('Invalid parse of ', entry)

        # place entries as tuple into list
        data.append(entry)


    return data

### YOUR CODE HERE ###
#Get the .csv file from files

covid_data = parse_nyt_data('data/covid/us-counties.csv')

# date,county,state,fips,cases,deaths
# Create empty lists to filter out unneeded locality data
Harrisonburg = []
Rockingham = []

#Keep and return covid data for only Harrisonburg and Rockingham va
for place in covid_data:
    if "Harrisonburg" in place[1] and place[2] == "Virginia":
        Harrisonburg.append(place)

    elif "Rockingham" in place[1] and place[2] == "Virginia":
        Rockingham.append(place)

# New lists to store date entries
earliest_case1 = Harrisonburg[0][0]
earliest_case2 = Rockingham[0][0]


# Find earliest date, we can just compare compare the dates because Python can read the format YYYY-MM-DD
for date in Harrisonburg:
    if date[0] < earliest_case1 and Harrisonburg[date][4] > 0 :
        earliest_case1 = date[0]
    
        
for date in Rockingham:
    if date[0] < earliest_case2 and Rockingham[date][4] > 0:
        earliest_case2 = date[0]

#Part 1 answers
print(f"The earliest COVID case in Harrisonburg was on: {earliest_case1}")
print(f"The earliest COVID case in Rockingham was on: {earliest_case2}")

case_max1 = Harrisonburg[0]
case_max2 = Rockingham[0]
max_new1 = 0
max_new2 = 0
for i in range(1, len(Harrisonburg)):
    new_case = Harrisonburg[i][4] - Harrisonburg[i-1][4]
    if new_case > max_new1:
        max_new1 = new_case
        case_max1 = Harrisonburg[i]

for i in range(1, len(Rockingham)):
    new_caseR = Rockingham[i][4] - Rockingham[i-1][4]
    if new_caseR > max_new2:
        max_new2 = new_caseR
        case_max2 = Rockingham[i]

#Part 2 answers
print(f"There greatest number of new COVID cases in Harrisonburg was on {case_max1[0]}")
print(f"There greatest number of new COVID cases in Rockingham was on {case_max2[0]}")

#Q3  What was the worst seven-day period in Harrisonburg city for new COVID cases? What period in Rockingham County? 
# These are the seven-day periods when the number of new cases was maximal. (2 questions)

seven_day_max1 = 0
seven_day_sum1 = 0
worst_seven_days1 = []
Daily_cases = []
for i in range(1,len(Harrisonburg)):
    Daily_cases.append(Harrisonburg[i][4] - Harrisonburg[i-1][4])

#Worst seven days in Harrisonburg
#Daily_case[0] --> Harrisonburg[1] so worst_seven_days is s+1
for s in range(len(Daily_cases) - 6):
    seven_day_sum1 = sum(Daily_cases[s:s+7])
    if seven_day_sum1 > seven_day_max1:
        seven_day_max1 = seven_day_sum1
        worst_seven_days1 = Harrisonburg[s+1][0], Harrisonburg[s+7][0]


#Rockingham worst seven days
seven_day_max2 = 0
seven_day_sum2 = 0
worst_seven_days2 = []
Daily_cases2 = []
for i in range(1, len(Rockingham)):
    Daily_cases2.append(Rockingham[i][4] - Rockingham[i-1][4])

for s in range(len(Daily_cases2) - 6):
    seven_day_sum2 = sum(Daily_cases2[s:s+7])
    if seven_day_sum2 > seven_day_max2:
        seven_day_max2 = seven_day_sum2
        worst_seven_days2 = Rockingham[s+1][0], Rockingham[s+7][0]

#Question 3 answers
print(f"The seven day period with the greatest number of new cases in Harrisonburg was, {worst_seven_days1[0]} to {worst_seven_days1[1]}")
print(f"The seven day period with the greatest number of new cases in Rockingham was, {worst_seven_days2[0]} to {worst_seven_days2[1]}")




