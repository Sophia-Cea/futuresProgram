from inspect import getfile
from operator import ge
import requests


url = 'https://finviz.com/futures_performance.ashx'


def getDayFuturePerf(session):
    headers = {
        'authority': 'finviz.com',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="98", "Google Chrome";v="98"',
        'accept': 'application/json,*/*',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://finviz.com/futures_performance.ashx',
        'accept-language': 'en-US,en;q=0.9',
        'cookie': '_ga=GA1.2.1433269068.1644857401; _gid=GA1.2.366353804.1644857401; pv_date=Mon Feb 14 2022 10:50:00 GMT-0600 (Central Standard Time); usprivacy=1---; __qca=P0-1349380262-1644857400750; __aaxsc=2; _admrla=2.2-b645ccefd7965025-27380052-8db6-11ec-867f-57bd53afba1e; cto_bundle=IC_KaV8zNlRjMnpDSGRvdzVMWTFOdHdtR2VQdEMxaE9jNWZuYiUyRlVXb3JUbUJLaVY5dWFxYTN2OURuZ0t5MDhvQXBUMDNWWVN5a1pCRSUyRjQ0Mkk0QVkwOHBaaGwzY0RFWmQ1ZSUyQk1MRjdncjliWUxnZEdpZHhGbFNmc1dlaThzMENMS1ZXQ1lLYiUyRk9vbUNBOU1EYVRKejg0Nm5MQSUzRCUzRA; __gads=ID=322adc14b26a574c:T=1644857402:S=ALNI_MaalNEUhsfMWfp2jQDzsux631p3ew; pv_count=2; aasd=3%7C1644860965495; _awl=2.1644860965.0.5-97630df246e0ef30f984e1e8afac0bdc-6763652d75732d63656e7472616c31-0',
    }

    response = session.get('https://finviz.com/api/futures_perf.ashx', headers=headers)
    return response

def getWeekFuturePerf(session):
    headers = {
        'authority': 'finviz.com',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="98", "Google Chrome";v="98"',
        'accept': 'application/json,*/*',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://finviz.com/futures_performance.ashx?v=12',
        'accept-language': 'en-US,en;q=0.9',
        'cookie': '_ga=GA1.2.1433269068.1644857401; _gid=GA1.2.366353804.1644857401; usprivacy=1---; __qca=P0-1349380262-1644857400750; __aaxsc=2; _admrla=2.2-b645ccefd7965025-27380052-8db6-11ec-867f-57bd53afba1e; __gads=ID=322adc14b26a574c:T=1644857402:S=ALNI_MaalNEUhsfMWfp2jQDzsux631p3ew; pv_date=Tue Feb 15 2022 09:51:29 GMT-0600 (Central Standard Time); cto_bundle=ZDBzY18zNlRjMnpDSGRvdzVMWTFOdHdtR2VPNDZObHN5aWhtNVBhdWRkRUpIY0dKazdJSkU5TzI2UWdPbXolMkZlRHprQ25NMXRlRmlld3NtVVdGemVYUzMlMkI5VjJVQVFtWDViNk4lMkJwSTV3JTJCQXdQN3lpakRxaW5kMVdzTXlRbXRMN3ZJNDNwUEJwZkQ2N08wbzg4QzNtSkUzNWk2dyUzRCUzRA; pv_count=11; IC_ViewCounter_finviz.com=2; aasd=3%7C1644952041369; _awl=2.1644952044.0.5-97630df246e0ef30f984e1e8afac0bdc-6763652d75732d63656e7472616c31-0',
    }

    params = (
        ('v', '12'),
    )

    response = session.get('https://finviz.com/api/futures_perf.ashx', headers=headers, params=params)

    return response

def getMonthFuturePerf(session):
    headers = {
        'authority': 'finviz.com',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="98", "Google Chrome";v="98"',
        'accept': 'application/json,*/*',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://finviz.com/futures_performance.ashx?v=13',
        'accept-language': 'en-US,en;q=0.9',
        'cookie': '_ga=GA1.2.1433269068.1644857401; _gid=GA1.2.366353804.1644857401; usprivacy=1---; __qca=P0-1349380262-1644857400750; __aaxsc=2; _admrla=2.2-b645ccefd7965025-27380052-8db6-11ec-867f-57bd53afba1e; __gads=ID=322adc14b26a574c:T=1644857402:S=ALNI_MaalNEUhsfMWfp2jQDzsux631p3ew; pv_date=Thu Feb 17 2022 09:49:35 GMT-0600 (Central Standard Time); cto_bundle=lM16nl8zNlRjMnpDSGRvdzVMWTFOdHdtR2VHVHFyY0gwcGN2bEVSeTQlMkZMOTFxQUd3ZHRMcXFEbkR0TlhkRWRvMFpNZm5WZTlSZkZEYlBsJTJCYkpJd2Q1eUhTd0JJdmlXR2FIeVM4NlZLRlE5ZzNQbHQ0UVdXM0U1TW8yZ21Jc0xwWnd0TEZGZ1FPeEVRN1pnYmtBaEM2MlRaZGpCb1pxNFNjd212YThhbTJWRlBUNk1ieFBHZVZIQ0RBRzI4R3VnJTJGQVJlUDk; pv_count=4; IC_ViewCounter_finviz.com=4; aasd=12%7C1645112976635; _awl=2.1645113092.0.5-97630df246e0ef30f984e1e8afac0bdc-6763652d75732d63656e7472616c31-0',
    }

    params = (
        ('v', '13'),
    )

    response = session.get('https://finviz.com/api/futures_perf.ashx', headers=headers, params=params)

    return response

def writeInfoToFile(futureInfo):
    with open("futures.txt", 'w') as file:
        file.write('[\n')
        for thingy in futureInfo:
            file.write('\t{\n')
            for unit in thingy:
                file.write("\t\t'" + str(unit) + "': '" + str(thingy[unit]) + "',\n")
            file.write('\t},\n')

        file.write(']\n')



def getDayInfo():
    with requests.Session() as session:
        info = getDayFuturePerf(session)
        info: str = str(info.content)[2:-1]
        return info

def getWeekInfo():
    with requests.Session() as session:
        info = getWeekFuturePerf(session)
        info: str = str(info.content)[2:-1]
        # with open('file.txt', 'w') as file:
        #     file.write(str(info))
        return info

def getMonthInfo():
    with requests.Session() as session:
        info = getMonthFuturePerf(session)
        info: str = str(info.content)[2:-1]
        with open('file.txt', 'w') as file:
            file.write(str(info))
        return info
