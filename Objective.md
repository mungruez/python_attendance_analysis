Attendance & Punctuality Analysis 

Objective 

Develop a solution to identify employees who have a habit of coincidentally being either tardy, absent or depart early from work on the day of, day before, or day after popular fetes and events. 

Scenario 

####################MOCK SCENARIO START #################### 

We Employ is an international company that employees 10,000 staff and operates in Port-of- Spain, Trinidad and Tobago; Edmonton, Canada; Oregon, USA; Sydney, Australia; Düsseldorf, Germany. Every employee is expected to start work at 8:00am with a grace period of 15 minutes for late comers and must work until 4:00pm, Monday - Friday.

HR has been getting complaints from team members in Germany who have noted that a number of their international colleagues have a habit of coincidentally being either tardy, absent or depart early from work on the day of, day before, or day after popular fetes and events, which has significantly affected production timelines.

The board finds this unacceptable and have requested that HR work together with IT to identify the employees demonstrating this pattern of behaviour and issue warning letters.

The board accepts that external factors will affect an employee's ability to be present at work and as such are exempt. One such external factor is extreme weather including hail, blizzards, thunderstorms, extreme heat (>40C), and hurricanes. 

The following API services provide weather and event data:  

- https://www.pingtt.com/exam/weather
- https://www.pingtt.com/exam/events

Event API

Available query parameters:

- year 
- country 
- fields (a comma separated list of fields to be included in your result) (acts as a field filter) 

Notes: 

- ID is a unique identifier for event data 
- Each id uniquely identifies an event 
- There may be events two days or fewer apart in the same country 

Weather API

Available query parameters:

- year 
- country 
- fields (a comma separated list of fields to be included in your result) (acts as a field filter) 

Notes: 

- There is a record in weather data for each weekday of 2023 
- Date & country are together a unique identifier for weather 

The attendance and employee data files can be downloaded from:  ![](Aspose.Words.678a66ae-26e1-4016-b16b-9c6ea3c7b3c8.001.png)![](Aspose.Words.678a66ae-26e1-4016-b16b-9c6ea3c7b3c8.002.png)ping\_lead\_developer\_exam  

Employee Data 

- record\_id in employee data file is unique 
- Each record\_id uniquely identifies an employee

Attendance Data 

- There are no null clock-ins with non-null clock-outs
- There are no null clock-outs with non-null clock-ins
- There is a record in attendance data for every employee on each weekday of 2023
- A null clock-out and a null clock-in on the same day indicate an absence

####################MOCK SCENARIO END ####################

Requirements 

- Develop a solution using any available tools or techniques to identify all employees in 2023 in the mock scenario above who show a pattern of tardiness/leaving early or absenteeism on the day of, day after, or day before a popular fete/event in their country with the exception of days with extreme weather.
  - Each day an employee is tardy or leaves early or is absent on the day of, the day before, or the day after an event counts as a separate infraction toward establishing a pattern (assuming the weather was good on that day). 
  - If an employee is both tardy and leaves early on a suspicious date, this counts as one infraction 
  - If an employee is tardy or leaves early or is absent on the day of, the day before, and the day after an event, this counts as three infractions  
  - An employee can incur a maximum of three infractions for the same event
  - An employee should not incur more than one infraction for the same attendance date
  - A pattern is determined as having more than 3 infractions for the year
- Generate a list of the identified employees with their record id, name, work id number, average number of hours worked per week, email address, phone number, country, and a list of the events that they are suspected to have attended. The final result should be 

  in json format. 

  Example format:

  [{"record\_id": 85,

  `  `"name": "Andrea Maldonado",

  `  `"work\_id\_number": "baa8f78b-9ea6-42fb-8857-42d55e74ec7b",   "email\_address": "chenjillian@example.net",

  `  `"country": "Australia",

  `  `"phone\_number": "001-719-806-6647x917",

  `  `"average\_hours\_per\_week": 44.15160256410258,

  `  `"events": [

  `    `{

  `      `"country": "Australia",

  `      `"event\_name": "Electrifying Affair",

  `      `"event\_date": "2023-05-22"

  `    `},

  `    `{

  `      `"country": "Australia",

  `      `"event\_name": "Lively Gala",

  `      `"event\_date": "2023-07-24"

  `    `},

  `    `{

  `      `"country": "Australia",

  `      `"event\_name": "Electrifying Soiree",

  `      `"event\_date": "2023-08-29"

  `    `},

  `    `{

  `      `"country": "Australia",

  `      `"event\_name": "Energetic Fete",

  `      `"event\_date": "2023-11-03"

  `    `}]

  },

  {

    ...

  }]

Deliverables 

- Link to the GitHub repository 
- Link to solution json file  

Submission 

- Upload the source code and the solution json file to a repository on GitHub 
