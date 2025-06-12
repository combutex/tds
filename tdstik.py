#Coded by Traodoisub.com
import os
from time import sleep
from datetime import datetime
import io
from contextlib import redirect_stdout
import sys
import re

os.environ['TZ'] = 'Asia/Ho_Chi_Minh'

try:
	import requests
except:
	os.system("pip3 install requests")
	import requests

try:
	from pystyle import Colors, Colorate, Write, Center, Add, Box
except:
	os.system("pip3 install pystyle")
	from pystyle import Colors, Colorate, Write, Center, Add, Box

headers = {
	'authority': 'traodoisub.com',
	'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
	'accept-language': 'en-US,en;q=0.9,vi;q=0.8',
	'user-agent': 'traodoisub tiktok tool',
}

def login_tds(token):
	try:
		r = requests.get('https://traodoisub.com/api/?fields=profile&access_token='+token, headers=headers, timeout=5).json()
		if 'success' in r:
			os.system('clear')
			print(Colors.green + f"Đăng nhập thành công!\nUser: {Colors.yellow + r['data']['user'] + Colors.green} | Xu hiện tại: {Colors.yellow + r['data']['xu']}")
			return 'success'
		else:
			print(Colors.red + f"Token TDS không hợp lệ, hãy kiểm tra lại!\n")
			return 'error_token'
	except:
		return 'error'

def load_job(type_job, token):
	try:
		r = requests.get('https://traodoisub.com/api/?fields='+type_job+'&access_token='+token, headers=headers, timeout=5).json()
		if 'data' in r:
			return r
		elif "countdown" in r:
			sleep(round(r['countdown']))
			print(Colors.red + f"{r['error']}\n")
			return 'error_countdown'
		else:
			print(Colors.red + f"{r['error']}\n")
			return 'error_error'
	except:
		return 'error'

def duyet_job(type_job, token, uid):
	try:
		r = requests.get(f'https://traodoisub.com/api/coin/?type={type_job}&id={uid}&access_token={token}', headers=headers, timeout=5).json()
		if "cache" in r:
			return r['cache']
		elif "success" in r:
			dai = f'{Colors.yellow}------------------------------------------'
			print(dai)
			print(f"{Colors.cyan}Nhận thành công {r['data']['job_success']} nhiệm vụ | {Colors.green}{r['data']['msg']} | {Colors.yellow}{r['data']['xu']}")
			print(dai)
			return 'error'
		else:
			print(f"{Colors.red}{r['error']}")
			return 'error'
	except:
		return 'error'


def check_tiktok(id_tiktok, token):
	try:
		r = requests.get('https://traodoisub.com/api/?fields=tiktok_run&id='+id_tiktok+'&access_token='+token, headers=headers, timeout=5).json()
		if 'success' in r:
			os.system('clear')
			print(Colors.green + f"{r['data']['msg']}|ID: {Colors.yellow + r['data']['id'] + Colors.green}")
			return 'success'
		else:
			print(Colors.red + f"{r['error']}\n")
			return 'error_token'
	except:
		return 'error'

