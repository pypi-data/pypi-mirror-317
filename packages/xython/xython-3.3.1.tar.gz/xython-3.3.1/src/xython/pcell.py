# -*- coding: utf-8 -*-
import re, math, string, random, os, itertools, copy, time, sys, chardet
import pywintypes
from itertools import combinations_with_replacement  # 내장모듈
import win32gui, win32com.client, win32con  # pywin32의 모듈
import win32com.client.gencache
import jfinder, scolor, youtil,xy_list, basic_data  # xython 모듈


class pcell:
	"""
	엑셀을 컨트롤 할수있는 모듈
	2023-03-02 : 전반적으로 이름을 수정함
	2023-05-09 : 이름과 부족한 것을 추가함
	2023-10-21 : 비슷한것들을 삭제하고 하나씩만 남기도록 하였다
	2023-11-25 : 속도를 높이기 위해, 자주사용하는 일부 함수를 새롭게 만듦
	2023-12-16 : 영역을 별도로 선택하지 않아도 잘 되는 것을 선택
	2024-03-10 : 전반적으로 확인을 하고, 새로 만든것과 sopt으로 사용하는것도 기초적인것만 가능하도록 같이 묶음
				event부분도 pcell에 벌도의 class로 같이 묶음

	기본값을 value -> value2로 변경
	2024-05-05 : 전체적으로 이름을 확인
	2024-05-12 : 1,2차원의 리스트를 xylist(1로 시작하는 기능을 가진 리스트)를 만들어서 이 형태로 나오도록 만듦

	xylist에 대한 기준 : 내부에서 이루어지는것은 기존의 0부터 시작하는 것으로
	외부에서 이루어지는 모든 것은 1부터 시작하는 형식으로 한다
	엑셀과 같이 1부터 시작하는 형태로 모든것을 변경

	Range객체는 전달이 불가능하다, 그러니 Range객체를 돌려줄때는 주소를 돌려준다
	2024-06-15 : 모든 pcell의 메소드를 합친것이다
	2024-08-10 : 비슷한 것들을 제거하고 전체적으로 재확인함
	"""

	def __getattr__(self, name: str) -> int:
		# excel.activesheet처럼 함수가 아닌 클래스변수처럼 사용하는것
		result = ""
		if name == "activesheet":
			result = self.read_activesheet_name()
		if name == "activecell":
			result = self.read_activecell_value()
		return result

	def __init__(self, filename="", cache_on_off=""):
		"""
		공통으로 사용할 변수들을 설정하는 것
		"""
		self.color = scolor.scolor()
		self.util = youtil.youtil()
		self.xyre = jfinder.jfinder()
		self.xylist = xy_list.xy_list()
		self.vars = basic_data.basic_data().vars  # package안에서 공통적으로 사용되는 변수들

		self.menu_dic = {}
		self.cell_value = False
		self.range_value = False
		self.result = False
		self.sheet_object = None
		self.range_object = None
		self.use_same_sheet = False
		self.r1c1 = False
		self.workbook_count = 0
		self.pen_color = ""
		self.pen_style = 4
		self.pen_thickness = 5
		self.start_point_width = 2
		self.start_point_length = 2
		self.start_point_style = 1
		self.end_point_width = 2
		self.end_point_length = 2
		self.end_point_style = 1
		self.max_x = 1
		self.max_y = 1

		if filename == "no" or filename == "not":
			# 화일을 열지 않고 실행시키기위한 부분
			pass
		else:
			self.__start_pcell(filename, cache_on_off)

	def __start_pcell(self, filename="", cache_on_off=""):
		# if cache_on_off == "" or cache_on_off == "on":
		#	self.xlapp = win32com.client.gencache.EnsureDispatch('Excel.Application')
		self.xlapp = win32com.client.dynamic.Dispatch("Excel.Application")
		self.use_same_sheet = False
		if type(filename) == type("abc"):
			filename = str(filename).lower()

		if filename in [None, "", "activeworkbook", "active_workbook", "active"]:
			if self.xlapp.ActiveWorkbook:
				self.xlbook = self.xlapp.ActiveWorkbook
			else:
				self.xlapp.WindowState = -4137
				self.xlapp.Visible = 1
				self.xlbook = self.xlapp.Workbooks.Add()
		elif filename == "new":
			self.xlapp.WindowState = -4137
			self.xlapp.Visible = 1
			self.xlbook = self.xlapp.Workbooks.Add()

		elif filename:
			# 이미 열린화일에 같은 화일 이름이 있는지 확인
			file_found = False

			for index in range(self.xlapp.Workbooks.Count):
				one_file = self.util.check_file_path(self.xlapp.Workbooks[index].FullName)
				if str(one_file).lower() == str(filename).lower():
					self.xlbook = self.xlapp.Workbooks[index]
					file_found = True
					print("기존 엑셀 화일 발견", self.filename)
					break
			if not file_found:
				self.xlapp.WindowState = -4137
				self.xlapp.Visible = 1
				self.xlbook = self.xlapp.Workbooks.Open(filename)

		# 현재 시트의 제일 큰  가로와 세로열을 설정한다
		self.count_max_x_y()

	def add_num_in_range(self, sheet_name, xyxy, input_no, text_only=False):
		"""
		영역의 모든 값에 입력으로 들어온 숫자를 더하는 것
		add :  현재있는 자료를 변경하거나 추가 삭제하는 것이다

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		:param input_no: 숫자
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)

		for x in range(x1, x2 + 1):
			for y in range(y1, y2 + 1):
				o_value = self.read_value_in_cell_with_sheet_object(sheet_object, [x, y])
				if text_only and type(o_value) == type("abc"):
					self.write_value_in_cell_with_sheet_object(sheet_object, [x, y], o_value + input_no)

	def add_text_in_range_at_left(self, sheet_name="", xyxy="", input_text="입력필요", text_only=False):
		"""
		선택한 영역의 왼쪽에 입력한 글자를 추가
		단, 기존의 값이 숫자라도 문자로 만들어서 추가한다

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		:param input_text: 입력 text
		"""

		sheet_object = self.check_sheet_name(sheet_name)
		[x1, y1, x2, y2] = self.check_address_value(xyxy)
		range_object = sheet_object.Range(sheet_object.Cells(x1, y1),	sheet_object.Cells(x2, y2))

		for x in range(x1, x2 + 1):
			for y in range(y1, y2 + 1):
				value = self.read_value_in_cell("", [x, y])

				if text_only and type(value) == type("abc"):
					self.write_value_in_cell(sheet_name, [x, y], input_text + str(value))

	def add_text_in_range_at_right(self, sheet_name="", xyxy="", input_text="입력필요", text_only=False):
		"""
		** 보관용
		선택한 영역의 오른쪽에 입력한 글자를 추가
		단, 기존의 값이 숫자라도 문자로 만들어서 추가한다

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		:param input_text: 입력 text
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		[x1, y1, x2, y2] = self.check_address_value(xyxy)
		range_object = sheet_object.Range(sheet_object.Cells(x1, y1), sheet_object.Cells(x2, y2))

		for x in range(x1, x2 + 1):
			for y in range(y1, y2 + 1):
				value = self.read_value_in_cell("", [x, y])
				if text_only and type(value) == type("abc"):
					self.write_value_in_cell(sheet_name, [x, y], str(value) + input_text)

	def add_text_in_range_at_right_by_xy_step(self, sheet_name="", xyxy="", input_text="입력필요", xy_step=""):
		"""
		영역의 특정 위치에만 기논값 + 입력값으로 만들기
		시작점부터 x,y 번째 셀마다 값을 넣기

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		:param input_text: 입력 text
		:param xy_step: [1, 1]
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)

		for x in range(x1, x2 + 1):
			if divmod(x, xy_step[0])[1] == 0:
				for y in range(y1, y2 + 1):
					if divmod(x, xy_step[1])[1] == 0:
						cell_value = sheet_object.Cells(x, y).Value
						if cell_value == None:
							cell_value = ""
						sheet_object.Cells(x, y).Value = cell_value + str(input_text)

	def arrange_all_sheet_by_name(self):
		"""
		이름순으로 시트를 정렬하는것
		"""
		all_sheet_names = self.read_all_sheet_name()
		all_sheet_names.sort()
		for index, value in enumerate(all_sheet_names):
			self.move_sheet_position_by_no(value, index + 1)

	def change_address_all(self, xyxy, input_values):
		"""
		입력된 주소와 입력갯수에 따라서 가능한 모든 종류의 영역을 돌려준다

		:param xyxy: 입력주소
		:param input_values:
		:return:
		"""
		self.menu_dic['change_address_all'] = {'표시여부': 'x', '그리드메뉴': ['change', 'address', '3가지 종류로 만듦'],
												'실행메뉴': ['change', 'address', 'all']}
		result = {}
		x1, y1, x2, y2 = self.check_address_value(xyxy)

		y_len = len(input_values)
		x_len = len(input_values[0])
		y_len_rng = y2 - y1
		x_len_rng = x2 - x1

		max_num = max(map(lambda y: len(y), input_values))
		min_num = min(map(lambda y: len(y), input_values))
		max_y = max(y_len, y_len_rng)
		max_x = max(max_num, x_len_rng)
		min_y = max(y_len, y_len_rng)
		min_x = max(x_len, x_len_rng)

		# 입력할것중 가장 적은것을 기준으로 적용
		result["xyxy_min"] = [y1, x1, y1 + min_x, x1 + min_num]
		# 입력할것중 가장 큰것을 기준으로 적용
		result["xyxy_max"] = [y1, x1, y1 + max_x, x1 + max_x]
		# 일반적인기준으로 적용하는것
		result["xyxy_basic"] = [y1, x1, y1 + x_len, x1 + max_num]
		return result

	def change_address_to_xyxy(self, input_address):
		"""
		어떤 형태의 주소값이라도 xyxy형식으로 바꾸는 것

		:param input_address:
		:return:
		"""
		result = self.check_address_value(input_address)
		return result

	def change_address_value(self, xyxy):
		"""
		셀의 $aa$10 --> aa10,  으로 바꾸어주는 함수
		문자, 숫자, :만을 남겨놓고 나머지는 모두 삭제하는 것이다
		*** $를 없애는 코드를 별도로 만든다
		"""

		char_in_start_cell = ""
		eng_spell = string.ascii_lowercase + string.digits + ':'
		list_cell = list(xyxy)

		for one_word in list_cell:
			one_word = str(one_word).lower()
			if one_word in eng_spell:
				char_in_start_cell = char_in_start_cell + one_word
		return char_in_start_cell

	def change_any_color_to_rgb(self, input_color):
		"""
		입력으로 들어오는 색에 대한 입력값에따라 RGB값으로 바꾼다
		입력 : rgb[22,34,35], 123456, 빨강++, hsv[123,234,234]
		출력값 : rgb[123,234,234]
		"""
		input_type = type(input_color)
		if input_type == type(123):
			result = self.color.change_rgbint_to_rgb(input_color)
		elif input_type == type("abc"):
			result = self.color.change_scolor_to_rgb(input_color)
		elif input_type == type([]):
			if input_color[0] > 100 or input_color[1] > 100 or input_color[2] > 100:
				# 리스트는 2가지 형태로 rgb나 hsv가 가능하니 100이상이 되면 hsv이니, 전부 100이하이면 hsv로 하도록 한다
				result = input_color
			else:
				result = self.color.change_hsl_to_rgb(input_color)
		return result

	def change_char_to_num(self, input_char):
		"""
		문자열 주소를 숫자로 바꿔주는 것 ( b -> 2 )
		문자가 오던 숫자가 오던 숫자로 변경하는 것이다
		주소를 바꿔주는 것이다

		:param input_char: 입력 text
		"""
		aaa = re.compile("^[a-zA-Z]+$")  # 처음부터 끝가지 알파벳일때
		result_str = aaa.findall(str(input_char))

		bbb = re.compile("^[0-9]+$")  # 처음부터 끝가지 숫자일때
		result_num = bbb.findall(str(input_char))

		if result_str != []:
			no = 0
			result = 0
			for one in input_char.lower()[::-1]:
				num = string.ascii_lowercase.index(one) + 1
				result = result + 26 ** no * num
				no = no + 1
		elif result_num != []:
			result = int(input_char)
		else:
			result = "error"
		return result

	def change_excel56_no_to_rgb(self, input_excel56_no):
		"""
		엑셀 56색의 번호 -> rgb 값

		:param input_excel56_no:
		:return:
		"""
		result = self.vars["excel56_rgb"][int(input_excel56_no) - 1]
		return result

	def change_excel56_to_color_name(self, input_excel56):
		"""
		엑셀의 56가지 색번호를 색이름으로 돌려주는것

		:param input_excel56: 엑셀의 56가지 색상 번호중 하나인 숫자
		"""
		result = self.color.change_excel56_to_color_name(input_excel56)
		return result

	def change_excel56_to_rgb(self, input_excel56):
		"""
		엑셀의 56가지 색번호 => rgb값

		:param input_excel56: 엑셀의 56가지 색상 번호중 하나인 숫자
		:return: [r, g, b]
		"""
		result = self.change_excel56_no_to_rgb(int(input_excel56))
		return result

	def change_excel56_to_rgbint(self, input_excel56):
		"""
		엑셀의 56가지 색번호 => rgb int값

		:param input_rgbint: rgb의 정수값
		"""
		rgb = self.change_56color_no_to_rgb(input_excel56)
		result = self.color.change_rgb_to_rgbint(rgb)
		return result

	def change_list_2d_over_to_list_2d(self, input_list_2d_over):
		"""
		2 차원자료가 넘어가는것은 콤마(,)로 연결한 하나의 자료로 만드는 것
		2 차원의 자료중에서 정규표현식에서 여러 개를 찾은 경우에, 하나의 자료로 만들어 주는 기능

		:param input_list_2d_over:
		:return:
		"""
		for x, list_1d in enumerate(input_list_2d_over):
			for y, value in enumerate(list_1d):
				temp = ""
				if value and len(value) > 1:
					for one in value:
						temp = temp + str(one) + ","
					input_list_2d_over[x][y] = temp[:-1]

	def change_num_to_char(self, input_any_type):
		"""
		주소를 변경하기 위해서 숫자를 문자로 바꿔주는 것
		사용법 : 2 -> b

		:param input_any_type: 입력숫자
		"""
		re_com = re.compile(r"([0-9]+)")
		result_num = re_com.match(str(input_any_type))

		if result_num:
			base_number = int(input_any_type)
			result_01 = ''
			result = []
			while base_number > 0:
				div = base_number // 26
				mod = base_number % 26
				if mod == 0:
					mod = 26
					div = div - 1
				base_number = div
				result.append(mod)
			for one_data in result:
				result_01 = string.ascii_lowercase[one_data - 1] + result_01
			final_result = result_01
		else:
			final_result = input_any_type
		return final_result

	def change_r1c1_to_xyxy(self, input_r1c1):
		"""
		사용법 : a1 => [1,1]
		문자열 주소형태를 [1,1,3,3]의 형태로 바꿔주는 것

		:param input_r1c1: 입력 text
		"""
		result = self.change_string_address_to_xyxy(input_r1c1)
		return result

	def change_range_name_to_address(self, input_range_name):
		"""
		이름영역의 주소를 갖고오는 것
		단, 이름영역의 주소형태는 시트이름또한 포함이 되어있어서, 시트이름과 주소의 2개로 결과값을 돌려준다

		:param input_range_name:
		:return:
		"""
		if type(input_range_name) == type("str"):
			aaa = input_range_name.replace("=", "").split("!")
			if len(aaa) == 2:
				sheet_name = aaa[0]
				xyxy = aaa[1]
			else:
				sheet_name = ""
				xyxy = aaa[0]
		elif type(input_range_name) == type([]):
			if len(input_range_name) == 2:
				sheet_name = input_range_name[0]
				xyxy = input_range_name[1]
			else:
				sheet_name = ""
				xyxy = input_range_name[0]

		xyxy = self.check_address_value(xyxy)

		return [sheet_name, xyxy]

	def change_sheet_name(self, old_name, new_name):
		"""
		시트이름 변경

		:param old_name: 변경전 시트이름
		:param new_name: 변경후 시트이름
		"""
		all_sheet_names = self.read_all_sheet_name()
		if not new_name in all_sheet_names:
			self.xlbook.Worksheets(old_name).Name = new_name

	def change_string_address_to_xyxy(self, input_string_address):
		"""
		문자열형식의 모든 주소형태 => [x1, y1, x2, y2]
		입력된 주소값을 [x1, y1, x2, y2]의 형태로 만들어 주는 것이다

		:param input_string_address: 입력으로 들어오는 영역을 나타내는 text, "", "$1:$8", "1", "a","a1", "a1b1", "2:3", "b:b"
		:return: [x1, y1, x2, y2]의 형태
		"""
		aaa = re.compile("[a-zA-Z]+|\d+")
		address_list = aaa.findall(str(input_string_address))
		temp = []
		result = []

		for one in address_list:
			temp.append(self.util.check_one_address(one))

		if len(temp) == 1 and temp[0][1] == "string":
			# "a"일때
			result = [0, temp[0][0], 0, temp[0][0]]
		elif len(temp) == 1 and temp[0][1] == "num":
			# 1일때
			result = [temp[0][0], 0, temp[0][0], 0]
		elif len(temp) == 2 and temp[0][1] == temp[1][1] and temp[0][1] == "string":
			# "a:b"일때
			result = [0, temp[0][0], 0, temp[1][0]]
		elif len(temp) == 2 and temp[0][1] == temp[1][1] and temp[0][1] == "num":
			# "2:3"일때
			result = [temp[0][0], 0, temp[1][0], 0]
		elif len(temp) == 2 and temp[0][1] != temp[1][1] and temp[0][1] == "num":
			# "2a"일때
			result = [temp[0][0], temp[1][0], temp[0][0], temp[1][0]]
		elif len(temp) == 2 and temp[0][1] != temp[1][1] and temp[0][1] == "string":
			# "a2"일때
			result = [temp[1][0], temp[0][0], temp[1][0], temp[0][0]]
		elif len(temp) == 4 and temp[0][1] != temp[1][1] and temp[0][1] == "num":
			# "a2b3"일때
			result = [temp[0][0], temp[1][0], temp[2][0], temp[3][0]]
		elif len(temp) == 4 and temp[0][1] != temp[1][1] and temp[0][1] == "string":
			# "2a3c"일때
			result = [temp[1][0], temp[0][0], temp[3][0], temp[2][0]]
		return result

	def change_tuple_2d_to_list_2d(self, input_tuple_2d):
		"""
		2차원의 듀플을 2차원 리스트로 만드는 것

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		:return:
		"""
		result = []
		for x in range(len(input_tuple_2d)):
			temp = []
			for y in range(len(input_tuple_2d[0])):
				value = input_tuple_2d[x][y]
				if value:
					pass
				else:
					value = ""
				temp.append(value)
			result.append(temp)
		return result

	def read_value_in_range_as_list(self, sheet_name="", xyxy=""):
		"""
		2차원의 듀플을 2차원 리스트로 만드는 것

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		:return:
		"""
		list_2d = self.read_value_in_range(sheet_name, xyxy)

		result = []
		for x in range(len(list_2d)):
			temp = []
			for y in range(len(list_2d[0])):
				value = list_2d[x][y]
				if value:
					pass
				else:
					value = ""
				temp.append(value)
			result.append(temp)
		return result

	def change_value_in_range_as_capital(self, sheet_name="", xyxy=""):
		"""
		선택한 영역의 값들을 첫글자만 대문자로 변경
		입력값 : 입력값없이 사용가능

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		:return:
		"""
		self.menu_dic['change_capital'] = {'표시여부': '필요', '그리드메뉴': ['change', 'capital', '첫글자만 대문자'],
											'실행메뉴': ['change', 'capital', '']}
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)

		for x in range(x1, x2 + 1):
			for y in range(y1, y2 + 1):
				value = sheet_object.Cells(x, y).Value
				if value == None: value = ""
				sheet_object.Cells(x, y).Value = str(value.capitalize())

	def change_value_in_range_as_lower(self, sheet_name="", xyxy=""):
		"""
		소문자로 만드는 것
		:param sheet_name: 시트이름
		:param xyxy: [1,1,2,2]
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)

		for x in range(x1, x2 + 1):
			for y in range(y1, y2 + 1):
				value = sheet_object.Cells(x, y).Value
				if value == None: value = ""
				sheet_object.Cells(x, y).Value = str(value.lower())

	def change_value_in_range_as_rtrim(self, sheet_name="", xyxy=""):
		"""
		오른쪽 공백을 없애는 것

		:param sheet_name: 시트이름
		:param xyxy: [1,1,2,2]
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)

		for x in range(x1, x2 + 1):
			for y in range(y1, y2 + 1):
				value = sheet_object.Cells(x, y).Value
				if value == None: value = ""
				sheet_object.Cells(x, y).Value = str(value.rstrip())

	def change_value_in_range_as_swapcase(self, sheet_name="", xyxy=""):
		"""
		영역안의 대소문자를 바꾸는 것

		:param sheet_name: 시트이름
		:param xyxy: [1,1,2,2]
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)

		for x in range(x1, x2 + 1):
			for y in range(y1, y2 + 1):
				value = sheet_object.Cells(x, y).Value
				if value == None: value = ""
				sheet_object.Cells(x, y).Value = str(value.swapcase())

	def change_value_in_range_as_trim(self, sheet_name="", xyxy=""):
		"""
		영역의 값의 앞뒤 공백을 지우는 것

		:param sheet_name: 시트이름
		:param xyxy: [1,1,2,2]
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)

		for x in range(x1, x2 + 1):
			for y in range(y1, y2 + 1):
				value = sheet_object.Cells(x, y).Value
				if value == None: value = ""
				sheet_object.Cells(x, y).Value = str(value.strip())

	def change_value_in_range_as_upper(self, sheet_name="", xyxy=""):
		"""
		대문자로 만드는 것

		:param sheet_name: 시트이름
		:param xyxy: [1,1,2,2]
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)

		for x in range(x1, x2 + 1):
			for y in range(y1, y2 + 1):
				value = sheet_object.Cells(x, y).Value
				if value == None: value = ""
				try:
					sheet_object.Cells(x, y).Value = str(value.upper())
				except:
					pass

	def change_value_in_range_by_jfsql(self, sheet_name, xyxy, iy, jfsql, new_value):
		"""
		선택한 영역의 한줄을 기준으로, 각 셀의값을 jfsql로 찾아서
		찾은값을 변경하는 것

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		:param iy:
		:param search_jfre:
		:param new_value:
		:return:
		"""
		list_2d = self.read_value_in_range(sheet_name, xyxy)
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)

		for index, list_1d in enumerate(list_2d):
			try:
				aa = self.xyre.replace_with_jf_sql(jfsql, new_value, list_1d[iy])
				if aa == list_1d[index]:
					pass
				else:
					self.write_value_in_cell(sheet_object, [x1 + index, y1 + iy], aa)
			except:
				pass

	def change_value_in_range_to_dic_with_xy_position(self, sheet_name="", xyxy=""):
		"""
		선택된 영역안의 2차원자료를 사전형식으로 돌려 주는 것
		같은값을 발견하면, 주소를 추가하는 형태
		예: [["가나","다라"],["ab", "다라"]] => {"가나":[[1,1]], "다라":[[1,2], [2,2]],"ab":[[2,1]]}

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		:return:
		"""
		result = {}
		list_2d = self.read_value_in_range(sheet_name, xyxy)

		for ix, list_1d in enumerate(list_2d):
			for iy, one_value in enumerate(list_1d):
				if one_value in result.keys():
					result[ix + 1, iy + 1].append([one_value])
				else:
					result[one_value] = [[ix + 1, iy + 1]]
		return result

	def change_xy_list_to_address_char(self, xy_list=[[1, 1], [2, 3], [2, 4]]):
		"""
		xy형식의 자료 묶음을 a1형식의 값으로 바꾸는 것

		:param xy_list: [[1, 1], [2, 3], [2, 4]]
		"""
		xy_list = self.change_xylist_to_list(xy_list)
		result = ""
		for one_data in xy_list:
			y_char = self.change_num_to_char(one_data[1])
			result = result + str(y_char[0]) + str(one_data[0]) + ', '
		return result[:-2]

	def change_xy_to_a1(self, xy=[3, 4]):
		"""
		xy의 형태([1,2])로 넘어온 셀값을 A1형식으로 바꾸는 것

		:param xy: [2,3]의 형식
		"""
		x_char = self.change_num_to_char(xy[0])
		result = str(x_char[0]) + str(xy[1])
		return result

	def change_xylist_to_addresschar(self, input_xylist=[[1, 1], [2, 3], [2, 4]]):
		"""
		xy형식의 자료들을 a1형식의 값으로 바꾸는 것

		:param xy_list: [[1, 1], [2, 3], [2, 4]]
		:return:
		"""
		result = ""
		for one_data in input_xylist:
			y_char = self.change_num_to_char(one_data[1])
			result = result + str(y_char[0]) + str(one_data[0]) + ', '
		return result[:-2]

	def change_xylist_to_list(self, input_xylist):
		# 입력으로 들어오는 자료형태가 xylist인지를 확인하는 것
		if type(input_xylist) == type(xy_list):
			temp = []
			for value in input_xylist:
				if type(value) == type(xy_list):
					temp.append(list(value))
				else:
					temp.append(value)
			return temp

		else:
			return input_xylist

	def change_xyxy_to_pxywh(self, sheet_name="", xyxy=""):
		"""
		[1,1,2,2] => 위치의 픽셀값으로 변경 [왼쪽위 가로 픽셀값, 왼쪽위 세로 픽셀값, 픽셀 넓이, 픽셀 높이]

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		:return:
		"""
		range_object = self.get_range_object_by_xyxy(sheet_name, xyxy)
		result = [range_object.Left, range_object.Top, range_object.Width, range_object.Height]
		return result

	def change_xyxy_to_pxyxy(self, xyxy):
		"""
		셀의 번호를 주면, 셀의 왼쪽과 오른쪽아래의 픽셀 주소를 돌려준다
		픽샐의 값으로 돌려주는것

		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		"""
		x1, y1, x2, y2 = self.check_address_value(xyxy)

		px1, py1, px1_w, py1_h = self.read_coord_in_cell("", [x1, y1])
		px2, py2, px2_w, py2_h = self.read_coord_in_cell("", [x2, y2])

		result = [px1, py1, px2 + px2_w - px1, py2 + py2_h - py1]
		return result

	def change_xyxy_to_r1c1(self, xyxy):
		"""
		입력으로 들어오는 [1,2,3,4] 를 "b1:d3"로 변경하는 것

		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		"""
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		str_1 = self.change_num_to_char(y1)
		str_2 = self.change_num_to_char(y2)
		if str(x1) == "0": x1 = ""
		if str(x2) == "0": x2 = ""
		if str_1 == "0": str_1 = ""
		if str_2 == "0": str_2 = ""

		result = str_1 + str(x1) + ":" + str_2 + str(x2)
		self.r1c1 = result
		return result

	def change_xyxy_to_r1r1(self, xyxy):
		"""
		[1,2,3,4] => "b1:b1"

		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:return:
		"""
		x1, y1, x2, y2 = self.check_address_value(xyxy)

		str_1 = self.change_num_to_char(y1)
		result = str_1 + str(x1) + ":" + str_1 + str(x1)
		return result

	def check_address_value(self, input_address):
		"""
		입력형태 :, "", [1,2], [1,2,3,4], "$1:$8", "1", "a","a1", "a1b1", "2:3", "b:b"
		입력된 주소값을 [x1, y1, x2, y2]의 형태로 만들어 주는 것이다
		입력된 자료의 형태에 따라서 구분을 한다

		:param input_address:
		:return:
		"""
		# print("input_address ==> ", input_address)
		if type(input_address) == type(self.xlapp.Selection):
			# range객체가 들어왔을때 적용하기 위한것
			input_address = input_address.Address

		if input_address == "" or input_address == None:  # 아무것도 입력하지 않을때
			result = self.read_address_for_selection()
		elif input_address == [0, 0] or input_address == [0, 0, 0, 0]:
			result = [1, 0, 1048576, 0]

		elif type(input_address) == type("string"):  # 문자열일때
			if "!" in input_address:
				one = input_address.replace("=", "").split("!")[1]
			result = self.change_string_address_to_xyxy(input_address)

		elif type(input_address) == type([]):  # 리스트형태 일때
			if len(input_address) == 2:
				revised_input_address = input_address + input_address
			elif len(input_address) == 4:
				revised_input_address = input_address

			result = []
			for one in revised_input_address:
				if type(one) == type("string"):  # 문자열일때
					if "!" in one:
						one = one.replace("=", "").split("!")[1]
					temp = self.change_char_to_num(one)
					result.append(temp)
				elif type(one) == type(123):
					result.append(one)
		else:
			result = self.read_address_for_selection()

		try:
			changed_result = [min(result[0], result[2]), min(result[1], result[3]), max(result[0], result[2]),
							  max(result[1], result[3])]
		except:
			changed_result = result
		return changed_result

	def check_address_value_3_sets(self, xyxy, input_address):
		"""
		어떤 형식의 주소 => 3개의 주소형태로 만들어 주는 것
		입력주소와 자료를 받아서 최소로할것인지 최대로 할것인지를 골라서 나타낼려고 만든것

		입력값 : [$A$1], [$A$1:$B$2], [$1:$7], [$A:$B] ["A1"],[2,1,3,2], [1,2]이 경우가 가능
		출력값 : [["$A$2:$B$3"],["A1","B2],[2,1,3,2]]무조건 3개의 형태로 나오도록 만든다

		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		:param input_address: 입력자료
		"""
		input_address = self.change_xylist_to_list(input_address)
		x1, y1, x2, y2 = self.check_address_value(xyxy)

		result = {}
		x_len = len(input_address)
		y_len = len(input_address[0])

		y_len_rng = y2 - y1 + 1
		x_len_rng = x2 - x1 + 1

		max_num = max(map(lambda y: len(y), input_address))
		min_num = min(map(lambda y: len(y), input_address))

		max_y = max(y_len, y_len_rng)
		max_x = max(max_num, x_len_rng)
		min_y = max(y_len, y_len_rng)
		min_x = max(x_len, x_len_rng)

		# 입력할것중 가장 적은것을 기준으로 적용
		result["xyxy_min"] = [x1, y1, x1 + min_y, y1 + min_num]
		# 입력할것중 가장 큰것을 기준으로 적용
		result["xyxy_max"] = [x1, y1, x1 + max_y, y1 + max_y]
		# 일반적인기준으로 적용하는것
		result["xyxy_basic"] = [x1, y1, x1 + x_len, y1 + max_num]
		return result

	def check_basic_data(self, sheet_name="", xyxy=""):
		"""
		자주 사용하는 것을 하나로 만들어서 관리하는것이 코드를 줄일것으로 보여서 만듦

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		range_object = self.get_range_object_by_xyxy(sheet_name, xyxy)

		self.r1c1 = self.change_xyxy_to_r1c1([x1, y1, x2, y2])

		return [sheet_object, range_object, x1, y1, x2, y2]

	def check_differ_at_2_area(self, input_sa1, input_sa2):
		"""
		2개의 같은 크기의 영역의 2개 자료를 비교하여
		첫번째 같은입력된 자료형을 확인하는것

		:param input_sa1:
		:param input_sa2:
		:return:
		"""
		datal = self.read_value_in_range(input_sa1[0], input_sa1[1])
		data2 = self.read_value_in_range(input_sa2[0], input_sa2[1])
		start_x = input_sa2[1][0]
		start_y = input_sa2[1][1]
		for x in range(len(datal)):
			for y in range(len(datal[0])):
				if datal[x][y] == data2[x][y]:
					pass
				else:
					self.paint_color_in_cell_by_excel_colorno(input_sa2[0], [x + start_x, y + start_y], 3)

	def check_differ_at_2_same_area(self, sheet_name1, xyxy1, sheet_name2, xyxy2):
		"""
		동일한 사이즈의 2영역의 값을 비교해서, 다른것이 발견되면 색칠하는 것

		:param sheet_name1:
		:param xyxy1:
		:param sheet_name2:
		:param xyxy2:
		:return:
		"""
		list_2d_1 = self.read_value_in_range(sheet_name1, xyxy1)
		list_2d_2 = self.read_value_in_range(sheet_name2, xyxy2)

		x11, y11, x12, y12 = self.check_address_value(xyxy1)
		x21, y21, x22, y22 = self.check_address_value(xyxy2)

		for x in range(len(list_2d_1)):
			for y in range(len(list_2d_1[0])):
				if list_2d_1[x][y] == list_2d_2[x][y]:
					pass
				else:
					self.paint_cell_by_scolor(sheet_name1, [x + x11, y + y11], "yel")
					self.paint_cell_by_scolor(sheet_name2, [x + x21, y + y21], "yel")

	def check_excel_filename(self, input_file):
		"""
		입력으로 들어온 엑셀 화일이름을 적절하게 변경 시킨다

		:param input_file:
		:return:
		"""
		if "\\" in input_file or "/" in input_file:
			pass
		else:
			path = self.get_current_path()
			input_file = path + "\\" + input_file

		input_file = self.util.check_file_path(input_file)

		if input_file.endswith("xlsx") or input_file.endswith("xls"):
			pass
		else:
			input_file = input_file + ".xlsx"

		return input_file

	def check_file_in_folder(self, path, file_name):
		"""
		화일이 폴더안에 있는지를 확인하는 것

		:param path: path
		:param file_name: file_name
		:return:
		"""
		result = ""
		if path == "":
			path = "C:/Users/Administrator/Documents"
		file_name_all = self.util.get_all_file_name_in_folder(path)

		if file_name in file_name_all:
			result = file_name
		return result

	def check_file_path(self, input_filename):
		"""
		경로를 /와 \으로 사용하는 경우가 잇어서, 그걸 변경하는 것

		:param input_filename:
		:return:
		"""
		changed_filename = str(input_filename).lower()
		changed_filename = changed_filename.replace("\\\\", "/")
		changed_filename = changed_filename.replace("\\", "/")
		return changed_filename

	def check_font_element(self, input_key):
		"""
		단어중 가장 가까운 단어들 찾기
		입력형식은 bold(),진하게(yes).. 이런식으로 입력이 되도록 하면 어떨까??

		:param input_key:
		:return:
		"""
		base_dic = self.vars["check_font_para"]
		try:
			result = base_dic[input_key]
		except:
			result = input_key
		return result

	def check_input_range(self, input_range):
		"""
		입력으로 들어오는 영역을 확인하는 것

		:param input_range:
		:return:
		"""
		if type(input_range[0]) != type([]):
			result = [input_range]
		else:
			result = input_range
		return result

	def check_input_values(self, input_any_type):
		"""
		보통의 어떤자료가 들어오면, 알아서 변수로 만들어 주는 것

		:param input_any_type:
		:return:
		"""
		input_any_type = self.change_xylist_to_list(input_any_type)
		result = {}

		if type(input_any_type) == type({}):
			result.update(input_any_type)

		elif type(input_any_type) == type([]) and input_any_type != []:
			if type(input_any_type[0]) == type([]):
				result["datas"] = input_any_type
			elif len(input_any_type) == 2 or len(input_any_type) == 4:
				try:
					result["xyxy"] = self.check_address_value(input_any_type)
				except:
					pass

		elif type(input_any_type) == type("abc"):
			if "sheet" in input_any_type:
				result["sheet_name"] = input_any_type
			else:
				try:
					result["xyxy"] = self.check_address_value(input_any_type)
				except:
					pass

		return result

	def check_line_style(self, input_list):
		"""
		영역의 선의 형태를 적용할때, 일반적인 단어를 사용해도, 알아서 코드에서 사용하는 기본 용어로 바꿔주는 코드이다

		:param input_list:
		:return:
		"""

		result = {"color": "bla", "thickness": "", "style": "", "area": "box"}

		for one in input_list:
			if one in self.vars["check_line_thickness"].keys():
				result["thickness"] = self.vars["check_line_thickness"][one]
			elif one in self.vars["check_line_style"].keys():
				result["style"] = self.vars["check_line_style"][one]
			elif one in self.vars["check_line_position"].keys():
				result["area"] = self.vars["check_line_position"][one]
			elif self.color.check_input_scolor(one):
				try:
					result["color"] = self.color.change_scolor_to_rgb(one)
				except:
					pass
		return result

	def check_list_address(self, input_list):
		"""
		주소값을 4자리 리스트로 만들기 위하여 사용하는것

		:param input_list: list type
		"""
		input_list = self.change_xylist_to_list(input_list)

		result = []
		if len(input_list) == 1:
			xy = str(input_list[0]).lower()
			# 값이 1개인경우 : ['1'], ['a']
			if xy[0] in string.digits:
				result = [xy, 0, xy, 0]
			elif xy[0].lower() in string.ascii_lowercase:
				result = [0, xy, 0, xy]
		elif len(input_list) == 2:
			# 값이 2개인경우 : ['a', '1'], ['2', '3'], ['a', 'd']
			y1 = str(input_list[0]).lower()
			x1 = str(input_list[1]).lower()
			if y1[0] in string.digits:
				if x1[0] in string.digits:
					result = [y1, 0, x1, 0]
				elif x1[0] in string.ascii_lowercase:
					result = [y1, y1, y1, y1]
			elif y1[0] in string.ascii_lowercase:
				if x1[0] in string.digits:
					result = [x1, y1, y1, y1]
				elif x1[0] in string.ascii_lowercase:
					result = [0, y1, 0, x1]
		elif len(input_list) == 4:
			y1 = str(input_list[0]).lower()
			x1 = str(input_list[1]).lower()
			y2 = str(input_list[2]).lower()
			x2 = str(input_list[3]).lower()
			# 값이 4개인경우 : ['aa', '1', 'c', '44'], ['1', 'aa', '44', 'c']
			if y1[0] in string.digits and x2[0] in string.digits:
				if x1[0] in string.ascii_lowercase and x2[0] in string.ascii_lowercase:
					result = [x1, y1, x2, y2]
				elif x1[0] in string.digits and x2[0] in string.digits:
					result = [x1, y1, x2, y2]
			elif y1[0] in string.ascii_lowercase and x2[0] in string.ascii_lowercase:
				if x1[0] in string.digits and x2[0] in string.digits:
					result = [x1, y1, x2, x2]
		final_result = []
		for one in result:
			one_value = str(one)[0]
			if one_value in string.ascii_lowercase:
				aaa = self.change_char_to_num(one)
			else:
				aaa = str(one)
			final_result.append(aaa)
		return final_result

	def check_n_make_sheet_name(self, sheet_name):
		"""
		시트이름을 입력받아 없으면 새로이 만드는것

		:param sheet_name:
		"""
		all_sheet_names = self.get_all_sheet_name()

		if sheet_name in all_sheet_names:
			pass
		else:
			self.new_sheet_with_name(sheet_name)

	def check_numberformat(self, sheet_name="", xyxy=""):
		"""
		셀의 여러 값들을 가지고 셀값의 형태를 분석하는 것이다
		단, 속도가 좀 느려진다

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		range_object = self.get_range_object_by_xyxy(sheet_name, xyxy)

		result = []

		for x in range(x1, x2 + 1):
			temp = []
			for y in range(y1, y2 + 1):
				one_dic = {}
				one_cell = sheet_object.Cells(x, y)
				one_dic["y"] = x
				one_dic["x"] = y
				one_dic["value"] = one_cell.Value
				one_dic["value2"] = one_cell.Value2
				one_dic["text"] = one_cell.Text
				one_dic["formula"] = one_cell.Formula
				one_dic["formular1c1"] = one_cell.FormulaR1C1
				one_dic["numberformat"] = one_cell.NumberFormat
				one_dic["type"] = type(one_cell.Value)

				if type(one_cell.Value) is pywintypes.TimeType:
					# pywintypes.datetime가 맞는지를 확인하는 코드이다
					print('날짜에요!', one_cell.Value, str(type(one_cell.Value)))

				tem_1 = ""
				if (
						"h" in one_cell.NumberFormat or "m" in one_cell.NumberFormat or "s" in one_cell.NumberFormat) and ":" in one_cell.NumberFormat:
					tem_1 = "time"

				if "y" in one_cell.NumberFormat or "mmm" in one_cell.NumberFormat or "d" in one_cell.NumberFormat:
					tem_1 = "date" + tem_1

				if type(one_cell.Value) == type(123.45) and one_cell.Value > 1 and tem_1 == "time":
					tem_1 = "datetime"

				one_dic["style"] = tem_1
				temp.append(one_dic)
			result.append(temp)
		return result

	def check_ok_or_no(self, jf_sql, input_text):
		"""
		입력값이 jf_sql의 정규표현식의 내용이 들어가 있는지 확인하는 것

		:param jf_sql:
		:param input_text:
		:return:
		"""
		re_sql = self.xyre.change_jf_sql_to_re_sql(jf_sql)
		result = self.xyre.search_all_by_jf_sql(re_sql, input_text)
		if result == []:
			output_text = False
		else:
			output_text = True
		return output_text

	def check_one_address(self, input_text):
		"""
		입력된 1개의 주소를 문자인지, 숫자인지
		숫자로 변경하는 것이다

		:param input_text: 입력 text
		:return:
		"""
		re_com_1 = re.compile("^[a-zA-Z]+$")  # 처음부터 끝가지 알파벳일때
		result_str = re_com_1.findall(str(input_text))

		re_com_2 = re.compile("^[0-9]+$")  # 처음부터 끝가지 숫자일때
		result_num = re_com_2.findall(str(input_text))

		if result_num == [] and result_str != []:
			address_type = "string"
			no = 0
			address_int = 0
			for one in input_text.lower()[::-1]:
				num = string.ascii_lowercase.index(one) + 1
				address_int = address_int + 26 ** no * num
				no = no + 1
		elif result_str == [] and result_num != []:
			address_type = "num"
			address_int = int(input_text)
		else:
			address_int = "error"
			address_type = "error"
		return [address_int, address_type, input_text]

	def check_password_for_sheet(self, isnum="yes", istext_small="yes", istext_big="yes", isspecial="no", len_num=10):
		"""
		시트의 암호를 찾아주는것

		:param isnum:
		:param istext_small:
		:param istext_big:
		:param isspecial:
		:param len_num:
		"""
		check_char = []
		if isnum == "yes":
			check_char.extend(list(string.digits))
		if istext_small == "yes":
			check_char.extend(list(string.ascii_lowercase))
		if istext_big == "yes":
			check_char.extend(list(string.ascii_uppercase))
		if isspecial == "yes":
			for one in "!@#$%^*M-":
				check_char.extend(one)
		for no in range(1, len_num + 1):
			zz = itertools.combinations_with_replacement(check_char, no)
			for aa in zz:
				try:
					pswd = "".join(aa)
					self.set_sheet_lock_off("", pswd)
					return
				except:
					pass

	def check_price(self, input_price):
		"""
		백만원단위, 전만원단위, 억단위로 구분

		:param input_price:
		:return:
		"""
		input_price = int(input_price)
		if input_price > 100000000:
			result = str('{:.If}'.format(input_price / 100000000)) + "억원"
		elif input_price > 10000000:
			result = str('{: .0f}'.format(input_price / 1000000)) + "백만원"
		elif input_price > 1000000:
			result = str('{:.If}'.format(input_price / 1000000)) + "백만원"
		return result

	def check_same_data(self, input_list, check_line=10):
		"""
		엑셀의 선택한 자료에서 여러줄을 기준으로 같은 자료만 갖고오기

		:param input_list: list type
		:param check_line:
		"""
		input_list = self.change_xylist_to_list(input_list)
		result = []
		base_value = ""
		xy = self.read_address_for_activecell()
		for no in input_list:
			base_value = base_value + str(self.read_value_in_cell("", [xy[0], no]))

		# 혹시 1보다 작은 숫자가 나올 수있으므로, 최소시작점을 1로하기위해
		start_x = max(int(xy[0]) - check_line, 1)

		# 위로10개 아래로 10개의 자료를 확인한다
		for no in range(start_x, start_x + 20):
			one_value = ""
			for one in input_list:
				one_value = one_value + str(self.read_value_in_cell("", [no, one]))
			if base_value == one_value:
				# 보통 50개이상의 줄을 사용하지 않으므로 50개를 갖고온다
				temp = self.read_value_in_range("", [no, 1, no, 50])
				result.append(temp[0])
		return result

	def check_same_data_for_two_yline_to_new_sheet(self, sheet_name, xyxy1, xyxy2):
		# 2개 자료를 정렬 하는것
		data1 = self.read_range(sheet_name, xyxy1)
		data2 = self.read_range(sheet_name, xyxy2)

		data1_found = []
		data1_not_found = []
		data2_not_found = []

		for one in data2:
			if not one in data1:
				data2_not_found.append(one)

		for one in data1:
			if one in data2:
				data1_found.append(one)
			else:
				data1_not_found.append(one)

		self.new_sheet()
		self.write_cell("", [1, 1], "결과중 찾은 것")
		self.write_list_2d_from_cell("", [2, 1], data1_found)
		self.write_cell("", [1, 3], "비교자료중 못찾은 것")
		self.write_list_2d_from_cell("", [2, 3], data1_not_found)
		self.write_cell("", [1, 4], "결과가 중요한 것중 못찾은 것")
		self.write_list_2d_from_cell("", [2, 4], data2_not_found)

	def check_sheet_name(self, sheet_name):
		"""
		시트이름으로 객체를 만들어서 돌려주는 것이다
		이름이 없으면 현재 활성화된 시트를 객체로 만들어 사용한다
		숫자가 들어오면, 번호숫자로 생각해서 앞에서 n번째의 시트이름을 갖고과서 시트객체를 돌려준다

		#1 : 현재 워크북의 순번에 따른 시트객체를 갖고온다
		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		"""

		if type(self.xlbook.ActiveSheet) == type(sheet_name):  # 시트객체가 오면, 그대로 넘어가는 것
			self.sheet_object = self.xlbook.ActiveSheet
		if sheet_name == "" or sheet_name == None or str(sheet_name).lower() == "activesheet":
			self.sheet_object = self.xlbook.ActiveSheet
		elif type(sheet_name) == type(123):  # 1
			sheet_name = self.get_sheet_name_by_position_no(sheet_name)
			self.sheet_object = self.xlbook.Worksheets(str(sheet_name))
		elif self.use_same_sheet:
			pass
		else:
			try:
				self.sheet_object = self.xlbook.Worksheets(str(sheet_name))
			except:
				self.sheet_object = self.xlbook.ActiveSheet

		return self.sheet_object

	def check_sheet_name_n_xyxy(self, sheet_name="", xyxy=""):
		"""
		** 보관용

		:param sheet_name:
		:param xyxy:
		:return:
		"""
		self.check_sheet_name(sheet_name)
		self.x1, self.y1, self.x2, self.y2 = self.check_address_value(xyxy)
		# print("주소는 => ", self.x1, self.y1, self.x2, self.y2)
		self.r1c1 = self.change_xyxy_to_r1c1([self.x1, self.y1, self.x2, self.y2])
		# print("r1c1 => ", self.r1c1)
		self.range_object = self.sheet_object.Range(self.sheet_object.Cells(self.x1, self.y1),
													self.sheet_object.Cells(self.x2, self.y2))

	def check_string_address(self, input_address):
		"""
		string형태의 address를 문자와 숫자로 나누는것

		:param input_address: 입력 text, "$1:$8", "1", "a","a1", "a1b1", "2:3", "b:b"
		:return: 숫자와 문자로 된부분을 구분하는 것
		"""
		aaa = re.compile("[a-zA-Z]+|\d+")
		result = aaa.findall(str(input_address))
		return result

	def check_string_address_style(self, input_address):
		"""
		주소형태의 문자열이 어떤 형태인지 알아 내는 것

		:param input_address: 입력자료,주소형태의 문자열
		:return: "a1", "aa", "11"
		"""
		result = ""
		if input_address[0][0] in string.ascii_lowercase and input_address[1][0] in string.digits:
			result = "a1"
		if input_address[0][0] in string.ascii_lowercase and input_address[1][0] in string.ascii_lowercase:
			result = "aa"
		if input_address[0][0] in string.digits and input_address[1][0] in string.digits:
			result = "11"
		return result

	def check_title_value(self, temp_title):
		"""
		화일의 제목으로 사용이 불가능한것을 제거한다

		:param temp_title:
		:return:
		"""
		for temp_01 in [[" ", "_"], ["(", "_"], [")", "_"], ["/", "_per_"], ["%", ""], ["'", ""], ['"', ""], ["$", ""],
						["__", "_"], ["__", "_"]]:
			temp_title = temp_title.replace(temp_01[0], temp_01[1])
		if temp_title[-1] == "_": temp_title = temp_title[:-2]
		return

	def check_type_for_input_value(self, one_value):
		"""
		입력으로 들어온 자료를 확인하는 것
		:return:
		"""
		result = None
		if type(one_value) == type("abc"):
			result = "str"
		elif type(one_value) == type(123):
			result = "int"
		elif type(one_value) == type(123.45):
			result = "real"
		elif type(one_value) == type(True) or type(one_value) == type(False):
			result = "boolen"
		elif type(one_value) == type([]):
			result = "list"
		elif type(one_value) == type(()):
			result = "tuple"
		else:
			result = one_value
		return result

	def check_xx_address(self, xyxy):
		"""
		입력 주소중 xx가 맞는 형식인지를 확인하는것

		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		:return: [2, 2]의 형태로 만들어 주는것
		"""
		if type(xyxy) == type([]):
			if len(xyxy) == 1:
				result = [xyxy[0], xyxy[0]]
			elif len(xyxy) == 2:
				result = xyxy
		else:
			x = self.change_char_to_num(xyxy)
			result = [x, x]
		return result

	def check_xy_address(self, xy):
		"""
		x나 y의 하나를 확인할때 입력을 잘못하는 경우를 방지하기위해 사용

		:param xy: 3, [3], [2,3], D, [A,D], [D]
		:return: [3,3], [2,3], [4,4], [1,4]
		"""
		x1, y1, x2, y2 = self.check_address_value(xy)
		return [x1, y1]

	def check_y_address(self, input_any_type):
		"""
		결과 = "b"의 형태로 만들어 주는것

		:param input_any_type: 입력자료
		"""
		result = self.check_yy_address(input_any_type)[0]
		return result

	def check_yy_address(self, input_any_type):
		"""
		결과 = ["b", "b"]의 형태로 만들어 주는것

		:param input_any_type: 입력자료
		:return: ["b", "b"]의 형태로 만들어 주는것
		"""

		if input_any_type == "" or input_any_type == None:
			temp = self.read_address_for_selection()
			result = [temp[1], temp[3]]
		elif type(input_any_type) == type("string") or type(input_any_type) == type(123):
			temp = self.change_num_to_char(input_any_type)
			result = [temp, temp]
		elif type(input_any_type) == type([]):
			if len(input_any_type) == 2:
				result = input_any_type  # 이부분이 check_address_value와 틀린것이다
			elif len(input_any_type) == 4:
				temp = input_any_type
				result = [temp[1], temp[3]]
		else:
			temp = self.read_address_for_selection()
			result = [temp[1], temp[3]]

		new_y1 = self.change_num_to_char(result[0])
		new_y2 = self.change_num_to_char(result[1])

		return [new_y1, new_y2]

	def close(self):
		"""
		열려진 화일을 닫는것
		"""
		self.xlbook.Close(SaveChanges=0)
		del self.xlapp

	def close_active_workbook(self):
		"""
		열려진 엑셀 화일을 닫는것
		여러개가 있다면 활성화된 화일을 닫는다
		"""
		self.xlbook.Close(SaveChanges=0)

	def close_workbook(self, work_book_obj):
		"""
		열려진 엑셀 화일을 닫는것
		여러개가 있다면 활성화된 화일을 닫는다

		:param work_book_obj:
		"""
		work_book_obj.Close(SaveChanges=0)

	def concate_xline(self, input_list_2d, xy):
		"""
		선택한 영역의 세로 자료들을 다 더해서 제일위의 셀에 다시 넣는것

		:param input_list_2d:
		:param xy:
		:return:
		"""

		x_len = len(input_list_2d)
		y_len = len(input_list_2d[0])
		for y in range(y_len):
			temp = ""
			for x in range(x_len):
				self.write_value_in_cell("", [x + xy[0], y + xy[1]], "")
				if input_list_2d[x][y]:
					temp = temp + " " + input_list_2d[x][y]
			self.write_value_in_cell("", [xy[0], y + xy[1]], str(temp).strip())

	def conditional_format(self, sheet_name, xyxy, operator, range_format):
		"""
		조건부서식을 update 한것
		일반적으로 사용하는 어떤 형식의 값이 와도 알아서 적용되는것

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		:param operator: 조건을 만드는 부분
		:param range_format: 영역의 형태를 설정
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		range_object = self.get_range_object_by_xyxy(sheet_name, xyxy)
		operator = str(operator).strip().upper()
		aaa = self.util.split_operator(operator)
		if operator.startswith("AND") or operator.startswith("OR"):
			# "and(100<=$A1, $A1<200)"	 "or(100<=$A1, $A1<200)" 등을 사용할때
			cf_object = range_object.FormatConditions.Add(2, None, "=" + operator)
		elif operator.startswith("="):
			# 보통 수식을 사용할때 적용되는 것
			cf_object = range_object.FormatConditions.Add(2, None, operator)
		elif not "," in operator and len(aaa) == 5:
			# "100<-$A31<200"
			cf_object = range_object.FormatConditions.Add(2, None,
														  "=AND(" + aaa[0] + aaa[1] + aaa[2] + "," + aaa[2] + aaa[3] +
														  aaa[
															  4] + ")")
		elif not "," in operator and len(aaa) == 3:
			# "100>$A10"
			cf_object = range_object.FormatConditions.Add(2, None, "=" + operator)

		self.set_format_in_range(cf_object, range_format)

	def copy_function_from_xyxy1_to_xyxy2(self, sheet_name, xyxy1, xyxy2):
		"""
		xlSheet_to_final.Range("A53:A54").AutoFill(xlSheet_to_final.Range("A53:A61"),xlFillDefault)

		:param sheet_name:
		:param xyxy1:
		:param xyxy2:
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy1)
		range_object_1 = sheet_object.Range(sheet_object.Cells(x1, y1), sheet_object.Cells(x2, y2))

		x1, y1, x2, y2 = self.check_address_value(xyxy2)
		range_object_2 = sheet_object.Range(sheet_object.Cells(x1, y1), sheet_object.Cells(x2, y2))

		range_object_1.AutoFill(range_object_2)

	def copy_range(self, sheet_name="", xyxy=""):
		"""
		영역의 복사까지만 하는 기능이다

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		"""
		range_object = self.get_range_object_by_xyxy(sheet_name, xyxy)
		range_object.Copy()

	def copy_sheet_at_same_workbook(self, old_sheet_name, new_sheet_name):
		"""
		시트복사하기

		:param old_sheet_name: 복사할 전의 이름
		:param new_sheet_name: 새로운 시트이름
		"""

		all_sheet_names = self.read_all_sheet_name()
		if old_sheet_name in all_sheet_names:
			sheet_object = self.check_sheet_name(old_sheet_name)

			sheet_object.Copy(Before=sheet_object)
			if not new_sheet_name == "":
				old_name = self.read_activesheet_name()
				self.change_sheet_name(old_name, new_sheet_name)
		else:
			print("Can not found sheet name")

	def copy_value_in_range_to_another_sheet(self, sheet_name1, range1, sheet_name2, range2):
		"""
		특정 영역을 복사해서 다른시트의 영역에 붙여 넣기

		:param sheet_name1:
		:param range1:
		:param sheet_name2:
		:param range2:
		:return:
		"""
		self.xlbook.Worksheets(sheet_name1).Range(range1).Select()
		self.xlbook.Worksheets(sheet_name2).Range(range2).Paste()
		self.xlapp.CutCopyMode = 0

	def copy_xxline(self, sheet_name="", xyxy=""):
		"""
		가로영역을 복사

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		"""
		self.sheet_object = self.check_sheet_name(sheet_name)
		x1, x2 = self.check_xx_address(xyxy)
		self.sheet_object.Rows(str(x1) + ":" + str(x2)).Copy()

	def copy_yyline(self, sheet_name="", xyxy=""):
		"""
		세로영역을 복사

		:param sheet_name: 시트이름 ("" : 활성화된 시트이름)
		:param xyxy: [1,1,2,2], 가로세로셀영역 ("" : 현재 선택영역)
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		y1, y2 = self.check_yy_address(xyxy)
		sheet_object.Columns(str(y1) + ":" + str(y2)).Copy()

	def count_continuous_same_value_in_range(self, sheet_name="", xyxy=""):
		"""
		delete_samevalue_continuous(sheet_name="", xyxy)
		선택한 영역중 세로로 연속된 같은자료만 삭제
		밑에서부터 올라가면서 찾는다
		"""
		self.menu_dic['count_continuous_samevalue'] = {'표시여부': '필요',
														'그리드메뉴': ['delete', 'continuous_samevalue', '연속된 같은 값 삭제'],
														'실행메뉴': ['delete', 'continuous_samevalue', '']}
		x1, y1, x2, y2 = self.check_address_value(xyxy)

		for y in range(y2, y1, -1):
			for x in range(x1, x2 + 1):
				base_value = self.read_cell_value(sheet_name, [x, y])
				up_value = self.read_cell_value(sheet_name, [y - 1, x])
				if base_value == up_value:
					self.write_cell_value(sheet_name, [x, y], "")

	def count_empty_cell_in_range(self, sheet_name="", xyxy=""):
		"""
		영역안의 빈셀의 갯수를 계산
		빈셀의 의미 : None인것
		"""
		self.menu_dic['count_emptycell'] = {'표시여부': 'x', '그리드메뉴': ['count', 'emptycell', '없음'],
											'실행메뉴': ['count', 'emptycell', '']}
		x1, y1, x2, y2 = self.check_address_value(xyxy)

		temp_result = 0
		for y in range(y1, y2 + 1):
			for x in range(x1, x2 + 1):
				cell_value = self.read_value_in_cell(sheet_name, [x, y])
				if cell_value == None:
					self.paint_color(sheet_name, [x, y], 16)
					temp_result = temp_result + 1
		return temp_result

	def count_empty_xline_in_range(self, sheet_name="", xyxy=""):
		"""
		count_emptycols(sheet_name="", xyxy)
		선택한영역에서 x줄의 값이 없으면 y줄을 삭제한다
		"""
		self.menu_dic['count_emptycols'] = {'표시여부': '필요', '그리드메뉴': ['delete', 'emptycols', '없음'],
											'실행메뉴': ['delete', 'emptycols', '']}
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)

		for x in range(x2, x1, -1):
			x_new = self.change_num_char(x)
			changed_address = str(x_new) + ":" + str(x_new)
			num = self.xlapp.WorksheetFunction.CountA(sheet_object.Range(changed_address))
			if num == 0:
				self.delete_cols(sheet_name, x)

	def count_empty_yline_in_range(self, sheet_name="", xyxy=""):
		"""
		count_emptyrows(sheet_name="", xyxy)
		선택한영역에서 x줄의 값이 없으면 x줄을 삭제한다
		"""
		self.menu_dic['count_emptyrows'] = {'표시여부': '필요', '그리드메뉴': ['delete', 'emptyrows', '없음'],
											'실행메뉴': ['delete', 'emptyrows', '']}
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)

		for y in range(y2, y1, -1):
			changed_address = str(y) + ":" + str(y)
			num = self.xlapp.WorksheetFunction.CountA(sheet_object.Range(changed_address))
			if num == 0:
				self.delete_yyline(sheet_name, y)

	def count_max_x_y(self):
		"""
		각 엑셀 버전마다 가로, 세로의 크기가 틀리기 때문에 전체를 설정할때를 나타낼려고 합니다
		엑셀에서는 전체 영역을 주소형태로 나타낼때 $1:$1048576와같이 나타내고있읍니다

		:return:
		"""
		sheet_object = self.get_sheet_object_for_activesheet()
		self.max_x = sheet_object.Rows.Count
		self.max_y = sheet_object.Columns.Count
		return [self.max_x, self.max_y]

	def count_same_value_in_range(self, sheet_name="", xyxy=""):
		"""
		 입력값 - 입력값없이 사용가능
		 선택한 영역의 반복되는 갯수를 구한다
		 - 선택한 영역에서 값을 읽어온다
		 - 사전으로 읽어온 값을 넣는다
		 - 열을 2개를 추가해서 하나는 값을 다른하나는 반복된 숫자를 넣는다


		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		range_object = self.get_range_object_by_xyxy(sheet_name, xyxy)

		all_data = self.read_value_in_range("", [x1, y1, x2, y2])
		py_dic = {}
		# 읽어온 값을 하나씩 대입한다
		for line_data in all_data:
			for one_data in line_data:
				# 키가와 값을 확인
				if one_data in py_dic:
					py_dic[one_data] = py_dic[one_data] + 1
				else:
					py_dic[one_data] = 1
		self.insert_yyline(sheet_name, 1)
		self.insert_yyline(sheet_name, 1)
		dic_list = list(py_dic.keys())
		for no in range(len(dic_list)):
			sheet_object.Cells(no + 1, 1).Value = dic_list[no]
			sheet_object.Cells(no + 1, 2).Value = py_dic[dic_list[no]]

	def count_shape_in_sheet(self, sheet_name):
		"""
		선택한 시트안의 도형의 갯수

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:return: 갯수
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		result = sheet_object.Shapes.Count
		return result

	def count_sheet(self):
		"""
		시트의 갯수를 돌려준다
		"""
		return self.xlbook.Worksheets.Count

	def count_workbook(self):
		"""
		열려있는 워크북의 갯수
		"""
		result = self.xlapp.Workbooks.Count
		return result

	def count_worksheet(self):
		"""
		시트의 갯수를 돌려준다
		"""
		return self.xlbook.Worksheets.Count

	def cut_number_for_float_data_by_no_of_under_point(self, no_of_under_point=3):
		"""
		선택영역안의 모든 숫자중에서, 입력받은 소숫점아래 몇번째부터, 값을 아예 삭제하는것

		:param no_of_under_point:
		"""
		times = 10 ** no_of_under_point
		x1, y1, x2, y2 = self.read_address_for_selection()
		for x in range(x1, x2 + 1):
			for y in range(y1, y2 + 1):
				one_value = self.read_value_in_cell("", [x, y])
				try:
					one_value = math.floor(float(one_value) * times) / times
					self.write_value_in_cell("", [x, y], one_value)
				except:
					pass

	def cut_range(self, sheet_name="", xyxy=""):
		"""
		영역을 잘라내기 하는 것

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		:return:
		"""
		range_object = self.get_range_object_by_xyxy(sheet_name, xyxy)
		range_object.Cut()

	def delete_all_empty_sheet(self):
		"""
		워크북에서 빈 시트를 전부 삭제하는 것
		"""
		all_sheet_name = self.read_all_sheet_name()
		for one_sheet_name in all_sheet_name:
			check_sheet = self.is_empty_sheet(one_sheet_name)
			if check_sheet:
				self.delete_sheet_by_name(one_sheet_name)

	def delete_all_line_in_range(self, sheet_name="", xyxy=""):
		"""
		영역의 모든선을 지운다

		:param sheet_name: 시트이름
		:param xyxy: [1,1,2,2]
		:return:
		"""
		range_object = self.get_range_object_by_xyxy(sheet_name, xyxy)

		for each in [5, 6, 7, 8, 9, 10, 11, 12]:
			range_object.Borders(each).LineStyle = -4142

	def delete_all_range_name(self):
		"""
		모든 rangename을 삭제하는 것

		"""
		aaa = self.xlapp.Names
		for one in aaa:
			ddd = str(one.Name)
			if ddd.find("!") < 0:
				# print("삭제중인 이름영역 -> ", ddd)
				self.xlbook.Names(ddd).Delete()

	def delete_all_shape_in_sheet(self, sheet_name):
		"""
		시트안의 모든 객체를 삭제하는 것

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		drawings_nos = sheet_object.Shapes.Count

		if drawings_nos > 0:
			for num in range(drawings_nos, 0, -1):
				# Range를 앞에서부터하니 삭제하자마자 번호가 다시 매겨져서, 뒤에서부터 삭제하니 잘된다
				sheet_object.Shapes(num).Delete()
		return drawings_nos

	def delete_color_in_range(self, sheet_name="", xyxy=""):
		"""
		선택한 영역안의 색을 지우는 것

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		"""
		range_object = self.get_range_object_by_xyxy(sheet_name, xyxy)

		range_object.Interior.Pattern = -4142
		range_object.Interior.TintAndShade = 0
		range_object.Interior.PatternTintAndShade = 0

	def delete_continuous_same_value_in_range(self, sheet_name="", xyxy=""):
		"""
		대상 : 선택한 영역
		밑으로 같은 값들이 있으면 지우는것

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		"""

		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)

		tuple_2d = self.read_range(sheet_name, xyxy)
		list_2d = self.change_tuple_2d_to_list_2d(tuple_2d)
		print(list_2d)
		#list_2d = self.util.change_tuple_to_list_2d(sheet_name, xyxy)

		for y in range(len(list_2d[0])):
			old_value = ""
			for x in range(len(list_2d)):
				current_value = list_2d[x][y]
				if old_value == current_value:
					list_2d[x][y] = ""
				else:
					old_value = list_2d[x][y]
		sheet_object.Range(sheet_object.Cells(x1, y1), sheet_object.Cells(x2, y2)).Value = list_2d

	def delete_each_cell_value_from0toN_in_range(self, sheet_name, xyxy, num):
		"""
		앞에서부터 N개까지의 글자를 삭제하는것

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		:param num: 숫자
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)

		for x in range(x1, x2 + 1):
			for y in range(y1, y2 + 1):

				one_value = sheet_object.Cells(x, y).Value2
				if one_value != "" or one_value != None or one_value != None:
					sheet_object.Cells(x, y).Value = one_value[int(num):]

	def delete_empty_xline_in_range(self, sheet_name="", xyxy=""):
		"""
		현재 선택된 영역안에서 x라인이 모두 빈것을 삭제하는것

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		range_object = self.get_range_object_by_xyxy(sheet_name, xyxy)

		for x in range(x2, x1, -1):
			changed_address = str(x) + ":" + str(x)
			num = self.xlapp.WorksheetFunction.CountA(sheet_object.Range(changed_address))
			if num == 0:
				sheet_object.Rows(changed_address).Delete()

	def delete_empty_yline_in_range(self, sheet_name="", xyxy=""):
		"""
		현재 선택된 영역안에서 y라인이 모두 빈것을 삭제하는것

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)

		for y in range(y2, y1, -1):
			cha_y = self.change_num_to_char(y)
			changed_address = str(cha_y) + ":" + str(cha_y)
			num = self.xlapp.WorksheetFunction.CountA(sheet_object.Range(changed_address))
			if num == 0:
				sheet_object.Columns(changed_address).Delete()

	def delete_file(self, old_path):
		"""
		화일삭제

		:param old_path:
		:return:
		"""
		old_path = self.util.check_file_path(old_path)
		os.remove(old_path)

	def delete_from_n_words_01(self, sheet_name, xyxy, num):
		"""
		선택한 영역에서 각셀마다 왼쪽에서 N번째까지의 글자삭제하기
		"""
		x1, y1, x2, y2 = self.check_address_value(xyxy)

		for x in range(x1, x2 + 1):
			for y in range(y1, y2 + 1):
				current_data = str(self.read_cell_value(sheet_name, [x, y]))
				if current_data == "" or current_data == None or current_data == None:
					pass
				else:
					self.write_cell_value(sheet_name, [x, y], current_data[int(num):])

	def delete_jf_sql_from_found_to_end_for_selection(self, jf_sql):
		"""
		처음 찾은 자료의 오른쪽의 모든 자료를 삭제하는것

		:param jf_sql:
		:return:
		"""
		xyxy = self.read_address_for_selection()
		for x in range(xyxy[0], xyxy[2] + 1):
			for y in range(xyxy[1], xyxy[3] + 1):
				value = self.read_value_in_cell("", [x, y])
				aaa = self.xyre.search_all_with_jf_sql(jf_sql, value)
				if aaa:
					temp = value[:int(aaa[0][2])]
				self.write_value_in_cell("", [x, y], temp)
				print(aaa, temp)

	def delete_line_color_in_range(self, sheet_name="", xyxy=""):
		"""
		영역안의 라인의 색을 지우는 것

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		"""
		range_object = self.get_range_object_by_xyxy(sheet_name, xyxy)

		range_object.Interior.Pattern = 0
		range_object.Interior.PatternTintAndShade = 0

	def delete_link_in_range(self, sheet_name="", xyxy=""):
		"""
		선택된 영역안의 => 링크를 삭제하는 것

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		"""
		range_object = self.get_range_object_by_xyxy(sheet_name, xyxy)
		range_object.Hyperlinks.Delete()

	def delete_memo_in_range(self, sheet_name="", xyxy=""):
		"""
		선택된 영역안의 => 메모를 삭제하는 것

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		"""
		range_object = self.get_range_object_by_xyxy(sheet_name, xyxy)
		range_object.ClearComments()

	def delete_panthom_range_name_in_workbook(self):
		"""
		이름영역중에서 연결이 끊긴것을 삭제하는 것
		"""
		cnt = self.xlapp.Names.Count
		for num in range(1, cnt + 1):
			aaa = self.xlapp.Names(num).Name
			if aaa.find("!") < 0:
				self.xlapp.Names(aaa).Delete()

	def delete_range_name_by_name(self, range_name):
		"""
		입력한 영역의 이름을 삭제

		:param range_name: 영역이름
		"""
		result = self.xlbook.Names(range_name).Delete()
		return result

	def delete_same_value_in_range(self, sheet_name="", xyxy=""):
		"""
		영역안에서 같은것이 있으면 모두 지우고, 고유한것만 남기는것
		2개가 같으면 2개모두 지우는 것이다

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		"""
		temp_dic = {}
		temp = []
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)

		# 모든 자료의 반복 갯수와 셀주소를 저장한다
		for x in range(x1, x2 + 1):
			for y in range(y1, y2 + 1):
				value = sheet_object.Cells(x, y).Value2
				if value == None or value == "":
					pass
				else:
					if value in temp:
						sheet_object.Cells(x, y).Value = ""
					else:
						temp.append(value)

	def delete_same_value_in_range_by_many_same_column(self, sheet_name="", xyxy=""):
		"""
		같은 값을 지우는 것

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		"""
		self.delete_xxline_value_in_range_by_same_line(sheet_name, xyxy)

	def delete_shape_by_name(self, sheet_name, shape_name):
		"""
		객체의 이름으로 제거하는것

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param shape_name: 도형/그림객체의 이름
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		sheet_object.Shapes(shape_name).Delete()

	def delete_sheet_by_name(self, sheet_name):
		"""
		시트하나 삭제하기

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		"""
		try:
			sheet_object = self.check_sheet_name(sheet_name)
			self.xlapp.DisplayAlerts = False
			sheet_object.Delete()
			self.xlapp.DisplayAlerts = True
		except:
			pass

	def delete_sheet_by_no(self, input_no):
		"""
		앞에서부터 n번째의 시트를 삭제하는 것
		:param input_no:
		"""

		all_sheet_name_list = self.read_all_sheet_name()
		self.delete_sheet_by_name(all_sheet_name_list[input_no - 1])

	def delete_tab_color_for_sheet(self, sheet_name):
		"""
		시트탭의 색을 넣는것

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param input_scolor: 색이름
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		sheet_object.Tab.ColorIndex = -4142  # none : -4142,  xlAutomatic:-4105
		sheet_object.Tab.TintAndShade = 0

	def delete_value_in_cell(self, sheet_name="", xyxy=""):
		"""
		선택한 셀의 값을 삭제하는것

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		"""
		range_object = self.get_range_object_by_xyxy(sheet_name, xyxy)
		range_object.ClearContents()

	def delete_value_in_range(self, sheet_name="", xyxy=""):
		"""
		delete_value(sheet_name="", xyxy)
		range의 입력방법은 [row1, col1, row2, col2]이다
		선택한 영역안의 모든 값을 지운다
		"""
		self.menu_dic['delete_value'] = {'표시여부': '필요', '그리드메뉴': ['delete', 'value', '없음'],
										 '실행메뉴': ['delete', 'value', '']}
		range_object = self.get_range_object_by_xyxy(sheet_name, xyxy)
		range_object.ClearContents()

	def delete_value_in_range_between_a_and_b(self, sheet_name, xyxy, input_list=["(", ")"]):
		"""
		선택된 영역안의 값중에서 괄호안의 값을 삭제하는 것

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		:param input_list: list type
		"""
		input_list = self.change_xylist_to_list(input_list)
		self.delete_value_in_range_between_specific_letter(sheet_name, xyxy, input_list)

	def delete_value_in_range_between_specific_letter(self, sheet_name, xyxy, input_list=["(", ")"]):
		"""
		선택된 영역안의 값중에서 입력된 특수문자 사이의 값을 삭제하는 것
		입력자료의 두사이의 자료를 포함하여 삭제하는것
		예: abc(def)gh ==>abcgh

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		:param input_list: ["(",")"]
		"""
		input_list = self.change_xylist_to_list(input_list)

		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		range_object = self.get_range_object_by_xyxy(sheet_name, xyxy)

		input_list[0] = str(input_list[0]).strip()
		input_list[1] = str(input_list[1]).strip()

		special_char = ".^$*+?{}[]\|()"
		# 특수문자는 역슬래시를 붙이도록
		if input_list[0] in special_char: input_list[0] = "\\" + input_list[0]
		if input_list[1] in special_char: input_list[1] = "\\" + input_list[1]
		re_basic = str(input_list[0]) + ".*" + str(input_list[1])

		# 찾은값을 넣을 y열을 추가한다
		new_x = int(x2) + 1
		self.insert_yline(sheet_name, new_x)
		for y in range(y1, y2 + 1):
			temp = ""
			for x in range(x1, x2 + 1):
				one_value = sheet_object.Cells(x, y).Value2
				result_list = re.findall(re_basic, str(one_value))

				if result_list == None or result_list == []:
					pass
				else:
					temp = temp + str(result_list)
					self.paint_cell_by_scolor("", [x, y], "yel++")
			sheet_object.Cells(y, new_x).Value = temp

	def delete_value_in_range_by_step(self, sheet_name, xyxy, step_no=""):
		"""
		예전자료를 위해서 남겨 놓음
		선택자료중 n번째 가로열의 자료를 값만 삭제하는것
		일하다보면 3번째 줄만 삭제하고싶은경우가 있다, 이럴때 사용하는 것이다

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		:param step_no: 번호, 반복되는 횟수의 번호
		"""
		self.sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)

		for x in range(x1, x2 + 1):
			if divmod(x - x1 + 1, step_no)[1] == 0:
				self.sheet_object.Range(self.sheet_object.Cells(x, y1), self.sheet_object.Cells(x, y2)).ClearContents()

	def delete_value_in_usedrange(self, sheet_name):
		"""
		자주사용하는 것 같아서 usedrange의 값을 지우는것을 만들어 보았다
		2005-02-18
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		temp_range = self.read_usedrange_address(sheet_name)
		sheet_object.Range(temp_range[2]).ClearContents()

	def delete_vba_module(self, module_name_list):
		"""
		열려있는 화일안에서 입력리스트의 메크로를 삭제를 하는 것

		:param module_name_list:리스트형, 메크로 모듈이름
		"""
		for module_name in module_name_list:
			xlmodule = self.xlbook.VBProject.VBComponents(module_name)
			self.xlbook.VBProject.VBComponents.Remove(xlmodule)

	def delete_xline(self, sheet_name, xx=""):
		"""
		선택한영역에서 x줄의 값이 없으면 x줄을 삭제한다

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xx: [2,4], 2~4까지의 x줄
		"""
		self.sheet_object = self.check_sheet_name(sheet_name)
		new_xx = self.check_xx_address(xx)
		self.sheet_object.Rows(str(new_xx[0]) + ':' + str(new_xx[1])).Delete()

	def delete_xline_in_range_by_step(self, sheet_name, xyxy, step_no):
		"""
		선택영역안의 => 선택한 n번째 가로행을 삭제한다. 값만 삭제하는것이 아니다
		위에서부터 삭제가 되게 만든것

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		:param step_no: 번호, 반복되는 횟수의 번호
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		range_object = self.get_range_object_by_xyxy(sheet_name, xyxy)

		del_no = 0  # 삭제된 줄수
		total_no = 1  # 천체 라인수
		for x in range(x1, x2 + 1):
			if x2 == total_no:
				break
			if divmod(total_no, step_no)[1] == 0:
				current_x = total_no - del_no
				self.delete_xline(sheet_name, [current_x, current_x])
				del_no = del_no + 1
			total_no = total_no + 1

	def delete_xline_value_in_range_by_step(self, sheet_name, xyxy, step_no):
		"""
		삭제 : 2 ==> 기존의 2번째 마다 삭제 (1,2,3,4,5,6,7 => 1,3,5,7)
		삭제 : 선택자료중 n번째 세로줄의 자료를 값만 삭제하는것
		일하다보면 3번째 줄만 삭제하고싶은경우가 있다, 이럴때 사용하는 것

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		:param step_no: 번호, 반복되는 횟수의 번호
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		range_object = self.get_range_object_by_xyxy(sheet_name, xyxy)

		for x in range(x1, x2 + 1):
			if divmod(x - x1 + 1, step_no)[1] == 0:
				sheet_object.Range(sheet_object.Cells(x, y1),
									sheet_object.Cells(x, y2)).ClearContents()

	def delete_xxline_in_sheet(self, sheet_name, xx=""):
		"""
		선택한영역에서 x줄의 값이 없으면 x줄을 삭제한다

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xx: [2,4], 2~4까지의 x줄
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		new_xx = self.check_xx_address(xx)
		sheet_object.Rows(str(new_xx[0]) + ':' + str(new_xx[1])).Delete()

	def delete_xxline_value_in_range_by_same_line(self, sheet_name="", xyxy=""):
		"""
		한줄씩 비교를 해서, 줄의 모든 값이 똑같으면 처음것을 제외하고 다음 자료부터 값만 삭제하는 것이다

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		range_object = self.get_range_object_by_xyxy(sheet_name, xyxy)

		all_values = self.read_value_in_range(sheet_name, xyxy)

		# same_nos = self.get_nos_in_input_list_2d_by_same_xline(all_values)
		for no in range(len(all_values)):
			sheet_object.Range(sheet_object.Cells(no + x1, y1),
								sheet_object.Cells(no + x1, y2)).ClearContents()

	def delete_yline_in_range_by_same_xxline(self, sheet_name, xyxy, input_list):
		"""
		delete_steplist(sheet_name="", xyxy, input_list)
		선택한 영역중 여러부분이 같을 때 그 열을 삭제하는것
		입력값 : 1,3,4 (이 3개의 자료가 모두 같은것만 삭제하기)
		코드 : 1과 3과 4의 값을 모두 특수문자를 사용하여 연결한후 이것을 사전의
			  키로 만들어서 비교하여 선택한다
			  각개개는 틀리지만 합쳤을때 같아지는 형태가 있을수 있어 특수문자를 포함한다
			  예 : 123, 45 과 12, 345
		"""
		self.menu_dic['delete_yline_condition_by_same_xxline'] = {'표시여부': '필요',
																  '그리드메뉴': ['delete', 'row', '[1,3,4]열의 값이 같은 x열을 삭제'],
																  '실행메뉴': ['delete', 'row', 'condition_by_same_xxline']}
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		range_object = self.get_range_object_by_xyxy(sheet_name, xyxy)
		base_data_1 = self.read_value(sheet_name, xyxy)
		base_data_2 = base_data_1
		same_num = len(input_list)
		del_list = []
		for y in range(y1, y2 + 1):
			line_data = base_data_1[y]
			for x_2 in range(x1 + 1, x2 + 1):
				count = 0
				com_one_line = base_data_1[x_2]
				for one_num in input_list:
					if line_data[one_num] == com_one_line[one_num]:
						count = count + 1
				if count == same_num:
					del_list.append(x_2)
					sheet_object.Range(sheet_object.Cells(y1 + y, x1), sheet_object.Cells(y1 + y, x2)).ClearContents()

	def delete_yline_in_range_by_step(self, sheet_name, xyxy, step_no):
		"""
		선택한 영역안의 세로줄중에서 선택한 몇번째마다 y라인을 삭제하는것
		(선택한 영역안에서 3번째 마다의 y라인을 삭제하는것)

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		:param step_no: 번호, 반복되는 횟수의 번호
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		range_object = self.get_range_object_by_xyxy(sheet_name, xyxy)

		current_no = 0
		for y in range(1, y2 - y1 + 1):
			mok, namuji = divmod(y, int(step_no))
			if namuji == 0:
				self.delete_yline(sheet_name, [current_no + y1, current_no + y1])
			else:
				current_no = current_no + 1

	def delete_yline_value_in_range_by_step(self, sheet_name, xyxy, step_no):
		"""
		선택한 영역안의 세로줄중에서 선택한 몇번째마다 y라인의 값을 삭제하는것
		(선택한 영역안에서 3번째 마다의 y라인의 값을 삭제하는것)

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		:param step_no: 번호, 반복되는 횟수의 번호
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		range_object = self.get_range_object_by_xyxy(sheet_name, xyxy)

		for y in range(y1, y2 + 1):
			if divmod(y - y1 + 1, step_no)[1] == 0:
				sheet_object.Range(sheet_object.Cells(x1, y), sheet_object.Cells(x2, y)).ClearContents()

	def delete_yline_when_same_multi_x_lines(self, sheet_name, xyxy, input_list):
		"""
		영역에서 위에서부터 찾아내려오면서 입력으로 받은
		[1,3,5]값이 다 같은 것만 삭제하는것

		:param self:
		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		:param input_list:
		:return:
		"""
		input_list = self.change_xylist_to_list(input_list)

		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		range_object = self.get_range_object_by_xyxy(sheet_name, xyxy)

		data_dic = {}
		del_no = 0

		for x in range(x1, x2 + 1):
			new_x = x - del_no
			one_data = ""
			for a in input_list:
				new_y = y1 + int(a) - 1
				one_data = one_data + str(self.read_value_in_cell(sheet_name, [new_x, new_y])) + "#!$@"

			if one_data in data_dic.keys():
				self.delete_xline(sheet_name, new_x)
				del_no = del_no + 1
				data_dic[one_data] = data_dic[one_data] + 1
			else:
				data_dic[one_data] = 1

	def delete_ylines_in_list_2d_by_line_nos(self, input_list_2d, no_list):
		"""
		입력으로받은 번호리스트를 기준으로 2차원의 자료를 삭제하는 것

		입력형태 : 2차원리스트, [2,5,7]
		"""
		no_list.sort()
		no_list.reverse()
		for one in no_list:
			for x in range(len(input_list_2d)):
				del input_list_2d[x][one]
		return input_list_2d

	def delete_yyline_in_sheet(self, sheet_name, yy=""):
		"""
		선택한영역에서 x줄의 값이 없으면 x줄을 삭제한다
		여러줄의 라인이 들어오더라도, 한줄만 삭제하는 것이다

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param yy: 세로줄의 사작과 끝 => [3,7]
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		y1, y2 = self.check_yy_address(yy)

		sheet_object.Columns(y1 + ':' + y1).Delete()

	def differ_position_for_2list_2d(self, list_2d_1, list_2d_2, colored=False):
		"""
		두개의 리스트가 다른 부분을 찾는데, 기준은 앞의것을 기준으로 한다

		:param list_2d_1:
		:param list_2d_2:
		:param colored:
		:return:
		"""
		result = []
		for list_1d, ix in enumerate(list_2d_1):
			for one_data, iy in enumerate(list_1d):
				if list_2d_1[ix][iy] == list_2d_2[ix][iy]:
					pass
				else:
					result.append([ix + 1, iy + 1])
					if colored:
						self.paint_cell("", [ix + 1][iy + 1], "red++")

	def draw_bottom_line_in_range(self, sheet_name="basic", xyxy="basic", line_style="_", thickness="thin",
								  scolor="bla"):
		"""
		영역의 아랫쪽 라인을 그리기

		:param sheet_name:
		:param xyxy:
		:param line_style:
		:param thickness:
		:param scolor:
		:return:
		"""
		self.draw_line(sheet_name, xyxy, ["bottom", scolor, line_style, thickness])

	def draw_detail_line_in_range(self, **input):
		"""
		선택영역에서 선을 긋는것
		선긋기를 좀더 상세하게 사용할수 있도록 만든것
		밐의 base_data의 값들을 이용해서 입력하면 된다

		:param input:
		"""
		enum_line = self.vars["end_style_vs_enum"]
		base_data = self.vars["dic_base_cell_data"]
		# 기본자료에 입력받은값을 update하는것이다
		sheet_object = self.check_sheet_name("")
		base_data.update(input)
		sheet = self.check_sheet_name(base_data["sheet_name"])
		set_line = sheet_object.Shapes.AddLine(base_data["xyxy"][0], base_data["xyxy"][1], base_data["xyxy"][2],
												base_data["xyxy"][3])
		set_line.Select()
		set_line.Line.ForeColor.RGB = base_data["color"]
		set_line.Line.DashStyle = enum_line[base_data["line_style"]]
		set_line.Line.Weight = base_data["thickness"]
		set_line.Line.Transparency = base_data["transparency"]
		# 엑셀에서는 Straight Connector 63의 형태로 이름이 자동적으로 붙여진다
		set_line.Line.BeginArrowheadStyle = enum_line[base_data["head_style"]]
		set_line.Line.BeginArrowheadLength = enum_line[base_data["head_length"]]
		set_line.Line.BeginArrowheadWidth = enum_line[base_data["head_width"]]
		set_line.Line.EndArrowheadStyle = enum_line[base_data["tail_style"]]  # 화살표의 머리의 모양
		set_line.Line.EndArrowheadLength = enum_line[base_data["tail_length"]]  # 화살표의 길이
		set_line.Line.EndArrowheadWidth = enum_line[base_data["tail_width"]]  # 화살표의 넓이
		result = set_line.Name
		return set_line

	def draw_detail_line_in_range_with_object(self, **input):
		"""
		선택영역에서 선을 긋는것
		선긋기를 좀더 상세하게 사용할수 있도록 만든것
		밐의 base_data의 값들을 이용해서 입력하면 된다

		:param input:
		"""
		enum_line = self.vars["end_style_vs_enum"]
		base_data = self.vars["dic_base_cell_data"]
		# 기본자료에 입력받은값을 update하는것이다
		sheet_object = self.check_sheet_name("")
		base_data.update(input)
		sheet = self.check_sheet_name(base_data["sheet_name"])
		set_line = sheet_object.Shapes.AddLine(base_data["xyxy"][0], base_data["xyxy"][1], base_data["xyxy"][2],
												base_data["xyxy"][3])
		set_line.Select()
		set_line.Line.ForeColor.RGB = base_data["color"]
		set_line.Line.DashStyle = enum_line[base_data["line_style"]]
		set_line.Line.Weight = base_data["thickness"]
		set_line.Line.Transparency = base_data["transparency"]
		# 엑셀에서는 Straight Connector 63의 형태로 이름이 자동적으로 붙여진다
		set_line.Line.BeginArrowheadStyle = enum_line[base_data["head_style"]]
		set_line.Line.BeginArrowheadLength = enum_line[base_data["head_length"]]
		set_line.Line.BeginArrowheadWidth = enum_line[base_data["head_width"]]
		set_line.Line.EndArrowheadStyle = enum_line[base_data["tail_style"]]  # 화살표의 머리의 모양
		set_line.Line.EndArrowheadLength = enum_line[base_data["tail_length"]]  # 화살표의 길이
		set_line.Line.EndArrowheadWidth = enum_line[base_data["tail_width"]]  # 화살표의 넓이
		return set_line

	def draw_inner_line_in_range(self, sheet_name, xyxy, line_style="basic", thickness="basic", color="blu"):
		"""
		영역에서 가로와세로 라인의 선을 긎는것

		:param sheet_name:
		:param xyxy:
		:param line_style:
		:param thickness:
		:param color:
		:return:
		"""
		self.draw_line_one_in_range(sheet_name, xyxy, line_style, thickness, color, 11)

	def draw_inner_xline_in_range(self, sheet_name, xyxy, line_style="basic", thickness="basic", scolor="basic",
								  setup=False):
		"""
		영역에서 안쪽 가로 라인의 선을 긎는것

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		:param line_style: 선의 스타일, (점선, 실선등)
		:param thickness: 선의 두께
		:param color: scolor 형식의 색이름, 빨강++
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		range_object = self.get_range_object_by_xyxy(sheet_name, xyxy)

		if setup:
			# setup의 자료를 이용할려고 할때
			v1 = self.vars["range_line"]["left"]["color"]
			v2 = self.vars["range_line"]["left"]["weight"]
			v3 = self.vars["range_line"]["left"]["style"]
		else:
			v1 = self.color.change_scolor_to_rgbint(scolor)
			v2 = self.vars["line"][thickness]
			v3 = self.vars["line"][line_style]

		range_object.Borders(12).Color = v1
		range_object.Borders(12).Weight = v2
		range_object.Borders(12).LineStyle = v3

	def draw_inner_yline_in_range(self, sheet_name, xyxy, line_style="basic", thickness="basic", color="blu"):
		"""
		영역에서 안쪽 세로 부분의 선을 긎는것

		:param sheet_name:
		:param xyxy:
		:param line_style:
		:param thickness:
		:param color:
		:return:
		"""
		self.draw_line(sheet_name, xyxy, ["|"], line_style, thickness, color)

	def draw_left_line_in_range(self, sheet_name, xyxy, line_style="basic", thickness="basic", color="blu"):
		"""
		영역에서 왼쪽 부분의 선을 긎는것

		:param sheet_name:
		:param xyxy:
		:param line_style:
		:param thickness:
		:param color:
		:return:
		"""
		self.draw_line(sheet_name, xyxy, ["left"], line_style, thickness, color)

	def draw_line(self, sheet_name, xyxy, *input_list):
		"""
		 draw_range_line(sheet_name="", xyxy, input_list) : [선의위치, 라인스타일, 굵기, 색깔]
		 입력예 : [7,1,2,1], ["left","-","t0","bla"]

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:param input_list: list type
		:return:
		 """
		self.check_sheet_name_n_xyxy(sheet_name, xyxy)
		temp_color = "bla"
		temp_position = [7, 8, 9, 10]
		temp_thickness = "t-1"
		temp_line = "-"

		for one in input_list:
			if type(one) == type([]) or type(one) == type(()):
				temp_position = one
			elif one in self.vars["check_line_position"].keys():
				temp_position = self.vars["check_line_position"][one]
			elif one in self.vars["check_color_name"].keys():
				temp_color = self.vars["check_color_name"][one]
			elif one in self.vars["check_line_style"].keys():
				temp_line = self.vars["check_line_style"][one]
			elif one in self.vars["check_line_thickness"].keys():
				temp_thickness = self.vars["check_line_thickness"][one]

			aaa = self.color.check_input_scolor(one)
			if aaa:
				temp_color = one

		for abc in temp_position:
			self.range_object.Borders(abc).Color = self.color.change_scolor_to_rgbint(temp_color)
			self.range_object.Borders(abc).Weight = temp_thickness
			self.range_object.Borders(abc).LineStyle = temp_line

	def draw_line_basic(self, sheet_name, xyxy, *para_list):
		self.draw_line(sheet_name, xyxy, *para_list)

	def draw_line_for_easy(self, sheet_name, xyxy, *para_list):
		self.draw_line(sheet_name, xyxy, *para_list)

	def draw_line_for_selection_as_well_used_2(self):
		"""
		자주사용하는 테이블형식의 선을 그리는 것

		:return:
		"""
		x1, y1, x2, y2 = self.check_address_value("")
		range_head = [x1, y1, x1, y2]
		range_body = [x1 + 1, y1, x2 - 1, y2]
		range_tail = [x2, y1, x2, y2]
		range_outline = [x1, y1, x2, y2]

		self.draw_line("", range_outline, [[7, 8, 9, 10], "bla", "실선", "t1"])
		self.draw_line("", range_body, [[11], "bla", "실선", "t-1"])
		self.draw_line("", range_outline, [[12], "bla", ".", "t-1"])
		self.draw_line("", range_head, [[9], "bla", "실선", "t0"])
		self.draw_line("", range_tail, [[8], "bla", "실선", "t0"])

	def draw_line_in_range(self, sheet_name="", xyxy="", position="", scolor="", line_style="", thickness=""):
		"""
		입력예 : [선의위치, 색깔, 라인스타일, 굵기] ==> [7,1,2,1], "", "",""
		""으로 된것이 기본으로 설정하는 것이다
		"l": left, "t": top, "b": bottom, "r": right, "h": horizental, "v": vertical, "a": all,"o": outside,"/": "/","\\": "\",
		""으로 된것이 기본으로 설정하는 것이다
		color = rgb 값
		"""
		line_position = self.vars["dic_선위치_vs_index번호"]
		line_thickness_dic = self.vars["dic_선굵기_vs_번호"]
		line_style_dic = self.vars["dic_선형태_vs_번호"]

		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)

		my_range = sheet_object.Range(sheet_object.Cells(x1, y1), sheet_object.Cells(x2, y2))
		#print(scolor)
		rgb_list = self.color.change_scolor_to_rgb(scolor)
		colorint = self.color.change_rgb_to_rgbint(rgb_list)
		aa = []
		if type(position) == type([]):
			for one in position:
				aa.extend(line_position[one])
		else:
			aa.extend(line_position[position])

		for po_no in aa:
			my_range.Borders(po_no).Color = colorint
			my_range.Borders(po_no).Weight = line_thickness_dic[str(thickness)]
			my_range.Borders(po_no).LineStyle = line_style_dic[line_style]

	def draw_line_in_range_as_basic(self, sheet_name="", xyxy="", position="all", scolor="black", line_style="basic", thickness="thin"):
		"""
		입력예 : [선의위치, 색깔, 라인스타일, 굵기] ==> [7,1,2,1], "", "",""
		""으로 된것이 기본으로 설정하는 것이다
		"l": left, "t": top, "b": bottom, "r": right, "h": horizental, "v": vertical, "a": all,"o": outside,"/": "/","\\": "\",
		""으로 된것이 기본으로 설정하는 것이다
		color = rgb 값
		"""
		line_position = self.vars["dic_선위치_vs_index번호"]
		line_thickness_dic = self.vars["dic_선굵기_vs_번호"]
		line_style_dic = self.vars["dic_선형태_vs_번호"]

		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)

		my_range = sheet_object.Range(sheet_object.Cells(x1, y1), sheet_object.Cells(x2, y2))
		#print(scolor)
		rgb_list = self.color.change_scolor_to_rgb(scolor)
		colorint = self.color.change_rgb_to_rgbint(rgb_list)
		aa = []
		if type(position) == type([]):
			for one in position:
				aa.extend(line_position[one])
		else:
			aa.extend(line_position[position])

		for po_no in aa:
			my_range.Borders(po_no).Color = colorint
			my_range.Borders(po_no).Weight = line_thickness_dic[str(thickness)]
			my_range.Borders(po_no).LineStyle = line_style_dic[line_style]

	def draw_line_in_range_as_basic_1(self, sheet_name="", xyxy=""):
		"""
		선택된 영역을 기본 설정된 선의 형태로 그리는 것이다

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		:param position:
		:param scolor:
		:param line_style:
		:param thickness:
		:return:
		"""

		position = "all"
		scolor = "bla"
		line_style = ""
		thickness = "thin"
		self.draw_line_basic(sheet_name, xyxy, position, scolor, line_style, thickness)

	def draw_line_in_range_as_pxyxy(self, sheet_name, xyxy, rgb_list):
		"""
		선택영역에서 선을 긋는것
		pixel을 기준으로 선긋기
		선을 그을때는 위치와 넓이 높이로 긋는데, change_xyxy_to_pxyxy을 사용하면 셀위치를 그렇게 바꾸게 만든다

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy:
		:param rgb_list:
		"""
		rgb_list = self.change_xylist_to_list(rgb_list)

		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		range_object = self.get_range_object_by_xyxy(sheet_name, xyxy)
		pxyxy = self.change_xyxy_to_pxyxy([x1, y1, x2, y2])

		sheet_object.Shapes.AddLine(pxyxy[0], pxyxy[1], pxyxy[2], pxyxy[3]).Select()
		self.xlapp.Selection.ShapeRange.Line.ForeColor.RGB = self.color.change_rgb_to_rgbint(rgb_list)
		self.xlapp.Selection.ShapeRange.Line.Weight = 5

	def draw_line_with_for_speed(self, sheet_name="", xyxy="", position="", rgbint="", line_style="", thickness=""):
		"""
		영역안의 라인을 그리는것
		예제 : self.draw_line_with_speed("", [3, 3, 10, 10], [7, 8, 9], rgbint, 1, 1)
		파라미터 변수들의 기본값이 "" 의 뜻 : default value
		* boribori (pcell용 gui프로그램의 내장용 함수)에 사용가능

		:param sheet_name: sheet name
		:param xyxy: [1,1,2,3]
		:param position: all, outline...
		:param rgbint: color
		:param line_style: _, .,
		:param thickness: t0, t-1
		:return:
		"""
		range_object = self.get_range_object_by_xyxy(sheet_name, xyxy)
		for abc in position:
			range_object.Borders(abc).Color = int(rgbint)
			range_object.Borders(abc).Weight = int(thickness)
			range_object.Borders(abc).LineStyle = int(line_style)

	def draw_right_line_in_range(self, sheet_name, xyxy, line_style, thickness, scolor):
		"""
		영역에서 오른쪽 라인을 그리는 것

		:param sheet_name:
		:param xyxy:
		:param line_style:
		:param thickness:
		:param scolor:
		:return:
		"""
		self.menu_dic['draw_range_rightline'] = {'표시여부': '필요', '그리드메뉴': ['선그리기', 'range', '오른쪽에 선그리기'],
												 '실행메뉴': ['draw', 'range', 'rightline']}
		range_object = self.get_range_object_by_xyxy(sheet_name, xyxy)

		range_object.Borders(10).Color = self.color.change_scolor_to_rgbint(scolor)
		range_object.Borders(10).Weight = thickness
		range_object.Borders(10).LineStyle = line_style

	def draw_shape_line_in_sheet(self, sheet_name, xywh, xyxy_style=True):
		"""
		영역안의 도형라인을 그리는것
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		if xyxy_style:
			xywh = self.change_xyxy_to_pxyxy(xywh)
		left, top, width, height = xywh
		aaa = sheet_object.Shapes.AddConnector(1, left, top, left + width,
												top + height)  # aaa. Dash Style = msoLineDashDotDot
		# aaa.ForeColor.RGB = RGB(50, 0,128)
		size = xywh

	def draw_triangle(self, xyxy, per=100, reverse=1, size=100):
		"""
		직각삼각형
		정삼각형에서 오른쪽이나 왼쪽으로 얼마나 더 간것인지
		100이나 -100이면 직삼각형이다
		사각형은 왼쪽위에서 오른쪽 아래로 만들어 진다

		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		:param per:
		:param reverse:
		:param size:
		"""
		x1, y1, x2, y2 = xyxy
		width = x2 - x1
		height = y2 - y1
		lt = [x1, y1]  # left top
		lb = [x2, y1]  # left bottom
		rt = [x1, y2]  # right top
		rb = [x2, y2]  # right bottom
		tm = [x1, int(y1 + width / 2)]  # 윗쪽의 중간
		lm = [int(x1 + height / 2), y1]  # 윗쪽의 중간
		rm = [int(x1 + height / 2), y1]  # 윗쪽의 중간
		bm = [x2, int(y1 + width / 2)]  # 윗쪽의 중간
		center = [int(x1 + width / 2), int(y1 + height / 2)]

		result = [lb, rb, rt]
		return result

	def draw_user_style_01(self, sheet_name, xyxy, scolor="bla"):
		"""
		선택영역에서 선을 긋는것
		사용자가 만든 스타일의 선긋기

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		"""
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		head_count = 1  # head의 갯수
		tail_count = 1  # tail의 갯수

		range_head = [x1, y1, x1 + head_count - 1, y2]
		range_body = [x1 + head_count - 1, y1, x2 - tail_count + 1, y2]
		range_tail = [x2 - tail_count + 1, y1, x2, y2]
		range_outside = [x1, y1, x2, y2]

		line_list_head = [["o", scolor, "", "t-1"], ["h", scolor, "", "t-1"], ]
		line_list_body = [["v", scolor, ".", "t-1"], ["h", scolor, "", "t-1"], ]
		line_list_tail = [["o", scolor, "", "t-1"], ["h", scolor, "", "t-1"], ]
		line_list_outside = [["o", scolor, "", "t0"], ]

		# self.draw_line("", [12,12,17,17], ["all", "_", "가는", "pin---"])
		for one in line_list_head:
			self.draw_line(sheet_name, range_head, one)
		for one in line_list_tail:
			self.draw_line(sheet_name, range_tail, one)
		for one in line_list_body:
			self.draw_line(sheet_name, range_body, one)
		for one in line_list_outside:
			self.draw_line(sheet_name, range_outside, one)

	def draw_user_style_02(self, sheet_name, xyxy, scolor="bla"):
		"""
		선택영역에서 선을 긋는것
		사용자가 만든 스타일의 선긋기

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		"""
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		range_head = [x1, y1, x1, y2]
		range_body = [x1 + 1, y1, x2 - 1, y2]
		range_tail = [x2, y1, x2, y2]
		range_outside = [x1, y1, x2, y2]

		line_list_head = [["o", scolor, "", "t-1"], ["h", scolor, "", "t-1"], ]
		line_list_body = [["v", scolor, "", "t-2"], ["h", scolor, "", "t-1"], ]
		line_list_tail = [["o", scolor, "", "t-1"], ["h", scolor, "", "t-1"], ]
		line_list_outside = [["o", scolor, "", "t0"], ]

		for one in line_list_head:
			self.draw_line(sheet_name, range_head, one)
		for one in line_list_tail:
			self.draw_line(sheet_name, range_tail, one)
		for one in line_list_body:
			self.draw_line(sheet_name, range_body, one)
		for one in line_list_outside:
			self.draw_line(sheet_name, range_outside, one)

	def file_dialog(self):
		"""
		화일 다이얼로그를 불러오는 것
		"""
		filter = "Picture Files \0*.jp*;*.gif;*.bmp;*.png\0Text files\0*.txt\0"
		# filter = "Picture Files (*.jp*; *.gif; *.bmp; *.png),*.xls"
		result = win32gui.GetOpenFileNameW(InitialDir=os.environ["temp"],
											Filter=filter,
											Flags=win32con.OFN_ALLOWMULTISELECT | win32con.OFN_EXPLORER,
											File="somefilename",
											DefExt="py",
											Title="GetOpenFileNameW",
											FilterIndex=0)
		return result

	def filter_list_by_index(self, input_list, position_list):
		"""
		리스트로 넘오온 자료를 원하는 열만 추출하는것

		:param input_list:
		:param position_list:
		:return:
		"""

		input_list = self.change_xylist_to_list(input_list)
		position_list = self.change_xylist_to_list(position_list)

		result = []
		for list_1d in input_list:
			temp = []
			for one in position_list:
				temp.append(list_1d[one - 1])
			result.append(temp)
		return result

	def find_word_in_range(self, sheet_name="", xyxy="", input_text="입력필요"):
		"""
		영역안의 글자를 찾는다

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		:param input_text: 입력 text
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		range_object = self.get_range_object_by_xyxy(sheet_name, xyxy)

		first_range = range_object.Find(input_text)
		temp_range = first_range
		if first_range != None:
			while 1:
				temp_range = range_object.FindNext(temp_range)
				if temp_range == None or temp_range == first_range.Address:
					break
				else:
					temp_range = temp_range

	def find_value_in_range(self, sheet_name, xyxy, old_word, start_cell, value_or_fomular, part_or_whole=False,
							direction=1, direction_next=1, case=False, byte_type=False, cell_format=False):
		"""
		엑셀의 찾기 바꾸기 기능을 이용하는 것

		만약  * 또는 ? 기호가 포함된 데이터를 찾거나 수식에 포함하고 싶다면 해당 문자 앞에 ~(물결표)를 붙여주면 됩니다.

		찾기를 하는 것

		What	필수 검색할 문자열	 문자열이나 숫자 같은 모든 데이터 유형
		After  선택사항	검색을 시작할 셀  셀 주소
		LookIn 선택사항	검색에 수식, 값, 코맨트 사용  xlValues, xlFormulas, xlComments
		LookAt 선택사항	부분일치 또는 전체 일치  xlWhole, xlPart
		SearchOrder	 선택사항	검색할 순서 – 행 또는 열	 xlByRows, xlByColummns
		SearchDirection	 선택사항	검색할 방향 – 순방향 또는 역방향	 xlNext, xlPrevious
		MatchCase  선택사항	대소문자 구분 여부 True 또는 False
		MatchByte  선택사항	더블 바이트 문자 지원을 설치한 경우에만 사용(예: 중국어)  True 또는 False
		SearchFormat	선택사항	 셀 서식으로 검색 허용  True 또는 False
		"""
		range_object = self.get_range_object_by_xyxy(sheet_name, xyxy)

		range_object.Find(old_word, old_word, start_cell, value_or_fomular, part_or_whole, direction,
						  direction_next, case,
						  byte_type, cell_format)

	def get_4_edge_xy_for_xyxy(self, xyxy=[1, 2, 3, 4]):
		"""
		영역을 주면, 4개의 꼭지점을 돌려주는것
		기준은 왼쪽위부터 시계방향으로 돌아간다

		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		"""
		x1, y1, x2, y2 = xyxy
		result = [[x1, y1], [x1, y2], [x2, y2], [x2, y1]]
		return result

	def get_5_value_set_for_cell(self, sheet_name, xy=[]):
		"""
		엑셀에서 값의 형태로 나타나는 모든 5가지 형식을 돌려준다
		:param sheet_name:
		:param xy:
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		one_cell = sheet_object.Cells(xy[0], xy[1])
		result = {}
		result["value"] = one_cell.Value
		result["value2"] = one_cell.Value2
		result["formula"] = one_cell.Formula
		result["formular1c1"] = one_cell.FormulaR1C1
		result["text"] = one_cell.Text
		return result

	def get_address_for_all_empty_cell_in_range(self, sheet_name="", xyxy=""):
		"""
		영역안의 빈셀의 주소값을 묶어서 돌려준다
		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		:return:
		"""
		result = []
		x1, y1, x2, y2 = self.check_address_value(xyxy)

		list_2d = self.read_value_in_range(sheet_name, xyxy)
		for ix, list_1d in enumerate(list_2d):
			for iy, value in enumerate(list_1d):
				if list_2d[ix][iy] == "" or list_2d[ix][iy] == None:
					result.append([ix + x1, iy + y1])
		return result

	def get_address_for_range_name(self, input_range_name):
		"""
		이름영역의 주소형태를 분리해서, 자료를 만드는 것

		:param input_range_name: 이름영역
		:return:
		"""
		# print("--> ", input_range_name)
		sheet_obj = self.get_sheet_object("")

		range_address = sheet_obj.Range(input_range_name).Address

		sheet_name = self.read_activesheet_name()
		xyxy = self.check_address_value(range_address)
		return [range_address, sheet_name, xyxy]

	def get_address_for_right_end_n_bottom_from_cell(self, sheet_name, xy):
		"""
		특정셀을 기준으로 연속된 오른쪽과 아래쪽까지의 주소값

		:param sheet_name:
		:param xy:
		:return:
		"""
		x1, y1, x2, y2 = self.check_address_value(xy)
		result = []
		address_l = self.move_activecell_in_range_to_bottom(sheet_name, [x1, y1])
		result.append(address_l)
		address_2 = self.move_activecell_in_range_to_rightend(sheet_name, [x1, y1])
		result.append(address_2)
		return result

	def get_address_for_selection(self):
		"""
		선택된 영역의 주소값을 돌려준다
		"""
		result = ""
		temp_address = self.xlapp.Selection.Address
		temp_list = temp_address.split(",")
		if len(temp_list) == 1:
			result = self.check_address_value(temp_address)
		if len(temp_list) > 1:
			result = []
			for one_address in temp_list:
				result.append(self.check_address_value(one_address))
		return result

	def get_all_address_in_range_for_empty_cell(self, sheet_name="", xyxy=""):
		"""
		영역안의 빈셀의 주소값을 묶어서 돌려준다
		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		:return:
		"""
		result = []
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		list_2d = self.read_value_in_range(sheet_name, xyxy)
		for ix, list_1d in enumerate(list_2d):
			for iy, value in enumerate(list_1d):
				if list_2d[ix][iy] == "" or list_2d[ix][iy] == None:
					result.append([ix + x1, iy + y1])
		return result

	def get_all_filename_in_folder_by_extension_name(self, directory="./", filter_list=["pickle"]):
		"""
		아래의 함수가 여러 화일확장자도 가능하게 변경함
		"""
		all_files = os.listdir(directory)
		if filter_list == "*" or filter_list == "":
			file_names = all_files
		else:
			file_names = []
			for one in all_files:
				for ext in filter_list:
					if one.endswith(ext):
						file_names.append(one)
						break
		return file_names

	def get_all_range_name(self):
		"""
		모든 영역의 이름(rangename)을 돌려주는것
		"""
		names_count = self.xlbook.Names.Count
		result = []
		if names_count > 0:
			for aaa in range(1, names_count + 1):
				name_name = self.xlbook.Names(aaa).Name
				name_range = self.xlbook.Names(aaa)
				result.append([aaa, str(name_name), str(name_range)])
		return result

	def get_all_shape_name_for_selected_shape(self):
		"""
		도형의 이름 갖고오기 - 현재 선택된 객체의 이름을 갖고오는 것이다
		영역이면, 그냥 무시한다
		2024-01-11 : 조금 변경함

		"""
		result = []
		sel_shape_objects = self.xlapp.Selection.ShapeRange
		if sel_shape_objects.Count:
			for one_object in sel_shape_objects:
				shape_name = one_object.Name
				result.append(shape_name)
		return result

	def get_all_shape_name_in_sheet(self, sheet_name):
		"""
		현재 시트의 모든 객체의 이름에 대해서 갖고오는 것이다

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:return:
		"""
		result = []
		sheet_object = self.check_sheet_name(sheet_name)
		shape_ea = sheet_object.Shapes.Count
		if shape_ea > 0:
			for no in range(shape_ea):
				result.append(sheet_object.Shapes(no + 1).Name)

		return result

	def get_all_shape_name_in_workbook(self):
		"""
		엑셀화일안의 모든 그림객체에대한 이름을 갖고온다
		결과 : [시트이름, 그림이름]

		:return:
		"""
		result = []
		all_sheet_name = self.read_all_sheet_name()
		for sheet_name in all_sheet_name:
			all_shape_name = self.read_all_shape_names(sheet_name)
			if all_shape_name:
				for shape_name in all_shape_name:
					result.append([sheet_name, shape_name])
		return result

	def get_all_sheet_name(self):
		"""
		모든 워크시트의 이름을 읽어온다
		"""
		result = []
		for a in range(1, self.xlbook.Worksheets.Count + 1):
			result.append(self.xlbook.Worksheets(a).Name)
		return result

	def get_all_sheet_name_sort_by_position(self):
		"""
		워크시트의 모든 이름을 위치를 기준으로 정렬해서 돌려준다
		"""
		result = []
		for a in range(1, self.xlbook.Worksheets.Count + 1):
			result.append(self.xlbook.Worksheets(a).Name)
		return result

	def get_cell_object(self, sheet_name, xy=[7, 7]):
		"""
		셀의 객체를 갖고오는 것

		:param sheet_name:
		:param xy:
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		one_cell = sheet_object.Cells(xy[0], xy[1])
		return one_cell

	def get_current_path(self):
		"""
		현재 경로를 알아내는 것
		"""
		result = os.getcwd()
		return result

	def get_degree_for_shape(self, sheet_name, shape_no):
		"""
		도형의 각도를 읽는 것

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param shape_no: 이동시킬 도형 이름
		"""
		shape_object = self.get_shape_object(sheet_name, shape_no)
		result = shape_object.Rotation
		return result

	def get_diagonal_xy(self, xyxy=[5, 9, 12, 21]):
		"""
		좌표와 대각선의 방향을 입력받으면, 대각선에 해당하는 셀을 돌려주는것
		좌표를 낮은것 부터 정렬하기이한것 [3, 4, 1, 2] => [1, 2, 3, 4]

		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		"""
		result = []
		if xyxy[0] > xyxy[2]:
			x1, y1, x2, y2 = xyxy[2], xyxy[3], xyxy[0], xyxy[1]
		else:
			x1, y1, x2, y2 = xyxy

		x_height = abs(x2 - x1) + 1
		y_width = abs(y2 - y1) + 1
		step = x_height / y_width
		temp = 0

		if x1 <= x2 and y1 <= y2:
			# \형태의 대각선
			for y in range(1, y_width + 1):
				x = y * step
				if int(x) >= 1:
					final_x = int(x) + x1 - 1
					final_y = int(y) + y1 - 1
					if temp != final_x:
						result.append([final_x, final_y])
						temp = final_x
		else:
			for y in range(y_width, 0, -1):
				x = x_height - y * step

				final_x = int(x) + x1
				final_y = int(y) + y1 - y_width
				temp_no = int(x)

				if temp != final_x:
					temp = final_x
					result.append([final_x, final_y])
		return result

	def get_excel56_for_cell(self, sheet_name="", xyxy=""):
		"""
		셀의 색을 엑셀의 기본 56가지 색의 번호로 돌려주는것

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		"""
		range_object = self.get_range_object_by_xyxy(sheet_name, xyxy)
		result = range_object.Interior.ColorIndex
		return result

	def get_filename_for_active_workbook(self):
		"""
		현재 엑셀화일의 파일이름

		"""
		result = self.get_filename_for_activeworkbook()
		return result

	def get_filename_for_activeworkbook(self):
		"""
		현재 활성화된 엑셀화일의 이름을 갖고읍니다
		"""
		result = self.xlapp.ActiveWorkbook.Name
		return result

	def get_font_color_in_cell(self, sheet_name="", xyxy=""):
		"""
		셀의 폰트 색을 돌려주는것

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		"""
		self.check_sheet_name_n_xyxy(sheet_name, xyxy)
		result = self.range_object.Font.Color
		return result

	def get_font_data_in_range_as_dic(self, sheet_name="", xyxy=""):
		"""
		영역안의 폰트정보를 사전형식으로 갖고온다

		:param sheet_name:
		:param xyxy:
		:return:
		"""
		range_object = self.get_range_object_by_xyxy(sheet_name, xyxy)
		result = {}
		result["name"] = range_object.Font.Name
		result["size"] = range_object.Font.Size
		# result["color"] = range_object.Interior.Color
		result["colorindex"] = range_object.Font.ColorIndex
		result["underline"] = range_object.Font.Underline
		result["bold"] = range_object.Font.Bold

		return result

	def get_font_name_in_range(self, sheet_name="", xyxy=""):
		"""
		글씨체를 설정하는 것

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		:return:
		"""
		range_object = self.get_range_object_by_xyxy(sheet_name, xyxy)
		result = range_object.Font.Name
		return result

	def get_full_name_for_workbook(self):
		"""
		현재 엑셀화일의 화일 이름
		"""
		return self.xlapp.FullName

	def get_height_for_xxline(self, sheet_name, xx):
		"""
		가로의 xx영역의 높이를 설정

		:param sheet_name:
		:param xx:
		:return:
		"""
		sheet_object = self.check_sheet__name(sheet_name)
		range_object = sheet_object.Range(sheet_object.Cells(xx[0], 1), sheet_object.Cells(xx[1], 1))
		result = range_object.RowHeight
		return result

	def get_hour_value(self, time_char=time.localtime(time.time())):
		"""
		시 -----> ['10', '22', 'PM']
		"""
		return [time.strftime('%I', time_char), time.strftime('%H', time_char), time.strftime('%P', time_char)]

	def get_information_for_cell(self, sheet_name, xy=[7, 7]):
		"""
		특정셀의 모든 정보를 갖고오는 것

		:param sheet_name:
		:param xy:
		:return:
		"""
		result = self.read_all_property_in_cell(sheet_name, xy)
		return result

	def get_information_for_shape(self, sheet_name, shape_no):
		"""
		시트안의 도형번호로 그 도형에 대한 기본적인 정보들 갖고오는 것
		2024-01-11 : 조금 변경함
		"""
		result = {}
		sheet_object = self.check_sheet_name(sheet_name)
		if type(shape_no) == type(1):
			shape_no = self.check_shape_name(sheet_name, shape_no)
		shape_object = sheet_object.Shapes(shape_no)
		result["title"] = shape_object.Title
		result["text"] = shape_object.TextFrame2.TextRange.Characters.Text
		result["xy"] = [shape_object.TopLeftCell.Row, shape_object.TopLeftCell.Column]
		result["no"] = shape_no
		result["name"] = shape_object.Name
		result["rotation"] = shape_object.Rotation
		result["left"] = shape_object.Left
		result["top"] = shape_object.Top
		result["width"] = shape_object.Width
		result["height"] = shape_object.Height
		result["pxywh"] = [shape_object.Left, shape_object.Top, shape_object.Width, shape_object.Height]
		return result

	def get_information_for_sheet_object(self, sheet_object):
		"""
		시트객체의 정보를 갖고오는 것

		:param sheet_object:
		:return:
		"""
		result = {}
		result["name"] = sheet_object.Name
		result["usedrange"] = sheet_object.UsedRange
		result["visible"] = sheet_object.Visible
		result["standardwidth"] = sheet_object.StandardWidth
		result["standardheight"] = sheet_object.StandardHeight
		result["index"] = sheet_object.Index
		result["autofiltermode"] = sheet_object.AutoFilterMode
		result["pagesetup"] = sheet_object.PageSetup
		result["names"] = sheet_object.Names
		result["tab_color"] = sheet_object.Tab.Color
		return result

	def get_intersect_address(self, xyxy1, xyxy2):
		"""
		두개의 영역에서 교차하는 구간을 돌려준다
		만약 교차하는게 없으면 ""을 돌려준다

		:param xyxy1:
		:param xyxy2:
		:return:
		"""
		result = self.get_intersect_address_with_range1_and_range2(xyxy1, xyxy2)
		return result

	def get_intersect_address_with_range1_and_range2(self, rng1, rng2):
		"""
		두개의 영역에서 교차하는 구간을 돌려준다
		만약 교차하는게 없으면 ""을 돌려준다

		:param rng1: [1,1,5,5]형식 1번째
		:param rng2: [1,1,5,5]형식 2번째
		"""
		x11, y11, x12, y12 = self.check_address_value(rng1)
		x21, y21, x22, y22 = self.check_address_value(rng2)
		if x11 == 0:
			x11 = 1
			x12 = 1048576
		if x21 == 0:
			x21 = 1
			x22 = 1048576
		if y11 == 0:
			y11 = 1
			y12 = 16384
		if y21 == 0:
			y21 = 1
			y22 = 16384
		new_range_x = [x11, x21, x12, x22]
		new_range_y = [y11, y21, y12, y22]
		new_range_x.sort()
		new_range_y.sort()
		if x11 <= new_range_x[1] and x12 >= new_range_x[2] and y11 <= new_range_y[1] and y12 >= new_range_y[1]:
			result = [new_range_x[1], new_range_y[1], new_range_x[2], new_range_y[2]]
		else:
			result = "교차점없음"
		return result

	def get_intersect_address_with_range_and_input_address(self, xyxy, input_address):
		"""
		이름을 좀더 사용하기 쉽도록 만든것

		:param xyxy: [1,1,2,2]
		:param input_address:
		:return:
		"""
		result = self.check_address_with_datas(xyxy, input_address)
		return result

	def get_intersect_range(self, rng1, rng2):
		"""
		두 영역의 교집합 영역을 돌려주는 것

		:param rng1:
		:param rng2:
		:return:
		"""
		result = self.get_intersect_address_with_range1_and_range2(rng1, rng2)
		return result


	def get_missing_num_in_serial_num_in_range(self, sheet_name, input_xyxy):
		"""
		선택영역에서 연속된 번호중 빠진것을 찾는것
		pcell  #check_missing_num_in_serial_num_at_selection("", "  aa
		print(aa)

		:param sheet_name:
		:param input_xyxy:
		:return:
		"""
		result = []
		set_data = set()
		list_2d = self.read_value2_in_range(sheet_name, input_xyxy)
		max_num = None
		min_num = None
		for list_1d in list_2d:
			for one in list_1d:
				if one:
					one = int(one)
		if max_num == None:
			max_num = one
		if min_num == None:
			min_num = one
		max_num = max(one, max_num)
		min_num = min(one, min_num)
		set_data.add(one)
		for num in range(min_num, max_num + 1):
			if not num in set_data:
				result.append(num)
		return result

	def get_nos_in_input_list_2d_by_same_xline(self, input_2dlist=""):
		"""
		2dlist의 자료의 형태로 된것중에서
		위에서 부터 같은것을 삭제 한다
		0,3,5의 3개가 같은것이라면 제일 앞의 1개는 제외하고 [3,5]를 돌려준다
		"""

		all_datas = input_2dlist
		total_len = len(all_datas)
		same_nos = []
		for no in range(total_len):
			if no in same_nos:
				pass
			else:
				one_list = all_datas[no]
				# print(one_list)
				for num in range(no + 1, total_len):
					if num in same_nos:
						pass
					else:
						if one_list == all_datas[num]:
							same_nos.append(num)
		return same_nos

	def get_pixel_size_for_cell(self, sheet_name="", xyxy=""):
		"""
		영역의 픽셀값을 4개로 얻어오는 것
		:param sheet_name:
		:param xyxy:
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		range_object = self.get_range_object_by_xyxy(sheet_name, xyxy)

		rng_x_coord = range_object.Left
		rng_y_coord = range_object.Top
		rng_width = range_object.Width
		rng_height = range_object.Height
		return [rng_x_coord, rng_y_coord, rng_width, rng_height]

	def get_pxywh_for_cell(self, sheet_name="", xyxy=""):
		"""
		셀의 픽셀값을 갖고온다

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		:return:
		"""
		result = self.get_pxywh_for_range(sheet_name, xyxy)

		return result

	def get_pxywh_for_range(self, sheet_name="", xyxy=""):
		"""
		영역의 위치를 픽셀로 갖고오는 것

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		range_object = self.get_range_object_by_xyxy(sheet_name, xyxy)

		return [range_object.Left, range_object.Top, range_object.Width, range_object.Height]

	def get_pxywh_in_range(self, sheet_name="", xyxy=""):
		"""
		영역의 위치를 픽셀로 갖고오는 것

		:param sheet_name:
		:param xyxy:
		:return:
		"""
		result = self.get_pxywh_for_range(sheet_name, xyxy)
		return result

	def get_random_data_set_on_base_letter(self, digit=2, total_no=1, letters="가나다라마바사아자차카타파하"):
		"""
		입력으로들어오는 것을 랜덤하여 갯수만큼 자료를 만드는것

		:param digit:
		:param total_no:
		:param letters:
		:return:
		"""
		result = []
		for no in range(total_no):
			temp = ""
			for one in range(digit):
				number = random.choice(letters)
				temp = temp + str(number)
			result.append(temp)
		return result

	def get_random_number(self, digit=2, total_no=1):
		"""
		입력으로들어오는 것을 랜덤하여 갯수만큼 자료를 만드는것

		:param digit:
		:param total_no:
		:return:
		"""
		result = []
		for no in range(total_no):
			temp = ""
			for one in range(digit):
				number = random.choice([1, 2, 3, 4, 5, 6, 7, 8, 9, 0])
				temp = temp + str(number)
			result.append(temp)
		return result

	def get_range_object_by_xyxy(self, sheet_name="", xyxy=""):
		"""
		range 객체를 영역으로 만드는 것

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)

		if x1 == 0 or x2 == 0:
			start = self.change_num_to_char(y1)
			end = self.change_num_to_char(y2)
			changed_address = str(start) + ":" + str(end)
			self.range_object = sheet_object.Columns(changed_address)
		elif y1 == 0 or y2 == 0:
			start = self.change_char_to_num(x1)
			end = self.change_char_to_num(x2)
			changed_address = str(start) + ":" + str(end)
			self.range_object = sheet_object.Rows(changed_address)
		else:
			self.range_object = sheet_object.Range(sheet_object.Cells(x1, y1), sheet_object.Cells(x2, y2))
		return self.range_object

	def get_range_object_for_selection(self):
		"""
		예전자료를 위해서 남겨 놓음
		"""
		range_object = self.xlapp.Selection
		return range_object.Address

	def get_range_object_for_xxline(self, sheet_name, xx):
		"""
		xx영역을 객체로 돌려주는것

		:param sheet_name: 시트이름
		:param xx: 가로줄의 시작과 끝 => [3,5]
		:return:
		"""
		new_x = self.check_xx_address(xx)
		sheet_object = self.check_sheet_name(sheet_name)
		result = sheet_object.Rows(str(new_x[0]) + ':' + str(new_x[1]))
		return result

	def get_range_object_for_yyline(self, sheet_name, yy):
		"""
		yy영역을 객체로 돌려주는것

		:param sheet_name: 시트이름
		:param yy: 세로줄의 사작과 끝 => [3,7]
		:return:
		"""
		new_y = self.check_yy_address(yy)
		sheet_object = self.check_sheet_name(sheet_name)
		result = sheet_object.Columns(str(new_y[0]) + ':' + str(new_y[1]))
		return result

	def replace_value_in_range(self, sheet_name, xyxy, old_word, new_word, part_or_whole=False, direction=1, case=False,
								byte_type=False, cell_format=False, replace_cell_format=False):
		"""
		만약  * 또는 ? 기호가 포함된 데이터를 찾거나 수식에 포함하고 싶다면 해당 문자 앞에 ~(물결표)를 붙여주면 됩니다.
		바꾸기를 하는 것
		What	필수 검색할 값  문자열 또는 숫자와 같은 모든 데이터 유형
		Replacement	필수 대체할 값  문자열 또는 숫자와 같은 모든 데이터 유형
		LookAt 선택사항	셀의 일부 일치 또는 셀 전체일치 xlPart 또는 xlWhole
		SearchOrder	선택사항	검색할 순서 – 행 또는 열	xlByRows 또는 xlByColumns
		MatchCase  선택사항	대/소문자 구분 검색 여부 True 또는 False
		MatchByte  선택사항	더블 바이트 언어 지원을 설치한 경우에만 사용됩니다.  True 또는 False
		SearchFormat	선택사항	셀 서식을 활용한 검색 허용	True 또는 False
		ReplaceFormat  선택사항	검색할 셀의 서식  True 또는 False
		"""
		range_object = self.get_range_object_by_xyxy(sheet_name, xyxy)
		range_object.Replace(old_word, new_word, part_or_whole, direction, case, byte_type, cell_format,
							 replace_cell_format)

	def get_rgb_for_cell(self, sheet_name="", xyxy=""):
		"""
		셀의 배경색을 rgb로 돌려주는것
		"""
		range_object = self.get_range_object_by_xyxy(sheet_name, xyxy)
		rgbint = range_object.Interior.Color
		result = self.color.change_rgbint_to_rgb(rgbint)
		return result

	def get_rgbint_for_cell(self, sheet_name="", xyxy=""):
		"""
		셀의 배경색을 rgbint로 돌려주는것

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		:return:
		"""
		range_object = self.get_range_object_by_xyxy(sheet_name, xyxy)
		result = range_object.Interior.Color
		return result

	def get_rgbint_of_font_for_cell(self, sheet_name="", xyxy=""):
		"""
		셀의 폰트 색을 rgbint로 돌려주는것

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		"""
		range_object = self.get_range_object_by_xyxy(sheet_name, xyxy)
		result = range_object.Font.Color
		return result

	def get_same_value_in_range(self, sheet_name="", xyxy=""):
		"""
		선택한 자료중에서 고유한 자료만을 골라내는 것이다
		1. 관련 자료를 읽어온다
		2. 자료중에서 고유한것을 찾아낸다
		3. 선택영역에 다시 쓴다

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)

		temp_datas = self.read_value_in_range("", xyxy)
		temp_result = []
		for xylist_data in temp_datas:
			for one_data in xylist_data:
				if one_data in temp_result or type(one_data) == type(None):
					pass
				else:
					temp_result.append(one_data)
		self.delete_value_in_range("", xyxy)
		for num in range(len(temp_result)):
			mox, namuji = divmod(num, x2 - x1 + 1)
			sheet_object.Cells(x1 + namuji, y1 + mox).Value = temp_result[num]

	def get_shape_name_by_no(self, sheet_name, shape_no):
		"""
		도형의 번호를 확인하는 것
		번호가 들어오던 이름이 들어오던 도형의 번호를 기준으로 확인해서 돌려주는 것
		"""
		check_dic = {}

		if type(123) == type(shape_no):
			result = shape_no
		else:
			sheet_object = self.check_sheet_name(sheet_name)
			for index in sheet_object.Shapes.Count:
				shape_name = sheet_object.Shapes(index).Name
				check_dic[shape_name] = index
			result = check_dic[shape_no]
		return result

	def get_shape_object_by_no(self, sheet_name, shape_no):
		"""
		도형번호를 입력하면 도형의 객체를 돌려주는 것이다

		:param sheet_name:
		:param shape_no:
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)

		if type(shape_no) == type(123):
			shape_name = self.check_shape_name(sheet_name, shape_no)
			shape_object = sheet_object.Shapes(shape_name)
		elif type(shape_no) == type("abc"):
			shape_object = sheet_object.Shapes(shape_no)
		return shape_object

	def get_shape_object_by_no_or_name(self, sheet_name, shape_no):
		"""
		도형의 객체를 갖고오는 것

		:param sheet_name:
		:param shape_no:
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		if type(shape_no) == type(123):
			shape_name = self.check_shape_name(sheet_name, shape_no)
			shape_object = sheet_object.Shapes(shape_name)
		elif type(shape_no) == type("abc"):
			shape_object = sheet_object.Shapes(shape_no)
		return shape_object

	def get_sheet_name_by_position_no(self, input_no):
		"""
		워크시트의 위치번호로 워크시트 이름을 갖고온다
		"""
		result = self.xlbook.Worksheets(input_no).Name
		return result

	def get_sheet_object(self, sheet_name):
		"""
		입력한 시트이름의 시트객체를 돌려주는 것

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		"""
		result = self.check_sheet_name(sheet_name)
		return result

	def get_sheet_object_by_sheet_name(self, sheet_name):
		"""
		시트이름으로 객체를 만들어서 돌려주는 것이다
		이름이 없으면 현재 활성화된 시트를 객체로 만들어 사용한다
		숫자가 들어오면, 번호숫자로 생각해서 앞에서 n번째의 시트이름을 갖고과서 시트객체를 돌려준다

		#1 : 현재 워크북의 순번에 따른 시트객체를 갖고온다
		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		"""

		if sheet_name == "" or sheet_name == None or str(sheet_name).lower() == "activesheet":
			sheet_object = self.xlbook.ActiveSheet
		elif type(self.xlbook.ActiveSheet) == type(sheet_name):  # 시트객체가 오면, 그대로 넘어가는 것
			sheet_object = self.xlbook.ActiveSheet

		elif type(sheet_name) == type(123):  # 1
			sheet_name = self.get_sheet_name_by_position_no(sheet_name)
			sheet_object = self.xlbook.Worksheets(str(sheet_name))
		elif self.use_same_sheet:
			pass
		else:
			try:
				sheet_object = self.xlbook.Worksheets(str(sheet_name))
			except:
				sheet_object = self.xlbook.ActiveSheet
		return sheet_object

	def get_sheet_object_for_activesheet(self):
		"""
		현재 활성화된 시트를 객체형식으로 돌려주는 것

		:return: 시트객체
		"""
		sheet_name = self.xlapp.ActiveSheet.Name
		sheet_object = self.check_sheet_name(sheet_name)
		return sheet_object

	def get_unique_value_in_range(self, sheet_name="", xyxy=""):
		"""
		선택한 자료중에서 고유한 자료만을 골라내는 것이다
		1. 관련 자료를 읽어온다
		2. 자료중에서 고유한것을 찾아낸다
		3. 선택영역에 다시 쓴다

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		range_object = self.get_range_object_by_xyxy(sheet_name, xyxy)

		temp_datas = self.read_value_in_range("", xyxy)
		temp_result = []
		for xylist_data in temp_datas:
			for one_data in xylist_data:
				if one_data in temp_result or type(one_data) == type(None):
					pass
				else:
					temp_result.append(one_data)
		return temp_result


	def get_username_for_workbook(self):
		"""
		사용자 이름을 읽어온다
		"""
		return self.xlapp.UserName

	def get_valued_range_set(self, sheet_name):
		"""
		시트 전체에서 수식을 제외하고, 셀에 값이 있는 영역만 갖고오는것
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		sheet_object.Cells.SpecialCells(2).Select()
		myString = self.xlapp.Selection.Address
		return myString

	def get_vba_module_name_all(self):
		"""
		현재 열려진 엑셀 화일안의 매크로모듈 이름을 찾아서 돌려주는 것
		아래에 1,2,3을 쓴것은 모듈의 종류를 여러가지인데, 해당하는 모듈의 종류이며.
		이것을 하지 않으면 다른 종류의 것들도 돌려주기 때문이다

		"""
		result = []
		for i in self.xlbook.VBProject.VBComponents:
			if i.type in [1, 2, 3]:
				result.append(i.Name)
		return result

	def get_vba_sub_name_all(self):
		"""
		*** 잘 되지 않음

		현재 열려진 엑셀 화일안의 매크로모듈 이름을 찾아서 돌려주는 것
		아래에 1,2,3을 쓴것은 모듈의 종류를 여러가지인데, 해당하는 모듈의 종류이며.
		이것을 하지 않으면 다른 종류의 것들도 돌려주기 때문이다

		"""
		module_name_list = []
		sub_name_list = []

		VBProj = self.xlbook.VBProject

		for i in VBProj.VBComponents:
			if i.type in [1, 2, 3]:
				module_name_list.append(i.Name)

		for i in VBProj.VBComponents:
			num_lines = i.CodeModule.CountOfLines

			for j in range(1, num_lines + 1):

				if 'Sub' in i.CodeModule.Lines(j, 1) and not 'End Sub' in i.CodeModule.Lines(j, 1):
					aaa = i.CodeModule.Lines(j, 1)
					aaa = str(aaa).replace("Sub", "")
					aaa = aaa.split("(")[0]

					sub_name_list.append(aaa.strip())

		return sub_name_list

	def get_xlines_when_same_yline_with_input_data_in_range(self, sheet_name, xyxy, filter_line, input_value,
															first_line_is_title=True):
		"""
		선택한 영역의 특정 y값이 입력값과 같은 x라인들을 돌려 주는것

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		:param filter_line:
		:param input_value:
		:param first_line_is_title:
		"""
		list_2d = self.read_value_in_range(sheet_name, xyxy)
		result = []

		if first_line_is_title:
			result.append(list_2d[0])

		for list_1d in list_2d:
			if input_value in list_1d[int(filter_line)]:
				result.append(list_1d)

		return result

	def get_width_of_yyline(self, sheet_name, yy):
		"""
		넓이를 설정하는 것

		:param sheet_name:
		:param yy:
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		range_object = sheet_object.Range(sheet_object.Cells(1, yy[0]), sheet_object.Cells(1, yy[1]))
		result = range_object.ColumnWidth
		return result

	def get_xy_list_for_circle(self, r, precious=10, xy=[0, 0]):
		"""
		엑셀을 기준으로, 반지름이 글자를 원으로 계속 이동시키는 것

		:param r: 반지금
		:param precious: 얼마나 정밀하게 할것인지, 1도를 몇번으로 나누어서 계산할것인지
		:param xy: [가로번호, 세로번호]
		"""
		result = []
		temp = []
		for do_1 in range(1, 5):
			for do_step in range(90 * precious + 1):
				degree = (do_1 * do_step) / precious
				# r을 더하는 이유는 마이너스는 않되므로 x, y측을 이동시키는것
				x = math.cos(degree) * r
				y = math.sin(degree) * r
				new_xy = [int(round(x)), int(round(y))]

				if not new_xy in temp:
					temp.append(new_xy)
		area_1 = []
		area_2 = []
		area_3 = []
		area_4 = []

		for x, y in temp:
			new_x = x + r + 1 + xy[0]
			new_y = y + r + 1 + xy[1]

			if x >= 0 and y >= 0:
				area_1.append([new_x, new_y])
			elif x >= 0 and y < 0:
				area_2.append([new_x, new_y])
			elif x < 0 and y < 0:
				area_3.append([new_x, new_y])
			elif x < 0 and y >= 0:
				area_4.append([new_x, new_y])
		area_1.sort()
		area_1.reverse()
		area_2.sort()
		area_3.sort()
		area_4.sort()
		area_4.reverse()

		result.extend(area_2)
		result.extend(area_1)
		result.extend(area_4)
		result.extend(area_3)
		return result

	def get_xyxy_for_range_object(self, input_range_obj):
		"""
		영역객체의 주소를 xyxy형식으로 갖고오는 것

		:param input_range_obj:
		:return:
		"""
		result = self.change_address_to_xyxy(input_range_obj.Address)
		return result

	def group_input_list_2d_by_index_no(self, input_list_2d, index_no=4):
		"""
		2차원의 자료를 번호를 기준으로 그룹화하는것


		:param input_list_2d:
		:param index_no:
		:return:
		"""
		result = []
		# 2차원자료를 원하는 열을 기준으로 정렬
		sorted_input_list_2d = self.sort_list_2d_by_index(input_list_2d, index_no)

		check_value = sorted_input_list_2d[0][index_no]
		temp = []
		for one_list in sorted_input_list_2d:
			if one_list[index_no] == check_value:
				temp.append(one_list)
			else:
				result.append(temp)
				temp = [one_list]
				check_value = one_list[index_no]
		if temp:
			result.append(temp)
		return result

	def insert_all_picture_of_folder_in_sheet(self, sheet_name, folder_name, ext_list, xywh, link=0J, image_in_file=1):
		"""
		특정폴다안이 모든 사진을 전부 불러오는 것이다

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param folder_name:
		:param ext_list:
		:param xywh:
		:param link:
		:param image_in_file:
		"""

		aaa = self.util.get_all_file_name_in_folder_filter_by_extension_name(folder_name, ext_list)
		sheet_object = self.check_sheet_name(sheet_name)

		rng = sheet_object.Cells(xywh[0], xywh[1])

		for index, file_name in enumerate(aaa):
			full_path = folder_name + "/" + file_name
			full_path = str(full_path).replace("/", "\\")

			sheet_object.Shapes.AddPicture(full_path, link, image_in_file, rng.Left + index * 5,
											rng.Top + index * 5,
											xywh[2], xywh[3])

		return aaa

	def insert_data_in_list_2d(self, sheet_name, xyxy, xy, input_value):
		"""
		엑셀의 2차원자료에서 중간에 값을 넣으면, 자동으로 뒤로 밀어서적용되게 하기

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		:param xy:
		:param input_value:
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		range_object = self.get_range_object_by_xyxy(sheet_name, xyxy)

		len_x = x2 - x1 + 1
		if type(xy) == type([]):
			insert_position = len_x * xy[0] + xy[1] - 1
		else:
			insert_position = xy - 1
		reverse_list_2d = self.read_value_in_range(sheet_name, xyxy)
		list_1d = self.util.change_list_2d_to_list_1d(reverse_list_2d)
		list_1d.insert(insert_position, input_value)
		result = self.util.change_list_1d_to_list_2d_group_by_step(list_1d, len_x)
		return result

	def insert_image(self, sheet_name, file_path, xywh, link=0, image_in_file=1):
		"""
		image화일을 넣는것
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		rng = sheet_object.Cells(xywh[0], xywh[1])
		# sh.Shapes.AddPicture("화일이름", "링크가있나", "문서에저장", "x좌표", "y좌표", "넓이","높이")
		sheet_object.Shapes.AddPicture(file_path, link, image_in_file, rng.Left, rng.Top, xywh[2], xywh[3])

	def insert_image_at_range_name(self, sheet_name, folder_path, ext_list=["jgp", "png"]):
		"""
		입력으로 들어오는 사진을 이름역역안에 맞춰서 넣는 것이다

		1. 입력된 폴더에서 사진의 화일이름을 갖고온다
		2. 사진자료를 이름기준으로 정렬 시킨다
		3. 엑셀의 시트에서 이름영역을 갖고온다
		4. 이름영역의 주소를 기준으로 정렬을 시킨다
		5. 이름영영역의 갯수를 기준으로 사진자료를 넣는다
		"""
		ext_list = self.change_xylist_to_list(ext_list)

		self.select_sheet(sheet_name)
		all_files = self.util.get_all_file_name_in_folder_filter_by_extension_name(folder_path, ext_list)  # 1
		all_files.sort()  # 2

		all_rng_name = self.read_all_range_name()  # 3
		list_2d = []
		for one in all_rng_name:
			bbb = self.check_address_value(one[2])
			bbb.append(one[1])
			list_2d.append(bbb)

		list_2d.sort()  # 4

		min_count = min(len(list_2d), len(all_files))
		for index in range(min_count):
			one_file = all_files[index]
			# insert_all_picture_of_folder_in_sheet(self, sheet_name, folder_name, ext_list, xywh, link=0J, image_in_file=1):
			self.insert_all_picture_of_folder_in_sheet("", "D:\\", ["jpg"])  # 5

	def insert_image_in_xyxy(self, sheet_name, xyxy, file_path):
		"""
		선택한 영역에 image화일을 넣는것
		선택한 영역안에 자동으로 올수있도록 만들어 보자
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		xywh = self.change_xyxy_to_pxyxy(xyxy)
		sheet_object.Shapes.AddPicture(file_path, 0, 1, xywh[0], xywh[1], xywh[2], xywh[3])

	def insert_list_2d_blank_by_index(self, input_list_2d, no_list):
		"""
		입력형태 : 2차원리스트, [2,5,7]
		"""
		no_list.sort()
		no_list.reverse()
		for one in no_list:
			for x in range(len(input_list_2d)):
				input_list_2d[x].insert(int(one), "")
		return input_list_2d

	def insert_picture_at_xyxy(self, sheet_name, xyxy, file_name, space=1):
		"""
		특정 사진을 셀안에 맞토록 사이즈 조절하는 것
		sh.Shapes.AddPicture("화일이름", "링크가있나”, "문서에저장", "x좌표", "y좌표", "넓이", "높이")
		"""

		xy_1 = self.read_coord_in_cell(sheet_name, [xyxy[0], xyxy[1]])
		xy_2 = self.read_coord_in_cell(sheet_name, [xyxy[2], xyxy[3]])

		x_start = xy_1[0] + space
		y_start = xy_1[1] + space

		width = xy_2[0] + xy_2[2] - xy_1[0] - space * 2
		height = xy_2[1] + xy_2[3] - xy_1[1] - space * 2

		sheet_object = self.check_sheet_name(sheet_name)
		# sh.Shapes.AddPicture("화일이름", "링크가있나", "문서에저장", "x좌표", "y좌표", "넓이","높이")
		sheet_object.Shapes.AddPicture(file_name, 0, 1, x_start, y_start, width, height)

	def insert_picture_by_pixel(self, sheet_name, file_path, pxpywh, link=0, image_in_file=1):
		"""
		그림을 픽셀크기로 시트에 넣는 것

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param file_path: 화일의 경로,  file_path
		:param pxpywh:
		:param link:
		:param image_in_file:
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		sheet_object.Shapes.AddPicture(file_path, link, image_in_file, pxpywh[0], pxpywh[1], pxpywh[2], pxpywh[3])

	def insert_picture_in_cell(self, sheet_name, xy, full_path):
		"""
		셀 하나에 그림을 맞춰서 넣는것

		:param sheet_name:
		:param xy:
		:param full_path:
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		sheet_object.Cells(xy[0], xy[1]).Select()
		aaa = sheet_object.Pictures
		aaa.Insert(full_path).Select()

	def insert_picture_in_sheet(self):
		"""
		시트에 그림을 넣는것

		:return:
		"""
		sh = self.xlbook.Worksheets("Sheet1")
		sh.Shapes.AddPicture("c:\icon_sujun.gif", 0, 1, 541.5, 92.25, 192.75, 180)

	def insert_shape(self, sheet_name, xy="", size=[25, 25], shape_style="circle", input_scolor="", input_value=""):
		"""
		원을 만들고, 안에 숫자를 연속적으로 만드는 것
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		pxyxy = self.change_xyxy_to_pxyxy(xy)
		check_shape_style = {"circle": 9, "원": 9}

		Shp1 = sheet_object.Shapes.AddShape(check_shape_style[shape_style], pxyxy[0], pxyxy[1], size[0], size[1])

		Shp1.Fill.ForeColor.RGB = self.color.change_scolor_to_rgbint(input_scolor)
		if input_value:
			Shp1.TextFrame2.VerticalAnchor = self.vars["shape_font"]["align_v"]
			Shp1.TextFrame2.HorizontalAnchor = self.vars["shape_font"]["align_h"]
			Shp1.TextFrame2.TextRange.Font.Bold = self.vars["shape_font"]["bold"]

			Shp1.TextFrame2.TextRange.Characters.Font.Fill.ForeColor.RGB = self.vars["shape_font"]["color"]
			Shp1.TextFrame2.TextRange.Characters.Text = input_value
			Shp1.TextFrame2.TextRange.Characters.Font.Size = self.vars["shape_font"]["size"]

	def insert_shape_as_circle_with_number(self, sheet_name, xy="", pwh=25, scolor="red", input_value=1, font_size=""):
		"""
		원을 만들고, 안에 숫자를 연속적으로 만드는 것
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		if font_size: self.vars["font"]["size"] = font_size

		pxyxy = self.change_xyxy_to_pxyxy(xy)
		Shp1 = sheet_object.Shapes.AddShape(9, pxyxy[0], pxyxy[1], pwh, pwh)
		Shp1.Fill.ForeColor.RGB = self.color.change_scolor_to_rgbint(scolor)
		Shp1.TextFrame2.VerticalAnchor = 3
		Shp1.TextFrame2.HorizontalAnchor = 2
		Shp1.TextFrame2.TextRange.Font.Bold = self.vars["font"]["bold"]
		Shp1.TextFrame2.TextRange.Characters.Text = input_value
		Shp1.TextFrame2.TextRange.Characters.Font.Size = self.vars["font"]["size"]

	def insert_shape_at_xywh(self, sheet_name, shape_no=35, xywh=""):
		"""
		그림을 픽셀크기로 시트에 넣는 것

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param shape_no: shape_no, 엑셀에서 정의한 도형의 번호
		:param xywh: [x, y, width, height], 왼쪽윗부분의 위치에서 너비와 높이
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		sheet_object.Shapes.Addshape(shape_no, xywh[0], xywh[1], xywh[2], xywh[3])

	def insert_sheet(self, sheet_name):
		"""
		시트이름과 함께 시트하나 추가하기
		함수의 공통적인 이름을 위해서 만든것
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:return:
		"""
		all_sheet_name = self.read_all_sheet_name()
		if sheet_name in all_sheet_name:
			self.util.messagebox_for_show("같은 이름의 시트가 있읍니다")
		else:
			self.xlbook.Worksheets.Add()
			if sheet_name:
				old_name = self.xlapp.ActiveSheet.Name
				self.xlbook.Worksheets(old_name).Name = sheet_name

	def insert_sheet_with_name(self, sheet_name):
		"""
		시트이름과 함께 시트하나 추가하기
		함수의 공통적인 이름을 위해서 만든것
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:return:
		"""
		all_sheet_name = self.read_all_sheet_name()
		if sheet_name in all_sheet_name:
			self.util.messagebox_for_show("같은 이름의 시트가 있읍니다")
		else:
			self.xlbook.Worksheets.Add()
			if sheet_name:
				old_name = self.xlapp.ActiveSheet.Name
				self.xlbook.Worksheets(old_name).Name = sheet_name

	def insert_value_after_splitted(self, xyxy, splitted_char=","):
		"""
		1줄의 값을 특정문자를 기준으로 분리한후
		분리된 갯수가 있으면, 1개이상일때는, 아래부분에 새로운 열을 추가한후에 값을 넣는것
		여러줄을 선택하여도, 제일 첫줄만 적용한다
		"""
		for no in range(xyxy[2], xyxy[0], -1):
			value = self.read_value_in_cell("", [no, xyxy[1]])
			splited_value = value.split(splitted_char)
			self.write_value_in_cell("", [no, xyxy[1]], splited_value[0].strip())
			if len(splited_value) > 1:
				for index, one in enumerate(splited_value[1:]):
					self.insert_xline("", no + index + 1)
					self.write_value_in_cell("", [no + index + 1, xyxy[1]], one.strip())

	def insert_xline(self, sheet_name, x):
		"""
		가로열을 한줄삽입하기

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param x:
		"""
		self.sheet_object = self.check_sheet_name(sheet_name)
		num_r1 = self.change_char_to_num(x)
		self.sheet_object.Rows(str(num_r1) + ':' + str(num_r1)).Insert(-4121)

	def insert_xline_in_range_by_step(self, sheet_name, xyxy, step_no):
		"""
		insert_range_xline_bystep(sheet_name="", xyxy="", step_no)
		n번째마다 열을 추가하는것
		새로운 가로열을 선택한 영역에 1개씩 추가하는것
		n번째마다는 n+1번째가 추가되는 것
		입력형태 :
		출력형태 :
		"""
		self.menu_dic['insert_range_xline_bystep'] = {'표시여부': '필요', '그리드메뉴': ['insert', 'range', 'N 번째마다 x열 삽입'],
													  '실행메뉴': ['insert', 'range', 'xline_bystep']}
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		range_object = self.get_range_object_by_xyxy(sheet_name, xyxy)

		step_no = int(step_no)
		add_x = 0
		for no in range(1, x2 - x1 + 1):
			x = add_x + no
			if divmod(x, step_no)[1] == step_no - 1:
				self.insert_xxline_in_range(sheet_name, x + x1)
				add_x = add_x + 1

	def insert_xline_in_sheet(self, sheet_name, x):
		"""
		가로열을 한줄삽입하기

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param x:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		num_r1 = self.change_char_to_num(x)
		sheet_object.Rows(str(num_r1) + ':' + str(num_r1)).Insert(-4121)

	def insert_xline_with_sum_value_for_each_yline(self, input_list_2d, xy):
		"""
		선택한 영역의 세로자료들을 다 더해서 제일위의 셀에 다시 넣는것

		:param input_list_2d: 2차원의 리스트형 자료
		:param xy: [가로번호, 세로번호]
		"""

		input_list_2d = self.change_xylist_to_list(input_list_2d)

		x_len = len(input_list_2d)
		y_len = len(input_list_2d[0])
		for y in range(y_len):
			temp = ""
			for x in range(x_len):
				self.write_value_in_cell("", [x + xy[0], y + xy[1]], "")
				if input_list_2d[x][y]:
					temp = temp + " " + input_list_2d[x][y]
			self.write_value_in_cell("", [xy[0], y + xy[1]], str(temp).strip())

	def insert_xxline_in_range(self, sheet_name, xx):
		"""
		insert_xxline_in_range(sheet_name="", xx):
		가로열을 한줄삽입하기
		입력형태 :
		출력형태 :
		"""
		self.menu_dic['insert_xxline_in_range'] = {'표시여부': '필요', '그리드메뉴': ['insert', 'range', '입력받은 x열 삽입'],
													'실행메뉴': ['insert', 'range', 'xxline']}
		sheet_object = self.check_sheet_name(sheet_name)
		xx = self.check_xx_address(xx)
		sheet_object.Rows(str(xx[0]) + ':' + str(xx[1])).Insert()

	def insert_yline(self, sheet_name, y):
		"""
		세로행을 한줄삽입하기

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param y:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		num_r1 = self.change_num_to_char(y)
		sheet_object.Columns(str(num_r1) + ':' + str(num_r1)).Insert(-4121)

	def insert_yline_in_range_by_step(self, sheet_name, xyxy, step_no):
		"""
		insert_range_yline_bystep(sheet_name="", xyxy="", step_no)
		n번째마다 열을 추가하는것
		새로운 가로열을 선택한 영역에 1개씩 추가하는것
		입력형태 :
		출력형태 :
		"""
		self.menu_dic['insert_range_yline_bystep'] = {'표시여부': '필요', '그리드메뉴': ['insert', 'range', '몇번째마다 y-열을 삽입'],
													  '실행메뉴': ['insert', 'range', 'yline_bystep']}
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		range_object = self.get_range_object_by_xyxy(sheet_name, xyxy)

		# 일정부분으로 추가되는것을 앞에서부터 적용
		step_no = int(step_no)
		add_y = 0
		for no in range(0, y2 - y1 + 1):
			y = add_y + no
			if divmod(y, step_no)[1] == step_no - 1:
				self.insert_range_yyline(sheet_name, y + y1)
				add_y = add_y + 1

	def insert_ylines_in_list_2d_by_line_nos(self, input_list_2d, no_list):
		"""
		2차원 리스트의 자료에 원하는 가로줄을 삽입하는 것
		입력형태 : 2차원리스트, [2,5,7]
		"""

		input_list_2d = self.change_xylist_to_list(input_list_2d)
		no_list = self.change_xylist_to_list(no_list)

		no_list.sort()
		no_list.reverse()
		for one in no_list:
			for x in range(len(input_list_2d)):
				input_list_2d[x].insert(int(one), "")
		return input_list_2d

	def insert_yyline(self, sheet_name, yy):
		"""
		시트에 세로행을 여러줄 삽입한다

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param yy: 세로줄의 사작과 끝 => [3,7]
		"""
		self.sheet_object = self.check_sheet_name(sheet_name)
		if type(yy) == type([]) and len(yy) == 1:
			x2 = x1 = self.change_num_to_char(yy[0])
		elif type(yy) == type([]) and len(yy) == 2:
			x1 = self.change_num_to_char(yy[0])
			x2 = self.change_num_to_char(yy[1])
		else:
			x2 = x1 = self.change_num_to_char(yy)
		self.sheet_object.Columns(str(x1) + ':' + str(x2)).Insert()

	def insert_yyline_in_range(self, sheet_name, yy_list):
		"""
		시트에 세로행을 연속된 여러줄 삽입하기

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param yy_list: 세로줄의 사작과 끝 => [3,7]
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		if type(yy_list) == type([]) and len(yy_list) == 1:
			x2 = x1 = self.change_num_to_char(yy_list[0])
		elif type(yy_list) == type([]) and len(yy_list) == 2:
			x1 = self.change_num_to_char(yy_list[0])
			x2 = self.change_num_to_char(yy_list[1])
		else:
			x2 = x1 = self.change_num_to_char(yy_list)
		sheet_object.Columns(str(x1) + ':' + str(x2)).Insert()

	def intersect_address_and_input_data(self, xyxy, input_values):
		"""
		이름을 좀더 사용하기 쉽도록 만든것
		"""
		result = self.check_address_with_datas(xyxy, input_values)
		return result

	def intersect_range1_range2(self, rng1, rng2):
		"""
		두개의 영역에서 교차하는 구간을 돌려준다
		만약 교차하는게 없으면 ""을 돌려준다
		"""
		range_1 = self.check_address_value(rng1)
		range_2 = self.check_address_value(rng2)
		x11, y11, x12, y12 = range_1
		x21, y21, x22, y22 = range_2
		if x11 == 0:
			x11 = 1
			x12 = 1048576
		if x21 == 0:
			x21 = 1
			x22 = 1048576
		if y11 == 0:
			y11 = 1
			y12 = 16384
		if y21 == 0:
			y21 = 1
			y22 = 16384
		new_range_x = [x11, x21, x12, x22]
		new_range_y = [y11, y21, y12, y22]
		new_range_x.sort()
		new_range_y.sort()
		if x11 <= new_range_x[1] and x12 >= new_range_x[2] and y11 <= new_range_y[1] and y12 >= new_range_y[1]:
			result = [new_range_x[1], new_range_y[1], new_range_x[2], new_range_y[2]]
		else:
			result = "교차점없음"
		return result

	def is_all_empty_value_for_range(self, sheet_name="", xyxy=""):
		"""
		결과를 True / Flase로 나타내는 것

		값이 모두 비었을때는 True를 돌려주고 아닌경우는 False를 돌려준다
		여기는 기본으로 ""일때는 usedrange의 주소를 갖고온다
		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		"""
		if xyxy == "":
			xyxy = self.read_address_for_usedrange(sheet_name)
		# print(xyxy)
		list_2d = self.read_range(sheet_name, xyxy)
		if list_2d == None:
			return True
		else:
			for list_1d in list_2d:
				for value in list_1d:
					if value == "" or value == None:
						return False
			return True


	def is_empty_sheet(self, sheet_name):
		"""
		시트가 비었는지를 확인하는 것
		결과를 True / Flase로 나타내는 것

		:param sheet_name:
		:return:
		"""
		xyxy = self.read_address_for_usedrange(sheet_name)
		value = self.read_value_in_range(sheet_name, xyxy)
		result = False
		if xyxy == [1, 1, 1, 1] and value == None:
			result = True

		return result

	def is_empty_xline(self, sheet_name, x_no):
		"""
		결과를 True / Flase로 나타내는 것

		열전체가 빈 것인지 확인해서 돌려준다
		현재의 기능은 한줄만 가능하도록 하였다
		다음엔 영역이 가능하도록 하여야 겠다

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param no:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		result = self.xlapp.WorksheetFunction.CountA(sheet_object.Rows(x_no).EntireRow)
		return result

	def is_empty_yline(self, y_no):
		"""
		입력한 세로 한줄이 전체가 비어있는지 확인하는 것
		결과를 True / Flase로 나타내는 것

		:param y_no:
		:return:
		"""
		y1 = self.change_char_to_num(y_no)
		result = self.xlbook.WorksheetFunction.CountA(self.vars["sheet"].Columns(y1).EntireColumn)
		return result

	def is_file_in_folder(self, path, file_name):
		"""
		결과를 True / Flase로 나타내는 것

		:param path: path
		:param file_name: file_name
		:return:
		"""
		result = ""
		if path == "":
			path = "C:/Users/Administrator/Documents"
		file_name_all = self.util.get_all_file_name_in_folder(path)

		if file_name in file_name_all:
			result = True
		return result

	def is_range_name(self, input_range_name):
		"""
		이름영역의 하나인지 아닌지 확인하는 것

		:param input_range_name:
		:return:
		"""

		result = False
		all_range_name = self.get_all_range_name()
		if input_range_name in all_range_name:
			result = True
		return result

	def is_sheet_name(self, input_sheet_name):
		"""
		입력받은 시트의 이름이 현재 워크북의 이름중하나인지 확인해 보는것

		:param input_sheet_name:
		:return:
		"""
		result = False
		all_sheet_name = self.get_all_sheet_name()
		if input_sheet_name in all_sheet_name:
			result = True
		return result

	def jf_sql_is_in_input_text(self, jf_sql, input_value):
		"""
		입력으로 들어온 텍스트에서 정규표현식과 맞는 것을 갖고오는 것
		"""
		result = self.check_ok_or_no(jf_sql, input_value)
		return result

	def list_same_repeat_no(self, input_value, line_no):
		"""
		넘어온 자료중 line_no번째의 연속된 자료가 같은 갯수를 세어서 리스트형태로 돌려주는것
		"""
		result = []
		num = 1
		for no in range(len(input_value) - 1):
			if input_value[no][line_no] == input_value[no + 1][line_no]:
				# 위와 아래의 Item이 같은것일때
				num = num + 1
			else:
				result.append(num)
				num = 1
		return result

	def lock_off(self, sheet_name, password="1234"):
		"""
		시트를 암호 해제

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param password: 암호
		"""
		sheet_object = self.check_sheet_name(sheet_name)

		sheet_object.Unprotect(password)

	def lock_off_for_sheet(self, sheet_name, password="1234"):
		"""
		시트를 암호 해제

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param password: 암호
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		sheet_object.Unprotect(password)

	def lock_on_for_sheet(self, sheet_name, password="1234"):
		"""
		시트를 암호로 저장

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param password: 암호
		"""
		self.set_password_for_sheet(sheet_name, password)

	def lock_sheet_with_password(self, sheet_name):
		"""
		암호걸기

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		"""
		source_letter = "1234567890"
		repeat_no = 4
		count = 0
		for a in itertools.product(source_letter, repeat=repeat_no):
			count += 1
			temp_pwd = ("".os.path.join(map(str, a)))
			try:
				self.set_sheet_lock_off(sheet_name, temp_pwd)
			except:
				pass
			else:
				break

	def make_4_edge_xy_list_for_range(self, xyxy):
		"""
		좌표를 주면, 맨끝만 나터내는 좌표를 얻는다

		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		"""
		temp_1 = []
		for x in [xyxy[0], xyxy[2]]:
			temp = []
			for y in range(xyxy[1], xyxy[3] + 1):
				temp.append([x, y])
			temp_1.append(temp)

		temp_2 = []
		for y in [xyxy[1], xyxy[3]]:
			temp = []
			for x in range(xyxy[0], xyxy[2] + 1):
				temp.append([x, y])
			temp_2.append(temp)

		result = [temp_1[0], temp_2[1], temp_1[1], temp_2[0]]
		return result

	def make_basic_range(self, sheet_name="", xyxy=""):
		"""

		:param sheet_name:
		:param xyxy:
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		range_object = self.get_range_object_by_xyxy(sheet_name, xyxy)

		return range_object.Address

	def make_box_for_shape(self, sheet_name, xyxy, line_color="bla", line_thickness="thin"):
		"""
		영역의 테두리와 맞는 사각형 텍스트박스를 만드는데, 투명도가 100%로 설정한 것이다
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		pxywh = self.change_xyxy_to_pxywh(sheet_name, xyxy)

		Shpl = sheet_object.Shapes.AddShape(1, pxywh[0], pxywh[1], pxywh[2], pxywh[3])
		Shpl.Fill.Transparency = 1
		Shpl.Line.ForeColor.RGB = self.color.change_scolor_to_rgbint(line_color)

		try:
			thickness = self.vars["line"]["check_line_style"][line_thickness]
		except:
			thickness = line_thickness
		Shpl.Line.Weight = thickness

	def make_dic_for_range_by_ylist(self, sheet_name, xyxy, input_sero_set):
		"""
		가로열오 넣을수있도록 영역의 자료를

		:param sheet_name:
		:param xyxy:
		:param input_sero_set:
		:return:
		"""
		[x1, y1, x2, y2] = self.check_address_value(xyxy)
		l2d = self.read_value_in_range(sheet_name, [x1, y1, x2, y2])
		result_xy = {}
		result = {}
		for index, l1d in enumerate(l2d):
			temp = ""
			for sero in input_sero_set:
				temp = temp + str(l1d[sero - 1]) + "_"
				temp = temp[:-1]
				if not temp in result.keys():
					result[temp] = [list(l1d)]
					result_xy[temp] = [[x1 + index, y1, x1 + index, y2]]
				else:
					result[temp].append([x1 + index, y1, x1 + index, y2])
		return [result, result_xy]

	def make_dic_with_count_for_text(self, input_text):
		"""
		입력으로 들어온 텍스트를 공백으로 분리해서, 단어의 형태로 만들어서
		각 단어들의 갯수를 사전형식으로 만드는 것

		:param input_text:
		:return:
		"""
		input_text = input_text.replace(" ", "")
		input_text = input_text.upper()
		result = {}
		for one_letter in input_text:
			if one_letter in list(result.keys()):
				result[one_letter] = result[one_letter] + 1
			else:
				result[one_letter] = 1
		return result

	def make_dic_with_id(self, xyxy=[2, 2, 21818, 7]):
		"""
		주소록의 각 자료를 찾는 방법으로, 고유한 이름을 기준으로 ID를 리스트로 저장하는 것이다
		제일앞의 것이 id이다
		"""
		list_2d = self.read_value_in_range("", xyxy)
		result = {}
		for list_1d in list_2d:
			for no in range(len(list_1d), 0, -1):
				if list_1d[no - 1]:
					if list_1d[no - 1] in result.keys():
						result[list_1d[no - 1]].append(list_1d[0])
					else:
						result[list_1d[no - 1]] = [list_1d[0]]
					break
		return result

	def make_dict_by_first_value_in_range(self, sheet_name="", xyxy=""):
		"""
		맨앞의 글자를 키로 사용해서, 2차원자료를 사전형식으로 만드는 것
		퀴즈같은 문제를 만들때, 속도도 빠르게 하면서, 사용했던것을 다시 안물러 오도록 하는것

		:param sheet_name:
		:param xyxy:
		:return:
		"""
		result = {}
		l2d = self.change_tuple_2d_to_list_2d(sheet_name, xyxy)
		l2d_changed = self.util.delete_empty_line_in_list_2d(l2d)
		for l1d in l2d_changed:
			result[l1d[0]] = list(l1d)
		return result

	def make_file_as_same_group(self, sheet_name, xyxy, line_index, first_is_title_or_not, folder_name):
		"""
		선택한 영역의 몇번째 줄이 같은것들만 묶어서 엑셀화일 만들기
		1) 저장활 플더를 확인
		2) 첫즐에 제목이 있는지 아닌지에 따라서 자료영역을 바꾸는 것
		3) 읽어온 자료
		4) 자료증에서 어떤 줄을 기준으로 그룹화 하는것
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		range_object = self.get_range_object_by_xyxy(sheet_name, xyxy)

		self.util.make_folder(folder_name)  # 1
		sheet_object_0 = self.check_sheet_name(sheet_name)
		# 2
		if first_is_title_or_not:
			new_range = [1 + 1, y1, x2, y2]
		list_2d = self.read_value_in_range(sheet_name, new_range)  # 3
		grouped_data = self.util.group_list_2d_by_index_no(list_2d, line_index)  # 4
		startx = 1
		count = 1
		for one_group in grouped_data:
			range_2 = self.concate_range_n_line_no(new_range, [start_x, start_x + len(one_group) - 1])
			if first_is_title_or_not:
				self.select_multi_range(sheet_object_0, [[x1, y1, x1, y2], range_2])
			else:
				self.select_multi_range(sheet_object_0, [range_2])
			self.xlapp.selection.Copy()
			self.new_workbook("")
			sheet_object = self.check_sheet_name("")
			sheet_object.Cells(1, 1).Select()
			sheet_object.Paste()
			self.save(folder_name + "\\" + str(one_group[0][line_index]) + "_" + str(count) + ".xlsx")
			self.close_activeworkbook()
			start_x = start_x + len(one_group)
			count = count + 1

	def make_input_dic(self, input_text):
		"""
		단어중 가장 가까운 단어들 찾기
		입력형식은 bold(),진하게(yes).. 이런식으로 입력이 되도록 하면 어떨까??
		"""
		result = self.vars["check_font_para"][input_text]
		return result

	def make_line_for_splitted_data(self, xyxy, union_char="#"):
		"""
		앞에 숫자를 기준으로 옆줄의 자료를 합치는것
		맨앞의 자료 1줄만 합친다
		"""
		temp = ""
		old_x = xyxy[0]
		for x in range(xyxy[0], xyxy[2] + 1):
			gijun_data = self.read_value_in_cell("", [x, xyxy[1]])
			value = self.read_value_in_cell("", [x, xyxy[1] + 1])

			if gijun_data:
				self.write_value_in_cell("", [old_x, xyxy[1] + 2], temp[:-len(union_char)])
				temp = value + union_char
				old_x = x
			else:
				temp = temp + value + union_char
		self.write_value_in_cell("", [old_x, xyxy[1] + 2], temp[:-len(union_char)])

	def make_list_unique(self, input_value):
		"""
		1차원의 리스트가 중복값을 제외하고 돌려주는것, 집합형으로 돌려준다
		"""
		temp_dic = set()
		for one in input_value:
			temp_dic.add(one)
		return temp_dic

	def make_password(self, isnum="yes", istext_small="yes", istext_big="yes", isspecial="no", len_num=10):
		"""
		엑셀시트의 암호를 풀기위해 암호를 계속 만들어서 확인하는 것
		"""
		check_char = []
		if isnum == "yes":
			check_char.extend(list(string.digits))
		if istext_small == "yes":
			check_char.extend(list(string.ascii_lowercase))
		if istext_big == "yes":
			check_char.extend(list(string.ascii_uppercase))
		if isspecial == "yes":
			for one in "!@#$%^*_-":
				check_char.extend(one)

		zz = itertools.combinations_with_replacement(check_char, len_num)
		for aa in zz:
			try:
				pswd = "".join(aa)
				self.unlock_sheet("", pswd)
				break
			except:
				pass

	def make_password_1(self, isnum="yes", istext_small="yes", istext_big="yes", isspecial="no", len_num=10):
		"""
			엑셀시트의 암호를 풀기위해 암호를 계속 만들어서 확인하는 것
			메뉴에서 제외

			:param isnum:
			:param istext_small:
			:param istext_big:
			:param isspecial:
			:param len_num:
			:return:
			"""
		check_char = []
		if isnum == "yes":
			check_char.extend(list(string.digits))
		if istext_small == "yes":
			check_char.extend(list(string.ascii_lowercase))
		if istext_big == "yes":
			check_char.extend(list(string.ascii_uppercase))
		if isspecial == "yes":
			for one in "!@#$%^*_-":
				check_char.extend(one)

		zz = combinations_with_replacement(check_char, len_num)
		for aa in zz:
			try:
				pswd = "".join(aa)
				# pcell에 있는것
				self.set_sheet_lock_off("", pswd)
				break
			# print("발견", pswd)
			except:
				pass

	def make_ppt_table_from_xl_data(self, ):
		"""
		엑셀의 테이블 자료가 잘 복사가 않되는것 같아서, 아예 하나를 만들어 보았다
		엑셀의 선택한 영역의 테이블 자료를 자동으로 파워포인트의 테이블 형식으로 만드는 것이다
		"""

		activesheet_name = self.read_activesheet_name()
		[x1, y1, x2, y2] = self.read_address_for_selection()

		Application = win32com.client.Dispatch("Powerpoint.Application")
		Application.Visible = True
		active_ppt = Application.Activepresentation
		slide_no = active_ppt.Slides.Count + 1

		new_slide = active_ppt.Slides.Add(slide_no, 12)
		new_table = active_ppt.Slides(slide_no).Shapes.AddTable(x2 - x1 + 1, y2 - y1 + 1)
		shape_no = active_ppt.Slides(slide_no).Shapes.Count

		for y in range(y1, y2 + 1):
			for x in range(x1, x2 + 1):
				value = self.read_value_in_cell(activesheet_name, [x, y])
				active_ppt.Slides(slide_no).Shapes(shape_no).Table.Cell(x - x1 + 1,
																		y - y1 + 1).Shape.TextFrame.TextRange.Text = value

	def make_print_page(self, sheet_name, input_list_2d, line_list, start_xy, size_xy, y_line, position):
		"""
		input_ list_2d, 2차원의 기본자료들
		line list = [1,2,3], 각 라인에서 출력이 될 자료
		start_ xy = [1,1], 첫번째로 시작될 자료의 위치
		size_xy = [7,9], 하나가 출력되는 영역의 크기
		y_line = 2, 한페이지에 몇줄을 출력할것인지
		position = [1,31,[4,5],[7,9]], 한줄의 출력되는 위치, line_ list의 갯수와 같아야 한다
		1) 2차원의 자료에서 출력하는 자료들만 순서대로 골라서 새로 만드는 것
		"""

		changed_list_2d = self.pick_ylines_at_list_2d(input_list_2d, line_list)  # 1
		new_start_x = start_xy[0]
		new_start_y = start_xy[1]
		for index, list_1d in enumerate(changed_list_2d):
			mok, namuji = divmod(index, y_line)
			new_start_x = new_start_x + mok * size_xy[0]
			new_start_y = new_start_y + namuji * size_xy[1]
			for index_2, one_value in enumerate(list_1d):
				self.write_value_in_cell(sheet_name, [position[index_2][0], position[index_2][1]], list_1d[index_2])

	def make_random_xy_set_from_xyxy(self, xyxy, count_no=1):
		"""
		엑셀영역안에서 랜덤하게 셀주소를 돌려주는것

		:param xyxy:
		:param count_no:
		"""
		result = []
		x1, y1, x2, y2 = self.check_address_value(xyxy)

		for no in range(count_no):
			x = random.randint(x1, x2)
			y = random.randint(y1, y2)
			result.append([x, y])
		return result

	def make_same_len_for_list_2d(self, input_list_2d):
		"""
		change_list_to_samelen_list( input_list_2d)
		2차원 리스트의 최대 길이로 같게 만드는 것
		가끔 자료의 갯수가 달라서 생기는 문제가 발생할 가능성이 있는것을 맞추는것
		추가할때는 ""를 맞는갯수를 채워넣는다
		"""
		self.menu_dic['make_samelen_for_list_2d'] = {'표시여부': 'x', '그리드메뉴': ['make', 'samelen', 'for_list_2d'],
													 '실행메뉴': ['make', 'samelen', 'for_list_2d']}
		input_text = None
		max_num = max(map(lambda x: len(x), input_list_2d))
		result = []
		for one in input_list_2d:
			one_len = len(one)
			if max_num == one_len:
				result.append(one)
			else:
				one.extend([input_text] * (max_num - one_len))
				result.append(one)
		return result

	def make_scrollbar_in_range(self, sheet_name="", xyxy=""):
		"""
		엑셀의 시트에 스크롤바를 만드는것

		:param sheet_name:
		:param xyxy:
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		pxywh = self.change_xyxy_to_pxywh(sheet_name, xyxy)
		scrollbar_obj = sheet_object.Shapes.AddFormControl(Type=8, Left=pxywh[0], Top=pxywh[1], Width=pxywh[2],
															Height=pxywh[3])
		scrollbar_obj.Name = "abc_1"
		scrollbar_obj.ControlFormat.Value = 4
		scrollbar_obj.ControlFormat.Min = 0
		scrollbar_obj.ControlFormat.Max = 359
		scrollbar_obj.ControlFormat.SmallChange = 1
		scrollbar_obj.ControlFormat.LargeChange = 10
		scrollbar_obj.ControlFormat.LinkedCell = "$A$1"

	def make_serial_no(self, sheet_name, xyxy, last_len_char=3):
		"""
		바로위의 값과 비교해서, 알아서 연속된 번호를 만들어주는 기능
		맨마지막의 값을 읽어와서 그것에 1을 더한값을 돌려주는 것이다

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		:param last_len_char:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		range_object = self.get_range_object_by_xyxy(sheet_name, xyxy)

		upper_value = self.read_value_in_cell(sheet_name, [x1, y1])
		new_no = format(int(upper_value[:-1 * last_len_char]) + 1, )

		result = upper_value[last_len_char:] + str(int(upper_value[:-1 * last_len_char]) + 1)
		return result

	def make_several_unit_number(self, input_price):
		"""
		백만원단위, 전만원단위, 억단위로 구분

		:param input_price:
		:return:
		"""
		input_price = int(input_price)
		if input_price > 100000000:
			result = str('{:.If}'.format(input_price / 100000000)) + "억원"
		elif input_price > 10000000:
			result = str('{: .0f}'.format(input_price / 1000000)) + "백만원"
		elif input_price > 1000000:
			result = str('{:.If}'.format(input_price / 1000000)) + "백만원"
		return result


	def set_title_from_first_line_in_range(self, sheet_name="", xyxy=""):
		"""
		영역을 주면, 제일 첫번째 라인의 값들을 적절한 형태로 제목으로 만들어 주는 것

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		range_object = self.get_range_object_by_xyxy(sheet_name, xyxy)

		all_data = []
		for y in range(xyxy[1], xyxy[3] + 1):
			xylist_data = []
			for x in range(xyxy[0], xyxy[2] + 1):
				# 병합이 있는 자료를 위해서 필요한 것이다
				aa = self.check_merge_status_at_cell(sheet_name, [x, y])
				if aa:
					value = self.read_value_in_cell(sheet_name, [aa[2][0], aa[2][1]])
				else:
					value = self.read_value_in_cell(sheet_name, [x, y])

				# 양쪽 공백을 없앤다
				value = str(value).strip()
				xylist_data.append(value)

			# 2줄 이상의 제목라인이 있을때, 위 아래의것을 합치기 위해서 필요
			final_title = ""
			for one in xylist_data:
				if one:
					final_title = final_title + one + "_"
			# 아무런 제목도 없을경우는 가로의 숫자를 이용해서 만든 제목을 넣는다
			if final_title == "":
				final_title = "title_" + str(y) + "_"

			# 소문자로 만든다
			final_title = str(final_title[:-1]).lower()

			for bb in [[" ", "_"], ["&", ""], ["&", ""], ["(", ""], [")", ""], ["/", ""], ["-", ""], [".", ""],
						["%", ""]]:
				final_title = final_title.replace(bb[0], bb[1])


	def make_unique_id(self, xyxy=[2, 2, 21818, 6], start_no=100):
		"""
		자리수에 맞는 고유한번호 만들기 (_로 그냥 만들자)
		연속된 같은값일때만, 같은 숫자를 쓴다
		다른곳에 부분적으로 같은 이름이 있을수있다
		"""
		input_list_2d = self.read_value_in_range("", xyxy)
		result = []
		x_line_no = len(input_list_2d)
		y_line_no = len(input_list_2d[0])
		change_start_no = start_no

		for y in range(y_line_no):
			new_no = []
			for x in range(x_line_no):
				# 값이 없으면, None값으로 넣는다
				if input_list_2d[x][y] == "" or input_list_2d[x][y] == None:
					new_no.append("")
				else:
					if x == 0:
						new_no = [change_start_no, ]
					else:
						if input_list_2d[x][y] == input_list_2d[x - 1][y]:
							new_no.append(change_start_no)
						else:
							change_start_no = change_start_no + 1
							new_no.append(change_start_no)
			result.append(new_no)
			change_start_no = start_no  # 이부분을 없애면, 고유한 번호들이 할당된다

		for no, list_1d in enumerate(result):
			id1 = ""
			for one in list_1d:
				id1 = id1 + str(one) + "_"
			result[no].append(id1[:-1])

		return result

	def make_unique_words(self, input_list_2d):
		"""
		입력으로 들어온 자료들을 단어별로 구분하기위해서 만든것이며 /,&-등의 문자는 없앨려고 하는것이다
		"""
		list_1d = []
		for one in input_list_2d:
			list_1d.extend(one)
		temp_result = []
		for one in list_1d:
			one = str(one).lower()
			one = one.replace("/", "")
			one = one.replace(",", "")
			one = one.replace("&", "")
			one = one.replace("_", "")
			temp_result.extend(one.split(""))
		result = list(set(temp_result))
		return result

	def make_xy_list_for_box_style(self, xyxy):
		"""
		좌표를 주면, 맨끝만 나터내는 좌표를 얻는다

		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		:return:
		"""
		temp_1 = []
		for x in [xyxy[0], xyxy[2]]:
			temp = []
			for y in range(xyxy[1], xyxy[3] + 1):
				temp.append([x, y])
			temp_1.append(temp)

		temp_2 = []
		for y in [xyxy[1], xyxy[3]]:
			temp = []
			for x in range(xyxy[0], xyxy[2] + 1):
				temp.append([x, y])
			temp_2.append(temp)

		result = [temp_1[0], temp_2[1], temp_1[1], temp_2[0]]
		return result

	def making_tag(self, ):
		"""
		예제용

		:return:
		"""
		all_data = self.write_value_in_range("Sheet1", [1, 1, 90, 15])
		for no_1 in range(len(all_data)):
			x = int((no_1 + 1) / 5)
			y = (no_1 + 1) - x * 5
			for no_2 in range(15):
				self.write_value_in_cell("Tag", [x * 20 + no_2 + 4, y * 3 + 3], all_data[no_1][no_2])

	def manual(self):
		"""
		#간략한 이 모듈에 대한 설명입니다
		"""
		result = """
			"""
		return result

	def messagebox_for_input(self, input_title="Please Input Value"):
		"""
		입력창을 만들어서 입력값을 받는것
		"""
		result = self.xlapp.InputBox(input_title)
		return result

	def messagebox_for_show(self, input_text, input_title="Please Input Value"):
		"""
		사용하기 편하게 이름을 바꿈
		original : write_value_in_messagebox
		"""
		win32gui.MessageBox(0, input_text, input_title, 0)

	def move(self, sheet_list, xyxy_list):
		"""
		복사한후 붙여넣기

		:param sheet_list: 시트이름들
		:param xyxy_list:
		"""
		sheet_object_1 = self.check_sheet_name(sheet_list[0])
		x1, y1, x2, y2 = self.check_address_value(xyxy_list[0])
		my_range = sheet_object_1.Range(sheet_object_1.Cells(x1, y1), sheet_object_1.Cells(x2, y2))
		my_range.Copy()

		x21, y21, x22, y22 = self.check_address_value(xyxy_list[1])
		self.select_sheet(sheet_list[1])
		self.xlapp.ActiveSheet.Cells(x21, y22).Select()
		self.xlapp.ActiveSheet.Paste()

	def move_activecell_in_range_to_bottom(self, sheet_name="", xyxy=""):
		"""
		선택한 위치에서 제일왼쪽, 제일아래로 이동
		xlDown: - 4121,xlToLeft : - 4159, xlToRight: - 4161, xlUp : - 4162

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		"""
		self.check_sheet_name_n_xyxy(sheet_name, xyxy)
		self.range_object.End(-4121).Select()

	def move_arrange_two_sheet_y_02(self):
		"""
		두개의 시트에서 하나를 기준으로 다른 하나의 시트 내용을 정렬하는것
		첫번째 시트의 제일 윗줄을 기준으로 두번째 시트를 정렬 하는것

		"""
		input_list = []

		# 기준시트와 옮길시트의 이름을 갖고온다
		input_value = self.messagebox_for_input("Please input specific char : ex) sheet_a, sheet_b")
		sheet_names = input_value.split(",")

		# sheet_names=["aaa", "bbb"]

		# 사용한 범위를 갖고온다
		range_1 = self.read_address_for_usedrange(sheet_names[0])
		range_2 = self.read_address_for_usedrange(sheet_names[1])

		no_title2 = range_2[2]

		# 기준 시트의 제목을 읽어와서 저장한다
		title_1 = self.read_range_value(sheet_names[0], [1, range_1[1], 1, range_1[3]])
		title_1_list = []
		for no in range(1, len(title_1[0]) + 1):
			title_1_list.append([no, title_1[0][no - 1]])

		# 하나씩 옮길시트의 값을 읽어와서 비교한후 맞게 정렬한다
		for y1 in range(len(title_1_list)):
			found = 0
			basic_title = title_1_list[y1][1]
			# 기준자료의 제목이 비어있으면 새로이 한칸을 추가한다
			if basic_title == None or basic_title == "":
				self.insert_yline(sheet_names[1], y1 + 1)
				no_title2 = no_title2 + 1
			else:
				# 만약 기준시트의 제목보다 더 넘어가면 그냥 넘긴다
				if y1 > no_title2:
					pass
				else:
					for y2 in range(y1, no_title2 + 1):
						move_title = self.read_value_in_cell(sheet_names[1], [1, y2 + 1])
						if found == 0 and move_title == basic_title:
							found = 1
							if y1 == y2:
								pass
							else:
								self.move_yyline_in_sheet(sheet_names[1], sheet_names[1], y2 + 1, y1 + 1)

					if found == 0:
						# 빈칸을 하나 넣는다
						self.insert_yline(sheet_names[1], y1 + 1)

	def move_cell(self, sheet_name_1, xy_from, sheet_name_2, xy_to):
		"""
		1 개의 셀만 이동시키는 것. 다른 시트로 이동도 가능

		2023-09-27 : 다른 시트로도 옮길수있도록 변경

		:param sheet_name_1:
		:param xy_from:
		:param sheet_name_2:
		:param xy_to:
		"""
		sheet_object_1 = self.check_sheet_name(sheet_name_1)
		sheet_object_2 = self.check_sheet_name(sheet_name_2)
		x1, y1, x2, y2 = self.check_address_value(xy_from)
		sheet_object_1.Cells(x1, y1).Cut()
		x1, y1, x2, y2 = self.check_address_value(xy_to)
		range_object = sheet_object_2.Cells(x1, y1)
		sheet_object_2.Paste(range_object)

	def move_cell_in_front_by_startwith_aaa(self, startwith="*"):
		"""
		맨앞에 특정글자가 있으면, 앞으로 옮기기

		:param startwith:
		:return:
		"""
		x, y, x2, y2 = self.read_address_for_selection()
		self.insert_yline("", y)
		for one_x in range(x, x2):
			one_value = self.read_value_in_cell("", [one_x, y + 1])
			if one_value.startswith(startwith):
				self.write_value_in_cell("", [one_x, y], one_value)
				self.write_value_in_cell("", [one_x, y + 1], None)

	def move_cell_value_to_another_sheet(self, sheet_list, xy_list):
		"""
		다른시트로 값1개 옮기기
		입력형태 : [시트이름1, 시트이름2], [[2,3]. [4,5]]

		:param sheet_list:
		:param xy_list:
		"""

		sheet_list = self.change_xylist_to_list(sheet_list)
		xy_list = self.change_xylist_to_list(xy_list)

		sheet_object_1 = self.check_sheet_name(sheet_list[0])
		x1, y1 = xy_list[0]
		sheet_object_1.Cells(x1, y1).Cut()

		sheet_object_2 = self.check_sheet_name(sheet_list[1])
		x2, y2 = xy_list[1]
		sheet_object_2.Cells(x2, y2).Insert()

	def move_data_by_step_for_selection(self, sheet_name, xyxy, insert_step, insert_no=1, range_ext=False,
										del_or_ins="ins"):
		"""
		:param sheet name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		:param insert _step: 몇번째마다, 삽입이나 삭제를 할것인지
		:param insert_no: 몇개씩 넣을것인지
		:param range_ext: 넘어가는 자료가 있으면, 영역을 넘어서 글씨를 쓸것인지 아닌지를 설정
		:param del or_ins: 삭제인지 아니면 추가인지를 확인하는것
		"""
		# 전처리 구간
		data_2d = self.read_value_in_range(sheet_name, xyxy)

		changed_data_2d = []
		for list_1d in data_2d:
			temp = []
			for one in list_1d:
				temp.append(one)
			changed_data_2d.append(temp)

		empty_1d = []
		for one in changed_data_2d[0]:
			empty_1d.append("")

		actual_position = 0
		if del_or_ins == "ins":
			for no in range(len(changed_data_2d)):
				namuji = (no + 1) % insert_step
				if namuji == 0:
					for no_1 in range(insert_no):
						changed_data_2d.insert(actual_position, empty_1d)
						actual_position = actual_position + 1
			actual_position = actual_position + 1

		self.write_value_in_range(sheet_name, xyxy, changed_data_2d)

	def move_data_to_right_by_step(self, input_list_1d, step_no):
		"""
		1 차원으로 들어온 기료를 갯수에 i도록 분리해서 2차원의 자료로 만들어 주는것
		"""
		result = []
		for partial_list in input_list_1d[::step_no]:
			result.append(partial_list)
		return result

	def move_degree_distance(self, degree, distance):
		"""
		move_degree_distance( degree, distance)
		현재 위치 x,y에서 30도로 20만큼 떨어진 거리의 위치를 돌려주는 것
		"""
		degree = degree * 3.141592 / 180
		y = distance * math.cos(degree)
		x = distance * math.sin(degree)
		return [x, y]

	def move_position_in_selection(self, sheet_name, xyxy, insert_step, insert_no=1, range_ext=False, del_or_ins="ins"):
		"""
		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		:param insert_step: 몇번째마다, 삽입이나 삭제를 할것인지
		:param insert_no: 몇개씩 넣을것인지
		:param range_ext: 넘어가는 자료가 있으면, 영역을 넘어서 글씨를 쓸것인지 아닌지를 설정 :param del_or_ins: 삭제인지 아니면 추강니지를 확인하는것
		: return:
		"""
		# 전처리 구간
		data_2d = self.read_value_in_range(sheet_name, xyxy)
		changed_data_2d = []
		for list_1d in data_2d:
			temp = []
			for one in list_1d:
				temp.append(one)
			changed_data_2d.append(temp)

		empty_1d = []

		for one in changed_data_2d[0]:
			empty_1d.append("")
		actual_position = 0

		if del_or_ins == "ins":
			for no in range(len(changed_data_2d)):
				mok = (no + 1) % insert_step
				if mok == 0:
					for no_1 in range(insert_no):
						changed_data_2d.insert(actual_position, empty_1d)
						actual_position = actual_position + 1
				actual_position = actual_position + 1
		self.write_value_in_range(sheet_name, xyxy, changed_data_2d)

	def move_range(self, sheet_name_old, xyxy_from, sheet_name_new, xyxy_to):
		"""
		모든값을 그대로 이동시키는 것
		cut -> paste

		:param sheet_name_old:
		:param xyxy_from:
		:param sheet_name_new:
		:param xyxy_to:
		"""
		sheet_object_old = self.check_sheet_name(sheet_name_old)
		sheet_object_new = self.check_sheet_name(sheet_name_new)
		x1, y1, x2, y2 = self.check_address_value(xyxy_from)
		my_range1 = sheet_object_old.Range(sheet_object_old.Cells(x1, y1), sheet_object_old.Cells(x2, y2))
		my_range1.Cut()
		x1, y1, x2, y2 = self.check_address_value(xyxy_to)
		my_range2 = sheet_object_new.Range(sheet_object_new.Cells(x1, y1), sheet_object_new.Cells(x2, y2))
		sheet_object_new.Paste(my_range2)

	def move_range_ystep(self, sheet_name, xyxy, input_y, step):
		"""
		가로의 자료를 설정한 갯수만큼 한줄로 오른쪽으로 이동
		"""
		new_x = 0
		new_y = input_y
		for x in range(xyxy[0], xyxy[2] + 1):
			for y in range(xyxy[1], xyxy[3] + 1):
				new_x = new_x + 1
				value = self.read_cell_value("", [x, y])
				if value == None:
					value = ""
				self.write_cell_value("", [new_x, new_y], value)

	def move_rangevalue_line_value(self, sheet_name="", xyxy=""):
		"""
		move_value_01(self, sheet_name="", xyxy=""):
		선택한영역의 자료를 세로의 한줄로 만드는것
		새로운 세로행을 만든후 그곳에 두열을 서로 하나씩 포개어서 값넣기
		a 1  ==> a
		b 2	 1
				b
				2
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		range_object = self.get_range_object_by_xyxy(sheet_name, xyxy)

		output_list = self.read_range_value(sheet_name, xyxy)
		make_one_list = self.yt.list_change_2d_1d(output_list)
		self.insert_yy(sheet_name, y2 + 1)
		self.write_range_value_ydirection_only(sheet_name, [x1, y2 + 1], make_one_list)

	def move_shape(self, sheet_name, shape_object, top, left):
		"""
		shape_object: 이동시림 도형 이름

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param shape_object:
		:param top:
		:param left:
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		oShape = sheet_object.Shapes(shape_object)
		oShape.Top = oShape.Top + top
		oShape.Left = oShape.left + left

	def move_shape_by_xywh(self, input_shape_obj, xywh_list):
		"""
		도형을 이동시키는 것
		"""
		input_shape_obj.Top = xywh_list[0]
		input_shape_obj.Left = xywh_list[1]
		input_shape_obj.Width = xywh_list[2]
		input_shape_obj.Height = xywh_list[3]


	def move_shape_position(self, sheet_name, shape_no, top, left):
		"""
		도형을 이동 시키는 것

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param shape_no:
		:param top:
		:param left:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		shape_no = self.check_shape_name(sheet_name, shape_no)

		sheet_object.Shapes(shape_no).Top = sheet_object.Shapes(shape_no).Top + top
		sheet_object.Shapes(shape_no).Left = sheet_object.Shapes(shape_no).left + left



	def move_shape_position_by_dxy(self, sheet_name, shape_no, dxy):
		"""
		도형을 이동시키는 것

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param shape_no: 이동시킬 도형 이름
		:param dxy: 현재의 위치에서 각도를 옮기는 것
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		shape_no = self.check_shape_name(sheet_name, shape_no)
		sheet_object.Shapes(shape_no).incrementLeft(dxy)

	def move_sheet_to_end(self, sheet_name):
		"""
		시트를 제일 앞으로 이동시키는 방법
		:param sheet_name:
		:return:
		"""
		self.xlbook.Worksheets(sheet_name).Move(None, After=self.xlbook.Worksheets(self.xlbook.Worksheets.Count))

	def move_sheet_to_first(self, sheet_name):
		"""
		시트를 제일 앞으로 이동시키는 방법

		:param sheet_name:
		"""
		self.move_sheet_to_position_no(sheet_name, 1)

	def move_sheet_to_position_no(self, sheet_name, input_no):
		"""
		선택된 시트를 앞에서 몇번째로 이동시키는 것

		:param sheet_name:
		:param input_index:
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)

		all_shhet_names = self.read_all_sheet_name()
		current_sheet_no = 0
		for index, value in enumerate(all_shhet_names):
			if sheet_name == value:
				current_sheet_no = index + 1
				break

		if input_no <= current_sheet_no:
			move_to = input_no
		else:
			move_to = input_no + 1

		sheet_object.Move(Before=self.xlbook.Worksheets(move_to))

	def move_sheet_with_new_file(self, sheet_name):
		"""
		시트를 제일 앞으로 이동시키는 방법
		:param sheet_name:
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)

		sheet_object.Move(After=self.xlbook.Worksheets(1))

	def move_value_if_startwith_input_value_after_insert_new_line(self, sheet_name, xyxy, startwith="*"):
		"""
		맨앞부분에 세로줄을 하나 만든후
		입력값으로받은 글자와 각 셀의 앞부분부터 같은 값일경우 한줄 앞으로 값을 이동시키는 것

		가끔 많은 자료를 구분하는 경우가 필요해서 만든 것이다
		맨앞에 특정글자가 있으면, 앞으로 옮기기
		:param startwith:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x, y, x2, y2 = self.check_address_value(xyxy)

		self.insert_yline("", y)
		for one_x in range(x, x2):
			one_value = self.read_value_in_cell("", [one_x, y + 1])
			if one_value.startswith(startwith):
				self.write_value_in_cell("", [one_x, y], one_value)
				self.write_value_in_cell("", [one_x, y + 1], None)

	def move_value_in_cell_to_another_sheet(self, sheet_name_1="", xyxy_1="", sheet_name_2="", xyxy_2=""):
		"""

		값을 일정한 영역에서 갖고온다
		만약 영역을 두개만 주면 처음과 끝의 영역을 받은것으로 간주해서 알아서 처리하도록 변경하였다

		:param sheet_name_1:
		:param xyxy_1:
		:param sheet_name_2:
		:param xyxy_2:
		:return:
		"""
		sheet_object_1 = self.check_sheet_name(sheet_name_1)

		x11, y11, x21, y21 = self.check_address_value(xyxy_1)

		cell_value = sheet_object_1.Cells(x11, y11).Value
		cell_value = self.write_value_in_cell(sheet_name_2, xyxy_2, cell_value)

	def move_value_in_range_to_left_except_emptycell(self, sheet_name="", xyxy=""):
		"""
		x열을 기준으로 값이 없는것은 왼쪽으로 옮기기
		전체영역의 값을 읽어오고, 하나씩 다시 쓴다

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		range_object = self.get_range_object_by_xyxy(sheet_name, xyxy)

		value_2d = self.read_value_in_range(sheet_name, xyxy)
		self.delete_value_in_range(sheet_name, xyxy)
		for x in range(0, x2 - x1 + 1):
			new_y = 0
			for y in range(0, y2 - y1 + 1):
				value = value_2d[x][y]
				if value == "" or value == None:
					pass
				else:
					sheet_object.Cells(x + x1, new_y + y1).Value = value
					new_y = new_y + 1

	def move_value_of_range_to_another_sheet(self, sheet_name_old, xyxy_from, sheet_name_new, xyxy_to):
		"""
		모든값을 그대로 이동시키는 것
		cut -> paste

		:param sheet_name_old:
		:param xyxy_from:
		:param sheet_name_new:
		:param xyxy_to:
		"""
		sheet_object_old = self.check_sheet_name(sheet_name_old)
		sheet_object_new = self.check_sheet_name(sheet_name_new)
		x1, y1, x2, y2 = self.check_address_value(xyxy_from)
		range_object1 = sheet_object_old.Range(sheet_object_old.Cells(x1, y1),
												sheet_object_old.Cells(x2, y2))
		range_object1.Cut()
		x1, y1, x2, y2 = self.check_address_value(xyxy_to)
		range_object2 = sheet_object_new.Range(sheet_object_new.Cells(x1, y1),
												sheet_object_new.Cells(x2, y2))
		sheet_object_new.Paste(range_object2)

	def move_value_without_empty_cell_01(self, sheet_name="", xyxy=""):
		"""
		선택한 영역에서 세로의 값중에서 빈셀을 만나면
		아래의 값중 있는것을 위로 올리기
		전체영역의 값을 읽어오고,
		하나씩 다시 쓴다
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		range_object = self.get_range_object_by_xyxy(sheet_name, xyxy)

		read_data = self.read_range_value(sheet_name, xyxy)
		self.delete_range_value(sheet_name, xyxy)
		for y in range(y1, y2 + 1):
			new_x = x1
			for x in range(x1, x2 + 1):
				value = self.read_cell_value(sheet_name, [x, y])
				if value != "":
					self.write_cell_value(sheet_name, [new_x, y])
					new_x = new_x + 1

	def move_values_between_specific_words_01(self, sheet_name="", xyxy=""):
		"""
		괄호안의 모든 글자를 괄호를 포함하여 삭제하는것

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		range_object = self.get_range_object_by_xyxy(sheet_name, xyxy)

		input = self.messagebox_for_input("Please input specific char : ex) a, b")
		input_new = input.split(",")
		# re_basic = "\\"+str(input_new[0]) + "[\^" + str(input_new[0]) +"]*\\" + str(input_new[1])

		input_new[0] = str(input_new[0]).strip()
		input_new[1] = str(input_new[1]).strip()

		special_char = ".^$*+?{}[]\|()"
		# 특수문자는 역슬래시를 붙이도록
		if input_new[0] in special_char: input_new[0] = "\\" + input_new[0]
		if input_new[1] in special_char: input_new[1] = "\\" + input_new[1]

		re_basic = str(input_new[0]) + ".*" + str(input_new[1])

		self.insert_yyline(sheet_name, y1 + 1)
		for x in range(x1, x2 + 1):
			for y in range(y1, y2 + 1):
				one_value = str(self.read_value_in_cell(sheet_name, [x, y]))
				result_list = re.findall(re_basic, one_value)
				if result_list == None or result_list == []:
					pass
				else:
					self.write_cell_value(sheet_name, [x, y + 1], result_list[0])

	def move_without_empty_line_01(self):
		"""
		선택한 영역에서 각 세로행의 자료가 입삭제할것들을 입력받은 빈칸이상이 있으면 당겨오는 것이다
		이것은 여러곳에서 갖고온 자료들중 삭제한후에 값들을 당겨서 하기에 손이 많이 가는것을 코드로 만든 것이다

		"""
		[x1, y1, x2, y2] = self.read_address_for_selection()
		# 0칸일때 빈 공간이 없는것이다
		step_line = int(self.messagebox_for_input("0 : 빈칸이 없는것입니다")) + 1

		for y in range(y1, y2 + 1):
			temp_data = []
			flag = 0
			for x in range(x1, x2 + 1):
				temp_value = self.read_value_in_cell("", [x, y])
				if temp_value == "" or temp_value == None:
					flag = flag + 1
				else:
					flag = 0
				if flag >= step_line:
					pass
				else:
					temp_data.append([temp_value])
					self.write_cell_value("", [x, y], "")

			self.write_value_in_range_for_speed("", [1, y], temp_data)

	def move_xline_value_to_multi_input_lines(self, xyxy, repeat_no, start_xy):
		"""
		x라인의 가로 한줄의 자료를 여반복갯수에 따라서 시작점에서부터 아래로 복사하는것
		입력자료 : 1줄의 영역, 반복하는 갯수, 자료가 옮겨갈 시작주소

		:param xyxy:
		:param repeat_no:
		:param start_xy:
		"""
		all_data_set = self.read_value_in_range("", xyxy)
		for no in range(len(all_data_set[0])):
			mok, namuji = divmod(no, repeat_no)
			new_x = mok + start_xy[0]
			new_y = namuji + start_xy[1]
			self.write_value_in_cell("", [new_x, new_y], all_data_set[0][no])

	def move_xline_value_to_multi_lines(self, xyxy, repeat_no, start_xy):
		"""
		x라인의 가로 한줄의 자료를 여반복갯수에 따라서 시작점에서부터 아래로 복사하는것
		입력자료 :  1줄의 영역, 반복하는 갯수, 자료가 옮겨갈 시작주소

		:param xyxy:
		:param repeat_no:
		:param start_xy:
		:return:
		"""
		all_data_set = self.read_value_in_range("", xyxy)
		for no in range(len(all_data_set[0])):
			mok, namuji = divmod(no, repeat_no)
			new_x = mok + start_xy[0]
			new_y = namuji + start_xy[1]
			self.write_value_in_cell("", [new_x, new_y], all_data_set[0][no])

	def move_xxline_to_another_sheet(self, sheet_name1, sheet_name2, xx0, xx1):
		"""
		세로의 값을 이동시킵니다
		"""
		sheet1 = self.check_sheet_name(sheet_name1)
		sheet2 = self.check_sheet_name(sheet_name2)
		xx0_1, xx0_2 = self.check_xy_address(xx0)
		xx1_1, xx1_2 = self.check_xy_address(xx1)
		xx0_1 = self.change_char_num(xx0_1)
		xx0_2 = self.change_char_num(xx0_2)
		xx1_1 = self.change_char_num(xx1_1)
		xx1_2 = self.change_char_num(xx1_2)
		sheet1.Select()
		sheet1.Rows(str(xx0_1) + ':' + str(xx0_2)).Select()
		sheet1.Rows(str(xx0_1) + ':' + str(xx0_2)).Copy()
		sheet2.Select()
		sheet2.Rows(str(xx1_1) + ':' + str(xx1_2)).Select()
		sheet2.Paste()

	def move_xy_to_top_end_of_selection(self, sheet_name="", xyxy=""):
		"""
		영역의 제일 위로 이동

		:param sheet_name: 시트이름
		:param xy: [가로번호, 세로번호]
		:return:
		"""
		xldown = -4121
		xltoleft = -4159
		xltoright = -4161
		xlup = -4162

		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		range_object = self.get_range_object_by_xyxy(sheet_name, xyxy)
		for num in [xldown, xltoleft, xltoright, xlup]:
			range_object.End(num).Select()
			aa = self.read_address_in_activecell()

	def move_y(self, sheet_list, yy_list):
		"""
		가로의 값을 이동시킵니다
		"""
		range_1 = self.check_range_yy(sheet_list[0], yy_list[0])
		range_2 = self.check_range_yy(sheet_list[1], yy_list[1])
		range_1.Select()
		range_1.Cut()
		range_2.Select()
		range_2.Insert()

	def move_yline_value_to_multi_input_lines(self, xyxy, repeat_no, start_xy):
		"""
		y라인의 가로 한줄의 자료를 여반복갯수에 따라서 시작점에서부터 아래로 복사하는것
		입력자료 : 1줄의 영역, 반복하는 갯수, 자료가 옮겨갈 시작주소

		:param xyxy:
		:param repeat_no:
		:param start_xy:
		"""
		all_data_set = self.read_value_in_range("", xyxy)
		for no in range(len(all_data_set)):
			mok, namuji = divmod(no, repeat_no)
			new_x = mok + start_xy[0]
			new_y = namuji + start_xy[1]
			self.write_value_in_cell("", [new_x, new_y], all_data_set[no][0])

	def move_yline_value_to_multi_lines(self, xyxy, repeat_no, start_xy):
		"""
		y라인의 가로 한줄의 자료를 여반복갯수에 따라서 시작점에서부터 아래로 복사하는것
		입력자료 :  1줄의 영역, 반복하는 갯수, 자료가 옮겨갈 시작주소

		:param xyxy:
		:param repeat_no:
		:param start_xy:
		:return:
		"""
		all_data_set = self.read_value_in_range("", xyxy)
		for no in range(len(all_data_set)):
			mok, namuji = divmod(no, repeat_no)
			new_x = mok + start_xy[0]
			new_y = namuji + start_xy[1]
			self.write_value_in_cell("", [new_x, new_y], all_data_set[no][0])

	def move_ystep(self, sheet_name, xyxy, input_x, step):
		"""
		move_ystep(sheet_name="", xyxy="", input_w, step)
		가로의 자료를 설정한 갯수만큼 한줄로 오른쪽으로 이동
		"""
		self.menu_dic['move_ystep'] = {'표시여부': 'x', '그리드메뉴': ['move', 'ystep', '없음'], '실행메뉴': ['move', 'ystep', '']}
		new_y = 0
		new_x = input_x
		for y in range(xyxy[0], xyxy[2] + 1):
			for x in range(xyxy[1], xyxy[3] + 1):
				new_y = new_y + 1
				value = self.read_value_in_cell("", [x, y])
				if value == None:
					value = ""
				self.write_value_in_cell("", [new_y, new_x], value)

	def move_yy(self, sheet_name1, sheet_name2, yy0, yy1):
		"""
		세로의 값을 이동시킵니다
		"""
		sheet1 = self.check_sheet_name(sheet_name1)
		sheet2 = self.check_sheet_name(sheet_name2)
		yy0_1, yy0_2 = self.check_xy_address(yy0)
		yy1_1, yy1_2 = self.check_xy_address(yy1)
		yy0_1 = self.change_num_char(yy0_1)
		yy0_2 = self.change_num_char(yy0_2)
		yy1_1 = self.change_num_char(yy1_1)
		yy1_2 = self.change_num_char(yy1_2)
		sheet1.Select()
		sheet1.Columns(str(yy0_1) + ':' + str(yy0_2)).Select()
		sheet1.Columns(str(yy0_1) + ':' + str(yy0_2)).Cut()
		sheet2.Select()
		sheet2.Columns(str(yy1_1) + ':' + str(yy1_2)).Select()
		sheet2.Columns(str(yy1_1) + ':' + str(yy1_2)).Insert()

	def move_yyline_to_another_sheet(self, sheet1, sheet2, yy1, yy2):
		"""
		copy_yline( sheet_list, yy_list)
		가로의 값을 복사
		"""
		self.menu_dic['copy_yyline'] = {'표시여부': 'x', '그리드메뉴': ['copy', 'rows', '없음'], '실행메뉴': ['copy', 'rows', '']}
		sheet1 = self.check_sheet_name(sheet1)
		sheet2 = self.check_sheet_name(sheet2)
		yy0_1, yy0_2 = self.check_yx_address(yy1)
		yy1_1, yy1_2 = self.check_yx_address(yy2)
		yy0_1 = self.change_char_to_num(yy0_1)
		yy0_2 = self.change_char_to_num(yy0_2)
		yy1_1 = self.change_char_to_num(yy1_1)
		yy1_2 = self.change_char_to_num(yy1_2)
		sheet1.Select()
		sheet1.Rows(str(yy0_1) + ':' + str(yy0_2)).Select()
		sheet1.Rows(str(yy0_1) + ':' + str(yy0_2)).Copy()
		sheet2.Select()
		sheet2.Rows(str(yy1_1) + ':' + str(yy1_2)).Select()
		sheet2.Paste()

	def multi_input_vlookup(self, sheet_name, xyxy, search_no_list, search_value_list, find_no, option_all=True):
		"""
		#여러줄이 같은

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		:param search_no_list:
		:param search_value_list:
		:param find_no:
		:param option_all:
		"""
		result = []
		list_2d = self.read_value_in_range(sheet_name, xyxy)
		checked_no = len(search_value_list)

		for list_1d in list_2d:
			temp_no = 0
			for index, num in enumerate(search_no_list):
				if option_all:
					# 모든 값이 다 같을때
					if list_1d[num - 1] == search_value_list[index]:
						temp_no = temp_no + 1
					else:
						break
				else:
					# 값이 일부분일때도 OK
					if search_value_list[index] in list_1d[num - 1]:
						temp_no = temp_no + 1
					else:
						break
			if temp_no == checked_no:
				result = list_1d[find_no - 1]
		return result

	def multi_vlookup(self, input_value1, input_value2):
		"""
		에제-엑셀) 여러항목이 같은 값의 원하는 것만 갖고오기
		여러항목이 같은 값의 원하는 것만 갖고오기
		 input_valuel = [자료의영역, 같은것이있는위치, 결과값의위치]
		"""

		input_value1 = self.change_xylist_to_list(input_value1)
		input_value2 = self.change_xylist_to_list(input_value2)

		base_data2d = self.read_value_in_range("", input_value1[0])
		compare_data2d = self.read_value_in_range("", input_value2[0])
		result = ""
		for one_data_1 in base_data2d:
			gijun = []
			one_data_1 = list(one_data_1)
			for no in input_value1[1]:
				gijun.append(one_data_1[no - 1])
			x = 0

			for value_1d in compare_data2d:
				value_1d = list(value_1d)
				x = x + 1
				bikyo = []

				for no in input_value2[1]:
					bikyo.append(value_1d[no - 1])

					if gijun == bikyo:
						result = one_data_1[input_value1[2] - 1]
						self.write_value_in_cell("", [x, input_value2[2]], result)

	def new_button(self, sheet_name, xyxy, title=""):
		"""
		엑셀의 시트위에 버튼을 만드는것.

		버튼을 만들어서 그 버튼에 매크로를 연결하는 데,익서은 그냥 버튼만 만드는 것이다
		Add(왼쪽의 Pixel, 위쪽 Pixce, 넓이, 높이)

		:param sheet_name: 시트이름
		:param xyxy: 버튼 크기
		:param title: 버튼위에 나타나는 글씨
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		new_btn = sheet_object.Buttons()
		left_px, top_px, width_px, height_px = self.read_coord_in_cell(sheet_name, xyxy)
		new_btn.Add(left_px, top_px, width_px, height_px)
		new_btn.Text = title

	def new_button_with_macro(self, sheet_name, xyxy, macro_code="", title=""):
		"""
		매크로랑 연결된 버튼을 만드는것
		버튼을 만들어서 그 버튼에 매크로를 연결하는 것이다
		매크로와 같은것을 특정한 버튼에 연결하여 만드는것을 보여주기위한 것이다

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트 sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호 range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:param macro_code: macro code, 매크로 코드
		:param title: caption for button, 버튼위에 나타나는 글씨
		:return: X / 없음
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		range_object = self.get_range_object_by_xyxy(sheet_name, xyxy)

		new_btn = sheet_object.Buttons()
		sheet_object.Cells(x1, y1).Select()
		left_px, top_px, width_px, height_px = self.read_coord_in_cell("", [x1, y1])
		new_btn.Add(left_px, top_px, width_px, height_px)
		new_btn.OnAction = macro_code
		new_btn.Text = title

	def new_button_with_macro_name(self, sheet_name, xyxy, macro_name="", title=""):
		"""
		버튼을 만들어서 그 버튼에 입력된 매크로를 연결하는 것이다
		매크로와 같은것을 특정한 버튼에 연결하여 만드는것을 보여주기위한 것이다

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2]로 넣으면 , (왼쪽의 Pixel, 위쪽 Pixce, 넓이, 높이)이 들어감
		:param macro_code: 매크로 코드
		:param title: 버튼위에 나타나는 글씨
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		new_btn = sheet_object.Buttons()
		left_px, top_px, width_px, height_px = self.read_coord_in_cell("", xyxy)
		new_btn.Add(left_px, top_px, width_px, height_px)
		new_btn.OnAction = macro_name
		new_btn.Text = title

	def new_chart(self, sheet_name, dispaly_xyxy, chart_style, data_xyxy, main_title):
		"""
		챠트를 만드는 것  기본적인 설정을 해서 만듭니다

		:param sheet_name:
		:param dispaly_xyxy:
		:param chart_style:
		:param data_xyxy:
		:param main_title:
		:return:
		"""
		chart_style_vs_enum = {"line": 4, "pie": 5}
		sheet_object = self.check_sheet_name(sheet_name)
		data_range_object = sheet_object.Range(sheet_object.Cells(data_xyxy[0], data_xyxy[1]),
												sheet_object.Cells(data_xyxy[2], data_xyxy[3]))
		pxywh = self.change_xyxy_to_pxywh(sheet_name, dispaly_xyxy)
		chart_obj_all = sheet_object.ChartObjects().Add(pxywh[0], pxywh[1], pxywh[2], pxywh[3])
		chart_obj_all.Chart.SetSourceData(Source=data_range_object)
		chart_obj = chart_obj_all.Chart
		chart_obj.ChartType = chart_style_vs_enum[chart_style]
		if main_title:
			chart_obj.HasTitle = True  # 차트 제목 나오게(False면 안보임)  chart_obj.ChartTitle.Text = main_title # 차트 제목 설정
		return chart_obj

	def new_chart_1(self, sheet_name, chart_type, pxywh, source_xyxy):
		"""
		챠트를 만드는 것

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param pxywh:
		:param source_xyxy:
		"""

		chart_type = self.check_chart_style(chart_type)
		sheet_object = self.check_sheet_name(sheet_name)
		chart_object = sheet_object.Chartobjects.Add(pxywh)
		x1, y1, x2, y2 = self.check_address_value(source_xyxy)
		self.r1c1 = self.change_xyxy_to_r1c1([x1, y1, x2, y2])
		range_object = sheet_object.Range(self.r1c1)
		chart_object.SetSourceData(range_object)
		chart_object.ChartType = chart_type
		return chart_object

	def new_dic(self, old_dic, key_list, value):
		"""
		어떤 사전형식의 자료를 넣으면 알아서 분리해 주는것
		dim : 1차원자료인지 아닌지처럼, 몇차원으로 만드는 것
		그차원에서 key값과 value값
		"""
		temp = ""
		icount = len(key_list) - 1
		for index, one_key in enumerate(key_list):
			temp = temp + f"[{one_key}]"
			if icount == index:
				try:
					exec(f"old_dic{temp}=one_key")
				except:
					exec(f"old_dic{temp}=one_key")
			else:
				try:
					exec(f"old_dic{temp}=one_key")
				except:
					exec(f"old_dic{temp}=one_key")
		return old_dic

	def new_excel_file_for_xyxy(self, sheet_name, xyxy, file_name="D:\\aaa.xlsx"):
		"""
		현재화일의 자료를 복사해서
		선택영역에서 같은 영역의 자료들만 묶어서 엑셀화일 만들기

		:param sheet_name: 시트이름
		:param xyxy: 영역의 xy형식의 좌표
		:param file_name: 화일 이름
		"""
		range_object = self.make_range_object(sheet_name, xyxy)
		range_object.Select()
		self.xlapp.selection.Copy()
		self.new_workbook("")
		sheet_object = self.check_sheet_name("")
		sheet_object.Cells(1, 1).Select()
		sheet_object.Paste()
		self.save(file_name)

	def new_password(self, isnum="yes", istext_small="yes", istext_big="yes", isspecial="no", len_num=10):
		"""
		엑셀시트의 암호를 풀기위해 암호를 계속 만들어서 확인하는 것
		메뉴에서 제외

		:param isnum:
		:param istext_small:
		:param istext_big:
		:param isspecial:
		:param len_num:
		:return:
		"""
		check_char = []
		if isnum == "yes":
			check_char.extend(list(string.digits))
		if istext_small == "yes":
			check_char.extend(list(string.ascii_lowercase))
		if istext_big == "yes":
			check_char.extend(list(string.ascii_uppercase))
		if isspecial == "yes":
			for one in "!@#$%^*_-":
				check_char.extend(one)

		zz = itertools.combinations_with_replacement(check_char, len_num)
		for aa in zz:
			try:
				pswd = "".join(aa)
				# pcell에 있는것
				self.set_sheet_lock_off("", pswd)
				break
			# print("발견", pswd)
			except:
				pass

	def new_picture_by_pixel(self, sheet_name, file_path, pxpywh, link=0, image_in_file=1):
		"""
		시트에 픽셀크기로 그림 넣기

		:param sheet_name:
		:param file_path:
		:param pxpywh:
		:param link:
		:param image_in_file:
		:return:
		"""
		shape_obj = self.add_picture_in_sheet_by_pixel(sheet_name, file_path, pxpywh, link, image_in_file)
		return shape_obj

	def new_picture_in_sheet(self, sheet_name, file_path, xywh, link=0, image_in_file=1):
		"""
		시트에 그림 넣기

		:param sheet_name:
		:param file_path:
		:param xywh:
		:param link:
		:param image_in_file:
		:return:
		"""
		shape_obj = self.insert_picture_in_sheet(sheet_name, file_path, xywh, link, image_in_file)
		return shape_obj

	def new_picture_in_sheet_by_pixel(self, sheet_name, file_path, pxpywh, link=0, image_in_file=1):
		"""
		그림을 픽셀크기로 시트에 넣는 것

		:param sheet_name: 시트이름
		:param file_path: file_path
		:param pxpywh:
		:param link:
		:param image_in_file:
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		shape_obj = sheet_object.Shapes.AddPicture(file_path, link, image_in_file, pxpywh[0], pxpywh[1], pxpywh[2],
													pxpywh[3])
		return shape_obj

	def new_shape_at_pxyxy(self, sheet_name, pxyxy, shape_no=1):
		"""
		특정위치에 도형을 만드는 것

		:param sheet_name:
		:param pxyxy:
		:param shpae_no:
		"""
		if type(shape_no) == type(123):
			pass
		elif shape_no in list(self.vars["shape_enum"].keys()):
			shape_no = self.vars["shape_enum"][shape_no]

		sheet_object = self.check_sheet_name(sheet_name)
		px1, py1, px2, py2 = pxyxy
		shape_obj = sheet_object.Shapes.AddShape(shape_no, px1, py1, px2, py2)
		return shape_obj

	def new_shape_by_xywh(self, sheet_name, shape_no=35, xywh=""):
		"""
		그림을 픽셀크기로 시트에 넣는 것

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param shape_no: shape_no, 엑셀에서 정의한 도형의 번호
		:param xywh: [x, y, width, height], 왼쪽윗부분의 위치에서 너비와 높이
		"""
		if type(shape_no) == type(123):
			pass
		elif shape_no in list(self.vars["shape_enum"].keys()):
			shape_no = self.vars["shape_enum"][shape_no]

		sheet_object = self.check_sheet_name(sheet_name)
		pxyxy = self.change_xyxy_to_pxyxy([xywh[0], xywh[1]])
		shape_obj = sheet_object.Shapes.Addshape(shape_no, pxyxy[0], pxyxy[1], xywh[2], xywh[3])
		return shape_obj

	def new_shape_by_xyxy(self, sheet_name, shape_no=35, xyxy=""):
		"""
		도형객체를 추가하는것

		shape_no : 엑셀에서 정의한 도형의 번호
		xywh : 왼쪽윗부분의 위치에서 너비와 높이
		"""
		sheet_object = self.check_sheet_name(sheet_name)

		# 도형이 숫자이면 그대로, 문자이면 기본자료에서 찾도록 한다
		if type(shape_no) == type(123):
			pass
		elif shape_no in list(self.vars["shape_enum"].keys()):
			shape_no = self.vars["shape_enum"][shape_no]

		xywh = self.change_xyxy_to_pxywh(sheet_name, xyxy)
		shape_obj = sheet_object.Shapes.Addshape(shape_no, xywh[0], xywh[1], xywh[2], xywh[3])
		return shape_obj

	def new_shape_for_number_circle_by_setup(self, sheet_name, xy="", input_no=1):
		"""
		기본적인 자료를 제외하고, 나머지는 setup자료를 사용한다
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		pxyxy = self.change_xyxy_to_pxyxy(xy)

		rgb_list_1d = self.color.change_scolor_to_rgb(self.vars["shape"]["color"])
		rgb_int = self.color.change_rgb_to_rgbint(rgb_list_1d)

		Shp1 = sheet_object.Shapes.AddShape(9, pxyxy[0], pxyxy[1], self.vars["shape"]["width"],
											self.vars["shape"]["height"])
		Shp1.Fill.ForeColor.RGB = rgb_int
		Shp1.TextFrame2.VerticalAnchor = self.vars["shape_font"]["align_v"]
		Shp1.TextFrame2.HorizontalAnchor = self.vars["shape_font"]["align_h"]

		Shp1.TextFrame2.TextRange.Font.Size = self.vars["shape_font"]["size"]
		Shp1.TextFrame2.TextRange.Font.Bold = self.vars["shape_font"]["bold"]
		Shp1.TextFrame2.TextRange.Font.Italic = self.vars["shape_font"]["italic"]
		Shp1.TextFrame2.TextRange.Font.Name = self.vars["shape_font"]["name"]

		Shp1.TextFrame2.TextRange.Font.Strikethrough = self.vars["shape_font"]["strikethrough"]
		Shp1.TextFrame2.TextRange.Font.Subscript = self.vars["shape_font"]["subscript"]
		Shp1.TextFrame2.TextRange.Font.Superscript = self.vars["shape_font"]["superscript"]
		Shp1.TextFrame2.TextRange.Font.Alpha = self.vars["shape_font"]["alpha"]
		Shp1.TextFrame2.TextRange.Font.Underline = self.vars["shape_font"]["underline"]

		rgb2_list_1d = self.color.change_scolor_to_rgb(self.vars["shape_font"]["color"])
		rgb2_int = self.color.change_rgb_to_rgbint(rgb2_list_1d)
		Shp1.TextFrame2.TextRange.Font.Fill.ForeColor.RGB = rgb2_int

		Shp1.TextFrame2.TextRange.Characters.Text = input_no
		Shp1.TextFrame2.TextRange.Characters.Font.Size = self.vars["shape_font"]["size"]

	def new_sheet(self):
		"""
		새로운 시트 추가하기

		:return:
		"""
		self.new_sheet_with_name("")

	def new_sheet_name_with_checking(self, sheet_name):
		"""
		시트하나 추가
		단, 이름을 확인해서 같은것이 있으면, 그냥 넘어간다

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:return:
		"""
		if sheet_name == "":
			pass
		else:
			all_sheet_names = self.read_sheet_name_all()
			if sheet_name in all_sheet_names:
				pass
			else:
				self.xlbook.Worksheets.Add()
				old_name = self.xlbook.ActiveSheet
				self.xlbook.Worksheets(old_name).Name = sheet_name

	def new_sheet_with_name(self, sheet_name):
		"""
		시트하나 추가
		단, 이름을 확인해서 같은것이 있으면, 그냥 넘어간다

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		"""
		if sheet_name == "":
			self.xlbook.Worksheets.Add()
		else:
			all_sheet_names = self.read_all_sheet_name()
			if sheet_name in all_sheet_names:
				self.util.messagebox_for_show("같은 시트이름이 있읍니다")
			else:
				self.xlbook.Worksheets.Add()
				old_name = self.xlbook.ActiveSheet.Name
				self.xlbook.Worksheets(old_name).Name = sheet_name

	def new_vba_module(self, vba_code, macro_name):
		"""
		텍스트로 만든 매크로 코드를 실행하는 코드이다

		:param vba_code:
		:param macro_name:
		"""
		new_vba_code = "Sub " + macro_name + "()" + vba_code + "End Sub"
		mod = self.xlbook.VBProject.VBComponents.Add(1)
		mod.CodeModule.AddFromString(new_vba_code)

	def new_workbook_with_file_path(self, filename=""):
		"""
		엑셀화일 열기

		:param filename:
		:return:
		"""
		self.new_workbook(filename)

	def new_xy_list_for_box_style(self, xyxy):
		"""
		좌표를 주면, 맨끝만 나터내는 좌표를 얻는다

		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		:return:
		"""
		temp_1 = []
		for x in [xyxy[0], xyxy[2]]:
			temp = []
			for y in range(xyxy[1], xyxy[3] + 1):
				temp.append([x, y])
			temp_1.append(temp)

		temp_2 = []
		for y in [xyxy[1], xyxy[3]]:
			temp = []
			for x in range(xyxy[0], xyxy[2] + 1):
				temp.append([x, y])
			temp_2.append(temp)

		result = [temp_1[0], temp_2[1], temp_1[1], temp_2[0]]
		return result

	def open_file(self, filename=""):
		"""
		엑셀화일 열기

		:param filename:
		:return:
		"""
		self.new_workbook(filename)

	def paste_with_condition(self, range_object, value=False, memo=False, line=False, width=False, formula=False,
							 format=False, numberformat=False, condition_format=False):
		"""
		하나의 값을 여러단어들을 기준으로 나누도록 한것
		1) 원하는 셀의 위치를 갖고온다
		2) 복사하고 붙여넣기

		:param range_object:
		:param value:
		:param memo:
		:param line:
		:param width:
		:param formula:
		:param format:
		:param numberformat:
		:param condition_format:
		"""
		if value: range_object.PasteSpecial(-4163)
		if line: range_object.PasteSpecial(7)
		if width: range_object.PasteSpecial(8)
		if formula: range_object.PasteSpecial(-4123)
		if format: range_object.PasteSpecial(-4122)
		if numberformat: range_object.PasteSpecial(12)
		if condition_format: range_object.PasteSpecial(14)
		if memo: range_object.PasteSpecial(-4144)

	def open_workbook(self, file_name):
		"""
		엑셀화일을 여는것
		:param file_name:
		:return:
		"""
		self.open_file(file_name)

	def paint_bar_by_no(self, sheet_name, xyxy, color_value=255):
		"""
		바로 만드는 것

		:param sheet_name:
		:param xyxy:
		:param color_value:
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		range_object = self.get_range_object_by_xyxy(sheet_name, xyxy)

		range_object.FormatConditions.AddDatabar
		range_object.FormatConditions(1).NegativeBarFormat.ColorType = 0  # xlDataBarColor =0
		range_object.FormatConditions(1).NegativeBarFormat.Color.Color = color_value
		range_object.FormatConditions(1).NegativeBarFormat.Color.TintAndShade = 0

	def paint_bar_in_range(self, sheet_name, xyxy, color_value=255):
		"""
		영역안에 색으로된 바를 만드는 것

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		:param color_value:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		range_object = self.get_range_object_by_xyxy(sheet_name, xyxy)

		range_object.FormatConditions.AddDatabar()
		range_object.FormatConditions(1).NegativeBarFormat.ColorType = 0  # xlDataBarColor =0
		range_object.FormatConditions(1).NegativeBarFormat.Color.Color = color_value
		range_object.FormatConditions(1).NegativeBarFormat.Color.TintAndShade = 0

	def paint_cell(self, sheet_name, xyxy, input_scolor):
		"""
		셀의 배경색을 scolor형식으로 칠하는 것

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		:param input_scolor: 색이름
		"""
		self.check_sheet_name_n_xyxy(sheet_name, xyxy)

		self.range_object.Interior.Color = self.color.change_scolor_to_rgbint(input_scolor)

	def paint_cell_by_excel56color(self, sheet_name, xy, excel_56color_no):
		"""
		선택 셀에 색깔을 넣는다

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xy: [가로번호, 세로번호]
		:param excel_56color_no:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		xyxy = self.check_address_value(xy)
		sheet_object.Cells(xyxy[0], xyxy[1]).Interior.ColorIndex = int(excel_56color_no)

	def paint_cell_by_excel_colorno(self, sheet_name, xy, excel_56color_no):
		"""
		보관용

		:param sheet_name:
		:param xy:
		:param excel_56color_no:
		:return:
		"""
		self.paint_cell_by_excel56color(sheet_name, xy, excel_56color_no)

	def paint_cell_by_rgb(self, sheet_name, xyxy, input_rgb):
		"""
		셀의 배경색을 rgb를 기준으로 칠한다

		:param sheet_name:
		:param xyxy:
		:param input_rgb:
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		range_object = self.get_range_object_by_xyxy(sheet_name, xyxy)

		range_object.Interior.Color = self.color.change_rgb_to_rgbint(input_rgb)

	def paint_cell_by_scolor(self, sheet_name, xyxy, input_scolor):
		"""
		셀의 배경색을 scolor형식의 색으로 칠하는 것

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		:param input_scolor: 색이름
		"""
		range_object = self.get_range_object_by_xyxy(sheet_name, xyxy)

		rgb_int = self.color.change_scolor_to_rgbint(input_scolor)
		range_object.Interior.Color = rgb_int

	def paint_cell_for_specific_text_in_range(self, sheet_name, xyxy, input_list, input_scolor):
		"""
		역역안에 어떤 글자가 들어가 있는 셀에 색칠하는 것

		:param sheet_name:
		:param xyxy:
		:param input_list:
		:param input_scolor:
		:return:
		"""
		self.menu_dic['paint_range_specific_text'] = {'표시여부': '필요', '그리드메뉴': ['paint', 'range', '문자가 들어있는 셀에 색칠'],
													  '실행메뉴': ['paint', 'range', 'specific_text']}
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		selection_range = x1, y1, x2, y2
		datas = list(self.read_value_in_range(sheet_name, selection_range))
		temp = []
		result = []
		min_value = []
		# print(datas)
		input_text = input_list
		for data_xx in datas:
			temp_list = []
			temp_num = 0
			for data_x in data_xx:
				if str(input_text) in str(data_x) and data_x != None:
					self.paint_color_in_range(sheet_name, [x1, y1 + temp_num, x1, y1 + temp_num],
											  input_scolor)
				temp_num = temp_num + 1
			x1 = x1 + 1

	def paint_cell_having_input_words(self, sheet_name, xyxy, input_list):
		"""
		paint_color_bywords(sheet_name="", xyxy="", input_list = "입력필요")
		선택한 영역의 각셀에 아래의 글자가 모두 들어있는 셀에 초록색으로 배는경색 칠하기
		1. 원하자료를 inputbox를 이용하여,를 사용하여 받는다
		2. split함수를 이용하여 리스트로 만들어
		3. 전부 만족한것을 for문으로 만들어 확인한후 색칠을 한다
		"""
		self.menu_dic['paint_color_cell_having_input_words'] = {'표시여부': '필요',
																'그리드메뉴': ['paint', 'color', '특정단어의 셀에 색칠하기'],
																'실행메뉴': ['paint', 'color', 'cell_having_input_words']}
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		range_object = self.get_range_object_by_xyxy(sheet_name, xyxy)
		bbb = input_list
		basic_list = []
		for one_data in bbb.split(","):
			basic_list.append(one_data.strip())
		total_no = len(basic_list)
		for y in range(y1, y2 + 1):
			for x in range(x1, x2 + 1):
				cell_value = str(self.read_value_in_cell(sheet_name, [x, y]))
				temp_int = 0
				for one_word in basic_list:
					if re.match('(.*)' + one_word + '(.*)', cell_value):
						temp_int = temp_int + 1
				if temp_int == total_no:
					self.paint_color(sheet_name, [x, y], 4)

	def paint_cell_in_range_by_same_with_input_text(self, sheet_name, xyxy, input_value, input_scolor="gra50"):
		"""
		영역안에 입력받은 글자와 같은것이 있으면 색칠하는것

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		:param input_value: 입력 text
		:param input_scolor: 색이름
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		range_object = self.get_range_object_by_xyxy(sheet_name, xyxy)

		for x in range(x1, x2 + 1):
			for y in range(y1, y2 + 1):
				value = sheet_object.Cells(x, y).Value2
				if input_value in value:
					self.paint_cell_by_scolor(sheet_name, [x, y], input_scolor)

	def paint_cell_in_range_by_specific_text(self, sheet_name, xyxy, input_value, input_scolor):
		"""
		* 현재 선택영역 : 적용가능
		영역안에 입력받은 글자와 같은것이 있으면 색칠하는것

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		:param input_value: 입력 text
		:param input_scolor: 색이름
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		range_object = self.get_range_object_by_xyxy(sheet_name, xyxy)

		for x in range(x1, x2 + 1):
			for y in range(y1, y2 + 1):
				value = sheet_object.Cells(x, y).Value2
				if input_value in value:
					self.paint_color_in_cell_by_scolor(sheet_name, [x, y], input_scolor)

	def paint_cell_with_sheet_object(self, sheet_object, xy, input_scolor):
		"""
		셀의 배경색을 칠하는 것
		속도를 빠르게 하기위하여 시트객체를 입력으로 받는다

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		:param input_scolor: 색이름
		"""
		sheet_object.Cells(xy[0], xy[1]).Interior.Color = self.color.change_scolor_to_rgbint(input_scolor)

	def paint_color_by_words(self, input_list):
		"""


		:param input_list:
		:return:
		"""
		bbb = input_list
		basic_list = []
		for one_data in bbb.split(","):
			basic_list.append(one_data.strip())
		total_no = len(basic_list)
		for x in range(self.vars["x1"], self.vars["x2"] + 1):
			for y in range(self.vars["y1"], self.vars["y2"] + 1):
				cell_value = self.vars["sheet"].Cells(x, y).Value
				temp_int = 0
				for one_word in basic_list:
					if re.match('(.*)' + one_word + '(.*)', cell_value):
						temp_int = temp_int + 1
				if temp_int == total_no:
					# pcell_dot.sheet_object.range().paint_color([x, y], 4)
					pass

	def paint_color_for_sheet_tab(self, sheet_name, input_scolor):
		"""
		시트탭의 색을 넣는것

		:param sheet_name:
		:param input_scolor:
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		sheet_object.Tab.Color = self.color.change_scolor_to_rgbint(input_scolor)

	def paint_color_in_cell_by_rgb(self, sheet_name, xyxy, input_rgb):
		"""  보관용 """
		self.paint_cell_by_rgb(sheet_name, xyxy, input_rgb)

	def paint_color_in_cell_by_scolor(self, sheet_name, xyxy, input_scolor):
		self.paint_cell_by_scolor(sheet_name, xyxy, input_scolor)

	def paint_cell_by_hsl(self, sheet_name, xyxy, input_hsl):
		rgb = self.color.change_hsl_to_rgb(input_hsl)
		self.paint_cell_by_rgb(sheet_name, xyxy, rgb)

	def paint_color_in_xyxy_by_words(self, sheet_name, xyxy, input_list):
		"""
		영역안에 원하는 단어의 리스트안에 있는것 있으면 색칠하는 것

		:param input_list:
		:return:
		"""

		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)

		for x in range(x1, x2 + 1):
			for y in range(y1, y2 + 1):
				cell_value = self.vars["sheet"].Cells(x, y).Value
				temp_int = 0
				for one_word in input_list:
					if one_word in cell_value:
						self.paint_cell(sheet_name, [x, y], "yel")
						break

	def paint_data_bar_in_range(self, sheet_name, xyxy, input_scolor="red"):
		"""
		셀의 입력숫자에 따라서 Data Bar가 타나나도록 만드는 것

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		:param input_scolor:
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		range_object = self.get_range_object_by_xyxy(sheet_name, xyxy)
		range_object.FormatConditions.Delete()  # 영역에 포함된 조건부 서식을 지우는 것

		my_bar = range_object.FormatConditions.AddDatabar()
		my_bar.BarFillType = 1  # xlDataBarSolid
		my_bar.BarBorder.Type = 0  # xlDataBarBorderSolid
		my_bar.BarColor.Color = self.color.change_scolor_to_rgbint(input_scolor)
		my_bar.BarBorder.Color.TintAndShade = 0

	def paint_different_value_between_2_same_area(self, sheet_name1, xyxy1, sheet_name2, xyxy2, color_name="yel"):
		"""
		동일한 사이즈의 2영역의 값을 비교해서, 다른것이 발견되면 색칠하는 것

		:param sheet_name1:
		:param xyxy1:
		:param sheet_name2:
		:param xyxy2:
		:param color_name:
		:return:
		"""
		list_2d_1 = self.read_value_in_range(sheet_name1, xyxy1)
		list_2d_2 = self.read_value_in_range(sheet_name2, xyxy2)

		x11, y11, x12, y12 = self.check_address_value(xyxy1)
		x21, y21, x22, y22 = self.check_address_value(xyxy2)

		for x in range(len(list_2d_1)):
			for y in range(len(list_2d_1[0])):
				if list_2d_1[x][y] == list_2d_2[x][y]:
					pass
				else:
					self.paint_cell_by_scolor(sheet_name1, [x + x11, y + y11], color_name)
					self.paint_cell_by_scolor(sheet_name2, [x + x21, y + y21], color_name)

	def paint_empty_cell_in_range(self, sheet_name="", xyxy=""):
		"""
		영역안의 빈셀의 배경색을 칠하는 것

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		:return:
		"""
		self.menu_dic['count_emptycell'] = {'표시여부': 'x', '그리드메뉴': ['count', 'emptycell', '없음'],
											'실행메뉴': ['count', 'emptycell', '']}
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		range_object = self.get_range_object_by_xyxy(sheet_name, xyxy)
		temp_result = 0

		for x in range(x1, x2 + 1):
			for y in range(y1, y2 + 1):
				cell_value = sheet_object.Cells(x, y).Value
				if cell_value == None:
					self.paint_color_in_cell(sheet_name, [x, y], 16)
					temp_result = temp_result + 1
		return temp_result

	def paint_font_in_cell_by_rgb(self, sheet_name, xyxy, rgb=""):
		"""
		** 보관용
		셀안의 폰트 색깔을 넣는 것

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		:param rgb:
		"""
		self.check_sheet_name_n_xyxy(sheet_name, xyxy)
		self.range_object.Font.Color = int(rgb[0]) + int(rgb[1]) * 256 + int(rgb[2]) * 65536

	def paint_gradation_by_color_n_position(self, input_style, input_object, input_bg_color, input_list_2d):
		"""
		여러가지색을 정하면서 색의 가장 진한 위치를 0~100사이에서 정하는 것

		:param input_style:
		:param input_object:
		:param input_bg_color:
		:param input_list_2d:
		:return:
		"""
		style_dic = {"ver": 2, "hor": 1, "cor": 5, "cen": 7, "dow": 4, "up": 3, "mix": -2, }
		input_object.Fill.ForeColor.RGB = self.color.change_scolor_to_rgbint(input_bg_color)

		obj_fill = input_object.Fill
		obj_fill.OneColorGradient(style_dic[input_style], 1, 1)

		for index, list_1d in enumerate(input_list_2d):
			rgbint = self.color.change_scolor_to_rgbint(list_1d[0])
			obj_fill.GradientStops.Insert(rgbint, list_1d[1] / 100)

	def paint_max_cell_in_range(self, sheet_name="", xyxy=""):
		"""
		한줄에서 가장 큰 값에 색칠하는 것
		읽어온 값중에서 최대값구하기
		"""

		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		range_object = self.get_range_object_by_xyxy(sheet_name, xyxy)

		all_data = self.read_range_value(sheet_name, [x1, y1, x2, y2])
		if not (x1 == x2 and y1 == y2):
			for line_no in range(len(all_data)):
				line_data = all_data[line_no]
				filteredList = list(filter(lambda x: type(x) == type(1) or type(x) == type(1.0), line_data))
				if filteredList == []:
					pass
				else:
					max_value = max(filteredList)
					x_location = x1 + line_no
					for no in range(len(line_data)):
						y_location = y1 + no
						if (line_data[no]) == max_value:
							self.draw_cell_color(sheet_name, [x_location, y_location], 16)
		else:
			print("Please re-check selection area")

	def paint_max_value_in_range_in_each_xline(self, sheet_name, xyxy, input_scolor="yel++"):
		"""
		한줄에서 가장 큰 값에 색칠하는 것
		선택한 영역안의 => 각 x라인별로 최대값에 색칠하는 것

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		range_object = self.get_range_object_by_xyxy(sheet_name, xyxy)

		all_data = self.read_value_in_range(sheet_name, [x1, y1, x2, y2])
		if not (x1 == x2 and y1 == y2):
			for line_no in range(len(all_data)):
				line_data = all_data[line_no]
				filteredList = list(filter(lambda x: type(x) == type(1) or type(x) == type(1.0), line_data))
				if filteredList == []:
					pass
				else:
					max_value = max(filteredList)
					x_location = x1 + line_no
					for no in range(len(line_data)):
						y_location = y1 + no
						if (line_data[no]) == max_value:
							self.paint_cell_by_scolor(sheet_name, [x_location, y_location], input_scolor)
		else:
			print("Please re-check selection area")

	def paint_max_value_in_range_in_each_yline(self, sheet_name="", xyxy=""):
		"""
		가로줄이아닌 세로줄에서 제일 큰값에 색칠하는 것

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		:return:
		"""
		self.menu_dic['paint_maxvalue_each_yline'] = {'표시여부': '필요',
													  '그리드메뉴': ['paint', 'maxvalue', '영역중 각 x열의 최대값에 색칠하기'],
													  '실행메뉴': ['paint', 'maxvalue', 'each_yline']}
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		range_object = self.get_range_object_by_xyxy(sheet_name, xyxy)
		all_data = self.read_value(sheet_name, [y1, x1, y2, x2])

		if not (y1 == y2 and x1 == x2):
			for line_no in range(len(all_data)):
				line_data = all_data[line_no]
				filteredList = list(filter(lambda x: type(x) == type(1) or type(x) == type(1.0), line_data))
				if filteredList == []:
					pass
				else:
					max_value = max(filteredList)
					y_location = y1 + line_no
					for no in range(len(line_data)):
						x_location = x1 + no
						if (line_data[no]) == max_value:
							self.paint_color(sheet_name, [y_location, x_location], 16)
		else:
			print("Please re-check selection area")

	def paint_min_value_in_range_in_each_xline(self, sheet_name, xyxy, input_scolor="red++"):
		"""
		선택한 영역안의 => 각 x라인별로 최소값에 색칠하는 것

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		range_object = self.get_range_object_by_xyxy(sheet_name, xyxy)

		all_data = self.read_value_in_range(sheet_name, [x1, y1, x2, y2])
		if not (x1 == x2 and y1 == y2):
			for line_no in range(len(all_data)):
				line_data = all_data[line_no]
				filteredList = list(filter(lambda x: type(x) == type(1) or type(x) == type(1.0), line_data))
				if filteredList == []:
					pass
				else:
					max_value = min(filteredList)
					x_location = x1 + line_no
					for no in range(len(line_data)):
						y_location = y1 + no
						if (line_data[no]) == max_value:
							self.paint_cell_by_scolor(sheet_name, [x_location, y_location], input_scolor)
		else:
			print("Please re-check selection area")

	def paint_range(self, sheet_name, xyxy, input_scolor="gra"):
		"""
		선택 영역에 색깔을 넣는다

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		:param input_scolor: 색이름
		"""
		self.check_sheet_name_n_xyxy(sheet_name, xyxy)

		range_object = self.sheet_object.Range(self.r1c1)

		rgb_int = self.color.change_scolor_to_rgbint(input_scolor)
		self.range_object.Interior.Color = rgb_int

	def paint_range_by_scolor(self, sheet_name, xyxy, input_scolor):
		"""
		선택 영역에 색을 칠한다

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:param input_scolor: 색이름
		:return:
		"""
		range_object = self.get_range_object_by_xyxy(sheet_name, xyxy)
		range_object.Interior.Color = self.color.change_scolor_to_rgbint(input_scolor)

	def paint_range_by_words(self, sheet_name="", xyxy=""):
		"""
		선택한 영역의 각셀에 아래의 글자가 모두 들어있는 셀에 초록색으로 배는경색 칠하기
		1. 원하자료를 inputbox를 이용하여,를 사용하여 받는다
		2. split함수를 이용하여 리스트로 만들어
		3. 전부 만족한것을 for문으로 만들어 확인한후 색칠을 한다
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		range_object = self.get_range_object_by_xyxy(sheet_name, xyxy)

		bbb = self.read_messagebox_value("Please input text : in, to, his, with")
		basic_list = []
		for one_data in bbb.split(","):
			basic_list.append(one_data.strip())
		total_no = len(basic_list)
		for x in range(x1, x2 + 1):
			for y in range(y1, y2 + 1):
				cell_value = str(self.read_cell_value(sheet_name, [x, y]))
				temp_int = 0
				for one_word in basic_list:
					if re.match('(.*)' + one_word + '(.*)', cell_value):
						temp_int = temp_int + 1
				if temp_int == total_no:
					self.draw_cell_color(sheet_name, [x, y], 4)

	def paint_range_my_style(self, sheet_name="", xyxy=""):
		"""
		*입력값없이 사용가능*
		paint_range_line_form1(sheet_name, xyxy)
		내가 자주사용하는 형태의 라인
		[선의위치, 라인스타일, 굵기, 색깔]
		입력예 : [7,1,2,1], ["left","-","t0","bla"]
		선의위치 (5-대각선 오른쪽, 6-왼쪽대각선, 7:왼쪽, 8;위쪽, 9:아래쪽, 10:오른쪽, 11:안쪽세로, 12:안쪽가로)
		라인스타일 (1-실선, 2-점선, 3-가는점선, 6-굵은실선,
		굵기 (0-이중, 1-얇게, 2-굵게)
		색깔 (0-검정, 1-검정, 3-빨강),
		"""
		self.menu_dic['paint_range_mystyle'] = {"표시여부": '필요', "그리드메뉴": ['색칠하기', '선택영역', 'mystyle'],
												"실행메뉴": ['draw', 'range', 'mystyle']}
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		range_object = self.get_range_object_by_xyxy(sheet_name, xyxy)

		line_list_head = [
			["left", "basic", "t-2", "red"],
			["top", "basic", "t-2", "black"],
			["right", "basic", "t-2", "red"],
			["bottom", "basic", "t-2", "black"],
			["inside-h", "basic", "t-2", "black"],
			["inside-v", "basic", "t-2", "black"],
		]
		line_list_body = [
			["left", "basic", "basic", "black"],
			["top", "basic", "basic", "black"],
			["right", "basic", "basic", "black"],
			["bottom", "basic", "basic", "black"],
			["inside-h", "basic", "basic", "black"],
			["inside-v", "basic", "basic", "black"],
		]
		line_list_tail = [
			["left", "basic", "t0", "black"],
			["top", "basic", "t0", "red"],
			["right", "basic", "t0", "red"],
			["bottom", "basic", "basic", "red"],
			["inside-h", "basic", "basic", "red"],
			["inside-v", "basic", "basic", "red"],
		]
		# print(line_list_head)
		range_head = [x1, y1, x1, y2]
		range_body = [x1 + 1, y1, x2 - 1, y2]
		range_tail = [x2, y1, x2, y2]
		for one in line_list_head:
			self.paint_range_line("", range_head, one)
		for one in line_list_body:
			self.paint_range_line("", range_body, one)
		for one in line_list_tail:
			self.paint_range_line("", range_tail, one)

	def paint_same_value_in_range_as_rgb(self, sheet_name="", xyxy=""):
		"""
		*입력값없이 사용가능*
		선택한 영역에서 2번이상 반복된것만 색칠하기
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		range_object = self.get_range_object_by_xyxy(sheet_name, xyxy)

		set_a = set([])
		for x in range(x1, x2 + 1):
			for y in range(y1, y2 + 1):
				value = self.read_cell_value(sheet_name, [x, y])
				if value == "" or value == None:
					pass
				else:
					len_old = len(set_a)
					set_a.add(value)
					len_new = len(set_a)
					if len_old == len_new:
						self.draw_cell_color(sheet_name, [x, y], "red++")

	def paint_same_value_in_range_by_excel56(self, sheet_name, xyxy, excel_56color_no=4):
		"""
		선택영역 => 같은 값에 색칠

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		:param excel_56color_no: 엑셀의 56가시 색번호중 하나
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		range_object = self.get_range_object_by_xyxy(sheet_name, xyxy)

		set_a = set([])
		for x in range(x1, x2 + 1):
			for y in range(y1, y2 + 1):
				value = str(sheet_object.Cells(x, y).Value2)
				if value == "" or value == None:
					pass
				else:
					len_old = len(set_a)
					set_a.add(value)
					len_new = len(set_a)
					if len_old == len_new:
						self.paint_color_in_cell_by_excel_colorno(sheet_name, [x, y], excel_56color_no)

	def paint_same_value_in_range_by_excel_colorno(self, sheet_name, xyxy, excel_56color_no=4):
		"""
		선택영역안의 => 같은 값을 색칠하는 것

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		:param excel_56color_no: 엑셀의 56가시 색번호중 하나
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		range_object = self.get_range_object_by_xyxy(sheet_name, xyxy)

		set_a = set([])
		for x in range(x1, x2 + 1):
			for y in range(y1, y2 + 1):
				value = str(sheet_object.Cells(x, y).Value2)
				if value == "" or value == None:
					pass
				else:
					len_old = len(set_a)
					set_a.add(value)
					len_new = len(set_a)
					if len_old == len_new:
						self.read_address_for_selection(sheet_name, [x, y], excel_56color_no)

	def paint_same_value_in_range_by_scolor(self, sheet_name, xyxy, input_scolor="gray"):
		"""
		영역안의 같은 값에 scolor색으로 색칠하는것

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		:param input_scolor:
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		range_object = self.get_range_object_by_xyxy(sheet_name, xyxy)

		set_a = set([])
		for x in range(x1, x2 + 1):
			for y in range(y1, y2 + 1):
				value = self.read_value_in_cell(sheet_name, [x, y])
				if value == "" or value == None:
					pass
				else:
					len_old = len(set_a)
					set_a.add(value)
					len_new = len(set_a)
					if len_old == len_new:
						self.paint_range_by_scolor(sheet_name, [x, y], "red++")

	def paint_same_value_over_n_times(self, sheet_name, xyxy, n_times):
		"""
		선택한 영역에서 n번이상 반복된 것만 색칠하기
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		range_object = self.get_range_object_by_xyxy(sheet_name, xyxy)

		py_dic = {}
		for x in range(x1, x2 + 1):
			for y in range(y1, y2 + 1):
				one_value = self.read_value_in_cell(sheet_name, [x, y])
				if one_value != "" and one_value != None:
					if not py_dic[one_value]:
						py_dic[one_value] = 1
					else:
						py_dic[one_value] = py_dic[one_value] + 1

					if py_dic[one_value] >= n_times:
						self.paint_cell_by_scolor(sheet_name, [x, y], "pin")

	def paint_search_range_by_regex(self, sheet_name, xyxy, xyre, scolor):
		"""
		엑셀의 영역에서 값을 찾으면, 셀에 색칠하기

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		:param xyre:
		:param scolor:
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		range_object = self.get_range_object_by_xyxy(sheet_name, xyxy)

		list_2d = range_object.Formula
		for ix, list_1d in enumerate(list_2d):
			for iy, value in enumerate(list_1d):
				if not value or str(value).startswith("="):
					pass
				else:
					temp = self.xyre.search_all_by_jf_sql(xyre, value)
				if temp:
					self.paint_cell_by_scolor(sheet_name, [x1 + ix, y1 + iy], scolor)

	def paint_selection_by_scolor(self, input_scolor):
		"""
		paint_color(sheet_name, xyxy, input_value)
		선택 영역에 색깔을 넣는다

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:param input_scolor: 색이름
		:return:
		"""
		[sheet_object, range_object, x1, y1, x2, y2] = self.check_basic_data("", "")

		range_object.Interior.Color = self.color.change_scolor_to_rgbint(input_scolor)

	def paint_sheet_tab_by_scolor(self, sheet_name, input_scolor="gra50"):
		"""
		시트탭의 색을 넣는것

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param input_scolor: 색이름
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		sheet_object.Tab.Color = self.color.change_scolor_to_rgbint(input_scolor)

	def paint_space_cell_in_range_by_scolor(self, sheet_name, xyxy, input_scolor="gra50"):
		"""
		영역안의 셀의 배경색을 scolor색으로 정하는 것

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		:param input_scolor:
		:return:
		"""
		self.paint_spacecell_in_range(sheet_name, xyxy, input_scolor)

	def paint_text_in_range_by_scolor(self, sheet_name, xyxy, input_scolor):
		"""
		영역안의 글자들의 색을 scolor색으로 정하는 것

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		:param input_scolor:
		:return:
		"""
		self.set_font_color_in_range(sheet_name, xyxy, input_scolor)

	def paste_range(self, sheet_name="", xyxy=""):
		"""
		영역에 붙여넣기 하는것

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		range_object = self.get_range_object_by_xyxy(sheet_name, xyxy)

		sheet_object.Cells(x1, y1).Select()
		sheet_object.Paste()

	def pcell_util_change_encoding_type_001_success(self, ):
		"""
		기본적인 시스템에서의 인코딩을 읽어온다

		:return:
		"""
		system_in_basic_incoding = sys.stdin.encoding
		system_out_basic_incoding = sys.stdout.encoding
		print("시스템의 기본적인 입력시의 인코딩 ====> ", system_in_basic_incoding)
		print("시스템의 기본적인 출력시의 인코딩 ====> ", system_out_basic_incoding)

	def pick_unique_value_in_range(self, sheet_name="", xyxy=""):
		"""
		선택한 자료중에서 고유한 자료만을 골라내는 것이다
		1. 관련 자료를 읽어온다
		2. 자료중에서 고유한것을 찾아낸다
		3. 선택영역에 다시 쓴다
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		range_object = self.get_range_object_by_xyxy(sheet_name, xyxy)

		temp_datas = self.read_value_in_range("", xyxy)
		temp_result = []
		for one_list_data in temp_datas:
			for one_data in one_list_data:
				if one_data in temp_result or type(one_data) == type(None):
					pass
				else:
					temp_result.append(one_data)
		self.delete_value_in_range("", xyxy)
		for num in range(len(temp_result)):
			mox, namuji = divmod(num, x2 - x1 + 1)
			sheet_object.Cells(x1 + namuji, y1 + mox).Value = temp_result[num]

	def pick_ylines_at_list_2d(self, input_list_2d, list_1d):
		"""
		2차원자료중에서 원하는 가로열들의 자료만 갖고오는 것

		:param input_list_2d:
		:param list_1d:
		:return:
		"""
		result = []
		for one_list in input_list_2d:
			temp = []
			for index in list_1d:
				temp.append(one_list[index])
			result.append(temp)
		return result

	def ppt_make_ppt_table_from_xl_data(self, ):
		"""
		엑셀의 테이블 자료가 잘 복사가 않되는것 같아서, 아예 하나를 만들어 보았다
		엑셀의 선택한 영역의 테이블 자료를 자동으로 파워포인트의 테이블 형식으로 만드는 것이다
		"""

		activesheet_name = self.read_activesheet_name()
		[x1, y1, x2, y2] = self.read_select_address()
		# print([x1, y1, x2, y2])

		Application = win32com.client.Dispatch("Powerpoint.Application")
		Application.Visible = True
		active_ppt = Application.Activepresentation
		slide_no = active_ppt.Slides.Count + 1

		new_slide = active_ppt.Slides.Add(slide_no, 12)
		new_table = active_ppt.Slides(slide_no).Shapes.AddTable(x2 - x1 + 1, y2 - y1 + 1)
		shape_no = active_ppt.Slides(slide_no).Shapes.Count

		for y in range(y1, y2 + 1):
			for x in range(x1, x2 + 1):
				value = self.read_cell_value(activesheet_name, [x, y])
				active_ppt.Slides(slide_no).Shapes(shape_no).Table.Cell(x - x1 + 1,
																		y - y1 + 1).Shape.TextFrame.TextRange.Text = value

	def preview(self, sheet_name):
		"""
		미리보기기능입니다
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		sheet_object.PrintPreview()

	def print_as_pdf(self, sheet_name, area, file_name):
		"""
		sheet_object.PageSetup.Zoom = False
		sheet_object.PageSetup.FitToPagesTall = 1
		sheet_object.PageSetup.FitToPagesWide = 1
		sheet_object.PageSetup.LeftMargin = 25
		sheet_object.PageSetup.RightMargin = 25
		sheet_object.PageSetup.TopMargin = 50
		sheet_object.PageSetup.BottomMargin = 50
		sheet_object.ExportAsFixedFormat(0, file_name)

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param area:
		:param file_name:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		sheet_object.ExportAsFixedFormat(0, file_name)

	def print_label_style(self, sheet_name, input_list_2d, line_list, start_xy, size_xy, y_line, position):
		"""
		라벨프린트식으로 만드는 것

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param input_list_2d:
		:param line_list:
		:param start_xy:
		:param size_xy:
		:param y_line:
		:param position:
		"""
		input_list_2d = self.change_xylist_to_list(input_list_2d)
		line_list = self.change_xylist_to_list(line_list)

		changed_list_2d = self.pick_ylines_at_list_2d(input_list_2d, line_list)
		for index, list_1d in enumerate(changed_list_2d):
			new_start_x, new_start_y = self.util.new_xy(index, start_xy, size_xy, y_line)
			for index_2, one_value in enumerate(list_1d):
				self.write_value_in_cell(sheet_name,
										 [new_start_x + position[index_2][0], new_start_y + position[index_2][1]],
										 list_1d[index_2])

	def print_letter_cover(self, ):
		"""
		봉투인쇄
		"""
		# 기본적인 자료 설정
		data_from = [["sheet1", [1, 2]], ["sheet1", [1, 4]], ["sheet1", [1, 6]], ["sheet1", [1, 8]]]
		data_to = [["sheet2", [1, 2]], ["sheet2", [2, 2]], ["sheet2", [3, 2]], ["sheet2", [2, 3]]]
		no_start = 1
		no_end = 200
		step = 5
		# 실행되는 구간
		for no in range(no_start, no_end):
			for one in range(len(data_from)):
				value = self.read_cell_value(data_from[one][0], data_from[one][1])
				self.write_cell_value(data_to[one][0], [data_to[one][1][0] + (step * no), data_to[one][1][1]], value)

	def print_letter_cover_01(self, ):
		"""
		봉투인쇄
		"""

		# 기본적인 자료 설정
		data_from = [["sheet1", [1, 2]], ["sheet1", [1, 4]], ["sheet1", [1, 6]], ["sheet1", [1, 8]]]
		data_to = [["sheet2", [1, 2]], ["sheet2", [2, 2]], ["sheet2", [3, 2]], ["sheet2", [2, 3]]]

		no_start = 1
		no_end = 200
		step = 5

		# 실행되는 구간
		for no in range(no_start, no_end):
			for one in range(len(data_from)):
				value = self.read_cell_value(data_from[one][0], data_from[one][1])
				self.write_cell_value(data_to[one][0], [data_to[one][1][0] + (step * no), data_to[one][1][1]], value)

	def print_page(self, sheet_name, **var_dic):
		"""

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param var_dic:
		"""
		self.set_print_page(sheet_name, **var_dic)

	def print_preview(self, sheet_name):
		"""
		인쇄 미리보기 기능

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		sheet_object.PrintPreview()

	def print_preview_sheet(self, sheet_name):
		"""
		미리보기기능입니다
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		sheet_object.PrintPreview()

	def quit(self):
		"""
		엑셀 프로그램을 끄는것
		"""
		self.xlapp.Quit()

	def read_activesheet_name(self):
		"""
		현재 활성화된 시트의 이름
		"""
		sheet_name = self.xlapp.ActiveSheet.Name
		return sheet_name

	def read_address(self):
		"""
		현재 영역의 주소값을 읽어온다
		"""
		self.menu_dic['read_address'] = {'표시여부': 'x', '그리드메뉴': ['read', 'address', '없음'],
										 '실행메뉴': ['read', 'address', '']}
		temp_address = self.xlApp.Selection.Address
		result = self.check_address(temp_address)
		return result


	def read_address_for_activecell(self):
		"""
		현재 활성화된 셀의 주소를 돌려준다
		"""
		result = self.check_address_value(self.xlapp.ActiveCell.Address)
		return result

	def read_address_for_cell(self):
		""" ** 예전자료를 위해 남겨둠 ** """
		result = self.read_activecell_address()
		return result

	def read_address_for_currentregion(self, sheet_name, xy=""):
		"""
		이것은 현재의 셀에서 공백과 공백열로 둘러싸인 활성셀영역을 돌려준다

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xy: [가로번호, 세로번호]
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		range_object = sheet_object.Cells(xy[0], xy[1])
		result = self.check_address_value(range_object.CurrentRegion.Address)
		return result

	def read_address_for_range(self):
		"""
		현재 선택영역을 xyxy형태의 주소로 돌려주는 것
		:return:
		"""
		temp_address = self.xlApp.Selection.Address
		result = self.check_address_value(temp_address)
		return result

	def read_address_for_range_name(self, sheet_name, range_name):
		"""
		rangename의 주소를 돌려주는것

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param range_name: 영역이름
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		temp = sheet_object.Range(range_name).Address

		result = self.check_address_value(temp)
		return result

	def read_address_for_selection(self):
		"""
		현재선택된 영역의 주소값을 돌려준다
		"""
		result = ""
		temp_address = self.xlapp.Selection.Address
		temp_list = temp_address.split(",")
		if len(temp_list) == 1:
			result = self.check_address_value(temp_address)
		if len(temp_list) > 1:
			result = []
			for one_address in temp_list:
				result.append(self.check_address_value(one_address))
		return result

	def read_address_for_usedrange(self, sheet_name):
		"""
		사용자영역을 돌려주는것

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		result = self.check_address_value(sheet_object.UsedRange.Address)
		# result = [temp[1], temp[0], temp[3], temp[2]]
		return result

	def read_address_in_activecell(self):
		"""
		예전 자료를 위해서 남겨 둠
		"""
		result = self.read_address_for_activecell()
		return result

	def read_address_in_selection(self):
		"""
		보관용
		"""
		result = self.read_address_for_selection()
		return result

	def read_all_data_for_cell(self, sheet_name, yx=[7, 7]):
		"""
		read_all_data_of_one_cell(self, sheet_name, xy=[7,7])
		한개의 셀에 대한 중요한 모든 자료를 다 읽어오기위한 것이다
		목적은 pcell에 엑셀의 모든 정보를 옮길수있는 기준을 만들기 위한 것이다
		1 : Hairline, -4138: Medium, 4 : Thick, 2 : Thin
		7 : left, 8:top, 9:bottom, 10:right, 11: x1, 12:x2
		"""
		basic_cell = basic_data.basic_cell_class()
		sheet_object = self.check_sheet_name(sheet_name)
		one_cell = sheet_object.Cells(yx[0], yx[1])
		result = basic_cell.values
		y = result["y"] = yx[0]
		x = result["x"] = yx[1]
		result["value"] = one_cell.Value
		result["value2"] = one_cell.Value2
		result["formula"] = one_cell.Formula
		result["formular1c1"] = one_cell.FormulaR1C1
		result["text"] = one_cell.Text
		if result["value"] != "" and result["value"] != None:
			# 값이 없으면 font에 대한 것을 읽지 않는다
			result["font_dic"]["background"] = one_cell.Font.Background
			result["font_dic"]["bold"] = one_cell.Font.Bold
			result["font_dic"]["color"] = one_cell.Font.Color
			result["font_dic"]["colorindex"] = one_cell.Font.ColorIndex
			# result["font_dic"]["creator"] = one_cell.Font.Creator
			result["font_dic"]["style"] = one_cell.Font.FontStyle
			result["font_dic"]["italic"] = one_cell.Font.Italic
			result["font_dic"]["name"] = one_cell.Font.Name
			result["font_dic"]["size"] = one_cell.Font.Size
			result["font_dic"]["strikethrough"] = one_cell.Font.Strikethrough
			result["font_dic"]["subscript"] = one_cell.Font.Subscript
			result["font_dic"]["superscript"] = one_cell.Font.Superscript
			# result["font_dic"]["themecolor"] = one_cell.Font.ThemeColor
			# result["font_dic"]["themefont"] = one_cell.Font.ThemeFont
			# result["font_dic"]["tintandshade"] = one_cell.Font.TintAndShade
			result["font_dic"]["underline"] = one_cell.Font.Underline
		try:
			result["memo"] = one_cell.Comment.Text()
		except:
			result["memo"] = ""
		result["background_color"] = one_cell.Interior.Color
		result["background_colorindex"] = one_cell.Interior.ColorIndex
		result["numberformat"] = one_cell.NumberFormat
		if one_cell.Borders.LineStyle != -4142:
			if one_cell.Borders(7).LineStyle != -4142:
				# linestyle이 없으면 라인이 없는것으로 생각하고 나머지를 확인하지 않으면서 시간을 줄이는 것이다
				result["line_top_dic"]["style"] = one_cell.Borders(7).LineStyle
				result["line_top_dic"]["color"] = one_cell.Borders(7).Color
				result["line_top_dic"]["colorindex"] = one_cell.Borders(7).ColorIndex
				result["line_top_dic"]["thick"] = one_cell.Borders(7).Weight
				result["line_top_dic"]["tintandshade"] = one_cell.Borders(7).TintAndShade
			if one_cell.Borders(8).LineStyle != -4142:
				result["line_bottom_dic"]["style"] = one_cell.Borders(8).LineStyle
				result["line_bottom_dic"]["color"] = one_cell.Borders(8).Color
				result["line_bottom_dic"]["colorindex"] = one_cell.Borders(8).ColorIndex
				result["line_bottom_dic"]["thick"] = one_cell.Borders(8).Weight
				result["line_bottom_dic"]["tintandshade"] = one_cell.Borders(8).TintAndShade
			if one_cell.Borders(9).LineStyle != -4142:
				result["line_left_dic"]["style"] = one_cell.Borders(9).LineStyle
				result["line_left_dic"]["color"] = one_cell.Borders(9).Color
				result["line_left_dic"]["colorindex"] = one_cell.Borders(9).ColorIndex
				result["line_left_dic"]["thick"] = one_cell.Borders(9).Weight
				result["line_left_dic"]["tintandshade"] = one_cell.Borders(9).TintAndShade
			if one_cell.Borders(10).LineStyle != -4142:
				result["line_right_dic"]["style"] = one_cell.Borders(10).LineStyle
				result["line_right_dic"]["color"] = one_cell.Borders(10).Color
				result["line_right_dic"]["colorindex"] = one_cell.Borders(10).ColorIndex
				result["line_right_dic"]["thick"] = one_cell.Borders(10).Weight
				result["line_right_dic"]["tintandshade"] = one_cell.Borders(10).TintAndShade
			if one_cell.Borders(11).LineStyle != -4142:
				result["line_x1_dic"]["style"] = one_cell.Borders(11).LineStyle
				result["line_x1_dic"]["color"] = one_cell.Borders(11).Color
				result["line_x1_dic"]["colorindex"] = one_cell.Borders(11).ColorIndex
				result["line_x1_dic"]["thick"] = one_cell.Borders(11).Weight
				result["line_x1_dic"]["tintandshade"] = one_cell.Borders(11).TintAndShade
			if one_cell.Borders(12).LineStyle != -4142:
				result["line_x2_dic"]["style"] = one_cell.Borders(12).LineStyle
				result["line_x2_dic"]["color"] = one_cell.Borders(12).Color
				result["line_x2_dic"]["colorindex"] = one_cell.Borders(12).ColorIndex
				result["line_x2_dic"]["thick"] = one_cell.Borders(12).Weight
				result["line_x2_dic"]["tintandshade"] = one_cell.Borders(12).TintAndShade
		return result

	def read_all_filename_for_opened_workbook(self):
		"""
		모든 열려있는 엑셀화일의 이름을 갖고옵니다

		"""
		result = []
		for one in self.xlapp.Workbooks:
			result.append(one.Name)
		return result

	def read_all_filename_in_folder(self, directory):
		"""
		폴더 안의 화일을 읽어오는것

		:param directory:
		:return:
		"""
		result = []
		filenames = os.listdir(directory)
		for filename in filenames:
			full_filename = os.path.join(directory, filename)
			result.append(filename)
		return result

	def read_all_filename_in_folder_by_extension_name(self, directory="./", filter="pickle"):
		"""
		pickle로 만든 자료를 저장하는것
		변경함,여러 확장자도 사용할수있도록 ["txt", "png"]
		youtil에 있음
		"""
		result = []
		all_files = os.listdir(directory)
		if filter == "+" or filter == "":
			result = all_files
		else:
			for x in all_files:
				if type(filter) == type([]):
					for one in filter:
						if x.endswith("." + one):
							result.append(x)
				elif x.endswith("." + filter):
					result.append(x)
		return result

	def read_all_filename_in_folder_filter_by_extension_name(self, directory="./", filter="pickle"):
		"""
		pickle로 만든 자료를 저장하는것
		변경함,여러 확장자도 사용할수있도록 ["txt", "png"]
		youtil에 있음

		:param directory:
		:param filter:
		:return:
		"""
		result = []
		all_files = os.listdir(directory)
		if filter == "+" or filter == "":
			result = all_files
		else:
			for x in all_files:
				if type(filter) == type([]):
					for one in filter:
						if x.endswith("." + one):
							result.append(x)
				elif x.endswith("." + filter):
					result.append(x)
		return result

	def read_all_formula_in_range(self, sheet_name="", xyxy=""):
		"""
		영역안의 모든 수식을 갖고온다

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		range_object = self.get_range_object_by_xyxy(sheet_name, xyxy)
		return range_object.Formula

	def read_all_information_for_shape(self, sheet_name, shape_no):
		"""
		한 도형에 대한 기본적인 정보들
		2024-01-11 : 조금 변경함
		"""
		result = {}
		sheet_object = self.check_sheet_name(sheet_name)
		if type(shape_no) == type(1):
			shape_no = self.check_shape_name(sheet_name, shape_no)
		shape_object = sheet_object.Shapes(shape_no)
		result["title"] = shape_object.Title
		result["text"] = shape_object.TextFrame2.TextRange.Characters.Text
		result["xy"] = [shape_object.TopLeftCell.Row, shape_object.TopLeftCell.Column]
		result["no"] = shape_no
		result["name"] = shape_object.Name
		result["rotation"] = shape_object.Rotation
		result["left"] = shape_object.Left
		result["top"] = shape_object.Top
		result["width"] = shape_object.Width
		result["height"] = shape_object.Height
		result["pxywh"] = [shape_object.Left, shape_object.Top, shape_object.Width, shape_object.Height]
		return result

	def read_all_property_in_cell(self, sheet_name, xy=[7, 7]):
		"""
		셀의 모든 속성을 돌려주는것

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xy: [가로번호, 세로번호]
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		one_cell = sheet_object.Cells(xy[0], xy[1])
		result = {}
		result["y"] = xy[0]
		result["x"] = xy[1]
		result["value"] = one_cell.Value
		result["value2"] = one_cell.Value2
		result["formula"] = one_cell.Formula
		result["formular1c1"] = one_cell.FormulaR1C1
		result["text"] = one_cell.Text
		result["font_background"] = one_cell.Font.Background
		result["font_bold"] = one_cell.Font.Bold
		result["font_color"] = one_cell.Font.Color
		result["font_colorindex"] = one_cell.Font.ColorIndex
		result["font_creator"] = one_cell.Font.Creator
		result["font_style"] = one_cell.Font.FontStyle
		result["font_italic"] = one_cell.Font.Italic
		result["font_name"] = one_cell.Font.Name
		result["font_size"] = one_cell.Font.Size
		result["font_strikethrough"] = one_cell.Font.Strikethrough
		result["font_subscript"] = one_cell.Font.Subscript
		result["font_superscript"] = one_cell.Font.Superscript
		try:
			result["font_themecolor"] = one_cell.Font.ThemeColor
			result["font_themefont"] = one_cell.Font.ThemeFont
			result["font_tintandshade"] = one_cell.Font.TintAndShade
			result["font_underline"] = one_cell.Font.Underline
			result["memo"] = one_cell.Comment.Text()
		except:
			result["memo"] = ""
		result["background_color"] = one_cell.Interior.Color
		result["background_colorindex"] = one_cell.Interior.ColorIndex
		result["numberformat"] = one_cell.NumberFormat
		# linestyle이 없으면 라인이 없는것으로 생각하고 나머지를 확인하지 않으면서 시간을 줄이는 것이다
		result["line_top_style"] = one_cell.Borders(7).LineStyle
		result["line_top_color"] = one_cell.Borders(7).Color
		result["line_top_colorindex"] = one_cell.Borders(7).ColorIndex
		result["line_top_thick"] = one_cell.Borders(7).Weight
		result["line_top_tintandshade"] = one_cell.Borders(7).TintAndShade
		result["line_bottom_style"] = one_cell.Borders(8).LineStyle
		result["line_bottom_color"] = one_cell.Borders(8).Color
		result["line_bottom_colorindex"] = one_cell.Borders(8).ColorIndex
		result["line_bottom_thick"] = one_cell.Borders(8).Weight
		result["line_bottom_tintandshade"] = one_cell.Borders(8).TintAndShade
		result["line_left_style"] = one_cell.Borders(9).LineStyle
		result["line_left_color"] = one_cell.Borders(9).Color
		result["line_left_colorindex"] = one_cell.Borders(9).ColorIndex
		result["line_left_thick"] = one_cell.Borders(9).Weight
		result["line_left_tintandshade"] = one_cell.Borders(9).TintAndShade
		result["line_right_style"] = one_cell.Borders(10).LineStyle
		result["line_right_color"] = one_cell.Borders(10).Color
		result["line_right_colorindex"] = one_cell.Borders(10).ColorIndex
		result["line_right_thick"] = one_cell.Borders(10).Weight
		result["line_right_tintandshade"] = one_cell.Borders(10).TintAndShade
		result["line_x1_style"] = one_cell.Borders(11).LineStyle
		result["line_x1_color"] = one_cell.Borders(11).Color
		result["line_x1_colorindex"] = one_cell.Borders(11).ColorIndex
		result["line_x1_thick"] = one_cell.Borders(11).Weight
		result["line_x1_tintandshade"] = one_cell.Borders(11).TintAndShade
		result["line_x2_style"] = one_cell.Borders(12).LineStyle
		result["line_x2_color"] = one_cell.Borders(12).Color
		result["line_x2_colorindex"] = one_cell.Borders(12).ColorIndex
		result["line_x2_thick"] = one_cell.Borders(12).Weight
		result["line_x2_tintandshade"] = one_cell.Borders(12).TintAndShade
		return result

	def read_all_property_in_cell_except_none(self, sheet_name, xy=[7, 7]):
		"""
		셀의 모든 속성을 돌려주는것

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xy: [가로번호, 세로번호]
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		one_cell = sheet_object.Cells(xy[0], xy[1])
		result = {}
		result["y"] = xy[0]
		result["x"] = xy[1]
		result["value"] = one_cell.Value
		result["value2"] = one_cell.Value2
		result["formula"] = one_cell.Formula
		result["formular1c1"] = one_cell.FormulaR1C1
		result["text"] = one_cell.Text
		if result["value"] != "" and result["value"] != None:
			# 값이 없으면 font에 대한 것을 읽지 않는다
			result["font_background"] = one_cell.Font.Background
			result["font_bold"] = one_cell.Font.Bold
			result["font_color"] = one_cell.Font.Color
			result["font_colorindex"] = one_cell.Font.ColorIndex
			result["font_creator"] = one_cell.Font.Creator
			result["font_style"] = one_cell.Font.FontStyle
			result["font_italic"] = one_cell.Font.Italic
			result["font_name"] = one_cell.Font.Name
			result["font_size"] = one_cell.Font.Size
			result["font_strikethrough"] = one_cell.Font.Strikethrough
			result["font_subscript"] = one_cell.Font.Subscript
			result["font_superscript"] = one_cell.Font.Superscript
			result["font_themecolor"] = one_cell.Font.ThemeColor
			result["font_themefont"] = one_cell.Font.ThemeFont
			result["font_tintandshade"] = one_cell.Font.TintAndShade
			result["font_underline"] = one_cell.Font.Underline
		try:
			result["memo"] = one_cell.Comment.Text()
		except:
			result["memo"] = ""
		result["background_color"] = one_cell.Interior.Color
		result["background_colorindex"] = one_cell.Interior.ColorIndex
		result["numberformat"] = one_cell.NumberFormat
		if one_cell.Borders.LineStyle != -4142:
			if one_cell.Borders(7).LineStyle != -4142:
				# linestyle이 없으면 라인이 없는것으로 생각하고 나머지를 확인하지 않으면서 시간을 줄이는 것이다
				result["line_top_style"] = one_cell.Borders(7).LineStyle
				result["line_top_color"] = one_cell.Borders(7).Color
				result["line_top_colorindex"] = one_cell.Borders(7).ColorIndex
				result["line_top_thick"] = one_cell.Borders(7).Weight
				result["line_top_tintandshade"] = one_cell.Borders(7).TintAndShade
			if one_cell.Borders(8).LineStyle != -4142:
				result["line_bottom_style"] = one_cell.Borders(8).LineStyle
				result["line_bottom_color"] = one_cell.Borders(8).Color
				result["line_bottom_colorindex"] = one_cell.Borders(8).ColorIndex
				result["line_bottom_thick"] = one_cell.Borders(8).Weight
				result["line_bottom_tintandshade"] = one_cell.Borders(8).TintAndShade
			if one_cell.Borders(9).LineStyle != -4142:
				result["line_left_style"] = one_cell.Borders(9).LineStyle
				result["line_left_color"] = one_cell.Borders(9).Color
				result["line_left_colorindex"] = one_cell.Borders(9).ColorIndex
				result["line_left_thick"] = one_cell.Borders(9).Weight
				result["line_left_tintandshade"] = one_cell.Borders(9).TintAndShade
			if one_cell.Borders(10).LineStyle != -4142:
				result["line_right_style"] = one_cell.Borders(10).LineStyle
				result["line_right_color"] = one_cell.Borders(10).Color
				result["line_right_colorindex"] = one_cell.Borders(10).ColorIndex
				result["line_right_thick"] = one_cell.Borders(10).Weight
				result["line_right_tintandshade"] = one_cell.Borders(10).TintAndShade
			if one_cell.Borders(11).LineStyle != -4142:
				result["line_x1_style"] = one_cell.Borders(11).LineStyle
				result["line_x1_color"] = one_cell.Borders(11).Color
				result["line_x1_colorindex"] = one_cell.Borders(11).ColorIndex
				result["line_x1_thick"] = one_cell.Borders(11).Weight
				result["line_x1_tintandshade"] = one_cell.Borders(11).TintAndShade
			if one_cell.Borders(12).LineStyle != -4142:
				result["line_x2_style"] = one_cell.Borders(12).LineStyle
				result["line_x2_color"] = one_cell.Borders(12).Color
				result["line_x2_colorindex"] = one_cell.Borders(12).ColorIndex
				result["line_x2_thick"] = one_cell.Borders(12).Weight
				result["line_x2_tintandshade"] = one_cell.Borders(12).TintAndShade

		for one in list(result.keys()):
			if result[one] == None:
				del result[one]
		return result

	def read_all_range_name(self):
		"""
		모든 영역의 이름(rangename)을 돌려주는것

		"""
		names_count = self.xlbook.Names.Count
		result = []
		if names_count > 0:
			for aaa in range(1, names_count + 1):
				name_name = self.xlbook.Names(aaa).Name
				name_range = self.xlbook.Names(aaa)
				result.append([aaa, str(name_name), str(name_range)])
		return result

	def read_all_shape_in_file(self):
		"""
		엑셀화일안의 모든 그림객체에대한 이름을 갖고온다
		결과 : [시트이름, 그림이름]

		:return:
		"""
		result = []
		all_sheet_name = self.read_all_sheet_name()
		for sheet_name in all_sheet_name:
			all_shape_name = self.read_all_shape_name_in_sheet(sheet_name)
			if all_shape_name:
				for shape_name in all_shape_name:
					result.append([sheet_name, shape_name])
		return result

	def read_all_sheet_name(self):
		"""
		워크시트의 모든 이름을 읽어온다
		"""
		result = []
		for a in range(1, self.xlbook.Worksheets.Count + 1):
			result.append(self.xlbook.Worksheets(a).Name)
		return result

	def read_cell(self, sheet_name="", xyxy=""):
		"""
		보관용 : 예전에 사용했던 코드
		"""
		result = self.read_value_in_cell(sheet_name, xyxy)
		return result

	def read_conditional_format(self, sheet_name):
		"""
		현재 시트안의 조건부서식의 내용을 갖고오는 것
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		cf_count = sheet_object.Cells.FormatConditions.Count
		for index in range(cf_count):
			fc_object = sheet_object.Cells.FormatConditions.Item(index + 1)
			cfBase = fc_object.Type
			dd = fc_object.AppliesTo.Address
			dd2 = fc_object.Formula1
			try:
				dd3 = fc_object.Formula2
			except:
				dd3

	def read_continuous_range_value(self, sheet, xyxy):
		"""
		현재선택된 셀을 기준으로 연속된 영역을 가지고 오는 것입니다
		"""
		row = xyxy
		col = xyxy
		sheet_object = self.check_sheet_name(sheet)
		bottom = row  # 아래의 행을 찾는다
		while sheet_object.Cells(bottom + 1, col).Value not in [None, '']:
			bottom = bottom + 1
		right = col  # 오른쪽 열
		while sheet_object.Cells(row, right + 1).Value not in [None, '']:
			right = right + 1
		return sheet_object.Range(sheet_object.Cells(row, col), sheet_object.Cells(bottom, right)).Value

	def read_coord_in_cell(self, sheet_name="", xyxy=""):
		"""
		셀의 픽셀 좌표를 갖고온다

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		range_object = self.get_range_object_by_xyxy(sheet_name, xyxy)

		rng_x_coord = range_object.Left
		rng_y_coord = range_object.Top
		rng_width = range_object.Width
		rng_height = range_object.Height
		return [rng_x_coord, rng_y_coord, rng_width, rng_height]

	def read_day_value(self, time_char=time.localtime(time.time())):
		"""
		일 -----> ['05', '095']
		"""
		return [time.strftime('%d', time_char), time.strftime('%j', time_char)]

	def read_excel_color_no_as_rgb(self, color_no):
		"""
		:param color_no:
		:return:
		"""
		result = self.var_common["dic_colorindex_rgblist"][color_no]
		return result

	def read_filename_for_activeworkbook(self):
		"""
		워크북의 이름을 읽어온다

		"""
		return self.xlbook.Name

	def read_formula_in_range(self, sheet_name="", xyxy=""):
		"""
		선택한 영역의 수식을 읽어오는 것

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		:return:
		"""

		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		range_object = self.get_range_object_by_xyxy(sheet_name, xyxy)
		result = range_object.Formula
		return result

	def read_formula_only_in_range(self, sheet_name="", xyxy=""):
		"""
		선택한 영역의 수식을 읽어오면, 수식이 없는 것은 입력값이 들어가 있다
		그래서, =로시작하는 수식만 남기는 것이다

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		:return:
		"""
		result = []
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		range_object = self.get_range_object_by_xyxy(sheet_name, xyxy)

		tup_2d = range_object.Formula
		if type(tup_2d) == type([]) or type(tup_2d) == type(()):
			pass
		else:
			tup_2d = [tup_2d]
		for tup_1d in tup_2d:
			temp_list = []
			for value in tup_1d:
				if str(value).startswith("="):
					temp_list.append(value)
				else:
					temp_list.append(None)
			result.append(temp_list)
		return result

	def read_general(self):
		"""
		몇가지 엑셀에서 자주사용하는 것들정의
		엑셀의 사용자, 현재의 경로, 화일이름, 현재시트의 이름
		"""
		return [self.xlapp.ActiveWorkbook.Name, self.xlapp.UserName, self.xlapp.ActiveWorkbook.ActiveSheet.Name]

	def read_general_for_workbook(self):
		"""
		몇가지 엑셀에서 자주사용하는 것들정의
		엑셀의 사용자, 현재의 경로, 화일이름, 현재시트의 이름
		"""
		return [self.xlapp.ActiveWorkbook.Name, self.xlapp.UserName, self.xlapp.ActiveWorkbook.ActiveSheet.Name]

	def read_general_inform_for_excel(self):
		"""
		몇가지 엑셀에서 자주사용하는 것들정의
		엑셀의 사용자, 현재의 경로, 화일이름, 현재시트의 이름

		"""
		result = []
		result.append(self.xlapp.ActiveWorkbook.Name)
		result.append(self.xlapp.UserName)
		result.append(self.xlapp.ActiveWorkbook.ActiveSheet.Name)
		return result

	def read_line_value(self, sheet_name, xyxy, position):
		"""
		 입력예 : "", [1,1,3,4], ["left", "right"],"bla","-","t0"]
		 선의위치 (5-대각선 오른쪽, 6-왼쪽대각선, 7:왼쪽, 8;위쪽, 9:아래쪽,	10:오른쪽, 11:안쪽세로, 12:안쪽가로)
		 라인스타일 (1-실선, 2-점선, 3-가는점선, 6-굵은실선,
		 굵기 (0-이중, 1-얇게, 2-굵게)
		 색깔 (0-검정, 1-검정, 3-빨강),

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		:param input_list: list type
		:return:
		 """

		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		range_object = self.get_range_object_by_xyxy(sheet_name, xyxy)
		position_list = []
		if type("abc") == type(position):
			position_list = self.vars["check_line_position"][position]
		elif type([]) == type(position):
			for one in position:
				aa = self.vars["check_line_position"][one]
				position_list.extend(aa)
		result = []
		# print(position_list)
		for one in position_list:
			rgb_int = range_object.Borders(one).Color
			thickness = range_object.Borders(one).Weight
			style = range_object.Borders(one).LineStyle
			result.append([one, rgb_int, thickness, style])
		return result

	def read_memo_in_cell(self, sheet_name="", xyxy=""):
		"""
		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		:return:

		셀의 메모를 돌려주는것

		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		range_object = self.get_range_object_by_xyxy(sheet_name, xyxy)

		one_value = range_object.Comment.Text()
		return one_value

	def read_n_char_from_start_in_range(self, sheet_name, xyxy, n_char):
		"""
		자주사용하는 형태중의 하나가, 앞에서 몇번째의 문장을 갓고와서 리스트로 만드는 방법을 아래와 같이 만들어 보았다
		생각보다, 많이 사용하면서, 간단한것이라, 아마 불러서 사용하는것보다는 그냥 코드로 새롭게 작성하는경우가
		많겠지만, 그냥. . 그냥 만들어 보았다

		시군 구자료에서 앞의 2 글자만 분리해서 얻어오는 코드
		어떤자료중에 앞에서 몇번째것들만 갖고오고 싶을때

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		:param n_char:
		"""
		list_2d = self.read_value_in_range(sheet_name, xyxy)
		result = []
		for list_1d in list_2d:
			for one in list_1d:
				try:
					result.append(one[0:n_char])
				except:
					pass

	def read_n_write_with_two_sheet(self, read_sheet, read_x_no, write_xy_list):
		# 현재 시트의 한줄을 읽어와서, 다른시트에 값을 넣는 경우
		one_list = self.read_value_in_xline(read_sheet, read_x_no)[0]
		for list_1d in write_xy_list:
			read_no, write_sheet, write_xy = list_1d
			self.write_cell(write_sheet, write_xy, one_list[read_no - 1])

	def read_path_for_workbook(self):
		"""
		현재 엑셀화일의 경로와 화일명을 갖고오는 것

		:return:
		"""
		return self.xlapp.Path

	def read_range(self, sheet_name="", xyxy=""):
		"""
		제일 많이 사용하는 것이라, 만듦
		:param xyxy:
		:return:
		"""
		result = self.read_value_in_range(sheet_name, xyxy)
		return result

	def read_range_value(self, sheet_name="", xyxy=""):
		"""
		예전자료를 위해서 남겨 놓음
		original : read_value_in_range
		"""
		result = self.read_value_in_range(sheet_name, xyxy)
		return result

	def read_rangename_all(self):
		"""
		모든 영역의 이름(rangename)을 돌려주는것

		"""
		names_count = self.xlbook.Names.Count
		result = []
		if names_count > 0:
			for aaa in range(1, names_count + 1):
				name_name = self.xlbook.Names(aaa).Name
				name_range = self.xlbook.Names(aaa)
				result.append([aaa, str(name_name), str(name_range)])
		return result

	def read_second_value(self, time_char=time.localtime(time.time())):
		"""
		초 -----> ['48']
		"""
		return [time.strftime('%S', time_char)]

	def read_selection_address(self):
		"""
		예전자료를 위해서 남겨 놓음
		original : read_address_for_selection
		"""
		result = self.read_address_for_selection()
		return result

	def read_shape_name_in_sheet_by_index(self, sheet_name, shape_no):
		"""
		번호로 객체의 이름을 갖고오는것

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param shape_no:
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		result = sheet_object.Shapes(shape_no).Name
		return result

	def read_sheet_name_all(self):
		""" ** 예전자료를 위해 남겨둠 ** """
		result = self.read_all_sheet_name()
		return result

	def read_sheet_name_by_position_no(self, input_no):
		"""
		선택된 시트를 앞에서 몇번째로 이동시키는 것
		:param sheet_name:
		:param input_index:
		:return:
		"""
		all_sheet_names = self.read_all_sheet_name()
		result = all_sheet_names[input_no - 1]

		return result

	def read_sheet_name_for_activesheet(self):
		"""
		read_name_for_activesheet()
		간략설명 : 현재의 활성화된 시트의 이름을 돌려준다
		출력형태 : 시트이름
		"""
		return self.xlApp.ActiveSheet.Name

	def read_today_value(self, time_char=time.localtime(time.time())):
		"""
		종합 -----> ['04/05/02', '22:07:48', '04/05/02 22:07:48','2002-04-05']
		040621 : 이름을 변경 (total -> today)
		"""
		aaa = string.split(time.strftime('%c', time_char))
		total_dash = time.strftime('%Y', time_char) + "-" + time.strftime('%m', time_char) + "-" + time.strftime('%d',
																												 time_char)
		return [aaa[0], aaa[1], time.strftime('%c', time_char), total_dash]

	def read_username(self):
		"""
		사용자 이름을 읽어온다

		"""
		return self.xlapp.UserName

	def read_value(self, sheet_name="", xyxy=""):
		"""
		read_value(sheet_name="", xyxy="")
		값을 일정한 영역에서 갖고온다
		만약 영역을 두개만 주면 처음과 끝의 영역을 받은것으로 간주해서 알아서 처리하도록 변경하였다
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		range_object = self.get_range_object_by_xyxy(sheet_name, xyxy)
		temp_result = range_object.Value
		result = []
		if 1 < len(temp_result):
			for one_data in temp_result:
				result.append(list(one_data))
		else:
			result = temp_result
		return result

	def read_value2_in_cell(self, sheet_name="", xyxy=""):
		"""
		엑셀의 값중에서 화면에 보여지는 값을 읽어오는 것

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		"""
		result = self.read_value2_in_range(sheet_name, xyxy)
		return result

	def read_value2_in_range(self, sheet_name="", xyxy=""):
		"""
		엑셀의 값중에서 화면에 보여지는 값을 읽어오는 것

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		range_object = self.get_range_object_by_xyxy(sheet_name, xyxy)
		return range_object.Value2

	def read_value2_in_range_with_sheet_object(self, sheet_object, xyxy):
		"""
		속도를 높이는 목적으로 입력값이 제대로라고 가정한다

		:param sheet_object:
		:param xyxy:
		"""

		range_object = sheet_object.Range(sheet_object.Cells(xyxy[0], xyxy[1]),
										  sheet_object.Cells(xyxy[2], xyxy[3]))
		return range_object.Value2

	def read_value3_in_cell(self, sheet_name="", xyxy=""):
		"""
		읽어온값 자체를 변경하지 않고 그대로 읽어오는 것
		그자체로 text형태로 돌려주는것
		만약 스캔을 한 숫자가 ,를 잘못 .으로 읽었다면
		48,100 => 48.1로 엑셀이 바로 인식을 하는데
		이럴때 48.100으로 읽어와서 바꾸는 방법을 하기위해 사용하는 방법

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		range_object = self.get_range_object_by_xyxy(sheet_name, xyxy)

		result = sheet_object.Cells(x1, y1).Text
		return result

	def read_value3_in_range(self, sheet_name="", xyxy=""):
		"""
		영역의 값을 갖고온다
		주) 원래는 value였으나 pyside6에서 코딩중에 날짜부분이 문제가 일으키는데 value2로 변경하니 문제가 없어서 변경함

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		"""
		result = self.read_value_in_range_as_text(sheet_name, xyxy)

		return result

	def read_value_for_continuous_range(self, sheet_name="", xyxy=""):
		"""
		read_continuousrange_value(sheet_name="", xyxy="")
		현재선택된 셀을 기준으로 연속된 영역을 가지고 오는 것입니다
		"""
		self.menu_dic['read_value_for_continuousrange'] = {'표시여부': 'x',
															'그리드메뉴': ['read', 'value', 'for_continuousrange'],
															'실행메뉴': ['read', 'value', 'for_continuousrange']}
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		range_object = self.get_range_object_by_xyxy(sheet_name, xyxy)
		row = xyxy
		col = xyxy
		sheet_object = self.xlBook.Worksheets(sheet_name)
		bottom = row  # 아래의 행을 찾는다
		while sheet_object.Cells(bottom + 1, col).Value not in [None, '']:
			bottom = bottom + 1
		right = col  # 오른쪽 열
		while sheet_object.Cells(row, right + 1).Value not in [None, '']:
			right = right + 1
		return sheet_object.Range(sheet_object.Cells(row, col), sheet_object.Cells(bottom, right)).Value

	def read_value_for_range_name(self, sheet_name, input_range_name):
		"""
		이름영역으로 값을 읽어오는 것

		:param sheet_name:
		:param input_range_name:
		:return:
		"""
		xyxy = self.read_address_for_range_name(sheet_name, input_range_name)
		result = self.read_value_in_range(sheet_name, xyxy)
		return result

	def read_value_in_activecell(self):
		"""
		현재셀의 값을 돌려주는것

		"""
		result = self.xlapp.ActiveCell.Value2
		self.result = result
		return result

	def read_value_in_cell(self, sheet_name="", xyxy=""):
		"""
		주) value -> value2
		값을 일정한 영역에서 갖고온다
		만약 영역을 두개만 주면 처음과 끝의 영역을 받은것으로 간주해서 알아서 처리하도록 변경하였다


		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		range_object = self.get_range_object_by_xyxy(sheet_name, xyxy)
		one_value = sheet_object.Cells(x1, y1).Value
		if type(one_value) == type(123):
			one_value = int(one_value)
		elif one_value == None:
			one_value = ""
		self.result = one_value
		result = one_value

		return result

	def read_value_in_cell_as_text(self, sheet_name="", xyxy=""):
		"""
		읽어온값 자체를 변경하지 않고 그대로 읽어오는 것
		그자체로 text형태로 돌려주는것
		만약 스캔을 한 숫자가 ,를 잘못 .으로 읽었다면
		48,100 => 48.1로 엑셀이 바로 인식을 하는데
		이럴때 48.100으로 읽어와서 바꾸는 방법을 하기위해 사용하는 방법

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		range_object = self.get_range_object_by_xyxy(sheet_name, xyxy)

		result = sheet_object.Cells(x1, y1).Text
		return result

	def read_value_in_cell_with_sheet_object_as_speedy(self, sheet_object, xy):
		"""
		보관용
		"""
		self.read_value_in_cell_with_sheet_object_for_speed(sheet_object, xy)

	def read_value_in_cell_with_sheet_object_for_speed(self, sheet_object, xy):
		"""
		속도를 높이는 목적으로 입력값이 제대로라고 가정한다
		"""
		result = sheet_object.Cells(xy[0], xy[1]).Value
		if type(result) == type(123):
			result = int(result)
		elif result == None:
			result = ""
		return result

	def read_value_in_continuous_range(self, sheet_name="", xyxy=""):
		"""
		현재선택된 셀을 기준으로 연속된 영역을 가지고 오는 것입니다

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		range_object = self.get_range_object_by_xyxy(sheet_name, xyxy)

		address = range_object.CurrentRegion()
		result = self.read_value_in_range(sheet_name, address)
		self.result = result
		return result

	def read_value_in_currentregion(self, sheet_name="", xyxy=""):
		"""
		선택한 시트의 currentregion의 값들

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		"""
		result = self.read_value_in_continuous_range(sheet_name, xyxy)
		self.result = result
		return result

	def read_value_in_multi_cell(self, sheet_name, xyxy_list):
		"""
		추가) 여러셀값을 한번에 갖고오는것도 넣음

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		"""
		sheet_object = self.check_sheet_name(sheet_name)

		if type(xyxy_list[0]) != type([]):
			xyxy_list = [xyxy_list]
		result = []
		for xyxy in xyxy_list:
			x1, y1, x2, y2 = self.check_address_value(xyxy)
			range_object = self.get_range_object_by_xyxy(sheet_name, xyxy)
			one_value = sheet_object.Cells(x1, y1).Value
			if type(one_value) == type(123):
				one_value = int(one_value)
			elif one_value == None:
				one_value = ""
			result.append(one_value)
		return result

	def read_value_in_range(self, sheet_name="", xyxy=""):
		"""
		영역의 값을 갖고온다
		주) 원래는 value였으나 pyside6에서 코딩중에 날짜부분이 문제가 일으키는데 value2로 변경하니 문제가 없어서 변경함

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		"""
		range_object = self.get_range_object_by_xyxy(sheet_name, xyxy)
		self.set_screen_update_off()
		result = range_object.Value
		self.set_screen_update_on()
		return result

	def read(self, sheet_name="", xyxy=""):
		result = self.read_value_in_range(sheet_name="", xyxy="")
		return result

	def read_value_in_range_as_speedy(self, xyxy):
		"""
		보관용
		"""
		self.read_value_in_range_for_speed(xyxy)

	def read_value_in_range_as_text(self, sheet_name="", xyxy=""):
		"""
		읽어온값 자체를 변경하지 않고 그대로 읽어오는 것  그자체로 text 형태로 돌려주는것  만약 스캔을 한 숫자가 .를 잘못 .으로 읽었다면
		48,100 => 48.1로 엑셀이 바로 인식을 하는데  이럴때 48.100 으로 읽어와서 바꾸는 방법을 하기위해 사용하는 방법

		:param sheet_ name: 시트이름, ""를 입력하면 현재 활성화된 시트이름으로 자동으로 변경됩
		:param xyxy: [1,1,2,2], 가로세로셀영역, ""로 입력하면 현재 선택영역이 자동으로 입력됨
		"""
		self.sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		self.set_screen_update_off()
		result = []
		for x in range(x1, x2 + 1):
			temp = []
			for y in range(y1, y2 + 1):
				one_value = self.sheet_object.Cells(x, y).Text
				temp.append(one_value)
			result.append(temp)
		self.set_screen_update_on()
		return result

	def read_value_in_range_check_date(self, sheet_name="", xyxy=""):
		"""
		영역의 자료를 읽어와서
		- 모든 자료를 리스트로 바꿔준다
		- 날짜와 시간의 자료가 있으면, 의미가있는 영역까지만 나타냄

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		range_object = self.get_range_object_by_xyxy(sheet_name, xyxy)

		self.set_screen_update_off()
		result = []
		for list_1d in range_object.Value:
			empty_list = []
			for value in list_1d:
				if pywintypes.TimeType == type(value):
					temp = str(value).split(" ")
					if temp[1] == "00:00:00+00:00":
						empty_list.append(temp[0])
					else:
						aaa = temp[0] + " " + temp[1].split("+")[0]
						empty_list.append(aaa)
				else:
					empty_list.append(value)
			result.append(empty_list)
		self.set_screen_update_on()
		return result

	def read_value_in_range_for_speed(self, xyxy):
		"""
		영역의 값을 갖고온다

		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:return:
		"""
		x1, y1, x2, y2 = xyxy
		range_object = self.var_pcell["sheet_object"].Range(self.var_pcell["sheet_object"].Cells(x1, y1),
															self.var_pcell["sheet_object"].Cells(x2, y2))
		if x1 == -1:
			return self.var_pcell["sheet_object"].Range(x1, y1).Value
		return range_object.Value

	def read_value_in_range_object(self, input_range_obj):
		"""
		range object로 값을 읽어오는 것

		:param input_range_obj:
		:return:
		"""
		result = input_range_obj.Value
		return result

	def read_value_in_range_with_numberformat(self, sheet_name="", xyxy=""):
		"""
		속성을 포함한 값을 읽어오는 것

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		range_object = self.get_range_object_by_xyxy(sheet_name, xyxy)

		result = []

		for x in range(x1, x2 + 1):
			temp = []
			for y in range(y1, y2 + 1):
				one_dic = {}
				one_cell = sheet_object.Cells(x, y)
				one_dic["y"] = x
				one_dic["x"] = y
				one_dic["value"] = one_cell.Value
				one_dic["value2"] = one_cell.Value2
				one_dic["text"] = one_cell.Text
				one_dic["formula"] = one_cell.Formula
				one_dic["formular1c1"] = one_cell.FormulaR1C1
				one_dic["numberformat"] = one_cell.NumberFormat
				temp.append(one_dic)
			result.append(temp)
		return result

	def read_value_in_range_with_sheet_object_as_speedy(self, sheet_object, xyxy):
		"""
		보관용
		"""

		self.read_value_in_range_with_sheet_object_for_speed(sheet_object, xyxy)

	def read_value_in_range_with_sheet_object_for_speed(self, sheet_object, xyxy):
		"""
		속도를 높이는 목적으로 입력값이 제대로라고 가정한다
		"""
		range_object = sheet_object.Range(sheet_object.Cells(xyxy[0], xyxy[1]), sheet_object.Cells(xyxy[2], xyxy[3]))
		return range_object.Value

	def read_value_in_range_with_xy_headers(self, sheet_name="", xyxy=""):
		"""
		영역의 값을 갖고온다. 맨앞과 위에 번호로 행과열을 추가한다
		가끔은 자료중에서 필요없는것을 삭제했더니, 원래 있었던 자료의 위치를 알수가 없어서, 만들어 본것임

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		range_object = self.get_range_object_by_xyxy(sheet_name, xyxy)

		top_line = list(range(y1 - 1, y2 + 1))

		all_data = list(range_object.Value2)
		result = []
		for x in range(0, x2 - x1 + 1):
			temp = [x + 1]
			temp.extend(list(all_data[x]))
			result.append(temp)
		result.insert(0, top_line)
		return result

	def read_value_in_selection(self, sheet_name):
		"""
		값을 일정한 영역에서 갖고온다
		만약 영역을 두개만 주면 처음과 끝의 영역을 받은것으로 간주해서 알아서 처리하도록 변경하였다

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		"""
		result = []
		sheet_object = self.check_sheet_name(sheet_name)
		address_set = self.xlapp.Selection.Address
		list_address = str(address_set).split(",")
		for one_address in list_address:
			temp = self.read_value_in_range(sheet_name, one_address)
			# print(one_address, temp)
			result.append(temp)
		return result

	def read_value_in_usedrange(self, sheet_name):
		"""
		usedrange 안의 값을 갖고온다

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		# print(sheet_object.UsedRange.Address)
		xyxy = self.check_address_value(sheet_object.UsedRange.Address)
		result = self.read_value_in_range(sheet_name, xyxy)
		return result

	def read_value_in_xline(self, sheet_name, xx):
		"""
		한줄인 x라인 의 모든값을 읽어온다

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xx: 가로줄의 시작과 끝 => [3,5]
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, x2 = self.check_xx_address(xx)
		result = sheet_object.Range(sheet_object.Cells(x1, 1),
									sheet_object.Cells(x1, 1)).EntireRow.Value2

		return result

	def read_value_in_xline_at_activecell(self):
		"""
		현재 활성화된 셀이 있는 한줄을 읽어옵니다
		"""
		sheet_object = self.check_sheet_name("")
		xyxy = self.check_address_value(self.xlapp.ActiveCell.Address)
		result = sheet_object.Cells(xyxy[0], 1).EntireRow.Value2[0]
		return result

	def read_value_in_xxline(self, sheet_name, xx):
		"""
		xx라인의 모든값을 읽어온다

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xx: 가로줄의 시작과 끝 => [3,5]
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		result = sheet_object.Range(sheet_object.Cells(xx[0], 1),
									sheet_object.Cells(xx[1], 1)).EntireRow.Value2
		return result

	def read_value_in_xywh(self, sheet_name, xywh):
		"""
		시작점을 기준으로 가로세로의 갯수만큼의 값을 읽어오는 것이다
		:param sheet_name:
		:param xywh:
		:return:
		"""
		xyxy = [xywh[0], xywh[1], xywh[0] + xywh[2] - 1, xywh[1] + xywh[3] - 1]
		result = self.read_value_in_range(sheet_name, xyxy)
		return result

	def read_value_in_yline(self, sheet_name, yy):
		"""
		한줄인 y라인의 모든값을 읽어온다

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param yy: 세로줄의 사작과 끝 => [3,7]
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		y1, y2 = self.check_yy_address(yy)
		result = sheet_object.Range(sheet_object.Cells(1, y1),
									sheet_object.Cells(1, y1)).EntireColumn.Value2

		return result

	def read_value_in_yline_at_activecell(self, sheet_name):
		"""
		사용된 범위안에서 현재셀이 선택된 y 라인 한줄을 갖고오는 것 영역을 가르킬때는 가장 왼쪽위의 셀을 기준으로 한다
		"""
		xyxy = self.read_address_for_activecell()
		xyxy2 = self.read_address_for_usedrange(sheet_name)
		result = self.read_value_in_range(sheet_name, [1, xyxy[1], 1, xyxy2[2]])[0]
		return result

	def read_value_in_yyline(self, sheet_name, yy):
		"""
		read_yyline_value(sheet_name="", xx)
		가로줄들의 전체의 값을 읽어온다
		"""
		self.menu_dic['read_value_for_yyline'] = {'표시여부': 'x', '그리드메뉴': ['read', 'value', 'for_yyline'],
												  '실행메뉴': ['read', 'value', 'for_yyline']}
		sheet_object = self.check_sheet_name(sheet_name)
		return sheet_object.Range(sheet_object.Cells(yy[0], 1), sheet_object.Cells(yy[1], 1)).EntireRow.Value

	def read_workbook_path(self):
		"""
		워크북의 경로를 읽어온다

		"""
		return self.xlbook.Path

	def read_xy_last_same_value(self):
		"""
		중복된 내용들  중에서 가장 마지막 위치 찾기
		"""
		pass

	def replace_first_char_in_range(self, sheet_name, xyxy, input_list_2d=[]):
		"""
		가끔 맨 앞글자만 바꾸고 싶을때가 있다
		그럴때 사용하는 것으로, 한번에 여러개도 가능하도록 만들었다

		사용법 : change_first_char("", [1,1,100,1], [["'", ""], ["*", ""], [" ", ""],])

		:param sheet_name: 시트이름
		:param xyxy: [1,1,2,2]
		:param input_list_2d: 2차원의 리스트형 자료
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		range_object = self.get_range_object_by_xyxy(sheet_name, xyxy)

		to_be_changed = []
		for one in input_list_2d:
			to_be_changed.append(one[0])

		for x in range(x1, x2 + 1):
			for y in range(y1, y2 + 1):
				try:
					cell_value = sheet_object.Cells(x, y).Value
					one_char = str(cell_value[0])
					if cell_value[0] in to_be_changed:
						for list_1d in input_list_2d:
							one_char = one_char.replace(list_1d[0], list_1d[1])
					sheet_object.Cells(x, y).Value = one_char + cell_value[1:]
				except:
					pass

	def replace_last_char_in_range(self, sheet_name, xyxy, input_list_2d=[]):
		"""
		가끔 맨 뒷글자만 바꾸고 싶을때가 있다
		그럴때 사용하는 것으로, 한번에 여러개도 가능하도록 만들었다
		사용법 : ("", [1,1,100,1], [["'", ""], ["*", ""], [" ", ""],])

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		:param input_list_2d: 2차원의 리스트형 자료
		"""
		# input_list_2d = self.change_xylist_to_list(input_list_2d)
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		range_object = self.get_range_object_by_xyxy(sheet_name, xyxy)

		to_be_changed = []
		for one in input_list_2d:
			to_be_changed.append(one[0])

		for x in range(x1, x2 + 1):
			for y in range(y1, y2 + 1):
				one_value = sheet_object.Cells(x, y).Value2
				one_char = str(one_value[-1])
				if one_value[-1] in to_be_changed:
					for list_1d in input_list_2d:
						one_char = one_char.replace(list_1d[0], list_1d[1])
				sheet_object.Cells(x, y).Value = one_value[:-1] + one_char

	def replace_many_times_with_jf_sql(self, jf_sql_list, replace_word_list, input_text):
		"""
		하나의 값을 여러 sql로 계속 값을 변경하는 것

		:param jf_sql_list:
		:param replace_word_list:
		:param input_text:
		:return:
		"""
		re_sql_list = []
		for one in jf_sql_list:
			re_sql_list.append(self.xyreinder(one))
			for index, one_re_sql in enumerate(re_sql_list):
				input_text = re.sub(one_re_sql, replace_word_list[index], input_text, flags=re.MULTILINE)
		return input_text

	def replace_many_word_in_range(self, sheet_name, xyxy, input_list):
		"""
		한번에 여러 갯수를 바꾸는 것이다

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		:param input_list: list type
		"""
		input_list = self.change_xylist_to_list(input_list)
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		range_object = self.get_range_object_by_xyxy(sheet_name, xyxy)

		for y in range(y1, y2 + 1):
			for x in range(x1, x2 + 1):
				one_value = str(self.read_value_in_cell(sheet_name, [x, y]))
				if one_value:
					for one_xylist in input_list:
						one_value = one_value.replace(one_xylist[0], one_xylist[1])
					self.write_value_in_cell(sheet_name, [x, y], one_value)

	def replace_with_jf_sql_as_selection_directly(self, jf_sql, replace_text):
		"""
		엑셀의 선택한 부분을 그대로 변경하는 것

		:param jf_sql:
		:param replace_text:
		:return:
		"""
		xyxy = self.read_address_for_selection()

		for x in range(xyxy[0], xyxy[2] + 1):
			for y in range(xyxy[1], xyxy[3] + 1):
				value = self.read_value_in_cell("", [x, y])
				aaa = self.xyre.replace_with_jf_sql(jf_sql, replace_text, value)
				self.write_value_in_cell("", [x, y], aaa)

	def reset_basic_pen_setup(self):
		"""
		펜의 기본값을 초기화 하는 것

		"""

		self.pen_color = self.color.change_scolor_to_rgbint("bla")
		self.pen_style = 4
		self.pen_thickness = 5
		self.start_point_width = 2
		self.start_point_length = 2
		self.start_point_style = 1
		self.end_point_width = 2
		self.end_point_length = 2
		self.end_point_style = 1

	def resize_data_by_xyxy(self, input_list_2d, xyxy):
		"""
		xyxy영역안에만 자료를 만들려고 할때
		이영역안의 맞도록 자료를 변경하는 것
		:param input_list_2d:
		:param xyxy:
		:return:
		"""
		result = []
		x1, y1, x2, y2 = self.check_address_value(xyxy)

		if len(input_list_2d) > x2 - x1 + 1:
			input_list_2d = input_list_2d[:x2 - x1 + 1]

		for list_1d in input_list_2d:
			if len(list_1d) > y2 - y1 + 1:
				list_1d = list_1d[:y2 - y1 + 1]
			result.append(list_1d)
		return result

	def resize_list(self, xy_list, resize=[1, 1]):
		"""
		리스트의 크기를 다시 설정하는 것
		"""
		result = []
		# 자료의 x갯수를 요청한것과 비교
		if len(xy_list) < resize[0] or resize[0] == 0:
			pass
		else:
			xy_list = xy_list[:resize[0]]
		# 자료의 y갯수를 요청한것과 비교
		for x_list in xy_list:
			if len(x_list) < resize[1] or resize[1] == 0:
				pass
			else:
				x_list = xy_list[:resize[0]]
			result.append(x_list)
		return result

	def resize_list_2d_by_xyxy(self, input_list_2d, xyxy):
		"""
		xyxy영역안에만 자료를 넣는다고 할때,  이영역안의 맞도록 자료를 변경하는 것
		자료를 dump할때 사용하면 된다
		만약 xyxy가 더 크면, None을 집어 넣는다

		:param input_list_2d:
		:param xyxy:
		:return:
		"""
		x1, y1, x2, y2 = self.check_address_value(xyxy)

		new_x = x2 - x1 + 1 - len(input_list_2d)
		new_y = y2 - y1 + 1 - len(input_list_2d[0])

		result = self.util.resize_list_2d_as_xy_list(input_list_2d, [new_x, new_y])
		return result

	def reverse_list_2d_top_n_bottom(self, sheet_name="", xyxy=""):
		"""
		2차원자료를 뒤집는 것

		:param sheet_name:
		:param xyxy:
		:return:
		"""
		t2d = self.read_value_in_range(sheet_name, xyxy)
		l2d = self.util.change_tuple_to_list_2d(t2d)
		l2d.reverse(self.write_list_2d_in_range(sheet_name, xyxy, l2d))
		return l2d

	def rotate_shape_by_name(self, input_shape_obj, rotation_degree):
		"""
		도형을 회전시키는 것
		도형은 중간을 기준으로 회=전을 합니다
		"""
		input_shape_obj.Rotation = rotation_degree

	def run_vba_module(self, macro_name):
		"""
		텍스트로 만든 매크로 코드를 실행하는 코드이다

		:param macro_name:
		"""
		self.xlapp.Run(macro_name)

	def sample_conditional_format(self):
		"""
		예제용

		:return:
		"""
		result = """
		conditional_format_with_operator("", [1, 1, 7, 7], "100<=value <200")
		conditional_format_with_function("", [1, 1, 7, 7], "=LEN(TRIM($A1))=0")
		"""
		return result

	def save(self, newfilename=""):
		"""
		엑셀화일을 저장하는것

		:param newfilename:
		"""
		if newfilename == "":
			self.xlbook.Save()
		else:
			# wb.SaveAs(Filename="C:\\NewFileName.xlsx")
			self.xlbook.SaveAs(newfilename, 51)

	def search_jf_sql_for_selection_with_new_sheet(self, jf_sql):
		"""
		엑셀의 현재 선택한 영역의 셀들을 적용한후에 새로운 시트에 그 결과를 나타내주는 것

		:param jf_sql:
		:return:
		"""
		list_2d = self.read_value_in_range("", "")
		result_list_2d = self.xyre.search_result_only_with_jf_sql_for_list_2d(jf_sql, list_2d)

		result_list_2d = self.change_list_2d_over_to_list_2d(result_list_2d)
		self.new_sheet()
		self.write_list_2d_from_cell("", [1, 1], result_list_2d)

	def search_value_by_jf_sql_in_range_with_paint(self, sheet_name, xyxy, jf_sql, input_scolor="yel"):
		"""
		엑셀의 영역에서 값을 찾으면, 셀에 색칠하기

		:param sheet_name:
		:param xyxy:
		:param jf_sql:
		:param input_scolor:
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		for x in range(x1, x2 + 1):
			for y in range(y1, y2 + 1):
				one_value = sheet_object.Cells(x, y).Value2
				found_or_not = self.xyre.search_all_with_jf_sql(jf_sql, str(one_value))
				if found_or_not:
					self.paint_cell_with_sheet_object(sheet_object, [x, y], input_scolor)

	def search_value_in_range_with_paint(self, sheet_name, xyxy, input_list, input_scolor="yel"):
		"""
		엑셀의 영역에서 값을 찾으면, 셀에 색칠하기
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		range_object = self.get_range_object_by_xyxy(sheet_name, xyxy)

		if type(input_list) != type([]):
			input_list = [input_list]

		for x in range(x1, x2 + 1):
			for y in range(y1, y2 + 1):
				one_value = sheet_object.Cells(x, y).Value2
				if one_value in input_list:
					self.paint_cell_with_sheet_object(sheet_object, [x, y], input_scolor)

	def select_active_workbook(self, input_file_name):
		"""
		보관용
		"""
		self.change_activeworkbook(input_file_name)

	def select_all(self, sheet_name):
		"""
		모든 영역을 선택한다

		:param sheet_name:
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		sheet_object.Cells.Select()

	def select_by_offset(self, oxyxy):
		"""
		현재의 셀 위치에서, offset으로 옮기는 것

		:param oxyxy:
		"""
		sheet_object = self.check_sheet_name("")
		x1, y1, x2, y2 = self.read_address_for_selection()
		ox1, oy1, ox2, oy2 = self.check_address_value(oxyxy)
		range_object = sheet_object.Range(sheet_object.Cells(x1 + ox1, y1 + oy1),
										  sheet_object.Cells(x2 + ox2, y2 + oy2))
		range_object.Select()

	def select_cell(self, sheet_name="", xyxy=""):
		"""
		셀을 활성화 하는것은 셀을 선택하는것과 같으며
		만약 영역이 들어오면 가장 왼쪽위의 영역을 선택합니다

		:param sheet_name: 시트이름
		:param xyxy: [1,1,2,2]
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		range_object = self.get_range_object_by_xyxy(sheet_name, xyxy)

		range_object.Select()

	def select_cell_in_range_by_xy_step(self, sheet_name="", xyxy=""):
		"""
		activecell을 offset으로 이동시키는것

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xy: [가로번호, 세로번호]
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		range_object = self.get_range_object_by_xyxy(sheet_name, xyxy)
		xyxy2 = self.read_address_for_activecell()
		sheet_object.Cells(xyxy2[0] + x1, xyxy2[1] + y1).Select()

	def select_cell_in_range_to_bottom(self, sheet_name="", xyxy=""):
		"""
		선택한 위치에서 제일왼쪽, 제일아래로 이동
		xlDown: - 4121,xlToLeft : - 4159, xlToRight: - 4161, xlUp : - 4162

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		range_object = self.get_range_object_by_xyxy(sheet_name, xyxy)
		range_object.End(-4121).Select()

	def select_cell_in_range_to_left_end(self, sheet_name="", xyxy=""):
		"""
		입력값 : 입력값없이 사용가능
		선택한 위치에서 끝부분으로 이동하는것
		xlDown : - 4121, xlToLeft : - 4159, xlToRight : - 4161, xlUp : - 4162

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		range_object = self.get_range_object_by_xyxy(sheet_name, xyxy)
		range_object.End(-4159).Select()

	def select_cell_in_range_to_right_end(self, sheet_name="", xyxy=""):
		"""
		선택한 위치에서 끝부분으로 이동하는것
		xlDown: - 4121,xlToLeft : - 4159, xlToRight: - 4161, xlUp : - 4162

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		range_object = self.get_range_object_by_xyxy(sheet_name, xyxy)
		range_object.End(-4161).Select()

	def select_cell_in_range_to_top(self, sheet_name="", xyxy=""):
		"""
		선택한 위치에서 끝부분으로 이동하는것
		xlDown: - 4121,xlToLeft : - 4159, xlToRight: - 4161, xlUp : - 4162

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		range_object = self.get_range_object_by_xyxy(sheet_name, xyxy)
		range_object.End(-4162).Select()

	def select_list_1d_unique_y(self, data1, data2):
		"""
		고유한 컬럼만 골라낸다
		"""
		result = []
		columns = self.read_y_names(data1)
		update_data2 = self.change_waste_data(data2)
		for temp_3 in update_data2:
			if not temp_3.lower() in columns:
				result.append(temp_3)
		return result

	def select_multi_range(self, sheet_name, input_range_list=""):
		"""
		영역을 선택한다

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		"""

		sheet_object = self.check_sheet_name(sheet_name)
		input_range_list = self.check_input_range(input_range_list)

		x1, y1, x2, y2 = self.check_address_value(input_range_list[0])
		multi_range = self.get_range_object_by_xyxy(sheet_name, [x1, y1, x2, y2])

		if len(input_range_list) > 1:
			for index, one_range in enumerate(input_range_list[1:]):
				x1, y1, x2, y2 = self.check_address_value(one_range)
				range_2 = self.get_range_object_by_xyxy(sheet_name, [x1, y1, x2, y2])

				multi_range = self.xlapp.Union(multi_range, range_2)
		multi_range.Select()

	def select_range(self, sheet_name, input_range_list=""):
		"""
		여러 영역을 선택하게 해주는것
		사용예 : select_list_1d("", [[1,1], [3,4], [7,8]])
		"""
		self.select_multi_range(sheet_name, input_range_list)

	def select_range_by_range_name(self, named_range_list):
		"""
		여러 영역을 선택하는 방법
		이것은 이름영역의 주소형태를 다루는 것이다
		sheet_xyxy_list = [["시트이름1", [1,1,4,4]], ["시트이름2", []], ]

		:param named_range_list:
		"""

		uninput_range = []

		if type([]) != type(named_range_list):
			named_range_list = [named_range_list]

		# print(named_range_list)
		for one_named_range in named_range_list:
			all_address, sheet, xyxy = self.get_address_for_range_name(one_named_range)
			# print("==> ", all_address, sheet, xyxy)
			sheet_object = self.check_sheet_name(sheet)
			x1, y1, x2, y2 = xyxy
			self.r1c1 = self.change_xyxy_to_r1c1([x1, y1, x2, y2])
			range_object = sheet_object.Range(self.r1c1)
			if uninput_range == []:
				uninput_range = range_object
				check_name = sheet
			else:
				if check_name == sheet:
					uninput_range = self.xlapp.Union(uninput_range, range_object)
				else:
					uninput_range.Select()
					sheet_object.Select()
					uninput_range = range_object
					check_name = sheet
			uninput_range.Select()

	def select_range_by_xxline(self, sheet_name, xx_list=[]):
		"""
		연속된 가로열을 선택한다

		:param sheet_name:
		:param xx_list:
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		start = self.change_char_to_num(xx_list[0])
		end = self.change_char_to_num(xx_list[1])
		changed_address = str(start) + ":" + str(end)
		self.range_object = sheet_object.Rows(changed_address).Select()

	def select_range_by_xyxy(self, sheet_name="", xyxy=""):
		"""
		영역을 선택한다

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		"""

		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		range_object = self.get_range_object_by_xyxy(sheet_name, xyxy)

		range_object.Select()
		result = range_object.Address
		return result

	def select_range_by_yyline(self, sheet_name, yy_list=[]):
		"""
		연속된 세로열을 선택한다

		:param sheet_name:
		:param yy_list:
		:return:
		"""

		sheet_object = self.check_sheet_name(sheet_name)
		start = self.change_num_to_char(yy_list[0])
		end = self.change_num_to_char(yy_list[1])

		changed_address = str(start) + ":" + str(end)
		sheet_object.Columns(changed_address).Select()

	def select_sheet(self, sheet_name):
		"""
		시트이름으로 시트를 선택
		:param sheet_name:
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		sheet_object.Select()

	def select_top_line_in_range(self, sheet_name="", xyxy=""):
		"""
		영역의 제일 위로 이동

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		range_object = self.get_range_object_by_xyxy(sheet_name, xyxy)

		sheet_object.Cells(x1, y1).Select()

	def select_workbook(self, input_file_name):
		"""
		열려진 워드 화일중 이름으로 선택하는것

		:param input_file_name:
		"""
		self.xlapp.Visible = True
		win32gui.SetForegroundWindow(self.xlapp.hwnd)
		self.xlapp.Workbooks(input_file_name).Activate()
		self.xlapp.WindowState = win32com.client.constants.xlMaximized

	def select_xline(self, sheet_name, x_list):
		"""
		하나의 가로줄을 선택하는 것

		:param sheet_name:
		:param x_list:
		:return:
		"""
		self.sheet_object = self.check_sheet_name(sheet_name)
		if type(123) == type(x_list):
			x_list = [x_list]

		start = self.change_char_to_num(x_list[0])
		changed_address = str(start) + ":" + str(start)
		self.range_object = self.sheet_object.Rows(changed_address).Select()

	def select_xxline(self, sheet_name, xx_list=[]):
		"""
		연속된 가로줄을 선택하는 것

		:param sheet_name:
		:param xx_list:
		:return:
		"""

		self.sheet_object = self.check_sheet_name(sheet_name)
		start = self.change_char_to_num(xx_list[0])
		end = self.change_char_to_num(xx_list[1])
		changed_address = str(start) + ":" + str(end)
		self.range_object = self.sheet_object.Rows(changed_address).Select()

	def select_yline(self, sheet_name, y_list):
		"""
		하나의 세로열을 선택하는 것

		:param sheet_name:
		:param y_list:
		:return:
		"""
		self.sheet_object = self.check_sheet_name(sheet_name)
		if type(123) == type(y_list):
			y_list = [y_list]

		start = self.change_num_to_char(y_list[0])
		changed_address = str(start) + ":" + str(start)
		self.range_object = self.sheet_object.Columns(changed_address).Select()

	def select_yyline(self, sheet_name, yy_list=[]):
		"""
		연속된 세로열을 선택하는 것

		:param sheet_name:
		:param yy_list:
		:return:
		"""

		self.sheet_object = self.check_sheet_name(sheet_name)
		start = self.change_num_to_char(yy_list[0])
		end = self.change_num_to_char(yy_list[1])

		changed_address = str(start) + ":" + str(end)
		self.sheet_object.Columns(changed_address).Select()

	def set_align_for_range(self, sheet_name, xyxy, x_align, y_align=""):
		"""
		정렬에 대해서 설정하는 부분
		가로와 세로 방향으로 모두 설정하는 것이다
		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		:param x_align:
		:param y_align:
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		range_object = self.get_range_object_by_xyxy(sheet_name, xyxy)

		dic_x = {"right": -4152, "middle": -4108, "center": -4108, "left": -4131, "오른쪽": -4152, "중간": 2, "왼쪽": -4131}
		dic_y = {"middle": -4108, "center": -4108, "top": -4160, "bottom": -4107, "low": -4107, "중간": -4108, "위": -4160,
				 "아래": - 4107}
		if x_align: range_object.HorizontalAlignment = dic_x[x_align]
		if y_align: range_object.VerticalAlignment = dic_y[y_align]

	def set_all_format_for_target_line(self, target_drawing):
		"""
		선택된 도형객체에 공통변수들을 할당하는 것

		:param target_drawing: 도형객체
		"""
		target_drawing.DashStyle = self.pen_style
		target_drawing.ForeColor.RGB = self.pen_color
		target_drawing.Weight = self.pen_thickness
		target_drawing.BeginArrowheadLength = self.start_point_length
		target_drawing.BeginArrowheadStyle = self.start_point_style
		target_drawing.BeginArrowheadWidth = self.start_point_width
		target_drawing.EndArrowheadLength = self.end_point_length
		target_drawing.EndArrowheadStyle = self.end_point_style
		target_drawing.EndArrowheadWidth = self.end_point_width

	def set_auto_next_line_in_range(self, sheet_name, xyxy, input_value=""):
		"""
		셀의 줄바꿈을 설정할때 사용한다
		만약 status를 false로 하면 줄바꿈이 실행되지 않는다.

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		:param input_value: 입력자료
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		sheet_object.Range(xyxy).WrapText = input_value

	def set_autofilter_in_range(self, sheet_name="", xyxy=""):
		"""
		선택한 영역안의 자동필터를 실행하는 것

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		range_object = self.get_range_object_by_xyxy(sheet_name, xyxy)
		range_object.Columns.AutoFilter(1)

	def set_autofilter_in_range_with_by_criteria(self, sheet_name, xyxy, y_line, operator, input_value_1,
												 input_value_2):
		"""
		선택한 영역안의 자동필터를 실행과
		입력값으로 필터링하기

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)

		Field : 설정이되는 Autofilter에서 적용을 원하는 열의 번호 (no)
		Criteria1 : 걸러내고자하는 기준값1, 다음과 같은 특수값 허용( "=" 값이 공백인 경우, "<>" 값이 공백이 아닌 경우, "><" (No Data)생략될 경우, 모든 데이터를 선택하는 것과 같다.
		Operator : 열겨형 XlAutoFilterOperaotr에 자세히 설명
		Criteria2 : 걸러내고자하는 기준값2
		VisibleDropDown : 제목 필드에 세모 버튼을 표기할지 유무


		xlAnd : 1, Criteria1 과 Criteria2에 대한논리적 AND 연산 결과
		xlOr : 2, Criteria1 과 Criteria2에 대한논리적 OR 연산 결과
		xlTop10Items : 3, 상위 10 개 아이템
		xlBottom10Items : 4, 하위 10 개 아이템
		xlTop10Percent : 5, 상위 10 퍼센트
		xlBottom10Percent : 6, 하위 10 퍼센트
		xlFilterValues : 7, 값에 대한 필터
		xlFilterCellColor : 8, 셀의 색깔에 대한 필터
		xlFilterFontColor : 9, 글자색에 대한 필터
		xlFilterIcon : 10, 아이콘에 대한 필터
		xlFilterDynamic : 11, 다이나믹 필터
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		range_object = self.get_range_object_by_xyxy(sheet_name, xyxy)
		range_object.Columns.AutoFilter(1)
		input_dic = {"Field": y_line}

		not_empty = ["not empty", "있음"]
		empty = ["empty", "비었음", "없음", ""]

		if operator == "and":
			input_dic["Criteria1"] = input_value_1
			input_dic["Criteria2"] = input_value_2
			input_dic["Operator"] = 1

		elif operator == "or":
			input_dic["Criteria1"] = input_value_1
			input_dic["Criteria2"] = input_value_2
			input_dic["Operator"] = 2

		elif operator == "top10":
			input_dic["Operator"] = 3

		elif operator == "bottom10":
			input_dic["Operator"] = 4

		elif operator == "top10%":
			input_dic["Operator"] = 5

		elif operator == "bottom10%":
			input_dic["Operator"] = 6

		elif operator == "value" or operator == "":
			input_dic["Operator"] = 7

			if input_value_1 in empty:
				input_value_1 = "="
			elif input_value_1 in not_empty:
				input_value_1 = "<>"
			input_dic["Criteria1"] = input_value_1

		elif operator == "cell_color":
			input_dic["Operator"] = 8
			if type(input_value_1) == type([]):
				input_value_1 = self.color.change_rgb_to_rgbint(input_value_1)
			input_dic["Criteria1"] = input_value_1

		elif operator == "font_color":
			input_dic["Operator"] = 9
			if type(input_value_1) == type([]):
				input_value_1 = self.color.change_rgb_to_rgbint(input_value_1)
			input_dic["Criteria1"] = input_value_1
		elif operator == "icon":
			operator = 10
		elif operator == "dynamic":
			operator = 11

		range_object.AutoFilter(**input_dic)

	def set_autofilter_off_in_range(self, sheet_name="", xyxy=""):
		"""
		선택한 영역안의 자동필터를 실행하는 것

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)


		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		range_object = self.get_range_object_by_xyxy(sheet_name, xyxy)
		range_object.Columns.AutoFilter()

	def set_autofit_in_range(self, sheet_name, xyxy="all"):
		"""
		자동 맞춤을 실시

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		range_object = self.get_range_object_by_xyxy(sheet_name, xyxy)

		new_y1 = self.change_num_to_char(y1)
		new_y2 = self.change_num_to_char(y2)
		if xyxy == "" or xyxy == "all":
			sheet_object.Columns.AutoFit()
		else:
			sheet_object.Columns(new_y1 + ':' + new_y2).AutoFit()

	def set_bold_in_range(self, sheet_name="", xyxy=""):
		"""
		과거 자료를 위해서 남겨둠

		:param sheet_name:
		:param xyxy:
		:return:
		"""
		self.set_font_bold_in_range(sheet_name, xyxy)

	def set_chart_style(self, chart_obj, chart_style):
		"""
		그래프의 형태를 정하는 것입니다
		:param chart_obj:
		:param chart_style:
		:return:
		"""
		chart_style_vs_enum = {"line": 4, "pie": 5}
		checked_chart_no = chart_style_vs_enum[chart_style]
		chart_obj.ChartType = checked_chart_no
		return chart_obj

	def set_conditional(self):
		"""
		set_conditional(self )
		a1을 기준으로 조건부서식 적용
		"""

		self.menu_dic['conditional_set'] = {'표시여부': '필요', '그리드메뉴': ['조건부서식', 'conditional', '조건부서식 적용-sample'],
											'실행메뉴': ['set', 'conditional', '']}
		sheet_object = self.check_sheet_name("")
		range_object = sheet_object.Range(sheet_object.Cells(1, 1), sheet_object.Cells(20, 20))
		formula1 = '=IF($A1="", TRUE, FALSE)'
		# win32com.client.constants.xlCellValue => 1
		# win32com.client.constants.xlGreaterEqual => 7
		range_object.FormatConditions.Add(1, 7, formula1)
		range_object.FormatConditions(range_object.FormatConditions.Count).SetFirstPriority()
		range_object.FormatConditions(1).Font.Bold = True
		range_object.FormatConditions(1).Font.Strikethrough = False
		range_object.FormatConditions(1).Font.TintAndShade = 0
		range_object.FormatConditions(1).Interior.PatternColorIndex = 1
		range_object.FormatConditions(1).Interior.Color = 5296274
		range_object.FormatConditions(1).Interior.TintAndShade = 0
		range_object.FormatConditions(1).StopIfTrue = False

	def set_conditional_format(self, sheet_name, xyxy, operator, range_format):
		"""
		조건부서식을 update 한것
		일반적으로 사용하는 어떤 형식의 값이 와도 알아서 적용되는것

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		:param operator:
		:param range_format:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		range_object = self.get_range_object_by_xyxy(sheet_name, xyxy)

		operator = str(operator).strip().upper()
		aaa = self.util.split_operator(operator)
		if operator.startswith("AND") or operator.startswith("OR"):
			# "and(100<=$A1, $A1<200)"	 "or(100<=$A1, $A1<200)" 등을 사용할때
			cf_object = range_object.FormatConditions.Add(2, None, "=" + operator)
		elif operator.startswith("="):
			# 보통 수식을 사용할때 적용되는 것
			cf_object = range_object.FormatConditions.Add(2, None, operator)
		elif not "," in operator and len(aaa) == 5:
			# "100<-$A31<200"
			cf_object = range_object.FormatConditions.Add(2, None,
														  "=AND(" + aaa[0] + aaa[1] + aaa[2] + "," + aaa[2] + aaa[3] +
														  aaa[4] + ")")
		elif not "," in operator and len(aaa) == 3:
			# "100>$A10"
			cf_object = range_object.FormatConditions.Add(2, None, "=" + operator)

		self.set_format_in_range(cf_object, range_format)

	def set_conditional_format_for_line_colored_when_not_empty_nth_yline_value(self, sheet_name, xyxy, input_scolor,
																				start_xy):
		"""
		선택한 영역의 n번째에 자료가 들어가면 들어간 가로줄에 색칠하기

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		:param input_scolor:
		:param start_xy:
		:return:
		"""

		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		range_object = self.get_range_object_by_xyxy(sheet_name, xyxy)

		range_object.FormatConditions.Delete()  # 영역에 포함된 조건부 서식을 지우는 것
		range_object.FormatConditions.Add(win32com.client.constants.xlExpression, win32com.client.constants.xlNotEqual,
										  '=IF($(]="",FALSE, TRUE)'.format(start_xy))
		range_object.FormatConditions(1).Interior.Color = self.color.change_scolor_to_rgbint(input_scolor)

	def set_conditional_format_in_range(self):
		"""
		조건부서식을 좀더 사용하기 쉽도록 변경이 필요

		:return:
		"""
		sheet_object = self.check_sheet_name("")
		range_object = sheet_object.Range(sheet_object.Cells(1, 1), sheet_object.Cells(20, 20))
		formula1 = ' = IF($A1 = "", TRUE, FALSE)'
		# win32com.client.constants.xlCellValue = > 1
		# win32com.client.constants.xlGreaterEqual = > 7
		range_object.FormatConditions.Add(1, 7, formula1)
		range_object.FormatConditions(range_object.FormatConditions.Count).SetFirstPriority()
		range_object.FormatConditions(1).Font.Bold = True
		range_object.FormatConditions(1).Font.Strikethrough = False
		range_object.FormatConditions(1).Font.TintAndShade = 0
		range_object.FormatConditions(1).Interior.PatternColorIndex = 1
		range_object.FormatConditions(1).Interior.Color = 5296274
		range_object.FormatConditions(1).Interior.TintAndShade = 0
		range_object.FormatConditions(1).StopIfTrue = False

	def set_conditional_format_with_data_bar(self, sheet_name="", xyxy=""):
		"""
		조건부서식 : 바타입
		만약 형태를 바꾸고 싶으면 setup을 먼저 이요해서 형태를 설정합니다

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		range_object = self.get_range_object_by_xyxy(sheet_name, xyxy)
		range_object.FormatConditions.Delete()
		range_object.FormatConditions.AddDatabar()

	def set_conditional_format_with_function(self, sheet_name, xyxy, input_formula, range_format):
		"""
		조건부서식 : 함수사용
		만약 형태를 바꾸고 싶으면 setup을 먼저 이요해서 형태를 설정합니다

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		:param input_formula:
		:param range_format:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		range_object = self.get_range_object_by_xyxy(sheet_name, xyxy)

		self.select_range(sheet_name, xyxy)
		range_object.FormatConditions.Delete()
		cf_count = self.xlapp.Selection.FormatConditions.Count
		range_object.FormatConditions.Add(2, None, input_formula)
		range_object.FormatConditions(cf_count + 1).SetFirstPriority()
		rng_con_for = range_object.FormatConditions(cf_count + 1)
		self.set_format_in_range(rng_con_for, range_format)

	def set_conditional_format_with_operator(self, sheet_name, xyxy, type, operator, range_format):
		"""
		조건부서식 사용하기
		만약 형태를 바꾸고 싶으면 setup을 먼저 이용해서 형태를 설정합니다

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		:param type:
		:param operator:
		:param range_format:
		"""
		type_dic = {"AboveAverageCondition": 12, "BlanksCondition": 10,
					"CellValue": 1, "ColorScale": 3, "DataBar": 4, "ErrorsCondition": 16,
					"Expression": 2, "IconSet": 6, "NoBlanksCondition": 13, "NoErrorsCondition": 17,
					"TextString": 9, "TimePeriod": 11, "Top10": 5, "Uniquevalues": 8, }
		oper_dic = {"between": 1, "equal": 3, "greater": 5, "greaterequal": 7, "less": 6, "Lessequal": 8,
					"notbetween": 2, "notequal": 4,
					"-": 3, ">": 5, ">=": 7, "<": 6, "<=": 8, "|-": 4}
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		range_object = self.get_range_object_by_xyxy(sheet_name, xyxy)

		self.select_range(sheet_name, xyxy)

		cf_count = self.xlapp.Selection.FormatConditions.Count
		type_value = type_dic[type]
		if type_value == 1:  # 셀값을 기준으로 판단
			aaa = self.util.split_operator(operator)
			if len(aaa) == 5:
				range_object.FormatConditions.Add(1, 1, "=" + aaa[0], "=" + aaa[-1])
			elif len(aaa) == 3:
				range_object.FormatConditions.Add(1, oper_dic[aaa[2]], "=" + aaa[2])
				range_object.FormatConditions(cf_count + 1).SetFirstPriority()
				rng_con_for = range_object.FormatConditions(cf_count + 1)
				self.set_format_in_range(rng_con_for, range_format)

	def set_conditional_format_with_xline_colored(self, sheet_name, xyxy, input_scolor, start_xy):
		"""
		선택한 영역의 n 번째에 자료가 들어가면 들어간 가로줄에 색칠하기

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		:param input_scolor:
		:param start_xy:
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		range_object = self.get_range_object_by_xyxy(sheet_name, xyxy)

		range_object.FormatConditions.Delete()  # 영역에 포함된 조건부 서식을 지우는 것
		range_object.FormatConditions.Add(2, 4, '=IF($(]="",FALSE, TRUE)'.format(start_xy))
		range_object.FormatConditions(1).interior.Color = self.color.change_scolor_to_rgbint(input_scolor)

	def set_conditional_in_range(self):
		"""
		set_range_conditional(self )
		a1을 기준으로 조건부서식 적용
		입력형태 :
		출력형태 :
		"""
		self.menu_dic['conditional_range_set'] = {'표시여부': '필요', '그리드메뉴': ['조건부서식', 'range', '조건부서식 적용-sample'],
												  '실행메뉴': ['set', 'range', 'conditional']}
		sheet_object = self.check_sheet_name("")
		range_object = sheet_object.Range(sheet_object.Cells(1, 1), sheet_object.Cells(20, 20))
		formula1 = '=IF($A1="", TRUE, FALSE)'
		# win32com.client.constants.xlCellValue => 1
		# win32com.client.constants.xlGreaterEqual => 7
		range_object.FormatConditions.Add(1, 7, formula1)
		range_object.FormatConditions(range_object.FormatConditions.Count).SetFirstPriority()
		range_object.FormatConditions(1).Font.Bold = True
		range_object.FormatConditions(1).Font.Strikethrough = False
		range_object.FormatConditions(1).Font.TintAndShade = 0
		range_object.FormatConditions(1).Interior.PatternColorIndex = 1
		range_object.FormatConditions(1).Interior.Color = 5296274
		range_object.FormatConditions(1).Interior.TintAndShade = 0
		range_object.FormatConditions(1).StopIfTrue = False

	def set_degree_of_shape(self, sheet_name, shape_obj, degree):
		"""
		도형을 회전시키는 것
		도형은 중간을 기준으로 회=전을 합니다
		shape _ obi :이동시킬 도형 이름
		"""
		shape_obj.IncrementRotation(degree)

	def set_fill(self, **input_dic):
		"""

		:param input_dic:
		:return:
		"""
		self.fill_setup.update(input_dic)
		return self.fill_setup

	def set_font_bold_at_cell(self, sheet_name, xy):
		"""
		셀안의 값을 진하게 만든다

		:param sheet_name:
		:param xy:
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		sheet_object.Cells(xy[0], xy[1]).Font.Bold = True

	def set_font_bold_for_cell(self, sheet_name, xyxy, bold_ox=True):
		"""
		set_cell_bold(sheet_name="", xyxy="", bold_ox = True)
		셀안의 값을 진하게 만든다
		"""
		self.menu_dic['set_bold_for_cell'] = {'표시여부': 'x', '그리드메뉴': ['set', 'bold', 'for_cell'],
											  '실행메뉴': ['set', 'bold', 'for_cell']}
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		range_object = self.get_range_object_by_xyxy(sheet_name, xyxy)

		range_object.Font.Bold = bold_ox

	def set_font_bold_in_range(self, sheet_name="", xyxy=""):
		"""
		선택영역의 폰트의 bold를 설정

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		:param input_value:
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		range_object = self.get_range_object_by_xyxy(sheet_name, xyxy)
		range_object.Font.Bold = True

	def set_font_border_style(self, input_color, thickness="", input_line_style=""):
		"""
		외곽선을 설정하는 것

		:param input_color:
		:param thickness:
		:param input_line_style:
		"""
		border_thick = {}
		border_thick["---"] = 2  # 0.25 point.
		border_thick["--"] = 4  # 0.50 point.
		border_thick["--"] = 6  # 0.75 point.
		border_thick[""] = 8  # 1.00 point. default.
		border_thick["+"] = 12  # 1.50 points.

		border_thick["++"] = 18  # 2.25 points.
		border_thick["+++"] = 24  # 3.00 points.
		border_thick["++++"] = 36  # 4.50 points
		border_thick["+++++"] = 48  # 6.00 points.
		border_ltbr = {}
		border_ltbr["bottom"] = -3
		border_ltbr["x_down"] = -7
		border_ltbr["x_up"] = -8
		border_ltbr["left"] = -2
		border_ltbr["right"] = -4
		border_ltbr["top"] = -1
		border_ltbr["-"] = -5
		border_ltbr["!"] = -6

		line_style = {}
		line_style["-."] = 5
		line_style["-.."] = 6
		line_style["."] = 2
		line_style["="] = 7

		line_style["DashDot"] = 5
		line_style["DashDotDot"] = 6
		line_style["DashDotStroked"] = 20
		line_style["DashLargeGap"] = 4
		line_style["DashSmal lGap"] = 3
		line_style["Dot"] = 2
		line_style["Double"] = 7
		line_style["DoubleWavy"] = 19
		line_style["Emboss3D"] = 21
		line_style["Engrave3D"] = 22
		line_style["Inset"] = 24

		line_style["None"] = 0
		line_style["Outset"] = 23
		line_style["Single"] = 1
		line_style["SingleWavy"] = 18
		line_style["ThickThinLargeGap"] = 16
		line_style["ThickThinMedGap"] = 13
		line_style["ThickThinSmallGap"] = 10
		line_style["ThinThickLargeGap"] = 15
		line_style["ThinThickMedGap"] = 12
		line_style["ThinThickSmallGap"] = 9
		line_style["ThinThickThinLargeGap"] = 17
		line_style["ThinThickThinMedGap"] = 14
		line_style["ThinThickThinSmallGap"] = 11
		line_style["Triple"] = 8
		all_font_border_style = {}
		all_font_border_style["line_style"] = input_color
		all_font_border_style["thickness"] = border_thick[thickness]
		all_font_border_style["line_style"] = input_line_style
		return all_font_border_style

	def set_font_color_for_part_of_cell_value(self, sheet_name, xy, from_to, input_font_list):
		"""

		:param sheet_name:
		:param xy:
		:param from_to:
		:param input_font_list:
		:return:
		"""

		input_font_list = self.change_xylist_to_list(input_font_list)

		sheet_object = self.check_sheet_name(sheet_name)
		range_object = sheet_object.Cells(xy[0], xy[1])
		ddd = range_object.GetCharacters(from_to[0], from_to[1] - from_to[0])

		checked_font = self.util.check_font_data(input_font_list)

		if "color" in checked_font.keys(): ddd.Font.Color = checked_font["color"]
		if "bold" in checked_font.keys(): ddd.Font.Bold = True
		if "size" in checked_font.keys(): ddd.Font.Size = checked_font["size"]
		if "underline" in checked_font.keys(): ddd.Font.Underline = True

	def set_font_color_in_cell(self, sheet_name, xy="", font_color=""):
		"""
		폰트의 컬러를 설정하는 것

		:param sheet_name:
		:param xy:
		:param font_color:
		:return:
		"""
		self.set_font_color_in_range(sheet_name, xy, font_color)

	def set_font_color_in_cell_by_rgb(self, sheet_name, xyxy, rgb=""):
		"""
		폰트의 컬러를 설정하는 것

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		:param rgb:
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		range_object = self.get_range_object_by_xyxy(sheet_name, xyxy)
		range_object.Font.Color = self.color.change_rgb_to_rgbint(rgb)

	def set_font_color_in_range(self, sheet_name, xyxy, font_color):
		"""
		draw_range_fontcolor(sheet_name, xyxy, font_color)
		영역에 글씨체를 설정
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		range_object = self.get_range_object_by_xyxy(sheet_name, xyxy)
		range_object.Font.Color = self.color.change_scolor_to_rgbint(font_color)

	def set_font_color_in_range_by_scolor(self, sheet_name, xyxy, font_color=""):
		"""

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		:param font_color:
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		range_object = self.get_range_object_by_xyxy(sheet_name, xyxy)
		range_object.Font.Color = self.color.change_scolor_to_rgbint(font_color)

	def set_font_for_shape(self, **input_dic):
		"""
		도형의 폰트를 설정하는 것

		:param input_dic: 변수들을 사전형식으로 입력
		:return:
		"""
		if "color" in input_dic.keys():
			input_dic["color"] = self.color.change_scolor_to_rgbint(input_dic["color"])
		self.vars["shape_font"].update(input_dic)
		return self.vars["shape_font"]

	def set_font_in_part_of_cell_value(self, sheet_name, xy, from_to, input_font_list):
		"""
		** 보관용

		:param sheet_name:
		:param xy:
		:param from_to:
		:param input_font_list:
		:return:
		"""

		input_font_list = self.change_xylist_to_list(input_font_list)

		self.sheet_object = self.check_sheet_name(sheet_name)
		range_object = self.sheet_object.Cells(xy[0], xy[1])
		ddd = range_object.GetCharacters(from_to[0], from_to[1] - from_to[0])

		checked_font = self.util.check_font_data(input_font_list)

		if "color" in checked_font.keys(): ddd.Font.Color = checked_font["color"]
		if "bold" in checked_font.keys(): ddd.Font.Bold = True
		if "size" in checked_font.keys(): ddd.Font.Size = checked_font["size"]
		if "underline" in checked_font.keys(): ddd.Font.Underline = True

	def set_font_in_range_with_setup(self, sheet_name, xyxy, input_list=[]):
		"""
		3. 영역에 적용한다
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		range_object = self.get_range_object_by_xyxy(sheet_name, xyxy)
		self.vars["my_range"] = range_object
		self.vars["sheet_object"] = sheet_object
		# self.vars["range_object"] = self.vars["my_range"] = self.check_address_value(xyxy)

		if input_list:
			# 아무것도 없으면, 기존의 값을 사용하고, 있으면 새로이 만든다
			if type(input_list) == type([]):
				self.setup_font(input_list)
			elif type(input_list) == type({}):
				# 만약 사전 형식이면, 기존에 저장된 자료로 생각하고 update한다
				self.vars["font"].update(input_list)

		self.vars["my_range"].Font.Size = self.vars["font"]["size"]
		self.vars["my_range"].Font.Bold = self.vars["font"]["bold"]
		self.vars["my_range"].Font.Italic = self.vars["font"]["italic"]
		self.vars["my_range"].Font.Name = self.vars["font"]["name"]

		self.vars["my_range"].Font.Strikethrough = self.vars["font"]["strikethrough"]
		self.vars["my_range"].Font.Subscript = self.vars["font"]["subscript"]
		self.vars["my_range"].Font.Superscript = self.vars["font"]["superscript"]
		self.vars["my_range"].Font.Underline = self.vars["font"]["underline"]
		self.vars["my_range"].Font.Color = self.vars["font"]["rgb_int"]

	def set_font_name_in_range(self, sheet_name, xyxy, input_value):
		"""
		선택영역의 폰트의 글씨체를 설정

		:param sheet_name:시트이름, ""를 입력하면 현재 활성화된 시트이름으로 자동으로 변경됨
		:param xyxy:[1,1,2,2], 가로세로셀영역, ""로 입력하면 현재 선택영역이 자동으로 입력됨
		:param input_value:
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		range_object = self.get_range_object_by_xyxy(sheet_name, xyxy)
		range_object.Font.Name = input_value

	def set_font_size_in_range(self, sheet_name, xyxy, size="+"):
		"""
		영역에 글씨크기를 설정한다
		2023-07-24 : +-도 가능하게 변경

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		:param size:
		:return:
 		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		range_object = self.get_range_object_by_xyxy(sheet_name, xyxy)

		if str(size)[0] == "+":
			size_up = 2 * len(size)
			for one in self.range_object:
				basic_size = one.Font.Size
				one.Font.Size = int(basic_size) + size_up
		elif str(size)[0] == "-":
			size_down = -2 * len(size)
			for one in self.range_object:
				new_size = one.Font.Size + size_down
				if new_size <= 0:
					one.Font.Size = 3
				else:
					one.Font.Size = new_size
		else:
			range_object.Font.Size = size

	def set_font_strikethrough_in_range(self, sheet_name="", xyxy=""):
		"""
		영역안의 값에 취소선을 긎는 것

		:param sheet_name: 시트이름
		:param xyxy: [1,1,2,2]
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		range_object = self.get_range_object_by_xyxy(sheet_name, xyxy)

		range_object.Font.Strikethrough = True

	def set_font_italic_in_range(self, sheet_name="", xyxy=""):
		"""
		영역안의 값에 취소선을 긎는 것

		:param sheet_name: 시트이름
		:param xyxy: [1,1,2,2]
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		range_object = self.get_range_object_by_xyxy(sheet_name, xyxy)

		range_object.Font.Italic = True

	def set_font_style(self, sheet_name, xyxy, input_value):
		"""
		선택영역의 폰트의 글씨체를 설정
		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		:param input_value:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		range_object = self.get_range_object_by_xyxy(sheet_name, xyxy)

		range_object.Font.Style = input_value

	def set_font_underline_in_range(self, sheet_name="", xyxy=""):
		"""
		영역의 값에 밑줄을 긎는것

		:param sheet_name: 시트이름
		:param xyxy: [1,1,2,2]
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		range_object = self.get_range_object_by_xyxy(sheet_name, xyxy)

		range_object.Font.Underline = True

	def set_font_with_dic_style(self, sheet_name, xyxy, **input_dic):
		"""
		폰트의 속성을 설정한다

		:param sheet_name:
		:param xyxy:
		:param input_dic:
		:return:
		"""
		self.sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		self.range_object = self.sheet_object.Range(self.sheet_object.Cells(x1, y1), self.sheet_object.Cells(x2, y2))
		for one in list(input_dic.keys()):
			if type(one) == type(123):
				self.range_object.Font.Size = input_dic[one]
			elif one in ["bold", "굵게", "찐하게", "진하게"]:
				self.range_object.Font.Bold = input_dic[one]
			elif one in ["italic", "이태리", "이태리체", "기울기"]:
				self.range_object.Font.Italic = input_dic[one]
			elif one in ["strikethrough", "취소선", "취소", "통과선" "strike"]:
				self.range_object.Font.Strikethrough = input_dic[one]
			elif one in ["subscript", "하위첨자", "아래첨자", "아랫첨자", "밑첨자"]:
				self.range_object.Font.Subscript = input_dic[one]
			elif one in ["superscript", "윗첨자", "위첨자", "웃첨자"]:
				self.range_object.Font.Superscript = input_dic[one]
			elif one in ["underline", "밑줄"]:
				self.range_object.Font.Underline = input_dic[one]
			elif one in ["vertical", "ver", "alignv"]:
				ver_value = {"middle": -4108, "top": 1, "bottom": 4, "default": 2, "중간": 3, "위": 1, "아래": 4}
				self.range_object.VerticalAlignment = ver_value[input_dic[one]]
			elif one in ["horizental", "hor", "alignh"]:
				ver_value = {"middle": -4108, "top": 1, "bottom": 4, "중간": 3, "위": 1, "아래": 4, "default": 2}
				self.range_object.HorizontalAlignment = ver_value[input_dic[one]]
			elif one in ["color", "색"]:
				self.range_object.Font.Color = self.color.change_scolor_to_rgbint(input_dic[one])
			else:
				pass

	def set_fore_color_for_chart(self, chart_object, input_rgb):
		"""
		차트의 forecolor를 설정하는 것

		:param chart_object:
		:param input_rgb:
		"""

		chart_object.ChartArea.Format.Fill.ForeColor.RGB = input_rgb

	def set_format_in_range(self, input_object, range_format="basic"):
		"""
		조건부서식에서 셀의 셀서식을 정의하기위한 설정
		""나 "basic"으로 입력이 되어있으면 기본설정값으로 적용이 되는 것입니다
		사용법 : {"line_style":1, "line_color":"red", "line_color":"red", "font_bold":1, "line_color":"red", }
		:param input_object:
		:param range_format:
		:return:
		"""
		if range_format == "" or range_format == "basic":
			input_object.Borders.LineStyle = 1
			input_object.Borders.ColorIndex = 1
			input_object.Interior.Color = 5296274
			input_object.Font.Bold = 1
			input_object.Font.ColorIndex = 1
		else:
			if "line_style" in range_format.keys():
				input_object.Borders.LineStyle = range_format["line_style"]
			if "line_color" in range_format.keys():
				rgbint = self.color.change_scolor_to_rgbint(range_format["line_color"])
				input_object.Borders.Color = rgbint
			if "color" in range_format.keys():
				rgbint = self.color.change_scolor_to_rgbint(range_format["color"])
				input_object.Interior.Color = rgbint
			if "font_bold" in range_format.keys():
				input_object.Font.Bold = range_format["font_bold"]
			if "font_color" in range_format.keys():
				rgbint = self.color.change_scolor_to_rgbint(range_format["font_color"])
				input_object.Font.Color = rgbint

	def set_formula_in_range(self, sheet_name, xyxy, input_value="=Now()"):
		"""
		영역에 수식을 넣는것

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		:param input_value: 입력자료
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		range_object = self.get_range_object_by_xyxy(sheet_name, xyxy)

		range_object.Formula = input_value

	def set_full_screen(self, fullscreen=1):
		"""
		전체화면으로 보이게 하는 것

		:param fullscreen:
		"""
		self.xlapp.DisplayFullScreen = fullscreen

	def set_gridline_off(self, true_or_flase=False):
		"""
		그리드라인을 없애는것
		"""
		self.xlapp.ActiveWindow.DisplayGridlines = true_or_flase

	def set_gridline_on(self, true_or_flase=True):
		"""
		그리드라인을 나탄게 하는것
		"""
		self.xlapp.ActiveWindow.DisplayGridlines = true_or_flase

	def set_gridline_onoff(self, onoff=""):
		"""
		그리드라인을 껏다 켰다하는 것

		:return:
		"""
		if onoff == "":
			if self.xlapp.ActiveWindow.DisplayGridlines == 0:
				self.xlapp.ActiveWindow.DisplayGridlines = 1
			else:
				self.xlapp.ActiveWindow.DisplayGridlines = 0
		else:
			self.xlapp.ActiveWindow.DisplayGridlines = onoff

	def set_height_for_xline(self, sheet_name, x, height=13.5):
		"""
		높이를 설정하는 것

		:param sheet_name:
		:param x:
		:param height:
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		sheet_object.Cells(x, 1).EntireRow.RowHeight = height

	def set_height_for_xxline(self, sheet_name, xx, height=13.5):
		"""
		가로줄의 높이를 설정.
		기본높이는 13.5로 되어있다

		:param sheet_name:
		:param xx:
		:param height:
		:return:
		"""
		self.menu_dic['set_xxline_height'] = {'표시여부': 'x', '그리드메뉴': ['set', 'xxline', 'height'],
											  '실행메뉴': ['set', 'xxline', 'height']}
		range_object = self.read_range_xx(sheet_name, xx)
		range_object.RowHeight = height

	def set_height_in_xxline(self, sheet_name, xx, height=13.5):
		"""
		** 보관용
		가로줄의 높이를 설정

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xx: 가로줄의 시작과 끝 => [3,5]
		:param height: 높이설정
		"""
		self.sheet_object = self.check_sheet_name(sheet_name)
		range_object = self.sheet_object.Range(self.sheet_object.Cells(xx[0], 1), self.sheet_object.Cells(xx[1], 1))
		range_object.RowHeight = height

	def set_hide_for_sheet(self, sheet_name, hide=0):
		"""
		시트 숨기기

		:param sheet_name:
		:param hide:
		"""

		sheet_object = self.check_sheet_name(sheet_name)
		sheet_object.Visible = hide

	def set_hide_for_workbook(self):
		"""
		실행되어있는 엑셀을 화면에 보이지 않도록 설정합니다
		"""

		self.xlapp.Visible = 0

	def set_interactive_off(self):
		"""
		자료가 변경이되면 차트등이 연결되서 실행되는것을 interactive라고 한다
		interactive => off
		"""

		self.xlapp.Interactive = False

	def set_interactive_on(self):
		"""
		자료가 변경이되면 차트등이 연결되서 실행되는것을 interactive라고 한다
		interactive => on
		"""
		self.xlapp.Interactive = True

	def set_invisible_for_workbook(self, value=1):
		"""
		실행되어있는 엑셀을 화면에 보이지 않도록 설정합니다
		기본설정은 보이는 것으로 되너 있읍니다

		:param value:
		"""
		self.xlapp.Visible = 0

	def set_maxmized_for_screen(self):
		"""
		엑셀화일을 최대화합니다

		:return:
		"""
		self.xlapp.WindowState = -4137

	def set_minimized_for_screen(self):
		"""
		xlMaximized : -4137
		xlMinimized : -4140
		xlNormal : -4143
		:return:
		"""
		# 엑셀화일을 최소화합니다
		self.xlapp.WindowState = -4140

	def set_numberformat_for_xline(self, sheet_name, x_no, style):
		"""
		보관용
		"""
		self.set_numberformat_for_xxline(sheet_name, x_no, style)

	def set_numberformat_for_xxline(self, sheet_name, x0, style):
		"""
		set_xxline_numberformat(sheet_name="", x0, style)
		각 열을 기준으로 셀의 속성을 설정하는 것
		입력형태 :
		출력형태 :
		"""
		self.menu_dic['set_xxline_numberformat'] = {'표시여부': 'x', '그리드메뉴': ['set', 'xxline', 'numberformat'],
													'실행메뉴': ['set', 'xxline', 'numberformat']}
		sheet_object = self.check_sheet_name(sheet_name)
		x1 = self.check_xy_address(x0)
		x = self.change_char_num(x1)
		if style == 1:  # 날짜의 설정
			sheet_object.Columns(x).NumberFormatLocal = "mm/dd/"
		elif style == 2:  # 숫자의 설정
			sheet_object.Columns(x).NumberFormatLocal = "_-* #,##0.00_-;-* #,##0.00_-;_-* '-'_-;_-@_-"
		elif style == 3:  # 문자의 설정
			sheet_object.Columns(x).NumberFormatLocal = "@"

	def set_numberformat_in_cell(self, sheet_name, xyxy, type1):
		"""
		보관용
		"""
		self.set_numberformat_in_range(sheet_name, xyxy, type1)

	def set_numberformat_in_column(self, sheet_name, num_col, style):
		"""
		각 열을 기준으로 셀의 속성을 설정하는 것이다
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		if style == 1:  # 날짜의 설정
			sheet_object.Columns(num_col).NumberFormatLocal = "mm/dd/yy"
		elif style == 2:  # 숫자의 설정
			sheet_object.Columns(num_col).NumberFormatLocal = "_-* #,##0.00_-;-* #,##0.00_-;_-* '-'_-;_-@_-"
		elif style == 3:  # 문자의 설정
			sheet_object.Columns(num_col).NumberFormatLocal = "@"

	def set_numberformat_in_range(self, sheet_name, xyxy, type1):
		"""
		좀더 사용하기 쉽도록 변경이 필요

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		:param type1:
		"""
		if type1 == 'general' or type1 == '':
			result = "#,##0.00_ "
		elif type1 == 'number':
			result = "US$""#,##0.00"
		elif type1 == 'account':
			result = "_-""US$""* #,##0.00_ ;_-""US$""* -#,##0.00 ;_-""US$""* ""-""??_ ;_-@_ "
		elif type1 == 'date':
			result = "mm""/""dd""/""xx"
		elif type1 == 'datetime':
			result = "xxxx""-""m""-""d h:mm AM/PM"
		elif type1 == 'percent':
			result = "0.00%"
		elif type1 == 'bunsu':
			result = "# ?/?"
		elif type1 == 'jisu':
			result = "0.00E+00"
		elif type1 == 'text':
			result = "@"
		elif type1 == 'etc':
			result = "000-000"
		elif type1 == 'other':
			result = "$#,##0.00_);[빨강]($#,##0.00)"
		else:
			result = "#,##0.00_ "
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		range_object = self.get_range_object_by_xyxy(sheet_name, xyxy)

		range_object.NumberFormat = result

	def set_numberformat_in_xxline(self, sheet_name, y0, style):
		"""
		보관용
		"""
		self.set_yyline_numberformat(sheet_name, y0, style)

	def set_numberproperty_in_range(self, sheet_name, xyxy, type1):
		"""
		좀더 사용하기 쉽도록 변경이 필요

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		:param type1:
		"""
		if type1 == 'general' or type1 == '':
			result = "#,##0.00_ "
		elif type1 == 'number':
			result = "US$""#,##0.00"
		elif type1 == 'account':
			result = "_-""US$""* #,##0.00_ ;_-""US$""* -#,##0.00 ;_-""US$""* ""-""??_ ;_-@_ "
		elif type1 == 'date':
			result = "mm""/""dd""/""xx"
		elif type1 == 'datetime':
			result = "xxxx""-""m""-""d h:mm AM/PM"
		elif type1 == 'percent':
			result = "0.00%"
		elif type1 == 'bunsu':
			result = "# ?/?"
		elif type1 == 'jisu':
			result = "0.00E+00"
		elif type1 == 'text':
			result = "@"
		elif type1 == 'etc':
			result = "000-000"
		elif type1 == 'other':
			result = "$#,##0.00_);[빨강]($#,##0.00)"
		self.sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		self.r1c1 = self.change_xyxy_to_r1c1([x1, y1, x2, y2])
		range_object = self.sheet_object.Range(self.r1c1)
		range_object.NumberFormat = result

	def set_pattern_in_range(self, sheet_name, xyxy, input_list=[]):
		"""
		셀에 색상과 특정한 패턴을 집어 넣어서 다른것들과 구분할수가 있다
		1. 배경색에 격자무늬를 집어넣을수가 있는데, 이것은 패턴을 칠하고 남은 공간을 칠할수가 있다
		2. 배경색 + 무늬선택(색과 무늬형식)
		3. 만약 배경색으로 채우기효과를 주면서 그라데이션을 준다면, 무늬선택은 불가능하다
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		range_object = self.get_range_object_by_xyxy(sheet_name, xyxy)

		input_list = self.change_xylist_to_list(input_list)

		self.setup_basic_data(sheet_name, xyxy)
		if input_list:
			# 아무것도 없으면, 기존의 값을 사용하고, 있으면 새로이 만든다
			if type(input_list) == type([]):
				self.setup_font(input_list)
			elif type(input_list) == type({}):
				# 만약 사전 형식이면, 기존에 저장된 자료로 생각하고 update한다
				self.vars["pattern"].update(input_list)
		a = 2
		if a == 1:
			range_object.Interior.Color = 5296274
			range_object.Interior.Pattern = self.vars["range_color"]["pattern"]
			range_object.Interior.PatternColor = self.vars["range_color"]["pattern"]

		elif a == 2:
			range_object.Interior.Gradient.Degree = 180
			range_object.Interior.Gradient.ColorStops.Clear()
			range_object.Interior.Gradient.ColorStops.Add(0)

		elif a == 3:
			range_object.Interior.Color = 5296274
			range_object.Interior.Pattern = self.vars["range_color"]["pattern"]  # xlSolid
			range_object.Interior.PatternColor = self.vars["range_color"][
				"pattern"]  # PatternColorIndex = xlAutomatic
			range_object.Interior.ThemeColor = 4  # xlThemeColorDark1 색상과 색조를 미리 설정한것을 불러다가 사용하는것
			# 이것은 기본적으로 마우스의 색을 선택할때 나타나는 테마색을 말하는 것이다

			range_object.Interior.TintAndShade = -0.249977111117893  # 명암을 조절
			range_object.Interior.PatternTintAndShade = 0

		return self.vars["range_color"]

	def set_pattern_in_range_with_setup(self, sheet_name, xyxy, input_list=[]):
		"""
		영역의 패턴을 설정하는 것

		:param sheet_name:
		:param xyxy:
		:param input_list:
		:return:
		"""
		self.setup_basic_data(sheet_name, xyxy)
		if input_list:
			# 아무것도 없으면, 기존의 값을 사용하고, 있으면 새로이 만든다
			if type(input_list) == type(0):
				self.setup_font(input_list)
			elif type(input_list) == type({}):
				# 만약 xf전 형식이 면, 기존에 저장된 자료로 생각하고 update 한다
				self.vars["pattern"].update(input_list)
		self.vars["range_object"].Interior.Color = 5296274
		self.vars["range_object"].Interior.Pattern = self.vars["range_color"]["pattern"]
		self.vars["range_object"].Interior.PatternColor = self.vars["range_color"]["pattern"]
		self.vars["range_object"].Interior.Pattern = 1  # xlPatternLinearGradient
		self.vars["range_object"].Interior.Gradient.Degree = 180
		# self.vars["range_object"].Interior.Gradient.ColorStops.Clear
		self.vars["range_object"].Interior.Gradient.ColorStops.Add(0)
		self.vars["range_object"].Interior.Color = self.color.change_rgb_to_rgbint([255, 255, 255])
		self.vars["range_object"].Interior.Pattern = 1  # xlSolid
		self.vars["range_object"].Interior.PatternColorlndex = 1  # xlAutomatic
		self.vars["range_object"].Interior.ThemeColor = 12  # xlThemeColorDark1
		self.vars["range_object"].Interior.TintAndShade = -0.249977111117893
		self.vars["range_object"].Interior.PatternTintAndShade = 0
		return self.vars["range_color"]

	def set_pen_color_style_thickness(self, scolor="bla", style="", thickness=5):
		"""
		여러곳에 사용하기위해 공통변수에 색, 모양, 두께를 설정하는 것

		:param scolor:
		:param style:
		:param thickness:
		"""

		self.pen_color = self.color.change_scolor_to_rgbint(scolor)
		self.pen_style = style
		self.pen_thickness = thickness

	def set_pen_color_style_thickness_for_object(self, target_drawing="", scolor="bla", style=4, thickness=5):
		"""
		도형객체의 색, 모양, 두께를 설정하는 것

		:param target_drawing: 도형객체
		:param scolor:
		:param style:
		:param thickness:
		"""
		target_drawing.DashStyle = style
		target_drawing.ForeColor.RGB = self.color.change_scolor_to_rgbint(scolor)
		target_drawing.Weight = thickness

	def set_pen_end_style(self, length=2, style=1, width=2):
		"""

		:param length: 길이
		:param style:
		:param width:
		"""
		self.end_point_length = length  # 2-default, 3-long, 1-short
		self.end_point_style = style  # 1-없음,2-삼각형,3-얇은화살촉,4-화살촉,5-다이아몬드,6-둥근
		self.end_point_width = width  # 2-default, 3-넓은, 1-좁은

	def set_pen_end_style_for_object(self, target_drawing="", length=2, style=1, width=2):
		"""
		도형객체의 끝모양을 설정하는 것

		:param target_drawing: 도형객체
		:param length: 길이
		:param style:
		:param width:
		"""
		target_drawing.EndArrowheadLength = length  # 2-default, 3-long, 1-short
		target_drawing.EndArrowheadstyle = style  # 1-없음,2-삼각형 ,3-얇은화살촉,4-화살촉,5-다이아몬드,6-둥근
		target_drawing.EndArrowheadwidth = width  # 2-default, 3-넓은, 1-좁은

	def set_pen_start_style(self, length=2, style=1, width=2):
		"""
		도형객체에 모두 사용하기위해 시작모양을 설정하는 것

		:param length: 길이
		:param style:
		:param width:
		"""
		self.start_point_length = length  # 2-default, 3-long, 1-short
		self.start_point_style = style  # 1-없음,2-삼각형,3-얇은화살촉,4-화살촉,5-다이아몬드,6-둥근
		self.start_point_width = width  # 2-default, 3-넓은, 1-좁은

	def set_pen_start_style_for_object(self, target_drawing="", length=2, style=1, width=2):
		"""
		도형객체의 시작모양을 설정하는 것

		:param target_drawing: 도형객체
		:param length: 길이
		:param style:
		:param width:
		"""
		target_drawing.BeginArrowheadlength = length  # 2-default, 3-long, 1-short
		target_drawing.BeginArrowheadstyle = style  # 1-없음,2-삼각형,3-얇은화살촉,4-화살촉,5-다이아몬드,6-둥근
		target_drawing.BeginArrowheadwidth = width  # 2-default, 3-넓은, 1-좁은

	def set_picture_in_cell(self, sheet_name, xy, full_path):
		"""
		보관용
		"""
		self.insert_image_in_xyxy(sheet_name, xy, full_path)

	def set_print_area(self, sheet_name, area, fit_wide=1):
		"""
		프린트영역을 설정

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param area:
		:param fit_wide:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		new_area = self.change_xyxy_to_r1c1(area)
		sheet_object.PageSetup.PrintArea = new_area

		sheet_object.PageSetup.Orientation = 1
		sheet_object.PageSetup.Zoom = False
		sheet_object.PageSetup.FitToPagesTall = False
		sheet_object.PageSetup.FitToPagesWide = fit_wide

	def set_print_page(self, sheet_name, input_list_2d, line_list, start_xy, size_xy, y_line, position):
		"""
		input_ list_2d, 2차원의 기본자료들
		line list = [1,2,3], 각 라인에서 출력이 될 자료
		start_ xy = [1,1], 첫번째로 시작될 자료의 위치
		size_xy = [7,9], 하나가 출력되는 영역의 크기
		y_line = 2, 한페이지에 몇줄을 출력할것인지
		position = [1,31,[4,5],[7,9]], 한줄의 출력되는 위치, line_ list의 갯수와 같아야 한다
		1) 2차원의 자료에서 출력하는 자료들만 순서대로 골라서 새로 만드는 것
		"""
		input_list_2d = self.change_xylist_to_list(input_list_2d)
		line_list = self.change_xylist_to_list(line_list)

		changed_list_2d = self.pick_ylines_at_list_2d(input_list_2d, line_list)  # 1
		new_start_x = start_xy[0]
		new_start_y = start_xy[1]
		for index, list_1d in enumerate(changed_list_2d):
			mok, namuji = divmod(index, y_line)
			new_start_x = new_start_x + mok * size_xy[0]
			new_start_y = new_start_y + namuji * size_xy[1]
			for index_2, one_value in enumerate(list_1d):
				self.write_value_in_cell(sheet_name, [position[index_2][0], position[index_2][1]], list_1d[index_2])

	def set_print_page_01(self, sheet_name, **var_dic):
		"""
		좀더 사용하기 쉽도록 변경이 필요

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param var_dic:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		sheet_object.PageSetup.Zoom = False
		sheet_object.PageSetup.FitToPagesTall = 1
		sheet_object.PageSetup.FitToPagesWide = 1
		# sheet_object.PageSetup.PrintArea = print_area
		sheet_object.PageSetup.LeftMargin = 25
		sheet_object.PageSetup.RightMargin = 25
		sheet_object.PageSetup.TopMargin = 50
		sheet_object.PageSetup.BottomMargin = 50
		# sheet_object.ExportAsFixedFormat(0, path_to_pdf)
		sheet_object.PageSetup.LeftFooter = "&D"  # 날짜
		sheet_object.PageSetup.LeftHeader = "&T"  # 시간
		sheet_object.PageSetup.CenterHeader = "&F"  # 화일명
		sheet_object.PageSetup.CenterFooter = "&N/&P"  # 현 page/ 총 page
		sheet_object.PageSetup.RightHeader = "&Z"  # 화일 경로
		sheet_object.PageSetup.RightFooter = "&P+33"  # 현재 페이지 + 33

	def set_print_preview(self, sheet):
		"""
		미리보기기능입니다

		:param sheet:
		:return:
		"""
		sheet_object = self.xlBook.Worksheets(sheet)
		sheet_object.PrintPreview()

	def set_range_name_for_range(self, sheet_name, xyxy, input_name):
		"""
		영역을 이름으로 설정
		"""
		range_object = self.get_range_object_by_xyxy(sheet_name, xyxy)

		self.xlbook.Names.Add(input_name, range_object)

	def set_ratio_for_shape(self, sheet_name, shape_name, wh_connect=True):
		"""
		사진의 비율변경을 해제하거나 설정하는 목적
		Selection.ShapeRange.LockAspectRatio = msoTrue

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param shape_name:
		:param wh_connect:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		shape_object = sheet_object.Shapes(shape_name)
		shape_object.LockAspectRatio = wh_connect

	def set_screen_update_off(self):
		"""
		화면 변화를 잠시 멈추는것
		"""
		self.xlapp.ScreenUpdating = False

	def set_screen_update_on(self):
		"""
		화면 변화를 시작
		"""
		self.xlapp.ScreenUpdating = True

	def set_style(self, sheet_name, xyxy, **arg):
		"""
		set_style("", [1,1,5,5], bold=True, color=[23,23,23], fontcolor=[2,220,24], numberformat="xxxx-mm-dd", size=17)
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		range_object = self.get_range_object_by_xyxy(sheet_name, xyxy)

		if "bold" in arg.keys():
			range_object.Font.Bold = arg["bold"]
		if "fontcolor" in arg.keys():
			range_object.Font.Color = int(arg["fontcolor"][0]) + int(arg["fontcolor"][1]) * 256 + int(
				arg["fontcolor"][2]) * 256 * 256
		if "numberformat" in arg.keys():
			range_object.NumberFormatLocal = arg["numberformat"]
		if "size" in arg.keys():
			range_object.Font.Size = arg["size"]
		if "color" in arg.keys():
			range_object.Interior.Color = int(arg["color"][0]) + int(arg["color"][1]) * 256 + int(
				arg["color"][2]) * 256 * 256

	def set_visible_for_sheet(self, value=0):
		"""
		실행되어있는 엑셀을 화면에 보이지 않도록 설정합니다
		기본설정은 보이는 것으로 되너 있읍니다
		"""
		self.xlapp.Visible = value

	def set_visible_for_workbook(self, true_or_false=1):
		"""
		실행되어있는 엑셀을 화면에 보이지 않도록 설정합니다
		기본설정은 보이는 것으로 되너 있읍니다

		:param value:
		"""
		self.xlapp.Visible = true_or_false

	def set_width_for_yline(self, sheet_name, y, height=13.5):
		"""
		가로열의 높이를 설정하는 것이다
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		new_y = self.check_xy_address(y)
		range_object = sheet_object.Range(sheet_object.Cells(new_y[0], 1), sheet_object.Cells(new_y[1], 5))
		range_object.EntireRow.RowHeight = height

	def set_width_for_yyline(self, sheet_name, xyxy, width=13.5):
		"""
		가로길이를 설정하는 것
		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		:param width:
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		range_object = self.get_range_object_by_xyxy(sheet_name, xyxy)

		range_object.ColumnWidth = width

	def set_width_in_yyline(self, sheet_name, yy, width=5):
		"""
		** 보관용
		가로줄의 넓이를 설정

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param yy: 세로줄의 사작과 끝 => [3,7]
		:param width:
		"""
		self.sheet_object = self.check_sheet_name(sheet_name)
		range_object = self.sheet_object.Range(self.sheet_object.Cells(1, yy[0]), self.sheet_object.Cells(1, yy[1]))
		range_object.ColumnWidth = width

	def set_wrap_for_range(self, sheet_name, xyxy, input_value):
		"""
		셀안의 값이 여러줄일때 줄바꿈이 되도록 설정하는 것

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		:param input_value:
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		range_object = self.get_range_object_by_xyxy(sheet_name, xyxy)

		range_object.WrapText = input_value

	def setup_bgcolor_in_chart(self, input_chart_obj, chart_area_bg="", plot_area_bg=""):
		"""
		차트의 배경색을 칠하는 것

		:param input_chart_obj:
		:param chart_area_bg:
		:param plot_area_bg:
		:return:
		"""
		input_chart_obj.ChartArea.Format.Fill.Visible = False
		input_chart_obj.PlotArea.Format.Fill.Visible = False

	def setup_font(self, input_list):
		"""
		기존적인 폰트의 설정
		["진하게", 12, "red50", "밑줄"] 이런형식으로 들어오면 알아서 값이 되는 것이다
		"""
		if self.vars["font"]:
			# 하위값이 있으면, 기존의것을 사용하고, 아무것도 없으면 기본값으로 설정한다
			pass
		else:
			self.setup_font_basic()

		for one in input_list:
			if one in ["진하게", "굵게", "찐하게", "bold"]: self.vars["font"]["bold"] = True
			if one in ["italic", "이태리", "이태리체", "기울기"]: self.vars["font"]["italic"] = True
			if one in ["strikethrough", "취소선", "통과선", "strike"]: self.vars["font"]["strikethrough"] = True
			if one in ["subscript", "하위첨자", "밑첨자"]: self.vars["font"]["subscript"] = True
			if one in ["superscript", "위첨자", "웃첨자"]: self.vars["font"]["superscript"] = True
			if one in ["underline", "밑줄"]: self.vars["font"]["underline"] = True
			if one in ["vertical", "수직", "가운데"]: self.vars["font"]["align_v"] = 3
			if one in ["horizental", "수평", "중간"]: self.vars["font"]["align_h"] = 2

		try:
			self.vars["font"]["size"] = int(one)
		except:
			pass

		try:
			result = self.xyre.search_all_by_jf_sql("[한글&영어:1~]", one)
			if result:
				if result[0][0] in self.vars["check_color_name"]:
					self.vars["font"]["rgb_int"] = self.color.change_scolor_to_rgbint(one)
		except:
			pass
		result = copy.deepcopy(self.vars["font"])

		return result

	def setup_font_basic(self):
		"""
		1. 기본자료를 만든다
		"""
		# 기본값을 만들고, 다음에 이것을 실행하면 다시 기본값으로 돌아온다

		# 폰트 설정의 모든것을 초기화 하는것
		# self.vars["font"]["background"] = None
		# self.vars["font"]["colorindex"] = 1
		# self.vars["font"]["creator"] = None
		# self.vars["font"]["style"] = None
		# self.vars["font"]["themecolor"] = None
		# self.vars["font"]["themefont"] = None
		# self.vars["font"]["tintandshade"] = None
		self.vars["font"]["bold"] = False
		self.vars["font"]["color"] = "bla"
		self.vars["font"]["italic"] = False
		self.vars["font"]["name"] = "Arial"
		self.vars["font"]["size"] = 12
		self.vars["font"]["strikethrough"] = False
		self.vars["font"]["subscript"] = False
		self.vars["font"]["superscript"] = False
		self.vars["font"]["alpha"] = False  # tintandshade를 이해하기 쉽게 사용하는 목적
		self.vars["font"]["underline"] = False
		self.vars["font"]["align_v"] = 3  # middle =3, top = 1, bottom = 4, default=2
		self.vars["font"]["align_h"] = 1  # None =1, center=2, left=1, default=1
		self.vars["font"]["color"] = 1

	def setup_gradation_for_color_n_position(self, in_style, in_object, bg_scolor, in_list_2d):
		"""
		여러 가지색을 정하면서, 색의 가장 진한 위치를 0~100 사이에서 정하는 것
		self.setup _gradation_for_ color_n_position("hor", aaa, "blu++", ["red++++", 0])

		:param in_style:
		:param in_object:
		:param bg_scolor:
		:param in_list_2d:
		:return:
		"""
		style_dic = {"ver": 2, "hor": 1, "corner": 5, "center": 7, "down": 4, "up": 3, "mix": -2}
		in_object.Fill.ForeColor.RGB = self.color.change_scolor_to_rgbint(bg_scolor)
		obj_fill = in_object.Fill
		obj_fill.OneColorGradient(style_dic[in_style], 1, 1)
		for index, list_1d in enumerate(in_list_2d):
			rgbint = self.color.change_scolor_to_rgbint(list_1d[0])
			obj_fill.GradientStops.Insert(rgbint, list_1d[1] / 100)

	def setup_gridline_in_chart(self, input_chart_obj, major_onoff, minor_onoff):
		"""
		차트의 그리드라인을 설정하는 것

		:param input_chart_obj:
		:param major_onoff:
		:param minor_onoff:
		:return:
		"""
		input_chart_obj.Axes(2).MajorGridlines.Delete()
		input_chart_obj.Axes(2).MinorGridlines.Delete()

	def setup_legend_for_chart(self, input_chart_obj, lrtb="top"):
		"""
		차트의 범례에대한 속성을 설정

		:param input_chart_obj:
		:param lrtb:
		:return:
		"""
		lrtb_dic = {"left": 103, "right": 101, "top": 102, "bottom": 104}
		input_chart_obj.SetElement(lrtb_dic[lrtb])

	def setup_print_header(self, sheet_name, position, input_value=""):
		"""
		입력한 값들을 엑셀에서 사용하는 형식으로 변경하는 것
		:param sheet_name:
		:param position:
		:param input_value:
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		temp_dic = {"화일명": "&F", "시간": "&T", "경로": "&Z", "현재페이지": "&N", "총페이지": "&P", "날짜": "&D"}
		for one in temp_dic.keys():
			input_value = input_value.replace(one, temp_dic[one])

		if position == "left":
			sheet_object.PageSetup.LeftHeader = input_value
		elif position == "center":
			sheet_object.PageSetup.CenterHeader = input_value
		elif position == "right":
			sheet_object.PageSetup.RightHeader = input_value

	def setup_x_scale_for_chart(self, chart_obj, min_scale="", max_scale=""):
		"""
		차트의 속성을 설정 : x_scale

		:param chart_obj:
		:param min_scale:
		:param max_scale:
		:return:
		"""
		temp = chart_obj.Axes(1)
		temp.MinimumScale = min_scale
		temp.MaximumScale = max_scale

	def setup_x_title_for_chart(self, chart_obj, xtitle="", size="", color="", bold=""):
		"""
		차트의 속성을 설정 : x_title

		:param chart_obj:
		:param xtitle:
		:param size:
		:param color:
		:param bold:
		:return:
		"""
		temp = chart_obj.Axes(1)  # 1 : xlCategory, 3 :xlSeriesAxis, 2 : xlValue, 1: primary, 2 : secondary
		temp.HasTitle = True
		temp.AxisTitle.Text = xtitle
		temp.AxisTitle.Format.TextFrame2.TextRange.Font.Fill.ForeColor.RGB = self.color.change_scolor_to_rgbint("red")
		temp.AxisTitle.Format.TextFrame2.TextRange.Font.Bold = True
		temp.AxisTitle.Format.TextFrame2.TextRange.Font.Size = 20

	def setup_y_scale_for_chart(self, chart_obj, min_scale="", max_scale=""):
		"""
		차트의 속성을 설정 : y_scale

		:param chart_obj:
		:param min_scale:
		:param max_scale:
		:return:
		"""
		temp = chart_obj.Axes(2)
		temp.MinimumScale = min_scale
		temp.MaximumScale = max_scale

	def setup_y_title_for_chart(self, chart_obj, xtitle, size="", color="", bold=""):
		"""
		차트의 속성을 설정 : y_title

		:param chart_obj:
		:param xtitle:
		:param size:
		:param color:
		:param bold:
		:return:
		"""
		temp = chart_obj.Axes(2)  # 1: xlCategory, 3 :xlSeriesAxis, 2 : xlValue, 1: primary, 2 : secondary
		temp.HasTitle = True
		temp.AxisTitle.Text = xtitle
		temp.AxisTitle.Format.TextFrame2.TextRange.Font.Fill.ForeColor.RGB = self.color.change_scolor_to_rgbint("red")
		temp.AxisTitle.Format.TextFrame2.TextRange.Font.Bold = True
		temp.AxisTitle.Format.TextFrame2.TextRange.Font.Size = 20

	def sort_2_excel_files_001(self):
		"""
		두개시트의 자료를 기준으로 정렬한다선택한
		단 두개의 자료는 각각 정렬이되어있어야 한다
		빈칸은 없어야 한다

		"""
		# 1. 두개의 시트의 첫번째 열을 읽어온다
		sheet_names = self.read_all_sheet_name()

		# 첫번째 시트의 첫번째 행의 자료를 갖고오는 것이다
		sheet1_name = sheet_names[0]
		# sheet1_usedrange = self.read_address_for_usedrange(sheet1_name)
		y_start, x_start, y_end, x_end = self.read_address_for_usedrange(sheet1_name)
		datas1 = self.read_range_value(sheet1_name, [1, x_start, 1, x_end])

		# 두번째 시트의 첫번째 행의 자료를 갖고오는 것이다
		sheet2_name = sheet_names[1]
		# sheet2_usedrange = self.read_address_for_usedrange(sheet2_name)
		y_start, x_start, y_end, x_end = self.read_address_for_usedrange(sheet2_name)
		datas2 = self.read_range_value(sheet2_name, [1, x_start, 1, x_end])

		# 첫번째것과 두번째것을 비교하여 컬럼을 추가한다
		all_dic = {}
		for data1 in datas1:
			if data1[0] in all_dic:
				all_dic[data1[0]] = all_dic[data1[0]] + 1
			else:
				all_dic[data1[0]] = 1

		for data2 in datas2:
			if data2[0] in all_dic:
				all_dic[data2[0]] = all_dic[data2[0]] + 1
			else:
				all_dic[data2[0]] = 1

		# 각각 시트를 돌아가며 칸을 넣는다
		# 딕셔너리의 키를 리스트로 만든다
		all_dic_list = list(all_dic.keys())

		try:
			all_dic_list.remove(None)
		except:
			pass

		all_dic_list_sorted = sorted(all_dic_list)

		# 딕셔너리의 값들을 리스트로 만들어서 값을 만든다
		all_dic_values_list = list(all_dic.values())
		temp_1 = 0
		for one in all_dic_values_list:
			temp_1 = temp_1 + int(one)

		# 첫번째 시트를 맞도록 칸을 넣는다
		temp_2 = []
		for one in all_dic_list_sorted:
			for two in range(int(all_dic.get(one))):
				temp_2.append(one)

		temp_3 = 0
		for one in range(len(temp_2)):
			try:
				if temp_2[one] == datas1[temp_3][0]:
					temp_3 = temp_3 + 1
				else:
					self.insert_xxline(sheet1_name, one + 1)
			except:
				self.insert_xxline(sheet1_name, one + 1)

		temp_4 = 0
		for one in range(len(temp_2)):
			try:
				if temp_2[one] == datas2[temp_4][0]:
					temp_4 = temp_4 + 1
				else:
					self.insert_xxline(sheet2_name, one + 1)
			except:
				self.insert_xxline(sheet2_name, one + 1)

	def sort_file_두개의화일을_같게_정렬하기_001(self, ):
		"""
		sort_file_두개의화일을_같게_정렬하기_001()
		두개시트의 자료를 기준으로 정렬한다선택한
		단 두개의 자료는 각각 정렬이되어있어야 한다
		빈칸은 없어야 한다
		"""

		# 1. 두개의 시트의 첫번째 열을 읽어온다
		# excel = self.myez_xl.jcell("activeworkbook")
		sheet_names = self.read_sheet_names()

		# 첫번째 시트의 첫번째 행의 자료를 갖고오는 것이다
		sheet1_name = sheet_names[0]
		sheet1_usedrange = self.read_range_usedrange(sheet1_name)
		y_start, x_start, y_end, x_end = self.change_address_type(sheet1_usedrange[2])[1]
		datas1 = self.read_range_value(sheet1_name, [1, x_start, 1, x_end])

		# 두번째 시트의 첫번째 행의 자료를 갖고오는 것이다
		sheet2_name = sheet_names[1]
		sheet2_usedrange = self.read_range_usedrange(sheet2_name)
		y_start, x_start, y_end, x_end = self.change_address_type(sheet2_usedrange[2])[1]
		datas2 = self.read_range_value(sheet2_name, [1, x_start, 1, x_end])

		# 첫번째것과 두번째것을 비교하여 컬럼을 추가한다
		all_dic = {}
		for data1 in datas1:
			if data1[0] in all_dic:
				all_dic[data1[0]] = all_dic[data1[0]] + 1
			else:
				all_dic[data1[0]] = 1

		for data2 in datas2:
			if data2[0] in all_dic:
				all_dic[data2[0]] = all_dic[data2[0]] + 1
			else:
				all_dic[data2[0]] = 1

		# 각각 시트를 돌아가며 칸을 넣는다
		# 딕셔너리의 키를 리스트로 만든다
		all_dic_list = list(all_dic.keys())

		try:
			all_dic_list.remove(None)
		except:
			pass

		all_dic_list_sorted = sorted(all_dic_list)
		# print (all_dic_list_sorted)

		# 딕셔너리의 값들을 리스트로 만들어서 값을 만든다
		all_dic_values_list = list(all_dic.values())
		# print (all_dic_values_list)
		temp_1 = 0
		for one in all_dic_values_list:
			temp_1 = temp_1 + int(one)
		# print (temp_1)

		# 첫번째 시트를 맞도록 칸을 넣는다
		temp_2 = []
		for one in all_dic_list_sorted:
			#  print (one)
			for two in range(int(all_dic.get(one))):
				temp_2.append(one)

		temp_3 = 0
		for one in range(len(temp_2)):
			# print(temp_2[one], datas1[temp_3][0])
			try:
				if temp_2[one] == datas1[temp_3][0]:
					temp_3 = temp_3 + 1
				else:
					self.insert_range_line(sheet1_name, one + 1)
			except:
				self.insert_range_line(sheet1_name, one + 1)

		temp_4 = 0
		for one in range(len(temp_2)):
			try:
				if temp_2[one] == datas2[temp_4][0]:
					temp_4 = temp_4 + 1
				else:
					self.insert_range_line(sheet2_name, one + 1)
			except:
				self.insert_range_line(sheet2_name, one + 1)

	def sort_with_two_range(self, sheet_name, xyxy1, xyxy2):
		"""
		두가지 영역을 정렬 하는 것

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy1:
		:param xyxy2:
		"""
		list_2d_1 = self.read_value_in_range(sheet_name, xyxy1)
		list_2d_2 = self.read_value_in_range(sheet_name, xyxy2)
		list_2d_3 = list(list_2d_2)
		self.new_sheet()
		line = 1
		len_width = len(list_2d_1[0])
		total_line_no = 1
		current_x = 0

		for index, one in enumerate(list_2d_1):
			current_x = current_x + 1
			self.write_value_in_range("", [current_x, 1], one)
			temp = 0
			for index2, one_2 in enumerate(list_2d_2):
				if one[0] == one_2[0] and (one[0] != "" or one[0] != None):
					temp = temp + 1
					if temp > 1:
						current_x = current_x + 1
					self.write_value_in_range("", [current_x, len_width + 1], one_2)
					list_2d_3[index2] = ["", ""]

		total_line_no = line + len(list_2d_1)
		for one in list_2d_3:
			if one[0] != "" and one[0] != None:
				current_x = current_x + 1
				self.write_value_in_range("", [current_x, len_width + 1], one)

	def split_all_list_2d_value_by_special_char(self, input_list_2d, split_char="_"):
		"""
		2차원자료안의 모든 값을 특정문자로 분리하는 기능

		:param input_list_2d:
		:param split_char:
		:return:
		"""
		result = []
		for ix, list_1d in enumerate(input_list_2d):
			temp = ""
			for iy, value in enumerate(list_1d):
				value = input_list_2d[ix][iy]
				# value = self.read_value_in_cell("", [ix + 1, iy + 1])
				if type(value) == type("abc"):
					splited_value = value.split(split_char)
					if type(splited_value) == type([]):
						result.append(splited_value)
					else:
						result.append([splited_value])
				else:
					result.append([value])
		return result

	def split_filename_to_path_n_file_name(self, filename=""):
		"""
		화일 이름을 경로와 이름으로 구분하는 것이다

		:param filename:
		:return:
		"""
		path = ""
		changed_filename = filename.replace("\\", "/")
		split_list = changed_filename.split("/")
		file_name_only = split_list[-1]
		if len(changed_filename) == len(file_name_only):
			path = ""
		else:
			path = changed_filename[:len(file_name_only)]

		return [path, file_name_only]

	def split_jf_sql_for_selection_with_new_sheet(self, jf_sql):
		"""
		발견한것을 기준으로 원래 값을 분리하는것

		:param jf_sql:
		:return:
		"""
		result = []
		xyxy = self.read_address_for_selection()
		for x in range(xyxy[0], xyxy[2] + 1):
			for y in range(xyxy[1], xyxy[3] + 1):
				value = self.read_value_in_cell("", [x, y])
				aaa = self.xyre.search_all_with_jf_sql(jf_sql, value)
				atemp = []
				if aaa:
					for num in range(len(aaa) - 1, -1, -1):
						one = aaa[num]
						no = one[2]
						temp = value[no:]
						value = value[:no]
						atemp.append(temp)
						atemp.insert(0, value)
				result.append(atemp)
		self.new_sheet()
		self.write_list_2d_from_cell("", [1, 1], result)

	def split_partial_value_in_range_by_step_from_start(self, sheet_name, xyxy, n_char):
		"""
		어떤 자료중에 앞에서 몇번째것들만 갖고오고 싶을때
		예:시군구 자료에서 앞의 2글자만 분리해서 얻어오는 코드

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		:param n_char:
		"""
		list_2d = self.read_value_in_range(sheet_name, xyxy)
		result = set()
		for list_1d in list_2d:
			for one in list_1d:
				try:
					result.add(one[0:n_char])
				except:
					pass
		return list(result)

	def split_range_as_head_body_tail(self, input_xyxy, head_height=1, tail_height=1):
		"""
		테이블 형식의 영역을 head, body, tail 로 구분하는 것

		:param input_xyxy:
		:param head_height:
		:param tail_height:
		:return:
		"""
		x1, y1, x2, y2 = self.check_address_value(input_xyxy)
		range_head = [x1, y1, x1 + head_height - 1, y2]
		range_body = [x1 + head_height, y1, x2 - tail_height, y2]
		range_tail = [x2 - tail_height - 1, y1, x2, y2]
		return [range_head, range_body, range_tail]

	def split_text_by_special_string(self, input_text):
		"""
		선택한 1줄의 영역에서 원하는 문자나 글자를 기준으로 분리할때
		2개의 세로행을 추가해서 결과값을 쓴다
		"""
		sheet_name = self.read_activesheet_name()
		rng_select = self.read_selection_address()
		rng_used = self.read_usedrange_address()
		[x1, y1, x2, y2] = self.intersect_range1_range2(rng_select, rng_used)
		self.insert_yy("", y1 + 1)
		self.insert_yy("", y1 + 1)
		result = []
		length = 2
		# 자료를 분리하여 리스트에 집어 넣는다
		for x in range(x1, x2 + 1):
			for y in range(y1, y2 + 1):
				cell_value = str(self.read_cell_value(sheet_name, [x, y]))
				list_data = cell_value.split(input_text)
				result.append(list_data)
		# 집어넣은 자료를 다시 새로운 세로줄에 넣는다
		for x_no in range(len(result)):
			if len(result[x_no]) > length:
				for a in range(len(result[x_no]) - length):
					self.insert_yy("", y1 + length)
				length = len(result[x_no])
			for y_no in range(len(result[x_no])):
				self.write_cell_value(sheet_name, [x1 + x_no, y1 + y_no + 1], result[x_no][y_no])

	def split_value_by_special_string(self, sheet_name, input_value):
		"""
		split_inputvalue_as_special_string( input_value):
		선택한 1줄의 영역에서 원하는 문자나 글자를 기준으로 분리할때
		2개의 세로행을 추가해서 결과값을 쓴다

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param input_value: 입력 text
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		rng_select = self.read_address_for_selection()
		rng_used = self.read_address_for_usedrange()
		[x1, y1, x2, y2] = self.get_intersect_address_with_range1_and_range2(rng_select, rng_used)
		self.insert_xline("", x1 + 1)
		self.insert_xline("", x1 + 1)
		result = []
		length = 2
		# 자료를 분리하여 리스트에 집어 넣는다
		for x in range(x1, x2 + 1):
			for y in range(y1, y2 + 1):
				one_value = sheet_object.Cells(x, y).Value2
				list_data = one_value.split(input_value)
				result.append(list_data)
		# 집어넣은 자료를 다시 새로운 세로줄에 넣는다
		for y_no in range(len(result)):
			if len(result[x_no]) > length:
				for a in range(len(result[x_no]) - length):
					self.insert_xline("", x1 + length)
				length = len(result[x_no])
			for x_no in range(len(result[x_no])):
				sheet_object.Cells(x1 + x_no, y1 + y_no + 1).Value = result[x_no][y_no]

	def split_xline_as_per_input_word_in_yline(self, sheet_name, xyxy, yline_index, input_value,
												first_line_is_title=True):
		"""
		선택한 영역에서 특정 y값이 입력값을 갖고있을때, 입력값들에 따라서 x라인들을 저장한후 돌려준다

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		:param yline_index:
		:param input_value:
		:param first_line_is_title:
		"""
		list_2d = self.read_value_in_range(sheet_name, xyxy)
		result = {"_main_data": []}
		for one_value in input_value:
			result[one_value] = []

		if first_line_is_title:
			for one_key in result.keys():
				result[one_key].append(list_2d[0])
			list_2d = list_2d[1:]

		for list_1d in list_2d:
			found = False
			for one_key in result.keys():
				if one_key in list_1d[int(yline_index)]:
					result[one_key].append(list_1d)
					found = True
			if found == False:
				result["_main_data"].append(list_1d)

		return result

	def split_value_to_special_string(self, sheet_name, input_text):
		"""
		split_inputvalue_as_special_string( input_text):
		선택한 1줄의 영역에서 원하는 문자나 글자를 기준으로 분리할때
		2개의 세로행을 추가해서 결과값을 쓴다
		Input Style :
		Output Style :
		"""
		self.menu_dic['split_inputvalue_as_special_string'] = {'표시여부': '필요',
																'그리드메뉴': ['split', 'as', '특정글자를 기준으로 자료 분리'],
																'실행메뉴': ['split', 'as', 'special_string']}
		sheet_object = self.check_sheet_name(sheet_name)
		rng_select = self.read_address_in_selection()
		rng_used = self.read_usedrange_address()
		[x1, y1, x2, y2] = self.intersect_range1_range2(rng_select, rng_used)
		self.insert_xline("", x1 + 1)
		self.insert_xline("", x1 + 1)
		result = []
		length = 2
		# 자료를 분리하여 리스트에 집어 넣는다
		for x in range(x1, x2 + 1):
			for y in range(y1, y2 + 1):
				cell_value = str(sheet_object.Cells(x, y).Value)
				list_data = cell_value.split(input_text)
				result.append(list_data)
		# 집어넣은 자료를 다시 새로운 세로줄에 넣는다
		for y_no in range(len(result)):
			if len(result[x_no]) > length:
				for a in range(len(result[x_no]) - length):
					self.insert_xline("", x1 + length)
				length = len(result[x_no])
			for x_no in range(len(result[x_no])):
				sheet_object.Cells(x1 + x_no, y1 + y_no + 1).Value = result[x_no][y_no]

	def statusbar(self, sheet, row_or_col):
		"""
		스테이터스바,  아직 미확인
		"""
		sheet_object = self.xlBook.Worksheets(sheet)
		sheet_object.Range(str(row_or_col) + ':' + str(row_or_col)).Insert(-4121)

	def switch_data(self):
		"""
		새로운 세로행을 만든후 그곳에 두열을 서로 하나씩 포개어서 값넣기
		a 1	==> a
		b 2		 1
					b
					2
		"""
		sheet_name = self.read_activesheet_name()
		[x1, y1, x2, y2] = self.read_address_for_selection()

		new_x = 1

		self.insert_yline("", 1)
		for x in range(x1, x2 + 1):
			for y in range(y1, y2 + 1):
				one_value = str(self.read_cell(sheet_name, [x, y + 1]))
				self.write_one_value(sheet_name, [new_x, 1], one_value)
				new_x = new_x + 1

	def switch_datas_01(self):
		"""
		# 새로운 세로행을 만든후 그곳에 두열을 서로 하나씩 포개어서 값넣기
		# a 1	==> a
		# b 2		1
		#			b
		#			2

		:return:
		"""
		sheet_name = self.read_activesheet_name()
		[x1, y1, x2, y2] = self.read_select_address()
		new_x = 1
		self.insert_y_line("", 1)
		for x in range(x1, x2 + 1):
			for y in range(y1, y2 + 1):
				cell_value = str(self.read_cell_value(sheet_name, [x, y + 1]))
				self.write_cell_value(sheet_name, [new_x, 1], cell_value)
				new_x = new_x + 1

	def terms(self):
		"""
		용어들에 대한 설명
		"""
		result = """
			add : 기존것에 추가하는 것
			insert : 새로운 뭔가를 만드는 것
			new : 어떤 객체를 하나 만들때 사용
		"""
		return result

	def unlock_for_sheet(self, sheet_name, password="1234"):
		"""
		시트 잠그기 해제
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		sheet_object.Unprotect(password)

	def unlock_sheet(self, sheet_name, password="1234"):
		""" 시트 보호를 설정 하는 것 """
		sheet_object = self.check_sheet_name(sheet_name)
		sheet_object.Unprotect(password)

	def get_merged_address_list_in_range(self, sheet_name="", xyxy=""):
		"""
		영역안에 병합된것이 잇으면, 병합된 주소를 리스트형태로 돌려준다

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		"""
		result = []
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)

		for x in range(x1, x2 + 1):
			for y in range(y1, y2 + 1):
				my_range = sheet_object.Cells(x, y)

				if my_range.MergeCells:
					my_range.Select()
					ddd = self.read_address_for_selection()
					if not ddd in result:
						result.append(ddd)
		return result


	def read_address_at_xy_for_multi_input_merged_area(self, start_xy, step_xy, num):
		"""

		:param start_xy:
		:param step_xy:
		:param num:
		:return:
		"""
		result = self.read_address_at_xy_for_multi_merged_area(start_xy, step_xy, num)
		return result

	def read_address_at_xy_for_multi_merged_area(self, start_xy, step_xy, num):
		"""
		다음번 셀의 주소틀 눙려주는것
		병합이된  셀이  동일하게  연속적으로  있다고  할때,  n번째의  셀  주소를  계산하는것

		:param start_xy:
		:param step_xy:
		:param num:
		:return:
		"""

		mok, namuji = divmod((num - 1), step_xy[1])
		new_x = mok * step_xy[0] + start_xy[0]

		new_y = namuji * step_xy[1] + start_xy[1] + 1
		return [new_x, new_y]

	def check_merge_status_at_cell(self, sheet_name, xy=""):
		result = self.is_cell_in_merge(sheet_name, xy)
		return result

	def is_cell_in_merge(self, sheet_name, xyxy=""):
		"""
		결과를 True / Flase로 나타내는 것
		현재 셀이 merge가 된것인지를 알아 내는것

		:param sheet_name:
		:param xyxy:
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		range_object = sheet_object.Cells(x1, y1)
		merge_count = range_object.MergeArea.Cells.Count
		result = False
		if merge_count > 1:
			merge_address = range_object.MergeArea.Address
			result = True
		return result

	def unmerge_for_range(self, sheet_name="", xyxy=""):
		"""
		병합된 것을 푸는 것이다
		"""
		range_object = self.get_range_object_by_xyxy(sheet_name, xyxy)
		range_object.UnMerge()

	def merge_each_xline_in_range(self, sheet_name="", xyxy=""):
		"""
		입력된 영역을 기준으로 	각 y라인을 병합하는 것
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		range_object = self.get_range_object_by_xyxy(sheet_name, xyxy)

		for x in range(x1, x2 + 1):
			self.merge_for_range("", [x, y1, x, y2])

	def merge_extend_for_xline(self):
		"""
		:return:
		"""
		x1, y1, x2, y2 = self.read_address_in_selection()
		for x in range(x1, x2 + 1):
			self.merge_for_range("", [x, y1, x, y2])


	def merge_for_range(self, sheet_name="", xyxy=""):
		"""
		셀들을 병합하는 것

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		"""
		range_object = self.get_range_object_by_xyxy(sheet_name, xyxy)
		range_object.Merge(0)


	def merge_for_selection(self):
		"""
		셀들을 병합하는 것
		"""
		range_object = self.xlapp.Selection
		range_object.Merge(0)

	def merge_for_xyxy(self, sheet_name="", xyxy=""):
		self.merge_for_range(sheet_name, xyxy)

	def merge_range(self, sheet_name="", xyxy=""):
		self.merge_for_range(sheet_name, xyxy)


	def merge_for_each_line_in_range(self, sheet_name="", xyxy=""):
		"""
		셀들을 합하는 것이다

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		range_object = self.get_range_object_by_xyxy(sheet_name, xyxy)

		if y1 == y2:
			range_object.Merge(0)
		else:
			for a in range(y2 - y1 + 1):
				sheet_object.Range(sheet_object.Cells(y1 + a, x1), sheet_object.Cells(y1 + a, x2)).Merge(0)


	def merge_top_2_ylines_in_range(self, sheet_name="", xyxy=""):
		self.merge_left_2_ylines_in_range(sheet_name, xyxy)

	def merge_top_2_xlines_in_range(self, sheet_name="", xyxy=""):  # 셀들을 합하는 것이다
		"""

		선택 영역중 바로 위의것과 아랫것만 병합하는것
		제일위의 2줄만 세로씩 병합하는 것이다
		가로줄 갯수만큰 병합하는것
		위와 아래에 값이 있으면 알람이 뜰것이다

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		range_object = self.get_range_object_by_xyxy(sheet_name, xyxy)

		if y1 == y2:
			pass
		else:
			for y in range(y1, y2 + 1):
				sheet_object.Range(sheet_object.Cells(x1, y), sheet_object.Cells(x1 + 1, y)).Merge(0)

	def merge_left_2_ylines_in_range(self, sheet_name="", xyxy=""):  # 셀들을 합하는 것이다
		"""
		선택 영역중 바로 위의것과 아랫것만 병합하는것
		왼쪽의 2줄을 병합하는 것이다

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		range_object = self.get_range_object_by_xyxy(sheet_name, xyxy)

		if x1 == x2:
			pass
		else:
			for x in range(x1, x2 + 1):
				sheet_object.Range(sheet_object.Cells(x, y1), sheet_object.Cells(x, y1 + 1)).Merge(0)



	def vlookup_for_multi_input(self, sheet_name, xyxy, search_no_list, search_value_list, find_no, option_all=True):
		"""
		여러 값이 같은 줄을 갖고오는 방법

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		:param search_no_list:
		:param search_value_list:
		:param find_no:
		:param option_all:
		"""
		result = []
		list_2d = self.read_value_in_range(sheet_name, xyxy)
		checked_no = len(search_value_list)

		for list_1d in list_2d:
			temp_no = 0
			for index, num in enumerate(search_no_list):
				if option_all:
					# 모든 값이 다 같을때
					if list_1d[num - 1] == search_value_list[index]:
						temp_no = temp_no + 1
					else:
						break
				else:
					# 값이 일부분일때도 OK
					if search_value_list[index] in list_1d[num - 1]:
						temp_no = temp_no + 1
					else:
						break
			if temp_no == checked_no:
				result = list_1d[find_no - 1]
		return result

	def vlookup_multi_yy_line(self, input_value1, input_value2):
		"""
		에제-엑셀) 여러항목이 같은 값의 원하는 것만 갖고오기
		여러항목이 같은 값의 원하는 것만 갖고오기
		 input_valuel = [자료의영역, 같은것이있는위치, 결과값의위치]
		"""

		input_value1 = self.change_xylist_to_list(input_value1)
		input_value2 = self.change_xylist_to_list(input_value2)

		base_data2d = self.read_value_in_range("", input_value1[0])
		compare_data2d = self.read_value_in_range("", input_value2[0])
		result = ""
		for one_data_1 in base_data2d:
			gijun = []
			one_data_1 = list(one_data_1)
			for no in input_value1[1]:
				gijun.append(one_data_1[no - 1])
			x = 0

			for value_1d in compare_data2d:
				value_1d = list(value_1d)
				x = x + 1
				bikyo = []

				for no in input_value2[1]:
					bikyo.append(value_1d[no - 1])

					if gijun == bikyo:
						result = one_data_1[input_value1[2] - 1]
						self.write_value_in_cell("", [x, input_value2[2]], result)

	def vlookup_with_multi_input_line(self, input_value1, input_value2):
		"""
		보통 vlookup은 한줄을 비교해서 다른 자료를 찾는데
		이것은 여러항목이 같은 값을 기준으로 원하는 것을 찾는 것이다
		input_valuel = [자료의영역, 같은것이있는위치, 결과값의위치]

		:param input_value1:
		:param input_value2:
		"""
		input_value1 = self.change_xylist_to_list(input_value1)
		input_value2 = self.change_xylist_to_list(input_value2)

		base_data2d = self.read_value_in_range("", input_value1[0])
		compare_data2d = self.read_value_in_range("", input_value2[0])
		result = ""
		for one_data_1 in base_data2d:
			gijun = []
			one_data_1 = list(one_data_1)
			for no in input_value1[1]:
				gijun.append(one_data_1[no - 1])
			x = 0

			for value_1d in compare_data2d:
				value_1d = list(value_1d)
				x = x + 1
				bikyo = []

				for no in input_value2[1]:
					bikyo.append(value_1d[no - 1])

				if gijun == bikyo:
					result = one_data_1[input_value1[2] - 1]
				self.write_value_in_cell("", [x, input_value2[2]], result)

	def vlookup_xyxy(self, sheet_name, find_xyxy, check_xyxy, find_value_option, find_value_oxy, write_value_oxy):
		"""
		vlookup을 위한것

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param find_xyxy:
		:param check_xyxy:
		:param find_value_option:
		:param find_value_oxy:
		:param write_value_oxy:
		"""
		original_list_2d = self.read_value_in_range(sheet_name, find_xyxy)
		dic_data = self.change_value_in_range_to_dic_with_xy_position(sheet_name, find_xyxy)

		list_2d = self.read_value_in_range(sheet_name, check_xyxy)

		for ix, list_1d in enumerate(list_2d):
			for iy, one_value in enumerate(list_1d):
				if one_value in dic_data.keys():
					find_x, find_y = dic_data[one_value][0]

				if find_value_option == "top":
					change_x = 0
					change_y = find_y - 1
				else:
					change_x = find_x - 1 + find_value_oxy[0]
					change_y = find_y - 1 + find_value_oxy[1]
				write_value = original_list_2d[change_x][change_y]
				write_x = check_xyxy[0] + write_value[0] + ix
				write_y = check_xyxy[1] + write_value[1] + iy
				self.write_value_in_cell("", [write_x, write_y], write_value)

	def write_cell(self, sheet_name, xyxy, input_value):
		"""
		많이 사용하는 것이라 짧게 만듦

		original : write_value_in_cell
		"""
		self.write_value_in_cell(sheet_name, xyxy, input_value)

	def write(self, sheet_name, xyxy, input_value):
		"""
		많이 사용하는 것이라 짧게 만듦

		original : write_value_in_cell
		"""
		self.write_value_in_cell(sheet_name, xyxy, input_value)

	def write_df_to_excel(self, sheet_name, df_obj, xyxy=[1, 1]):
		"""
		pandas의 dataframe의 자료를 커럼과 값을 기준으로 나누어서
		엑셀에 써넣는다
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		col_list = df_obj.columns.values.tolist()
		value_list = df_obj.values.tolist()
		self.write_range_value(sheet_name, xyxy, [col_list])
		self.dump_range_value(sheet_name, [xyxy[0] + 1, xyxy[1]], value_list)

	def write_dic_from_cell(self, sheet_name, xyxy, input_dic):
		"""
		사전자료를 한줄로 셀에 쓰는것
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		range_object = self.get_range_object_by_xyxy(sheet_name, xyxy)

		list_2d = list(input_dic.items())

		for x in range(0, len(list_2d)):
			sheet_object.Cells(x + x1, y1).Value = list_2d[x]

	def write_dic_key_in_cell(self, sheet_name, xyxy, input_dic):
		"""
		사전으로 입력된 키값을 엑셀에 쓰는것

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		:param input_dic:
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		range_object = self.get_range_object_by_xyxy(sheet_name, xyxy)

		list_1d = list(input_dic.keys())

		for x in range(0, len(list_1d)):
			sheet_object.Cells(x + x1, y1).Value = list_1d[x]

	def write_excel_function_in_cell(self, sheet_name, xy, input_fucntion, xyxy):
		"""
		셀에 엑셀의 함수를 입력해 주는 것

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xy: [가로번호, 세로번호]
		:param input_fucntion:
		:param xyxy:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		range = self.change_xyxy_to_r1c1(xyxy)
		x1, y1, x2, y2 = self.check_address_value(xy)
		result = "=" + input_fucntion + "(" + range + ")"
		sheet_object.Cells(x1, y1).Value = result

	def write_formula_in_range(self, sheet_name, xyxy, input_value="=Now()"):
		"""
		수식을 넣는 것

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		:param input_value: 입력자료
		"""
		range_object = self.get_range_object_by_xyxy(sheet_name, xyxy)
		range_object.Formula = input_value

	def write_hangul_cjj(self, letters="박상진", canvas_size=[50, 50], stary_xy=[1, 1]):
		"""
		# 입력받은 한글을 크기가 50 x 50의 엑셀 시트에 글씨를 색칠하여 나타내는 것이다
		"""

		# 기본 설정부분
		size_x = canvas_size[0]
		size_y = canvas_size[1]
		# 문자 하나의 기본크기
		# 기본문자는 10을 기준으로 만들었으며, 이것을 얼마만큼 크게 만들것인지 한글자의 배수를 정하는것
		h_mm = int(canvas_size[0] / 10)
		w_mm = int(canvas_size[1] / 10)
		# 시작위치
		h_start = stary_xy[0]
		w_start = stary_xy[1]

		check_han = re.compile("[ㄱ-ㅎ|ㅏ-ㅣ|가-힣]")
		for one_char in letters:
			# 한글을 초성, 중성, 종성으로 나누는 것이다
			if check_han.match(one_char):
				jamo123 = self.split_hangul_to_jamo(one_char)
				if jamo123[0][2] == "":
					# 가, 나, 다
					if jamo123[0][1] in ["ㅏ", "ㅐ", "ㅑ", "ㅒ", "ㅓ", "ㅔ", "ㅕ", "ㅖ", "ㅣ"]:
						# 기본설정은 시작점은 [1,1]이며, 캔버스의 크기는 [50, 50]인것이다

						start_xy = [1, 1]
						size = [10, 5]  # 위에서 배수를 5,5를 기본으로 해서 50x50되는 것이다
						# 자음의 시작점은 1,1이며, 크기는 50 x 25의 사이즈의 자음을 만드는 것이다
						self.draw_jaum_color(jamo123[0][0],
											 [h_start + h_mm * (start_xy[0] - 1), w_start + w_mm * (start_xy[1] - 1)],
											 [h_mm * size[0], w_mm * size[1]])
						# 모음의 시작점은 자음의 끝점에서 5를 이동한 1,30이며, 크기는 자음보다 가로의 크기를 좀 줄인
						# 50 x 20의 사이즈의 자음을 만드는 것이다

						start_xy = [1, 7]
						size = [10, 4]
						self.draw_moum_color(jamo123[0][1],
											 [h_start + h_mm * (start_xy[0] - 1), w_start + w_mm * (start_xy[1] - 1)],
											 [h_mm * size[0], w_mm * size[1]])

					# 구, 누, 루
					if jamo123[0][1] in ["ㅗ", "ㅛ", "ㅜ", "ㅡ"]:
						start_xy = [1, 1]
						size = [4, 10]
						self.draw_jaum_color(jamo123[0][0],
											 [h_start + h_mm * (start_xy[0] - 1), w_start + w_mm * (start_xy[1] - 1)],
											 [h_mm * size[0], w_mm * size[1]])
						start_xy = [6, 1]
						size = [5, 10]
						self.draw_moum_color(jamo123[0][1],
											 [h_start + h_mm * (start_xy[0] - 1), w_start + w_mm * (start_xy[1] - 1)],
											 [h_mm * size[0], w_mm * size[1]])

					# 와, 왜, 궈
					if jamo123[0][1] in ["ㅘ", "ㅙ", "ㅚ", "ㅝ", "ㅞ", "ㅟ", "ㅢ"]:
						# lists = self.div_mo2_mo1(jamo123[0][1])

						start_xy = [1, 1]
						size = [10, 5]
						self.draw_jaum_color(jamo123[0][0],
											 [h_start + h_mm * (start_xy[0] - 1), w_start + w_mm * (start_xy[1] - 1)],
											 [h_mm * size[0], w_mm * size[1]])
						start_xy = [8, 1]
						size = [3, 8]
						self.draw_moum_color(jamo123[0][1],
											 [h_start + h_mm * (start_xy[0] - 1), w_start + w_mm * (start_xy[1] - 1)],
											 [h_mm * size[0], w_mm * size[1]])
						start_xy = [1, 8]
						size = [6, 3]
						self.draw_moum_color(jamo123[0][1],
											 [h_start + h_mm * (start_xy[0] - 1), w_start + w_mm * (start_xy[1] - 1)],
											 [h_mm * size[0], w_mm * size[1]])

				if jamo123[0][2] != "":
					# 왕, 웍, 윔
					if jamo123[0][1] in ["ㅘ", "ㅙ", "ㅚ", "ㅝ", "ㅞ", "ㅟ", "ㅢ"]:
						hangul_type = "23자음+1332-2중모음+24자음"
						# lists = div_mo2_mo1(jamo123[0][1])

						start_xy = [1, 1]
						size = [4, 5]
						self.draw_jaum_color(jamo123[0][0],
											 [h_start + h_mm * (start_xy[0] - 1), w_start + w_mm * (start_xy[1] - 1)],
											 [h_mm * size[0], w_mm * size[1]])
						start_xy = [4, 1]
						size = [3, 7]
						self.draw_moum_color(jamo123[0][1],
											 [h_start + h_mm * (start_xy[0] - 1), w_start + w_mm * (start_xy[1] - 1)],
											 [h_mm * size[0], w_mm * size[1]])
						start_xy = [1, 7]
						size = [6, 3]
						self.draw_moum_color(jamo123[0][1],
											 [h_start + h_mm * (start_xy[0] - 1), w_start + w_mm * (start_xy[1] - 1)],
											 [h_mm * size[0], w_mm * size[1]])
						start_xy = [8, 1]
						size = [3, 6]
						self.draw_jaum_color(jamo123[0][0],
											 [h_start + h_mm * (start_xy[0] - 1), w_start + w_mm * (start_xy[1] - 1)],
											 [h_mm * size[0], w_mm * size[1]])

					# 앙, 양, 건
					if jamo123[0][1] in ["ㅏ", "ㅐ", "ㅑ", "ㅒ", "ㅓ", "ㅔ", "ㅕ", "ㅖ", "ㅣ"]:
						start_xy = [1, 1]
						size = [3, 5]
						self.draw_jaum_color(jamo123[0][0],
											 [h_start + h_mm * (start_xy[0] - 1), w_start + w_mm * (start_xy[1] - 1)],
											 [h_mm * size[0], w_mm * size[1]])
						start_xy = [1, 6]
						size = [5, 4]
						self.draw_moum_color(jamo123[0][1],
											 [h_start + h_mm * (start_xy[0] - 1), w_start + w_mm * (start_xy[1] - 1)],
											 [h_mm * size[0], w_mm * size[1]])
						start_xy = [7, 2]
						size = [3, 6]
						self.draw_jaum_color(jamo123[0][0],
											 [h_start + h_mm * (start_xy[0] - 1), w_start + w_mm * (start_xy[1] - 1)],
											 [h_mm * size[0], w_mm * size[1]])

					# 곡, 는
					if jamo123[0][1] in ["ㅗ", "ㅛ", "ㅜ", "ㅡ"]:
						start_xy = [1, 1]
						size = [3, 10]
						self.draw_jaum_color(jamo123[0][0],
											 [h_start + h_mm * (start_xy[0] - 1), w_start + w_mm * (start_xy[1] - 1)],
											 [h_mm * size[0], w_mm * size[1]])
						start_xy = [4, 1]
						size = [3, 10]
						self.draw_moum_color(jamo123[0][1],
											 [h_start + h_mm * (start_xy[0] - 1), w_start + w_mm * (start_xy[1] - 1)],
											 [h_mm * size[0], w_mm * size[1]])
						start_xy = [8, 1]
						size = [3, 10]
						self.draw_jaum_color(jamo123[0][0],
											 [h_start + h_mm * (start_xy[0] - 1), w_start + w_mm * (start_xy[1] - 1)],
											 [h_mm * size[0], w_mm * size[1]])

	def write_input_text_in_range_by_xy_step(self, sheet_name, xyxy, input_value="", xy_step=[1, 1]):
		"""
		선택한 영역의 시작점부터 x,y 번째 셀마다 값을 넣기

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		:param input_value: 입력 text
		:param xy_step: 가로, 세로번째만큼 반복하는 것
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		range_object = self.get_range_object_by_xyxy(sheet_name, xyxy)

		for x in range(x1, x2 + 1):
			if divmod(x, xy_step[0])[1] == 0:
				for y in range(y1, y2 + 1):
					if divmod(x, xy_step[1])[1] == 0:
						one_value = sheet_object.Cells(x, y).Value2
						if one_value == None:
							one_value = ""
						sheet_object.Cells(x, y).Value = one_value + str(input_value)

	def write_key_n_value_of_dic_in_range(self, sheet_name, xyxy, input_dic):
		"""
		사전으로 입력된 키값을 엑셀에 쓰는것

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		:param input_dic:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		range_object = self.get_range_object_by_xyxy(sheet_name, xyxy)

		list_2d = list(input_dic.items())

		for x in range(len(list_2d)):
			sheet_object.Cells(x + x1, y1).Value = list_2d[x][0]
			sheet_object.Cells(x + x1, y1 + 1).Value = list_2d[x][1]

	def write_list_1d_at_cell(self, sheet_name, xyxy, input_list_1d="입력 필요"):
		"""
		1차원자료를 시작셀을 기준으로 아래로 값을 넣는 것

		:param sheet_name:
		:param xyxy:
		:param input_list_1d:
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		range_object = self.get_range_object_by_xyxy(sheet_name, xyxy)

		self.r1c1 = self.change_xyxy_to_r1c1([x1, y1, x1, y1 + len(input_list_1d) - 1])
		sheet_object.Range(self.r1c1).Value = input_list_1d

	def write_list_1d_at_cell_as_group(self, sheet_name, xyxy, input_list_1d="입력 필요"):
		"""
		1차원자료를 시작셀을 기준으로 아래로 값을 넣는 것

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xy: [가로번호, 세로번호]
		:param input_list_1d: list type, 1차원 리스트형
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		range_object = self.get_range_object_by_xyxy(sheet_name, xyxy)

		for index, value in enumerate(input_list_1d):
			sheet_object.Cells(x1 + index, y1).Value = value

	def write_list_1d_at_cell_to_down(self, sheet_name, xyxy, input_list_1d="입력 필요"):
		"""
		1차원자료를 시작셀을 기준으로 아래로 값을 넣는 것

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xy: [가로번호, 세로번호]
		:param input_list_1d: list type, 1차원 리스트형
		:return:
		"""

		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		range_object = self.get_range_object_by_xyxy(sheet_name, xyxy)

		for index, value in enumerate(input_list_1d):
			sheet_object.Cells(x1 + index, y1).Value = value

	def write_list_1d_from_cell(self, sheet_name, xy, input_list_1d):
		"""
		1차원리스트의 값을
		특정셀에서부터 다 써주는 것이다

		:param sheet_name:
		:param xy:
		:param input_list_1d:
		:return:
		"""
		input_list_1d = self.change_xylist_to_list(input_list_1d)
		self.sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xy)

		self.sheet_object.Range(self.sheet_object.Cells(x1, y1),
								self.sheet_object.Cells(x1, y1 + len(input_list_1d) - 1)).Value = input_list_1d

	def write_list_1d_from_cell_as_step(self, sheet_name, xyxy, input_list_1d, input_step):
		"""
		1차원자료를 n개로 분리해서  2차원자료처럼 만든후 값을 쓰는 것

		:param sheet_name:
		:param xyxy:
		:param input_list_1d:
		:param input_step:
		:return:
		"""
		self.util.split_list_1d_by_step(input_list_1d, input_step)
		self.write_list_2d_from_cell(sheet_name, xyxy, input_list_1d)

	def write_list_1d_from_cell_as_yline(self, sheet_name, xyxy, input_list_1d=""):
		"""
		1차원자료를 세로줄로 써내려가는 것

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:param input_list_1d: list type, 1차원 리스트형
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		range_object = self.get_range_object_by_xyxy(sheet_name, xyxy)

		for x, value in enumerate(input_list_1d):
			sheet_object.Cells(x1 + x, y1).Value = input_list_1d[x]

	def write_list_1d_in_range(self, sheet_name, xyxy, input_list):
		"""
		예전것을 위해 남겨 두는 것
		"""
		input_list = self.change_xylist_to_list(input_list)
		self.write_list_in_range(sheet_name, xyxy, input_list)

	def write_list_1d_in_yline(self, sheet_name, xyxy, input_values="입력 필요"):
		"""
		아래의 예제는 엑셀의 값중에서 y라인으로 자동으로 한줄을 넣는 기능이 없어서, 만들어 보았다
		영역에 값는 넣기

		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:param input_values:
		:return:
		"""
		sheet_object = self.check_sheet_name("")
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		range_object = self.get_range_object_by_xyxy("", xyxy)

		for x in range(0, len(input_values)):
			sheet_object.Cells(x + x1, y1).Value = input_values[x]

	def write_list_1d_in_yline_speed_up(self, xyxy, input_list_1d="입력 필요"):
		"""
		아래의 예제는 엑셀의 값중에서 y라인으로 자동으로 한줄을 넣는 기능이 없어서, 만들어 보았다
		영역에 값는 넣기

		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:param input_list_1d:
		:return:
		"""
		sheet_object = self.check_sheet_name("")
		x1, y1, x2, y2 = self.check_address_value(xyxy)

		for x in range(0, len(input_list_1d)):
			sheet_object.Cells(x + x1, y1).Value = input_list_1d[x]

	def write_list_2d_from_cell(self, sheet_name, xyxy, input_list_2d=""):
		"""
		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		:param input_list_2d: 2차원의 리스트형 자료
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		range_object = self.get_range_object_by_xyxy(sheet_name, xyxy)

		self.set_screen_update_off()
		for x, list_1d in enumerate(input_list_2d):
			for y, value in enumerate(list_1d):
				sheet_object.Cells(x1 + x, y1 + y).Value = input_list_2d[x][y]
		self.set_screen_update_on()

	def write_list_2d_from_start_cell_by_mixed_types(self, sheet_name, xyxy, input_mixed=""):
		"""
		여러가지 자료가 쉬여있는 자료를 쓰는것
		아래의 자료를 쓰기위한것

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:param input_mixed:
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		range_object = self.get_range_object_by_xyxy(sheet_name, xyxy)

		for x, list_1d in enumerate(input_mixed):
			shift_y = 0
			for y, one_data in enumerate(list_1d):
				if type(one_data) == type("abc") or type(one_data) == type(1):
					# 문자나 숫자일때
					sheet_object.Cells(x1 + x, y1 + shift_y).Value = one_data
					shift_y = shift_y + 1
				elif type(one_data) == type([]) or type(one_data) == type((1)):
					# 리스트나 튜플일때
					for num, value in enumerate(one_data):
						sheet_object.Cells(x1 + x, y1 + shift_y).value = value
						shift_y = shift_y + 1
				elif type(one_data) == type(()):
					# 사전형식일때
					changed_list = list(one_data.items())
					for num, value in enumerate(changed_list):
						sheet_object.Cells(x1 + x, y1 + shift_y).value = value[0]
						shift_y = shift_y + 1
						sheet_object.cel1s(x1 + x, y1 + shift_y).value = value[1]
						shift_y = shift_y + 1

	def write_list_2d_in_range(self, sheet_name, xyxy, input_list):
		"""
		2차원 리스트의 값을 영역에 쓰는것
		갯수가 크면, 그게 더 우선 된다

		:param sheet_name:
		:param xyxy:
		:param input_list:
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		range_object = self.get_range_object_by_xyxy(sheet_name, xyxy)

		for index, list_1d in enumerate(input_list):
			count = len(list_1d)
			sheet_object.Range(sheet_object.Cells(x1 + index, y1),
								sheet_object.Cells(x1 + index, y1 + count - 1)).Value = list_1d

	def write_list_2d_in_range_by_xy_step(self, sheet_name, xyxy, input_list_2d="", xy_step=[1, 1]):
		"""
		입력으로 들어온 2차원값을 1개의 라인씩
		xy번째 마다 옮겨서 쓰는 것이다


		:param sheet_name:
		:param xyxy:
		:param input_list_2d:
		:param xy_step:
		:return:
		"""
		input_list_2d = self.change_xylist_to_list(input_list_2d)
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		range_object = self.get_range_object_by_xyxy(sheet_name, xyxy)

		for index, list_1d in enumerate(input_list_2d):
			self.write_list_1d_from_cell(sheet_name, [x1 + index * xy_step[0], y1 + index * xy_step[1]], list_1d)

	def write_list_in_range(self, sheet_name, xyxy, input_list):
		"""
		1차원의자료도 2차원으로 바꿔서, 값을 입력할 수 있다

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		:param input_list: list type
		"""
		# input_list = self.change_xylist_to_list(input_list)

		list_2d = self.util.change_any_data_type_to_list_2d(input_list)
		self.write_list_2d_in_range(sheet_name, xyxy, list_2d)

	def write_memo_in_cell(self, sheet_name, xyxy, text):
		"""
		셀에 메모를 넣는것

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		:param text:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		range_object = self.get_range_object_by_xyxy(sheet_name, xyxy)

		range_object.AddComment(text)

	def write_nansu_in_range(self, sheet_name, xyxy, input_list=[1, 100]):
		"""
		입력한 숫자범위에서 난수를 만들어서 영역에 써주는것

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		:param input_list: list type
		"""
		input_list = self.change_xylist_to_list(input_list)
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		range_object = self.get_range_object_by_xyxy(sheet_name, xyxy)

		no_start, no_end = input_list
		basic_data = list(range(no_start, no_end + 1))
		random.shuffle(basic_data)
		temp_no = 0
		for x in range(x1, x2 + 1):
			for y in range(y1, y2 + 1):
				self.write_cell_value(sheet_name, [x, y], basic_data[temp_no])
				if temp_no >= no_end - no_start:
					random.shuffle(basic_data)
					temp_no = 0
				else:
					temp_no = temp_no + 1

	def write_range(self, sheet_name, xyxy, input_list):
		"""
		1차원의자료도 2차원으로 바꿔서, 값을 입력할 수 있다

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		:param input_list: list type
		"""
		input_list = self.change_xylist_to_list(input_list)

		list_2d = self.util.change_any_data_type_to_list_2d(input_list)
		self.write_list_2d_in_range(sheet_name, xyxy, list_2d)

	def write_searched_value_at_special_position(self, xyxy, value_line_no, changed_value_line_no, result_line_no,
												 input_jf_sql):
		"""
		선택한 영역의 모든 셀의 값에대하여, 정규표현식으로 찾은 값을 나열하는 것
		1개의 라인만 적용을 해야 한다

		xyxy :영역
		value-line_no : 정규표현식을 적용할 y 라인
		changed_value_line-no : value_line_no의 값을 바꾼후의 값, False값이면 적용되지 않는다
		result_line_no : 찾은 값을 쓰는 첫번째 라인
		input_jf_sql : 적용할 정규표현식
		"""
		all_data = self.read_value_in_range("", xyxy)  # 1
		x1, y1, x2, y = self.check_address_value(xyxy)
		for index, list_1d in enumerate(all_data):
			current_x = x1 + index
			if list_1d:
				value = str(list_1d[value_line_no]).lower().strip()
				found = self.xyre.search_all_by_jf_sql(input_jf_sql, value)  # 정규표현식에 맞는 값을 확인
				# [[결과값, 시작순서, 끝순서, [그룹1, 그룹2...], match결과].....]
				if found:  # 만약 발견하면
					gijon = self.read_value_in_cell("", [current_x, result_line_no])
					changed_gijon = gijon + "," + list_1d[0] + ":" + str(list_1d[1]) + ":" + str(list_1d[2])
					if not changed_value_line_no:
						self.write_value_in_cell("", [current_x, result_line_no], changed_gijon)

	def write_serial_no(self, sheet_name, xyxy, start_no=1, step=1):
		"""
		숫자를 주면 시작점부터 아래로 숫자를 써내려가는것

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:param start_no:
		:param step: n번째마다 반복되는것
		:return:
		"""
		new_no = start_no
		for no in range(0, xyxy[2] - xyxy[0] + 1):
			self.write_value_in_cell(sheet_name, [xyxy[0] + no, xyxy[1]], new_no)
			new_no = new_no + step

	def write_serial_no_by_step_to_yline(self, xyxy, start_no=1, step=1):
		"""
		선택한 영역에 시작번호, 간격으로 이루어진 연속된 숫자를 쓰는것

		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		:param start_no:
		:param step: n번째마다 반복되는것
		"""
		new_no = start_no
		for no in range(0, xyxy[2] - xyxy[0] + 1):
			self.write_value_in_cell("", [xyxy[0] + no, xyxy[1]], new_no)
			new_no = new_no + step

	def write_serial_no_in_range_by_step(self, xyxy, start_no, step=1):
		"""
		선택한 영역에 시작번호, 간격으로 이루어진 연속된 숫자를 쓰는것
		"""
		new_no = start_no
		for no in range(0, xyxy[2] - xyxy[0] + 1):
			self.write_value_in_cell("", [xyxy[0] + no, xyxy[1]], new_no)
			new_no = new_no + step

	def write_serial_no_in_range_by_step_to_xline(self, xyxy, start_no=1, step=1):
		"""
		선택한 영역에 시작번호, 간격으로 이루어진 연속된 숫자를 쓰는것
		예 : 0,2,4,6,8....
		어떤경우는 필요할것 같아서, 만듦

		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		:param start_no:
		:param step: n번째마다 반복되는것
		"""
		new_no = start_no
		for no in range(0, xyxy[2] - xyxy[0] + 1):
			self.write_value_in_cell("", [xyxy[0], xyxy[1] + no], new_no)
			new_no = new_no + step

	def write_serial_no_in_range_by_step_to_yline(self, xyxy, start_no=1, step=1):
		"""
		선택한 영역에 시작번호, 간격으로 이루어진 연속된 숫자를 쓰는것

		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		:param start_no:
		:param step: n번째마다 반복되는것
		"""
		new_no = start_no
		for no in range(0, xyxy[2] - xyxy[0] + 1):
			self.write_value_in_cell("", [xyxy[0] + no, xyxy[1]], new_no)
			new_no = new_no + step

	def write_unique_value_in_range(self, sheet_name, xyxy):
		"""
		선택한 자료중에서 고유한 자료만을 골라내는 것이다
		1. 관련 자료를 읽어온다
		2. 자료중에서 고유한것을 찾아낸다
		3. 선택영역에 다시 쓴다
		"""
		temp_datas = self.read_value_in_range(sheet_name, xyxy)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		temp_result = []
		for one_list_data in temp_datas:
			for one_data in one_list_data:
				if one_data in temp_result or type(one_data) == type(None):
					pass
				else:
					temp_result.append(one_data)

		self.delete_value_in_range(sheet_name, xyxy)
		for num in range(len(temp_result)):
			mok, namuji = divmod(num, y2-y1 + 1)
			self.write_value_in_cell(sheet_name, [x1 + mok, y1 + namuji], temp_result[num])

	def write_uppercell_value_in_emptycell_in_range(self, sheet_name="", xyxy=""):
		"""
		빈셀을 위의것으로 채우는 것

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		"""
		self.sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		list_2d = self.read_value_in_range(sheet_name, xyxy)

		for y in range(len(list_2d[0])):
			old_value = ""
			for x in range(len(list_2d)):
				if list_2d[x][y] == "" or list_2d[x][y] == None:
					self.write_value_in_cell_with_sheet_object(self.sheet_object, [x + x1, y + y1], old_value)
				else:
					old_value = list_2d[x][y]

	def write_value_at_empty_cell_in_range_as_upper_cell(self, sheet_name="", xyxy=""):
		"""
		빈셀을 발견하면 바로위의 자료로 넣기
		채우기 : 빈셀 바로위의 것으로 채우기
		"""
		x1, y1, x2, y2 = self.check_address_value(xyxy)

		old_data = ""
		for y in range(y1, y2 + 1):
			for x in range(x1, x2 + 1):
				cell_value = self.read_cell_value(sheet_name, [x, y])
				if x == x1:
					# 만약 자료가 제일 처음이라면
					old_data = cell_value
				else:
					if cell_value == None:
						self.write_cell_value(sheet_name, [x, y], old_data)
					else:
						old_data = cell_value

	def write_value_at_end_of_column(self, sheet_name, base_xy, list_1d):
		"""
		** 보관용
		a3을 예로들어서, a3을 기준으로, 입력한 값이있는제일 마지막 가로줄번호를 갖고온후,
		그 다음줄에 값을 넣는것
		어떤 선택된 자료의 맨 마지막에 값을 넣기

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param base_xy:
		:param list_1d:
		"""
		list_1d = self.change_xylist_to_list(list_1d)

		self.move_activecell_in_range_to_bottom(sheet_name, base_xy)
		xy = self.read_address_for_activecell()
		self.write_value_in_range(sheet_name, [xy[0] + 1, xy[1]], list_1d)

	def write_searched_data_at_special_position(self, xyxy, value_line, changed_value_line, result_start_no,
												input_jf_sql):
		"""
		정규표현식으로 찾은 값을 특정위치에 쓰는것

		xyxy : 영역
		value_line : 정규표현식을 적용할 y 라인
		changed_value_line : value_line의 값을 바꾼후의 값, False값이면 적용되지 않는다
		result_start_no : 찾은값을 쓰는 첫번째 라인
		input_jf_sql : 적용할 정규표현식
		"""
		all_data = self.read_value_in_range("", xyxy)  # 1
		x1, y1, x2, y2 = self.check_address_value(xyxy)

		total_input_line_nos = 1
		self.insert_yline("", result_start_no)
		self.insert_yline("", result_start_no)

		for index, list_1d in enumerate(all_data):
			current_x = x1 + index
			if list_1d:
				value = str(list_1d[value_line]).lower().strip()
				found = self.xyre.search_all_by_jf_sql(input_jf_sql, value)  # 정규표현식에 맞는 값을 확인
				# [[결과값, 시작순서, 끝순서, [그룹1, 그룹2...], match결과].....]
				if found:  # 만약 발견하면
					if len(found) > total_input_line_nos:  # 3개씩 자리를 만드는 것
						for no in range((total_input_line_nos - len(found)) * 3):
							self.insert_yline("", result_start_no + (total_input_line_nos - 1) * 3)
						total_input_line_nos = len(found)
					next_no = 0
					for ino, list_1d in enumerate(found):
						next_no = next_no + 1
						self.write_value_in_cell("", [current_x, (next_no - 1) * 3 + 0], list_1d[0])
						self.write_value_in_cell("", [current_x, (next_no - 1) * 3 + 1], list_1d[1])
						self.write_value_in_cell("", [current_x, (next_no - 1) * 3 + 2], list_1d[2])
					value = value[0:list_1d[1]] + value[list_1d[2]:]
					if not changed_value_line:
						self.write_value_in_cell("", [current_x, changed_value_line], value)

	def write_value_in_activecell(self, input_value):
		"""
		활성화된 셀에 값을 쓰기
		"""
		xy = self.read_address_for_activecell()
		self.write_value_in_cell("", [xy[0], xy[1]], input_value)

	def write_value_in_cell(self, sheet_name, xyxy, value):
		"""
		셀에 값는 넣기

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		:param value: 입력값
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)

		# 문자형식의 숫자인지를 확인하는 것
		# 숫자와 문자가 모두 숫자형으로 인식하여서 첨가해야하는 것
		if type(value) == type("abc"):
			re_com = re.compile("^[0-9.]+$")
			check_type = re_com.search(value)
			if check_type != None:
				changed_value = "'" + value
			else:
				changed_value = value
		else:
			changed_value = value
		sheet_object.Cells(x1, y1).Value = changed_value

	def write_value_in_cell_as_linked(self, sheet_name, xy, web_site_address, tooltip=""):
		"""
		값을 쓰면서, 링크를 거는것

		:param sheet_name: 시트이름
		:param xy:
		:param web_site_address:
		:param tooltip:
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xy)

		sheet_object.Hyperlinks.Add(Anchor=sheet_object.Cells(x1, y1), Address=web_site_address, ScreenTip=tooltip)

	def write_value_in_cell_for_speed(self, xy, value):
		"""
		먼저 set_sheet함수를 이용해서 sheet를 설정하여야 한다
		문자형식의 숫자인지를 확인하는 것
		숫자와 문자가 모두 숫자형으로 인식하여서 첨가해야하는 것

		:param xy: [가로번호, 세로번호]
		:param value:
		:return:
		"""
		if type(value) == type("abc"):
			re_com = re.compile("^[0-9.]+$")
			check_type = re_com.search(value)
			if check_type != None:
				changed_value = "'" + value
			else:
				changed_value = value
		else:
			changed_value = value
		self.vars["sheet"].Cells(xy[0], xy[1]).Value = changed_value

	def write_value_in_cell_with_offset(self, sheet_name, base_xy, offset_xy, value):
		# offset 으로 값을 쓸수있도록 만든것
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(base_xy)
		sheet_object.Cells(x1 + offset_xy[0], y1 + offset_xy[1]).Select()
		sheet_object.Cells(x1 + offset_xy[0], y1 + offset_xy[1]).Value = value

	def write_value_in_cell_with_sheet_object(self, sheet_object, xy, value):
		"""
		속도를 높이는 목적으로 입력값이 제대로라고 가정한다

		:param sheet_object:
		:param xy:
		:param value:
		"""

		sheet_object.Cells(xy[0], xy[1]).Value = value

	def write_value_in_cell_with_sheet_object_for_speed(self, sheet_object, xy, value):
		"""
		속도를 높이는 목적으로 입력값이 제대로라고 가정한다

		:param sheet_name:
		:param xy:
		:param value:
		:return:
		"""
		if type(value) == type("abc"):
			re_com = re.compile("^[0-9.]+$")
			check_type = re_com.search(value)
			if check_type != None:
				changed_value = "'" + value
			else:
				changed_value = value
		else:
			changed_value = value
		sheet_object.Cells(xy[0], xy[1]).Value = changed_value

	def write_value_in_range(self, sheet_name, xyxy, input_any_type):
		"""
		영역에 값는 넣기 (기본은 값이 우선임)
		이것은 하나하나 입력이 되는 모습을 보여주며서, 실행되는 것이다

		1 : 모든자료를 2차원자료로 만들어 준다
		2 : 속도를 올리기위해 사용하는 것이며,

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		:param input_any_type:
		"""
		input_any_type = self.change_xylist_to_list(input_any_type)
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)

		checked_list_2d = self.util.change_any_data_type_to_list_2d(input_any_type)  # 1

		self.set_screen_update_off()  # 2
		for index, list_1d in enumerate(checked_list_2d):
			self.r1c1 = self.change_xyxy_to_r1c1([x1 + index, y1, x1 + index, y1 + len(list_1d) - 1])
			sheet_object.Range(self.r1c1).Value = list_1d
		self.set_screen_update_on()

	def write_value_in_range_as_dump(self, sheet_name, xyxy, input_values):
		"""
		보관용
		"""
		self.write_value_in_range_for_dump(sheet_name, xyxy, input_values)

	def write_value_in_range_as_speedy(self, sheet_name, xyxy, input_list_2d):
		"""
		보관용
		"""
		self.write_value_in_range_for_speed(sheet_name, xyxy, input_list_2d)

	def write_value_in_range_as_xy_step(self, sheet_name, xyxy, input_value, xy_step=[1, 1]):
		"""
		선택한 영역의 시작점부터 x,y 번째 셀마다 값을 넣기
		step : 간격을 두고 값을 쓸때 (예 : 현재 위치를 기준으로 가로로 2칸씩, 세로로 3칸씩 반복되는 위치에 쓸때)

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		:param input_value: 입력 text
		:param xy_step:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)

		for x in range(x1, x2 + 1):
			if divmod(x, xy_step[0])[1] == 0:
				for y in range(y1, y2 + 1):
					if divmod(y, xy_step[1])[1] == 0:
						sheet_object.Cells(x, y).Value = str(input_value)

	def write_value_in_range_by_range_priority(self, sheet_name, xyxy, input_value):
		"""
		선택한 영역의 갯수와 입력자료의 갯수가 틀릴때 => 영역안에서만 쓰기

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		:param input_value:
		:return:
		"""

		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		l2d = self.util.change_any_data_type_to_list_2d(input_value)

		for index, l1d in enumerate(l2d):
			if index >= x2 - x1 + 1:
				break
			else:
				if len(l1d) > y2 - y1 + 1:
					self.r1c1 = self.change_xyxy_to_r1c1([x1 + index, y1, x1 + index, y2])
					sheet_object.Range(self.r1c1).Value = l1d[:y2 - y1 + 1]
				else:
					self.r1c1 = self.change_xyxy_to_r1c1([x1 + index, y1, x1 + index, y1 + len(l1d) - 1])
					sheet_object.Range(self.r1c1).Value = l1d

	def write_value_in_range_by_reverse(self, sheet_name="", xyxy=""):
		"""
		입력자료의 xy를 yx로 바꿔서 입력하는 것

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		:param input_list_2d: 2차원의 리스트형 자료
		"""
		l2d = self.read_value_in_range("", xyxy)

		changed_l2d = []

		for y in range(len(l2d)):
			temp = []
			for x in range(len(l2d[0])):
				temp.append(l2d[x][y])
			changed_l2d.append(temp)

		self.write_list_2d_from_cell(sheet_name, [1, 1], changed_l2d)

	def write_value_in_range_by_value_priority(self, sheet_name, xyxy, input_any_type):
		"""
		선택한 영역의 갯수와 입력자료의 갯수가 틀릴때 => 입력자료의 갯수를 기준으로 모두 쓰기

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		:param input_any_type:
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		l2d = self.util.change_any_data_type_to_list_2d(input_any_type)

		for index, l1d in enumerate(l2d):
			self.r1c1 = self.change_xyxy_to_r1c1([x1 + index, y1, x1 + index, y1 + len(l1d) - 1])
			sheet_object.Range(self.r1c1).Value = l1d

	def write_value_in_range_except_none(self, sheet_name, xyxy, input_any_type):
		"""
		None으로 들어간 자리는 그냥 건너띄는 형식으로 자료를 입력한다
		즉, 자료를 변경하고싶지 않을때는 None으로 그위치에 넣으면, 기존의 값이 보존 된다

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		:param input_any_type:
		:return:
		"""

		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)

		list_2d = self.util.change_any_data_type_to_list_2d(input_any_type)

		self.set_screen_update_off()
		for ix, list_1d in enumerate(list_2d):
			for iy, one_value in enumerate(list_1d):
				if one_value != None:
					sheet_object.Cells(x1 + ix, y1 + iy).Value = one_value
		self.set_screen_update_on()

	def write_value_in_range_for_dump(self, sheet_name, xyxy, input_values):
		"""
		한꺼번에 값을 써넣을때 사용

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		:param input_values:
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)

		sheet_object.Range(sheet_object.Cells(x1, y1), sheet_object.Cells(x1 + len(input_values) - 1, y1 + len(
			input_values[0]) - 1)).Value = input_values

	def write_value_in_range_for_speed(self, sheet_name, xyxy, input_list_2d):
		"""
		2022-12-23 : x1, y1이 잘못되어서 변경함
		영역과 자료의 갯수중에서 작은것을 기준으로 값을 쓰는데
		만약 영역이 셀하나이면 자료를 전부 쓴다

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		:param input_list_2d:
		"""
		input_list_2d = self.change_xylist_to_list(input_list_2d)
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)

		min_x = min(x2 - x1 + 1, len(input_list_2d))
		min_y = min(y2 - y1 + 1, len(input_list_2d[0]))

		if x1 == x2 and y1 == y2:
			# 셀이 영역을 선택하지 않았다면, 전체 자료를 전부 넣는다
			changed_datas = input_list_2d
			self.r1c1 = self.change_xyxy_to_r1c1([x1, y1, x1 + len(input_list_2d) - 1, y1 + len(input_list_2d[0]) - 1])
			sheet_object.Range(self.r1c1).Value = changed_datas
		else:
			# 영역을 선택하면, 두 영역중에 작은 부분을 기준으로 자료를 넣는다
			changed_datas = []
			for x in range(min_x):
				changed_datas.append(input_list_2d[x][:min_y])
				self.r1c1 = self.change_xyxy_to_r1c1([x1, y1, x1 + min_x - 1, y1 + min_y - 1])
				sheet_object.Range(self.r1c1).Value = changed_datas

	def write_value_in_range_to_ydirection_only(self, sheet_name, xyxy, input_list):
		"""
		1차원리스트의 자료를 가로로 쓰는것
		영역보다 갯수 많으면, 갯수가 우선된다

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		:param input_list:
		:return:
		"""
		for x in range(len(input_list)):
			self.write_cell_value(sheet_name, [int(xyxy[0]) + x, xyxy[1]], input_list[x])

	def write_value_in_range_with_new_sheet(self, input_any_value):
		"""
		새로운 시트를 만들면서 값을 넣는것
		어떤 형태의 값이라도 알아서 써준다

		:param input_any_value:
		"""
		self.new_sheet()
		self.write_value_in_range("", [1, 1], input_any_value)

	def write_value_in_range_with_sheet_object_for_speed(self, sheet_object, xyxy, input_values):
		"""
		속도를 빠르게 하기 위해서 시트객체를 이용하는 것입니다
		반복작업을 위하여 속도를 올리고 싶을때 사용하는 것

		:param sheet_object:
		:param xyxy:
		:param input_values:
		:return:
		"""
		self.set_screen_update_off()
		for x in range(0, len(input_values)):
			for y in range(0, len(input_values[x])):
				sheet_object.Cells(x + xyxy[0], y + xyxy[1]).Value = input_values[x][y]
		self.set_screen_update_on()

	def write_value_in_statusbar(self, input_value="test"):
		"""
		스테이터스바에 원하는 글씨를 쓰는 것
		변경하거나 알리고싶은 내용을 나타낼수 있다

		:param input_value: 나타내고 싶은 글자
		"""
		self.xlapp.StatusBar = input_value

	def paint_rgb_set_from_xy_with_new_sheet(self, xy_list, rgb_set):
		self.new_sheet()
		for ix, one_rgb in rgb_set:
			self.paint_cell_by_rgb("", [xy_list[0]+ix, xy_list[1]], one_rgb)

	def write_vba_module(self, vba_code, macro_name):
		"""
		텍스트로 만든 엑셀 매크로 코드를 엑셀에 만들어서 실행하는 코드이다

		:param vba_code:
		:param macro_name:
		"""
		self.write_vba_module_in_workbook(vba_code, macro_name)

	def write_vba_module_in_workbook(self, vba_code, macro_name):
		"""
		텍스트로 만든 엑셀 매크로 코드를 엑셀에 만들어서 실행하는 코드이다

		:param vba_code:
		:param macro_name:
		"""
		new_vba_code = "Sub " + macro_name + "()" + vba_code + "End Sub"
		mod = self.xlbook.VBProject.VBComponents.Add(1)
		mod.CodeModule.AddFromString(new_vba_code)

	def read_value_in_range_as_text_speed(self, sheet_name="", xyxy=""):
		# 읽어온 자료중에서 TimeType 만 다시 불러서 보이는 형식으로 바꾸는것
		self.sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		old_l2d =  self.read_value_in_range(sheet_name, xyxy)
		result = []
		for ix, one_line in enumerate(old_l2d):
			one_line_list = list(one_line)
			for iy, one_value in enumerate(one_line_list):
				if type(one_value) == pywintypes.TimeType:
					one_line_list[iy]= self.sheet_object.Cells(ix+x1, iy+y1).Text
					result.append(one_line_list)
		return result

	def move_cell_in_front_by_start_with_aaa(self, startwith="*"):
		"""
		맨앞에 특정글자가 있으면, 앞으로 옮기기

		:param startwith:
		:return:
		"""
		x, y, x2, y2 = self.read_address_for_selection()
		self.insert_yline("", y)
		for one_x in range(x, x2):
			one_value = self.read_value_in_cell("", [one_x, y + 1])
			if one_value.startswith(startwith):
				self.write_value_in_cell("", [one_x, y], one_value)
				self.write_value_in_cell("", [one_x, y + 1], None)

	def write_korean_cjj(self, letters="박상진", canvas_size=[50, 50], stary_xy=[1, 1]):
		"""
		입력받은 한글을 크기가 50 x 50의 엑셀 시트에 글씨를 색칠하여 나타내는 것이다

		:param letters:
		:param canvas_size:
		:param stary_xy:
		:return:
		"""

		# 기본 설정부분
		size_x = canvas_size[0]
		size_y = canvas_size[1]
		# 문자 하나의 기본크기
		# 기본문자는 10을 기준으로 만들었으며, 이것을 얼마만큼 크게 만들것인지 한글자의 배수를 정하는것
		h_mm = int(canvas_size[0] / 10)
		w_mm = int(canvas_size[1] / 10)
		# 시작위치
		h_start = stary_xy[0]
		w_start = stary_xy[1]

		check_han = re.compile("[ㄱ-ㅎ|ㅏ-ㅣ|가-힣]")
		for one_char in letters:
			# 한글을 초성, 중성, 종성으로 나누는 것이다
			if check_han.match(one_char):
				jamo123 = self.change_korean_to_jamo(one_char)
				if jamo123[0][2] == "":
					# 가, 나, 다
					if jamo123[0][1] in ["ㅏ", "ㅐ", "ㅑ", "ㅒ", "ㅓ", "ㅔ", "ㅕ", "ㅖ", "ㅣ"]:
						# 기본설정은 시작점은 [1,1]이며, 캔버스의 크기는 [50, 50]인것이다

						start_xy = [1, 1]
						size = [10, 5]  # 위에서 배수를 5,5를 기본으로 해서 50x50되는 것이다
						# 자음의 시작점은 1,1이며, 크기는 50 x 25의 사이즈의 자음을 만드는 것이다
						self.draw_jaum_color(jamo123[0][0],
													[h_start + h_mm * (start_xy[0] - 1), w_start + w_mm * (start_xy[1] - 1)],
													[h_mm * size[0], w_mm * size[1]])
						# 모음의 시작점은 자음의 끝점에서 5를 이동한 1,30이며, 크기는 자음보다 가로의 크기를 좀 줄인
						# 50 x 20의 사이즈의 자음을 만드는 것이다

						start_xy = [1, 7]
						size = [10, 4]
						self.draw_moum_color(jamo123[0][1],
													[h_start + h_mm * (start_xy[0] - 1), w_start + w_mm * (start_xy[1] - 1)],
													[h_mm * size[0], w_mm * size[1]])

					# 구, 누, 루
					if jamo123[0][1] in ["ㅗ", "ㅛ", "ㅜ", "ㅡ"]:
						start_xy = [1, 1]
						size = [4, 10]
						self.draw_jaum_color(jamo123[0][0],
													[h_start + h_mm * (start_xy[0] - 1), w_start + w_mm * (start_xy[1] - 1)],
													[h_mm * size[0], w_mm * size[1]])
						start_xy = [6, 1]
						size = [5, 10]
						self.draw_moum_color(jamo123[0][1],
													[h_start + h_mm * (start_xy[0] - 1), w_start + w_mm * (start_xy[1] - 1)],
													[h_mm * size[0], w_mm * size[1]])

					# 와, 왜, 궈
					if jamo123[0][1] in ["ㅘ", "ㅙ", "ㅚ", "ㅝ", "ㅞ", "ㅟ", "ㅢ"]:
						# lists = self.div_mo2_mo1(jamo123[0][1])

						start_xy = [1, 1]
						size = [10, 5]
						self.draw_jaum_color(jamo123[0][0],
													[h_start + h_mm * (start_xy[0] - 1), w_start + w_mm * (start_xy[1] - 1)],
													[h_mm * size[0], w_mm * size[1]])
						start_xy = [8, 1]
						size = [3, 8]
						self.draw_moum_color(jamo123[0][1],
													[h_start + h_mm * (start_xy[0] - 1), w_start + w_mm * (start_xy[1] - 1)],
													[h_mm * size[0], w_mm * size[1]])
						start_xy = [1, 8]
						size = [6, 3]
						self.draw_moum_color(jamo123[0][1],
													[h_start + h_mm * (start_xy[0] - 1), w_start + w_mm * (start_xy[1] - 1)],
													[h_mm * size[0], w_mm * size[1]])

				if jamo123[0][2] != "":
					# 왕, 웍, 윔
					if jamo123[0][1] in ["ㅘ", "ㅙ", "ㅚ", "ㅝ", "ㅞ", "ㅟ", "ㅢ"]:
						hangul_type = "23자음+1332-2중모음+24자음"
						# lists = div_mo2_mo1(jamo123[0][1])

						start_xy = [1, 1]
						size = [4, 5]
						self.draw_jaum_color(jamo123[0][0],
													[h_start + h_mm * (start_xy[0] - 1), w_start + w_mm * (start_xy[1] - 1)],
													[h_mm * size[0], w_mm * size[1]])
						start_xy = [4, 1]
						size = [3, 7]
						self.draw_moum_color(jamo123[0][1],
													[h_start + h_mm * (start_xy[0] - 1), w_start + w_mm * (start_xy[1] - 1)],
													[h_mm * size[0], w_mm * size[1]])
						start_xy = [1, 7]
						size = [6, 3]
						self.draw_moum_color(jamo123[0][1],
													[h_start + h_mm * (start_xy[0] - 1), w_start + w_mm * (start_xy[1] - 1)],
													[h_mm * size[0], w_mm * size[1]])
						start_xy = [8, 1]
						size = [3, 6]
						self.draw_jaum_color(jamo123[0][0],
													[h_start + h_mm * (start_xy[0] - 1), w_start + w_mm * (start_xy[1] - 1)],
													[h_mm * size[0], w_mm * size[1]])

					# 앙, 양, 건
					if jamo123[0][1] in ["ㅏ", "ㅐ", "ㅑ", "ㅒ", "ㅓ", "ㅔ", "ㅕ", "ㅖ", "ㅣ"]:
						start_xy = [1, 1]
						size = [3, 5]
						self.draw_jaum_color(jamo123[0][0],
													[h_start + h_mm * (start_xy[0] - 1), w_start + w_mm * (start_xy[1] - 1)],
													[h_mm * size[0], w_mm * size[1]])
						start_xy = [1, 6]
						size = [5, 4]
						self.draw_moum_color(jamo123[0][1],
													[h_start + h_mm * (start_xy[0] - 1), w_start + w_mm * (start_xy[1] - 1)],
													[h_mm * size[0], w_mm * size[1]])
						start_xy = [7, 2]
						size = [3, 6]
						self.draw_jaum_color(jamo123[0][0],
													[h_start + h_mm * (start_xy[0] - 1), w_start + w_mm * (start_xy[1] - 1)],
													[h_mm * size[0], w_mm * size[1]])

					# 곡, 는
					if jamo123[0][1] in ["ㅗ", "ㅛ", "ㅜ", "ㅡ"]:
						start_xy = [1, 1]
						size = [3, 10]
						self.draw_jaum_color(jamo123[0][0],
													[h_start + h_mm * (start_xy[0] - 1), w_start + w_mm * (start_xy[1] - 1)],
													[h_mm * size[0], w_mm * size[1]])
						start_xy = [4, 1]
						size = [3, 10]
						self.draw_moum_color(jamo123[0][1],
													[h_start + h_mm * (start_xy[0] - 1), w_start + w_mm * (start_xy[1] - 1)],
													[h_mm * size[0], w_mm * size[1]])
						start_xy = [8, 1]
						size = [3, 10]
						self.draw_jaum_color(jamo123[0][0],
													[h_start + h_mm * (start_xy[0] - 1), w_start + w_mm * (start_xy[1] - 1)])

	def check_selection_address(self):
		# 선택한 영역이 부분으로 되어있을때를 위한것
		sheet_object = self.check_sheet_name("")
		xlCellTypeVisible = 12
		aaa = self.xlapp.Selection.SpecialCells(xlCellTypeVisible).Address
		bbb = self.xlapp.Selection.Address
		if aaa == bbb:
			print("같읍니다")
		else:
			print("다릅니다")
			print(aaa, " ====> ", bbb)


		"""
			 Set ws = ActiveSheet
	 
			For Each ThisCell In Selection.SpecialCells(xlCellTypeVisible)
					targetColumn = ThisCell.Column + 2
					ws.Cells(ThisCell.Row, targetColumn).Value = ThisCell.Value
			Next ThisCell
		:return: 
		"""

	def move_data(self, step, rng):
		#세로로 되어있는 자료를 반복하여 오른쪽으로 옮기는것
		flag_num = rng[1] % step
		start = rng[1]
		nnn = 0
		for num in range(rng[1], rng[2] + 1):
			nnn = nnn + 1
			if nnn == 1:
				x_num = num
			else:
				value = self.read_cell_value("", [num, rng[1]])
				self.write_cell_value("", [num - nnn + 1, rng[1] + nnn - 1], value)
				self.write_cell_value("", [num, rng[1]], "")
				if nnn == step:
					nnn = 0


	def change_list_samesize(self, input_data):
		#가변적인 2차원배열을 같은 크기로 만들어 준다
		result=[]
		max_len = max(len(row) for row in input_data)
		for list_x in input_data:
			temp=list_x
			for no in range(len(list_x), max_len):
				temp.append("")
			result.append(temp)
		return result


	def check_list_maxsize(self, list_2d_data):
	#2차원 배열의 제일 큰 갯수를 확인한다
		max_length = max(len(row) for row in list_2d_data)
		return max_length

	def make_dic_2list(self, key_list, value_list):
		# 두개의 리스트를 받으면 사전으로 만들어 주는 코드
		result = dict(zip(key_list, value_list))
		return result



	def change_alpha_int (self, input_data):
		#엑셀의 컬럼 주소를 숫자로 변경해 주는것
		result = 0
		for num in range(len(input_data)):
			digit = string.ascii_lowercase.index(input_data[num])
			result = result + (digit+1)*(26**num)
		return result

	def delete_all_data_inside_circle(self, input_text):
		#괄호안의 모든 문자를 지우는것
		re_basic = '\([^)]*\)'
		new_value = re.sub(re_basic, '', input_text)
		return new_value

	def make_comma_string(self, input_list):
		# 리스트를 주면, 콤마로 연결한 문자열을 만들어주는것
		result = ""
		for one_item in input_list:
			if one_item == "":
				pass
			else:
				result += str(one_item) + ", "
		return result[:-2]

	def delete_blank(self, xyxy= [1, 2, 2759, 2]):
		#선택한 영역의 모든자료의 앞뒤의 공백을 없애는것
		x1, y1, x2, y2 = xyxy
		source_datas = self.read_range_value("", xyxy)
		for x in range(len(source_datas)):
			for y in range(len(source_datas[0])):
				one_source = source_datas[x][y]
				if one_source != None:
					source_datas[x][y] = str(one_source).strip()
		self.dump_range_value("", [x1, y1], source_datas)



	def check_item(self, xyxy = [1, 2, 260, 2], ez_sql = "[영어:1~10]-[숫자:1~10](,[숫자:1~10]){1,5}", changed_text =""):
		#조건에 맞는 것을 변경하는 것
		# xyxy, ez_sql, changed_text
		#text_mod = re.sub('^[0-9]{3}-[0-9]{4}-[0-9]{4}', "***-****-****", text, flags=re.MULTILINE)

		re_sql = self.xyre.change_jf_sql_to_re_sql(ez_sql)
		x1, y1, x2, y2 = xyxy
		source_datas = self.read_range("", xyxy)
		for x in range(len(source_datas)):
			for y in range(len(source_datas[0])):
				one_source = source_datas[x][y]
				if one_source != None:
					source_datas[x][y] = re.sub(re_sql,one_source, changed_text)
		self.dump_range_value("", [x1, y1], source_datas)

	def cal_range_address(self, son, mother):
		# 두 영역이 겹쳐지는 영역을 게산하는것
		if len(son) == 2: son = son + son
		if len(mother) == 2: mother = mother + mother

		x1, y1, x2, y2 = self.arrange_min(son)
		x3, y3, x4, y4 = self.arrange_min(mother)

		## case1 오른쪽, 왼쪽, 위, 아래으로 벗어나 있는 경우
		if x2 < x3 or x1 > x4 or y2 < y3 or y1 > y4:
			kyo = [0, 0, 0, 0]
		else:
			cross_area = [max(x1, x3), max(y1, y3), min(x2, x4), min(y2, y4)]
			x_long_with_cross_area = [max(x1, x3), mother[1], min(x2, x4), mother[3]]
			y_long_with_cross_area = [mother[0], max(y1, y3), mother[2], min(y2, y4)]

		return [cross_area, x_long_with_cross_area, y_long_with_cross_area]



	def arrange_min (self, input_data):
		#xyxy의 영역자료가 들어오면, 작은것부터 정렬하는것
		x1, y1, x2, y2 = input_data
		if x1 > x2 :
			new_x1 = x2
			new_x2 = x1
		else:
			new_x1 = x1
			new_x2 = x2

		if y1 > y2 :
			new_y1 = y2
			new_y2 = y1
		else:
			new_y1 = y1
			new_y2 = y2
		return [new_x1, new_y1, new_x2, new_y2]



	def change_eng_int(self, eng):
			# [x, y]형태의 자료를 a1의 형태로 변경해 주는것
			result = []
			for one in eng:
				aaa = string.ascii_lowercase
				result.append(aaa.find(one)+1)
			print(result)
			return result

	def file_type_change(self, path, file_name, original_type="EUC-KR", new_type="UTF-8", new_file_name=""):
		full_path = path + "\\" + file_name
		full_path_changed = path + "\\" + new_file_name + file_name
		try:
			aaa = open(full_path, 'rb')
			result = chardet.detect(aaa.read())
			print(result['encoding'], file_name)
			aaa.close()

			if result['encoding'] == original_type:
				print("화일의 인코딩은 ======> {}, 화일이름은 {} 입니다".format(original_type, file_name))
				aaa = open(full_path, "r", encoding=original_type)
				file_read = aaa.readlines()
				aaa.close()

				new_file = open(full_path_changed, mode='w', encoding=new_type)
				for one in file_read:
					new_file.write(one)
				new_file.close()
		except:
			print("화일이 읽히지 않아요=====>", file_name)

	def make_ppt_table_from_xl_data(self, ):

		"""
		엑셀의 테이블 자료가 잘 복사가 않되는것 같아서, 아예 하나를 만들어 보았다
		엑셀의 선택한 영역의 테이블 자료를 자동으로 파워포인트의 테이블 형식으로 만드는 것이다
		"""
		activesheet_name = self.excel.read_name_for_activesheet()
		[x1, y1, x2, y2] = self.excel.read_address_for_selection()
		print([x1, y1, x2, y2])

		Application = win32com.client.Dispatch("Powerpoint.Application")
		Application.Visible = True
		active_ppt = Application.Activepresentation
		slide_no = active_ppt.Slides.Count + 1

		new_slide = active_ppt.Slides.Add(slide_no, 12)
		new_table = active_ppt.Slides(slide_no).Shapes.AddTable(x2 - x1 + 1, y2 - y1 + 1)
		shape_no = active_ppt.Slides(slide_no).Shapes.Count

		for y in range(y1, y2 + 1):
			for x in range(x1, x2 + 1):
				value = self.excel.read_value_in_cell(activesheet_name, [x, y])
				active_ppt.Slides(slide_no).Shapes(shape_no).Table.Cell(x - x1 + 1,
																		y - y1 + 1).Shape.TextFrame.TextRange.Text = value

	def print_letter_cover_01(self, ):
		"""
		봉투인쇄
		"""


		# 기본적인 자료 설정
		data_from = [["sheet1", [1, 2]], ["sheet1", [1, 4]], ["sheet1", [1, 6]], ["sheet1", [1, 8]]]
		data_to = [["sheet2", [1, 2]], ["sheet2", [2, 2]], ["sheet2", [3, 2]], ["sheet2", [2, 3]]]

		no_start = 1
		no_end = 200
		step = 5

		# 실행되는 구간
		for no in range(no_start, no_end):
			for one in range(len(data_from)):
				value = self.excel.read_cell_value(data_from[one][0], data_from[one][1])
				self.excel.write_cell_value(data_to[one][0], [data_to[one][1][0] + (step * no), data_to[one][1][1]], value)
