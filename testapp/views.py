from django.shortcuts import render
import pandas as pd
from django.views.decorators.csrf import csrf_exempt
import logging
import json
import pickle
from .models import Data, Temp
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import seaborn as sns
from xgboost import XGBClassifier
from xgboost import XGBRegressor

logger = logging.getLogger('my')

def index(request) :
    logger.info("index 진입")

    return render(request, "index.html")

@csrf_exempt
def upfile(request) :
    logger.info("upfile 진입")
    # 첫화면에서 파일업로드 submit 적용시

    if request.method == 'POST':
        format = request.POST.get('data_format')
        file = request.FILES['data_file']

        if format == 'csv' :
            try:
                df = pd.read_csv(file, encoding='cp949')
                # cols = df.columns.tolist()
                # test1 = df.to_json(orient='split')
                # test2 = json.loads(test1)
                # test_cols = test2['columns']
                # test_data = test2['index']
                # test3 = pd.DataFrame(test_data, columns=test_cols)

            except:
                df = pd.read_csv(file, encoding='utf-8')
        # else :
        #     try:
        #         df = pd.read_excel(file, encoding='cp949')
        #     except:
        #         df = pd.read_excel(file, encoding='utf-8')

    df_save = df.to_json(orient='split')
    d = Data(datafile=df_save)
    d.save()
    id = Data.objects.latest('idx').idx
    df = df.reset_index(drop=False)
    js = df.to_json(orient='split')
    js_to_data = []
    js_to_data = json.loads(js)
    cols = js_to_data['columns']
    # idx = js_to_data['index']
    data = js_to_data['data']
    lendata = range(len(data))
    context = {'cols': cols, 'data':data, 'id': id, 'lendata' : lendata}
    return render(request, 'table.html', context)

@csrf_exempt
def getdetail(request) :
    logger.info("getdetail 진입")

    if request.method == 'POST':
        idx = request.POST.get('id')
        data = Data.objects.filter(idx=idx).values()[0]['datafile']

        try :
            df_ori = pd.read_json(data, orient='split')
        except :
            js_to_data = json.loads(data)
            js_cols = js_to_data['columns']
            js_data = js_to_data['index']
            df_ori = pd.DataFrame(js_data, columns=js_cols)

        try :
            ifnan = request.POST.get('ifnan')
        except :
            ifnan = ''

        if ifnan == 'dropna0' :
            df_ori.dropna(axis=0, how='any', inplace=True)

        elif ifnan == 'dropna1' :
            df_ori.dropna(axis=1, how='any', inplace=True)
        elif ifnan == 'fillmedi' :
            df_ori.fillna(df_ori.median(axis=1), inplace=True)
            pass
        elif ifnan == 'fillmean' :
            df_ori.fillna(df_ori.mean(axis=1), inplace=True)
        else :
            pass

        # for i in df_ori.columns :
        #     try :
        #         df_ori[i].astype('int64')
        #     except :
        #         df_ori[i] = df_ori[i].astype('O')

        old_cols = df_ori.columns.tolist()
        cols = []

        for i in old_cols :

            if (df_ori[i].dtypes != 'O') :
                cols.append(i)
                # if (df_ori[i].dtypes != None) :
                #     cols.append(i)
        df = df_ori[cols]

        df_detail = pd.DataFrame(columns=cols, index=['HISTOGRAM', 'COUNT', 'MEAN', 'STD', 'MIN', '25%', '50%', '75%', 'MAX', 'HIST_STEP'])

        for i in cols :
            df_detail.loc['COUNT', i] = len(df[i].tolist())
            df_detail.loc['MIN', i] = df[i].min()
            df_detail.loc['MAX', i] = df[i].max()
            df_detail.loc['MEAN', i] = round(df[i].mean(), 2)
            df_detail.loc['STD', i] = round(df[i].std(), 2)
            df_detail.loc['50%', i] = round(df[i].median(), 2)
            df_detail.loc['25%', i] = round(df[i].quantile(.25), 2)
            df_detail.loc['75%', i] = round(df[i].quantile(.75), 2)

            range_num = round((df_detail.loc['MAX', i] - df_detail.loc['MIN', i]), 2)
            step = round(range_num/10)
            counts = []
            hist = []
            num1 = df_detail.loc['MIN', i]
            hist.append(num1)
            for h in range(10):
                num2 = num1 + step
                counts.append(len(df[(df[i]>=num1) & (df[i]<=num2)][i].tolist()))
                num1 = num2
                hist.append(num1)
            df_detail.loc['HISTOGRAM', i] = counts
            df_detail.loc['HIST_STEP', i] = hist
        pv = df_detail.T

        df_fixed = df_ori.to_json(orient='split')
        df_num = df.to_json(orient='split')
        df_pv = pv.to_json(orient='split')

        fixed = Data.objects.get(pk=idx)
        fixed.fixedfile = df_fixed
        fixed.fixednumfile = df_num
        fixed.detailfile = df_pv
        fixed.save()

        # fixedfile & fixednumfile 저장

        context = {'HIST': pv.iloc[:,0].tolist(),
                   'COUNT': pv.iloc[:,1].tolist(),
                   'MEAN': pv.iloc[:,2].tolist(),
                   'STD': pv.iloc[:,3].tolist(),
                   'MIN': pv.iloc[:,4].tolist(),
                   'per25': pv.iloc[:,5].tolist(),
                   'per50': pv.iloc[:,6].tolist(),
                   'per75': pv.iloc[:,7].tolist(),
                   'MAX': pv.iloc[:,8].tolist(),
                   'len': range(len(cols)),
                   'cols' : cols,
                   'label' : pv.iloc[:,9].tolist(),
                   'id' : idx
                   }

        return render(request, 'detail.html', context)

