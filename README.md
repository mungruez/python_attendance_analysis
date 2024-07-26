# Attendance and Punctuality Analysis
## solution : python script - attendance_analysis.py

- ![#f03c15](https://www.iconsdb.com/icons/download/color/f03c15/circle-16.png) line(1-19) The requests module was used to fetch the weather and events from the APIs.
  
- ![#f03c15](https://www.iconsdb.com/icons/download/color/f03c15/circle-16.png) line(19-25) Opened the employee.json and attendance.json file from the same directory and loaded files from json to python list.
 
- ![#f03c15](https://www.iconsdb.com/icons/download/color/f03c15/circle-16.png) line(25-53) Process the weather, events and atttendance to compute and store the start record for the weather and events for each country and for each employee's attendance. The location of the first record where the weather and events start for a new country is stored in dictionaries to implement an efficient sliding window algorithm. Th same is done for the attendance records where a different employee ateendance record starts.

- ![#f03c15](https://www.iconsdb.com/icons/download/color/f03c15/circle-16.png) line(53-243) For each employee ,  for each event date in the employee's country events list and for each record in the attendance for the employees, check the attendance list :
 
- ![#f03c15](https://www.iconsdb.com/icons/download/color/f03c15/circle-16.png)  line(77-91) The events[i][event_date'] was checked for bad weather in the same country as the event.
- ![#f03c15](https://www.iconsdb.com/icons/download/color/f03c15/circle-16.png)  line(94) The events[i][event_date'] was split to compare to the date of the attendance records for employees in the same country as the event.
- ![#f03c15](https://www.iconsdb.com/icons/download/color/f03c15/circle-16.png) line(115-150) The employee records was checks for late on, before or after the event date
 
- ![#f03c15](https://www.iconsdb.com/icons/download/color/f03c15/circle-16.png) line(151-158) clock_in(_on,_after,_before)="N/A" for on the day of,day before or day after the event is used to indicate absenteeism.
- ![#f03c15](https://www.iconsdb.com/icons/download/color/f03c15/circle-16.png) line(158-165) Give a sepate infraction for being late on,before or after an event.
  
- ![#f03c15](https://www.iconsdb.com/icons/download/color/f03c15/circle-16.png) line(172-180) The year_analysis[] list stores all infractions in a year for an employee. Here this list must be cleared when an event with a new year is encountered and stored if the yearly_infractions is greater than 2.
 
- ![#f03c15](https://www.iconsdb.com/icons/download/color/f03c15/circle-16.png) line(183-188) If 3 or more infractions are found in a year the year_analysis[] list will become the list of suspicious events for the employee.
- ![#f03c15](https://www.iconsdb.com/icons/download/color/f03c15/circle-16.png) line(197-208) The soloution is placed in identified_employees[] which is a list of dictionaries. The last items in this dictionary is the list of suspicious events.
- ![#f03c15](https://www.iconsdb.com/icons/download/color/f03c15/circle-16.png) line(208-239) 'average_hours_per_week' is only computed for employees identified as having 3 or more infraction in a year.
  
- ![#f03c15](https://www.iconsdb.com/icons/download/color/f03c15/circle-16.png) binary_search_weather(weather,event_date,...) function : A tweaked Binary Search Algorithm with memoization to find the weather condition on a given event_date or before or after the event_date.
  When either of the three days are found the function checks the weather and dates for records for the day before and after then returns.
  
### Anormalies 
 Some recodrs in the attendance contain anormalies
 
 attendance[77927]['clock_in'] = None and attendance[77927]['clock_out'] = None,

### Fields contained in the Weather, Events, Employee and Attendance data

#####  WEATHER
######  "country": "Australia",
######  "date": "2022-01-01",
######  "condition": "rainy",
######  "max_temp": 24,

#####  EVENT
######  "id": 24,
######  "event_name": "Whimsical Festival",
######  "event_date": "2024-04-19",
######  "country": "Australia", 

##### EMPLOYEE
###### record_id": 1, 
###### "name": "Dawn Hartman", 
###### "work_id_number": "1d27d30c-0da9-4cd4-8624-ee33f954b637", 
###### "email_address": "nicholascook@example.org", 
###### "country": "Trinidad and Tobago", 
###### "phone_number": "484.871
#
#  ATTENDANCE
#  "record_id": 1, 
#  "date": "2022-01-03", 
#  "clock_in": "08:06:00", 
#  "clock_out": "16:32:00", 
#  "employee_record_id":
