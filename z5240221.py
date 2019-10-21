import pandas as pd
import matplotlib.pyplot as matplot


def convert_int(n):
    if ',' in n:
        n = n.replace(',', '')
        return int(n)
    else:
        return int(n)


def question_1(check_print=False):
    if check_print:
        print("--------------- question_1 ---------------")
    # importing the data sets
    df1 = pd.read_csv('Olympics_dataset1.csv')
    df2 = pd.read_csv('Olympics_dataset2.csv')

    # merging the data sets
    df = pd.merge(left=df1, right=df2, on=None, left_on='Team', right_on='Team')

    # dropping the first row of the data sets
    df.drop(df.index[0], inplace=True)

    # dropping the unused columns
    df.drop(['Combined Total', 'Unnamed: 7', 'Unnamed: 8', 'Unnamed: 9', 'Unnamed: 10', ], axis='columns', inplace=True)

    # creating a dict to map the renaming of columns
    rename_dict = {
        "Team": "Country",
        "Unnamed: 1": "summer_rubbish",
        "Summer Games": "summer_participation",
        "Unnamed: 3_x": "summer_gold",
        "Unnamed: 4_x": "summer_silver",
        "Unnamed: 5_x": "summer_bronze",
        "Unnamed: 6": "summer_total",
        "Winter Games": "winter_participation",
        "Unnamed: 2": "winter_gold",
        "Unnamed: 3_y": "winter_silver",
        "Unnamed: 4_y": "winter_bronze",
        "Unnamed: 5_y": "winter_total",
    }

    # renaming the columns
    df.rename(columns=rename_dict, inplace=True)

    # removing the 'Totals' row from the data frame
    df = df[df.Country != 'Totals']
    # df.drop(df.index[df.shape[0]-1], inplace=True)

    # printing first five rows of data frame
    if check_print:
        print(df.head().to_string())
    return df


def question_2(check_print=False):
    if check_print:
        print("--------------- question_2 ---------------")
    df = question_1()

    # function for removing the words in brackets
    def remove_words_in_brackets(cell):
        for i in range(len(cell)):
            if cell[i] == '(':
                return cell[:i]
        return cell

    # removing words in brackets
    df['Country'] = df['Country'].map(remove_words_in_brackets)

    # setting index as Country
    df.set_index('Country', inplace=True)

    # removing the undesired columns
    df.drop(['summer_rubbish', 'summer_total', 'winter_total'], axis='columns', inplace=True)

    # printing the data
    if check_print:
        print(df.head().to_string())
    return df


def question_3(check_print=False):
    if check_print:
        print("--------------- question_3 ---------------")
    df = question_2()
    # dropping rows with na values
    df.dropna(how='all', inplace=True)

    # printing values
    if check_print:
        print(df.tail(10).to_string())
    return df


def question_4(check_print=False):
    if check_print:
        print("--------------- question_4 ---------------")
    df = question_3()

    # function for casting string to integer


    # converting string into numbers
    df['summer_gold'] = df['summer_gold'].map(convert_int)

    # printing the country with max gold
    if check_print:
        print(df[df['summer_gold'] == df['summer_gold'].max()].index[0])
    return df


def question_5(check_print=False):
    if check_print:
        print("--------------- question_5 ---------------")
    df = question_4()
    # converting string into numbers
    df['winter_gold'] = df['winter_gold'].map(convert_int)

    # finding the max difference
    max_diff = abs(df['winter_gold'] - df['summer_gold']).max()

    # finding the name of the country
    if check_print:
        print(df[abs(df['winter_gold'] - df['summer_gold']) == max_diff].index[0], max_diff)
    return df


def question_6(check_print=False):
    if check_print:
        print("--------------- question_6 ---------------")
    # changing the str values to numberic values
    df = question_5()
    df['summer_silver'] = df['summer_silver'].map(convert_int)
    df['summer_bronze'] = df['summer_bronze'].map(convert_int)
    df['winter_silver'] = df['winter_silver'].map(convert_int)
    df['winter_bronze'] = df['winter_bronze'].map(convert_int)

    # creating a new column with sum of all medals
    df['total'] = df['summer_gold'] + df['summer_silver'] + df['summer_bronze'] + df['winter_gold'] + df[
        'winter_silver'] + df['winter_bronze']

    # printing the values
    if check_print:
        print(df.sort_values(by='total', ascending=False).head().to_string())
        print(df.sort_values(by='total', ascending=False).tail().to_string())
    return df


