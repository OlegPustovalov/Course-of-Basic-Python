import requests
import pprint
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
        print (response_href)
        #поиск в этом словаре параметра href ссылки
        Url = response_href.get("href")
        print (Url)
        print(filename)
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

#access_token и user_id получены из ссылки выданной VK
access_token = '...'
user_id = '741291334'
#cчитываем информацию о файлах с VK
vk = VK(access_token, user_id)
res ={}
res = vk.photo_info()
 # токен к OlegPolygon
token = '...'
uploader = YaUploader(token)
i= 0
while  i < 5:
    str_=str(res['response']['items'][i]['likes']['user_likes'])
#создаем имя нового файла фото
    file_name = 'file_'+str(i+1)+'_likes_'+str_
#достаем Url из json от VK
    Url = res['response']['items'][i]['sizes'][-1]['url']
#копируем  буферный файл cached_photo1.jpg  на компе
#используем функцию urlopen для извлечения данных по указанному Url
    cached_photo = urlopen(Url).read()   
#записываем данные в файл на компе
    filename3 = 'D://Netology/cached_photo1.jpg'
    file = open(filename3, 'wb')
    file.write(cached_photo)
    file.close()
#вызываем метод записи на Ya диск
    result = uploader.upload(file_name,filename3)
    i+=1
    

