"""Hackbright Project Tracker.

A front-end for a database that allows users to work with students, class
projects, and the grades students receive in class projects.
"""

import sqlite3

db_connection = sqlite3.connect("hackbright.db", check_same_thread=False)
db_cursor = db_connection.cursor()


def get_student_by_github(github):
    """Given a github account name, print information about the matching student."""

    QUERY = """
        SELECT first_name, last_name, github
        FROM Students
        WHERE github = ?
        """
    db_cursor.execute(QUERY, (github,))
    row = db_cursor.fetchone()
    print "Student: %s %s\nGithub account: %s" % (
        row[0], row[1], row[2])


def make_new_student(first_name, last_name, github):
    """Add a new student and print confirmation.
    
    Given a first name, last name and Github account, add student 
    to the database and print a confirmation message.
    """
    QUERY = """INSERT INTO Students VALUES(?,?,?)"""
    db_cursor.execute(QUERY, (first_name, last_name, github))
    db_connection.commit()
    print "Successfully added student: %s %s" % (first_name, last_name)


def get_project_by_title(title):
    """Given a project title, print information about the project."""
    
    QUERY = """SELECT title, description, max_grade FROM Projects WHERE title = ?"""
    db_cursor.execute(QUERY, (title,))
    row = db_cursor.fetchone()
    print "Project title: %s, description: %s, and max grade is %s." % (
        row[0], row[1], row[2])


def get_grade_by_github_title(github, title):
    """Print grade student received for a project."""
    QUERY = """SELECT grade FROM Grades WHERE student_github = ? AND 
    project_title = ?"""
    db_cursor.execute(QUERY, (github, title))
    row = db_cursor.fetchone()
    print "Grade: %d" %(row[0])


def assign_grade(github, title, grade):
    """Assign a student a grade on an assignment and print a confirmation."""
    QUERY = """INSERT INTO Grades VALUES(?,?,?)"""
    db_cursor.execute(QUERY, (github, title, grade))
    db_connection.commit()
    print "Success! %s received a grade of %s on the %s project!" % (github, grade, title)

def add_new_project(title, description, max_grade):
    """Add a new project with a Project Title, Description, and Max Grade"""
    QUERY = """INSERT into Projects (title, description, max_grade) VALUES(?,?,?)"""
    db_cursor.execute(QUERY, (title, description, max_grade))
    db_connection.commit()
    print "Success! Add %s project, and here is the description: %s, and max grade: %s"\
    %(title, description, max_grade)

def get_all_grades(first_name, last_name):
    """Shows the grades of each project for the student"""
    QUERY = """ SELECT s.first_name, s.last_name, g.project_title, g.grade 
    FROM Students AS s 
    INNER JOIN Grades AS g ON s.github = g.student_github
    WHERE s.first_name = ? AND s.last_name = ? """
    db_cursor.execute(QUERY, (first_name, last_name))
    grades_data = db_cursor.fetchone()
    print grades_data[-1]



def handle_input():
    """Main loop.

    Repeatedly prompt for commands, performing them, until 'quit' is received as a
    command."""

    command = None

    while command != "quit":
        input_string = raw_input("HBA Database> ")
        tokens = input_string.split()
        command = tokens[0]
        args = tokens[1:]

        if command == "student":
            github = args[0]
            get_student_by_github(github)

        elif command == "new_student":
            first_name, last_name, github = args   # unpack!
            make_new_student(first_name, last_name, github)

        elif command == "project":
            title = args[0]   # unpack!
            get_project_by_title(title)

        elif command == "grade":
            github = args[0]
            title = args[1]
            get_grade_by_github_title(github, title)

        elif command == "update_grade":
            github, title, grade = args
            assign_grade(github, title, grade)

        elif command == "new_project":
            title = args[0]
            description = " ".join(args[1:-1])
            max_grade = int(args[-1])
            add_new_project(title, description, max_grade)
        elif command == "get_all_grades":
            first_name = args[0]
            last_name = args[1]
            get_all_grades(first_name, last_name)




            


if __name__ == "__main__":
    handle_input()

    # To be tidy, we'll close our database connection -- though, since this
    # is where our program ends, we'd quit anyway.

    db_connection.close()
