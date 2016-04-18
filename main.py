import requests
from bs4 import BeautifulSoup
import json

class Semester(object):
    """docstring for Semester"""

    url = 'http://websismit.manipal.edu/websis/control/StudentAcademicProfile'
    url += '?productCategoryId=0905-TERM-'
    url_details = 'http://websismit.manipal.edu/websis/control/'
    url_details += 'ListCTPEnrollment?customTimePeriodId='

    #HTML IDs to be used in first url
    form_id = 'ProgramAdmissionItemDetail'
    credits_id = 'ProgramAdmissionItemDetail_pcredits_title'
    gpa_id = 'ProgramAdmissionItemDetail_ptermResultScore_title'
    course_code_id = 'cc_TermGradeBookSummary_internalName_'
    course_id = 'cc_TermGradeBookSummary_productName_'
    course_credit_id = 'cc_TermGradeBookSummary_credit_'
    course_grade_id = 'cc_TermGradeBookSummary_pfinalResult_'
    course_session_id = 'cc_TermGradeBookSummary_customTimePeriodId_'

    #HTML IDs to be used in second url
    attendance_id = 'cc_ListAttendanceSummary_'
    attendance_code_id = attendance_id + 'productId_'
    attendance_name_id = attendance_id + 'productName_'
    attendance_classes_id = attendance_id + 'attendanceTaken_'
    attendance_attended_id = attendance_id + 'classesAttended_'
    attendance_absent_id = attendance_id + 'classesAbsent_'
    attendance_percent_id = attendance_id + 'attendancePercentage_'
    attendance_last_updated = attendance_id + 'lastUpdatedStamp_'
    internal_id = 'cc_ListAssessmentScores_'
    internal_code_id = internal_id + 'internalName_'
    internal_subject_name = internal_id + 'productName_'
    internal_marks_id = internal_id + 'obtainedMarks_'

    #HTML IDs to be used in get_personal_details
    user_name_id = 'cc_ProfileTitle_name'
    user_section_id = 'cc_ProfileTitle_sectionCode'
    user_gender_id = 'ProfileSummary_gender_title'
    user_birth_date_id = 'ProfileSummary_birthDate_title'
    user_joining_year_id = 'ProfileSummary_customTimePeriodId_title'
    user_nationality_id = 'ProfileSummary_nationalityId_title'
    user_identification_table_id = 'listPartyIdentification_table'


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
        self.all_data = all_data
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
        current_url = Semester.url_details + currentSession
        r = session.get(current_url)
        if r.status_code == 200:
            html = r.text
            html = html.replace('\n', '')
            soup = BeautifulSoup(html, "lxml")
            self.soup_detailed = soup
        i = 1
        while True:
            i_str = str(i)
            if soup.find('span', {'id' : self.attendance_code_id + i_str})!=None:
                attendance_details = {}
                subject_name = soup.find('span', {'id' : Semester.attendance_name_id + i_str})
                classes_taken = soup.find('span', {'id' : Semester.attendance_classes_id + i_str})
                classes_absent = soup.find('span', {'id' : Semester.attendance_absent_id + i_str})
                classes_attended = soup.find('span', {'id' : Semester.attendance_attended_id + i_str})
                attendance_percent = soup.find('span', {'id' : Semester.attendance_percent_id + i_str})
                last_updated = soup.find('span', {'id' : Semester.attendance_last_updated + i_str})

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

    def get_personal_details(self):
        user_details = {}
        current_url = 'http://websismit.manipal.edu/websis/control/viewStudentProfile'
        r = session.get(current_url)
        if r.status_code == 200:
            html = r.text
            html = html.replace('\n', '')
            soup = BeautifulSoup(html, "lxml")
        if soup.find('span', {'id' : Semester.user_name_id})!=None:
            user_name = soup.find('span', {'id' : Semester.user_name_id})
            user_details['name'] = user_name.text.strip()
            user_section = soup.find('span', {'id' : Semester.user_section_id})
            user_details['section'] = user_section.text.strip('Section ');
            gender = soup.find('span', {'id' : Semester.user_gender_id})
            user_gender = gender.findNext('td')
            user_details['gender'] = user_gender.text.strip()
            birth_date = soup.find('span', {'id' : Semester.user_birth_date_id})
            user_birth_date = birth_date.findNext('td')
            user_details['birth_date'] = user_birth_date.text.strip()
            joining_year = soup.find('span', {'id' : Semester.user_joining_year_id})
            user_joining_year = joining_year.findNext('td')
            user_details['year_of_joining'] = user_joining_year.text.split('-')[0]
            nationality = soup.find('span', {'id' : Semester.user_nationality_id})
            user_nationality = nationality.findNext('td')
            user_details['nationality'] =  user_nationality.text.strip()
            mobile_number = soup.find('b', string = 'Mobile Phone')
            user_mobile_number = mobile_number.findNext('div')
            user_details['mobile_number'] = user_mobile_number.text.strip()
            email_id = soup.find('b', string = 'Email Address')
            user_email_id = email_id.findNext('div')
            user_details['email_id'] = user_email_id.text.strip()
            home_phone = soup.find('b', string = 'Home Phone')
            user_home_phone = home_phone.findNext('div')
            user_details['home_phone'] = user_home_phone.text.strip()
            permanent_address = soup.find('b', string = 'Permanent Address')
            user_permanent_address = permanent_address.findNext('div')
            user_details['permanent_address'] = " ".join(user_permanent_address.text.split())
            identification_table = soup.find('table', {'id' : Semester.user_identification_table_id})
            user_identification_table = identification_table.find_all('td')
            user_registeration_number = user_identification_table[1].text.strip()
            user_admission_number = user_identification_table[3].text.strip()
            user_roll_number = user_identification_table[5].text.strip()
            user_details['registeration_number'] = user_registeration_number
            user_details['admission_number'] = user_admission_number
            user_details['roll_number'] = user_roll_number

        return user_details

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
            if soup.find('span', {'id' : self.internal_code_id + i_str})!=None:
                internal_details = {}
                subject_code = soup.find('span', {'id' : Semester.internal_code_id + i_str})
                subject_name = soup.find('span', {'id' : Semester.internal_subject_name + i_str})
                marks = soup.find_all('span', {'id' : Semester.internal_marks_id + i_str})

                internal_details['subject_name'] = str(subject_name.text)
                for j in range(len(marks)):
                    internal_details['sessional'+position[j][-1]] = str(marks[j].text)
                internals.append(internal_details)
                i = i + 1
            else:
                break
        self.all_data['internals'] = internals
        all_data['internals'] = internals
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
    user_details = {}
    internal_details = {}
    if response.text.find('Profile of') == -1:
        print "Invalid details"
    else:
        sem_obj = Semester(session, str(1))
        user_details = sem_obj.get_personal_details()
        sem_details = sem_obj.get_data()
        attendance_details = sem_obj.get_attendance()
        internal_details = sem_obj.get_internals()
        """for i in range(1, 1+8):
            try:
                sem_obj = Semester(session, str(i))
                sem_details['semester'+str(i)] = sem_obj.get_data()
                attendance_details['semester' + str(i)] =  sem_obj.get_attendance()
                attendance_details['semester' + str(i)] = sem_obj.get_personal_details()
                internal_details['semester' + str(i)] = sem_obj.get_internals()
            except AttributeError:
                break"""

    user_details_json = json.dumps(user_details, indent=4, sort_keys=True, ensure_ascii=False)
    f = open('user_details.json', 'w')
    f.write((user_details_json).encode('ascii', 'ignore')) 
    f.close()

    attendance_json = json.dumps(attendance_details, indent=4, sort_keys=True, ensure_ascii=False)
    f = open('attendance.json', 'w')
    f.write((attendance_json).encode('ascii', 'ignore')) # We need to figure out a better solution for this encoding issue. 
    f.close()

    details_json = json.dumps(sem_details, indent=4, sort_keys=True, ensure_ascii=False)
    f = open('data.json', 'w')
    f.write(str(details_json))
    f.close()

    internals_json = json.dumps(internal_details, indent=4, sort_keys=True, ensure_ascii=False)
    f = open('internal.json', 'w')
    f.write(str(internals_json))
    f.close()