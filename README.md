# Certificate Portal

`docker-compose up`

## SQL Requirements
- People table
	- Person ID, Name
- Course table
	- Course ID, Course Name
- CourseMentors table
	- CourseID, PersonID
- Certificate table
	- Person ID, Course ID, Mentor ID (also from People table)
