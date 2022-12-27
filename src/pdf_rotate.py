# List all non-standard packages to be imported by your 
# script here (only missing packages will be installed)
from ayx import Package
try:
    Package.installPackages(package=['pandas','PyPDF2==2.11.0'], install_type="install --user")
except:
    pass

from ayx import Alteryx
import pandas as pd
from PyPDF2 import PdfReader
from PyPDF2 import PdfWriter
import os
output_path=""
try:
    pdf_list = Alteryx.read("#1")
    input_page = pdf_list['input_page'].iloc[0]
    input_rotate = pdf_list['input_rotate'].iloc[0]
    input_isTodoAll = pdf_list['input_isTodoAll'].iloc[0]
    input_isConnectFile = pdf_list['input_isConnectFile'].iloc[0]
    if (input_isConnectFile==True):
        input_path = pdf_list['connect_input_path']
    else:
        input_path = pdf_list['pwc_input_path']
    # 建立pandas表格資料,最後輸出該表
    resultTemplate = {
        "Source File":input_path,
        "Status":"",
        "Message":"",
        "Output Path":""
    }
    resultData = pd.DataFrame(resultTemplate)

    for file_num in range(len(input_path)):
        try:
            output_path=""
            isExist = os.path.exists(input_path[file_num])
            if(isExist == False):
                raise Exception("該檔案不存在，或路徑輸入錯誤，請確認後再重新執行 ! ")
            file = os.path.splitext(input_path[file_num])[0]
            ext = os.path.splitext(input_path[file_num])[1]
            if(ext != ".pdf"):
                # raise Exception("該檔案非 PDF 檔，故不處理 ! ")
                continue
            pdfRead = open(input_path[file_num], 'rb')
            reader = PdfReader(pdfRead, strict=False)
            writer = PdfWriter()

            arrangeInputData = str(input_page).replace(" ","").split(",")
            isTodoAll = input_isTodoAll
            rotate = input_rotate
            toDoPage=[]

            if(isTodoAll):
                for pageNum in range(reader.numPages):
                    page = reader.getPage(pageNum)
                    page.rotateClockwise(rotate)
                    writer.addPage(page)
            else:
                # 分析待處理頁數，將1-3拆成1,2,3
                for index in range(len(arrangeInputData)):
                    if(len(str(arrangeInputData[index]))==0):
                        continue
                    if('-' in str(arrangeInputData[index])):
                        startAndEndPage = str(arrangeInputData[index]).split('-')
                        startPage = ""
                        endPage = ""
                        # 起始頁與結束頁未輸入時, 始頁自動更改為第一頁, 結束頁自動取pdf最後一頁
                        if(len(str(startAndEndPage[0]))==0):
                            startAndEndPage[0]=1
                        if(len(str(startAndEndPage[1]))==0):
                            startAndEndPage[1]=reader.numPages

                        # 判斷起始頁和結束頁
                        if(int(startAndEndPage[0])<int(startAndEndPage[1])):
                            startPage = startAndEndPage[0]
                            endPage = startAndEndPage[1]
                        else:
                            startPage = startAndEndPage[1]
                            endPage = startAndEndPage[0]
                        
                        # 展開並寫入至待處理頁數
                        for addPageNum in range(int(startPage),int(endPage)+1):
                            # 頁數字串轉數字
                            toDoPage.append(int(addPageNum))
                    else:
                        toDoPage.append(int(arrangeInputData[index]))
                
                # 頁數字串轉數字
                for index in range(len(toDoPage)):
                    toDoPage[index] = int(toDoPage[index])
                # 去除重複頁數
                toDoPage = list(set(toDoPage))


                # 獲取最大頁數
                maxPageNum = max(toDoPage)

                # 判斷輸入頁數是否超過檔案頁數
                if(maxPageNum > reader.numPages):
                    raise Exception("您輸入的頁數已超過檔案最大頁數，請更改頁數範圍後再執行")

                # 處理指定頁數 
                for pageNum in range(reader.numPages):
                    page = reader.getPage(pageNum)
                    if((pageNum+1) in toDoPage):
                        page.rotateClockwise(rotate)
                    writer.addPage(page)
            # pdfWriter.encrypt(password)
            output_path = f'{file}_rotated{ext}'
            i = 2
            while os.path.exists(output_path):
                output_path = f'{file}_rotated{i}{ext}'
                i += 1

            pdfOut = open(output_path, 'wb')
            writer.write(pdfOut)
            pdfOut.close()
            pdfRead.close()

            # 顯示成功與否
            resultData.at[file_num, "Status"] = "Success"
            resultData.at[file_num, "Message"] = "-"
            resultData.at[file_num, "Output Path"] = output_path
            print("Success:" + input_path[file_num])

        except Exception as e:
            # 顯示成功與否
            resultData.at[file_num, "Status"] = "Failure"
            resultData.at[file_num, "Message"] = str(e)
            resultData.at[file_num, "Output Path"] = "-"
            if(output_path and os.path.exists(output_path)):
                os.remove(output_path)
except Exception as e:
    # if(e.args[0])
    resultData["Status"] = "Failure"
    resultData["Message"] = "Alteryx 解析 PDF 過程發生錯誤，請與 AI&T 同仁聯繫("+str(e)+")"
    resultData["Output Path"] = "-"
    if(output_path and os.path.exists(output_path)):
        os.remove(output_path)
Alteryx.write(resultData,1)
# Copyright © 2001-2022 Python Software Foundation; All Rights Reserved.