#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  1 19:42:29 2020

@author: tedwoodsides
"""
#imports
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#reading in data from "https://catalog.data.gov/dataset/baby-names-from-social-security-card-applications-national-level-data"
def read_ssn(begin_year,end_year):
    all_years = pd.DataFrame()
    year = list(range(begin_year, end_year+1))
    for y in year:
        file = ("/Users/tedwoodsides/Downloads/names/yob"+str(y)+".txt")
        df = pd.read_csv(file, names=["names","gender","count"])
        #create year column
        df.insert(0, "year", y)
        #combine required data
        all_years = pd.concat([all_years, df], axis = 0)
        male = all_years[all_years.gender == "M"]
        female = all_years[all_years.gender == "F"]
        female_grouped = female.groupby('year')
        male_grouped = male.groupby('year')
        female_count = female_grouped['count'].sum()
        male_count = male_grouped['count'].sum()
    #dictionary
    return{'all_years': all_years,'female_count': female_count,'male_count': male_count}
#2b
def plot_names(*args, sex, begin_year = 1880, end_year = 2018):
    #can use brackets and function to a
    twob = read_ssn(begin_year,end_year)['all_years']
    if sex == 'M':
        twob_total = read_ssn(begin_year, end_year)['male_count']
    elif sex == 'F':
        twob_total = read_ssn(begin_year, end_year)['female_count']    
    twob = twob[twob.gender == sex]
    twob_names = twob[twob['names'].isin(args)]
    twob_1 = pd.merge(twob_names, twob_total, on = 'year', how='inner')
    #calc percentage
    twob_1['percentage'] = (twob_1['count_x'] / twob_1['count_y'])*100
    years = list(range(begin_year,end_year+1))
    twob_1 = twob_1.set_index('year')
    twob_1 = twob_1[['names','percentage']]
    #set axis, ignore warning
    fig, ax = plt.subplots(figsize = (10,8))
    xpos = np.arange(len(years))
    for arg in args:
        #have to use ax functions insted of plt
        temp = twob_1[twob_1['names'] == arg]['percentage']
        ax.bar(x = years,height = temp, width = .4, label = arg,alpha=.4)
        ax.legend()
        ax.set_title('Name Popularity over specified years')
        ax.set_xlabel('Years')
        ax.set_ylabel('Percent of Newborns With Specified Name')  
plot_names("Jack","Eli","Mike","Liam","Alexander",sex="M",begin_year=1770,end_year=2018)








