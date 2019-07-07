## Import all necessary packages and functions
import calendar
import csv
from datetime import datetime
from datetime import timedelta
import time
import statistics

## Filenames
chicago = 'chicago.csv'
new_york_city = 'new_york_city.csv'
washington = 'washington.csv'

def csv_to_dict(file):
    '''Converts lines imprted from a CSV file to a Python Dictionary data type.
    Code taken from:
    https://stackoverflow.com/questions/21572175/convert-csv-file-to-list-of-dictionaries/21572244
    
    Args:
        file
    Returns:
        (dict): result
    '''
    with open(file) as f:
        result = [{k: v for k, v in row.items()}
            for row in csv.DictReader(f, skipinitialspace=True)]
    return result

def load_city(city):
    '''Loads one of the city data files: Chicago, New York, Washington. Also, converts data types from string to their appropriate
    for Statistical processing.

    Args:
        city
    Returns:
        (dict): load_city
    '''
    load_city = csv_to_dict(city)
    for i in load_city:
        i['Start Time'] = datetime.strptime(i['Start Time'], '%Y-%m-%d %H:%M:%S')
        i['End Time'] = datetime.strptime(i['End Time'], '%Y-%m-%d %H:%M:%S')
        i['Trip Duration'] = float(i['Trip Duration'])
        if 'Gender' in i:
            if i['Gender'].strip() == '':
                i['Gender'] = 'Unknown'
        if 'Birth Year' in i:
            if i['Birth Year'].strip() == '':
                i['Birth Year'] = int(0)
            else:
                i['Birth Year'] = int(float(i['Birth Year']))
    return load_city

def get_city():
    '''Asks the user for a city and returns the filename for that city's bike share data.

    Args:
        none
    Returns:
        (str): Filename for a city's bikeshare data
    '''
    while True:
        city = input('\nHello, Let\'s explore some US bikeshare data!\n'
                     'Would you like to see data for Chicago, New York, or Washington?\n')
        if city.upper() == 'CHICAGO':
            return chicago
        elif city.upper() == 'NEW YORK':
            return new_york_city
        elif city.upper() == 'WASHINGTON':
            return washington
        else:
            print('\nERROR: Please enter Chicago, New York, or Washington!')

def get_time_period():
    '''Asks the user for a time period and returns the specified filter.

    Args:
        none
    Returns:
        (str): time_period, month, day
    '''
    month = 0
    day = 0
    
    while True:
        time_period = input('\nWould you like to filter the data by month, day, or not at'
                        ' all? Type "none" for no time filter.\n')
        if time_period.upper() == 'MONTH':
            month = get_month()
            return time_period.upper(), month, day
        elif time_period.upper() == 'DAY':
            month = get_month()
            day = get_day(month)
            return time_period.upper(), month, day
        elif time_period.upper() == 'NONE':
            return time_period.upper(), month, day
        else:
            print('\nERROR: month, day, or none!')

def get_month():
    '''Asks the user for a month and returns the specified month.

    Args:
        none
    Returns:
        (str): January, February, March, April, May, or June
    '''
    months = []
    # Create a list of months Jan-June and their abbreviation
    for i in range(1, 7):
        #months.append(calendar.month_abbr[i])
        months.append(calendar.month_name[i])

    while True:
        month = input('\nWhich month? January, February, March, April, May, or June?\n')
        if month in months:
            return month
        else:
            print('\nERROR: January, February, March, April, May, or June!')

def get_day(month):
    '''Asks the user for a day and returns the specified day.

    Args:
        month
    Returns:
        (int): 1-31
    '''
    correct_date = False
    month = list(calendar.month_name).index(month)
    while correct_date == False:
        day = int(input('\nWhich day? Please type your response as an integer.\n'))
        try:
            newDate = datetime(2017, month, day)
            correct_date = True
        except ValueError:
            print('{} is NOT a valid day in {}, 2017.'.format(day, calendar.month_name[month]))
            correct_date = False
    return newDate

