import os
import mysql.connector
import json
from PIL import Image , ImageDraw, ImageFont, ImageFilter
from colorama import Fore, Back, Style
from colorama import init
import datetime

blacklist =  ["zip", "rar", "7zip", "7z", "wmv ", "mkv", "webm", "avi", "mov"]

sfile = open("settings.json")
data = json.load(sfile)
sfile.close()

def progress_bar(progress, total):
    percent = 100 * (progress / float(total))
    bar = '▉' * int(percent) + '_' * (100 - int(percent))
    print(f"\r[{bar}] {percent: .2f}% | {progress}/{total}\n", end="\r")

def getdate():
    dt = datetime.datetime.now()
    data = dt.strftime('%H:%M:%S')

    return data
os.system("cls")
print(Style.BRIGHT + Fore.BLUE + "czDevelopment "+ Fore.WHITE + "| czPTaW |" + Fore.YELLOW + " Version 0.2" + Fore.WHITE + "\n")
print(f"{getdate()} | Инициализация, обождите..")

db_host = data['db_host']
db_user = data['db_user']
db_password = data['db_password']
db_database = data['db_database']
mysql_column_to_folder = data['mysql_column_to_folder']
mysql_column_to_path = data['mysql_column_to_path']

db = mysql.connector.connect(
    host=db_host,
    user=db_user,
    password=db_password,
    database=db_database
)

cursor = db.cursor()

TRANSPARENT = data['transparent']
AIWKF = data['asp_img_with_kf'] * 1.76
AIHKF = data['asp_img_height_kf'] * 3.4
AIIKF = data['asp_img_indent_kf'] * 17.14
LOGOPOS = data['logopos']
LOGOTYPE = data['logotype']

res_path = os.getcwd()+"\\res"
folders_in_res = os.listdir(res_path)

def getpos(pos, im_width, im_height, wm_width, wm_height, indent):
    match pos:
        case "lu":
            xpos = indent
            ypos = indent
        case "ru":
            xpos = im_width-indent-wm_width
            ypos = indent
        case "ld":
            xpos = indent
            ypos = im_height-indent-wm_height
        case "rd":
            xpos = im_width-indent-wm_width
            ypos = im_height-indent-wm_height
        case "cc":
            xtiw = int(im_width/2)
            xtww = int(wm_width/2)
            xpos =  xtiw-xtww

            ytiw = int(im_height/2)
            ytww = int(wm_height/2)
            ypos = ytiw-ytww

        case "cu":
            xtiw = int(im_width/2)
            xtww = int(wm_width/2)
            xpos =  xtiw-xtww

            ypos = indent

        case "cd":
            xtiw = int(im_width/2)
            xtww = int(wm_width/2)
            xpos =  xtiw-xtww

            ypos = im_height-indent-wm_height

        case "lc":
            xpos = indent

            ytiw = int(im_height/2)
            ytww = int(wm_height/2)
            ypos = ytiw-ytww

        case "rc":
            xpos = im_width-indent-wm_width

            ytiw = int(im_height/2)
            ytww = int(wm_height/2)
            ypos = ytiw-ytww

    return xpos, ypos

for folder in folders_in_res:
    folder_path = os.path.join(res_path, folder)
    i_num = 0
    if os.path.isdir(folder_path):
        print(f"\n\nДиапазон: {folder}")
        folders_in_folder = os.listdir(folder_path)
        for inner_folder in folders_in_folder:
            inner_folder_path = os.path.join(folder_path, inner_folder)
            num_lines = len(folders_in_folder)
            if os.path.isdir(inner_folder_path):
                print(f"  Папка: {inner_folder}")
                outstr = ""
                i_num = i_num + 1
                files_in_folder = os.listdir(inner_folder_path)
                progress_bar(i_num, num_lines)
                for file in files_in_folder:
                    file_path = os.path.join(inner_folder_path, file)

                    if os.path.isfile(file_path):
                        _, extension = os.path.splitext(file)
                        extension = extension.lstrip('.')
                        if extension not in blacklist:
                            im = Image.open(file_path)
                            im_width, im_height = im.size

                            if LOGOTYPE == "pm":
                                wm = Image.open("dist/pm.png").convert('RGBA')

                                asp_img_with = im_width/AIWKF
                                asp_img_height = asp_img_with/AIHKF
                                indent = im_width/AIIKF

                                wm = wm.resize((int(asp_img_with), int(asp_img_height)))

                            elif LOGOTYPE == "ym":
                                wm = Image.open("dist/ym.png").convert('RGBA')

                                asp_img_with = im_width/AIWKF
                                asp_img_height = asp_img_with/AIHKF
                                indent = im_width/AIIKF

                                wm = wm.resize((int(asp_img_with), int(asp_img_height)))

                            wm.putalpha(TRANSPARENT)
                            wm_width, wm_height = wm.size

                            file_dir = os.path.dirname(file_path)

                            if os.path.isdir(file_dir+"/"+LOGOTYPE):
                                pass
                            else:
                                os.mkdir(file_dir+"/"+LOGOTYPE)

                            xpos,ypos = getpos(LOGOPOS, im_width, im_height, wm_width, wm_height, int(indent))
                            im.paste(wm, (xpos,ypos),wm)
                            im.save(f'{file_dir}\\{LOGOTYPE}\\{file}')

                            outstr = f'{outstr} | {file_dir}\\{LOGOTYPE}\\{file}'

                sql = f"INSERT INTO `test` ({mysql_column_to_folder}, {mysql_column_to_path}) VALUES (%s, %s)"
                values = (inner_folder, outstr[3:])
                cursor.execute(sql, values)
                db.commit()
                
print(f"\n\n{getdate()} |" + Style.BRIGHT + Fore.GREEN + " Обработка завершена."+ Style.NORMAL + Fore.WHITE )
cursor.close()
db.close()