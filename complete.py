import os
from pathlib import Path
from pdf2image import convert_from_path
from PIL import Image


import sys
from subprocess import call

#----------------------------------------------------

import pyocr
import pyocr.builders
import re

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages


input="1E"

input_g=re.search('[0-9]',input)
input_c=re.search('[^0-9]{1,}',input)

top=0

if int(input_g.group())<4:
    pattern=["M","E","D","C","A"]
    top=187+(int(input_g.group())-1)*320+pattern.index(input_c.group())*64
else:
    pattern=["M","E(E)","E(J)","D","C","A"]
    top=1147+(int(input_g.group())-4)*384+pattern.index(input_c.group())*64

print(top)

#----------------------------------------
tools = pyocr.get_available_tools()
if len(tools) == 0:
     print("No OCR tool found")
     sys.exit(1)

tool = tools[0]
print("Will use tool '%s'" % (tool.get_name()))


langs = tool.get_available_languages()
print("Available languages: %s" % ", ".join(langs))
lang = 'jpn'
print("Will use lang '%s'" % (lang))

 # 時間割結果出力
dayname=['月曜日','火曜日','水曜日','木曜日','金曜日']
#---------------------------------------------------




# poppler/binを環境変数PATHに追加する
poppler_dir = Path(__file__).parent.absolute() / "poppler/bin"
os.environ["PATH"] += os.pathsep + str(poppler_dir)

# PDFファイルのパス
pdf_path = Path("jikanwari.pdf")
pdf_path2 = Path("jikanwarihenkou.pdf")

# PDF -> Image に変換（150dpi）
pages = convert_from_path(str(pdf_path), 200)

# 画像ファイルを１ページずつ保存
image_dir = Path("./imag")
for i, page in enumerate(pages):
    file_name = pdf_path.stem + "_{:02d}".format(i + 1) + ".png"
    image_path = image_dir / file_name
    # JPEGで保存
    page.save(str(image_path), "PNG",quality=100)

pages2 = convert_from_path(str(pdf_path2), 200)
for i, page2 in enumerate(pages2):
    file_name2 = pdf_path2.stem + "_{:02d}".format(i + 1) + ".png"
    image_path2 = image_dir / file_name2
    # JPEGで保存
    page2.save(str(image_path2), "PNG",quality=100)


#------------------------------------------------------------------------------------
 # pdf2txt.py のパス
py_path = Path(sys.exec_prefix) / "Scripts" / "pdf2txt.py"

 #pdf2txt.py の呼び出し
call(["py", str(py_path), "-o henkou.txt", "-p 1", "./jikanwarihenkou.pdf"])

f = open("henkou.txt",encoding="utf-8_sig")
data1 = f.read()  # ファイル終端まで全て読んだデータを返す
f.close()
data1=re.sub('[^A-Z0-9_ぁ-んァ-ン一-龥]','',data1)
#time = re.findall('(Ⅰ|Ⅱ|Ⅲ|Ⅳ|Ⅳa)',data1)
day = re.findall('[一-龥]曜日',data1)
days = re.findall('[0-9]{1,}月[0-9]{1,}日',data1)
grade=re.search('[0-9]{10,}',data1)
grade = re.findall('[0-9]',grade.group())
classname=re.search('[A-Z]{10,}',data1)
classname = re.findall('[A-Z]',classname.group())


#print(time)
#--------------------------------------------------------------------------------------
#match=False
#for i in range(16):
# print(grade[i]+classname[i])
# if grade[i]+classname[i]==input:
#  match=True

output1=""

im = Image.open('./imag/jikanwari_01.png')
for i in range(5):
 im_crop1 = im.crop((183+517*i, top, 700+517*i, top+65))
 save_name="./imag/jikanwari_class"+str(i)+".png"
  #im_crop1.save(save_name, quality=100)
 txt = tool.image_to_string(im_crop1,lang=lang,builder=pyocr.builders.TextBuilder())
 txt=re.sub('[^A-Z0-9_ぁ-んァ-ン一-龥]{3,}','',txt)
 txt=re.sub('[^A-Z0-9_ぁ-んァ-ン一-龥]','',txt)
 output1+=dayname[i]+" "+txt+"\n"
print(output1)


im = Image.open('./imag/jikanwarihenkou_01.png')

cal1=[""]*16
cal2=[""]*16
output2=""

for i in range(16):
 #print(grade[i]+classname[i])
 if input==grade[i]+classname[i]:
  im_crop2 = im.crop((871, 255+56*i, 1366, 312+56*i))
  save_name2="./imag/jikanwarihenkou_class"+str(i)+".png"

  file_name="./imag/jikanwarihenkou_class"+str(i)+".png"
  txt = tool.image_to_string(im_crop2,lang=lang,builder=pyocr.builders.TextBuilder())
  txt=re.sub('[^A-Z0-9_ぁ-んァ-ン一-龥]{3,}','',txt)
  txt=re.sub('[^A-Z0-9_ぁ-んァ-ン一-龥]','',txt)
  cal1[i]+=txt

  im_crop3 = im.crop((1366, 255+56*i, 2182, 312+56*i))
  save_name2="./imag/jikanwarihenkou_class"+str(i+16)+".png"
  file_name="./imag/jikanwarihenkou_class"+str(i)+".png"
  txt = tool.image_to_string(im_crop3,lang=lang,builder=pyocr.builders.TextBuilder())
  txt=re.sub('[^A-Z0-9_ぁ-んァ-ン一-龥]{3,}','',txt)
  txt=re.sub('[^A-Z0-9_ぁ-んァ-ン一-龥]','',txt)
  cal2[i]+=txt
  output2+=grade[i]+classname[i]+" "+day[i+1]+" "+days[i]+" "+cal1[i]+"→"+cal2[i]+"\n"
 #  時間割変更結果出力

print(output2)
