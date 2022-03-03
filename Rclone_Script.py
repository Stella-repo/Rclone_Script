import os
from ast import Continue
from copy import copy
from tabnanny import check
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

SCOPES = 'https://www.googleapis.com/auth/drive.file'
store = file.Storage('token.json')
creds = store.get()

if not creds or creds.invalid:
    os.system('color 04')
    print("토큰파일을 생성합니다.\n")
    flow = client.flow_from_clientsecrets('client_secret_drive.json', SCOPES)
    creds = tools.run_flow(flow, store, flags) if flags else tools.run(flow, store)

drive_service = build('drive', 'v3', http=creds.authorize(Http()))


def split_link(url):
    url = url.replace('?','\n')
    url = url.replace('/','\n')
    url = url.replace('=','\n')
    url = url.replace('#','\n')
    url = url.split('\n')
    output = 'x'
    for i in range(0, len(url)):
        if len(url[i]) >= 33:
            output = str(url[i])
            break
    return output

def check_api(id):
    try:
        return drive_service.files().get(fileId=id, supportsAllDrives='true', supportsTeamDrives='true').execute()
    except:
        return 'retry'


def work_script():
    # URL받아서 링크타입이랑 ID추출
    while True:
        while True:
            copied_link  = input('복사할 폴더 or 파일 (URL or ID) : ')
            copied_id = split_link(copied_link)
            if len(copied_id) >= 33:
                break
        checked_api = check_api(copied_id)
        if checked_api != 'retry':
            if 'folder' in checked_api.get('mimeType'):
                copied_type = 'folder'
                print('링크타입 :', copied_type)
                print('ID :', copied_id)
                print()
                break
            else:
                copied_type = 'file'
                print('링크타입 :', copied_type)
                print('ID :', copied_id)
                print()
                break


    # 복사방법 선택
    while True:
        method = input('(1)사본만들기 / (2)다운로드받기 (기본값 : 사본만들기) : ')
        if (method == '') or (method == '1'):
            method = 'copy'
            print('사본을 만듭니다.')
            print()
            break
        elif method == '2':
            method = 'down'
            print('다운로드를 받습니다.')
            print()
            break


    #폴더위치 설정
    while True:
        if method == 'copy':
            folder = input('사본을 만들 폴더 (폴더명 or URL or ID) (기본값 : MyDrive/Rclone-Script) : ')
        elif method == 'down':
            folder = input('다운받을 폴더 (폴더명 or 경로) (기본값 : Desktop/Rclone-Script) : ')
        if folder == '':
            folder = 'Rclone-Script'
            tocopy_loaction = 'folder'
            if method == 'copy':
                print('복사경로 : MyDrive/' + folder)
                print()
            elif method == 'down':
                print('다운경로 : Desktop/' + folder)
                print()
            break
        elif ('http' in folder) or ('google.com' in folder):
            if method == 'copy':
                folder = split_link(folder)
                if len(folder) == 33:
                    if 'folder' in check_api(folder).get('mimeType'):
                        tocopy_loaction = 'id'
                        print('복사경로 :', folder)
                        print()
                        break
                    else:
                        continue
            elif method == 'down':
                continue
        elif ' ' not in folder:
            if len(split_link(folder)) == 33:
                checkedd_api = check_api(folder)
                if checkedd_api != 'retry':
                    if 'folder' in checkedd_api.get('mimeType'):
                        tocopy_loaction = 'id'
                        print('복사경로 :', folder)
                        print()
                        break
                    else:
                        continue
        elif ':\\' in folder:
            if method == 'copy':
                continue
            elif method == 'down':
                tocopy_loaction = 'path'
                print('다운경로 :', folder)
                print()
                break
        else:
            tocopy_loaction = 'folder'
            if method == 'copy':
                print('복사경로 : MyDrive/' + folder)
                print()
            elif method == 'down':
                print('다운경로 : Desktop/' + folder)
                print()
            break

    # 작업실행
    os.system('color 03')
    if copied_type == 'file':
        if method == 'copy':
            if tocopy_loaction == 'folder':
                os.system('..\\rclone backend copyid stella: ' + copied_id + ' \"stella:' + folder + '/\" --drive-server-side-across-configs --progress -v')
            elif tocopy_loaction == 'id':
                os.system('..\\rclone backend copyid stella: '  + copied_id + ' stella,root_folder_id=' + folder + ': --drive-server-side-across-configs --progress -v')
        elif method == 'down':
            if tocopy_loaction == 'folder':
                os.system('..\\rclone backend copyid stella: ' + copied_id + ' \"' + os.path.expanduser('~') + '\\desktop\\' + folder + '/\" --drive-server-side-across-configs --progress -v')
            elif tocopy_loaction == 'path':
                os.system('..\\rclone backend copyid stella: ' + copied_id + ' \"' + folder + '/\" --drive-server-side-across-configs --progress -v')
    if copied_type == 'folder':
        folder_name = checked_api.get('name')
        if method == 'copy':
            if tocopy_loaction == 'folder':
                os.system('..\\rclone copy stella,root_folder_id=' + copied_id + ': \"stella:' + folder + '/' + folder_name + '\" --drive-server-side-across-configs --progress -v --transfers=10')
            elif tocopy_loaction == 'id':
                os.system('..\\rclone copy --drive-root-folder-id ' + copied_id + ' stella: \"stella,root_folder_id=' + folder + ':' + folder_name + '\" --drive-server-side-across-configs --progress -v')
        elif method == 'down':
            if tocopy_loaction == 'folder':
                os.system('..\\rclone copy stella,root_folder_id=' + copied_id + ': \"' + os.path.expanduser('~') + '\\desktop\\' + folder + '\\' + folder_name + '\" --drive-server-side-across-configs --progress -v --transfers=5')
            elif tocopy_loaction == 'path':
                os.system('..\\rclone copy stella,root_folder_id=' + copied_id + ': \"' + folder + '\\' + folder_name + '\" --drive-server-side-across-configs --progress -v --transfers=5')

    os.system('color 0A')
    print()
    print('작업완료!!')
    input('화면을 초기화하려면 아무 키나 누르십시오 . . .')


while True:
    check_rclone = os.path.isfile('..\\rclone.exe')
    if check_rclone == True:
        break
    elif check_rclone == False:
        os.system('color 04')
        input('스크립트 폴더를 rclone.exe가 있는 폴더의 하위폴더에 위치해 주세요.')

while True:
    print()
    print('     888888ba           dP                               .d88888b                    oo            dP')
    print('     88    `8b          88                               88.    \"\'                                 88')
    print('    a88aaaa8P\' .d8888b. 88 .d8888b. 88d888b. .d8888b.    `Y88888b. .d8888b. 88d888b. dP 88d888b. d8888P')
    print('     88   `8b. 88\'  `\"\" 88 88\'  `88 88\'  `88 88ooood8          `8b 88\'  `\"\" 88\'  `88 88 88\'  `88   88')
    print('     88     88 88.  ... 88 88.  .88 88    88 88.  ...    d8\'   .8P 88.  ... 88       88 88.  .88   88')
    print('     dP     dP `88888P\' dP `88888P\' dP    dP `88888P\'     Y88888P  `88888P\' dP       dP 88Y888P\'   dP')
    print('                                                                                        88')
    print('     Made by Stella＊                                                                   dP')
    print()
    os.system('color 07')
    work_script()
    os.system('cls')
