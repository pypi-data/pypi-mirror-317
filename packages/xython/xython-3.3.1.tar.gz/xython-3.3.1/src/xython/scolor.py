# -*- coding: utf-8 -*-
from unittest.mock import patch
with patch("ctypes.windll.user32.SetProcessDPIAware", autospec=True):
    import pyautogui

import jfinder, basic_data  # xython 모듈
import re, math  # 내장모듈

class scolor:
	"""
	색을 편하게 사용하기위해 만든 모듈
	기본값의 형태 : rgb

	2024-04-25 : 전체적으로 이름을 terms에 따라서 변경함
	"""

	def __init__(self):
		"""
		self.vars : package안에서 공통적으로 사용되는 변수들
		"""

		self.xyre = jfinder.jfinder()
		self.vars = basic_data.basic_data().vars

	def _change_scolor_to_hsl(self, input_scolor):
		# input _Hd=> [숫자만","색이름",숫자, "+ 갯수","- 갯수" rgb_list, rgb_int] # ==> [11,"red",60,3,5,[255,25,0], 12345]
		input_l1d = self._check_input_scolor(input_scolor)
		print(input_l1d)
		hsl_list = None

		if input_l1d[0]: # 정수, 12가지 기본색
			hsl_list = self.vars["list_basic_12hsl"][input_l1d[0]]
		elif input_l1d[1]: # 색이름
			hsl_list = self.vars["color_name_eng_vs_hsl_no"][input_l1d[1]]
			if input_l1d[2]: # 명도
				hsl_list[2] = input_l1d[2]
			if input_l1d[3]: #채도 +
				temp = hsl_list[0]+ 3* input_l1d[3]
				hsl_list[0] = divmod(temp, 360)[1]
			elif input_l1d[4]: #채도 -
				temp = hsl_list[0]- 3* input_l1d[4] + 360
				hsl_list[0] = divmod(temp, 360)[1]
		elif input_l1d[5]: # rgb_list
			hsl_list = self.change_rgb_to_hsl(input_l1d[5])
		elif input_l1d[6]: #rgb_int
			hsl_list = self.change_rgbint_to_hsl(input_l1d[6])
		return hsl_list

	def _check_input_scolor(self, input_scolor):
		"""
		scolor 형식의 입력값을 화인하는 것이다
		1. 정수만 오는경우 : 기본 12 색중에서 하나로 간주
		2. red++45 :red, ++, 45로 구분
		3. RGB 가 오는 경우
		4. 12 초과의 숫자가 오면 RGBINT 로 간주한다 -
		return: [숫자만","색이름",숫자, "+ 갯수","- 갯수" rgb _list, rgb_int] ==>

		:param input_scolor:
		:return:
		"""
		result = [None, None, None, None, None, None, None ]
		if type(input_scolor) == type([]): #rgb 리스트일때
			result[5] = input_scolor
		elif type(input_scolor) ==type(123):
			if input_scolor < 13: #기본색상일때
				result[0] = input_scolor
			else: #12 초과숫자로 rgbint로 간주
				result[6] = input_scolor
		elif type(input_scolor) == type("abc"): #영어나 한글로 된 색깔이름을 추출
			# 영어나 한글로 된 색깔이름을 추출
			re_com1 = re.compile("[a-zA-Z_가-힣]+")
			color_name = re_com1.findall(input_scolor)
			#print(color_name)
			checked_color_name = self.vars["check_color_name"][color_name[0]]
			result[1] = checked_color_name

			# scolor에서 숫자만 추출
			re_com2 = re.compile("[0-9]+")
			nos = re_com2.findall(input_scolor)
			if nos: result[2] = int(nos[0])

			# scolor에서 + 추출
			re_com3 = re.compile("[+]+")
			scolor_plus = re_com3.findall(input_scolor)
			if scolor_plus: result[3] = len(scolor_plus[0])

			# scolor에서 - 추출
			re_com4 = re.compile("[-]+")
			scolor_minus = re_com4.findall(input_scolor)
			if scolor_minus: result[4] = len(scolor_minus[0])
		return result

	def calculate_distance_two_3d_point(self, input_1, input_2):
		"""
		3 차원의 거리를 기준으로 RGB 값의 차이를 계산하는 것
		색간의 거리를 계산

		:param input_1:
		:param input_2:
		:return:
		"""
		dist = math.sqrt(
			math.pow((input_1[0] - input_2[0]), 2) + math.pow((input_1[1] - input_2[1]), 2) + math.pow(
				(input_1[2] - input_2[2]), 2))
		return dist

	def change_any_color_to_hsl(self, input_color):
		"""
		any_color라는 단어가 사용자의 입장에서 이해하기 더 편할것 같아서 추가하여 만든 것

		:param input_color:
		:return:
		"""
		result = self._change_scolor_to_hsl(input_color)
		return result

	def change_any_color_to_rgb(self, input_color):
		"""
		any_color라는 단어가 사용자의 입장에서 이해하기 더 편할것 같아서 추가하여 만든 것

		:param input_color:
		:return:
		"""
		result = self.change_input_color_to_rgb(input_color)
		return result

	def change_any_color_to_rgbint(self, input_color):
		"""
		any_color라는 단어가 사용자의 입장에서 이해하기 더 편할것 같아서 추가하여 만든 것

		:param input_color:
		:return:
		"""
		rgb = self.change_input_color_to_rgb(input_color)
		result = self.change_rgb_to_rgbint(rgb)
		return result

	def change_excel56_to_color_kor(self, input_excel56):
		"""
		엑셀 56색의 번호 -> 한글 색이름

		:param input_excel56:
		:return:
		"""
		result = self.vars["excel56_vs_color_kor"][int(input_excel56)]
		return result

	def change_excel56_to_color_name(self, input_excel56):
		result = self.change_excel56_to_color_kor(input_excel56)
		return result

	def change_excel56_to_rgb(self, i_no):
		"""
		엑셀 56색의 번호 -> rgb 리스트

		:param input_excel56:
		:return:
		"""
		result = self.vars["rgb56_for_excel"][int(i_no)]
		return result

	def change_hsl_by_color_style(self, basic_hsl, color_style="파스텔", style_step=5):
		"""
		hsl값을 색의 스타일과 강도로써 조정하는 것

		:param basic_hsl:
		:param color_style:
		:param style_step:
		:return:
		"""

		checked_color_style = self.vars["check_color_tone"][color_style]

		step_2 = self.vars["basic_15tone_eng_vs_sl"][checked_color_style]
		step_1 = self.vars["basic_10color_sl_small_step"][str(str(style_step))]
		h = int(basic_hsl[0])
		s = int(step_1[0]) + int(step_2[0])
		l = int(step_1[1]) + int(step_2[1])

		changed_rgb = self.change_hsl_to_rgb([h, s, l])
		return changed_rgb

	def change_hsl_by_plusminus100(self, hsl_list, plusminus100):
		"""
		hsl값을 미세조정하는 부분

		plusminus100 : ++, --, 70등의 값이 들어오면 변화를 시켜주는 것

		:param hsl_list:
		:param plusminus100:
		:return:
		"""
		if type(plusminus100) == type(123):
			# 50을 기본으로 차이나는 부분을 계산하는것
			l_value = plusminus100 - 50
			if l_value < 0:
				l_value = 0
		elif "+" == str(plusminus100)[0]:
			# 현재의 값에서 10만큼 밝아지도록 한다
			l_value = 10 * len(plusminus100)
		elif "-" == str(plusminus100)[0]:
			# 현재의 값에서 10만큼 어두워지도록 한다
			l_value = -10 * len(plusminus100)

		final_l_value = hsl_list[2] + l_value
		if final_l_value > 100:
			final_l_value = 100
		elif final_l_value < 0:
			final_l_value = 0

		result = [hsl_list[0], hsl_list[1], final_l_value]
		return result

	def change_hsl_for_sl_by_0to100(self, hsl, step_no):
		"""
		hsl값을 명도를 조정하는 방법
		+，-로 조정을 하는것이다

		:param hsl: [h,s,l]형식의 값
		:param step_no:
		:return:
		"""
		s, l = self.vars["색강도_vs_sl"][step_no]
		result = [hsl[0], hsl[1] + s, hsl[2] + l]

	def change_hsl_for_sl_by_plusminus100(self, hsl, s_step="++", l_step="++"):
		"""
		hsl값을 올리거나 내리는 것, sl의값을 조정하여 채도와 명도를 조절하는것
		입력 : [[36, 50, 50], "++", "--"]
		약 5씩이동하도록 만든다

		:param hsl: [h,s,l]형식의 값
		:param s_step:
		:param l_step:
		:return:
		"""
		step_no = 5  # 5단위씩 변경하도록 하였다
		h, s, l = hsl

		if s_step == "":
			pass
		elif s_step[0] == "+":
			s = s + len(s_step) * step_no
			if s > 100: s = 100
		elif s_step[0] == "-":
			s = s - len(s_step) * step_no
			if s < 0: s = 0

		if l_step == "":
			pass
		elif l_step[0] == "+":
			l = l + len(l_step) * step_no
			if l > 100: l = 100
		elif l_step[0] == "-":
			l = l - len(l_step) * step_no
			if l < 0: l = 0

		result = self.change_hsl_to_rgb([h, s, l])
		return result

	def change_hsl_to_2_hsl_for_near_bo(self, hsl, h_step=36):
		"""
		근접보색조합 : 보색의 근처색
		분열보색조합 : Split Complementary
		근접보색조합 : 보색의 강한 인상이 부담스러울때 보색의 근처에 있는 색을 사용

		:param hsl: [h,s,l]형식의 값
		:param h_step:
		:return:
		"""
		h, s, l = hsl

		new_h_1 = divmod(h - h_step + 180, 360)[1]
		new_h_3 = divmod(h + h_step + 180, 360)[1]

		hsl_1 = [new_h_1, s, l]
		hsl_3 = [new_h_3, s, l]
		return [hsl_1, hsl_3]

	def change_hsl_to_2_rgb_for_near_bo(self, hsl, h_step=36):
		"""
		근접보색조합 : 보색의 양쪽 근처색
		분열보색조합 : Split Complementary
		근접보색조합 : 보색의 강한 인상이 부담스러울때 보색의 근처에 있는 색을 사용
		2차원 list의 형태로 돌려줌

		:param hsl: [h,s,l]형식의 값
		:param h_step:
		:return:
		"""
		result =[]
		hsl_set = self.change_hsl_to_2_hsl_for_near_bo(hsl, h_step=36)
		for one_hsl in hsl_set:
			result.append(self.change_hsl_to_rgb(one_hsl))
		return result

	def change_hsl_to_2_hsl_for_near_bo_step_by_h_0to100(self, hsl, h_step=36):
		"""
		level100 : -100 ~ 100사이의 값
		근접보색조합 : 보색의 근처색
		분열보색조합 : Split Complementary
		근접보색조합이라고도 한다. 보색의 강한 인상이 부담스러울때 보색의 근처에 있는 색을 사용

		:param hsl: [h,s,l]형식의 값
		:param h_step:
		:return:
		"""
		h, s, l = hsl

		new_h_1 = divmod(h - h_step + 180, 360)[1]
		new_h_3 = divmod(h + h_step + 180, 360)[1]

		hsl_1 = [new_h_1, s, l]
		hsl_3 = [new_h_3, s, l]
		result = [hsl_1, hsl, hsl_3]
		return result

	def change_hsl_to_2_rgb_for_near_step_by_h_0to100(self, hsl, h_step=36):
		"""
		입력으로 들어오는 색의 양쪽 근처의 색을 돌려주는 것
		기본으로 h의 값을 36만큼의 양쪽 색을 돌려준다
		근접색조합 : 양쪽 근처색

		:param hsl: [h,s,l]형식의 값
		:param h_step:
		:return:
		"""
		h, s, l = hsl

		new_h_1 = divmod(h - h_step, 360)[1]
		new_h_3 = divmod(h + h_step, 360)[1]

		rgb_1 = self.change_hsl_to_rgb([new_h_1, s, l])
		rgb_2 = self.change_hsl_to_rgb(hsl)
		rgb_3 = self.change_hsl_to_rgb([new_h_3, s, l])
		result = [rgb_1, rgb_2, rgb_3]
		return result

	def change_hsl_to_2_hsl_for_side_color_step_by_h_0to100(self, hsl, h_step=36):
		"""
		level100 : -100 ~ 100사이의 값
		근접색조합 : 양쪽 근처색

		:param hsl: [h,s,l]형식의 값
		:param h_step:
		:return:
		"""
		h, s, l = hsl

		new_h_1 = divmod(h - h_step, 360)[1]
		new_h_3 = divmod(h + h_step, 360)[1]

		rgb_1 = self.change_hsl_to_rgb([new_h_1, s, l])
		rgb_2 = self.change_hsl_to_rgb(hsl)
		rgb_3 = self.change_hsl_to_rgb([new_h_3, s, l])
		result = [rgb_1, rgb_2, rgb_3]
		return result

	def change_hsl_to_2_hsl_for_side_color_by_l_0to100(self, hsl, l_step=30):
		"""
		level100 : -100 ~ 100사이의 값
		명도차가 큰 2가지 1가지색

		:param hsl: [h,s,l]형식의 값
		:param l_step:
		:return:
		"""
		h, s, l = hsl
		rgb_1 = self.change_hsl_to_rgb([h, s, l_step])
		rgb_2 = self.change_hsl_to_rgb(hsl)
		rgb_3 = self.change_hsl_to_rgb([h, s, 100 - l_step])
		result = [rgb_1, rgb_2, rgb_3]
		return result

	def change_hsl_to_2_hsl_for_side_color_by_s_0to100(self, hsl, s_step=30):
		"""
		level100 : -100 ~ 100사이의 값
		채도차가 큰 2가지 1가지색

		:param hsl: [h,s,l]형식의 값
		:param s_step:
		:return:
		"""
		rgb_1 = self.change_hsl_to_rgb([hsl[0], s_step, hsl[2]])
		rgb_2 = self.change_hsl_to_rgb(hsl)
		rgb_3 = self.change_hsl_to_rgb([hsl[0], 100 - s_step, hsl[2]])
		result = [rgb_1, rgb_2, rgb_3]
		return result

	def change_hsl_to_3_hsl_step_by_big_l(self, hsl, l_step=30):
		"""
		명도차가 큰 2가지 1가지색

		:param hsl: [h,s,l]형식의 값
		:param l_step:
		:return:
		"""
		rgb_1 = self.change_hsl_to_rgb([hsl[0], hsl[1], l_step])
		rgb_2 = self.change_hsl_to_rgb(hsl)
		rgb_3 = self.change_hsl_to_rgb([hsl[0], hsl[1], 100 - l_step])
		result = [rgb_1, rgb_2, rgb_3]
		return result

	def change_hsl_to_3_hsl_step_by_big_s(self, hsl, s_step=30):
		"""
		채도차가 큰 2가지 1가지색

		:param hsl: [h,s,l]형식의 값
		:param s_step:
		:return:
		"""
		rgb_1 = self.change_hsl_to_rgb([hsl[0], s_step, hsl[2]])
		rgb_2 = self.change_hsl_to_rgb(hsl)
		rgb_3 = self.change_hsl_to_rgb([hsl[0], 100 - s_step, hsl[2]])
		result = [rgb_1, rgb_2, rgb_3]
		return result

	def change_hsl_to_3_rgb_step_by_0_120_240(self, hsl):
		result = self.change_hsl_to_3_rgb_step_by_h_120(hsl)
		return result

	def change_hsl_to_3_rgb_step_by_h_120(self, hsl):
		"""
		등간격 3색조합 : triad
		활동적인 인상과 이미지를 보인다

		:param hsl: [h,s,l]형식의 값
		:return:
		"""
		h, s, l = hsl

		new_h_1 = divmod(h + 120, 360)[1]
		new_h_3 = divmod(h + 240, 360)[1]

		hsl_1 = [new_h_1, s, l]
		hsl_3 = [new_h_3, s, l]

		result_rgb = self.change_hsl_to_rgb([hsl_1, hsl, hsl_3])
		return result_rgb

	def change_hsl_to_bright_high(self, hsl):
		"""
		입력된 hsl값 -> 고명도로 바꾸는 것
		"""
		hsl[2] = 80
		return hsl

	def change_hsl_as_bright_low(self, hsl):
		"""
		입력된 hsl값 -> 저명도로 바꾸는 것 (저명도 : 명도값이 20%정도)
		"""
		hsl[2] = 20
		return hsl

	def change_hsl_as_bright_middle(self, hsl):
		"""
		입력된 hsl값 -> 중명도로 바꾸는 것
		"""
		hsl[2] = 50
		return hsl

	def change_hsl_as_bright_up_by_0to100(self, hsl, strong_level=50):
		"""
		입력받은 hsl값을 명도가 높은 쪽으로 이동시키는것

		level1 : 0~1사이의값
		bright = [100,100], sharp = [50,100], graish = [100,0], dark = [0,0], black = [50, 0]

		:param hsl: [h,s,l]형식의 값
		:param strong_level:
		:return:
		"""
		h, s, l = hsl

		changed_s = s + (100 - s) * strong_level/100
		changed_l = l + (100 - l) * strong_level/100
		return [h, changed_s, changed_l]

	def change_hsl_to_color_high(self, hsl):
		"""
		입력된 hsl값 -> 고채도로 바꾸는 것
		"""
		hsl[1] = 80
		return hsl

	def change_hsl_to_contrast_high(self, hsl):
		"""
		입력된 hsl값 -> 중채도로 바꾸는 것
		"""
		hsl[0] = 100
		return hsl

	def change_hsl_to_contrast_low(self, hsl):
		"""
		입력된 hsl값 -> 저채도로 바꾸는 것
		"""
		hsl[0] = 20
		return hsl

	def change_hsl_to_contrast_middle(self, hsl):
		"""
		입력된 hsl값 -> 중채도로 바꾸는 것
		"""
		hsl[0] = 50
		return hsl

	def change_hsl_as_dark_up_by_0to1(self, hsl, strong_level=0.5):
		"""
		입력받은 hsl값을 어두운 쪽으로 이동시키는것

		level1 : 0~1사이의값
		bright = [100,100], sharp = [50,100], graish = [100,0], dark = [0,0], black = [50, 0]

		:param hsl: [h,s,l]형식의 값
		:param strong_level:
		:return:
		"""
		h, s, l = hsl
		style = dark = [0, 0]

		delta_s = (style[0] - s) * strong_level
		delta_l = (style[1] - l) * strong_level

		changed_s = s + delta_s
		changed_l = l + delta_l
		return [h, changed_s, changed_l]

	def change_hsl_as_gray_up_by_0to1(self, hsl, strong_level=0.5):
		"""
		입력받은 hsl값을 어두운 쪽으로 이동시키는것

		level1 : 0~1사이의값
		bright = [100,100], sharp = [50,100], graish = [100,0], dark = [0,0], black = [50, 0]

		:param hsl: [h,s,l]형식의 값
		:param strong_level:
		:return:
		"""
		h, s, l = hsl
		style = graish = [100, 0]

		delta_s = (style[0] - s) * strong_level
		delta_l = (style[1] - l) * strong_level

		changed_s = s + delta_s
		changed_l = l + delta_l
		return [h, changed_s, changed_l]

	def change_hsl_as_pastel_style(self, hsl, strong_level=0.5):
		"""
		입력받은 hsl값을 파스텔톤으로 적용시키는것

		level1 : 0~1사이의값
		bright = [100,100], sharp = [50,100], graish = [100,0], dark = [0,0], black = [50, 0]

		:param hsl: [h,s,l]형식의 값
		:param strong_level:
		:return:
		"""
		h, s, l = hsl
		style = pastel = [0, 100]

		delta_s = (style[0] - s) * strong_level
		delta_l = (style[1] - l) * strong_level

		changed_s = s + delta_s
		changed_l = l + delta_l
		return [h, changed_s, changed_l]

	def change_hsl_to_rgb(self, hsl):
		"""
		hsl을 rgb로 변경

		:param hsl: [h,s,l]형식의 값
		:return:
		"""
		h, s, l = hsl

		h = float(h / 360)
		s = float(s / 100)
		l = float(l / 100)

		if s == 0:
			R = l * 255
			G = l * 255
			B = l * 255

		if l < 0.5:
			temp1 = l * (1 + s)
		else:
			temp1 = l + s - l * s

		temp2 = 2 * l - temp1

		# h = h / 360

		tempR = h + 0.333
		tempG = h
		tempB = h - 0.333

		if tempR < 0: tempR = tempR + 1
		if tempR > 1: tempR = tempR - 1
		if tempG < 0: tempG = tempG + 1
		if tempG > 1: tempG = tempG - 1
		if tempB < 0: tempB = tempB + 1
		if tempB > 1: tempB = tempB - 1

		if 6 * tempR < 1:
			R = temp2 + (temp1 - temp2) * 6 * tempR
		else:
			if 2 * tempR < 1:
				R = temp1
			else:
				if 3 * tempR < 2:
					R = temp2 + (temp1 - temp2) * (0.666 - tempR) * 6
				else:
					R = temp2

		if 6 * tempG < 1:
			G = temp2 + (temp1 - temp2) * 6 * tempG
		else:
			if 2 * tempG < 1:
				G = temp1
			else:
				if 3 * tempG < 2:
					G = temp2 + (temp1 - temp2) * (0.666 - tempG) * 6
				else:
					G = temp2
		if 6 * tempB < 1:
			B = temp2 + (temp1 - temp2) * 6 * tempB
		else:
			if 2 * tempB < 1:
				B = temp1
			else:
				if 3 * tempB < 2:
					B = temp2 + (temp1 - temp2) * (0.666 - tempB) * 6
				else:
					B = temp2
		R = int(abs(round(R * 255, 0)))
		G = int(abs(round(G * 255, 0)))
		B = int(abs(round(B * 255, 0)))

		return [R, G, B]

	def change_hsl_to_rgb_by_4_tetra_style(self, hsl):
		"""
		4가지 꼭지의 rgb값

		:param hsl: [h,s,l]형식의 값
		:return:
		"""
		h, s, l = hsl

		new_h_1 = divmod(h + 0, 360)[1]
		new_h_2 = divmod(h + 90, 360)[1]
		new_h_3 = divmod(h + 180, 360)[1]
		new_h_4 = divmod(h + 270, 360)[1]
		rgb_1 = self.change_hsl_to_rgb([new_h_1, s, l])
		rgb_2 = self.change_hsl_to_rgb([new_h_2, s, l])
		rgb_3 = self.change_hsl_to_rgb([new_h_3, s, l])
		rgb_4 = self.change_hsl_to_rgb([new_h_4, s, l])
		result = [rgb_1, rgb_2, rgb_3, rgb_4]

		return result

	def change_hsl_to_rgb_by_pccs_style(self, hsl, color_style="파스텔", style_step=5):

		color_style_checked = self.vars["check_color_tone"][color_style]
		step_2 = self.vars["basic_15tone_eng_vs_sl"][color_style_checked]  # 스타일을 적용하는것
		step_1 = self.vars["basic_10color_sl_small_step"][str(style_step)]  # 스타일을 얼마나 강하게 적용할것인가를 나타내는것

		h = int(hsl[0])
		s = int(step_1[0]) + int(step_2[0])
		l = int(step_1[1]) + int(step_2[1])

		changed_rgb = self.change_hsl_to_rgb([h, s, l])
		return changed_rgb

	def change_hsl_to_rgb_by_plusminus100(self, hsl, plusminus100):
		"""
		plusminus100 : ++, --, 70등의 값이 들어오면 변화를 시켜주는 것

		:param hsl: [h,s,l]값
		:param plusminus100:
		:return:
		"""
		if type(plusminus100) == type(123):
			# 50을 기본으로 차이나는 부분을 계산하는것
			l_value = plusminus100 - 50
			if l_value < 0:
				l_value = 0
		elif "+" == str(plusminus100)[0]:
			# 현재의 값에서 10만큼 밝아지도록 한다
			l_value = 10 * len(plusminus100)
		elif "-" == str(plusminus100)[0]:
			# 현재의 값에서 10만큼 어두워지도록 한다
			l_value = -10 * len(plusminus100)

		final_l_value = hsl[2] + l_value
		if final_l_value > 100:
			final_l_value = 100
		elif final_l_value < 0:
			final_l_value = 0

		result = [hsl[0], hsl[1], final_l_value]
		return result

	def change_hsl_to_rgb_by_tone(self, hsl, color_style="파스텔", style_step=5):
		"""
		입력된 기본 값을 스타일에 맞도록 바꾸고, 스타일을 강하게 할것인지 아닌것인지를 보는것
		color_style : pccs의 12가지 사용가능, 숫자로 사용가능, +-의 형태로도 사용가능
		입력예 : 기본색상, 적용스타일, 변화정도,("red45, 파스텔, 3)
		변화정도는 5를 기준으로 1~9까지임

		:param hsl: [h,s,l]형식의 값
		:param color_style:
		:param style_step:
		:return:
		"""

		color_style_checked = self.vars["check_color_tone"][color_style]
		step_2 = self.vars["basic_15tone_eng_vs_sl"][color_style_checked]  # 스타일을 적용하는것
		step_1 = self.vars["basic_10color_sl_small_step"][str(style_step)]  # 스타일을 얼마나 강하게 적용할것인가를 나타내는것

		h = int(hsl[0])
		s = int(step_1[0]) + int(step_2[0])
		l = int(step_1[1]) + int(step_2[1])

		changed_rgb = self.change_hsl_to_rgb([h, s, l])
		return changed_rgb

	def change_hsl_to_rgb_by_triangle_style(self, hsl):
		result = self.change_hsl_to_3_rgb_step_by_h_120(hsl)
		return result

	def change_hsl_to_rgbint(self, hsl):
		rgb = self.change_hsl_to_rgb(hsl)
		result = self.change_rgb_to_rgbint(rgb)
		return result

	def change_hsl_to_triangle_style(self, hsl):
		result = self.change_hsl_to_3_rgb_step_by_h_120(hsl)
		return result

	def change_hsl_as_vivid_by_0to1(self, hsl, strong_level=0.5):
		"""
		level1 : 0~1사이의값
		입력받은 hsl값을 어두운 쪽으로 이동시키는것
		bright = [100,100], sharp = [50,100], graish = [100,0], dark = [0,0], black = [50, 0]

		:param hsl: [h,s,l]형식의 값
		:param strong_level:
		:return:
		"""
		h, s, l = hsl
		style = sharp = [50, 100]

		delta_s = (style[0] - s) * strong_level
		delta_l = (style[1] - l) * strong_level

		changed_s = s + delta_s
		changed_l = l + delta_l
		return [h, changed_s, changed_l]

	def change_input_color_to_hsl(self, input_color):
		"""
		어떤 색을 나타내는 형태라도 hsl값을 돌려주는것

		:param input_value: rgb형식, hsl형식, scolor형식
		:return: hsl값
		"""
		if type(input_color) == type("string"):  # 문자열 형식일때 scolor형식으로 해석
			hsl = self._change_scolor_to_hsl(input_color)

		elif type(input_color) == type(123):  # 숫자가 입력되면 rgbint값으로 해석
			rgb = self.change_rgbint_to_rgb(input_color)
			hsl = self.change_rgb_to_hsl(rgb)

		elif type(input_color) == type([]) and len(input_color) == 3:  # 3개의 리스트형식일때는 확인해서 hsl 이나 rgb로 해석
			if input_color[0] > 255:
				hsl = input_color
			else:
				if input_color[1] > 100 or input_color[2] > 100:
					hsl = self.change_rgb_to_hsl(input_color)
				else:
					hsl = input_color
		else:
			hsl = "error"
		return hsl

	def change_input_color_to_rgb(self, input_color):
		"""
		입력된 색깔을 rgb의 리스트형태로 바꾸는 것
		scolor모듈 대신해서, 자주사용하는 것이라 여기더 만듦

		:param input_color: 어떤 형식이라도 들어오는 색이름
		"""
		result = ""
		input_type = type(input_color)
		if input_type == type(123):
			result = self.change_rgbint_to_rgb(input_color)
		elif input_type == type("abc"):
			result = self.change_scolor_to_rgb(input_color)
		elif input_type == type([]):
			result = input_color
		return result

	def change_input_color_to_rgbint(self, input_color):
		"""
		입력된 색깔을 rgb의 리스트형태로 바꾸는 것
		scolor모듈 대신해서, 자주사용하는 것이라 여기더 만듦

		:param input_color: 어떤 형식이라도 들어오는 색이름
		"""
		result = ""
		input_type = type(input_color)
		if input_type == type(123):
			rgb = self.change_rgbint_to_rgb(input_color)
		elif input_type == type("abc"):
			rgb = self.change_scolor_to_rgb(input_color)
		elif input_type == type([]):
			rgb = input_color
		result = self.change_rgb_to_rgbint(rgb)
		return result

	def change_rgb_by_sl_plusminus100(self, input_rgb, s_step="++", l_step="++"):
		"""

		:param input_rgb:
		:param s_step:
		:param l_step:
		:return:
		"""
		hsl = self.change_rgb_to_hsl(input_rgb)
		step_no = 5  # 5단위씩 변경하도록 하였다
		h, s, l = hsl

		if s_step == "":
			pass
		elif s_step[0] == "+":
			s = s + len(s_step) * step_no
			if s > 100: s = 100
		elif s_step[0] == "-":
			s = s - len(s_step) * step_no
			if s < 0: s = 0

		if l_step == "":
			pass
		elif l_step[0] == "+":
			l = l + len(l_step) * step_no
			if l > 100: l = 100
		elif l_step[0] == "-":
			l = l - len(l_step) * step_no
			if l < 0: l = 0

		result = self.change_hsl_to_rgb([h, s, l])
		return result

	def change_rgb_to_12_rgb_for_pccs_list(self, rgb):
		"""
		pccs : 일본색체연구서가 빌표한 12가지 색으로 구분한것
		어떤 입력된 색의 기본적인 PCSS 12색을 돌려준다
		pccs톤, rgb로 넘어온 색을 pcss톤 12개로 만들어서 돌려준다

		hsl : [색상, 채도, 밝기], rgb : [빨강의 농도, 초록의 농도, 파랑의 농도]
		rgbint = rgb[0] + rgb[1] * 256 + rgb[2] * (256 ** 2)

		:param rgb:
		:return:
		"""
		result = []
		h, s, l = self.change_rgb_to_hsl(rgb)
		result4 = self.vars["basic_12color_hsl"]
		for one in result4:
			result.append([h, one[0], one[1]])
		return result

	def change_rgb_to_close_excel56(self, input_rgb):
		"""
		입력으로 들어오는 RGB값중에서 엑셀의 56가지 기본색상의 RGB값과 가장 가까운값을 찾아내는것

		:param input_rgb:
		:return:
		"""
		result = 0
		max_rgbint = 255 * 255 * 255
		var_56_rgb = self.vars["excel56_vs_rgb"]

		for excel_color_no in var_56_rgb.keys():
			excel_rgb = var_56_rgb[excel_color_no]
			differ = self.calculate_distance_two_3d_point(input_rgb, excel_rgb)
			if max_rgbint > differ:
				max_rgbint = differ
				result = excel_color_no
		return result

	def change_rgb_to_close_highlight_no(self, input_rgb):
		result = 0
		max_rgbint = 255 * 255 * 255
		var_56_rgb = self.vars["highlight_vs_rgb"]

		for excel_color_no in var_56_rgb.keys():
			excel_rgb = var_56_rgb[excel_color_no]
			differ = self.calculate_distance_two_3d_point(input_rgb, excel_rgb)
			if max_rgbint > differ:
				max_rgbint = differ
				result = excel_color_no
		return result

	def change_rgb_to_hex(self, rgb):
		"""
		엑셀의 Cells(1, i).Interior.Color는 hex값을 사용한다

		:param rgb:
		:return:
		"""

		result = f"#{int(round(rgb[0])):02x}{int(round(rgb[1])):02x}{int(round(rgb[2])):02x}"
		return result

	def change_rgb_to_hsl(self, rgb):
		"""
		rgb를 hsl로 바꾸는 것이다

		:param rgb:  [r,g,b]값[r,g,b]값
		:return:
		"""
		r = float(rgb[0] / 255)
		g = float(rgb[1] / 255)
		b = float(rgb[2] / 255)
		max1 = max(r, g, b)
		min1 = min(r, g, b)
		l = (max1 + min1) / 2

		if max1 == min1:
			s = 0
		elif l < 0.5:
			s = (max1 - min1) / (max1 + min1)
		else:
			s = (max1 - min1) / (2 - max1 - min1)

		if s == 0:
			h = 0
		elif r >= max(g, b):
			h = (g - b) / (max1 - min1)
		elif g >= max(r, b):
			h = 2 + (b - r) / (max1 - min1)
		else:
			h = 4 + (r - g) / (max1 - min1)
		h = h * 60
		if h > 360:
			h = h - 360
		if h < 0:
			h = 360 - h

		return [int(h), int(s * 100), int(l * 100)]

	def change_rgb_to_rgbint(self, rgb):
		"""
		rgb인 값을 color에서 인식이 가능한 정수값으로 변경하는 것
		엑셀에서는 rgb형태의 리스트나 정수를 사용하여 색을 지정한다

		:param rgb:  [r,g,b]값
		:return:
		"""
		result = int(rgb[0]) + (int(rgb[1])) * 256 + (int(rgb[2]))* (256 ** 2)
		return result

	def change_rgbint_to_color_name(self, rgbint):
		"""
		rgb의 정수값을 color이름으로 변경

		:param rgbint: change rgb value to int, rgb를 정수로 변환한 값
		:return:
		"""
		try:
			rgblist = self.change_rgbint_to_rgb(rgbint)
			color_index = self.change_rgb_to_close_excel56(rgblist)
			colorname = self.change_excel56_to_color_name(color_index)
		except:
			colorname = None
		return colorname

	def change_rgbint_to_hsl(self, input_rgbint):
		"""
		정수형태의 int값을 [h,s,l]의 리스트형태로 바꾸는 것

		:param input_rgbint: rgb의 정수값
		:return:
		"""
		rgb = self.change_rgbint_to_rgb(input_rgbint)
		hsl = self.change_rgb_to_hsl(rgb)
		return hsl

	def change_rgbint_to_rgb(self, input_rgbint):
		"""
		정수형태의 int값을 [r,g,b]의 리스트형태로 바꾸는 것

		:param input_rgbint: rgb의 정수값
		:return:
		"""
		mok0, namuji0 = divmod(input_rgbint, 256 * 256)
		mok1, namuji1 = divmod(namuji0, 256)
		result = [namuji1, mok1, mok0]
		return result

	def change_scolor_to_5_rgb_for_pastel(self, input_scolor):
		"""
		기본적인 pastel은 [s, l] = [100, 90] 정도이다
		:param input_scolor:
		:return:
		"""

		result =[]
		h, s, l = self._change_scolor_to_hsl(input_scolor)

		for strong_level in [0.97, 0.95, 0.93, 0.9, 0.87]:
			new_hsl = [h, 100 * strong_level, 90 * strong_level]
			result.append(self.change_hsl_to_rgb(new_hsl))
		return result

	def change_scolor_to_any_color(self, input_scolor):
		result ={}
		rgbint = self.change_scolor_to_rgbint(input_scolor)
		rgb= self.change_scolor_to_rgb(input_scolor)
		hsl= self._change_scolor_to_hsl(input_scolor)
		hex = self.change_scolor_to_hex(input_scolor)
		excel56 = self.change_rgb_to_close_excel56(rgb)
		highlight_no = self.change_rgb_to_close_highlight_no(rgb)
		result["rgbint"] =rgbint
		result["rgb"] = rgb
		result["hsl"] = hsl
		result["hex"] = hex
		result["excel56"] = excel56
		result["highlight_no"] = highlight_no
		return result

	def change_scolor_as_bright_by_0to1(self, input_scolor, step1=.3):
		hsl = self._change_scolor_to_hsl(input_scolor)
		if step1 < 1: step1 = step1 *100

		basic_value = hsl[2]
		max_value = 100
		changed_value = (max_value - basic_value) * step1 + basic_value

		result = [hsl[0], hsl[1], changed_value]
		return result

	def change_scolor_to_close_excel56(self, input_scolor):
		"""
		scolor형식 : 12, "red", "red45", "red++"

		:param input_scolor: solor형태의 색깔입력, (12, "red", "red45", "red++")
		:return:
		"""
		rgb_value = self.change_scolor_to_rgb(input_scolor)
		result = self.change_rgb_to_close_excel56(rgb_value)
		return result

	def change_scolor_as_dark_by_0to1(self, input_scolor, step1=.3):
		hsl = self._change_scolor_to_hsl(input_scolor)
		if step1 < 1: step1 = step1 * 100

		basic_value = hsl[2]
		changed_value = basic_value * step1

		result = [hsl[0], hsl[1], changed_value]
		return result

	def change_scolor_to_hex(self, input_scolor):
		"""
		scolor값을 16진수인 hex로 변경하는 것
		scolor형식 : 12, "red", "red45", "red++"

		:param input_scolor:
		:return:
		"""
		my_rgb_color = self.change_scolor_to_rgb(input_scolor)
		result = self.change_rgb_to_hex(my_rgb_color)
		return result

	def change_scolor_to_hsl(self, input_scolor):
		"""
		입력된 자료를 기준으로 hsl값을 돌려주는것
		scolor형식 : 12, "red", "red45", "red++"

		:param input_scolor: solor형태의 색깔입력
		:return: [h, s, l]
		"""

		result = self._change_scolor_to_hsl(input_scolor)
		return result

	def change_scolor_to_nth_near_rgb_set(self, input_color="red", step=10):
		"""
		하나의 색을 지정하면 10가지의 단계로 색을 돌려주는 것이다
		scolor형식 : 12, "red", "red45", "red++"

		:param input_color:
		:param step:
		:return:
		"""
		result = []
		for no in range(0, 100, int(100 / step)):
			temp = self.change_scolor_to_rgb(input_color + str(no))
			result.append(temp)
		return result

	def change_scolor_as_pastel_style_by_0to1(self, input_scolor, step1=.3):
		"""
		** 추루 사용하지 말아주세요
		control의 의미는 입력의 자료형태를 그대로 유지하면서 미세 조정을 하는것인데, 이것은 다른 의미이므로 사용을 저제 하여 주시기 바랍니다

		level1 : 0~1사이의 값
		scolor값을 파스텔톤으로 변경한후, 명도를 조절하는 것

		:param input_scolor: solor형태의 색깔입력, (12, "red", "red45", "red++")
		:param my_value:
		:return:
		"""
		hsl = self._change_scolor_to_hsl(input_scolor)
		result = self.change_hsl_as_pastel_style(hsl, step1)
		return result

	def change_scolor_as_pastel_style_by_1to3(self, input_scolor, level1to3=2):
		"""
		입력받은 색의 값을 파스텔의 3가지 강도로 변경하는 방법
		level1to3 : 1~3 사이의 값
		pastel_style : ["연한", "밝은회색", "회색", "어두운회색", "옅은", "부드러운", "탁한", "어두운", "밝은", "강한", "짙은", "선명한"]
						basic_data의 self.vars["check_color_tone"] 를 이용해서 pastel_style의 공식적인 이름을 찾읍니다
		pastel의 0에서 100 : 중간값(sl) [100, 85]

		:return:
		"""
		level = [[95, 80], [100, 85], [90,90]] # 약, 중, 강
		hsl = self.change_scolor_to_hsl(input_scolor)
		h, s, l = hsl
		s = level[level1to3 -1][0]
		l = level[level1to3 -1][1]
		result = self.change_hsl_to_rgb([h, s, l])
		return result

	def change_scolor_to_rgb(self, input_scolor):
		"""
		scolor값을 rgb값으로 변경
		scolor형식 : 12, "red", "red45", "red++"

		:param input_scolor: solor형태의 색깔입력, (12, "red", "red45", "red++")
		"""
		hsl_list = self._change_scolor_to_hsl(input_scolor)
		result = self.change_hsl_to_rgb(hsl_list)
		return result

	def change_scolor_to_rgb_as_pccs_style_by_level10(self, input_scolor="red45", color_style="파스텔", style_step=5):
		"""
		입력된 기본 값을 스타일에 맞도록 바꾸고, 스타일을 강하게 할것인지 아닌것인지를 보는것
		scolor형식 : 12, "red", "red45", "red++"

		입력예 : 기본색상, 적용스타일, 변화정도,("red45, 파스텔, 3)

		:param input_scolor: solor형태의 색깔입력, (12, "red", "red45", "red++")
		:param color_style: pccs의 12가지 사용가능, 숫자로 사용가능, +-의 형태로도 사용가능
		:param style_step: 변화정도는 5를 기준으로 1~9까지임
		"""
		basic_hsl = self._change_scolor_to_hsl(input_scolor)
		checked_color_style = self.vars["check_color_tone"][color_style]

		step_2 = self.vars["basic_15tone_eng_vs_sl"][checked_color_style]
		step_1 = self.vars["basic_9color_sl_big_step"][int(style_step)]

		h = int(basic_hsl[0])
		s = int(basic_hsl[1]) + int(step_1[0]) + int(step_2[0])
		l = int(basic_hsl[2]) + int(step_1[1]) + int(step_2[1])

		changed_rgb = self.change_hsl_to_rgb([h, s, l])
		return changed_rgb

	def change_scolor_to_rgbint(self, input_scolor):
		"""
		scolor값을 rgbint로 변경
		scolor형식 : 12, "red", "red45", "red++"
		"""
		rgb_list = self.change_scolor_to_rgb(input_scolor)
		result = self.change_rgb_to_rgbint(rgb_list)
		return result

	def change_scolor_as_vivid_by_0to1(self, input_scolor, step1=.3):
		"""
		** 추후 사용하지 말아주세요
		control의 의미는 입력의 자료형태를 그대로 유지하면서 미세 조정을 하는것인데, 이것은 다른 의미이므로 사용을 저제 하여 주시기 바랍니다

		vivid : 생생한, 밝은
		level1 : 0~1사이의 값

		:param input_scolor: solor형태의 색깔입력, (12, "red", "red45", "red++")
		:param my_value:
		:return:
		"""
		hsl = self._change_scolor_to_hsl(input_scolor)
		result = self.change_hsl_as_vivid_by_0to1(hsl, step1)
		return result

	def change_style(self, input_scolor, style_name):
		"""
		자주 사용하는 형태라서 입력되는 색을 pccs스타일중의 하나로 변경하는 것

		:param input_scolor: solor형태의 색깔입력, (12, "red", "red45", "red++")
		:param style_name:
		:return:
		"""
		hsl = self._change_scolor_to_hsl(input_scolor)
		plusminus100 = self.vars["check_color_step"][style_name]
		result = self.change_hsl_to_rgb_by_plusminus100(hsl, plusminus100)
		return result

	def check_color_name(self, input_value):
		result = self.vars["check_color_name"][input_value]
		return result

	def check_color_name_by_rgbint(self, rgbint):
		"""
		예전 코드를 위해 남겨 놓는것

		original : change_rgbint_to_colorname
		"""
		result = self.change_rgbint_to_color_name(rgbint)
		return result

	def check_color_name_for_input_color(self, input_color):
		"""
		입력으로 들어오는 색이름을 확인해 주는 것

		:param input_list:
		:return:
		"""
		result = False
		result = self.check_color_name(input_color)
		return result

	def check_input_color(self, input_value):
		"""
		입력으로 들어오는 색을 확인하는 것
		:param input_value:
		:return:
		"""
		if type(input_value) == type([]):
			if input_value[1] > 100 or input_value[2] > 100:
				hsl = self.change_rgb_to_hsl(input_value)
			else:
				hsl = input_value
		else:
			hsl = self.check_input_scolor(input_value)
		return hsl

	def check_input_hsl(self, input_color):
		"""
		입력으로 들어온 색에 대한 hsl값을 돌려준다

		:param input_color:
		:return:
		"""
		result = hsl = self.check_input_scolor(input_color)
		return result

	def check_input_rgb(self, input_value):
		"""
		입력값이 rgbint인지 rgb리스트인지를 확인후 돌려주는것
		결과값 : [r,g,b]의 형식

		:param input_value: rgb의 값
		:return: [r,g,b]의 형식으로 돌려주는 것
		"""
		if type(input_value) == type(123):
			rgb = self.change_rgbint_to_rgb(input_value)
		else:
			rgb = input_value
		return rgb

	def check_input_scolor(self, input_scolor):
		"""
		scolor형식의 입력값을 확인하는 것이다
		scolor형식 : 12, "red", "red45", "red++"

		:param input_scolor: solor형태의 색깔입력, (12, "red", "red45", "red++")
		:return: ["숫자만","색이름","변화정도"] ==> ["","red","60"]
		"""
		#잘못입력했을때를 대비하여 기본값을 넣는것
		color_name = "bla"
		l_value = 50
		value_only = None

		#영어나 한글로 된 색깔이름을 추출
		re_com1 = re.compile("[a-zA-Z_가-힣]+")
		scolor_color = re_com1.findall(input_scolor)

		# scolor에서 숫자만 추출
		re_com2 = re.compile("[0-9]+")
		scolor_no = re_com2.findall(input_scolor)

		# scolor에서 + 추출
		re_com3 = re.compile("[+]+")
		scolor_plus = re_com3.findall(input_scolor)

		# scolor에서 - 추출
		re_com4 = re.compile("[-]+")
		scolor_minus = re_com4.findall(input_scolor)

		#print("scolor_no", scolor_no)

		#숫자만 입력이 되었을때
		if scolor_no and str(scolor_no) == str(input_scolor):
			value_only = int(input_scolor)
			color_name = None
			l_value = None
		else:
			if scolor_color:
				if scolor_color[0] in self.vars["check_color_name"].keys():
					color_name = self.vars["check_color_name"][scolor_color[0]]
				else:
					color_name = "not_found_" + str(scolor_color[0])

			if scolor_no:
				l_value = int(scolor_no[0])
			elif scolor_plus:
				l_value = 50 + 5 * len(scolor_plus[0])  # +를 10개까지 사용가능하며, 숫자로 바꾸는것
			elif scolor_minus:
				l_value = 50 - 5 * len(scolor_minus[0])  # -를 10개까지 사용가능하며, 숫자로 바꾸는것

		return [value_only, color_name, l_value]

	def check_plusminus100(self, plusminus100):
		"""

		:param plusminus100:
		:return:
		"""
		result = ""
		if type(plusminus100) == type([]):
			result = plusminus100
		elif "+" == str(plusminus100)[0]:
			# 현재의 값에서 10만큼 밝아지도록 한다
			l_value = 10 * len(plusminus100)
			result = [0, 0, l_value]
		elif "-" == str(plusminus100)[0]:
			# 현재의 값에서 10만큼 어두워지도록 한다
			l_value = -10 * len(plusminus100)
			result = [0, 0, l_value]
		elif plusminus100 in self.vars["tone_vs_index"].keys():
			no = self.vars["tone_vs_index"][plusminus100]
			result = self.vars["basic_9color_sl_big_step"][no]
		return result

	def control_hsl(self, hsl, position, strength=50):
		"""
		입력된 hsl값의 일부분을 변경하는 것

		(고) high = 80, (중) middle = 50, (저) low=20

		:param hsl: [h,s,l]형식의 값
		:param position: h,s,l중에 한다
		:return:
		"""
		dic_data = {"high": 80, "middle": 50, "low": 20}

		if type(strength) == type(123):
			pass
		elif strength in dic_data.keys():
			strength = dic_data[strength]

		if position == "h":
			result = hsl[0] = strength
		elif position == "s":
			result = hsl[1] = strength
		elif position == "l":
			result = hsl[2] = strength
		return result

	def data_for_color_name_all(self):
		"""
		모든 색깔의 이름들
		"""
		result = list(set(self.vars["check_color_name"].values()))
		return result

	def data_for_color_name_kor_basic(self):
		"""
		12가지 기본색이름(한글)
		:return:
		"""
		result = self.vars["color12_kor"]
		return result

	def data_for_color_name_12(self):
		"""
		12가지 영어 색깔이름을 돌려준다
		"""
		result = self.vars["color12"]
		return result

	def data_for_color_tone_kor_12(self):
		"""
		칼라톤에 대한 한글이름
		"""
		result = self.vars["color12_kor"]
		return result

	def data_for_contrast_2set_8(self):
		"""
		대비가 잘되는 8가지 배경과 텍스트를 위한 색조합
		:return:
		"""
		result = [ [[239, 68, 68],[255,255,255]],
					[[250, 163, 27],[0,0,0]],
					[[255, 240, 0],[0,0,0]],
					[[130, 195, 65],[0,0,0]],
					[[0, 159, 117],[255,255,255]],
					[[136, 198, 237],[0,0,0]],
					[[57,75,160],[255,255,255]],
					 [[231, 71, 153],[255,255,255]],
					]
		return result

	def data_for_excel_rgb46(self):
		"""
		엑셀 기본 46 rgb 값
		"""
		result = self.vars["excel46_rgb"]
		return result

	def data_for_excel_rgb56(self):
		"""
		엑셀 기본 56 rgb 값
		"""
		result = self.vars["excel56_rgb"]
		return result

	def data_for_hilight_7(self):
		"""
		하이라이트로 사용가능할 만한 7가지 색을 만든것
		:return:
		"""
		result = [[240, 117, 117], [240, 178, 117], [240, 240, 117], [178, 240, 117], [117, 240, 118], [117, 240, 179],	 [117, 239, 240]]
		return result

	def data_for_hsl_12(self):
		"""
		12가지 hsl의 값

		:return:
		"""
		result = self.vars["color12_hsl"]
		return result

	def data_for_hsl_36(self):
		"""
		기본적인 hsl로된 36색을 갖고온다
		빨간색을 0으로하여 시작한다
		"""
		result = []
		for one in range(0, 360, 10):
			temp = [one, 100, 50]
			result.append(temp)
		return result

	def data_for_hsl_4356(self):
		"""
		h : 36가지
		s : 11단계
		l : 11단계
		총 4356개의 색집합

		:return:
		"""
		result = {}
		for h in range(0, 360, 10):
			for s in range(0, 110, 10):
				for l in range(0, 110, 10):
					temp = self.change_hsl_to_rgb([h, s, l])
					result[str(h) + str("_") + str(s) + str("_") + str(l)] = temp
		return result

	def data_for_pastel_color_12(self):
		result = []
		for num in range(0, 360, 30):
			result.append(self.change_hsl_to_rgb([num, 90, 80]))
		return result

	def data_for_pastel_rgb_8(self):
		"""
		기본적인 자료가 있는 색들의 배경색으로 사용하면 좋은 색들
		"""
		color_set = self.vars["color12_hsl"][:-4]
		result = []
		for hsl_value in color_set:
			rgb = self.change_scolor_to_rgb_as_pccs_style_by_level10(hsl_value, "pastel", 4)
			result.append(rgb)
		return result

	def data_for_pccs_by_hsl_12(self, hsl):
		"""
		12가지 스타일의 hsl을 돌려주는 것이다

		:param hsl: [h,s,l]형식의 값
		"""
		result = []
		for one_value in self.vars["color12_hsl"]:
			temp = self.change_hsl_to_rgb([hsl[0], one_value[0], one_value[1]])
			result.append(temp)
		return result

	def data_for_pccs_name_12(self):
		"""
		pccs(퍼스널컬러)의 영어 12가지 이름
		"""
		result = ['white', 'vivid', 'soft', 'deep', 'pale', 'gray', 'darkgrayish', 'grayish', 'lightgrayish',
					 'strong', 'light', 'bright', 'black', 'dull', 'dark']
		return result

	def data_for_pccs_name_kor_12(self):
		"""
		pccs(퍼스널컬러)의 한글 12가지 이름
		"""
		result = ['밝은', '기본', '파스텔', '부드러운', '검정', '연한', '탁한', '어두운', '밝은회색', '검은', '짙은', '강한', '회색', '진한', '옅은',
					 '어두운회색', '흐린', '선명한']

		return result

	def data_for_rgb_12(self):
		"""
		기본 12가지 색에 대한 rgb 리스트 값
		"""
		result = self.vars["color12_rgb"]
		return result

	def find_near_list(self, rgb_list, target_rgb):
		"""
		주어진 RGB의 형태로 만든 리스트에서
		타겟 RGB와 어느 값에 가장 가까운 RGB 값인지를 찾는것
		꼭 3차원이 아닌 4차원, 5차원의 자료들도 가능하다

		:param rgb_list:
		:param target_rgb:
		:return:
		"""
		result = None
		min_distance = float('inf') #파이썬에서 양의 무한대를 나타내는 방법
		for rgb in rgb_list:
			distance = self.euclidean_distance(rgb, target_rgb)
			if distance < min_distance:
				min_distance = distance
				result = rgb
		return result

	def get_4_rgb_for_input_hsl_by_step_of_90h(self, hsl):
		"""
		360도의 색을 90도씩 변하는 4단계로 나누어서 돌려주는 것

		:param hsl: [h,s,l]형식의 값
		:return:
		"""
		h, s, l = hsl

		new_h_1 = divmod(h + 0, 360)[1]
		new_h_2 = divmod(h + 90, 360)[1]
		new_h_3 = divmod(h + 180, 360)[1]
		new_h_4 = divmod(h + 270, 360)[1]
		rgb_1 = self.change_hsl_to_rgb([new_h_1, s, l])
		rgb_2 = self.change_hsl_to_rgb([new_h_2, s, l])
		rgb_3 = self.change_hsl_to_rgb([new_h_3, s, l])
		rgb_4 = self.change_hsl_to_rgb([new_h_4, s, l])
		result = [rgb_1, rgb_2, rgb_3, rgb_4]

		return result

	def get_8_rgb_as_contrast_for_backgound_n_text(self):
		result = [ [[239, 68, 68],[255,255,255]],
					[[250, 163, 27],[0,0,0]],
					[[255, 240, 0],[0,0,0]],
					[[130, 195, 65],[0,0,0]],
					[[0, 159, 117],[255,255,255]],
					[[136, 198, 237],[0,0,0]],
					[[57,75,160],[255,255,255]],
					 [[231, 71, 153],[255,255,255]],
					]
		return result

	def get_basic_12_color_name_list_by_kor(self):
		result = self.vars["color12_kor"]
		return result

	def get_color_name_for_rgbint(self, rgbint):
		"""
		rgb의 정수값을 color이름으로 변경

		scolor로 이동
		:param rgbint: rgb를 정수로 변환한 값
		"""
		try:
			rgblist = self.change_rgbint_to_rgb(rgbint)
			color_index = self.change_rgb_to_close_excel56(rgblist)
			colorname = self.change_excel56_to_color_name(color_index)
		except:
			colorname = None
		return colorname

	def get_color_name_list_for_cool_style(self):
		"""
		차가운 색깔의 이름들
		"""
		result = ["파랑", "초록", "보라"]
		return result

	def get_color_name_list_for_worm_style(self):
		"""
		따뜻한 색깔의 이름들

		:return:
		"""
		result = ["빨강", "주황", "노랑"]
		return result

	def get_nth_hsl_from_input_hsl_by_step_of_h(self, hsl, input_nth=10):
		result = []
		for no in range(1, 361, input_nth):
			temp = [no, hsl[1], hsl[2]]
			result.append(temp)
		return result

	def get_nth_hsl_from_input_hsl_by_step_of_l(self, hsl, input_nth=10):
		result = []
		step = int(100/input_nth)
		for no in range(1, 101, step):
			temp = [hsl[0], hsl[1], no]
			result.append(temp)
		return result

	def get_nth_hsl_from_input_hsl_by_step_of_s(self, hsl, input_nth=10):
		result = []
		step = int(100/input_nth)
		for no in range(1, 101, step):
			temp = [hsl[0], no, hsl[2]]
			result.append(temp)
		return result

	def get_nth_rgb_between_scolor1_to_scolor2_by_step(self, scolor_1, scolor_2, step=10):
		"""
		두가지색을 기준으로 몇단계로 색을 만들어주는 기능
		예를들어, 발강 ~파랑사이의 색을 10단계로 만들어 주는 기능

		:param scolor_1:
		:param scolor_2:
		:param step:
		:return:
		"""
		rgb_1 = self.change_scolor_to_rgb(scolor_1)
		rgb_2 = self.change_scolor_to_rgb(scolor_2)
		r_step = int((rgb_2[0] - rgb_1[0]) / step)
		g_step = int((rgb_2[1] - rgb_1[1]) / step)
		b_step = int((rgb_2[2] - rgb_1[2]) / step)
		result = [rgb_1, ]
		for no in range(1, step - 1):
			new_r = int(rgb_1[0] + r_step * no)
			new_g = int(rgb_1[1] + g_step * no)
			new_b = int(rgb_1[2] + b_step * no)
			result.append([new_r, new_g, new_b])
		result.append(rgb_2)
		return result

	def get_nth_rgb_by_step_of_h(self, input_no=36):
		"""
		입력된 숫자만큼, rgt리스트를 갖고오는것
		기본적인 hsl로된 36색을 갖고온다
		빨간색을 0으로하여 시작한다
		결과값 : hsl

		:param input_no:
		:return:
		"""
		result = []
		for one in range(0, 360, int(360 / input_no)):
			temp = self.change_hsl_to_rgb([one, 100, 50])
			result.append(temp)
		return result

	def get_nth_rgb_from_input_hsl_by_step_of_s(self, hsl, step=10):
		"""
		위쪽으로 5개, 아래로 5개의 채도가 비슷한 색을 돌려준다
		채도의 특성상 비슷한 부분이 많아서 10단위로 만든다

		:param hsl: [h,s,l]형식의 값
		:param step:
		:return:
		"""
		h, s, l = hsl
		result = []
		for no in range(0, 100 + step, step):
			# print("변경된 hsl은 s=> ", [h, no, l])
			temp = self.change_hsl_to_rgb([h, no, l])
			result.append(temp)
		return result

	def get_rgb_at_input_pxy(self, input_pxy=""):
		"""
		pyclick에 같은 것 있음

		입력으로 들어오는 pxy위치의 rgb값을 갖고온다
		만약 "" 이면, 현재 마우스가 위치한곳의 rgb를 갖고온다
		:param input_pxy:
		:return:
		"""
		if input_pxy:
			x, y = input_pxy
		else:
			x, y = pyautogui.position()
		r, g, b = pyautogui.pixel(x, y)
		return [r,g,b]

	def get_rgb_by_bo_style_for_input_hsl(self, hsl):
		"""
		입력된 hsl에 대한 보색을 알려주는것
		보색 : Complementary
		2차원 list의 형태로 돌려줌

		:param hsl: [h,s,l]형식의 값
		:return:
		"""

		new_h = divmod(hsl[0] + 180, 360)[1]
		result = self.change_hsl_to_rgb([new_h, hsl[1], hsl[2]])
		return [result]

	def get_rgb_set_for_faber(self, start_color=11, code=5):
		"""
		파버 비덴의의 색체 조화론을 코드로 만든것이다
		한가지 색에대한 조화를 다룬것

		White(100-0) - Tone(10-50) - Color(0-0) : 색이 밝고 화사
		Color(0-0) - Shade(0-75) - Black(0-100) : 색이 섬세하고 풍부
		White(100-0) - GrayGray(25-75) - Black(0-100) : 무채색의 조화
		Tint(25-0) - Tone(10-50) - Shade(0-75) 의 조화가 가장 감동적이며 세련됨
		White(100-0) - Color(0-0) - Black(0-100) 는 기본적인 구조로 전체적으로 조화로움
		Tint(25-0) - Tone(10-50) - Shade(0-75) - Gray(25-75) 의 조화는 빨강, 주황, 노랑, 초록, 파랑, 보라와 모두 조화를 이룬다

		:param start_color:
		:param code:
		:return:
		"""
		h_list = self.vars["color12_hsl"]
		sl_faber = self.vars["faber_to_sl"]

		h_no = h_list[start_color][0]
		result = []
		temp_hsl = sl_faber[code]
		for one_sl in temp_hsl:
			rgb = self.change_hsl_to_rgb([h_no, one_sl[0], one_sl[1]])
			result.append(rgb)
		return result

	def get_rgb_set_for_highlight_7(self):
		result = []
		for num in range(0, 200, 30):
			result.append(self.change_hsl_to_rgb([num, 80, 70]))
		return result

	def get_rgb_set_for_johannes(self, start_color=11, num_color=4, stongness=5):
		"""
		요하네스 이텐의 색체 조화론을 코드로 만든것이다

		:param start_color: 처음 시작하는 색 번호, 총 색은 12색으로 한다
		:param num_color: 표현할 색의 갯수(2, 3, 4, 6만 사용가능)
		:param stongness: 색의 농도를 나타내는 것, 검정에서 하양까지의 11단계를 나타낸것, 중간이 5이다
		:return:
		"""
		h_list = self.vars["color12_hsl"]
		sl_list = self.vars["sl11_step"]
		hsl_johannes = self.vars["johannes_to_hsl"]
		color_set = [[], [], [0, 6], [0, 5, 9], [0, 4, 7, 10], [0, 3, 5, 8, 10], [0, 3, 5, 7, 9, 11]]

		h_no = h_list[start_color][0]
		new_color_set = []
		for temp in color_set[num_color]:
			new_color_set.append((temp + int(h_no / 30)) % 12)

		result = []
		for no in new_color_set:
			temp_hsl = hsl_johannes[no][stongness]
			rgb = self.change_hsl_to_rgb(temp_hsl)
			result.append(rgb)
		return result

	def is_scolor_style(self, input_scolor):
		"""
		scolor용
		입력된 자료의 형태가, scolor형식인지를 확인하는 것
		"""

		result1 = self.xyre.is_match_all("[한글&영어:2~10][숫자:0~7]", str(input_scolor))
		result2 = self.xyre.is_match_all("[한글&영어:2~10][+-:0~7]", str(input_scolor))
		if result1 and result2:
			result = result1
		elif result1 and not result2:
			result = result1
		elif not result1 and result2:
			result = result2
		elif not result1 and not result2:
			result = False

		return result

	def terms(self):
		"""
		간략한 용어정리
		"""
		result = """
		color_style : 파스텔 톤과 같은것
		scolor      : 색을 blu와 같이 3글자의 영문 시작 색이름으로 하고, 그 농도를 숫자나 +-기호로 변경하는것, 예: blu++, blu55
		pccs_style  : 일본색체연구서가 발표한 12가지 색으로 구분한것, 톤에 대한 12가지 구분, 연한, 밝은회색, 회색, 어두운회색, 옅은, 부드러운, 탁한, 어두운, 밝은, 강한, 짙은, 선명한
		hsl         : 색을 표현하는 기법중 하나, HSL(hue, saturation, lightness, 즉 색상, 채도, 밝기)
		excel56     : 엑셀의 기본 56가지색
		rgbint      : rgb값을 정수로 변경한것
		control     : 입력으로 들어오는 값의 형태는 같으면서, 조건에따라서 변경을 하는것
		level1      : 0~1까지의 값변화로 조정하는 것
		level100    : 0~100까지의 값변화로 조정하는 것
		plusminus100 : ++, --, 70등의 값이 들어오면 변화를 시켜주는 것
		data_로_시작_되는_단어 : 주로 사용되는 자료들을 쉽게 읽어올수있도록 만든것
		step_by_aaa : aaa에 대한 일정 간격마다
		hsl : [색상, 채도, 밝기], 
		rgb : [빨강의 농도, 초록의 농도, 파랑의 농도], 
		rgbint = rgb[0] + rgb[1] * 256 + rgb[2] * (256 ** 2)
		"""
		return result


