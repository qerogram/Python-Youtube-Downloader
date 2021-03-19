# Author : qerogram

import json, hashlib, ffmpeg, os
import requests, time
from selenium import webdriver

def getChromeDriver() :
    options = webdriver.ChromeOptions() # 크롬 옵션 객체 생성
    options.add_argument('headless') # headless 모드 설정
    options.add_argument("window-size=1920x1080") # 화면크기(전체화면)
    options.add_argument("disable-gpu") 
    options.add_argument("disable-infobars")
    options.add_argument("--disable-extensions")

    # 속도 향상을 위한 옵션 해제
    prefs = {'profile.default_content_setting_values': {'cookies' : 2, 'images': 2, 'plugins' : 2, 'popups': 2, 'geolocation': 2, 'notifications' : 2, 'auto_select_certificate': 2, 'fullscreen' : 2, 'mouselock' : 2, 'mixed_script': 2, 'media_stream' : 2, 'media_stream_mic' : 2, 'media_stream_camera': 2, 'protocol_handlers' : 2, 'ppapi_broker' : 2, 'automatic_downloads': 2, 'midi_sysex' : 2, 'push_messaging' : 2, 'ssl_cert_decisions': 2, 'metro_switch_to_desktop' : 2, 'protected_media_identifier': 2, 'app_banner': 2, 'site_engagement' : 2, 'durable_storage' : 2}}   
    options.add_experimental_option('prefs', prefs)

    return webdriver.Chrome('./chromedriver', options=options)


def parsingJSON(driver, url) :
    # 사이트 접속
    driver.get(url)

    # 초기화
    isFind = -1
    data = ""

    # 데이터가 로딩될 때까지 존버
    while isFind == -1 :
        data = driver.find_element_by_xpath("//*").get_attribute("innerHTML")
        isFind = data.find("ytInitialPlayerResponse")
        data = data[isFind:]
        time.sleep(0.5)
    print("[+] Success : Get a webm file address")

    # json Parsing
    data = data[data.find('\"url\"'):]
    data = data[:data.find('\"', 10)]

    return json.loads("{" + data + "\"}")

def makeFileName() :
    md5 = hashlib.new('md5')
    md5.update(os.urandom(16))
    return md5.hexdigest()


def DownloadFile(url) :
    res = requests.get(url)
    print("[+] Start Download webm File")
    filename = makeFileName() + ".webm"
    video_temp = open(filename, "wb")
    video_temp.write(res.content)
    video_temp.close()
    return filename

def webmTomp4(webm_filename, mp4_filename) :
    ffmpeg.input(webm_filename).output(mp4_filename + ".mp4").run()
    print("[+] Success Convert webm file to mp4 file")
    os.remove(webm_filename)

if __name__ == "__main__":
    url = input("[+] input url(youtube url) : ")
    mp4_FileName = input("[+] input filename : ")

    # execute chrome
    driver = getChromeDriver()

    # get video source in youtube page
    data = parsingJSON(driver, url)

    # Terminate chrome
    driver.close()

    # Download webm video
    data_url = data['url'].replace("mime=video/mp4", "mime=audio/webm")
    webm_FileName = DownloadFile(data_url)

    # Convert webm Video to mp4 Video
    webmTomp4(webm_FileName, mp4_FileName)