# Coded by Traodoisub.com - Re-coded for Instagram based on TikTok script
import os
from time import sleep
from datetime import datetime

# Đặt múi giờ cho chính xác (nếu cần)
os.environ['TZ'] = 'Asia/Ho_Chi_Minh'

try:
    import requests
except ImportError:
    os.system("pip3 install requests")
    import requests

try:
    from pystyle import Colors, Colorate, Write, Center, Add, Box
except ImportError:
    os.system("pip3 install pystyle")
    from pystyle import Colors, Colorate, Write, Center, Add, Box

headers = {
    'authority': 'traodoisub.com',
    'accept': 'application/json', # Đã đổi thành application/json cho API
    'accept-language': 'en-US,en;q=0.9,vi;q=0.8',
    'user-agent': 'traodoisub instagram tool',
}

def login_tds(token):
    try:
        r = requests.get('https://traodoisub.com/api/?fields=profile&access_token='+token, headers=headers, timeout=5).json()
        if 'success' in r:
            os.system('clear')
            print(Colors.green + f"Đăng nhập thành công!\nUser: {Colors.yellow + r['data']['user'] + Colors.green} | Xu hiện tại: {Colors.yellow + str(r['data']['xu'])}")
            return 'success'
        else:
            print(Colors.red + f"Token TDS không hợp lệ, hãy kiểm tra lại!\n")
            return 'error_token'
    except Exception as e:
        print(f"{Colors.red}Lỗi kết nối hoặc xử lý dữ liệu khi đăng nhập: {e}")
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
    except Exception as e:
        print(f"{Colors.red}Lỗi kết nối hoặc xử lý dữ liệu khi tải job: {e}")
        return 'error'

def duyet_job(type_job, token, uid):
    try:
        r = requests.get(f'https://traodoisub.com/api/coin/?type={type_job}&id={uid}&access_token={token}', headers=headers, timeout=5).json()
        if "cache" in r:
            # API trả về 'cache' là số, nên không cần chuyển đổi ở đây.
            # Trả về giá trị số lượng cache
            return r['cache']
        elif "success" in r:
            dai = f'{Colors.yellow}------------------------------------------'
            print(dai)
            print(f"{Colors.cyan}Nhận thành công {r['data']['job_success']} nhiệm vụ | {Colors.green}{r['data']['msg']} | {Colors.yellow}{r['data']['xu']}")
            print(dai)
            # Trả về một giá trị đặc biệt để báo hiệu đã hoàn thành và nhận xu
            return 'job_completed' 
        else:
            print(f"{Colors.red}{r['error']}")
            return 'error'
    except Exception as e:
        print(f"{Colors.red}Lỗi kết nối hoặc xử lý dữ liệu khi duyệt job: {e}")
        return 'error'

# Hàm này không còn được gọi trực tiếp trong vòng lặp chính
# vì việc nhận xu đã được xử lý trong hàm duyet_job khi API báo 'success'
# Tuy nhiên, giữ lại nếu bạn có thể cần gọi nó cho mục đích khác.
def nhan_xu_api(type_job, token, id_job):
    try:
        r = requests.get(f'https://traodoisub.com/api/coin/?type={type_job}&id={id_job}&access_token={token}', headers=headers, timeout=5).json()
        if "success" in r:
            print(f"{Colors.green}Nhận xu thành công: {r['data']['msg']} | Xu hiện tại: {Colors.yellow}{r['data']['xu']}")
            return True
        else:
            print(f"{Colors.red}Lỗi nhận xu: {r.get('error', 'Không rõ lỗi')}")
            return False
    except Exception as e:
        print(f"{Colors.red}Lỗi kết nối khi nhận xu: {e}!")
        return False

