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



copied_link = input('복사할 폴더 or 파일(URL or ID) : ')
copied_link = copied_link.replace('?','\n')
copied_link = copied_link.replace('/','\n')
copied_link = copied_link.replace('=','\n')
copied_link = copied_link.split('\n')
for i in range(0, len(copied_link)):
    if len(copied_link[i]) == 33:
        copied_id = str(copied_link[i])

if 'folder' in copied_link:
    copied_type = 'folder'
elif 'file' in copied_link:
    copied_type = 'file'
elif 'uc' in copied_link:
    copied_type = 'file'
else:
    check_type = drive_service.files().get(fileId=copied_id, supportsAllDrives='true', supportsTeamDrives='true').execute()
    if 'folder' in check_type.get('mimeType'):
        copied_type = 'folder'
    else:
        copied_type = 'file'