def popular_month(city_file, time_period):
    '''Answers the Question: What is the most popular month for start time?

    Args:
        city_file, time_period (currently not used)
    Returns:
        (str): Popular Month
    '''
    #Create list of 12 elements corresponding to each month
    months = [0] * 12
    for i in city_file:
        month = int(i['Start Time'].strftime('%m'))
        months[month-1] += 1
    #Find Max Value
    max_value = max(months)
    #Find Max Value Index
    max_index = months.index(max_value)
    #Convert Max Value Index to Date
    popular_month = datetime.strptime(str(max_index + 1), '%m')
    #Convert Date to calendar month
    popular_month = popular_month.strftime('%B')

    return popular_month

def popular_day(city_file, time_period):
    '''Answers the Question: What is the most popular day of week (Monday, Tuesday, etc.) for start time?
    Args:
        city_file, time_period
    Returns:
        (str): Popular Day
    '''
    days = [0] * 7

    if time_period[0] == 'MONTH':
        month = time_period[1]
        for i in city_file:
            if month == i['Start Time'].strftime('%B'):
                day = (int(i['Start Time'].strftime('%w')) + 6) % 7
                days[day] += 1
    else: #time_period[0] == 'NONE'
        for i in city_file:
            day = (int(i['Start Time'].strftime('%w')) + 6) % 7
            days[day] += 1
    #Find Max Value
    max_value = max(days)
    #Find Max Value Index
    max_index = days.index(max_value)
    #Convert Max Value Index to Weekday
    popular_day = calendar.day_name[max_index]

    return popular_day

def popular_hour(city_file, time_period):
    '''Answers the Question: What is the most popular hour of day for start time?
    Args:
        city_file, time_period
    Returns:
        (int): Popular Hour
    '''
    hours = [0] * 24
    
    if time_period[0] == 'MONTH':
        month = time_period[1]
        for i in city_file:
            if month == i['Start Time'].strftime('%B'):
                hour = int(i['Start Time'].strftime('%H'))
                hours[hour] += 1
    elif time_period[0] == 'DAY':
        day = time_period[2].date()
        for i in city_file:
            if day == i['Start Time'].date():
                hour = int(i['Start Time'].strftime('%H'))
                hours[hour] += 1
    else: #time_period[0] == 'NONE'
        for i in city_file:
            hour = int(i['Start Time'].strftime('%H'))
            hours[hour] += 1
    #Find Max Value
    max_value = max(hours)
    #Find Max Value Index
    max_index = hours.index(max_value)
    popular_hour = max_index

    return popular_hour

def trip_duration(city_file, time_period):
    '''Answers the Question: What is the total trip duration and average trip duration?
    Args:
        city_file, time_period
    Returns:
        (str): trip_total, trip_average
    '''
    trip_total = 0
    trip_average = 0
    trips = []
    if time_period[0] == 'MONTH':
        month = time_period[1]
        for i in city_file:
            if month == i['Start Time'].strftime('%B'):
                trip_stats = (i['End Time'] - i['Start Time']).total_seconds()
                trip_total += trip_stats
                trips.append(trip_stats)
    elif time_period[0] == 'DAY':
        day = time_period[2].date()
        for i in city_file:
            if day == i['Start Time'].date():
                trip_stats = (i['End Time'] - i['Start Time']).total_seconds()
                trip_total += trip_stats
                trips.append(trip_stats)
    else: #time_period[0] == 'NONE'
        for i in city_file:
            trip_stats = (i['End Time'] - i['Start Time']).total_seconds()
            trip_total += trip_stats
            trips.append(trip_stats)

    if not trips:
        return None
    else:
        trip_average = trip_total / len(trips)

    return str(timedelta(seconds=trip_total)), str(timedelta(seconds=trip_average))

