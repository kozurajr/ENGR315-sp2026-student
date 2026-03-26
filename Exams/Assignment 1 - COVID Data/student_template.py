import sys


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

def first_question(data):
    """
    # Write code to address the following question: Use print() to display your responses.
    # When was the first positive COVID case in Rockingham County?
    # When was the first positive COVID case in Harrisonburg?
    :return:
    """

    # your code here
    rockingham_date = None
    harrisonburg_date = None

   
    for (date, county, state, fips, cases, deaths) in data:
        if state == "Virginia":
            if county == "Rockingham" and cases > 0 and rockingham_date is None:
                rockingham_date = date
            if county == "Harrisonburg" and cases > 0 and harrisonburg_date is None:
                harrisonburg_date = date
    print("First positive covid case in Rockingham was on:", rockingham_date)
    print("First positive covid case in Harrisonburg was on:", harrisonburg_date)
    return

def second_question(data):
    """
    # Write code to address the following question: Use print() to display your responses.
    # What day was the greatest number of new daily cases recorded in Harrisonburg?
    # What day was the greatest number of new daily cases recorded in Rockingham County?
    :return:
    """

    # your code here
    prev_rockingham = None
    prev_harrisonburg = None

    max_rockingham_cases = -1
    max_rockingham_date = None

    max_harrisonburg_cases = -1
    max_harrisonburg_date = None
    
    for (date, county, state, fips, cases, deaths) in data:
        if state == "Virginia":
            if county == "Rockingham":
                if prev_rockingham is not None:
                    new_cases = cases - prev_rockingham
                    if new_cases > max_rockingham_cases:
                        max_rockingham_cases = new_cases
                        max_rockingham_date = date
                prev_rockingham = cases

            elif county == "Harrisonburg":
                if prev_harrisonburg is not None:
                    new_cases = cases - prev_harrisonburg
                    if new_cases > max_harrisonburg_cases:
                        max_harrisonburg_cases = new_cases
                        max_harrisonburg_date = date
                prev_harrisonburg = cases

    print("The greatest number of new daily cases in Rockingham County was on:", max_rockingham_date, "with", max_rockingham_cases, "new cases")
    print("The greatest number of new daily cases in Harrisonburg was on:", max_harrisonburg_date, "with", max_harrisonburg_cases, "new cases")
    
    return

def third_question(data):
    """
    # Write code to address the following question: Use print() to display your responses.
    # What was the worst 7-day period in either the city and county for new COVID cases?
    # This is the 7-day period where the number of new cases was maximal.
    :return:
    """
    
    # your code here
    rockingham_daily = []
    harrisonburg_daily = []

    prev_rockingham = None
    prev_harrisonburg = None

    for (date, county, state, fips, cases, deaths) in data:
        if state == "Virginia":
            if county == "Rockingham":
                if prev_rockingham is not None:
                    new_cases = cases - prev_rockingham
                    rockingham_daily.append((date, new_cases))
                prev_rockingham = cases

            elif county == "Harrisonburg":
                if prev_harrisonburg is not None:
                    new_cases = cases - prev_harrisonburg
                    harrisonburg_daily.append((date, new_cases))
                prev_harrisonburg = cases
    
    max_rockingham_sum = -1
    max_rockingham_start = None
    max_rockingham_end = None

    for i in range(len(rockingham_daily) - 6):
        window = rockingham_daily[i:i+7]
        total = 0
        for entry in window:
            total += entry[1]
        if total > max_rockingham_sum:
            max_rockingham_sum = total
            max_rockingham_start = window[0][0]
            max_rockingham_end = window[-1][0]

    max_harrisonburg_sum = -1
    max_harrisonburg_start = None
    max_harrisonburg_end = None

    for i in range(len(harrisonburg_daily) - 6):
        window = harrisonburg_daily[i:i+7]
        total = 0
        for entry in window:
            total += entry[1]
        if total > max_harrisonburg_sum:
            max_harrisonburg_sum = total
            max_harrisonburg_start = window[0][0]
            max_harrisonburg_end = window[-1][0]


    print("The worst week in Rockingham County was from", max_rockingham_start, "to",
          max_rockingham_end, "with", max_rockingham_sum, "new cases")

    print("The worst week in Harrisonburg was from", max_harrisonburg_start, "to",
          max_harrisonburg_end, "with", max_harrisonburg_sum, "new cases")

    return

if __name__ == "__main__":
    data = parse_nyt_data('\Exams\Assignment 1 - COVID Data\us-counties.csv')

    for (date,county, state, fips, cases, deaths) in data:
        print('On ', date, ' in ', county, ' ', state, ' there were ', cases, ' cases and ', deaths, ' deaths')


    # write code to address the following question: Use print() to display your responses.
    # When was the first positive COVID case in Rockingham County?
    # When was the first positive COVID case in Harrisonburg?
    first_question(data)


    # write code to address the following question: Use print() to display your responses.
    # What day was the greatest number of new daily cases recorded in Harrisonburg?
    # What day was the greatest number of new daily cases recorded in Rockingham County?
    second_question(data)

    # write code to address the following question: Use print() to display your responses.
    # What was the worst seven day period in Harrisonburg for new COVID cases (in terms of absolute number of cases)?
    # What was the worst seven day period in Rockingham County for new COVID cases (in terms of absolute number of cases)?
    third_question(data)


