# First Refactoring
import time
import pandas as pd

CITY_DATA = { "chicago": "chicago.csv",
              "new york city": "new_york_city.csv",
              "washington": "washington.csv" }

MONTHS = {
        "all": 0, "january": 1, "february": 2, "march": 3,
        "april": 4, "may": 5, "june": 6,
        "july": 7, "august": 8, "september": 9,
        "october": 10, "november": 11, "december": 12
        }

DAYS = {
        "all": 0, "monday": 1, "tuesday": 2, "wednesday": 3,
        "thursday": 4, "friday": 5, "saturday": 6,
        "sunday": 7
        }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print("Hello! Let\'s explore some US bikeshare data!\n")
    
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    print("|==> Chicago, New York City, Washington <==|")
    print("Please enter a city name from the list above.")
    while True:
        city = input("City: ").strip().lower()
        if city in CITY_DATA.keys():
            print(f"{city.capitalize()} is selected!\n")
            break
        if not city:
            print(f"City cannot be blank.")
        print(f"Your input \"{city}\" is not available")
   
    # get user input for month (all, january, february, ... , june)
    print("January, February, March, ..., December, All")
    print("Please enter a specific month, or 'all' to select all month.")
    while True:
        month = input("Month: ").strip().lower()
        if month in MONTHS.keys():
            print(f"{month.capitalize()} is selected!\n")
            break
        if not month:
            print(f"Month cannot be blank.")
        print(f"Your input \"{month}\" is invalid")
    

    # get user input for day of week (all, monday, tuesday, ... sunday)
    print("Monday, Tuesday, Wednesday, ..., Sunday, All")
    print("Please enter a specific day of the week, or 'all' to select all days.")
    while True:
        day = input("Day: ").strip().lower()
        if day in DAYS:
            print(f"{day.capitalize()} is selected!\n")
            break
        if not day:
            print(f"Day cannot be blank.")
        print(f"Your input \"{day}\" is invalid")

    print("-"*40)
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

    # Parse start time and end time as dates for ease of access and query
    df = pd.read_csv(CITY_DATA[city], parse_dates=["Start Time", "End Time"])

    if MONTHS[month] > 0:
        df = df[df["Start Time"].dt.month == MONTHS[month]]
    
    if DAYS[day] > 0:
        df = df[df["Start Time"].dt.day_name().apply(str.lower) == day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print("\nCalculating The Most Frequent Times of Travel...\n")
    start_time = time.time()

    # display the most common month
    most_common_month = df.groupby(df["Start Time"].dt.month_name())["Start Time"] \
                          .count() \
                          .sort_values(ascending=False)

    print(f"Most common month was {most_common_month.index[0]}.\nWith {most_common_month.values[0]} users using our service that month")
    print("="*25)

    # display the most common day of week
    most_common_day = df.groupby(df["Start Time"].dt.day_name())["Start Time"] \
                        .count() \
                        .sort_values(ascending=False)
                        
    print(f"Most common day was {most_common_day.index[0]}.\nWith {most_common_day.values[0]} users using our service on that day")
    print("="*25)

    # display the most common start hour
    most_common_time = df.groupby(df["Start Time"].dt.hour)["Start Time"] \
                         .count() \
                         .sort_values(ascending=False)

    print(f"Most common start hour was around {most_common_time.index[0]:02}:00.\nWith {most_common_time.values[0]} users using our service around that time")
    print("="*25)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-"*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print("\nCalculating The Most Popular Stations and Trip...\n")
    start_time = time.time()

    # display most commonly used start station
    most_common_start = df.groupby(df["Start Station"])["Start Station"] \
                          .count() \
                          .sort_values(ascending=False)

    print(f"Most commonly used start station was {most_common_start.index[0]}.\nWith {most_common_start.values[0]} users started their trip there")
    print("="*25)

    # display most commonly used end station
    most_common_end = df.groupby(df["End Station"])["End Station"] \
                        .count() \
                        .sort_values(ascending=False)

    print(f"Most commonly used end station was {most_common_end.index[0]}.\nWith {most_common_end.values[0]} users ended their trip there")
    print("="*25)

    # display most frequent combination of start station and end station trip
    most_common_combination = df.groupby(["Start Station", "End Station"])["Start Station"] \
                                .count() \
                                .sort_values(ascending=False)

    print(f"Most commonly used station combination were;\nStart Station:\t{most_common_combination.index[0][0]}\nEnd Station:\t{most_common_combination.index[0][1]}.\nWith {most_common_combination.values[0]} users chose to commute between those stations")
    print("="*25)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-"*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print("\nCalculating Trip Duration...\n")
    start_time = time.time()

    # display total travel time
    total_travel_time = df["Trip Duration"].sum()

    print(f"Total time traveled: {total_travel_time}")
    print("="*25)

    # display mean travel time
    mean_travel_time = df["Trip Duration"].mean()

    print(f"Average time traveled: {mean_travel_time}")
    print("="*25)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-"*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print("\nCalculating User Stats...\n")
    start_time = time.time()

    # Display counts of user types
    user_count = df.groupby(df["User Type"])["User Type"] \
                   .count()

    print(f"Number of Subscribers:\t{user_count['Subscriber']}")
    print(f"Number of Customers:\t{user_count['Customer']}")
    print("="*25)

    # Early exit if city equals to washington
    if city != "washington":

        # Display counts of gender
        gender_count = df.groupby(df["Gender"])["Gender"] \
                         .count()

        print(f"Number of Female:\t{gender_count['Female']}")
        print(f"Number of Male:\t\t{gender_count['Male']}")
        print("="*25)


        # Display earliest, most recent, and most common year of birth
        earliest_yob = int(df["Birth Year"].min())
        most_recent_yob = int(df["Birth Year"].max())
        most_common_yob = int(df["Birth Year"].mode()[0])

        print(f"Earliest Year of Birth:\t\t{earliest_yob}")
        print(f"Most Recent Year of Birth:\t{most_recent_yob}")
        print(f"Most Common Year of Birth:\t{most_common_yob}")
        print("="*25)

    else:
        print("Washington city has no Gender and Birth Year data")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-"*40)

def display_data(df: pd.DataFrame):
    """Displays raw data (if needed)."""
    cursor = 0
    print("Would you like to see the raw data?.")
    while True:
        print(f"See Data {cursor} to {cursor+10}?")
        answer = input("Yes/No: ").strip().lower()
        if answer in ("no","n"):
            break
        if answer in ("yes","y"):
            print(df.iloc[cursor:cursor+10])
            cursor += 10
            if cursor >= len(df):
                print("The end of data is reached")
                break
            continue
        if not answer:
            print(f"Answer cannot be blank.")

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        # Get rid of "Unnamed" column
        df.rename(columns={"Unnamed: 0" :"Transaction ID"}, inplace=True)

        # Handles empty DataFrame
        if not df.empty:
            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df, city)
            display_data(df)

        else:
            print("There are no record for the specified city, month, and day")

        restart = input("\nWould you like to restart? Enter yes or no.\n")
        if restart.lower() != "yes":
            break
        
    print("Thank you!")


if __name__ == "__main__":
	main()
