import constants

base_url = 'http://websismit.manipal.edu/websis/control/StudentAcademicProfile'
url = base_url + '?productCategoryId=0905-TERM-'
base_url_details = 'http://websismit.manipal.edu/websis/control/'
url_details = base_url_details + 'ListCTPEnrollment?customTimePeriodId='

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