def chon_id_tiktok():
	ids = []
	try:
		with open('tiktok_ids.txt', 'r') as f:
			for line in f:
				if '|' in line:
					id_, username = line.strip().split('|', 1)
					ids.append((id_, username))
				elif line.strip():
					ids.append((line.strip(), ''))
	except FileNotFoundError:
		pass
	if ids:
		print(Colors.yellow + 'Danh sách ID TikTok đã lưu:')
		for idx, (id_, username) in enumerate(ids, 1):
			print(f'{Colors.green}{idx}. {Colors.cyan}{id_} {Colors.light_gray}| {Colors.pink}{username}')
		print(f'{Colors.green}{len(ids)+1}. {Colors.red}Nhập ID mới')
		while True:
			try:
				chon = int(Write.Input('Chọn số thứ tự ID TikTok hoặc nhập số mới:', Colors.green_to_yellow, interval=0.0025))
				if 1 <= chon <= len(ids):
					return ids[chon-1][0]
				elif chon == len(ids)+1:
					break
				else:
					print(Colors.red + 'Chỉ chọn số trong danh sách!')
			except:
				print(Colors.red + 'Chỉ chọn số trong danh sách!')
	# Nhập ID mới
	while True:
		id_new = Write.Input('Nhập ID tiktok chạy (lấy ở mục cấu hình web):', Colors.green_to_yellow, interval=0.0025)
		if id_new:
			break
	username_new = Write.Input('Nhập username TikTok tương ứng:', Colors.green_to_yellow, interval=0.0025)
	if not any(id_new == id_ for id_, _ in ids):
		luu = Write.Input('Bạn có muốn lưu ID này vào danh sách? (y/n):', Colors.green_to_yellow, interval=0.0025)
		if luu.lower() == 'y':
			with open('tiktok_ids.txt', 'a') as f:
				f.write(f'{id_new}|{username_new}\n')
	return id_new

os.system('clear')
banner = r'''
████████╗██████╗ ███████╗
╚══██╔══╝██╔══██╗██╔════╝
   ██║   ██║  ██║███████╗
   ██║   ██║  ██║╚════██║
   ██║   ██████╔╝███████║
   ╚═╝   ╚═════╝ ╚══════╝
'''
gach  = '========================================='
option = f'''{gach}{Colors.green}
Danh sách nhiệm vu tool hỗ trợ: {Colors.red}
1. Follow
2. Tym
{Colors.yellow}{gach}
'''
option_acc = f'''{gach}{Colors.green}
Danh sách lựa chọn: {Colors.red}
1. Tiếp tục sử dụng acc TDS đã lưu
2. Sử dụng acc TDS mới
{Colors.yellow}{gach}
'''
print(Colorate.Horizontal(Colors.yellow_to_red, Center.XCenter(banner)))
print(Colors.red + Center.XCenter(Box.DoubleCube("Tool TDS tiktok free version 1.0")))


while True:
	try:
		f = open(f'TDS.txt','r')
		token_tds = f.read()
		f.close()
		cache = 'old'
	except FileNotFoundError:
		token_tds = Write.Input("Nhập token TDS:", Colors.green_to_yellow, interval=0.0025)
		cache = 'new'
	
	for _ in range(3):
		check_log = login_tds(token_tds)
		if check_log == 'success' or check_log == 'error_token':
			break
		else:
			sleep(2)

	if check_log == 'success':
		if cache == 'old':
			while True:
				print(option_acc)
				try:
					choice = int(Write.Input("Lựa chọn của bạn là (Ví dụ: sử dụng acc cũ nhập 1):", Colors.green_to_yellow, interval=0.0025))
					if choice in [1,2]:
						break
					else:
						os.system('clear')
						print(Colors.red + f"Lỗi lựa chọn!! Chỉ nhập 1 hoặc 2\n")
				except:
					os.system('clear')
					print(Colors.red + f"Lỗi lựa chọn!! Chỉ nhập 1 hoặc 2\n")
			
			os.system('clear')
			if choice == 1:
				break
			else:
				os.remove('TDS.txt')

		else:
			f = open(f'TDS.txt', 'w')
			f.write(f'{token_tds}')
			f.close()
			break
	else:
		sleep(1)
		os.system('clear')

