import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Connect to your SQLite database
DB_FILE = "D:\\Documentos\\Coding\\Python\\wca_data.db"
conn = sqlite3.connect(DB_FILE)
conn.execute("PRAGMA journal_mode = WAL;")
cursor = conn.cursor()

image_name_suffix = 'histogram_of_average_times_in_competition_number_'

country = 'Spain'
comparison_country_sql = '='
competition_number = 5

competition_number_equal_or_greater_than = True

if competition_number_equal_or_greater_than:
    image_name_suffix += '_greater_equal_'


def plot_competition_number(competition_number):
    country_filter = ''
    if country:
        country_filter = f'and person_countryId {comparison_country_sql} "{country}"'
    if competition_number_equal_or_greater_than:
        sql_comparison = '>='
    else:
        sql_comparison = '='
    query_old = f"""
    select
        res.average
    from
    (
        SELECT
            T1.personId
            , printf('%04d-%02d-%02d', T2.year, T2.month, T2.day) AS competition_date
            , min(average) as average
        FROM
            results AS T1
        JOIN
            competitions AS T2 ON T1.competitionId = T2.id
        where
            T1.eventId = '333'
            and T1.average > 0
        group by
            personId
            , competition_date
    ) res
    JOIN
    (
        WITH RankedCompetitions AS (
            SELECT
                T1.personId,
                T1.competitionId,
                printf('%04d-%02d-%02d', T2.year, T2.month, T2.day) AS competition_date,
                -- This assigns a sequential rank (1, 2, 3...) to each competition
                -- for *each* unique person, ordered chronologically.
                ROW_NUMBER() OVER (
                    PARTITION BY T1.personId
                    ORDER BY T2.year ASC, T2.month ASC, T2.day ASC
                ) as competition_rank
            FROM
                results AS T1
            JOIN
                competitions AS T2 ON T1.competitionId = T2.id
            -- Optimization: Use DISTINCT ON (personId, competitionId) if results table
            -- has multiple rows per person/competition, but WCA data often needs
            -- the competitionId/personId combination to be treated as one instance.
            -- Assuming a person's result is recorded multiple times for one competition
            -- due to different events, we need to ensure we count the competition only once.
            -- A simpler way is to work off a distinct list of personId and competitionId:
            GROUP BY
                T1.personId, T1.competitionId, T2.year, T2.month, T2.day
        )

        -- Select the required information where the rank is 10
        SELECT
            personId,
            competition_date
        FROM
            RankedCompetitions t1
        WHERE
            competition_rank {sql_comparison} {competition_number}
            {country_filter}
        ORDER BY
            personId ASC
    ) analysis_date
    on
        res.personId = analysis_date.personId
        and res.competition_date = analysis_date.competition_date
    """
    query = f"""
    select
        average
    from
    (

        select
            personId
            , min(average) as average
        from
            results_extended_with_rank
        where
            person_competition_number {sql_comparison} {competition_number}
            and eventId = '333'
            {country_filter}
            and average > 0
        group by
            personId
    )
    """
    print(query)

    cursor.execute(query)
    df = pd.read_sql_query(query, conn)
    df['average_seconds'] = df['average'] / 100.0

    ### PLOT
    print(f"Found {len(df)} rows")
    print("Stats (in seconds):")
    print(df['average_seconds'].describe())

    plt.figure(figsize=(12, 6))

    max_time = df['average_seconds'].mean() * 2

    df[df['average_seconds'] <= max_time]['average_seconds'].hist(bins=100, edgecolor='black', alpha=0.7)

    plt.title(f'Average Times at competition number {sql_comparison} {competition_number} on 3x3x3')
    plt.xlabel('Average Time (Seconds)')
    plt.ylabel('Frecuency (Number of competitiors)')
    plt.gca().ticklabel_format(style='plain', axis='y')
    plt.grid(axis='y', alpha=0.5)
    mean_value = df['average_seconds'].mean()
    plt.axvline(mean_value, color='red', linestyle='dashed', linewidth=1)
    under_10_seconds = len(df[df['average_seconds'] <= 10])
    total_competitors = len(df)
    # obtain mode value as the bin mode, not the values mode
    counts, bin_edges = np.histogram(df['average_seconds'], bins=100)
    max_count_index = np.argmax(counts)
    mode_value = (bin_edges[max_count_index] + bin_edges[max_count_index + 1]) / 2
    # mode_value = df['average_seconds'].mode()[0]
    plt.axvline(mode_value, color='green', linestyle='dashed', linewidth=1)
    plt.legend(
        [
            'Mean: {:.2f} seconds'.format(mean_value),
            'Mode: {:.2f} seconds'.format(mode_value),
            'Under 10 seconds: {} ({:.2f}%)'.format(under_10_seconds, (under_10_seconds / total_competitors) * 100),
        ]
    )
    plt.savefig(f'D:\\Documentos\\Coding\\Python\\cube\\wca_statistics\\results\{image_name_suffix}{competition_number}.png')
    plt.show()

# for i in range(2, 40):
#     plot_competition_number(i)
# for i in range(1, 2):
#     plot_competition_number(i)
plot_competition_number(competition_number)
