import requests
import pprint
import os
from urllib.request import urlopen

class YaUploader:
    def __init__(self, token: str):
        self.token = token

    def upload(self, disk_file_path: str, filename: str):
        """Метод загружает файл на яндекс диск"""
        #выделяем место на яндекс диске
        upload_url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
        #в заголовке авторизация с токеном
        headers = {"Authorization": self.token}
        #disk_file_path в параметрах указывается путь на яндекс диске куда надо записать файл
        #overwrite = true для возможности перезаписи файла, если тот существует
        params = {"path":disk_file_path,"overwrite":"true"}
        response = requests.get(upload_url,headers = headers,params = params)
        #проверка статуса http запроса
        res = response.status_code
        print (res)
        #считывание данных с яндекс диска в виде словаря
        response_href = response.json()
        print ('Ya',response_href)
        #поиск в этом словаре параметра href ссылки
        Url = response_href.get("href")
        #запись файла filename на выделенное яндекс диск место по disk_file_path
        with open(filename,'rb',) as file1:
             files = {'file': file1}
             response = requests.put(Url, files=files, headers=headers)
                
class VK:

   def __init__(self, access_token, user_id, version='5.131'):
       self.token = access_token
       self.id = user_id
       self.version = version
       self.params = {'access_token': self.token, 'v': self.version}

   def users_info(self):
       url = 'https://api.vk.com/method/users.get'
       params = {'user_ids': self.id}
       response = requests.get(url, params={**self.params, **params})
       return response.json()
    
   def photo_info(self):
       url = 'https://api.vk.com/method/photos.get'
       params = {'user_ids': self.id,'album_id':283920371,'extended':1,'count':5}
       response = requests.get(url, params={**self.params, **params})
       return response.json()

#считываем токены VK и Ya и user_id VK
with open('tokens_id.txt','r') as document:
#access_token и user_id получены из ссылки выданной VK
    str1 = document.readline()
    access_token = str1.replace('\n','')
    str1 = document.readline()
    str2 = str1.replace('\n','')
    user_id = int (str2)
# токен к OlegPolygon Yandex
    str1 = document.readline()
    token = str1.replace('\n','')

#cчитываем информацию о файлах с VK
vk = VK(access_token, user_id)
res ={}
res = vk.photo_info()
#записываем на Yandex disk
uploader = YaUploader(token)
i = 0
json_dic = []

count_photo = 0
count_photo = int(input ('Введите количество пересылаемых фото '))
while  i < count_photo:
    str_=str(res['response']['items'][i]['likes']['user_likes'])
#создаем имя нового файла фото
    file_name = 'photo_'+str(i+1)+'_likes_'+str_+'.jpg'
#достаем Url из json от VK
    Url = res['response']['items'][i]['sizes'][-1]['url']
    
#копируем через буферный файл cached_photo1.jpg  на компе
#используем функцию urlopen для извлечения данных по указанному Url
#   var 1 urlopen
#   cached_photo = urlopen(Url).read()
#   var 2 request
    data=[]
    response = requests.get(Url,data,stream=True)
    cached_photo = response.raw.read()
#записываем данные в файл на компе
    filename3 = os.getcwd() + '\cached_photo1.jpg'
    file = open(filename3, 'wb')
    file.write(cached_photo)
    file.close()
    json_dic.append({'file_name':file_name,'size':'z'})
#вызываем метод записи на Ya диск
    result = uploader.upload(file_name,filename3)
    i+=1
    
print (f'Загрузка {count_photo} фото завершена')
    
pprint.pprint(json_dic)
