import requests
from bs4 import BeautifulSoup
import json

class Semester(object):
    """docstring for Semester"""

    form_id = 'ProgramAdmissionItemDetail'
    credits_id = 'ProgramAdmissionItemDetail_pcredits_title'
    gpa_id = 'ProgramAdmissionItemDetail_ptermResultScore_title'
    course_code_id = 'cc_TermGradeBookSummary_internalName_'
    course_id = 'cc_TermGradeBookSummary_productName_'
    course_credit_id = 'cc_TermGradeBookSummary_credit_'
    course_grade_id = 'cc_TermGradeBookSummary_pfinalResult_'
    course_session_id = 'cc_TermGradeBookSummary_customTimePeriodId_'
    attendance_id = 'cc_ListAttendanceSummary_'
    subject_name = 'productName_'
    classes_taken = 'attendanceTaken_'
    classes_attended = 'classesAttended_'
    classes_absent = 'classesAbsent_'
    attendance_percentage = 'attendancePercentage_'
    last_updated = 'lastUpdatedStamp_'

    url = 'http://websismit.manipal.edu/websis/control/StudentAcademicProfile'
    url += '?productCategoryId=0905-TERM-'
    urlCustomTimePeriod = 'http://websismit.manipal.edu/websis/control/'
    urlCustomTimePeriod += 'ListCTPEnrollment?customTimePeriodId='

    def __init__(self, session, semester):
        self.session = session
        self.semester = semester
        current_url = Semester.url + semester
        r = session.get(current_url)
        if r.status_code == 200:
            html = r.text
            html = html.replace('\n', '')
            self.soup = BeautifulSoup(html, "lxml")

    def get_data(self):
        """docstring for get_data"""
        soup = self.soup
        all_data = {}

        #Getting semester details
        details = {}
        form = soup.find('form', {'id' : Semester.form_id})
        details_tag_list = form.find_all('input')
        details['session'] = details_tag_list[1]['value']
        details['credits'] = details_tag_list[2]['value']
        details['gpa'] = details_tag_list[3]['value']

        subjects = []
        i = 1
        while True:
            i_str = str(i)
            if soup.find('span', {'id': Semester.course_id + i_str}) != None:
                subject_details = {}
                #Fetching tags with details
                code = soup.find('span', {'id' : Semester.course_code_id + i_str})
                course = soup.find('span', {'id' : Semester.course_id + i_str})
                credits = soup.find('span', {'id' : Semester.course_credit_id + i_str })
                grade = soup.find('span', {'id' : Semester.course_grade_id + i_str})
                session = soup.find('span', {'id' : Semester.course_session_id + i_str})
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
        all_data['subject_details'] = subjects
        return all_data

    def get_attendance(self):
        """docstring for get_attendance"""
        soup = self.soup
        all_data = {}
        attendance = []
        #Getting attendance details
        form = soup.find('form', {'id' : Semester.form_id})
        details_tag_list = form.find_all('input')
        currentSession = details_tag_list[1]['value'] 
        current_url = Semester.urlCustomTimePeriod + currentSession
        r = session.get(current_url)
        if r.status_code == 200:
            html = r.text
            html = html.replace('\n', '')
            soup = BeautifulSoup(html, "lxml")
        i = 1
        while True:
            i_str = str(i)
            if soup.find('span', {'id' : self.attendance_id + self.attendance_percentage + i_str})!=None:
                attendance_details = {}
                subject = soup.find('span', {'id' : Semester.attendance_id + Semester.subject_name + i_str})
                numberOfClassesTaken = soup.find('span', {'id' : Semester.attendance_id + Semester.classes_taken + i_str})
                numberOfClassesAbsent = soup.find('span', {'id' : Semester.attendance_id + Semester.classes_absent + i_str})
                numberOfClassesAttended = soup.find('span', {'id' : Semester.attendance_id + Semester.classes_attended + i_str})
                attendancePercentage = soup.find('span', {'id' : Semester.attendance_id + Semester.attendance_percentage + i_str})
                lastUpdatedStamp = soup.find('span', {'id' : Semester.attendance_id + Semester.last_updated + i_str})

                attendance_details['subjectName'] = subject.text
                attendance_details['numberOfClassesTaken'] = numberOfClassesTaken.text
                attendance_details['numberOfClassesAbsent'] = numberOfClassesAbsent.text
                attendance_details['numberOfClassesAttended'] = numberOfClassesAttended.text
                attendance_details['attendancePercentage'] = attendancePercentage.text
                attendance_details['lastUpdatedStamp'] = lastUpdatedStamp.text
                attendance.append(attendance_details)
                i = i + 1
            else:
                break
        all_data['attendance'] =  attendance
        return all_data

if __name__ == '__main__':
    url = "http://websismit.manipal.edu/websis/control/createAnonSession"
    payload = {}
    payload['idValue'] = raw_input("Enter reg num: ")
    payload['birthDate'] = raw_input("Enter birthDate: ")
    session = requests.session()
    response = session.post(url, data=payload)
    sem_details = {}
    attendance_details = {}
    if response.text.find('Profile of') == -1:
        print "Invalid details"
    else:
        for i in range(1, 1+8):
            try:
                semObj = Semester(session, str(i))
                sem_details['semester'+str(i)] = semObj.get_data()
                attendance_details['semester' + str(i)] =  semObj.get_attendance()
            except AttributeError:
                break

    attendance_json = json.dumps(attendance_details, indent=4, sort_keys=True, ensure_ascii=False)
    f = open('attendance.json', 'w')
    f.write((attendance_json).encode('ascii', 'ignore')) # We need to figure out a better solution for this encoding issue. 
    f.close()

    details_json = json.dumps(sem_details, indent=4, sort_keys=True, ensure_ascii=False)
    f = open('data.json', 'w')
    f.write(str(details_json))
    f.close()