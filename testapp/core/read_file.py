from openpyxl import load_workbook
from django.http import HttpResponse
import json
import pandas as pd

def read_excel(request):
    if request.method == 'POST':
        file = request.FILES['file_excel']
        df = pd.read_excel(file)
        js = df.to_json(orient='columns')
        return js
        # return HttpResponse(json.dumps(js), content_type="application/json")

def read_csv(request):
    if request.method == 'POST':
        file = request.FILES['file_csv']
        df = pd.read_csv(file)
        js = df.to_json(orient='columns')
        return js





        # 파일 저장
        # file = request.FILES['file_excel']
        # fs = FileSystemStorage()
        # filename = fs.save(file.name, file)
        # uploaded_file_url = fs.url(filename)
        # print(uploaded_file_url)
        #
        # file = request.FILES['file_excel']
        #
        # data_only=Ture로 해줘야 수식이 아닌 값으로 받아온다.
        # load_wb = load_workbook(file, data_only=True)
        #
        # 시트 이름으로 불러오기
        # load_ws = load_wb['Sheet1']
        #
        # 셀 주소로 값 출력
        # print(load_ws['A1'].value)
        #
        # 일단 리스트에 담기
        # all_values = []
        # for row in load_ws.rows:
        #     row_value = []
        #     for cell in row:
        #         row_value.append(cell.value)
        #     all_values.append(row_value)
        #
        # cnt = 0
        # for idx, val in enumerate(all_values):
        #     if idx == 0:
        #         # 엑셀 형식 체크 (첫번째의 제목 row)
        #         if val[0] != '항목1' or val[1] != '항목2' or val[2] != '항목3':
        #             context = {'state': False, 'rtnmsg': '엑셀 항목이 올바르지 않습니다.'}
        #             return HttpResponse(json.dumps(context), content_type="application/json")
        #     else:
        #         # print(type(val[2]))
        #         if val[2] and type(val[2]) == int:
        #             newData = UpData.objects.get(msabun=val[0], mname=val[1])
        #             newData.myear_salary = val[2]
        #             newData.save()
        #             cnt += 1
        #
        # context = {'state': True, 'rtnmsg': '{0}건의 엑셀 데이터가 반영 되었습니다.'.format(cnt)}
        # return HttpResponse(json.dumps(context), content_type="application/json")