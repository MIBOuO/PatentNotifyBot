import requests
import json

class Patent:
    def __init__(self, pid, title, date, ipc, content):
        self.pid = pid
        self.title = title
        self.date = date
        self.ipc = ipc
        self.content = content
    def __dict__(self):
        return {
            "pid": self.pid, 
            "title": self.title,
            "date": self.date,
            "ipc": self.ipc,
            "content": self.content,
        }

def get_patents(date_from, date_to = '', ipc = '' , limit = 100000, skip = 0):
    if ipc == '':
        url = 'https://gpss1.tipo.gov.tw/gpsskmc/gpss_api?userCode=a61fB8FD648b0A06&patDB=TWA,TWB,TWD&patAG=A,B&patTY=I,M,D'+ '&ID=' + date_from + ':' + date_to + '&expFld=PN,AN,ID,AD,TI,AB,IC&expFmt=json&expQty=' + str(limit) + '&expSkip=' + str(skip)        
    else:
        ipc = ipc.replace(' ','%20')
        url = 'https://gpss1.tipo.gov.tw/gpsskmc/gpss_api?userCode=a61fB8FD648b0A06&patDB=TWA,TWB,TWD&patAG=A,B&patTY=I,M,D' + '&IC=' + ipc + '&ID=' + date_from + ':' + date_to + '&expFld=PN,AN,ID,AD,TI,AB,IC&expFmt=json&expQty=' + str(limit) + '&expSkip=' + str(skip)
    response = requests.get(url)
    lst = []

    if response.status_code == 200:

        data = response.json()
        if data['gpss-API'].get('total-rec') != None:
            total_num = int(data['gpss-API']['total-rec'])
        else:
            total_num = 0
        total = total_num

        if data['gpss-API']['status'] == 'success' and data['gpss-API'].get('message') == None:
            results = data['gpss-API']['patent']['patentcontent']
            for item in results:
                pid = item['publication-reference']['doc-number']
                title = item['patent-title']
                date = item['publication-reference']['date']
                ipc = []
                for ic in item['classifications-ipc']['ipc']:
                    ipc.append(ic['keyValue'])
                content = item['abstract']['p']
                patent = Patent(pid, title, date, ipc, content)
                lst.append(patent.__dict__())
                    
        elif data['gpss-API']['status'] == 'success' and data['gpss-API'].get('message') == 'No record found':
            print('沒有結果，請更換搜索條件')
        elif data['gpss-API']['status'] == 'fail':
            print('搜尋失敗')
            print(data['gpss-API']['message'])

    else:
        print('API請求失敗')
    return [total_num, lst]

print(get_patents('20230501','20230520','',30 ,30)[1][1])

