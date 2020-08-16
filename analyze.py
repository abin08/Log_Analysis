import argparse
import pandas as pd


def read_logs(log_file):
    """Reads the log file and returns a pandas dataframe.
    Fields are seperated using regular expression which matches
    space that are not inside double quotes or inside [].
    """    
    fields = ["host", "rfc_id", "user_id", "time", "request", 
        "status", "content_size"]

    print("Reading logs...")

    data_frame = pd.read_csv(
        log_file,
        sep=r'\s(?=(?:[^"]*"[^"]*")*[^"]*$)(?![^\[]*\])',
        engine='python',
        # set '-' as NaN value
        na_values='-',
        header=None,
        names=fields,
        # skip lines which cause error while reading
        error_bad_lines=False,
        # suppress the error message
        warn_bad_lines=False
    )
    return data_frame


def parse_request(req):
    """Extracts and returns request url from the request field.
    Returns request as it is if IndexError occurs.
    """
    try:
        return req.split()[1]
    except IndexError:
        return req


def clean(df):
    """Used for pre-processing of the dataframe before doing
    the analysis. Returns cleaned pandas dataframe.
    """
    print("Processing the logs...")
    # drop columns since it has NaN in all rows
    df.drop(columns=['rfc_id', 'user_id'], inplace=True)

    # Impute the NaN values of the field content_size using 0
    df['content_size'].fillna(0, inplace=True)

    # drop any remaining rows having NaN values
    df.dropna(axis=0, inplace=True)

    # convert type of the field status to int
    df = df.astype({'status': int})

    # extract request url from the field request
    df['request'] = df.request.apply(parse_request)
    return df


def top10_requests(df):
    """ Returns pandas dataframe with top 10 requested pages
    and the number of requests made for each.
    """
    return df.groupby('request')['status'].count() \
            .reset_index(name='count') \
            .sort_values('count', ascending=False) \
            .head(10) \
            .reset_index(drop=True)


def success_req_percentage(df):
    """Returns percentage of successful requests as float value
    (anything in the 200s and 300s range)
    """
    percentage = df[df.status.between(200, 399)]['status'].count()*100 / df['status'].count()
    return round(percentage, 2)


def unsuccessful_requests(df):
    """Returns dataframe only with unsuccessful requests
    """
    return df[df.status >= 400]


def unsuccess_req_percentage(df):
    """Returns percentage of unsuccessful requests as float value
    (anything that is not in the 200s or 300s range)
    """
    unsuccess_df = unsuccessful_requests(df)
    percentage = unsuccess_df['status'].count()*100 / df['status'].count()
    return round(percentage, 2)


def top10_unsuccess_requests(df):
    """Returns pandas dataframe with top 10 unsuccessfull requests
    and its count.
    """
    unsucc_df = unsuccessful_requests(df)
    return unsucc_df.groupby('request')['status'] \
            .count() \
            .reset_index(name='count') \
            .sort_values('count', ascending=False) \
            .head(10) \
            .reset_index(drop=True)


def top10_hosts(df):
    """Returns pandas dataframe containing top 10 hosts making the
    most requests, with number of requests made.
    """
    return df.groupby('host')['status'] \
            .count() \
            .reset_index(name='count') \
            .sort_values('count', ascending=False) \
            .head(10) \
            .reset_index(drop=True)


def top5_reqs_of_top_hosts(df):
    """For each of the top 10 hosts, finds the top 5 pages requested
    and the number of requests for each. Returns pandas dataframe.
    """
    top_ten_hosts = top10_hosts(df)
    # join top_ten_hosts dataframe with actual df to get requests in top_hosts
    top_hosts_reqs = pd.merge(top_ten_hosts, df, on='host')

    # group the field 'request' by 'host' and get counts
    top_hosts_reqs_grp = top_hosts_reqs['request'] \
                            .groupby(top_hosts_reqs['host']) \
                            .value_counts()
    
    groupby_result = top_hosts_reqs_grp.groupby(level=[0]) \
                        .nlargest(5) \
                        .reset_index(level=0, drop=True)
    return pd.DataFrame(groupby_result)


def display_top10_reqs(df):
    top10_reqs = top10_requests(df)
    print("\nTop 10 requested pages")
    print(top10_reqs)


def display_success_reqs(df):
    succ_reqs = success_req_percentage(df)
    print(f"\nSuccessful requests: {succ_reqs} %")


def display_unsuccess_reqs(df):
    unsucc_reqs = unsuccess_req_percentage(df)
    print(f"\nUnsuccessful requests: {unsucc_reqs} %")


def display_top10_unsuccess_reqs(df):
    top10_unsucc_reqs = top10_unsuccess_requests(df)
    print("\nTop 10 unsuccessful requests")
    print(top10_unsucc_reqs)


def display_top10_hosts(df):
    top_ten_hosts = top10_hosts(df)
    print("\nTop 10 hosts")
    print(top_ten_hosts)


def display_topreqs_of_top_hosts(df):
    top_hosts_reqs = top5_reqs_of_top_hosts(df)
    print("\nTop 5 requests of top 10 hosts")
    print(top_hosts_reqs)


if __name__ == "__main__":

    arg_p = argparse.ArgumentParser()
    arg_p.add_argument("-o", "--option", required=False,
        help="Option (1 to 6) to tell which usecase has to be displayed")
    option = vars(arg_p.parse_args())['option']

    if option and (int(option)<1 or int(option)>6):
        print("Invalid option..!")

    else:
        log_file = 'access_log_Aug95'
        df = read_logs(log_file)
        cleaned_df = clean(df)
            
        if option == '1':
            display_top10_reqs(cleaned_df)

        elif option == '2':
            display_success_reqs(cleaned_df)

        elif option == '3':
            display_unsuccess_reqs(cleaned_df)

        elif option == '4':
            display_top10_unsuccess_reqs(cleaned_df)

        elif option == '5':
            display_top10_hosts(cleaned_df)

        elif option == '6':
            display_topreqs_of_top_hosts(cleaned_df)
        
        else:
            # display all usecases
            display_top10_reqs(cleaned_df)
            display_success_reqs(cleaned_df)
            display_unsuccess_reqs(cleaned_df)
            display_top10_unsuccess_reqs(cleaned_df)
            display_top10_hosts(cleaned_df)
            display_topreqs_of_top_hosts(cleaned_df)