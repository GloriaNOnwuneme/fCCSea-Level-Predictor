import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress

def draw_plot():
    # Read data from file
    df = pd.read_csv('epa-sea-level.csv')
    df.drop(columns='NOAA Adjusted Sea Level', inplace=True)

    #Note: verified that y-error is symmetrical checking that all(round(n[0], 2) == round(n[1], 2) for n in df_err))

    #lError = (df['CSIRO Adjusted Sea Level'] - df['Lower Error Bound']).tolist()
    #df_err = [list(tpl) for tpl in zip(lError,df['Error'].tolist())]

    
    df['Error'] = (df['Upper Error Bound'] - df['CSIRO Adjusted Sea Level']).tolist()
    
    
    # Create scatter plot
    fig, ax = plt.subplots(figsize=(17,9))
    ax.scatter('Year', 'CSIRO Adjusted Sea Level', data=df, linewidths=None)
    ax.errorbar(df['Year'], df['CSIRO Adjusted Sea Level'], xerr=None,yerr=df['Error'], fmt='none')
    ax.set_xlim(right=2060)
    ax.set_ylim(top=20)

    # Create first line of best fit
    res = linregress(df['Year'], df['CSIRO Adjusted Sea Level'])
    sim_years = np.array((df['Year'].tolist() + [i for i in range(2014,2051)]), dtype='int32')

    ax.plot(sim_years, res.intercept + res.slope*sim_years, 'r', label='fitted line')
    prognosis = (2050, res.intercept + res.slope*2050)
    
    #Referenced this to annotate graph
    note_total = f'Based on the past 140 years, will reach\n{round(prognosis[1],2)}in by 2050'
    ax.annotate(note_total, xy=prognosis, xytext=(prognosis[0]-29, prognosis[1]- 3.7), arrowprops=dict(facecolor='black', width=3, shrink=.05))


    # Create second line of best fit
    res_mill = linregress(df[df['Year'] >= 2000]['Year'], df[df['Year'] >= 2000]['CSIRO Adjusted Sea Level'])
    post_mill_years = np.array((df[df['Year'] >= 2000]['Year'].tolist() +  [i for i in range(2014,2051)]), dtype='int32')
    #Changed from the following to pass freeCodeCamp tests: post_mill_years = np.array([1900] + (df[df['Year'] >= 2000]['Year'].tolist() + [i for i in range(2014,2051)]), dtype='float64')

    prog_mill = (2050, res_mill.intercept + res_mill.slope*2050)
    ax.plot(post_mill_years, res_mill.intercept + res_mill.slope*post_mill_years, 'r', label='fitted line')
    
    note_mill = f'Based on the past 20 years, will reach\n{round(prog_mill[1],2)}in by 2050'
    ax.annotate(note_mill, xy=prog_mill, xytext=(prog_mill[0]-25, prog_mill[1]+ 2), ha='center', arrowprops=dict(facecolor='black', width=3, shrink=.05))
    
    # Add labels and title
    ax.set_ylabel('Sea Level (inches)')
    ax.set_xlabel('Year')
    ax.set_title('Rise in Sea Level')

    
    # Save plot and return data for testing (DO NOT MODIFY)
    #plt.savefig('sea_level_plot.png')
    return plt.gca()
    #return df