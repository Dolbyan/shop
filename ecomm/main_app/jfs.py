import requests
import base64
import psycopg2
import os
from pyjavaproperties import Properties
import json

class JFS():
    def __init__(self):
        # self.url_upload = "http://89.74.210.195:1752/jfs-cloud-files/v1/api/storage/upload"
        # self.url_download = "http://89.74.210.195:1752/jfs-cloud-files/v1/api/storage/download?filename="
        # self.headers = {"Tenant-Id":"pmichniewicz"}
        # self.headers = {"Tenant-Id":""}
        self.properties = Properties()
        self.properties_file = os.path.join(os.path.dirname(__file__),
                                            "config1.properties")
        # self.properties_file = "config1.properties"
        self.load_properties()
    def load_properties(self):

        with open(self.properties_file, "r") as file:
            self.properties.load(file)
        self.url_upload = self.properties.getProperty("url_upload")
        self.url_download = self.properties.getProperty("url_download")
        self.headers = self.properties.getProperty("headers")


    def post_jfs(self, name_file):
        location = "C:/Users/Pepik/Downloads/"
        files = {'file':open(f'{location}{name_file}', 'rb')}
        print(self.headers, "PRINT POSTJFS")
        res = requests.post(f'{self.url_upload}', headers=json.loads(self.headers),
                            files=files)

        if res.status_code == 200:
            response_data = res.json()
            print(response_data, "RES DATA")
        else:
            print(res.status_code)


    def get_jfs(self, image_filename):
        url = self.url_download + f"{image_filename}"
        try:
            response = requests.get(url, headers=json.loads(self.headers))
            print(response)
            if response.status_code == 200:
                image_bytes = response.content
                image_base64 = base64.b64encode(image_bytes).decode('utf-8')
                return image_base64
            else:
                print("Error XD", response.status_code)
                return None
        except Exception as e:
            print("Error getting resource", e)
            return None

# class IntService:
#
#     def __init__(self):
#         self.link = "http://89.74.210.195:1752/jfs-cloud-files/v1/api/storage/upload"
#         self.headers = {'Tenant-Id':"pmichniewicz"}
#
#     def add_file(self, name_file: str, type_s: str, location: str):
#         files = {'file':open(f'{location}{name_file}', 'rb')}
#         res = requests.post(f'{self.link}', headers=self.headers,
#                             files=files)
#
#         if res.status_code == 200:
#             response_data = res.json()
#             print(response_data, "RES DATA")
#         else:
#             print(res.status_code)
