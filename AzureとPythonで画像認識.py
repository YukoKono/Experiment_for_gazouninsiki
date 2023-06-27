# API reference :
# https://westus.dev.cognitive.microsoft.com/docs/services/5adf991815e1060e6355ad44/operations/56f91f2e778daf14a499e1fa
# 参考 : https://ledge.ai/microsoft-computer-vision-api/
# 機能概要 : img フォルダ中の画像をAI解析し、ファイルのリネームを行います。
# 使い方 : python3 cv_demo.py
# 注意 : サブスクリプションキーは変更してください

import requests
import glob
import os
import time

subscription_key = ""
assert subscription_key

vision_base_url = "https://westcentralus.api.cognitive.microsoft.com/vision/v2.0/"
analyze_url = vision_base_url + "analyze"


# ファイル名を変更
def file_rename(list_1, list_2):
    for i in range(len(list_1)):
        os.rename(list_1[i], './img/' + list_2[i] + '.jpg')


def ms_computer_vision_api(filepath):
    headers = {'Ocp-Apim-Subscription-Key': subscription_key,'Content-Type': 'application/octet-stream'}
    params = {'visualFeatures': 'Categories,Description,Color'}

    img = open(filepath, 'rb')
    img_byte = img.read()

    response = requests.post(analyze_url, data=img_byte, headers=headers, params=params)
    response.raise_for_status()

    return response.json()


if __name__ == "__main__":
    # 画像ファイルを配列に格納
    image_file = glob.glob('./img/*')

    vision_file_name = []

    start = time.time()

    # Computer Vision APIにリクエストして結果を取得
    for i in range(len(image_file)):
        json_data = ms_computer_vision_api(image_file[i])

        # 生成された文章を取得
        file_name = json_data['description']['captions'][0]['text']
        vision_file_name.append(file_name)

    # 文章の空白をファイル名用にアンダーバーに修正
    for i in range(len(vision_file_name)):
        vision_file_name[i] = vision_file_name[i].replace(' ', '_')

    file_rename(image_file,vision_file_name)

    # 経過時間を出力
    print("elapsed_time:{0}".format(time.time() - start) + "[sec]")