@csrf_exempt
def gettableback(request, id) :
    logger.info("gettableback 진입")

    idx = id
    data = Data.objects.filter(pk=idx).values()[0]['datafile']
    # try :
    #     data = Data.objects.filter(pk=idx).values()[0]['fixedfile']
    # except :
    #     data = Data.objects.filter(pk=idx).values()[0]['datafile']

    # js = pd.read_json(data, orient='split')
    js_to_data = []
    js_to_data = json.loads(data)
    cols = js_to_data['columns']
    data = js_to_data['data']
    lendata = range(len(data))
    context = {'cols': cols, 'data': data, 'id': id, 'lendata': lendata}

    return render(request, 'table.html', context)

@csrf_exempt
def getdetailback(request, id) :
    logger.info("getdetailback 진입")

    idx = id
    data_pv = Data.objects.filter(pk=idx).values()[0]['detailfile']
    data_df = Data.objects.filter(pk=idx).values()[0]['fixednumfile']
    pv = pd.read_json(data_pv, orient='split')
    df = pd.read_json(data_df, orient='split')
    cols = df.columns.tolist()

    context = {'HIST': pv.iloc[:, 0].tolist(),
               'COUNT': pv.iloc[:, 1].tolist(),
               'MEAN': pv.iloc[:, 2].tolist(),
               'STD': pv.iloc[:, 3].tolist(),
               'MIN': pv.iloc[:, 4].tolist(),
               'per25': pv.iloc[:, 5].tolist(),
               'per50': pv.iloc[:, 6].tolist(),
               'per75': pv.iloc[:, 7].tolist(),
               'MAX': pv.iloc[:, 8].tolist(),
               'len': range(len(cols)),
               'cols': cols,
               'label': pv.iloc[:, 9].tolist(),
               'id': idx
               }

    return render(request, 'detail.html', context)

@csrf_exempt
def getgraph(request):
    logger.info("getgraph 진입")

    if request.method == 'POST':
        idx = request.POST.get('id')
        data = Data.objects.filter(idx=idx).values()[0]['fixednumfile']
        df = pd.read_json(data, orient='split')
        cols = df.columns.tolist()
        charts = []
        for i in cols :
            charts.append(df.loc[:, i].tolist())

        corrs = pd.DataFrame((df.corr()), columns=cols).fillna(0)
        corrz = corrs.to_numpy().tolist()

        context = {'cols' : cols, 'charts' : charts, 'id':idx, 'corrz' : corrz }

    return render(request, 'graph.html', context)

@csrf_exempt
def getgraphback(request, id):
    logger.info("getgraphback 진입")

    idx = id
    data = Data.objects.filter(idx=idx).values()[0]['fixednumfile']
    df = pd.read_json(data, orient='split')
    cols = df.columns.tolist()
    charts = []
    for i in cols:
        charts.append(df.loc[:, i].tolist())

    corrs = pd.DataFrame((df.corr()), columns=cols).fillna(0)
    corrz = corrs.to_numpy().tolist()

    context = {'cols': cols, 'charts': charts, 'id': idx, 'corrz': corrz}

    return render(request, 'graph.html', context)

