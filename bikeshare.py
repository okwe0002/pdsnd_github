import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv','new york city': 'new_york_city.csv','washington': 'washington.csv' }

months = ['all','january','february','march','april','may','june']

days = ['all','monday','tuesday','wednesday','thursday','friday','saturday','sunday']


def check_filters():
    """ Preliminary check which ensure user inputs are accurate

        Returns: Accurate user inputs for city, month, day"""


    while True:
        city = input("Enter the name of the city to explore: ").lower()
        if city in CITY_DATA:
            break
        else:
            print('Looks like there is no data for that city. Please try again with a valid city from: Washington, New York City and Chicago')

    while True:
        month = input("Enter the name of the month to filter by, or 'all' to apply no month filter: ").lower()
        if month in months:
            break
        else:
            print('Looks like {} is not a valid entry. Please enter a month from January to June or enter "all" to apply no filter'.format(month))

    while True:
        day = input("Enter the name of the day of week to filter by, or 'all' to apply no day filter: ").lower()
        if day in days:
            break
        else:
            print('Looks like {} is not a valid entry. Please enter a day from Sunday to Monday, or "all" to apply no filter'.format(day))
    return city, month, day


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
    city, month, day = check_filters()

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

    df = pd.read_csv(CITY_DATA[city]).rename(columns={'Unnamed: 0': 'Id'}).set_index(['Id'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['hour'] = df['Start Time'].dt.hour
    df['month'] = df['Start Time'].dt.month_name()
    df['day of the week'] = df['Start Time'].dt.day_name()

    if month != 'all':
       df = df[df['month'] == (month.title())]

    if day != 'all':
       df = df[df['day of the week'] == (day.title())]

    return df










def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print('The most common month is {}'.format(df['month'].mode()[0]))

    # display the most common day of week
    print('The most common day of the week is {}'.format(df['day of the week'].mode()[0]))

    # display the most common start hour
    print('The most common start hour is {}'.format(df['hour'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('The most commonly used start station is {}'.format(df['Start Station'].mode()[0]))

    # display most commonly used end station
    print('The most commonly used end station is {}'.format(df['End Station'].mode()[0]))

    # display most frequent combination of start station and end station trip
    print('The most frequent combination of start station and end station trip was from: "{}" TO "{}"'.format(((df['Start Station'] + ','+ df['End Station']).mode()[0]).split(',')[0], ((df['Start Station'] + ','+ df['End Station']).mode()[0]).split(',')[1]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    #display total travel time in minutes
    travel_time = df['Trip Duration']/60
    print('Total travel time was {} minutes'.format(int(travel_time.sum())))



    # display mean travel time
    print('The average travel time per trip was {} minutes'.format(int(travel_time.mean())))

    # display the shortest travel time
    print('The shortest trip lasted {} seconds'.format(int(travel_time.min() * 60)))

    # display the londest travel time
    print('The longest trip lasted {} minutes'.format(int(travel_time.max())))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('Counts by User type: Subscribers - {} and Customers - {} '.format(df['User Type'].value_counts()['Subscriber'], df['User Type'].value_counts()['Customer']))


    # Display counts of gender
    try:
        print('Counts by Gender: Male - {} and Female - {} '.format(df['Gender'].value_counts()['Male'], df['Gender'].value_counts()['Female']))
    except KeyError:
        print('No gender based stats for the city of Washington')

    # Display counts of gender based on user type

    try:                                                                            # Handle for any errors
        grouped_data = df.groupby('Gender')['User Type'].value_counts()             # Get the grouped data
        classes = df['User Type'].unique()
        if len(classes) > 1:
           message = 'Subscriber: {}, Customer: {}'
           count = 1
           i= 0
           while i < len(grouped_data) and count < len(grouped_data):                #Display grouped data
                 print('{}'.format(grouped_data.index[i][0]))
                 print(message.format(grouped_data[i], grouped_data[count]))
                 count+=2
                 i+=2
    except KeyError:
         print('No gender based stats for the city of Washington')

        # Display earliest, most recent, and most common year of birth
    try:
        print('The earliest year of birth is {}'.format(int(df['Birth Year'].min())))

        print('The most recent year of birth is {}'.format(int(df['Birth Year'].max())))

        print('The most common year of birth is {}'.format(int(df['Birth Year'].mode()[0])))
    except KeyError:
        print('No birth year stats for the city of Washington')



    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_data(df):
    """ Displays the 5 lines of data at a time, sequentially, at users request

        Input: DataFrame
        Returns: 5 rows of DataFrame sequentially"""
    row_ind = 0
    offset = 5
    while True:
        raw_data = input('Would you like to see 5 lines of the data? Enter yes or no ')
        if raw_data.lower() != 'yes':
            break
        print(df.iloc[row_ind:offset, :])
        row_ind = offset
        offset += 5



def main():
    while True:
         city, month, day = get_filters()
         df = load_data(city, month, day)
         try:
            time_stats(df)
         except Exception as e:
                print('{}'.format(e))
                print('Looks like there was an issue getting bikeshare stats for {}. {} or {} may not be a valid month or day of the week in the data. Please try again!'.format(city,month,day))
                continue
         station_stats(df)
         trip_duration_stats(df)
         user_stats(df)
         display_data(df)
         restart = input('\nWould you like to restart? Enter yes or no.\n')
         if restart.lower() != 'yes':
             print('Thanks for exploring bikeshare data!')
             break


if __name__ == "__main__":
	main()
