def weightgiver(api_key, host, offer_id, prob_minmax = (0.1, 0.9)):
    
    """
        Функция для раздачи офферам в партнёрке весов (сплитование)
    
        Args:
            api_key: (str) - апи-ключ для доступа в кейтаро
            host: (str) - url для доступа к кейтаро
            offer_id: (str) - id оффера из кейтаро
            prob_minmax: (tuple) - вектор из интервала минимальнго и максимального процента, который может дать модель
    
    """
    
    from scipy.optimize import linprog    
    import numpy as np
    from MVPanalytics.keitaro import keitaro_parser
    spl = keitaro_parser(api_key, host,
        interval='today',
        filters = [{'name': "stream_id", 'operator': "EQUALS", 'expression': offer_id}],
    grouping = ["stream", "offer"],
    metrics = ['epc_confirmed', 'clicks']
    )


    c = np.array(spl['epc_confirmed'].values)*(-1)

    A_eq = np.array([np.ones(len(c))])
    b_eq = np.array([1])

    prob_n = np.array([ prob_minmax for i in range(len(c))])

    res = linprog(c = c, A_eq = A_eq, b_eq = b_eq, bounds = prob_n)

    spl['weights'] = res.x *100
    return(spl)

def off_analyzer(data,target, report_type, showcases = False):
    
    """
        Функция, позволяющая выявлять витрины по потоку (или офферу), на которых его: target < EPC, 0 < EPC < target, EPC=0
        
        Args:
            data: (pd.Dataframe) - спаршенные данные с кейтаро, которые должны содержать колонки ['epc_confirmed', 'external_id', 'clicks', 'sale_revenue']
            target: (float) - нижнее удовлетворяющее значеие EPC
            showcases: (bool) - нужна ли подробная таблица, которая выдаёт сами external с epc ниже таргета (рботает для report_type == 'offer')
            report_type: (str) - Вид отчёта, если 'city' - делает разбивку по городам, если 'offer' - то отчёт по !Одному! офферу. Отчёт по городам рабоатет для всех офферов
            
            Выдача:
                Если showcases = False/report_type == 'city' : Возвращает одну таблицу, которая показывает сколько кликов отливается на витрины с epc по потоку/потоку+городу target < EPC, 0 < EPC < target, EPC=0 без уточнения того, какие это витрины
                Если showcases = True: Возвращает 2 таблицы, первая - как из showcases = False, вторая - вместе с external_id
    """
    
    
    if report_type == 'offer':
        data['more'] = data['epc_confirmed'].apply(lambda x: f'more than {target} epc' if x >target else( f'less then {target}' if ((x<target)&(x>0))  else 'zero_epc'))
        gr = data[['more', 'epc_confirmed','clicks','sale_revenue']].groupby(by='more').agg({'clicks':['sum','mean','max'], 'sale_revenue':'sum', 'epc_confirmed':['min', 'max']})

        gr['epc_agregated'] = gr[('sale_revenue','sum')]/gr[('clicks', 'sum')]
        if showcases == False:
            return(gr)
        else:
            gr_1 = data[['more', 'external_id','clicks','epc_confirmed']].groupby(by=['more','external_id']).sum().sort_values(by=['more','clicks'], ascending=False)
            return(gr, gr_1)
    
    if report_type == 'city':
        gr = data[['offer','city','epc_confirmed','clicks','sale_revenue']].groupby(by=['offer','city']).agg({'clicks':['sum','mean','max'], 'sale_revenue':'sum', 'epc_confirmed':['min', 'max']}).sort_values(by = ['offer',('clicks', 'sum')],ascending = False)

        gr['epc_agregated'] = gr[('sale_revenue','sum')]/gr[('clicks', 'sum')]
    
        gr[('clicks', '% of offer')] = 100*(data[['offer', 'city','clicks']].groupby(['offer', 'city']).sum())/(data[['offer', 'clicks']].groupby('offer').sum())
        return(gr.round(2))

def streamdiff(params_pars, target, metric, channel,minclick):
    '''
    Скрипт позволяет смотреть, сколько в рамках какого-то канала(витрина, вебмастер, пртнёр и тд) за промежуток времени(указыывается в параметрах запроса) было моментов в ремени в который целевая метрика была больше и меньше таргета
    
    Args:
    params_pars: dict() - параметры запроса функции keitaro_parser
    target: float - целевое значение с которым сравнивается
    metrics: string - метрика, по которой будет подсчёт
    channel: string - то, по чему должна идти группировка (stream\offer...)
    minclick: int - минимальное количество кликов, при который наблюдение будет взято для подсчёта сводной таблицы (напимер, если minclick=10, то в выборку не пойдут дни(если группировка по дням) в которые на потоке (если channel = 'streaam') было строго больше эктого количествоа кликов)
    
    '''
    from MVPanalytics.keitaro import keitaro_parser
    import matplotlib.pyplot as plt 
    import numpy as np 
    import pandas as pd 
    strm = keitaro_parser(**params_ext)
    strm = strm.loc[strm['clicks']>minclick]
    retr = strm[strm[metric] > target].groupby(channel).count()[[metric]].merge(strm[strm[metric] < target].groupby(channel).count()[[metric]], right_index=True, left_index=True, how = 'outer', suffixes = ['_more '+str(target), '_less '+str(target)]).fillna(0)
    retr['percent >'+str(target)] = retr[metric+'_more '+str(target)]*100/(retr[metric+'_more '+str(target)] + retr[metric+'_less '+str(target)])
    retr = retr.merge(strm[[channel, 'clicks']].groupby(channel).sum()['clicks'], right_index = True, left_index = True)
    if metric == 'epc_confirmed':
        retr = retr.merge(strm[[channel, 'sale_revenue']].groupby(channel).sum()['sale_revenue'], right_index = True, left_index = True)
        retr[metric+' for period'] = retr['sale_revenue']/retr['clicks']
        retr.drop(columns=['sale_revenue'], inplace=True)
    return(retr.sort_values('percent >'+str(target), ascending = 0))