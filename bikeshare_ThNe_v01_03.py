import time
import pandas as pd
import numpy as np
import os 
from time import strptime
import statistics

dir_path = os.path.dirname(os.path.realpath(__file__))

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    AvailableCities = list(CITY_DATA.keys())
    print('Available cities are:\n')
    for cities in range(0, len(AvailableCities)):
        print(str(cities+1), ' - ', AvailableCities[cities])

    UserInputCity = 0

    while UserInputCity <= 0 or UserInputCity >= len(AvailableCities)+1:
        try:
            UserInputCity = int(input('\nPlease choose a city by number: '))
        except:
            print('\nPlease use a number not a string!')
        if UserInputCity <= 0 or UserInputCity >= len(AvailableCities)+1:
            print('\nThe number you chest wasnt in the range of possible inputs.')
            print('Please try again!')

    city = AvailableCities[UserInputCity-1]
    
    # get user input for month (all, january, february, ... , june)
    AvailableMonth = list(['All', 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'])
    print('Available options for month are:\n')
    for monthes in range(0, len(AvailableMonth)):
        print(str(monthes), ' - ', AvailableMonth[monthes])

    UserInputMonth = -1

    while UserInputMonth <= -1 or UserInputMonth >= len(AvailableMonth):
        try:
            UserInputMonth = int(input('\nPlease choose a month option by number: '))
        except:
            print('\nPlease use a number not a string!')
        if UserInputMonth <= -1 or UserInputMonth >= len(AvailableMonth):
            print('\nThe number you chest wasnt in the range of possible inputs.')
            print('Please try again!')

    month = AvailableMonth[UserInputMonth]

    # get user input for day of week (all, monday, tuesday, ... sunday)
    AvailableDays = list(['All', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
    print('Available options for days are:\n')
    for days in range(0, len(AvailableDays)):
        print(str(days), ' - ', AvailableDays[days])

    UserInputDay = -1

    while UserInputDay <= -1 or UserInputDay >= len(AvailableDays):
        try:
            UserInputDay = int(input('\nPlease choose a month option by number: '))
        except:
            print('\nPlease use a number not a string!')
        if UserInputDay <= -1 or UserInputDay >= len(AvailableDays):
            print('\nThe number you chest wasnt in the range of possible inputs.')
            print('Please try again!')

    day = AvailableDays[UserInputDay]
    
    print('\nYou chest the following combination:')
    print('\nThe city is:', city.title())
    print('\nThe month is:', month.title())
    print('\nThe day is:', day.title())
    
    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    try:
        dfRaw = pd.read_csv(dir_path.replace('\\','/') + '/' + CITY_DATA[city])
        print('Loaded the following file:\n')
        print(dir_path.replace('\\','/') + '/' + CITY_DATA[city] + '\n')
    except:
        print('Error in loading the file')

    dfRaw['DateTime'] = pd.to_datetime(dfRaw['Start Time'])

    if month != 'All':
        MonthNumber = strptime(month, '%B').tm_mon
        df = dfRaw.loc[dfRaw['DateTime'].dt.month == MonthNumber]
        print('Filtered dataframe for ' + month)
    else:
        df = dfRaw
        print('No filtering for month')
        
    if day != 'All':
        DayNumber = strptime(day, '%A').tm_wday
        df = df.loc[df['DateTime'].dt.weekday == DayNumber]
        print('Filtered dataframe for ' + day)
    else:
        df = dfRaw
        print('No filtering for day')
        
    print('-'*40)
        
    return df


def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    if month == 'All':
           MonthVec = pd.to_datetime(df['Start Time']).dt.month
           MonthHist = MonthVec.value_counts()
           print('The month ' + str(MonthHist.nlargest(1).index[0]) + ' is the most common month with ' + str(MonthHist.nlargest(1).loc[MonthHist.nlargest(1).index[0]]) + ' Hits')

    # display the most common day of week
    if day == 'All':
           DayVec = pd.to_datetime(df['Start Time']).dt.dayofweek
           DayHist = DayVec.value_counts()
           print('The day ' + str(DayHist.nlargest(1).index[0]) + ' is the most common day with ' + str(DayHist.nlargest(1).loc[DayHist.nlargest(1).index[0]]) + ' Hits')

    # display the most common start hour
    HoursVec = pd.to_datetime(df['Start Time']).dt.hour
    HoursHist = HoursVec.value_counts()
    print('The hour ' + str(HoursHist.nlargest(1).index[0]) + ' is the most common hour with ' + str(HoursHist.nlargest(1).loc[HoursHist.nlargest(1).index[0]]) + ' Hits')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    StartStationVec = df['Start Station']
    StartStationHist = StartStationVec.value_counts()
    print('The most commonly used start station is \'' + str(StartStationHist.nlargest(1).index[0]) + '\' with ' + str(StartStationHist.nlargest(1).loc[StartStationHist.nlargest(1).index[0]]) + ' Hits')

    # display most commonly used end station
    EndStationVec = df['End Station']
    EndStationHist = EndStationVec.value_counts()
    print('The most commonly used end station is \'' + str(EndStationHist.nlargest(1).index[0]) + '\' with ' + str(EndStationHist.nlargest(1).loc[EndStationHist.nlargest(1).index[0]]) + ' Hits')


    # display most frequent combination of start station and end station trip
    RouteStationVec = 'from \'' + df['Start Station'] + '\' to \'' + df['End Station'] + '\''
    RouteStationHist = RouteStationVec.value_counts()
    print('The most commonly used route is \'' + str(RouteStationHist.nlargest(1).index[0]) + '\' with ' + str(RouteStationHist.nlargest(1).loc[RouteStationHist.nlargest(1).index[0]]) + ' Hits')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()


    # display total travel time
    TotalTravelTime = sum(df['Trip Duration'])/3600
    print('The total time travelled is ' + str(round(TotalTravelTime,2)) + ' Hours')

    # display mean travel time
    MeanTravelTime = statistics.mean(df['Trip Duration'])/60
    print('The mean time travelled is ' + str(round(MeanTravelTime, 2)) + ' Minutes')
    

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    UserTypeVec = df['User Type']
    UserTypeHist = UserTypeVec.value_counts()
    print('\nThe user type distribution in the dataset is as follows:')
    for users in range(0, len(UserTypeHist)):
        print(str(UserTypeHist.index[users]) + ' with ' + str(UserTypeHist.loc[UserTypeHist.index[users]]) + ' Participants')

    # Display counts of gender
    try:
        GenderVec = df['Gender']
        GenderHist = GenderVec.value_counts()
        print('\nThe users gender distribution in the dataset is as follows:')
        for users in range(0, len(GenderHist)):
            print(str(GenderHist.index[users]) + ' with ' + str(GenderHist.loc[GenderHist.index[users]]) + ' Participants')
    except:
        print('\nThe dataset doesn\'t contain any gender specific information')
        
    # Display earliest, most recent, and most common year of birth
    try:
        BirthVec = df['Birth Year']
        print('\nThe oldest customer was born in ' + str(int(min(BirthVec))))
        print('The youngest customer was born in ' + str(int(max(BirthVec))))
        BirthHist = BirthVec.value_counts()
        print('The most common birthyear is ' + str(int(BirthHist.nlargest(1).index[0])) + ' with ' + str(BirthHist.nlargest(1).loc[BirthHist.nlargest(1).index[0]]) + ' customers beeing born in this year')
    except:
        print('\nThe dataset doesn\'t contain any birthyear specific information')
        

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data_lookup(df):
    UserRawData = 0 #set intitial variable

    while UserRawData <= 0:
        # Input prompt if the user wants to see raw data
        UserRawAns = input('\nDo you want to see the raw data based on your filters? Please type yes or no!:')
        # Setting variables for the raw data
        if UserRawAns == 'yes':
            UserRawData = 1
        elif UserRawAns == 'no':
            UserRawData = 2
            break
        else:
            print('\nPlease answer with yes or no!')
            
        if UserRawData == 1:
    
            StartRow = 0
            Endrow = 5
            Scroll = 1
            UserScrollAns = 'yes'
            
            while Scroll == 1:
                if UserScrollAns == 'yes':
                    for RowIndex in range(StartRow, Endrow):
                        print(df.iloc[RowIndex])
                        print('\n')
                UserScrollAns = input('\nDo you want to see 5 more entries? Please type yes or no!:')
                if UserScrollAns == 'no':
                    Scroll = 0
                elif UserScrollAns == 'yes':
                    Scroll = 1
                    StartRow += 5
                    Endrow += 5
                else:
                    print('\nPlease answer with yes or no!')
        


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        
        if len(df) == 0:
            print('\nThere are no data found which fit to your filters')
            break

        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data_lookup(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
