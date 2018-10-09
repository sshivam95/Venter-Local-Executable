from __future__ import print_function
from googleapiclient import discovery
from googleapiclient.http import MediaFileUpload
from httplib2 import Http



def upload_to_drive(path_folder, filename, filename_diff, path_file, path_file_diff):
    from oauth2client import file, client, tools
    # try:
    #     import argparse
    #     flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
    # except ImportError:
    #     flags = None

    SCOPES = 'https://www.googleapis.com/auth/drive.appfolder https://www.googleapis.com/auth/drive.file'
    store = file.Storage('credentials.json')
    creds = store.get()

    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('client_secret.json', scope=SCOPES)
        creds = tools.run_flow(flow, store)
    DRIVE = discovery.build('drive', 'v3', http=creds.authorize(Http()))

    folder_metadata = {
        'name': path_folder,
        'mimeType': 'application/vnd.google-apps.folder'
    }
    file = DRIVE.files().create(body=folder_metadata,
                                fields='id').execute()
    # print ('Folder ID: %s' % file.get('id'))

    folder_id = file.get('id')

    file_metadata = {
        'name': filename,
        'parents': [folder_id]
    }

    diff_metadata = {
        'name' : filename_diff,
        'parents' : [folder_id]
    }

    media = MediaFileUpload(path_file,
                            mimetype=None,
                            resumable=False)

    media_diff = MediaFileUpload(path_file_diff,
                                 mimetype=None,
                                 resumable=False)

    file = DRIVE.files().create(body=file_metadata,
                                media_body=media,
                                fields='id').execute()
    print('File ID: %s' % file.get('id'))

    file_diff = DRIVE.files().create(body=diff_metadata,
                                media_body=media_diff,
                                fields='id').execute()
    print('File ID: %s' % file_diff.get('id'))

    # FILES = (
    #     # ('5k.csv', None),
    #     ('MEDIA','application/vnd.google-apps.folder')
    # )

    # for filename, mimeType in FILES:
    #     metadata = {'name': filename}
    #     if mimeType:
    #         metadata['mimeType'] = mimeType
    #     res = DRIVE.files().create(body=metadata,
    #             media_body=filename).execute()
    #     if res:
    #         print('Uploaded "%s" (%s)' % (filename, res['mimeType']))
