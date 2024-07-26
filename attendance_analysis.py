import requests
import json

def check_weather(condition, max_temp):
    if condition=='thunderstrom' or condition=='hail' or condition=='hurricane' or condition=='blizzard' or max_temp > 40 :
        return False
    
    return True

def num_to_str(num):
    if num<10:
        return "0"+str(num)
    else:
        return str(num)


def add_day_to_date(the_date):
    date_arr = the_date.split('-')
    
    if (date_arr[1]=='01' or date_arr[1]=='03' or date_arr[1]=='05' or date_arr[1]=='07' or date_arr[1]=='08' or date_arr[1]=='10' or date_arr[1]=='12') and date_arr[2]=='31':
        if date_arr[1]!='12':
            return date_arr[0]+"-"+num_to_str(int(date_arr[1])+1)+'-01' 
        else:
            return num_to_str(int(date_arr[0])+1)+'-01'+'-01'
  
    if (date_arr[1]=='04' or date_arr[1]=='06' or date_arr[1]=='09' or date_arr[1]=='11') and date_arr[2]=='30':
        return date_arr[0]+"-"+num_to_str(int(date_arr[1])+1)+'-01' 

    if (date_arr[1]=='02' and date_arr[2]=='29') or (date_arr[1]=='02' and date_arr[2]=='28' and int(date_arr[0])%4>0):
        return date_arr[0]+'-03'+'-01'
    
    if date_arr[1]=='02' and date_arr[2]=='28' and int(date_arr[0])%4==0:
        return date_arr[0]+'-02'+'-29'

    return date_arr[0]+"-"+date_arr[1]+"-"+num_to_str(int(date_arr[2])+1)


def minus_day_from_date(the_date):
    date_arr = the_date.split('-')
    
    if (date_arr[1]=='01' or date_arr[1]=='02' or date_arr[1]=='04' or date_arr[1]=='06' or date_arr[1]=='08' or date_arr[1]=='09' or date_arr[1]=='11') and date_arr[2]=='01':
        if date_arr[1]!='01':
            return date_arr[0]+"-"+num_to_str(int(date_arr[1])-1)+'-31' 
        else:
            return num_to_str(int(date_arr[0])-1)+'-12'+'-31'
  
    if (date_arr[1]=='05' or date_arr[1]=='07' or date_arr[1]=='10' or date_arr[1]=='12') and date_arr[2]=='01':
        return date_arr[0]+"-"+num_to_str(int(date_arr[1])-1)+'-30' 

    if date_arr[1]=='03' and date_arr[2]=='01' and int(date_arr[0])%4>0:
        return date_arr[0]+'-02'+'-28'
    
    if date_arr[1]=='03' and date_arr[2]=='01' and int(date_arr[0])%4==0:
        return date_arr[0]+'-02'+'-29'

    return date_arr[0]+"-"+date_arr[1]+"-"+num_to_str(int(date_arr[2])-1)