def popular_stations(city_file, time_period):
    '''Answers the Question: What is the most popular start station and most popular end station?
    Args:
        city_file, time_period
    Returns:
        (str): popular_start_station, popular_end_station
    '''
    popular_start_stations = {}
    popular_end_stations = {}
    
    if time_period[0] == 'MONTH':
        month = time_period[1]
        for i in city_file:
            if month == i['Start Time'].strftime('%B'):
                popular_start_stations[i['Start Station']] = popular_start_stations.get(i['Start Station'], 0) + 1
                popular_end_stations[i['End Station']] = popular_end_stations.get(i['End Station'], 0) + 1
    elif time_period[0] == 'DAY':
        day = time_period[2].date()
        for i in city_file:
            if day == i['Start Time'].date():
                popular_start_stations[i['Start Station']] = popular_start_stations.get(i['Start Station'], 0) + 1
                popular_end_stations[i['End Station']] = popular_end_stations.get(i['End Station'], 0) + 1
    else: #time_period[0] == 'NONE'
        for i in city_file:
            popular_start_stations[i['Start Station']] = popular_start_stations.get(i['Start Station'], 0) + 1
            popular_end_stations[i['End Station']] = popular_end_stations.get(i['End Station'], 0) + 1

    if not popular_start_stations:
        return None
    else:
        popular_start_station = max(popular_start_stations, key=popular_start_stations.get)
        popular_end_station = max(popular_end_stations, key=popular_end_stations.get)
    
    return popular_start_station, popular_end_station
    
def popular_trip(city_file, time_period):
    '''Answers the Question: What is the most popular trip?
    Args:
        city_file, time_period
    Returns:
        (str): popular_trip
    '''
    trips = {}
    
    if time_period[0] == 'MONTH':
        month = time_period[1]
        for i in city_file:
            if month == i['Start Time'].strftime('%B'):
                key = i['Start Station'], i['End Station'] #Cause Tuples are immutable
                trips[key] = trips.get(key, 0) + 1
    elif time_period[0] == 'DAY':
        day = time_period[2].date()
        for i in city_file:
            if day == i['Start Time'].date():
                key = i['Start Station'], i['End Station'] #Cause Tuples are immutable
                trips[key] = trips.get(key, 0) + 1
    else: #time_period[0] == 'NONE'
        for i in city_file:
            key = i['Start Station'], i['End Station'] #Cause Tuples are immutable
            trips[key] = trips.get(key, 0) + 1

    if not trips:
        return None
    else:
        popular_trip = max(trips, key=trips.get)
        return popular_trip
            
def users(city_file, time_period):
    '''Answers the Question: What are the counts of each user type?
    Args:
        city_file, time_period
    Returns:
        (dict): users
    '''
    users = {}
    
    if time_period[0] == 'MONTH':
        month = time_period[1]
        for i in city_file:
            if month == i['Start Time'].strftime('%B'):
                users[i['User Type']] = users.get(i['User Type'], 0) + 1
    elif time_period[0] == 'DAY':
        day = time_period[2].date()
        for i in city_file:
            if day == i['Start Time'].date():
                users[i['User Type']] = users.get(i['User Type'], 0) + 1
    else: #time_period[0] == 'NONE'
        for i in city_file:
            users[i['User Type']] = users.get(i['User Type'], 0) + 1

    return users

def gender(city_file, time_period):
    '''Answers the Question: What are the counts of gender?
    Args:
        city_file, time_period
    Returns:
        (dict): users
    '''
    if 'Gender' not in city_file[0]:
        return None

    genders = {}

    if time_period[0] == 'MONTH':
        month = time_period[1]
        for i in city_file:
            if month == i['Start Time'].strftime('%B'):
                genders[i['Gender']] = genders.get(i['Gender'], 0) + 1
    elif time_period[0] == 'DAY':
        day = time_period[2].date()
        for i in city_file:
            if day == i['Start Time'].date():
                genders[i['Gender']] = genders.get(i['Gender'], 0) + 1
    else: #time_period[0] == 'NONE'
        for i in city_file:
            genders[i['Gender']] = genders.get(i['Gender'], 0) + 1

    return genders