def question_7(check_print=False):
    if check_print:
        print("--------------- question_7 ---------------")
    df = question_6()
    # take out top 10 winners
    top_winners = df.sort_values(by='total', ascending=False).head(10)

    # add new column for summer and winter total
    top_winners['winter_total'] = df['winter_gold'] + df['winter_silver'] + df['winter_bronze']
    top_winners['summer_total'] = df['summer_gold'] + df['summer_silver'] + df['summer_bronze']

    # change the sort order
    top_winners_sorted = top_winners.sort_values(by='total')

    # plot
    plt = top_winners_sorted.plot.barh(y=['winter_total', 'summer_total'], stacked=True,
                                       title='Medals for Winter and Summer Games')
    plt.legend(['Winter games', 'Summer games'], ncol=3, edgecolor='None')
    if check_print:
        matplot.show()
    return df


def question_8(check_print=False):
    if check_print:
        print("--------------- question_8 ---------------")
    df = question_6()
    filtered_countries_list = [
        'United States',
        'Great Britain',
        'Japan',
        'New Zealand'
    ]
    filtered_df = df[df.index.str.strip().isin(filtered_countries_list)]

    # removing the undesired columns
    filtered_df.drop(
        ['summer_gold', 'summer_silver', 'summer_bronze', 'summer_participation', 'total', 'winter_participation'],
        axis='columns', inplace=True)

    rename_winter_dict = {
        "winter_gold": "Gold",
        "winter_silver": "Silver",
        "winter_bronze": "Bronze"
    }

    # renaming the columns
    filtered_df.rename(columns=rename_winter_dict, inplace=True)

    # plot
    plt = filtered_df.plot.bar(rot=0, color=['#4472C4', '#ED7D31', '#A5A5A5'], title='Winter Games').legend(
        edgecolor='None', ncol=3, loc='best')
    if check_print:
        matplot.show()


def question_9(check_print=False):
    if check_print:
        print("--------------- question_9 ---------------")
    df = question_6()
    # convert participation from string to int
    df['summer_participation'] = df['summer_participation'].map(convert_int)

    # make a new column in dataframe with the rule
    df['rate_summer'] = (df['summer_gold'] * 5 + df['summer_silver'] * 3 + df['summer_bronze']) / df[
        'summer_participation']

    # changing the NaN from  the above transformation to 0
    df.loc[df['summer_participation'] == 0, 'rate_summer'] = 0

    # printing the values
    if check_print:
        print(df.sort_values(by='rate_summer', ascending=False).head()['rate_summer'].to_string())
    return df


def question_10(check_print=False):
    if check_print:
        print("--------------- question_10 ---------------")
    df = question_9()

    # convert participation from string to int
    df['winter_participation'] = df['winter_participation'].map(convert_int)

    # make a new column in dataframe with the rule
    df['rate_winter'] = (df['winter_gold'] * 5 + df['winter_silver'] * 3 + df['winter_bronze']) / df[
        'winter_participation']

    # changing the NaN from  the above transformation to 0
    df.loc[df['winter_participation'] == 0, 'rate_winter'] = 0

    continents_df = pd.read_csv('Countries-Continents.csv')

    # merging the datasets
    df_joined = pd.merge(left=df, right=continents_df, on=None, left_on=df.index.str.strip(), right_on='Country',
                         how='left')
    df_joined["Continent"].fillna("Unknown", inplace=True)

    africa_df = df_joined.query('Continent == "Africa"')
    asia_df = df_joined.query('Continent == "Asia"')
    europe_df = df_joined.query('Continent == "Europe"')
    n_america_df = df_joined.query('Continent == "North America"')
    s_america_df = df_joined.query('Continent == "South America"')
    oceania_df = df_joined.query('Continent == "Oceania"')
    unknown_df = df_joined.query('Continent == "Unknown"')

    ax = africa_df.plot.scatter(x='rate_summer', y='rate_winter', color='green', label='Africa')
    ax = asia_df.plot.scatter(x='rate_summer', y='rate_winter', color='orange', label='Asia', ax=ax)
    ax = europe_df.plot.scatter(x='rate_summer', y='rate_winter', color='brown', label='Europe', ax=ax)
    ax = n_america_df.plot.scatter(x='rate_summer', y='rate_winter', color='dodgerblue', label='North America', ax=ax)
    ax = s_america_df.plot.scatter(x='rate_summer', y='rate_winter', color='red', label='South America', ax=ax)
    ax = oceania_df.plot.scatter(x='rate_summer', y='rate_winter', color='yellow', label='Oceania', ax=ax)
    ax = unknown_df.plot.scatter(x='rate_summer', y='rate_winter', color='grey', label='Unknown', ax=ax,
                                 title='Scatter plot of winning countries, Summer Rate vs Winner Rate')
    ax.set_xlabel("Summer Rate")
    ax.set_ylabel("Winter Rate")

    if check_print:
        matplot.show()


if __name__ == "__main__":
    # question_1(True)
    # question_2(True)
    # question_3(True)
    # question_4(True)
    # question_5(True)
    # question_6(True)
    # question_7(True)
    question_8(True)
    # question_9(True)
    # question_10(True)