def binary_search_weather(weather, event_date, country, weather_dict, weather_T):
    key_T=country+event_date
    if key_T in weather_T :
        return weather_T[key_T]

    day_before_event_date=minus_day_from_date(event_date)
    day_after_event_date=add_day_to_date(event_date)
    day_before_event_arr=day_before_event_date.split('-')
    day_after_event_arr=day_after_event_date.split('-')

    event_date_arr = event_date.split('-')
    weather_len=weather_dict[country][1]
    good_weather = [True, True, True]
    high = weather_dict[country][1]-1
    low = weather_dict[country][0]
    mid = 0
    
    while low <= high:
        mid = (high + low) // 2
        mid_date_arr = weather[mid]['date'].split('-')
       
        if mid_date_arr[0]<day_before_event_arr[0]  or (mid_date_arr[0]==day_before_event_arr[0] and mid_date_arr[1]<day_before_event_arr[1]) or (mid_date_arr[0]==day_before_event_arr[0] and mid_date_arr[1]==day_before_event_arr[1] and mid_date_arr[2]<day_before_event_arr[2]) :
            low = mid + 1
        elif mid_date_arr[0]>day_after_event_arr[0] or (mid_date_arr[0]==day_after_event_arr[0] and mid_date_arr[1]>day_after_event_arr[1]) or (mid_date_arr[0]==day_after_event_arr[0] and mid_date_arr[1]==day_after_event_arr[1] and mid_date_arr[2]>day_after_event_arr[2]) :
            high = mid - 1
        else:
            if weather[mid]['date']==day_before_event_date :
                good_weather[0]=check_weather(weather[mid]['condition'], weather[mid]['max_temp']) 
                
                if mid+1 < weather_len :
                    if weather[mid+1]['date']==event_date :
                        good_weather[1]=check_weather(weather[mid+1]['condition'], weather[mid+1]['max_temp'])

                        if mid+2 < weather_len :
                            if weather[mid+2]['date']==day_after_event_date :
                                good_weather[2]=check_weather(weather[mid+2]['condition'], weather[mid+2]['max_temp'])
                    
                    elif weather[mid+1]['date']==day_after_event_date :
                        good_weather[2]=check_weather(weather[mid+1]['condition'], weather[mid+1]['max_temp'])               
                    
            elif weather[mid]['date']==event_date :
                good_weather[1]=check_weather(weather[mid]['condition'], weather[mid]['max_temp'])  
                
                if mid+1 < weather_len :
                    if weather[mid+1]['date']==day_after_event_date :
                        good_weather[2]=check_weather(weather[mid+1]['condition'], weather[mid+1]['max_temp'])

                if mid > 0 :
                    mid_date_arr2 = weather[mid-1]['date'].split('-')    
                    if mid_date_arr2[0]==event_date_arr[0] and mid_date_arr2[1]==event_date_arr[1] and int(mid_date_arr2[2])==int(event_date_arr[2])-1:
                        good_weather[0]=check_weather(weather[mid-1]['condition'], weather[mid-1]['max_temp'])
                
            elif  weather[mid]['date']==day_after_event_date :
                if weather[mid]['condition']=='thunderstrom' or weather[mid]['condition']=='hail' or weather[mid]['condition']=='hurricane' or weather[mid]['condition']=='blizzard' or weather[mid]['max_temp'] > 40 :
                    good_weather[2]=False  
                
                if mid > 0 :
                    if weather[mid-1]['date']==event_date :
                        good_weather[1]=check_weather(weather[mid-1]['condition'], weather[mid-1]['max_temp'])

                        if mid > 1 :
                            if weather[mid-2]['date']==day_before_event_date :
                                good_weather[0]=check_weather(weather[mid-2]['condition'], weather[mid-2]['max_temp'])

                    elif weather[mid-1]['date']==day_before_event_date :
                        good_weather[0]=check_weather(weather[mid-1]['condition'], weather[mid-1]['max_temp'])

            weather_T[country+event_date]=good_weather
            return good_weather

    return good_weather


def check_clock(clock_in, clock_out):
    if clock_in[0] < '08' and clock_out[0] >= '04' :
        return False
    elif clock_in[0]=='08' and clock_in[1]<'16' and clock_out[0] >= '04' :
        return False
    
    return True



url = "https://www.pingtt.com/exam/weather"
response = requests.get(url)

if response.status_code == 200:
    weather = response.json()
else:
    print(f"Error: {response.status_code}")

url = "https://www.pingtt.com/exam/events"
response = requests.get(url)

if response.status_code == 200:
    events = response.json()
else:
    print(f"Error: {response.status_code}")

with open('employees.json') as emp_file :
    employees = json.load(emp_file)

with open('attendance.json') as attend_file :
    attendance = json.load(attend_file)

prev=events[0]['country']
events_dict={}
events_dict[prev]=0
for event in events :
    curr = event['country']
    if prev!= curr :
        events_dict[curr]=event['id']-1
    prev=curr

prev=attendance[0]['employee_record_id']
attendance_dict={}
attendance_dict[prev]=[0,0]
for rec in attendance :
    curr = rec['employee_record_id']
    if prev != curr :
        attendance_dict[prev]=[attendance_dict[prev][0], rec['record_id']-1]
        attendance_dict[curr]=[rec['record_id']-1, 0]
    prev=curr
attendance_dict[prev]=[attendance_dict[prev][0], len(attendance)]

prev=weather[0]['country']
weather_dict={}
weather_dict[prev]=[0,0]
for w in weather :
    curr = w['country']
    if prev != curr :
        weather_dict[prev]=[weather_dict[prev][0] ,w['id']-1]
        weather_dict[curr]=[w['id']-1, 0]
    prev=curr
weather_dict[prev]=[weather_dict[prev][0], len(weather)]