def birth_years(city_file, time_period):
    '''Answers the Question: What are the earliest, most recent, and most popular birth years?
    Args:
        city_file, time_period
    Returns:
        (int): earliest birth year, most recent birth year, most popular birth year
    '''
    if 'Birth Year' not in city_file[0]:
        return None

    birth_years = {}

    if time_period[0] == 'MONTH':
        month = time_period[1]
        for i in city_file:
            if month == i['Start Time'].strftime('%B'):
                if i['Birth Year'] != 0:
                    birth_years[i['Birth Year']] = birth_years.get(i['Birth Year'], 0) + 1
    elif time_period[0] == 'DAY':
        day = time_period[2].date()
        for i in city_file:
            if day == i['Start Time'].date():
                if i['Birth Year'] != 0:
                    birth_years[i['Birth Year']] = birth_years.get(i['Birth Year'], 0) + 1
    else: #time_period[0] == 'NONE'
        for i in city_file:
            if i['Birth Year'] != 0:
                birth_years[i['Birth Year']] = birth_years.get(i['Birth Year'], 0) + 1

    #If empty dictionary
    if not birth_years:
        return None
    else:
        earliest_year = min(birth_years.keys())
        latest_year = max(birth_years.keys())
        popular_year = max(birth_years, key=birth_years.get)

    return earliest_year, latest_year, popular_year

def display_data(city_file, time_period):
    '''Displays five lines of data if the user specifies that they would like to.
    After displaying five lines, ask the user if they would like to see five more,
    continuing asking until they say stop.

    Args:
        none.
    Returns:
        none.
    '''
    display = input('\nWould you like to view individual trip data? '
                    'Type \'yes\' or \'no\'. ')


    if display.lower() == 'yes':
        if time_period[0] == 'MONTH':
            month = time_period[1]
            count = 0
            for index, item in enumerate(city_file):
                #Print the Field Header First
                if index == 0:
                    header = str(list(item.keys())[0]) + ', '
                    for key in list(item.keys())[1:-2]:
                        header += str(key) + ', '
                    header += str(list(item.keys())[-1])
                    print(header)
                if month == item['Start Time'].strftime('%B'):
                    count += 1
                    #Print 5 records
                    data = str(list(item.values())[0]) + ', '
                    for value in list(item.values())[1:-2]:
                        data += str(value) + ', '
                    data += str(list(item.values())[-1])
                    print(data)
                    if index+1 == len(city_file):
                        print('\nThis is the end of the data.')
                        return
                    elif (count) % 5 == 0 or (count) % 10 ==0:
                        display = input('\nWould you like to view individual trip data? '
                                        'Type \'yes\' or \'no\'. ')
                        if display.lower() != 'yes':
                            return
            print('\nThis is the end of the data.')
        elif time_period[0] == 'DAY':
            day = time_period[2].date()
            count = 0
            for index, item in enumerate(city_file):
                #Print the Field Header First
                if index == 0:
                    header = str(list(item.keys())[0]) + ', '
                    for key in list(item.keys())[1:-2]:
                        header += str(key) + ', '
                    header += str(list(item.keys())[-1])
                    print(header)
                if day == item['Start Time'].date():
                    count += 1
                    #Print 5 records
                    data = str(list(item.values())[0]) + ', '
                    for value in list(item.values())[1:-2]:
                        data += str(value) + ', '
                    data += str(list(item.values())[-1])
                    print(data)
                    if index+1 == len(city_file):
                        print('\nThis is the end of the data.')
                        return
                    elif (count) % 5 == 0 or (count) % 10 ==0:
                        display = input('\nWould you like to view individual trip data? '
                                        'Type \'yes\' or \'no\'. ')
                        if display.lower() != 'yes':
                            return
            print('\nThis is the end of the data.')
        else: #time_period[0] == 'NONE'
            for index, item in enumerate(city_file):
                #Print the Field Header First
                if index == 0:
                    header = str(list(item.keys())[0]) + ', '
                    for key in list(item.keys())[1:-2]:
                        header += str(key) + ', '
                    header += str(list(item.keys())[-1])
                    print(header)
                #Print 5 records
                data = str(list(item.values())[0]) + ', '
                for value in list(item.values())[1:-2]:
                    data += str(value) + ', '
                data += str(list(item.values())[-1])
                print(data)
                if index+1 == len(city_file):
                    print('\nThis is the end of the data.')
                    return
                elif (index+1) % 5 == 0 or (index+1) % 10 ==0:
                    display = input('\nWould you like to view individual trip data? '
                                    'Type \'yes\' or \'no\'. ')
                    if display.lower() != 'yes':
                        return

