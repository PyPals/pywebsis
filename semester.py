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
    url = 'http://websismit.manipal.edu/websis/control/StudentAcademicProfile'
    url += '?productCategoryId=0905-TERM-'

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

if __name__ == '__main__':
    url = "http://websismit.manipal.edu/websis/control/createAnonSession"
    payload = {}
    payload['idValue'] = raw_input("Enter reg num: ")
    payload['birthDate'] = raw_input("Enter birthDate: ")
    session = requests.session()
    response = session.post(url, data=payload)
    sem_details = {}
    if response.text.find('Profile of') == -1:
        print "Invalid details"
    else:
        for i in range(1, 1+8):
            try:
                sem_details['semester'+str(i)] = Semester(session, str(i)).get_data()
            except AttributeError:
                break
    details_json = json.dumps(sem_details, indent=4, sort_keys=True, ensure_ascii=False)
    f = open('data.json', 'w')
    f.write(str(details_json))
    f.close()