months=[31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
year=[2022,2022,2022,2022]
day_of_the_week={}
mondays=3
fridays=7
saturdays=8
sundays=9
m=[0,0,0,0]
#day before firat day in month is 31 not 0
day_of_the_week["2022-01-03"]="monday"
day_of_the_week["2022-01-07"]="friday"
day_of_the_week["2022-01-08"]="saturday"
day_of_the_week["2022-01-09"]="sunday"
while(year[3]<2025):
    mondays=mondays+7
    fridays=fridays+7
    saturdays=saturdays+7
    sundays=sundays+7

    if year[0]%4==0:
        months[1]=29

    if mondays>months[m[0]]:
        mondays=mondays-months[m[0]]
        m[0]=m[0]+1
        if m[0]>11:
            year[0]=year[0]+1
            m[0]=0
        the_date=str(year[0])+"-"+num_to_str(m[0]+1)+"-"+num_to_str(mondays)
        day_of_the_week[the_date]="monday"
    else:
        the_date=str(year[0])+"-"+num_to_str(m[0]+1)+"-"+num_to_str(mondays)
        day_of_the_week[the_date]="monday"    
    
    months[1]=28
    if year[1]%4==0:
        months[1]=29

    if fridays>months[m[1]]:
        fridays=fridays-months[m[1]]
        m[1]=m[1]+1
        if m[1]>11:
            year[1]=year[1]+1
            m[1]=0
        the_date=str(year[1])+"-"+num_to_str(m[1]+1)+"-"+num_to_str(fridays)
        day_of_the_week[the_date]="friday"
    else:
        the_date=str(year[1])+"-"+num_to_str(m[1]+1)+"-"+num_to_str(fridays)
        day_of_the_week[the_date]="friday"

    months[1]=28
    if year[2]%4==0:
        months[1]=29
    if saturdays>months[m[2]]:
        saturdays=saturdays-months[m[2]]
        m[2]=m[2]+1
        if m[2]>11:
            year[2]=year[2]+1
            m[2]=0
        the_date=str(year[2])+"-"+num_to_str(m[2]+1)+"-"+num_to_str(saturdays)
        day_of_the_week[the_date]="saturday"
    else:
        the_date=str(year[2])+"-"+num_to_str(m[2]+1)+"-"+num_to_str(saturdays)
        day_of_the_week[the_date]="saturday"

    months[1]=28
    if year[3]%4==0:
        months[1]=29
    if sundays>months[m[3]]:
        sundays=sundays-months[m[3]]
        m[3]=m[3]+1
        if m[3]>11:
            year[3]=year[3]+1
            m[3]=0
        the_date=str(year[3])+"-"+num_to_str(m[3]+1)+"-"+num_to_str(sundays)
        day_of_the_week[the_date]="sunday"
    else:
        the_date=str(year[3])+"-"+num_to_str(m[3]+1)+"-"+num_to_str(sundays)
        day_of_the_week[the_date]="sunday"

    months[1]=28


weather_T = {}
identified_employees=[]
prev_year=0
curr_year=0
count=0
for employee in employees :
    
    yearly_infractions=0
    identified=False
    emp_analysis=[]
    year_analysis=[]
    prev_year_arr=events[events_dict[employee['country']]]['event_date'].split("-")
    prev_year=prev_year_arr[0]
    
    for i in range(events_dict[employee['country']] ,len(events)) :
        if not events[i]['event_date'] or events[i]['event_name']=='BAD_WEATHER':
            continue
        if events[i]['country']!=employee['country'] :
            break

        event_date_arr = events[i]['event_date'].split('-')
        if event_date_arr[0]=='2024' :
            break
        elif event_date_arr[0]=='2022' :
            continue

        good_weather = binary_search_weather(weather,events[i]['event_date'],events[i]['country'],weather_dict,weather_T)

        if not good_weather[1] :
            events[i]['event_name']="BAD_WEATHER"
      
        curr_year=event_date_arr[0]
        weather_before=good_weather[0]
        weather_after=good_weather[2]
        weather_on=good_weather[1]
        event_infractions=0
        clock_in_before="N/A"
        clock_in_after="N/A"
        clock_in_on="N/A"
        late_before=True
        late_after=True
        late_on=True  

        if weather_on and events[i]['country'] == employee['country'] :
            attendance_len = attendance_dict[ employee['record_id'] ][1]
            high = attendance_len-1
            low = attendance_dict[ employee['record_id'] ][0]
            mid = 0
               
            day_before_event_date=minus_day_from_date(events[i]['event_date'])
            day_after_event_date=add_day_to_date(events[i]['event_date'])
            day_before_event_arr=day_before_event_date.split('-')
            day_after_event_arr=day_after_event_date.split('-')
               
            while low <= high:
                mid = (high + low) // 2

                mid_date_arr = attendance[mid]['date'].split('-')

                if mid_date_arr[0]<day_before_event_arr[0]  or (mid_date_arr[0]==day_before_event_arr[0] and mid_date_arr[1]<day_before_event_arr[1]) or (mid_date_arr[0]==day_before_event_arr[0] and mid_date_arr[1]==day_before_event_arr[1] and mid_date_arr[2]<day_before_event_arr[2]) :
                    low = mid + 1
                
                elif mid_date_arr[0]>day_after_event_arr[0] or (mid_date_arr[0]==day_after_event_arr[0] and mid_date_arr[1]>day_after_event_arr[1]) or (mid_date_arr[0]==day_after_event_arr[0] and mid_date_arr[1]==day_after_event_arr[1] and mid_date_arr[2]>day_after_event_arr[2]) :
                    high = mid - 1

                
                else:
                    if attendance[mid]['date']==day_before_event_date:
                    
                        if attendance[mid]['clock_in'] and attendance[mid]['clock_out'] : 
                            late_before = check_clock(attendance[mid]['clock_in'].split(':'), attendance[mid]['clock_out'].split(':'))
                            clock_in_before=attendance[mid]['clock_in']  
                
                        if mid+1 < attendance_len and attendance[mid+1]['clock_in'] and attendance[mid+1]['clock_out'] :
                            
                            if attendance[mid+1]['date']==events[i]['event_date'] :
                                late_on = check_clock(attendance[mid+1]['clock_in'].split(':'), attendance[mid+1]['clock_out'].split(':'))
                                clock_in_on=attendance[mid+1]['clock_in']

                                if mid+2 < attendance_len and attendance[mid+2]['clock_in'] and attendance[mid+2]['clock_out'] :
                                    
                                    if attendance[mid+2]['date']==day_after_event_date :
                                        late_after = check_clock(attendance[mid+2]['clock_in'].split(':'), attendance[mid+2]['clock_out'].split(':'))
                                        clock_in_after=attendance[mid+2]['clock_in']
                    
                            elif attendance[mid+1]['date']==day_after_event_date:
                                late_after = check_clock(attendance[mid+1]['clock_in'].split(':'), attendance[mid+1]['clock_out'].split(':'))
                                clock_in_after=attendance[mid+1]['clock_in']              

                        break

                    elif attendance[mid]['date']==events[i]['event_date'] :
                        if attendance[mid]['clock_in'] and attendance[mid]['clock_out'] :
                            late_on = check_clock(attendance[mid]['clock_in'].split(':'), attendance[mid]['clock_out'].split(':'))
                            clock_in_on=attendance[mid]['clock_in']  
                
                        if mid+1 < attendance_len and attendance[mid+1]['clock_in'] and attendance[mid+1]['clock_out'] :
                            if attendance[mid+1]['date']==day_after_event_date:
                                late_after = check_clock(attendance[mid+1]['clock_in'].split(':'), attendance[mid+1]['clock_out'].split(':'))
                                clock_in_after=attendance[mid+1]['clock_in']
                    
                        if mid > 0 and attendance[mid-1]['clock_in'] and attendance[mid-1]['clock_out'] :
                            if attendance[mid-1]['date']==day_before_event_date:
                                late_before = check_clock(attendance[mid-1]['clock_in'].split(':'), attendance[mid-1]['clock_out'].split(':'))
                                clock_in_before=attendance[mid-1]['clock_in'] 

                        break

                    elif attendance[mid]['date']==day_after_event_date :
                        if attendance[mid]['clock_in'] and attendance[mid]['clock_out'] :
                            late_after = check_clock(attendance[mid]['clock_in'].split(':'), attendance[mid]['clock_out'].split(':'))
                            clock_in_after=attendance[mid]['clock_in']  
                
                        if mid > 0 and attendance[mid-1]['clock_in'] and attendance[mid-1]['clock_out'] :
                            if attendance[mid-1]['date']==events[i]['event_date'] :
                                late_on = check_clock(attendance[mid-1]['clock_in'].split(':'), attendance[mid-1]['clock_out'].split(':'))
                                clock_in_on=attendance[mid-1]['clock_in']

                                if mid > 1 and attendance[mid-2]['clock_in'] and attendance[mid-2]['clock_out']:
                                    if attendance[mid-2]['date']==day_before_event_date :
                                        late_before = check_clock(attendance[mid-2]['clock_in'].split(':'), attendance[mid-2]['clock_out'].split(':'))
                                        clock_in_before=attendance[mid-2]['clock_in']

                            elif attendance[mid-1]['date']==day_before_event_date:
                                clock_in_before=attendance[mid-1]['clock_in']
                                late_before = check_clock(attendance[mid-1]['clock_in'].split(':'), attendance[mid-1]['clock_out'].split(':'))
                        break
                    print("ALL 3 DAYS ABSENT")
                    print(employee)
                    break

        if clock_in_before=="N/A" :
            late_before=True
        if clock_in_on=="N/A" :
            late_on=True
        if clock_in_after=="N/A" :
            late_after=True

        if not weather_before :
            late_before=False
        if not weather_on :
            late_before=False
            late_on=False
            late_after=False
        if not weather_after :
            late_after=False

        if events[i]['event_date'] in day_of_the_week and day_of_the_week[events[i]['event_date']]=="monday":
            late_before=False
        elif events[i]['event_date'] in day_of_the_week and day_of_the_week[events[i]['event_date']]=="friday":
            late_after=False
        elif events[i]['event_date'] in day_of_the_week and day_of_the_week[events[i]['event_date']]=="saturday":
            late_after=False
            late_on=False
        elif events[i]['event_date'] in day_of_the_week and day_of_the_week[events[i]['event_date']]=="sunday":
            late_before=False
            late_on=False

        if late_on and late_after==False:
            event_infractions=event_infractions+1
            
        if late_before and late_after==False:
            event_infractions=event_infractions+1

        if late_on==False and late_before==False and late_after==True:
            event_infractions=event_infractions+1

        if late_on and late_after :
            event_infractions=3
        elif late_before and late_after :
            event_infractions=3

        if event_date_arr[0]!=prev_year :
            if yearly_infractions < 3 :
                year_analysis=[]
            else :
                emp_analysis.append(year_analysis)
                year_analysis=[]
            yearly_infractions=0 

        prev_year=curr_year

        yearly_infractions = yearly_infractions + event_infractions

        if event_infractions > 0 :
            year_analysis.append({ 
                'event_name': events[i]['event_name'], 
                'country': events[i]['country'],
                'event_date': events[i]['event_date'], 
                'number_of_infraction' : event_infractions,
                'yearly_infractions_to_this_date': yearly_infractions
        })

        if yearly_infractions >= 3:
            identified=True
  
    if identified :
        if curr_year==prev_year and yearly_infractions>2:
            emp_analysis.append(year_analysis)

        identified_employees.append({
            'record_id': employee['record_id'], 
            'name': employee['name'], 
            'work_id_number': employee['work_id_number'], 
            'email_address': employee['email_address'], 
            'country': employee['country'],
            'phone_number': employee['phone_number'],
            'average_hours_per_week': 0.00,  
            'events': emp_analysis 
        })
        
        total_days=0
        total_hours=0
        for j in range(attendance_dict[employee['record_id']][0], attendance_dict[employee['record_id']][1] ) :
            if not attendance[j]['clock_in']:
                continue
            if not attendance[j]['clock_out']:
                continue
            if attendance[j]['employee_record_id']!=employee['record_id'] :
                break

            clock_in = attendance[j]['clock_in'].split(':')
            clock_out = attendance[j]['clock_out'].split(':')
            hours=int(clock_out[0])+11
            mins=int(clock_out[1])+60

            if int(clock_out[0]) > int(clock_in[0]):
                hours=int(clock_out[0])-1    

            if int(clock_out[0]) == int(clock_in[0]):
                hours=int(clock_out[0])
                mins=int(clock_out[1])

            hours=hours-int(clock_in[0])
            mins=mins-int(clock_in[1])
                
            hours=(hours*60)+mins
            hours=hours/60.0
            total_hours=total_hours+hours
            total_days=total_days+1
        
        total_days=float(total_days)
        total_hours=total_hours/total_days
        identified_employees[count]['average_hours_per_week']=5.0*total_hours
        count=count+1
 
with open('result.json', 'w') as fp:
    json.dump(identified_employees, fp)

################################################################################################################################################
# line(1-19) The requests module was used to fetch the weather and events from the APIs. 
# line(19-25) Opened the employee.json and attendance.json file from the same directory and loaded files from json to python list.
# line(25-53) Process the weather, events and atttendance to compute and store the start record for the weather and events for each country and for each employee's attendance.
#     The location of the first record where the weather and events start for a new country is stored in dictionaries to implement an efficient sliding window algorithm. Th same is done for the attendance records where a different employee ateendance record starts.
# line(53-243) For each employee ,  for each event date in the employee's country events list and for each record in the attendance for the employees, check the attendance list to see :
# line(77-91) The events[i][event_date'] was checked for bad weather in the same country as the event.
# line(94) The events[i][event_date'] was split to compare to the date of the attendance records for employees in the same country as the event.
# line(115-150) The employee records was checks for late on, before or after the event date
# line(151-158) clock_in(_on,_after,_before)="N/A" for on the day of,day before or day after the event is used to indicate absenteeism. 
# line(158-165) Give a sepate infraction for being late on,before or after an event.
# line(172-180) The year_analysis[] list stores all infractions in a year for an employee. Here this list must be cleared when an event with a new year is encountered and stored if the yearly_infractions is greater than 2.
# line(183-188) If 3 or more infractions are found in a year the year_analysis[] list will become the list of suspicious events for the employee.
# line(197-208) The soloution is placed in identified_employees[] which is a list of dictionaries. The last items in this dictionary is the list of suspicious events.
# line(208-239) 'average_hours_per_week' is only computed for employees identified as having 3 or more infraction in a year. 
# attendance[77927] clockin: and clockout:None, 
#
#  WEATHER
#  "country": "Australia",
#  "date": "2022-01-01",
#  "condition": "rainy",
#  "max_temp": 24,
#
#  EVENT
#  "id": 24,
#  "event_name": "Whimsical Festival",
#  "event_date": "2024-04-19",
#  "country": "Australia", 
#
# EMPLOYEE
# record_id": 1, 
# "name": "Dawn Hartman", 
# "work_id_number": "1d27d30c-0da9-4cd4-8624-ee33f954b637", 
# "email_address": "nicholascook@example.org", 
# "country": "Trinidad and Tobago", 
# "phone_number": "484.871
#
#  ATTENDANCE
#  "record_id": 1, 
#  "date": "2022-01-03", 
#  "clock_in": "08:06:00", 
#  "clock_out": "16:32:00", 
#  "employee_record_id":


def binary_search_attendance(attendance, event_date):
    event_date_arr = event_date.split('-')
    late_before = True
    late_on = True
    late_after = True
    clock_in_before="N/A"
    clock_in_on="N/A"
    clock_in_after="N/A"
    low = 0
    high = len(attendance) - 1
    mid = 0
    

    while low <= high:
 
        mid = (high + low) // 2
        mid_date_arr = attendance[mid]['date'].split('-')

        # If x is greater, ignore left half
        if mid_date_arr[0]<event_date_arr[0] or mid_date_arr[1]<event_date_arr[1] or (mid_date_arr[0]==event_date_arr[0] and mid_date_arr[1]==event_date_arr[1] and mid_date_arr[2]<event_date_arr[2]-1 ):
            low = mid + 1
 
        # If weather[mid]['date'] > event_date then the event_date is smaller so ignore the right half
        elif mid_date_arr[0]>event_date_arr[0] or mid_date_arr[1]>event_date_arr[1] or (mid_date_arr[0]>event_date_arr[0] or mid_date_arr[1]>event_date_arr[1] and mid_date_arr[2]>event_date_arr[2]+1) :
            high = mid - 1
 
        # means x is present at mid
        elif mid_date_arr[0]==event_date_arr[0] and mid_date_arr[1]==event_date_arr[1] and mid_date_arr[2]==event_date_arr[2]-1 :
            late_before = check_clock(attendance[mid]['clock_in'].split(':'), attendance[mid]['clock_out'].split(':'))
            clock_in_before=attendance[mid]['clock_in']  
                
            mid_date_arr1 = attendance[mid+1]['date'].split('-')
            if mid_date_arr1[0]==event_date_arr[0] and mid_date_arr1[1]==event_date_arr[1] and mid_date_arr1[2]==event_date_arr[2] :
                late_on = check_clock(attendance[mid+1]['clock_in'].split(':'), attendance[mid+1]['clock_out'].split(':'))
                clock_in_on=attendance[mid+1]['clock_in']

                mid_date_arr2 = attendance[mid+2]['date'].split('-')
                if mid_date_arr2[0]==event_date_arr[0] and mid_date_arr2[1]==event_date_arr[1] and mid_date_arr2[2]==event_date_arr[2]+1 :
                    late_after = check_clock(attendance[mid+2]['clock_in'].split(':'), attendance[mid+2]['clock_out'].split(':'))
                    clock_in_after=attendance[mid+2]['clock_in']
                    
            elif mid_date_arr1[0]==event_date_arr[0] and mid_date_arr1[1]==event_date_arr[1] and mid_date_arr1[2]==event_date_arr[2]+1:
                late_after = check_clock(attendance[mid+1]['clock_in'].split(':'), attendance[mid+1]['clock_out'].split(':'))
                clock_in_after=attendance[mid+1]['clock_in']              
                
        elif mid_date_arr[0]==event_date_arr[0] and mid_date_arr[1]==event_date_arr[1] and mid_date_arr[2]==event_date_arr[2] :
            late_on = check_clock(attendance[mid]['clock_in'].split(':'), attendance[mid]['clock_out'].split(':'))
            clock_in_on=attendance[mid]['clock_in']  
                
            mid_date_arr1 = attendance[mid+1]['date'].split('-')
            if mid_date_arr1[0]==event_date_arr[0] and mid_date_arr1[1]==event_date_arr[1] and mid_date_arr1[2]==event_date_arr[2]+1:
                late_after = check_clock(attendance[mid+1]['clock_in'].split(':'), attendance[mid+1]['clock_out'].split(':'))
                clock_in_after=attendance[mid+1]['clock_in']
                    
            mid_date_arr2 = attendance[mid-1]['date'].split('-')
            if mid_date_arr2[0]==event_date_arr[0] and mid_date_arr2[1]==event_date_arr[1] and mid_date_arr2[2]==event_date_arr[2]-1:
                late_before = check_clock(attendance[mid-1]['clock_in'].split(':'), attendance[mid-1]['clock_out'].split(':'))
                clock_in_before=attendance[mid-1]['clock_in'] 

        elif mid_date_arr[0]==event_date_arr[0] and mid_date_arr[1]==event_date_arr[1] and mid_date_arr[2]==event_date_arr[2]+1 :
            late_after = check_clock(attendance[mid]['clock_in'].split(':'), attendance[mid]['clock_out'].split(':'))
            clock_in_after=attendance[mid]['clock_in']  
                
            mid_date_arr1 = attendance[mid-1]['date'].split('-')
            if mid_date_arr1[0]==event_date_arr[0] and mid_date_arr1[1]==event_date_arr[1] and mid_date_arr1[2]==event_date_arr[2] :
                late_on = check_clock(attendance[mid-1]['clock_in'].split(':'), attendance[mid-1]['clock_out'].split(':'))
                clock_in_on=attendance[mid-1]['clock_in']

                mid_date_arr2 = attendance[mid-2]['date'].split('-')
                if mid_date_arr2[0]==event_date_arr[0] and mid_date_arr2[1]==event_date_arr[1] and mid_date_arr2[2]==event_date_arr[2]-1:
                    late_before = check_clock(attendance[mid-2]['clock_in'].split(':'), attendance[mid-2]['clock_out'].split(':'))
                    clock_in_before=attendance[mid-2]['clock_in']

            elif mid_date_arr1[0]==event_date_arr[0] and mid_date_arr1[1]==event_date_arr[1] and mid_date_arr1[2]==event_date_arr[2]-1:
                clock_in_before=attendance[mid-1]['clock_in']
                late_before = check_clock(attendance[mid-1]['clock_in'].split(':'), attendance[mid-1]['clock_out'].split(':'))


            return [late_before,late_on,late_after]
 
    # Here, the employee was not present on the of event_date,niether the day before nor the day after.
    return [late_before,late_on,late_after]


