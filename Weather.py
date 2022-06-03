import tkinter as tk
from tkinter import ttk
import requests
import json
from datetime import datetime
import calendar

'''
    	API                          Method
    Current weather	            /current.json or /current.xml
    Forecast	                /forecast.json or /forecast.xml
    Search or Autocomplete	    /search.json or /search.xml
    History	                    /history.json or /history.xml
    Future	                    /future.json or /future.xml
    Time Zone	                /timezone.json or /timezone.xml
    Sports	                    /sports.json or /sports.xml
    Astronomy	                /astronomy.json or /astronomy.xml
    IP Lookup                   /ip.json or /ip.xml

        PARAMS
    key                         api_key
    q                           query parameter (usually location like a zip code or city name)
    if forecast, then days      # of days forecasted
'''

# fonts
FONTTINY='OCR\ A\ Extended 12'
FONTSMALL='OCR\ A\ Extended 14'
FONT='OCR\ A\ Extended 16'
FONTMED='OCR\ A\ Extended 18'
FONTLARGE='OCR\ A\ Extended 20'

THEMES = {
    'dark' : ('#003045','#00FF45'),
    'light' : ('white','black'),
    'high_c' : ('black','#40EE40')
    }
THEMES_KEYS_LIST = list(THEMES.keys())
THEMES_VALS_LIST = list(THEMES.values())
ACTIVE_THEME = THEMES['dark']
ACTIVE_THEME_ID = THEMES_VALS_LIST.index(ACTIVE_THEME)
BG = ACTIVE_THEME[0]
FG = ACTIVE_THEME[1]

root = tk.Tk()
root.option_add('*Font',FONTLARGE)
root.option_add('*Background', BG)
root.option_add('*Foreground', FG)
root.config(background=BG)
root.title('The Weather')

# General formatting options
options = {
    'padx':10,
    'pady':10,
    'ipadx':5,
    'ipady':5
}
# Label formatting options
label_options = {
    'padx':5,
    'pady':5
}

loc = tk.StringVar()
location_string = tk.StringVar()


base_url = 'http://api.weatherapi.com/v1'
key = '986365a886464cbeaca205542222405'

def frame_day(forecast):
    pass

def swap_theme():
    global ACTIVE_THEME_ID
    print(root['background'])
    print(results_lf.cget('foreground'))
    theme = (root.cget('background'), results_lf.cget('foreground'))
    print(theme)
    pos = THEMES_VALS_LIST.index(theme)

    print("Switching themes ", THEMES_KEYS_LIST[pos], "->", THEMES_KEYS_LIST[pos+1])

    new_theme = THEMES_VALS_LIST[pos+1]
    print("before change, active_theme_id is", str(ACTIVE_THEME_ID))
    ACTIVE_THEME_ID = pos+1
    print("just set active_theme_id to", str(ACTIVE_THEME_ID))
    BG = new_theme[0]
    FG = new_theme[1]

    root.option_add('*Background', BG)
    root.option_add('*Foreground', FG)
    root.config(background=BG)
    results_lf.config(background=BG, foreground=FG)


def convert_time(time_mil):
    ap=''
    if time_mil >= 0 and time_mil <= 11:
        ap = 'a'
        if time_mil == 0:
            h = 12
        else:
            h = time_mil
    elif time_mil >= 12 and time_mil <= 23:
        ap = 'p'
        if time_mil != 12:
            h = time_mil % 12
        else:
            h = time_mil
    return str(h)+ap