# def getgraph00(request):
#     logger.info("getgraph 진입")
#
#     if request.method == 'POST':
#         idx = request.POST.get('id')
#         data = Data.objects.filter(idx=idx).values()[0]['fixednumfile']
#         df_ori = pd.read_json(data, orient='split')
#         cols = df_ori.columns.tolist()
#         for i in cols :
#             if df_ori[i].dtypes == 'O' :
#                 cols.remove(i)
#         df= df_ori[cols]
#         idxs = df.index.tolist()
#         charts = []
#         for i in cols :
#             charts.append(df.loc[:, i].tolist())
#         colors20 = ["#9999FF","#CC99CC","#66CC66","#FFFF33","#00CCCC","#FF0066","#993333",
#                   "#006666","#FF9933","#66FFCC","#660066","#3399FF","#6699CC","#999999",
#                   "#6666CC","#FFCC66","#66FFFF","#FF9966","#FF6633","#99FF00"]
#         if len(cols) <= len(colors20) :
#             colors = colors20[:len(cols)]
#         else :
#             total_len = round(len(cols)/len(colors20))+1
#             colors_total = []
#             for i in range(total_len) :
#                 colors_total += colors20
#             colors = colors_total[:len(cols)]
#         context = {'cols' : cols, 'charts' : charts, 'idxs' : idxs, 'colors':colors, 'id':idx}
#     return render(request, 'graph.html', context)

@csrf_exempt
def presplitdata(request):
    logger.info("presplitdata 진입")

    if request.method == 'POST':
        idx = request.POST.get('id')
        data = Data.objects.filter(idx=idx).values()[0]['fixednumfile']
        df = pd.read_json(data, orient='split')
        cols = df.columns.tolist()

        context = {'cols': cols, 'id': idx}

    return render(request, 'splitdata.html', context)

@csrf_exempt
def splitdata(request):
    logger.info("splitdata 진입")

    if request.method == 'POST':
        idx = request.POST.get('id')
        xcols = request.POST.getlist('xcols[]')
        ycol = request.POST.get('ycol')
        testsize = int(request.POST.get('testsize'))/100

        d = Temp(xcols=xcols,
                 ycol=ycol,
                 testsize=testsize,
                 dataid=idx)
        d.save()
        tempid = Temp.objects.latest('idx').idx

        modellist = ['Regressor', 'Classifier']
        scalerlist = ['MinMax', 'Standard']

    context = {'id':idx, 'tempid':tempid, 'modellist':modellist, 'scalerlist':scalerlist}

    return render(request, 'choosemodel.html', context)

@csrf_exempt
def presplitdataback(request, id):
    logger.info("presplitdataback 진입")

    idx = id
    data = Data.objects.filter(idx=idx).values()[0]['fixednumfile']
    df = pd.read_json(data, orient='split')
    cols = df.columns.tolist()

    context = {'cols': cols, 'id': idx}

    return render(request, 'splitdata.html', context)

@csrf_exempt
def modelchoose(request):
    logger.info("modelchoose 진입")

    if request.method == 'POST':
        tempid = int(request.POST.get('tempid'))
        model = request.POST.get('model')
        scale = request.POST.get('scale')

        xcols = Temp.objects.filter(idx=tempid).values()[0]['xcols']
        ycol = Temp.objects.filter(idx=tempid).values()[0]['ycol']
        testsize = float(Temp.objects.filter(idx=tempid).values()[0]['testsize'])
        dataid = Temp.objects.filter(idx=tempid).values()[0]['dataid']

        data = Data.objects.filter(idx=dataid).values()[0]['fixednumfile']
        df_ori = pd.read_json(data, orient='split')

        y = df_ori[ycol]

        xcols = xcols.replace('[','').replace(']','').replace(', ','||').replace("'","")
        xcols = xcols.split('||')
        df = df_ori[xcols]

        if scale == 'MinMax' :
            scaler = MinMaxScaler().fit_transform(df)
            df = pd.DataFrame(scaler, columns=xcols)
        elif scale == 'Standard' :
            scaler = StandardScaler().fit_transform(df)
            df = pd.DataFrame(scaler, columns=xcols)

        if model == 'Regressor' :
            mod = XGBRegressor()
        # elif model == 'Classifier' :
        else :
            mod = XGBClassifier()

        X_train, X_test, y_train, y_test = train_test_split(df, y, test_size=testsize)

        mod = mod.fit(X_train, y_train)

        score = round(mod.score(X_test, y_test), 2)

        context = {'id': dataid, 'tempid': tempid, 'model': model, 'scaler': scale, 'score':score}

        return render(request, "score.html", context)

@csrf_exempt
def splitdataback(request, tempid) :
    logger.info("modelchooseback 진입")

    tempid = int(tempid)
    idx = Temp.objects.filter(idx=tempid).values()[0]['dataid']
    modellist = ['Regressor', 'Classifier']
    scalerlist = ['MinMax', 'Standard']

    context = {'id': idx, 'tempid': tempid, 'modellist': modellist, 'scalerlist': scalerlist}

    return render(request, 'choosemodel.html', context)



