import requests
from bs4 import BeautifulSoup
import json
import string_constants

class Semester(object):
    def __init__(self, session, semester, url = ''):
        self.session = session
        self.semester = semester
        if url == '':
            current_url = string_constants.url + semester
        else:
            current_url = url
        r = session.get(current_url)
        if r.status_code == 200:
            html = r.text
            html = html.replace('\n', '')
            self.soup = BeautifulSoup(html, "lxml")

    def _get_current_session_url(self):
        soup = self.soup
        tag = soup.find('a', {'title':'Latest Enrollment'})
        return tag['href']

    def get_data(self):
        """docstring for get_data"""
        soup = self.soup
        all_data = {}

        #Getting semester details
        details = {}
        form = soup.find('form', {'id' : string_constants.form_id})
        details_tag_list = form.find_all('input')
        details['session'] = details_tag_list[1]['value']
        details['credits'] = details_tag_list[2]['value']
        details['gpa'] = details_tag_list[3]['value']

        subjects = []
        i = 1
        while True:
            i_str = str(i)
            if soup.find('span', {'id': string_constants.course_id + i_str}) != None:
                subject_details = {}
                #Fetching tags with details
                code = soup.find('span', {'id' : string_constants.course_code_id + i_str})
                course = soup.find('span', {'id' : string_constants.course_id + i_str})
                credits = soup.find('span', {'id' : string_constants.course_credit_id + i_str })
                grade = soup.find('span', {'id' : string_constants.course_grade_id + i_str})
                session = soup.find('span', {'id' : string_constants.course_session_id + i_str})
                #Saving them in a dict
                subject_details['code'] = str(code.text)
                subject_details['course'] = str(course.text)
                subject_details['grade'] = str(grade.text)
                subject_details['credits'] = str(credits.text)
                subject_details['session'] = str(session.text)

                subjects.append(subject_details)
                i += 1
            else:
                break
        all_data['details'] = details
        all_data['sub_details'] = subjects
        self.all_data = all_data
        return [details, subjects]

    def get_attendance(self, url = ''):
        """docstring for get_attendance"""
        soup = self.soup
        all_data = {}
        attendance = []
        #Getting attendance details
        if url == '':
            form = soup.find('form', {'id' : string_constants.form_id})
            details_tag_list = form.find_all('input')
            current_session = details_tag_list[1]['value'] 
            current_url = string_constants.url_details + current_session
        else:
            current_url = url
        r = self.session.get(current_url)
        if r.status_code == 200:
            html = r.text
            html = html.replace('\n', '')
            soup = BeautifulSoup(html, "lxml")
            self.soup_detailed = soup
        i = 1
        while True:
            i_str = str(i)
            if soup.find('span', {'id' : string_constants.attendance_code_id + i_str})!=None:
                attendance_details = {}
                subject_name = soup.find('span', {'id' : string_constants.attendance_name_id + i_str})
                classes_taken = soup.find('span', {'id' : string_constants.attendance_classes_id + i_str})
                classes_absent = soup.find('span', {'id' : string_constants.attendance_absent_id + i_str})
                classes_attended = soup.find('span', {'id' : string_constants.attendance_attended_id + i_str})
                attendance_percent = soup.find('span', {'id' : string_constants.attendance_percent_id + i_str})
                last_updated = soup.find('span', {'id' : string_constants.attendance_last_updated + i_str})

                attendance_details['subject_name'] = subject_name.text
                attendance_details['classes_taken'] = classes_taken.text
                attendance_details['classes_absent'] = classes_absent.text
                attendance_details['classes_attended'] = classes_attended.text
                attendance_details['attendance_percent'] = attendance_percent.text
                attendance_details['last_updated'] = last_updated.text
                attendance.append(attendance_details)
                i = i + 1
            else:
                break
        all_data['attendance'] =  attendance
        return all_data

    def get_internals(self):
        """docstring for get_internals"""
        soup = self.soup_detailed
        all_data = {}
        internals = []
        position = []
        for i in '123':
            pos = str(soup.text.find('Internal Assessment (IA) - ['+i))
            if pos == -1:
                continue
            position.append(pos + 'ia' + i)
        position.sort()
        i = 1
        while True:
            i_str = str(i)
            if soup.find('span', {'id' : string_constants.internal_code_id + i_str})!=None:
                internal_details = {}
                subject_code = soup.find('span', {'id' : string_constants.internal_code_id + i_str})
                subject_name = soup.find('span', {'id' : string_constants.internal_subject_name + i_str})
                marks = soup.find_all('span', {'id' : string_constants.internal_marks_id + i_str})

                internal_details['subject_name'] = str(subject_name.text)
                for j in range(len(marks)):
                    internal_details['sessional'+position[j][-1]] = str(marks[j].text)
                internals.append(internal_details)
                i = i + 1
            else:
                break
        #self.all_data['internals'] = internals
        all_data['internals'] = internals
        return all_data
        