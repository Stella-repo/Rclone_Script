from ast import Continue
from copy import copy
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

try :
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

SCOPES = 'https://www.googleapis.com/auth/drive.file'
store = file.Storage('token.json')
creds = store.get()

if not creds or creds.invalid:
    print("make new storage data file ")
    flow = client.flow_from_clientsecrets('client_secret_drive.json', SCOPES)
    creds = tools.run_flow(flow, store, flags) if flags else tools.run(flow, store)

drive_service = build('drive', 'v3', http=creds.authorize(Http()))



# name = drive_service.files().get(fileId='1Guu2i0FIWTDRyc0FEiUshy97tFWUxmTkx2ShcLpObWo', supportsAllDrives='true', supportsTeamDrives='true').execute()
# print(name)
# items = name.get('name', [])
# print(items)


def split_link(url):
    url = url.replace('?','\n')
    url = url.replace('/','\n')
    url = url.replace('=','\n')
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


# URL받아서 링크타입이랑 ID추출
while True:
    while True:
        copied_link  = input('복사할 폴더 or 파일(URL or ID) : ')
        copied_id = split_link(copied_link)
        if len(copied_id) >= 33:
            break
    checked_type = check_api(copied_id).get('mimeType')
    if 'folder' in checked_type:
        copied_type = 'folder'
        print('링크타입 :', copied_type)
        print('ID :', copied_id)
        break
    elif checked_type == 'retry':
        continue
    else:
        copied_type = 'file'
        print('링크타입 :', copied_type)
        print('ID :', copied_id)
        break


# 복사방법 선택
while True:
    method = input('(1)Drive-server-side-across Copy / (2)Download to Local Storage (Default : (1)) : ')
    if method == '':
        print('Selected Drive-server-side-across Copy')
        break
    elif method == '1':
        print('Selected Drive-server-side-across Copy')
        break
    elif method == '2':
        print('Selected Download to Local Storage')
        break


#폴더위치 설정
while True:
    folder = input('Destination Folder (Default : Rclone-Folder-Copy) : ')
    if folder == '':
        folder = 'Rclone-Folder-Copy'
        tocopy_id = '0'
        print('copy to', folder)
        break
    elif ('http' in folder) or ('google.com' in folder):
        folder = split_link(folder)
        if len(folder) == 33:
            if 'folder' in check_api(folder).get('mimeType'):
                tocopy_id = '1'
                print('copy to 1', folder)
                break
            else:
                continue
    elif ' ' not in folder:
        if len(split_link(folder)) == 33:
            if 'folder' in check_api(folder).get('mimeType'):
                tocopy_id = '1'
                print('copy to 2', folder)
                break
            else:
                continue
    else:
        tocopy_id = '0'
        print('copy to', folder)
        break

