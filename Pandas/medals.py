#! /usr/bin/env python3.13
'''
This is a Pandas proof-of-concept Bite. We just added the library to our
platform!

For this Bite you find out the male and female athletes who won most medals in
all the Summer Olympic Games (csv = 1896-2012, but we also test a smaller subset
of the data).
'''


from __future__ import annotations
import pandas as pd


# Data location:
data = 'https://bites-data.s3.us-east-2.amazonaws.com/summer.csv'


def athletes_most_medals(data: str=data) -> pd.Series[str]:
    df = pd.read_csv(data, na_filter=False)
    man = df.loc[df['Gender'] == 'Men', 'Athlete'].value_counts().head(1)
    woman = df.loc[df['Gender'] == 'Women', 'Athlete'].value_counts().head(1)

    return pd.concat([man, woman])


if __name__ == '__main__':
    print(athletes_most_medals())