def load_weather():
    # kill all previous info in the results lframe
    for k in results_lf.grid_slaves():
        k.destroy()

    # make the api call for current weather conditions
    json_dict = {
        'key' : key,
        'q' : loc.get()
    }
    resp = requests.get(
        base_url+'/current.json',
        params=json_dict,
        verify=False
    )
    try:
        response = resp.json()
    except:
        print('loading didnt work, trying again forever. Hope it works soon.')
        load_weather()

    # separate response into two smaller json dicts
    location = response['location']
    current = response['current']

    print('LOCATION: '+json.dumps(location, indent=4))
    print('CURRENT: '+json.dumps(current, indent=4))
    json_dict.update({'days':3})
    forecast_resp = requests.get(base_url+'/forecast.json', params=json_dict, verify=False)
    forecast_response = forecast_resp.json()['forecast']['forecastday']

    current_datetime = datetime.strptime(location['localtime'], '%Y-%m-%d %H:%M')
    h1_mil = int(datetime.strftime(current_datetime, '%H'))
    h2_mil = (h1_mil + 1) % 24
    h3_mil = (h1_mil + 2) % 24


    print(json.dumps(forecast_response[0]['hour'][h1_mil], indent=4))

    fc1 = forecast_response[0]['hour'][h1_mil]
    fc2 = forecast_response[0]['hour'][h2_mil]
    fc3 = forecast_response[0]['hour'][h3_mil]

    hour1 = [convert_time(h1_mil), fc1['temp_f'], fc1['feelslike_f'], fc1['condition']['text'],
        fc1['wind_mph'], fc1['wind_dir'], fc1['will_it_rain'], fc1['chance_of_rain']]
    hour2 = [convert_time(h2_mil), fc2['temp_f'], fc2['feelslike_f'], fc2['condition']['text'],
        fc2['wind_mph'], fc2['wind_dir'], fc2['will_it_rain'], fc2['chance_of_rain']]
    hour3 = [convert_time(h3_mil), fc3['temp_f'], fc3['feelslike_f'], fc3['condition']['text'],
        fc3['wind_mph'], fc3['wind_dir'], fc3['will_it_rain'], fc3['chance_of_rain']]

    print(str(hour1)+'\n'+str(hour2)+'\n'+str(hour3))

    fd1 = forecast_response[0]['day']
    fd2 = forecast_response[1]['day']
    fd3 = forecast_response[2]['day']

    day1 = [forecast_response[0]['date'], fd1['maxtemp_f'], fd1['avgtemp_f'], fd1['mintemp_f'], fd1['condition']['text'], fd1['daily_chance_of_rain']]
    day2 = [forecast_response[1]['date'], fd2['maxtemp_f'], fd2['avgtemp_f'], fd2['mintemp_f'], fd2['condition']['text'], fd2['daily_chance_of_rain']]
    day3 = [forecast_response[2]['date'], fd3['maxtemp_f'], fd3['avgtemp_f'], fd3['mintemp_f'], fd3['condition']['text'], fd3['daily_chance_of_rain']]
    print(day1)
    print(day2)
    print(day3)

    # shorten usa if necessary and set location string
    if location['country'] not in [
        'United States of America','USA United States of America']:
        location_country = location['country']
    else:
        location_country = 'USA'

    location_string.set(
        '<'+location['name']+', '+location['region']+', '+location_country+'>')

    # set title of results lframe to the location searched
    results_lf.config(text=location_string.get())

    # framing conditions for the border.
    conditions_frame = tk.Frame(results_lf, relief='sunken', border=True)
    conditions_frame.columnconfigure(index=0, weight=2)
    conditions_frame.rowconfigure(index=0, weight=3)
    conditions_frame.grid(
        row=0, column=0,
        rowspan=3, columnspan=2,
        sticky='new', padx=5, pady=5, ipadx=30)

    conditions_label = tk.Label(conditions_frame,
        text=str(current['condition']['text']),
        font=FONTLARGE,
        wraplength=180)
    conditions_label.grid(
        row=0,column=0,
        columnspan=3,
        sticky='we')

    # night label
    daynight = tk.StringVar()
    if current['is_day'] == 0:
        daynight.set('night')
    if current['is_day'] == 1:
        daynight.set('day')
    daynight_label = tk.Label(conditions_frame,
        text=daynight.get(),
        justify='right',
        font=FONTTINY)

    daynight_label.grid(
        row=1, column=0,
        sticky='we')

    # temp label
    temp_label = tk.Label(conditions_frame,
        text=str(current['temp_f'])+' F',
        font=FONTLARGE)
    temp_label.grid(
        row=2, column=0,
        sticky='we')

    # feels like temp
    feelslike_label = tk.Label(conditions_frame,
        text='feels like '+str(current['feelslike_f']),
        font=FONTTINY)
    feelslike_label.grid(
        row=3, column=0,
        sticky='we')

    # framing wind results for multiline
    wind_frame = tk.Frame(results_lf, relief='sunken', border=True)
    wind_frame.columnconfigure((0,1), weight=1)
    wind_frame.grid(
        row=0, column=2,
        rowspan=1, columnspan=2,
        sticky='nwe', padx=5, pady=5)

    # wind
    wind_labelname = tk.Label(wind_frame,
        text='wind',
        font=FONTSMALL)
    wind_labelname.grid(
        row=0, column=0,
        rowspan=2,
        sticky='w', padx=10)

    wind_label = tk.Label(wind_frame,
        text=str(current['wind_mph'])+' mph '+current['wind_dir'],
        justify='right',
        font=FONTLARGE)
    wind_label.grid(
        row=0, column=1,
        sticky='e')

    gusts_label = tk.Label(wind_frame, text='gusts up to '+str(current['gust_mph']), justify='right', font=FONTTINY)
    gusts_label.grid(row=1, column=1, sticky='e')

    # framing humidity results for multiline
    humid_frame = tk.Frame(results_lf, relief='sunken', border=True)
    humid_frame.columnconfigure((0,1), weight=1)
    #humid_frame.rowconfigure(0,weight=2)
    humid_frame.grid(
        row=1, column=2,
        columnspan=2,
        sticky='nwe', padx=5, pady=5)

    # humidity
    humid_labelname = tk.Label(humid_frame,
        text='humidity',
        font=FONTSMALL)
    humid_labelname.grid(
        row=0, column=0,
        sticky='w', padx=10)

    humid_label = tk.Label(humid_frame,
        text=str(current['humidity'])+' %',
        justify='right',
        font=FONTLARGE)
    humid_label.grid(
        row=0, column=2,
        sticky='e')

    cloud_frame = tk.Frame(results_lf, relief='sunken', border=True)
    cloud_frame.columnconfigure((0,1), weight=1)
    cloud_frame.grid(
        row=2, column=2,
        columnspan=2,
        sticky='nwe', padx=5, pady=5)

    cloud_labelname = tk.Label(cloud_frame,
        text='cloud cover',
        font=FONTSMALL)
    cloud_labelname.grid(
        row=0, column=0,
        sticky='w', padx=10)

    cloud_label = tk.Label(cloud_frame,
        text=str(current['cloud'])+' %',
        justify='right',
        font=FONTLARGE)
    cloud_label.grid(row=0,column=1, sticky='e')

    # misc frame grid
    misc_frame = tk.Frame()

    # # FORECAST HOUR FRAMES
    hour_forecast_frame = tk.LabelFrame(results_lf,
        text='<later today>',
        labelanchor='nw',
        border=False,
        font=FONTMED)
    hour_forecast_frame.grid(
        row=5, column=0,
        rowspan=2, columnspan=4,
        sticky='ew', pady=10, ipadx=10)

    hour1_frame = tk.Frame(hour_forecast_frame,
        relief='ridge',
        border=True)
    hour1_frame.pack(side='left', padx=5, expand=True, fill='both')

    # hour1 time
    hour1_time_label = tk.Label(hour1_frame,
        text=hour1[0],
        font=FONTLARGE)
    hour1_time_label.pack(
        anchor='n',
        expand=True,
        fill='x')

    # hour1 hi
    hour1_hi_label = tk.Label(hour1_frame,
        text=str(hour1[1])+' F',
        font=FONTMED)
    hour1_hi_label.pack(
        anchor='n',
        expand=True,
        fill='x')

    # hour1 condition`
    hour1_condition_label = tk.Label(hour1_frame,
        text=hour1[3],
        font=FONTTINY,
        wraplength=95)
    hour1_condition_label.pack(
        anchor='s',
        expand=True,
        fill='both')

    # hour2 frame
    hour2_frame = tk.Frame(hour_forecast_frame,
        relief='sunken',
        border=True)
    hour2_frame.pack(side='left', padx=5, expand=True, fill='both')

    # hour2 time
    hour2_time_label = tk.Label(hour2_frame,
        text=hour2[0],
        font=FONTLARGE)
    hour2_time_label.pack(
        anchor='n',
        expand=True,
        fill='x')

    # hour2 hi
    hour2_hi_label = tk.Label(hour2_frame,
        text=str(hour2[1])+' F',
        font=FONTMED)
    hour2_hi_label.pack(
        anchor='n',
        expand=True,
        fill='x')

    # hour2 condition
    hour2_condition_label = tk.Label(hour2_frame,
        text=hour2[3],
        font=FONTTINY,
        wraplength=100)
    hour2_condition_label.pack(anchor='s', expand=True, fill='both')

    # hour3 frame
    hour3_frame = tk.Frame(hour_forecast_frame,
        relief='sunken',
        border=True)
    hour3_frame.pack(side='left', padx=5, expand=True, fill='both')

    hour3_time_label = tk.Label(hour3_frame,
        text=hour3[0],
        font=FONTLARGE)
    hour3_time_label.pack(anchor='n')

    hour3_hi_label = tk.Label(hour3_frame,
        text=hour3[1],
        font=FONTMED)
    hour3_hi_label.pack(
        anchor='center',
        expand=True,
        fill='both')

    hour3_condition_label = tk.Label(hour3_frame,
        text=hour3[3],
        font=FONTTINY,
        wraplength=100)
    hour3_condition_label.pack(anchor='center')


    # FORECAST DAY FRAME
    day_forecast_frame = tk.LabelFrame(results_lf,
        text='<look ahead>',
        border=False,
        labelanchor='nw',
        font=FONTMED)
    day_forecast_frame.grid(
        row=8, column=0,
        rowspan=1, columnspan=4,
        sticky='nwe')

    # framing day 1 forecast results
    day1_frame = tk.Frame(day_forecast_frame, relief='sunken', border=True)
    day1_frame.option_add('*Font', FONTSMALL)
    day1_frame.pack(side='left', padx=5, expand=True, fill='both')

    # framing day 2 forecast results
    day2_frame = tk.Frame(day_forecast_frame, relief='sunken', border=True)
    day2_frame.rowconfigure(index=2, weight=2)
    day2_frame.pack(side='left', padx=5, expand=True, fill='both')

    # framing day 3 forecast results
    day3_frame = tk.Frame(day_forecast_frame, relief='sunken', border=True)
    day3_frame.rowconfigure(index=2, weight=2)
    day3_frame.pack(side='left', padx=5, expand=True, fill='both')

    # day 1
    day1_date_labelname = tk.Label(day1_frame, text='Today', font=FONT)
    day1_date_labelname.pack()

    day1_conditions = tk.Label(day1_frame, text=day1[4], wraplength=100)
    day1_conditions.pack(expand=True)

    day1_maxtemp = tk.Label(day1_frame, text='Hi '+str(day1[1])+' F')
    day1_maxtemp.pack()

    day1_mintemp = tk.Label(day1_frame, text='Lo '+str(day1[3])+' F')
    day1_mintemp.pack()

    day1_chance_rain = tk.Label(day1_frame, text='rain '+str(day1[5])+' %')
    day1_chance_rain.pack()

    # day 2
    day2_date_labelname = tk.Label(day2_frame, text='Tomorrow', font=FONT, justify='center')
    day2_date_labelname.pack(anchor='n')

    day2_conditions = tk.Label(day2_frame, text=day2[4], wraplength=100)
    day2_conditions.pack(expand=True)

    day2_maxtemp = tk.Label(day2_frame, text=str(day2[1])+' F')
    day2_maxtemp.pack()

    day2_mintemp = tk.Label(day2_frame, text=str(day2[3])+' F')
    day2_mintemp.pack()

    day2_chance_rain = tk.Label(day2_frame, text=str(day2[5])+' %')
    day2_chance_rain.pack()

    # day 3
    day_of_week = calendar.day_name[datetime.strptime(
        day3[0], '%Y-%m-%d').weekday()]
    day3_date_labelname = tk.Label(day3_frame, text=day_of_week, font=FONT)
    day3_date_labelname.pack()

    day3_conditions = tk.Label(day3_frame, text=day3[4], wraplength=100)
    day3_conditions.pack(expand=True)

    day3_maxtemp = tk.Label(day3_frame, text=str(day3[1])+' F')
    day3_maxtemp.pack()

    day3_mintemp = tk.Label(day3_frame, text=str(day3[3])+' F')
    day3_mintemp.pack()

    day3_chance_rain = tk.Label(day3_frame, text=str(day3[5])+' %')
    day3_chance_rain.pack()

    # local time
    time_frame = tk.Frame(results_lf, relief='sunken', border=True)
    time_frame.columnconfigure(index=0, weight=2)
    time_frame.grid(row=20, column=0, rowspan=2, columnspan=4, sticky='sew', padx=5, pady=5)

    time_labelname = tk.Label(time_frame, text='Local Time', font=FONTSMALL)
    time_labelname.grid(row=0, column=0, rowspan=2, sticky='w')

    time_label = tk.Label(time_frame, text=str(location['localtime']),justify='right', font=FONT)
    time_label.grid(row=0, column=2, sticky='e')



