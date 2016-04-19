import requests
from bs4 import BeautifulSoup
import json
from semester import Semester

class WebsisProfile(object):
    """docstring for WebsisProfile"""
    base_url = 'http://websismit.manipal.edu'
    login_url = base_url + '/websis/control/createAnonSession'

    current_sem_url = base_url + '/websis/control/StudentAcademicProfile'

    #HTML IDs to be used in _fetch_personal_details
    user_current_sem = 'ProfileTitle_productCategoryId_title'
    user_name_id = 'cc_ProfileTitle_name'
    user_section_id = 'cc_ProfileTitle_sectionCode'
    user_gender_id = 'ProfileSummary_gender_title'
    user_birth_date_id = 'ProfileSummary_birthDate_title'
    user_joining_year_id = 'ProfileSummary_customTimePeriodId_title'
    user_nationality_id = 'ProfileSummary_nationalityId_title'
    user_identification_table_id = 'listPartyIdentification_table'

    def __init__(self, registration_number, birth_date):
        self._all_data = {}
        payload = {}
        payload['idValue'] = registration_number
        payload['birthDate'] = birth_date
        session = requests.session()
        response = session.post(self.login_url, data = payload)
        #print registration_number, birth_date
        f = open('blah.html', 'w')
        f.write(response.text)
        f.close()
        if response.text.find('Profile of') == -1:
            print "Invalid details"
            #Should raise exception
        else:
            self.session = session
            html = response.text
            html = html.replace('\n', '')
            self._profile_soup = BeautifulSoup(html, 'lxml')
            self._fetch_profile()
            current_sem = self._all_data['profile']['current_sem']
            self.semesters = list('0' * int(current_sem))
            self.num_semesters = len(self.semesters)

    def _fetch_semester_details(self, semester):
        if int(semester) > self.num_semesters:
            self._all_data['semester' + semester] = {'Not found'}
            return
        elif self.semesters[int(semester)-1]!='0':
            return
        elif self.num_semesters == int(semester):
            self._fetch_current_semester(semester)
            return
        sem_obj = Semester(self.session, semester)
        self.semesters[int(semester)-1] = sem_obj
        sem_details = sem_obj.get_data()
        sem_key = 'semester' + semester
        self._all_data[sem_key] = {}
        self._all_data[sem_key]['details'] = sem_details[0]
        self._all_data[sem_key]['sub_details'] = sem_details[1]
        self._all_data[sem_key]['attendance'] = sem_obj.get_attendance()
        self._all_data[sem_key]['internals'] = sem_obj.get_internals()
        
    def _fetch_current_semester(self, semester):
        print "current_sem"
        sem_obj = Semester(self.session, semester, self.current_sem_url)
        sem_key = 'semester' + semester
        url = self.base_url + sem_obj._get_current_session_url()
        self._all_data[sem_key] = {}
        self._all_data[sem_key]['attendance'] = sem_obj.get_attendance(url)
        self._all_data[sem_key]['internals'] = sem_obj.get_internals()

    def _fetch_profile(self):
        user_details = {}
        soup = self._profile_soup
        if soup.find('span', {'id' : WebsisProfile.user_name_id})!=None:
            current_sem_tag = soup.find('span', {'id': self.user_current_sem})
            for _ in range(4):
                current_sem_tag = current_sem_tag.next_element
            tag = str(current_sem_tag.text)
            user_details['current_sem'] = [i for i in tag.split(' ') if i!= ''][-1]
            user_name = soup.find('span', {'id' : WebsisProfile.user_name_id})
            user_details['name'] = user_name.text.strip()
            user_section = soup.find('span', {'id' : WebsisProfile.user_section_id})
            user_details['section'] = user_section.text.strip('Section ');
            gender = soup.find('span', {'id' : WebsisProfile.user_gender_id})
            user_gender = gender.findNext('td')
            user_details['gender'] = user_gender.text.strip()
            birth_date = soup.find('span', {'id' : WebsisProfile.user_birth_date_id})
            user_birth_date = birth_date.findNext('td')
            user_details['birth_date'] = user_birth_date.text.strip()
            joining_year = soup.find('span', {'id' : WebsisProfile.user_joining_year_id})
            user_joining_year = joining_year.findNext('td')
            user_details['year_of_joining'] = user_joining_year.text.split('-')[0]
            nationality = soup.find('span', {'id' : WebsisProfile.user_nationality_id})
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
            identification_table = soup.find('table', {'id' : WebsisProfile.user_identification_table_id})
            user_identification_table = identification_table.find_all('td')
            user_registration_number = user_identification_table[1].text.strip()
            user_admission_number = user_identification_table[3].text.strip()
            user_roll_number = user_identification_table[5].text.strip()
            user_details['registration_number'] = user_registration_number
            user_details['admission_number'] = user_admission_number
            user_details['roll_number'] = user_roll_number

        self._all_data['profile'] = user_details


        

if __name__ == '__main__':
    reg_no = raw_input("Enter reg num: ")
    birth_date = raw_input("Enter birthdate: ")
    student = WebsisProfile(reg_no, birth_date)
    student._fetch_semester_details('5')
    print student._all_data
    #student_json = json.dumps(student._all_data, indent=4, sort_keys=True, ensure_ascii=False)
    #f = open('data.json', 'w')
    #f.write(str(student_json))
    #f.close()