def statistics():
    '''Calculates and prints out the descriptive statistics about a city and time period
    specified by the user via raw input.

    Args:
        none.
    Returns:
        none.
    '''
    # Filter by city (Chicago, New York, Washington)
    city = get_city()
    #city = 'test.csv'
    
    # Load city
    city_file = [] # Reset variable each time to avoid running out of memory
    print("\nLoading city (WARNING this could take up to 10 minutes)...")
    start_time = time.time()
    city_file = load_city(city)
    print("{} records loaded, that took {} seconds.".format(len(city_file), time.time() - start_time))
    
    # Filter by time period (month, day, none)
    time_period = get_time_period()
    print('\nCalculating the first statistic...')
    start_time = time.time()

    # What is the most popular month for start time?
    if time_period[0] == 'NONE':
        # Call popular_month function and print the results
        print('Most popular month: {}'.format(popular_month(city_file, time_period)))
        print("That took %s seconds." % (time.time() - start_time))
        print("\nCalculating the next statistic...")
        start_time = time.time()

    # What is the most popular day of week (Monday, Tuesday, etc.) for start time?
    if time_period[0] == 'NONE' or time_period[0] == 'MONTH':
        # Call popular_day function and print the results
        print('Most popular day of week: {}'.format(popular_day(city_file, time_period)))
        print("That took %s seconds." % (time.time() - start_time))
        print("\nCalculating the next statistic...")
        start_time = time.time()

    # What is the most popular hour of day for start time?
    print('Most popular hour of day: {}'.format(popular_hour(city_file, time_period)))
    print("That took %s seconds." % (time.time() - start_time))
    print("\nCalculating the next statistic...")
    start_time = time.time()

    # What is the total trip duration and average trip duration?
    trip_stats = trip_duration(city_file, time_period)
    if trip_stats is not None:
        print("Average trip duration: {}".format(trip_stats[1]))
        print("Total trip duration: {}".format(trip_stats[0]))
    else:
        print("No trip data found.")
    print("That took %s seconds." % (time.time() - start_time))
    print("\nCalculating the next statistic...")
    start_time = time.time()

    # What is the most popular start station and most popular end station?
    popular_station = popular_stations(city_file, time_period)
    if popular_station is not None:
        print("Most popular start station: \"{}\"".format(popular_station[0]))
        print("Most popular end station: \"{}\"".format(popular_station[1]))
    else:
        print("No station data found.")
    print("That took %s seconds." % (time.time() - start_time))
    print("\nCalculating the next statistic...")
    start_time = time.time()

    # What is the most popular trip?
    pop_trip = popular_trip(city_file, time_period)
    if pop_trip is not None:
        print("Most popular trip: \"{}\" to \"{}\"".format(pop_trip[0], pop_trip[1]))
    else:
        print("No trip data found.")
    print("That took %s seconds." % (time.time() - start_time))
    print("\nCalculating the next statistic...")
    start_time = time.time()

    # What are the counts of each user type?
    user_types = users(city_file, time_period)
    for user in user_types:
        print("{}s: {}".format(user, user_types[user]))
    print("That took %s seconds." % (time.time() - start_time))
    print("\nCalculating the next statistic...")
    start_time = time.time()

    # What are the counts of gender?
    gender_types = gender(city_file, time_period)
    if gender_types is None:
        print("Gender info not in data file.")
    else:
        for genders in gender_types:
            print("{}s: {}".format(genders, gender_types[genders]))
    print("That took %s seconds." % (time.time() - start_time))
    print("\nCalculating the next statistic...")
    start_time = time.time()

    # What are the earliest, most recent, and most popular birth years?
    births = birth_years(city_file, time_period)
    if births is None:
        print("Birth year info not in data file.")
    else:
        print("Earliest birth year: {}".format(births[0]))
        print("Most recent birth year: {}".format(births[1]))
        print("Most popular birth year: {}".format(births[2]))

    print("That took %s seconds." % (time.time() - start_time))

    # Display five lines of data at a time if user specifies that they would like to
    display_data(city_file, time_period)

    # Restart?
    restart = input('\nWould you like to restart? Type \'yes\' or \'no\'. ')
    if restart.lower() == 'yes':
        statistics()

if __name__ == "__main__":
    statistics()
#EOF