# setup of main window elements

# results frame for viewing weather results
results_lf = tk.LabelFrame(root,
    width=500, height=600,
    relief='flat',
    labelanchor='nw',
    font=FONTMED)
results_lf.grid(row=0, column=0, padx=15, pady=15)
results_lf.columnconfigure(0, weight=2)
results_lf.rowconfigure((5,6,7,8,9,10), weight=1)

# without this mysterious next line, the height and width of the results labelframe doesnt actually do anything?
results_lf.grid_propagate(0)

# city search bar
loc.set('')
loc_entry = tk.Entry(root, borderwidth=1, textvariable=loc, justify='center')
loc_entry.grid(row=1, column=0,  **options)
loc_entry.focus()

# search button
search_button = tk.Button(
                        root,
                        borderwidth=0,
                        bg='grey',
                        fg='black',
                        font=FONT,
                        text='Go!',
                        command=load_weather)

search_button.grid(row=2, column=0, **options)
root.bind('<Return>', lambda event=None: search_button.invoke())


# first time info display
info_label = tk.Label(
    results_lf,
    font=FONTLARGE,
    text='Search a city or zip code to see the local weather forecast.',
    wraplength=250,
    justify='center'
).grid(row=0, column=0, sticky='nswe', pady=50)


#theme_button = tk.Button(root, text='Dark/Light', fg='black', command=swap_theme).grid(row=4, column=0, sticky='sw')

# Initiate program
root.mainloop()
