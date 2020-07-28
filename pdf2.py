import sys
from pathlib import Path
from subprocess import call

#----------------------------------------------------
from PIL import Image

import pyocr
import pyocr.builders
import re
# pdf2txt.py のパス
py_path = Path(sys.exec_prefix) / "Scripts" / "pdf2txt.py"

#pdf2txt.py の呼び出し
call(["py", str(py_path), "-o henkou.txt", "-p 1", "./jikanwarihenkou.pdf"])

f = open(" henkou.txt",encoding="utf-8_sig")
data1 = f.read()  # ファイル終端まで全て読んだデータを返す
f.close()
#print(type(data1)) # 文字列データ
#lines1 = data1.split('\n') # 改行で区切る(改行文字そのものは戻り値のデータには含まれない)
data1=re.sub('[^A-Z0-9_ぁ-んァ-ン一-龥]','',data1)
day = re.findall('[一-龥]曜日',data1)
days = re.findall('[0-9]{1,}月[0-9]{1,}日',data1)
grade=re.search('[0-9]{10,}',data1)
grade = re.findall('[0-9]',grade.group())
classname=re.search('[A-Z]{10,}',data1)
classname = re.findall('[A-Z]',classname.group())
#day = re.findall('[一-龥]曜日',data1)
#for line in lines1:
#    print(line)

#------------------------------------------------------------------------------------------

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

for i in range(5):
 file_name="./imag/jikanwari_class"+str(i)+".png"
 txt = tool.image_to_string(Image.open(file_name),lang=lang,builder=pyocr.builders.TextBuilder())
 txt=re.sub('[^A-Z0-9_ぁ-んァ-ン一-龥]{3,}','',txt)
 txt=re.sub('[^A-Z0-9_ぁ-んァ-ン一-龥]','',txt)
 output1=dayname[i]+" "+txt
 print(output1)




#  時間割変更結果出力

cal=[""]*32
for i in range(32):
 file_name="./imag/jikanwarihenkou_class"+str(i)+".png"
 txt = tool.image_to_string(Image.open(file_name),lang=lang,builder=pyocr.builders.TextBuilder())
 txt=re.sub('[^A-Z0-9_ぁ-んァ-ン一-龥]{3,}','',txt)
 txt=re.sub('[^A-Z0-9_ぁ-んァ-ン一-龥]','',txt)
 cal[i]=txt

for i in range(16):
 output2=grade[i]+classname[i]+" "+day[i+1]+" "+days[i]+" "+cal[i]+"→"+cal[i+16]+"\n"
 print(output2)