if check_log == 'success':
	#Nhập user tiktok
	while True:
		id_tiktok = chon_id_tiktok()
		for _ in range(3):
			check_log = check_tiktok(id_tiktok,token_tds)
			if check_log == 'success' or check_log == 'error_token':
				break
			else:
				sleep(2)

		if check_log == 'success':
			break
		elif check_log == 'error_token':
			os.system('clear')
			print(Colors.red + f"ID tiktok chưa được thêm vào cấu hình, vui lòng thêm vào cấu hình rồi nhập lại!\n")
		else:
			os.system('clear')
			print(Colors.red + f"Lỗi sever vui lòng nhập lại!\n")

	#Lựa chọn nhiệm vụ		
	while True:
		print(option)
		try:
			choice = int(Write.Input("Lựa chọn nhiệm vụ muốn làm (Ví dụ: Follow nhập 1):", Colors.green_to_yellow, interval=0.0025))
			if choice in [1,2]:
				break
			else:
				os.system('clear')
				print(Colors.red + f"Lỗi lựa chọn!! Chỉ nhập 1 hoặc 2\n")
		except:
			os.system('clear')
			print(Colors.red + f"Lỗi lựa chọn!! Chỉ nhập 1 hoặc 2\n")

	#Nhập delay nhiệm vụ
	while True:
		try:
			delay = int(Write.Input("Thời gian delay giữa các job (giây):", Colors.green_to_yellow, interval=0.0025))
			if delay > 1:
				break
			else:
				os.system('clear')
				print(Colors.red + f"Delay tối thiểu là 3\n")
		except:
			os.system('clear')
			print(Colors.red + f"Vui lòng nhập một số > 2\n")

	#Nhập max nhiệm vụ
	while True:
		try:
			max_job = int(Write.Input("Dừng lại khi làm được số nhiệm vụ là:", Colors.green_to_yellow, interval=0.0025))
			if max_job > 9:
				break
			else:
				os.system('clear')
				print(Colors.red + f"Tối thiểu là 10\n")
		except:
			os.system('clear')
			print(Colors.red + f"Vui lòng nhập một số > 9\n")

	os.system('clear')

	if choice == 1:
		type_load = 'tiktok_follow'
		type_duyet = 'TIKTOK_FOLLOW_CACHE'
		type_nhan = 'TIKTOK_FOLLOW'
		type_type = 'FOLLOW'
		api_type = 'TIKTOK_FOLLOW_API'
	elif choice == 2:
		type_load = 'tiktok_like'
		type_duyet = 'TIKTOK_LIKE_CACHE'
		type_nhan = 'TIKTOK_LIKE'
		api_type = 'TIKTOK_LIKE_API'
		type_type = 'TYM'

	dem_tong = 0

	while True:
		list_job = load_job(type_load, token_tds)
		sleep(2)
		if isinstance(list_job, dict) == True:
			for job in list_job['data']:
				uid = job['id']
				link = job['link']
				os.system(f'termux-open-url {link}')
				check_duyet = duyet_job(type_duyet, token_tds, uid)
				
				if check_duyet != 'error':
					dem_tong += 1
					t_now = datetime.now().strftime("%H:%M:%S")
					print(f'{Colors.yellow}[{dem_tong}] {Colors.red}| {Colors.cyan}{t_now} {Colors.red}| {Colors.pink}{type_type} {Colors.red}| {Colors.light_gray}{uid}')

					# Bổ sung lại bộ đếm thời gian ngược sau mỗi nhiệm vụ
					for i in range(delay, -1, -1):
						print(Colors.green + 'Vui lòng đợi: ' + str(i) + ' giây', end='\r')
						sleep(1)

					# Nhận xu nếu check_duyet > 9 (tránh lỗi tràn cache) và kiểm tra +0 xu
					if check_duyet > 9:
						msg = duyet_job(type_nhan, token_tds, api_type)
						# Tìm số xu nhận được trong chuỗi msg
						xu_nhan_duoc = None
						match = re.search(r'\+([0-9]+) xu', str(msg))
						if match:
							xu_nhan_duoc = int(match.group(1))
						# Nếu không match được hoặc nhận được 0 xu thì hiện menu
						if xu_nhan_duoc is None or xu_nhan_duoc == 0:
							print(Colors.red + f"\nPhát hiện ID TikTok bị hạn chế hoặc lỗi nhận xu!")
							while True:
								print(f"{Colors.yellow}Bạn muốn làm gì tiếp theo?")
								print(f"{Colors.cyan}1. Đổi ID TikTok và chạy tiếp")
								print(f"{Colors.red}2. Kết thúc chương trình")
								opt = None
								try:
									opt = int(Write.Input("Lựa chọn của bạn (1/2):", Colors.green_to_yellow, interval=0.0025))
								except:
									print(Colors.red + "Chỉ nhập 1 hoặc 2!")
									continue
								if opt == 1:
									id_tiktok = chon_id_tiktok()
									dem_tong = 0
									break
								elif opt == 2:
									print(Colors.red + "Kết thúc chương trình!")
									os._exit(0)
								else:
									print(Colors.red + "Chỉ nhập 1 hoặc 2!")

					if dem_tong == max_job:
						print(f'{Colors.green}Hoàn thành {max_job} nhiệm vụ!')
						while True:
							print(f"{Colors.yellow}Bạn muốn làm gì tiếp theo?")
							print(f"{Colors.green}1. Chạy tiếp với ID TikTok hiện tại")
							print(f"{Colors.cyan}2. Đổi ID TikTok và chạy tiếp")
							print(f"{Colors.red}3. Kết thúc chương trình")
							try:
								choice_menu = int(Write.Input("Lựa chọn của bạn (1/2/3):", Colors.green_to_yellow, interval=0.0025))
								if choice_menu == 1:
									while True:
										try:
											delay = int(Write.Input("Thời gian delay giữa các job (giây):", Colors.green_to_yellow, interval=0.0025))
											if delay > 1:
												break
											else:
												print(Colors.red + f"Delay tối thiểu là 3\n")
										except:
											print(Colors.red + f"Vui lòng nhập một số > 2\n")
									while True:
										try:
											max_job = int(Write.Input("Dừng lại khi làm được số nhiệm vụ là:", Colors.green_to_yellow, interval=0.0025))
											if max_job > 9:
												break
											else:
												print(Colors.red + f"Tối thiểu là 10\n")
										except:
											print(Colors.red + f"Vui lòng nhập một số > 9\n")
									dem_tong = 0
									os.system('clear')
									break
								elif choice_menu == 2:
									while True:
										id_tiktok = chon_id_tiktok()
										for _ in range(3):
											check_log = check_tiktok(id_tiktok,token_tds)
											if check_log == 'success' or check_log == 'error_token':
												break
											else:
												sleep(2)
										if check_log == 'success':
											break
										elif check_log == 'error_token':
											os.system('clear')
											print(Colors.red + f"ID tiktok chưa được thêm vào cấu hình, vui lòng thêm vào cấu hình rồi nhập lại!\n")
										else:
											os.system('clear')
											print(Colors.red + f"Lỗi sever vui lòng nhập lại!\n")
									while True:
										try:
											delay = int(Write.Input("Thời gian delay giữa các job (giây):", Colors.green_to_yellow, interval=0.0025))
											if delay > 1:
												break
											else:
												print(Colors.red + f"Delay tối thiểu là 3\n")
										except:
											print(Colors.red + f"Vui lòng nhập một số > 2\n")
									while True:
										try:
											max_job = int(Write.Input("Dừng lại khi làm được số nhiệm vụ là:", Colors.green_to_yellow, interval=0.0025))
											if max_job > 9:
												break
											else:
												print(Colors.red + f"Tối thiểu là 10\n")
										except:
											print(Colors.red + f"Vui lòng nhập một số > 9\n")
									dem_tong = 0
									os.system('clear')
									break
								elif choice_menu == 3:
									print(Colors.red + "Kết thúc chương trình!")
									os._exit(0)
								else:
									print(Colors.red + "Chỉ nhập 1, 2 hoặc 3!")
							except:
								print(Colors.red + "Chỉ nhập 1, 2 hoặc 3!")
								continue
