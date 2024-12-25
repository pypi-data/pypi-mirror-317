# -*- coding: utf-8 -*-
import os, datetime  # 내장모듈
import win32com.client  # pywin32의 모듈
import pywintypes

import youtil, pynal, jfinder  # xython 모듈
import basic_data

class mailmail:
	def __init__(self):
		self.xytime = pynal.pynal()
		self.xyre = jfinder.jfinder()
		self.util = youtil.youtil()

		self.vars = basic_data.basic_data()
		self.top_folder_obj = ""
		self.sub_folder_obj = ""

		self.outlook_program = win32com.client.dynamic.Dispatch('Outlook.Application')
		self.outlook = self.outlook_program.GetNamespace("MAPI")

		self.mail_properties = [
			'Subject', 'SenderName', 'Recipients', 'ReceivedTime', 'Body',
			'Importance', 'Categories', 'Attachments', 'HTMLBody', 'SentOn',
			'ConversationTopic', 'Importance', 'Sensitivity', 'Size',
			# ... 기타 원하는 속성 추가
		]

	def check_any_folder(self, input_value):
		"""
		폴더가 번호로 오는지 아니면 이름으로 입력값이 오는지에 따라서 폴더객체를 돌려준다
		:param input_value:
		:return:
		"""
		folder_object = None

		# 숫자가 들어왔을때는 폴더의 숫자로 인식
		if type(input_value) == type(123):
			#print("숫자가 들어왔을때는 폴더의 숫자로 인식")
			folder_object = self.outlook.GetDefaultFolder(input_value)
		# 문자일때
		elif type(input_value) == type("abc"):
			#print("문자일때")
			folder_no = self.check_folder_no(input_value)
			folder_object = self.outlook.GetDefaultFolder(folder_no)
		else:
			try:
				#폴더자체가 들어왔을때
				#print(input_value.__class__.__name__)
				if input_value.__class__.__name__ == 'CDispatch': #MAPIFolder
					#print("폴더자체가 들어왔을때")
					folder_object = input_value
			except:
				folder_object = input_value

		return folder_object

	def get_nea_latest_mail_list_in_input_folder(self, input_no=10):
		"""
		받은편지함에서 최신 n개메일을 갖고오는것

		:param input_no:
		:return:
		"""
		folder_object = self.outlook.GetDefaultFolder(6)
		mail_set =folder_object.Items

		mail_list = []
		mail_list.append(mail_set.GetFirst())
		for no in range(input_no-1):
			mail_list.append(mail_set.GetNext())
		return mail_list

	def check_element_name(self, input_value):
		"""
		일반적으로 사용하는 용어들을 확인하는 것
		:param input_value:
		:return:
		"""
		input_value = input_value.lower()
		if input_value in ["send", "sender", "보낸사람"]: result="SenderName"
		elif input_value in ["receivedtime", "받은시간", "임시", "보관함", "보관"]: result ="ReceivedTime"
		elif input_value in ["to" ]: result ="To"
		elif input_value in ["제목", "subject", "title"]: result ="Subject"
		elif input_value in ["body", "본문", "내용"]: result ="Body"
		elif input_value in ["bcc", "숨은참조"]: result ="Bcc"
		elif input_value in ["cc", "참조"]: result ="CC"
		elif input_value in ["attachments", "attachment", "첨부"]: result ="Attachments"
		else:  result =input_value
		return result

	def check_folder_no(self, input_value):
		"""
		폴더이름으로 번호를 갖고오는 것
		:param input_value:
		:return:
		"""
		if input_value in [6, "", "input", "received", "receive", "받은편지함", "받은 편지함", "받은"]: folder_no=6
		elif input_value in [5, "send", "sent", "보낸편지함", "보낸"]: folder_no=5
		elif input_value in [9, "promise", "예약", "임시", "보관함", "보관"]: folder_no =9
		elif input_value in [3, "삭제", "삭제함", "delete", "보관함", "보관"]: folder_no=3
		elif input_value in [16, "임시", "draft", "임시보관함", "temp"]: folder_no=16
		else:  folder_no =None
		return folder_no

	def check_sub_folder(self, input_sub_folder=""):
		"""
		sub_folder에 대한것을 선택하는것
		:param input_sub_folder:
		:return:
		"""
		if input_sub_folder == "":
			sub_folder_index = 0
			result = self.top_folder_obj.Folders[sub_folder_index]
		elif type(input_sub_folder) == type(123):
			sub_folder_index = input_sub_folder
			result = self.top_folder_obj.Folders[sub_folder_index]
		elif type(input_sub_folder) == type("abc"):
			if input_sub_folder in ["input", "default", "basic", "read"]:
				result = self.get_input_folder()
			elif input_sub_folder in ["write"]:
				result = self.get_promise_folder()
			else:
				sub_folder_index = input_sub_folder
				for no in range(self.top_folder_obj.count):
					this_name = self.top_folder_obj[no].Name
					if input_sub_folder == this_name:
						sub_folder_index = no
						break
				result = self.top_folder_obj.Folders[sub_folder_index]
		else:
			sub_folder_index = 0
			result = self.top_folder_obj.Folders[sub_folder_index]
		self.sub_folder_obj = result
		return result

	def check_top_folder(self, input_folder=""):
		"""
		top_folder에 대한것을 선택하는것

		:param input_sub_folder:
		:return:
		"""

		if input_folder == "":
			#기본자료는 input folder를 말한다
			result = self.outlook.Folders[0]
		elif type(input_folder) == type(123):
			top_folder_index = input_folder
			result = self.outlook.Folders[top_folder_index]
		elif type(input_folder) == type("abc"):
			if input_folder in ["default", "basic"]:
				result = self.get_input_folder()
			elif input_folder in ["write"]:
				result = self.get_promise_folder()
			else:
				top_folder_index = input_folder
				for no in range(self.outlook.Folders.count):
					this_name = self.outlook.Folders[no].Name
					if input_folder == self.outlook.Folders[no].Name:
						top_folder_index = no
						break
				result = self.outlook.Folders[top_folder_index]
		else:
			top_folder_index = 0
			result = self.outlook.Folders[top_folder_index]
		self.top_folder_obj = result
		return result

	def count_mail_in_folder(self, input_folder):
		"""
		폴더객체안의 메일 갯수

		:param input_folder:
		:return:
		"""
		checked_folder = self.check_any_folder(input_folder)
		result = checked_folder.Items.count
		return result

	def count_mail_in_folder_by_folder_name(self, input_folder_name):
		"""
		폴더이름안의 메일 갯수를 갖고온다

		:param input_folder_name:
		:return:
		"""
		folder_object = self.check_any_folder(input_folder_name)
		result = folder_object.Items.count
		return result

	def count_unread_mail_in_folder(self, input_folder):
		"""
		폴더객체안의 읽지않은 메일 갯수 확인

		:param input_folder:
		:return:
		"""
		# input_folder = mail.box.Items.count
		folder_object = self.check_any_folder(input_folder)
		mail_set = folder_object.Items.Restricts("[Unread] =True")
		result = mail_set.count
		return result

	def count_unread_mail_in_folder_by_folder_name(self, input_folder_name):
		"""
		 읽지않은 메일 갯수를 갖고온다

		:param input_folder_name:
		:return:
		"""
		folder_object = self.check_any_folder(input_folder_name)
		mail_set = folder_object.Items.Restricts("[Unread] =true")
		result = mail_set.count
		return result

	def count_unread_mail_in_input_folder(self):
		"""
		아웃룩에서 읽지않은 메일객체들을 돌려준다

		:return:
		"""
		folder_object = self.outlook.GetDefaultFolder(6)
		mail_set = folder_object.Items.Restricts("[Unread] =true")
		result = mail_set.count
		return result

	def data_all_properties_names_for_mail(self):
		"""
		매일객체의 속성들
		:return:
		"""

		result = self.vars["all_properties_list"]
		return result

	def delete_all_attached_file_in_one_mail(self, input_one_mail):
		for attachment in input_one_mail.Attachments:
			attachment.Delete()
		return input_one_mail

	def delete_bcc_in_one_mail(self, input_one_mail):
		input_one_mail.BCC = None
		return input_one_mail

	def delete_body_in_one_mail(self, input_one_mail, replace_text =""):
		input_one_mail.Body = replace_text
		return input_one_mail

	def delete_mail_in_folder_from_today_to_nea_day(self, input_folder, days=60):
		"""
		오늘기준으로 어떤 날짜 이전의 메일은 삭제하는 것

		:param input_folder:
		:param days:
		:return:
		"""
		folder_object = self.check_any_folder(input_folder)
		today = datetime.datetime.now()
		cutoff_date = today - datetime.timedelta(days=days)

		folder_object.Items.Sort("[ReceivedTime]", True)
		for one_mail in folder_object.Items:
			received_time = one_mail.ReceivedTime
			if received_time < cutoff_date:
				one_mail.Delete()

	def delete_mail_set(self, input_mail_set):
		"""
		입력으로 들어온 메일들을 삭제한다

		:param input_mail_set:
		:return:
		"""
		for one_mail in input_mail_set:
			one_mail.Delete()

	def delete_one_mail_from_mail_set(self, input_mail_set, input_no):
		"""
		입력으로 들어온 메일들을 삭제한다

		:param input_one_mail:
		:return:
		"""
		one_mail = input_mail_set[input_no-1]
		one_mail.Delete()

	def check_mail_list(self, input_mail_set):
		"""
		mail_set에는 두가지가 있다, 하나는 list형식의 자료와 다른하나는 maillitems형식이 있다

		:param input_mail_set:
		:return:
		"""
		if type(input_mail_set) == type([]):
			result = input_mail_set
		else:
			result = []
			#맨먼저 GetFirst부터 해야 한다
			result.append(input_mail_set.GetFirst())
			for no in range(input_mail_set.count-1):
				result.append(input_mail_set.GetNext())
		return result

	def filter_mail_set_as_body_by_jf_sql(self, input_mail_set, jf_sql):
		#어떤 폴더안에 찾고자 하는 이름이 같은 메일을 찾는것
		result = []
		#mails = input_folder.items
		#만약 mail_set이 list인지 아닌지를 확인한다
		mail_l1d = self.check_mail_list(input_mail_set)

		for index, one_mail in enumerate(mail_l1d):
			if self.xyre.search_all_with_jf_sql(jf_sql, one_mail.Body):
				print(one_mail.Subject)
				result.append(one_mail)
		return result

	def filter_element_in_mail_objects_as_dic_style(self, input_mail_objects, element = ["to", "subject", "sender", "body", "Cc",  "bcc"]):
		"""

		:param input_mail_objects:
		:param element:
		:return:
		"""
		l1d =[]
		for one in element:
			if one in ["to"]:  l1d.append("To")
			elif one in ["subject"]:  l1d.append("Subject")
			elif one in ["receive", "receivetime"]:  l1d.append("ReceivedTime")
			elif one in ["sender"]:  l1d.append("SenderName")
			elif one in ["attachment", "attach", "attachments"]:  l1d.append("Attachments")
			elif one in ["bcc"]:  l1d.append("BCC")
			elif one in ["body"]:  l1d.append("Body")
		result = []
		for one_mail in input_mail_objects:
			temp_dic = {}
			for ele in l1d:
				exec(f"temp_dic.{ele}= one_mail.{ele}")
				result.append(temp_dic)
		return result

	def filter_flag_for_mail_set(self, input_mail_set):
		"""
		플래그가 지정된 모든 이메일을 가져옵니다
		만약 색을 지정하고싶으면, FlagIcon의 값을 적용하면 됩니다

		:param input_mail_set:
		:return:
		"""

		result = []
		for one_mail in input_mail_set:
			if one_mail.FlagIcon != 0:
				result.append(one_mail)
		return result

	def get_10_latest_mail_set_in_input_folder(self):
		"""
		기본편지함에서 최신 10개의 메일 정보를 갖고오는 것

		:return:
		"""
		mail_list = self.get_nea_latest_mail_list_in_input_folder(10)
		return mail_list

	def get_all_attached_file_name_in_one_mail(self, input_one_mail):
		"""
		이메일 안에 들어있는 첨부화일의 이름들 알아보기

		:param input_mail:
		:return:
		"""
		result = []
		attachments = input_one_mail.Attachments
		num_attach = len([x for x in attachments])
		if num_attach > 0:
			for x in range(1, num_attach + 1):
				attachment = attachments.Item(x)
				result.append(attachment.FileName)
		return result

	def get_all_folder_information(self):
		result = self.get_information_for_all_folder()
		return result

	def get_all_information_for_one_mail(self, input_one_mail):
		result = self.get_information_for_one_mail(input_one_mail)
		return result

	def get_all_mail_in_input_folder(self):
		result = []
		folder_object = self.outlook.GetDefaultFolder(6)
		for one_mail in folder_object.Items:
			result.append(one_mail)

	def get_all_mail_set_in_folder(self, input_folder):
		"""

		:param input_folder:
		:return:
		"""
		folder_object = self.check_any_folder(input_folder)
		mail_set = folder_object.Items
		return mail_set

	def get_all_sub_folder_name_in_folder(self, input_folder_name):
		"""
		top 폴더의 하위폴더들의 이름을 돌려주는 것

		:param input_folder_name:
		:return:
		"""
		top_folder_index = self.get_top_folder_index_by_folder_name(input_folder_name)
		result = []
		for no in range(self.outlook.Folders[top_folder_index].Folders.count):
			sub_folder_name = self.outlook.Folders[top_folder_index].Folders[no].name
			result.append(sub_folder_name)
		return result

	def get_all_top_folder_name(self):
		"""
		가장 상위에있는 메일 폴더들의 이름

		:return:
		"""
		result = []
		for no in range(self.outlook.Folders.count):
			this_name = self.outlook.Folders[no].Name
			result.append([no, this_name])
		return result

	def get_attached_filename_all_for_one_mail(self, input_mail):
		result = self.get_all_attached_file_name_in_one_mail(input_mail)
		return result

	def get_basic_data_for_all_mail_set_in_input_folder_as_l2d(self):
		folder_object = self.outlook.GetDefaultFolder(6)
		mail_objects = folder_object.Items
		result = []
		for one_mail in mail_objects:
			result.append([one_mail.To, one_mail.Subject, one_mail.SenderName, one_mail.ReceivedTime])
			return result

	def get_basic_data_for_unread_mail_set_in_input_folder_as_l2d(self):
		folder_object = self.outlook.GetDefaultFolder(6)
		mail_objects = folder_object.Items.Restrict("[Unread]=true")
		result = []
		for one_mail in mail_objects:
			result.append([one_mail.To, one_mail.Subject, one_mail.SenderName, one_mail.ReceivedTime])
			return result

	def get_draft_folder(self):
		"""
		임시보관함의 메일박스
		:return:
		"""
		folder_object = self.outlook.GetDefaultFolder(16)
		return folder_object

	def get_empty_mail(self):
		list_1d = self.data_all_properties_names_for_mail()
		mail_dic = {}
		for one in list_1d:
			mail_dic[one]=None
		return mail_dic

	def get_folder_by_index(self, index_no=6):
		"""
		folder를 할지 folder_obj로 할지

		:param index_no:
		:return:
		"""
		folder_object = self.outlook.GetDefaultFolder(index_no)
		return folder_object

	def get_folder_by_top_n_sub_folder_index(self, top_folder_index=0, sub_folder_index=6):
		"""
		폴더의 이름으로 찾는것

		:param top_folder_index:
		:param sub_folder_index:
		:return:
		"""
		folder_object = self.outlook.Folders[top_folder_index].Folders[sub_folder_index]
		return folder_object

	def get_folder_by_top_n_sub_folder_name(self, top_folder_name="", sub_folder_name=""):
		"""
		top 폴더와 서브폴더이름으로 폴더 객체를 갖고온다

		:param top_folder_name:
		:param sub_folder_name:
		:return:
		"""
		top_folder_index = self.get_top_folder_index_by_folder_name(top_folder_name)
		sub_folder_index = self.get_sub_folder_index_by_folder_name(top_folder_index, sub_folder_name)
		result = self.outlook.Folders[top_folder_index].Folders[sub_folder_index]
		return result

	def get_information_for_all_folder(self):
		"""
		모든 기본폴더에 대한 정보

		:return:
		"""
		result = []
		for no in range(0, 50):
			try:
				temp = self.outlook.GetDefaultFolder(no)
				result.append([no, temp.name])
			except:
				pass
		return result

	def get_information_for_mail_set(self, input_mail_set):
		"""

		:param input_mail_set:
		:return:
		"""
		result = []
		for one_mail in input_mail_set:
			temp = self.get_information_for_one_mail(one_mail)
			result.append(temp)
		return result

	def get_information_for_nea_mail_in_folder(self, input_folder, limit_no=0):
		"""
		폴더 객체안의 모든 메세지에대한 정보를 리스트+사전 형태로 만든다

		:param input_folder:
		:param limit_no:
		:return:
		"""
		result = []
		mails = input_folder.Items
		mails.Sort("ReceivedTime", True)
		one_mail = mails.GetFirst()
		total_no = 1
		for no in range(input_folder.Items.count):
			temp = self.get_information_for_one_mail(one_mail)
			one_mail = mails.GetNext()
			result.append(temp)
			if limit_no:
				if limit_no == total_no:
					break
			total_no = total_no + 1
		return result

	def get_all_properties_for_one_mail(self, input_mail):
		"""
		한개의 메일에 대한 모든 정보를 돌려주는 것

		:param input_mail:
		:return:
		"""

		result = self.util.get_all_properties_for_object(input_mail)
		return result

	def get_major_information_for_one_mail(self, input_mail):
		"""
		한개의 메일에 대한 모든 정보를 돌려주는 것

		:param input_mail:
		:return:
		"""
		properties = [
			'Subject', 'SenderName', 'Recipients', 'ReceivedTime', 'Body',
			'Importance', 'Categories', 'Attachments', 'HTMLBody', 'SentOn',
			'ConversationTopic', 'Importance', 'Sensitivity', 'Size',
		]

		result_dic = {}
		for one in properties:
			try:
				value = getattr(input_mail, one)
				result_dic[one] = value
			except:
				result_dic[one] = None
		return result_dic

	def get_information_for_one_mail(self, input_mail):
		"""
		한개의 메일에 대한 모든 정보를 돌려주는 것

		:param input_mail:
		:return:
		"""


		abc = self.util.get_all_properties_for_object(input_mail)
		print(abc)

		for one in abc:
			try:
				if one[0:2] != "__":
					value = getattr(input_mail, one)
					print("one 속성", one, " ==> ", value)
			except:
				pass

	def get_input_folder(self):
		"""
		기본 받은편지함 객체

		:return:
		"""
		folder_object = self.outlook.GetDefaultFolder(6)
		return folder_object

	def get_mail_set_for_input_folder(self):
		"""
		기본 받은편지함 객체

		:return:
		"""
		result = self.outlook.GetDefaultFolder(6).Items
		return result

	def get_mail_box_by_top_n_sub_folder_name(self, top_folder_name="", sub_folder_name=""):
		# mailmail
		# top 폴더와 서브폴더이름으로 폴더 객체를 갖고온다
		top_folder_index = self.get_top_folder_index_by_folder_name(top_folder_name)
		sub_folder_index = self.get_sub_folder_index_by_folder_name(top_folder_index, sub_folder_name)
		result = self.outlook.Folders[top_folder_index].Folders[sub_folder_index]
		return result

	def get_mail_obj_in_folder_obj_between_date(self, input_folder, dt_obj_from, dt_obj_to):
		result = self.get_mail_set_in_folder_between_date(input_folder, dt_obj_from, dt_obj_to)
		return result

	def get_mail_obj_in_folder_obj_from_index_day(self,input_folder, input_day_no ):
		result = self.get_mail_set_in_folder_from_today_to_day_no(input_folder, input_day_no)
		return result

	def get_mail_object_between_two_date_in_input_folder(self, input_folder, start_date, end_date,  sort_by="") :
		dt_obj_from =self.xytime.change_anytime_to_dt_obj(start_date)
		dt_obj_to =self.xytime.change_anytime_to_dt_obj(end_date)
		dt_obj_to = dt_obj_to + datetime.timedelta(days=1)
		mails =self.get_sorted_mail_set_for_input_folder(input_folder, sort_by)
		aaa = "[ReceivedTime] >= '" + dt_obj_from.strftime("%Y-%m-%d %H:%M") + "' AND [ReceivedTime] < '" + dt_obj_to.strftime("%Y-%m-%d %H:%M") + "'"
		result = mails.Restrict(aaa)
		return result

	def get_mail_set_for_today_in_input_folder(self):
		"""
		받은편지함의 자료를 읽어서 새로운것만 제목보여주기

		:return:
		"""
		folder_object = self.get_input_folder()

		result = self.get_mail_set_in_folder_from_today_to_day_no(folder_object, 1)
		return result

	def get_mail_set_in_folder_between_date(self, input_folder, dt_obj_from, dt_obj_to):
		"""
		날짜사이의 메일 객체들을 갖고오는것

		:param input_folder: 메일박스
		:param dt_obj_from: 시작날짜 (2023-10-1)
		:param dt_obj_to: 종료날짜 (2023-10-3)
		:return:
		"""
		dt_obj_from = self.xytime.change_anytime_to_dt_obj(dt_obj_from)
		dt_obj_to = self.xytime.change_anytime_to_dt_obj(dt_obj_to)
		# 끝날묘포함하려면, 1 일을 더 더해줘야한다
		# #즉，2023-1-1 일 0 시 0 분 0 초를 넣어주는것과 같으므로, 2023-01-02 일 0 시 0 분 0 초로 하면 1 월 1 일의 모든 자료가 다 확인되는 것이다
		dt_obj_to = dt_obj_to + datetime.timedelta(days=1)
		# 폴더객체안의 받은 날짜사이에 들어온 메세지만 갖고오는것
		mails = input_folder.Items
		# 제일 최근에 받은즉，제일 받은시간이 늦은것을 기준으로 정렬
		mails.Sort("ReceivedTime", True)
		print(dt_obj_from.strftime("%Y/%m/%d"))
		result = mails.Restrict("[ReceivedTime] >= '" + dt_obj_from.strftime(
			"%Y-%m-%d %H:%M") + "' AND [ReceivedTime] <= '" + dt_obj_to.strftime("%Y-%m-%d %H:%M") + "'")
		return result

	def sort_for_mail_set_by_input_property(self, mail_set, input_property, desending=True):
		result = mail_set.Sort(input_property, desending)
		return result

	def sort_for_mail_list_by_input_property(self, mail_list, input_property):
		result = []
		new_mail_list = []
		for one_mail in mail_list:
			value = getattr(one_mail, input_property)
			new_mail_list.append([value, one_mail])


		sorted_l2d = self.util.sort_list_2d_by_index(new_mail_list, 0)

		for l1d in sorted_l2d:
			result.append(l1d[1])
		return result

	def get_mail_set_in_folder_by_from_to(self, input_mail_folder_obj, sender_name, receiver):
		"""
		폴더객체안의 날짜기준으로 정렬됭ㄴ자료에서, 최근에 들어온 몇개의 메세지만 갖고오는것

		:param input_mail_folder_obj:
		:param from_no:
		:param to_no:
		:return:
		"""
		mail_set = input_mail_folder_obj.Items
		if sender_name and receiver:
			result = mail_set.Restrict("[SenderName] = '" + sender_name + "' AND [To] = '" + receiver+"'")
		elif sender_name and not receiver:
			result = mail_set.Restrict("[SenderName] = '" + sender_name + "'")
		elif not sender_name and receiver:
			result = mail_set.Restrict("[To] = '" + receiver+"'")

		return result

	def get_mail_set_in_folder_from_today_to_day_no(self, input_folder, input_day_no):

		result = []
		dt_obj_to = self.xytime.get_dt_obj_for_today()
		ymd_list_today = self.xytime.get_ymd_list_for_dt_obj(dt_obj_to)
		mails = input_folder.Items
		mails.Sort("ReceivedTime", True)
		for one_mail in mails:
			dt_obj_rt = self.xytime.change_any_text_time_to_dt_obj(one_mail.ReceivedTime)
			ymd_list_rt = self.xytime.get_ymd_list_for_dt_obj(dt_obj_rt)
			if ymd_list_today == ymd_list_rt:
				result.append(one_mail)
		return result

	def get_mail_set_in_folder_from_today_to_day_no_old(self, input_folder, input_day_no):
		"""
		오늘을 기준으로 입력한 몇일전까지의 메일을 갖고오는것

		:param input_folder: 메일박스
		:param input_day_no: 몇일전까지일지 넣는 숫자
		:return:
		"""
		dt_obj_to = self.xytime.get_dt_obj_for_today()
		# 끝날포포함하려면, 1 일을 더 더해줘야한다
		# 즉, 2023-1-1 일 0 시 0 분 0 초를 넣어주는것과 같으므로, 2023-01-02 일 0 시 0 분 0 초로 하면 1 월 1 일의 모든 자료가 다 확인되는 것이다
		dt_obj_from = dt_obj_to - datetime.timedelta(days=input_day_no)
		# 폴더객체안의 받은 날짜사이에 들어온 메세지만 갖고오는것
		mails = input_folder.Items
		# 제일 최근에 받은것, 즉, 제일 받은시간이 늦은것을 기준으로 정렬
		mails.Sort("ReceivedTime", True)
		result = mails.Restrict("[ReceivedTime] >=	'" + dt_obj_from.strftime('%Y-%m-%d %H:%M') + "'")
		return result

	def get_mail_set_in_folder_on_yyyymmdd(self, input_folder, input_yyyy_mm_dd):
		"""
		특정 날짜의 메일을 얻는 것
		"""

		folder_object = self.check_any_folder(input_folder)
		dt_obj_to = self.xytime.change_anytime_to_dt_obj(input_yyyy_mm_dd)
		dt_obj_to_1 = dt_obj_to + datetime.timedelta(days=1)
		result = folder_object.Items.Restrict("[ReceivedTime] >= '" + dt_obj_to.strftime('%Y-%m-%d %H:%M') + "' AND [ReceivedTime] < '" + dt_obj_to_1.strftime('%Y-%m-%d %H:%M') + "'")
		return result

	def get_nea_latest_mail_in_folder(self, input_folder, input_no=10):
		folder_object = self.check_any_folder(input_folder)
		mails =folder_object.Items

		mails.Sort("ReceivedTime", True)
		result = list(mails)[:input_no]
		return result

	def get_nea_latest_mail_list_in_input_folder_rev1(self, input_no=10):
		"""
		기본 입력 폴더의 최근 갯수의 메일 자료를 갖고온다

		:param input_no:
		:return:
		"""
		folder_object = self.outlook.GetDefaultFolder(6)

		result = []
		mails = folder_object.Items
		result.append(mails.GetFirst())
		for no in range(input_no-1):
			result.append(mails.GetNext())
		return result

	def get_nea_mail_set_in_folder_sort_by_received_time(self, folder_object, input_no=5):
		result = []
		mail_set = folder_object.Items
		mail_set.Sort("ReceivesTime", True)
		one_mail = mail_set.GetFirst()

		for no in range(input_no):
			one_mail = mail_set.GetNext()
			result.append(one_mail)
		return result

	def get_nea_mail_set_in_input_folder(self, input_no=5):
		folder_object = self.check_any_folder(input_no)
		result = self.get_nea_mail_set_in_folder_sort_by_received_time(folder_object, input_no)
		return result

	def get_nth_mail_in_folder(self, input_folder_no, index_no=6):
		"""

		:param index_no:
		:return:
		"""
		folder_object = self.check_any_folder(input_folder_no)
		all_items = folder_object.Items
		result = all_items[index_no-1]
		return result

	def get_nth_mail_set_in_folder_sort_by_date(self, input_folder, to_no=25, from_no=0):
		"""
		폴더객체안의 날짜기준으로 정렬됭ㄴ자료에서, 최근에 들어온 몇개의 메세지만 갖고오는것

		:param input_folder:
		:param from_no:
		:param to_no:
		:return:
		"""
		mails = input_folder.Items
		mails.Sort("ReceivedTime", True)
		result = list(mails)[from_no:to_no]
		return result

	def get_one_mail_by_entry_id(self, entry_id):
		# EntryID 를 사용하여 메일 항목 가져오기
		mail_item = self.outlook.GetItemFromID(entry_id)
		return mail_item

	def get_one_mail_by_no_in_folder(self, input_folder, input_no, latest_ok = True):
		#특정폴더안의 메일객체를 돌려주는 것
		folder_object =self.check_any_folder(input_folder)
		mail_set = folder_object.Items
		if latest_ok:
			mail_set.Sort("ReceivedTime", True)
		result = list(mail_set)[input_no -1]
		return result

	def get_opened_mail(self, input_no = 1):
		mail = self.outlook_program.ActiveExplorer().Selection.Item(input_no)
		return mail

	def get_mail_set_for_selected(self):
		"""
		아웃록에서 어떤때를 보면, 선택한 자료를 확인할 필요가 있다
		이럴때 사용하기 힘든 것이다
		"""
		mail_s = self.outlook_program.ActiveExplorer().Selection
		#print(mail_s.Count)

		"""
		 Set myOlExp = Application.ActiveExplorer 
		 Set myOlSel = myOlExp.Selection 
		 
		 For x = 1 To myOlSel.Count 
		   MsgTxt = MsgTxt & myOlSel.Item(x).SenderName & ";" 
		 Next x 
		 
		"""
		return mail_s

	def get_promise_folder(self):
		"""
		기본적인 보관함 폴더

		:return:
		"""
		folder_object = self.outlook.GetDefaultFolder(9)
		return folder_object

	def get_sorted_mail_set_for_input_folder(self, input_folder, sort_by=""):
		folder_object = self.check_any_folder(input_folder)
		mails =folder_object.Items
		gijun = self.check_element_name(sort_by)
		mails.Sort(gijun, True)
		return mails

	def get_sub_folder_by_top_n_sub_folder_name(self, top_folder_name="", sub_folder_name=""):
		"""
		top 폴더의 index 와 원하는 폴더 번호를 넣으면 폴더 객체를 돌려준다

		:param top_folder_name:
		:param sub_folder_name:
		:return:
		"""
		top_folder_index = self.get_top_folder_index_by_folder_name(top_folder_name)
		print(top_folder_index)
		sub_folder_index = self.get_sub_folder_index_by_folder_name(top_folder_index, sub_folder_name)
		print(sub_folder_index)
		result = self.outlook.Folders[top_folder_index].Folders[sub_folder_index]
		return result

	def get_sub_folder_index_by_folder_name(self, top_folder_name="", sub_folder_name=""):
		"""
		폴더이름으로 폴더 객체를 만들고 확인하는 것

		:param self:
		:param top_folder_name:
		:param sub_folder_name:
		:return:
		"""
		top_folder_index = self.get_top_folder_index_by_folder_name(top_folder_name)
		result = ""
		if type(sub_folder_name) == type(123):
			result = sub_folder_name
		else:
			sub_folder_data = self.get_all_sub_folder_name_in_folder(top_folder_index)
			for sub_1 in sub_folder_data:
				if sub_1[2] == sub_folder_name:
					result = sub_1[1]
					break
		return result

	def get_sub_folder_names(self, folder_name):
		"""
		입력폴더의 하위 폴더들의 이름을 갖고오는 것

		:param folder_name:
		:return:
		"""
		result = []
		for no in range(self.outlook.Folders[folder_name].Folders.count):
			this_name = self.outlook.Folders[folder_name].Folders[no].name
			result.append([folder_name, no, this_name])
		return result

	def get_subject_set_for_unread_mails_in_input_folder(self):
		"""
		받은 편치함의 자료를 읽어서 새로운것만 제목보여주기

		:return:
		"""
		mail_set = self.get_unread_mail_set_in_input_folder()
		item_data_list2d = self.get_information_for_mail_set(mail_set)
		return item_data_list2d

	def get_top_folder_by_index(self, top_folder_index=0):
		"""
		top 폴더의 index 와
		원하는 폴더 번호를 넣으면 폴더 객체를 돌려준다

		:param top_folder_index:
		:return:
		"""
		result = self.outlook.Folders[top_folder_index]
		return result

	def get_top_folder_index_by_folder_name(self, folder_name=""):
		"""
		폴더이름을 입력하면 index 를 돌려주는것

		:param folder_name:
		:return:
		"""
		result = folder_name
		if type(folder_name) != type(123):
			top_folder_data = self.get_all_top_folder_name()
			for top_1 in top_folder_data:
				if top_1[1] == folder_name:
					result = top_1[0]
					break
		return result

	def get_unique_id_for_mail_set(self, input_mail_set):
		result = []
		for one_mail in input_mail_set:
			result.append(one_mail.EntryID)
		return result

	def get_unread_mail_set_for_input_mail_set(self, input_mail_set):
		"""
		읽지않은 메일객체를 갖고온다

		:param input_mail_set:
		:return:
		"""
		result = input_mail_set.Restrict("[Unread] =true")
		return result

	def get_unread_mail_set_in_folder(self, input_folder):
		"""
		입력한 폴데객체의 읽지 않은 메일을 객체로 돌려준다

		:param input_folder:
		:return:
		"""
		result = input_folder.Items.Restrict("[Unread] =true")
		return result

	def get_unread_mail_set_in_folder_index(self, input_index):
		folder_object = self.outlook.GetDefaultFolder(input_index)
		result = folder_object.Items.Restrict("[Unread]=True")
		return result

	def get_unread_mail_set_in_input_folder(self):
		folder_object = self.outlook.GetDefaultFolder(6)
		result = folder_object.Items.Restrict("[Unread]=True")
		return result

	def get_unread_mail_list_in_input_folder(self):
		result = []
		folder_object = self.outlook.GetDefaultFolder(6)
		for one_mail in folder_object.Items.Restrict("[Unread]=True"):
			result.append(one_mail)
		return result

	def make_html_inline_text(self, input_text, bold, size, color):
		text_style = '<p style="'
		aaa = ";"
		if bold:
			if text_style != '<p style= "': aaa = ''
			text_style = text_style + aaa + "font-weight: bold;"
		if size:
			if text_style != '<p style= "': aaa = ''
			text_style = text_style + aaa + "font-size:" + str(size) + "px;"
		if color:
			if text_style != '<p style= "': aaa = ''
			text_style = text_style + aaa + "color: " + str(color)+ ";"
		text_style = text_style + '">' + input_text + "</p>"
		result = text_style
		return result

	def make_n_send_by_input_dic(self, input_dic):
		new_mail = self.outlook.CreateItem(0)
		new_mail.To = input_dic["to"]
		new_mail.Subject = input_dic["subject"]
		new_mail.Body = input_dic["body"]
		# attachment = "첨부화일들"
		# new_mail.Attachments.Add(attachment)
		new_mail.Send()

	def make_table(self, style, title_list, data_list2d):
		table_style_id = ""
		if style != "":
			table_style_id = " id="+'"' + style + '"'

		table_html = "<table" + table_style_id + ">"
		for one in title_list:
			table_html = table_html + f"<th>{one}</th>"
		for list_1d in data_list2d:
			table_html = table_html + "<tr>"
			for value in list_1d:
				if value == None:
					value = ""
				if isinstance(value, pywintypes.TimeType):
					value = str(value)[:10]
				table_html = table_html + f"<td>{value}</td>"
			table_html = table_html + "</tr>"
		table_html = table_html + "</table>"
		return table_html

	def move_mail_set_to_folder(self, input_mail_set, target_folder):
		"""
		메일 객체를 다른 폴더로 옮기는 것

		:param input_mail_set:
		:param target_folder:
		:return:
		"""
		for one_mail in input_mail_set:
			one_mail.Move(target_folder)

	def move_one_mail_to_draft_folder(self, input_one_mail):
		# 어떤 메일 객체 1개가 오면, 그것을 draft메일로 이동시키는 것
		#어떤 메일을 reply하는 기능을 만들어봅니다
		folder_object = self.outlook.GetDefaultFolder(16)
		input_one_mail.Move(folder_object)

	def move_one_mail_to_folder(self, input_mail, target_folder):
		"""
		메일 객체를 다른 폴더로 옮기는 것

		:param input_mail:
		:param target_folder:
		:return:
		"""
		input_mail.Move(target_folder)

	def move_spam_mail_set_to_folder(self, input_folder, input_word_list, move_to_folder):
		#*****
		result = []
		mails = self.get_all_mail_set_in_folder(input_folder)
		for one_mail in mails:
			for one_word in input_word_list:
				if one_word in one_mail.Subject:
					one_mail.Move(move_to_folder)

	def new_one_mail_as_empty(self):
		"""
		빈 메일객체를 하나 만든것

		:return:
		"""
		new_mail = self.outlook_program.CreateItem(0)
		new_mail.To = "to"
		new_mail.Subject = "subject"
		new_mail.Body = "body"
		return new_mail

	def new_one_mail_by_basic_data_at_draft_folder(self, to="", subject="", body="", cc=""):
		folder_object = self.outlook.GetDefaultFolder(16)
		new_mail = self.outlook_program.CreateItem(0)

		if to: new_mail.To = to
		if subject:new_mail.Subject = subject
		if body: new_mail.HTMLbody = body
		if cc : new_mail.CC = cc
		new_mail.Move(folder_object)

	def new_one_mail_by_dic_type(self, input_dic):
		# mailmail
		new_mail = self.outlook_program.CreateItem(0)
		new_mail.To = input_dic["To"]
		new_mail.Subject = input_dic["Subject"]
		new_mail.Body = input_dic["Body"]
		if "Attachments" in input_dic.keys():
			attachment = input_dic["Attachments"]
			new_mail.Attachments.Add(attachment)
		return new_mail

	def new_one_mail_with_subject_body_attachment(self, to, subject="", body="", attachments=None):
		"""
		새로운 메일 보내기

		:param to: 수신인
		:param subject: 제목
		:param body: 내용
		:param attachments: 첨부물
		:return:
		"""
		new_mail = self.outlook_program.CreateItem(0)
		new_mail.To = to
		new_mail.Subject = subject
		new_mail.Body = body
		if attachments:
			for num in range(len(attachments)):
				new_mail.Attachments.Add(attachments[num])
		return new_mail

	def new_sub_folder(self, parent_folder, new_sub_folder_name):
		parent_folder.Folders.Add(new_sub_folder_name)

	def print_mail_set_for_basic_datas_with_easy_format(self, input_mail_set):

		try:
			for one_mail in input_mail_set:
				temp = []
				temp.append(one_mail.SenderName)
				to_list = (one_mail.To).split(";")
				temp.append(str(to_list[0]) + " 외 " + str(len(to_list) - 1) + "명")
				temp.append(self.xytime.change_dt_obj_to_format_time_as_input_format(one_mail.ReceivedTime))
				if len(one_mail.Subject) > 20:
					temp.append(one_mail.Subject[:17] + "...")
				else:
					temp.append(one_mail.Subject)
				print(temp)
		except:
			one_mail = input_mail_set.GetFirst()
			for no in range(input_mail_set.count):
				temp = []
				temp.append(one_mail.SenderName)
				to_list = (one_mail.To).split(";")
				temp.append(str(to_list[0]) + " 외 " + str(len(to_list) - 1) + "명")
				temp.append(self.xytime.change_dt_obj_to_format_time_as_input_format(one_mail.ReceivedTime))
				if len(one_mail.Subject) > 20:
					temp.append(one_mail.Subject[:17] + "...")
				else:
					temp.append(one_mail.Subject)
				print(temp)
				one_mail = input_mail_set.GetNext()

	def print_mail_set_for_basic_datas(self, input_mail_set):

		try:
			for one_mail in input_mail_set:
				temp = []
				temp.append(one_mail.SenderName)
				to_list = (one_mail.To).split(";")
				temp.append(str(to_list[0]) + " 외 " + str(len(to_list) - 1) + "명")
				temp.append(self.xytime.change_dt_obj_to_format_time_as_input_format(one_mail.ReceivedTime))
				temp.append(one_mail.Subject)
				print(temp)
		except:
			one_mail = input_mail_set.GetFirst()
			for no in range(input_mail_set.count):
				temp = []
				temp.append(one_mail.SenderName)
				to_list = (one_mail.To).split(";")
				temp.append(str(to_list[0]) + " 외 " + str(len(to_list) - 1) + "명")
				temp.append(self.xytime.change_dt_obj_to_format_time_as_input_format(one_mail.ReceivedTime))
				temp.append(one_mail.Subject)
				print(temp)
				one_mail = input_mail_set.GetNext()

	def print_mail_set_one_by_one(self, input_mail_set):
		for one_mail in input_mail_set:
			print(one_mail.SenderName, one_mail.ReceivedTime, one_mail.Subject)
			#one_mail.SenderName
			#one_mail.ReceivedTime
			#one_mail.To
			#one_mail.Subject
			#one_mail.Body

	def reply_one_mail(self, input_one_mail, input_text):
		"""
		자동응답 기능

		:param input_one_mail:
		:return:
		"""
		folder_object = self.outlook.GetDefaultFolder (16)
		reply = input_one_mail.ReplyAll()
		reply.Body = input_text + reply.Body
		reply.Move (folder_object)

	def reply_one_mail_and_save_to_draft_folder(self, old_mail, addtional_title="Re: ", addtional_body="", no_old_title = False, no_old_body =  False):
		one_mail = self.get_information_for_one_mail(old_mail)
		reply= one_mail.Reply()
		if no_old_title: one_mail. Subject = ""
		if no_old_body: reply.Body =""
		reply.Subject = addtional_title + one_mail.Subject
		reply.Body = addtional_body +"\n\n"  +  reply. Body
		self.move_one_mail_to_draft_folder(reply)

	def sample_001(self):
		"""
		받은편지함의 오늘날짜의 메일들에서,
		첨부자료가 있는것들을 특정 폴더안에 앞부분에 이름을 덧붙여서 저장하는 것이다
		"""
		yyyy_mm_dd = self.xytime.get_today_as_yyyy_mm_dd_style()
		mails = self.get_mail_set_for_today_in_input_folder()
		for mail in mails:
			self.save_attached_file_at_path(mail, "D:/__aaa/", str(yyyy_mm_dd) + "_")
		self.print_mail_set_one_by_one(mails)

	def sample_002(self):
		"""
		기준이되는 화일의 이름을 바꿔서, 메일에 첨부해서 보내는 것이다
		"""

		util = youtil.youtil()
		file_name = "ddd.xlsx"
		new_file_name = "20240514_"+file_name
		util.copy_file("D:/__aaa/"+file_name, "D:/__aaa/"+new_file_name)
		attach_file = ["D:/__aaa/"+new_file_name]
		aaa = self.new_one_mail_with_subject_body_attachment("sjp@lotte.net", "[가나다]/회신요망", "ㄴㅇㄹㄴㅇㄹㄴㅇㄹ<br>ㄴ ㄴㅇㄹㄴㅇㄹㄴㅇ", attach_file)
		self.send_one_mail(aaa)

	def sample_003(self):
		"""
		테스트를 위한것
		전체메일 갯수등의 자료들을 보여주는 것

		:return:
		"""

		outlook = win32com.client.Dispatch("Outlook.Application")
		namespace = outlook.GetNamespace("MAPI")

		input_folder = namespace.GetDefaultFolder(6)

		for i in input_folder.Items:
			print(i.subject)
			print(str(i.Sender) + '\t: ' + i.SenderEmailAddress)

		print("전체 메일 개수 :" + str(input_folder.Items.count))
		print("읽지않은 메일 개수 :" + str(input_folder.UnReadItemCount))
		print("읽은 메일 개수 :" + str(input_folder.Items.count - input_folder.UnReadItemCount))

		print(namespace.Folders[0].Name)
		print(namespace.Folders[1].Name)
		print(namespace.Folders[2].Name)

		root_folder = namespace.Folders.Item(1)
		for folder in root_folder.Folders:
			print("폴더이름 ==> ", folder.Name)
			print("갯수 ==> ", folder.Items.count)

		outlook = win32com.client.Dispatch("Outlook.Application")
		namespace = outlook.GetNamespace("MAPI")
		root_folder = namespace.Folders.Item(1)
		subfolder = root_folder.Folders['All'].Folders['Main Folder'].Folders['Subfolder']
		mails = subfolder.Items

	def save_attached_file_at_path(self, input_mail, path="", surname=""):
		"""
		# 이메일 안에 들어있는 첨부화일을 다른 이름으로 저장하기
		# path : 저장할 경로，없으면 현재의 위치
		# surname : 기존이름앞에 붙이는 목적，없으면 그대로
		"""
		attachments = input_mail.Attachments
		num_attach = len([x for x in attachments])
		if num_attach > 0:
			for x in range(1, num_attach + 1):
				attachment = attachments.Item(x)
				old_name_changed = surname + attachment.FileName
				attachment.SaveAsFile(os.path.join(path, old_name_changed))

	def select_folder(self, input_folder):
		folder_object = self.check_any_folder(input_folder)
		folder_object.Select()

	def select_text_for_one_mail_from_1_to_2(self, input_one_mail, start_no=0, end_no=20):
		aaa = input_one_mail.Getlnspector.WordEditor.Range(Start=start_no, End=end_no).Select()

	def send_one_mail(self, mail_object):
		mail_object.Send()

	def send_one_mail_on_datetime(self, input_one_mail, dt_obj):
		#지정된 시간에 메일 보내기
		# 2024년 1월 1일 오후 3시
		#dt obj = datetime.datetime(2024, 1, 1, 15, 0, 0)
		input_one_mail.DeliveryTime = dt_obj
		input_one_mail.Save()
		input_one_mail.Send()

	def set_attachment_in_one_mail(self, input_one_mail, file_full_list):
		"""
		메일에 첨부화일을 추가하는 것
		:param input_one_mail:
		:param file_full_list:
		:return:
		"""
		for one_file in file_full_list:
			input_one_mail.Attachments.Add(one_file)
		return input_one_mail

	def set_display_on(self, input_mail):
		input_mail.Display(True)

	def version(self):
		result = """ 2023-04-10 : 이름을 포함한, 많은 부분을 고침
	            default folder: outlook 에서 기본으로 설정되고 관리되는 기준의 폴더들
	            아웃룩의 메일은 item 과 folder 로 구성이 되어있다"""
		return result

	def xyprint(self, input_value, limit_no=20):
		#print할때 너무 많은 글자가 나오면 않되기 때문에 글자수를 줄여주면서 끝에 ~~을 넣어서 프린트해주는 기능이다
		if type(input_value) == type([]):
			result = []
			for one in input_value:
				if len(str(one)) > limit_no:
					result.append(str(one))[:limit_no] + str("~~")
		elif type(input_value) == type({}):
			result = {}
			for one in input_value.keys():
				if len(str(input_value[one])) > limit_no:
					result[one] = str(input_value[one])[:limit_no] + str("~~")
		elif type(input_value) == type("abc"):
			if len(input_value) > limit_no:
				result = input_value[:limit_no] + str("~~")
		else:
			result = input_value
		return result

	def select_nth_mail_in_folder(self, input_folder_value=6, input_no=1):
		#folder_object = self.check_any_folder(input_folder_value)
		current_folder = self.outlook.GetDefaultFolder (input_folder_value)
		#mail_set = folder_object.Items
		#one_mail = mail_set[input_no]
		#print()

		#one_mail = mail_set[input_no]  # 인덱스는 0부터 시작하므로 두 번째 메일은 인덱스 1
		#one_mail.GetConversation()
		# 폴더에 메일이 있는지 확인
		if current_folder.Items.Count > 0:
			# 첫 번째 메일 선택
			all_mail_set = current_folder.Items
			#ddd = list(all_mail_set)
			#all_mail_set.item(2).select()
			#first_email.Select()
			print("첫 번째 메일이 선택되었습니다.", all_mail_set.Count)
		else:
			print("현재 폴더에 메일이 없습니다.")

	def get_latest_mail_items_at_input_mail_box_in_outlook(self, input_no=5):
		result = []
		input_folder = self.namespace.GetDefaultFolder(6)
		messages = input_folder.Items
		messages.Sort("ReceivedTime", True)
		message = messages.GetFirst()

		for no in range(input_no):
			print(message.Subject)
			message = messages.GetNext()
			result.append(message)
		return result

	def outlook_email_check_test_01(self, ):
		"""
			아웃룩익스프레스 테스트 하는것
			"""
		outlook = win32com.client.Dispatch("Outlook.Application")
		namespace = outlook.GetNamespace("MAPI")

		input_folder = namespace.GetDefaultFolder(6)
		print("폴더이름 ==> ", input_folder.Name)

		for i in input_folder.items:
			print(i.subject)
			print(str(i.Sender) + "\t: " + i.SenderEmailAddress)

		print("전체 메일 개수 :" + str(input_folder.items.count))
		print("읽지않은 메일 개수 :" + str(input_folder.UnReadItemCount))
		print("읽은 메일 개수 :" + str(input_folder.items.count - input_folder.UnReadItemCount))

		print(namespace.Folders[0].Name)
		print(namespace.Folders[1].Name)
		print(namespace.Folders[2].Name)

		root_folder = namespace.Folders.Item(1)
		for folder in root_folder.Folders:
			print("폴더이름 ==> ", folder.Name)
			print("갯수 ==> ", folder.items.count)

		outlook = win32com.client.Dispatch("Outlook.Application")
		namespace = outlook.GetNamespace("MAPI")
		root_folder = namespace.Folders.Item(1)
		subfolder = root_folder.Folders['All'].Folders['Main Folder'].Folders['Subfolder']
		messages = subfolder.Items

	def read_basic_input_mails_data_with_outlook(self):
		input_folder = self.namespace.GetDefaultFolder(6)
		for message in input_folder.Items:
			print(message.Subject)

	def get_one_mail_information_in_outlook(self, one_email):
		result = {}
		result["sender"] = one_email.SenderName
		result["receiver"] = one_email.To
		result["title"] = one_email.Subject
		result["time"] = one_email.ReceivedTime
		result["body"] = one_email.Body
		return result

	def read_total_unread_mail_no_with_outlook(self, folder_name):
		input_folder = self.namespace.Folders[folder_name].Folders.items.count
		result = input_folder.UnReadItemsCount
		return result

	def read_unread_mail_from_basic_input_folder_with_outlook(self):
		input_folder = self.namespace.GetDefaultFolder(6)
		for message in input_folder.Items.Restrict("Unread]=true"):
			print(message.Subject)

	def get_mail_items_in_folder_in_outlook(self, folder_object, input_no=5):
		result = []
		messages = folder_object.Items
		messages.Sort("ReceivesTime", True)
		message = messages.GetFirst()

		for no in range(input_no):
			print(message.Subject)
			message = messages.GetNext()
			result.append(message)
		return result

	def get_total_mail_no_at_folder_in_outlook(self, folder_name):
		result = self.namespace.Folders[folder_name].Folders.items.count
		return result

	def get_sub_folders_names_in_outlook(self, folder_name):
		result = []
		for no in range(self.namespace.Folders[folder_name].Folders.count):
			this_name = self.namespace.Folders[folder_name].Folders[no].name
			result.append([folder_name, no, this_name])
		return result

	def get_top_folder_names_in_outlook(self):
		result = []
		for no in range(self.namespace.Folders.count):
			this_name = self.namespace.Folders[no].Name
			result.append([no, this_name])
		return result

