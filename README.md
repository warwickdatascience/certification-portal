# Certificate Portal

`docker-compose up`

## SQL Requirements
- People table
	- ID, Name
- Courses table
	- ID, Name, Description
- CourseMentors table
	- ID, MentorID, CourseID
- Certificates table
	- ID, HashValue, StudentID, MentorID, CourseID

- Process
	- Populate DB with information (we could have an administrative endpoint to do this)
	- Currently /generate passes name, mentor, course, desc
	- Instead, pass studentID, mentorID, courseID
	- Then, add to the certificate table with these alongside the PDF hash
	- On the other endpoint, hash should cause lookup of studentID, mentorID and courseID
	- The CourseMentors table only exists to perhaps inform a front-end that generates the certificate by limiting mentors to choose from