def check_instagram(id_instagram, token):
    try:
        r = requests.get('https://traodoisub.com/api/?fields=instagram_run&id='+id_instagram+'&access_token='+token, headers=headers, timeout=5).json()
        if 'success' in r:
            os.system('clear')
            print(Colors.green + f"{r['data']['msg']}|ID: {Colors.yellow + r['data']['id'] + Colors.green}")
            return 'success'
        else:
            print(Colors.red + f"{r['error']}\n")
            return 'error_token'
    except Exception as e:
        print(f"{Colors.red}Lỗi kết nối hoặc xử lý dữ liệu khi check Instagram ID: {e}")
        return 'error'

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
Danh sách nhiệm vụ tool hỗ trợ: {Colors.red}
1. Follow Instagram
{Colors.yellow}{gach}
'''
option_acc = f'''{gach}{Colors.green}
Danh sách lựa chọn: {Colors.red}
1. Tiếp tục sử dụng acc TDS đã lưu
2. Sử dụng acc TDS mới
{Colors.yellow}{gach}
'''
print(Colorate.Horizontal(Colors.yellow_to_red, Center.XCenter(banner)))
print(Colors.red + Center.XCenter(Box.DoubleCube("Tool TDS Instagram free version 1.0 (Hoàn chỉnh)")))

while True:
    try:
        f = open(f'TDS_IG.txt','r')
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
                os.remove('TDS_IG.txt')

        else:
            f = open(f'TDS_IG.txt', 'w')
            f.write(f'{token_tds}')
            f.close()
            break
    else:
        sleep(1)
        os.system('clear')

if check_log == 'success':
    # Nhập ID Instagram và tự động cấu hình nick
    while True:
        id_instagram = Write.Input("Nhập ID Instagram chạy (lấy ở mục cấu hình web):", Colors.green_to_yellow, interval=0.0025)
        for _ in range(3):
            check_log_instagram = check_instagram(id_instagram, token_tds)
            if check_log_instagram == 'success' or check_log_instagram == 'error_token':
                break
            else:
                sleep(2)

        if check_log_instagram == 'success':
            break
        elif check_log_instagram == 'error_token':
            os.system('clear')
            print(Colors.red + f"ID Instagram chưa được thêm vào cấu hình, vui lòng thêm vào cấu hình rồi nhập lại!\n")
        else:
            os.system('clear')
            print(Colors.red + f"Lỗi server vui lòng nhập lại!\n")

    # Lựa chọn nhiệm vụ (hiện tại chỉ có Follow)
    while True:
        print(option)
        try:
            choice = int(Write.Input("Lựa chọn nhiệm vụ muốn làm (Ví dụ: Follow nhập 1):", Colors.green_to_yellow, interval=0.0025))
            if choice == 1:
                break
            else:
                os.system('clear')
                print(Colors.red + f"Lỗi lựa chọn!! Chỉ nhập 1\n")
        except:
            os.system('clear')
            print(Colors.red + f"Lỗi lựa chọn!! Chỉ nhập 1\n")

    # Nhập delay nhiệm vụ
    while True:
        try:
            delay = int(Write.Input("Thời gian delay giữa các job (giây):", Colors.green_to_yellow, interval=0.0025))
            if delay > 1:
                break
            else:
                os.system('clear')
                print(Colors.red + f"Delay tối thiểu là 2\n")
        except:
            os.system('clear')
            print(Colors.red + f"Vui lòng nhập một số > 1\n")

    # Nhập max nhiệm vụ
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

    # Thiết lập các loại nhiệm vụ cho Instagram Follow
    type_load = 'instagram_follow'
    type_duyet = 'INS_FOLLOW_CACHE'
    type_nhan = 'INS_FOLLOW' # Tham số 'type' cho API nhận xu
    api_type_nhan_xu = 'INS_FOLLOW_API' # Tham số 'id' cho API nhận xu khi là INS_FOLLOW
    type_type = 'FOLLOW' # Kiểu nhiệm vụ hiển thị trên terminal

    dem_tong = 0

    while True:
        list_job = load_job(type_load, token_tds)
        sleep(2)
        # Kiểm tra list_job có phải dict, có 'data' và 'data' là list không rỗng
        if isinstance(list_job, dict) and 'data' in list_job and isinstance(list_job['data'], list) and len(list_job['data']) > 0:
            for job in list_job['data']:
                uid = job['id']
                link = job['link']
                os.system(f'termux-open-url {link}')
                
                check_duyet = duyet_job(type_duyet, token_tds, uid)
                
                # Xử lý các trường hợp trả về của hàm duyet_job
                if check_duyet == 'job_completed': # API báo đã nhận xu thành công (từ hàm duyet_job)
                    dem_tong += 1 # Vẫn tăng đếm tổng vì job đã xong
                    t_now = datetime.now().strftime("%H:%M:%S")
                    print(f'{Colors.yellow}[{dem_tong}] {Colors.red}| {Colors.cyan}{t_now} {Colors.red}| {Colors.pink}{type_type} {Colors.red}| {Colors.light_gray}{uid} {Colors.green}(Đã nhận xu)')
                    
                elif isinstance(check_duyet, int): # Nếu duyet_job trả về số lượng cache (là một số nguyên)
                    dem_tong += 1
                    t_now = datetime.now().strftime("%H:%M:%S")
                    print(f'{Colors.yellow}[{dem_tong}] {Colors.red}| {Colors.cyan}{t_now} {Colors.red}| {Colors.pink}{type_type} {Colors.red}| {Colors.light_gray}{uid}')
                    
                    if check_duyet > 9: # Kiểm tra số lượng cache có lớn hơn 9 không
                        sleep(3)
                        # Gọi API nhận xu riêng
                        nhan_xu_api(type_nhan, token_tds, api_type_nhan_xu)
                
                elif check_duyet == 'error' or check_duyet == 'error_countdown' or check_duyet == 'error_error': # Nếu có lỗi khi duyệt hoặc countdown
                    # Hàm duyet_job đã in thông báo lỗi, nên không cần in lại
                    pass 
                
                if dem_tong == max_job:
                    break
                else:
                    for i in range(delay,-1,-1):
                        print(Colors.green + 'Vui lòng đợi: '+str(i)+' giây',end=('\r'))
                        sleep(1)
        else:
            print(f"{Colors.red}Không có job nào hoặc lỗi khi tải job, vui lòng thử lại sau!")
            sleep(5)
        
        if dem_tong == max_job:
            print(f'{Colors.green}Hoàn thành {max_job} nhiệm vụ!')
            break
