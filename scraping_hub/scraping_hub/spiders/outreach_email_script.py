import pandas as pd
import numpy as np

def main():
    x = pd.read_csv('~/Desktop/marcela_outreach/new/emails/dmillerlaw/outreach_emails_for_dmillerlaw.csv')
    x = x.dropna(subset=['email']).reset_index(drop=True)
    x = x.drop_duplicates(subset='email').reset_index(drop=True)
    
    x['email']=x.apply(lambda x:peirama(x),axis=1)
    x = x[x.email != '0'].reset_index(drop=True)
    x['email']=x.apply(lambda x:peirama2(x),axis=1)
    x = x[x.email != '0'].reset_index(drop=True)
    x['email']=x.apply(lambda x:peirama3(x),axis=1)
    x = x[x.email != '0'].reset_index(drop=True)
    x['email']=x.apply(lambda x:peirama4(x),axis=1)
    x = x[x.email != '0'].reset_index(drop=True)
    x['email']=x.apply(lambda x:peirama5(x),axis=1)
    x = x[x.email != '0'].reset_index(drop=True)
    x['email']=x.apply(lambda x:peirama6(x),axis=1)
    x = x[x.email != '0'].reset_index(drop=True)
    x['email']=x.apply(lambda x:peirama7(x),axis=1)
    x = x[x.email != '0'].reset_index(drop=True)
    x['email']=x.apply(lambda x:peirama8(x),axis=1)
    x = x[x.email != '0'].reset_index(drop=True)
    x['email']=x.apply(lambda x:peirama9(x),axis=1)
    x = x[x.email != '0'].reset_index(drop=True)

    x['email']=x.email.astype(str)
    x['email']=x.apply(lambda x:peirama10(x),axis=1)
    
    x['email']=x.email.astype(str)
    x['email']=x.apply(lambda x:peirama11(x),axis=1)
    x = x[x.email != '0'].reset_index(drop=True)

    #x = x.drop_duplicates(subset='email').reset_index(drop=True)
    x.to_csv('~/Desktop/marcela_outreach/new/emails/dmillerlaw/outreach_emails_for_dmillerlaw_processed.csv', index=False)

def peirama(x): 
    lista=[] 
    k=x.email.split(",") 
    for i in k: 
        if ('website' not in i) and ('@id' not in i) and ('@context' not in i) and ('window.App' not in i) and ('@media' not in i) and ('@import' not in i) and ('{"origin' not in i) and ('= true'
  not in i) and ('var key' not in i) and ('colors' not in i) and ('CDATA' not in i) and ('window' not in i) and ('var ' not in i) and ('@type' not in i): 
            lista.append(i) 
        else: 
            pass 
    if len(lista)>0: 
        return set(lista) 
    else: 
        return '0' 

def peirama2(x):  
        #k=list(x.email).split(',')  
        lista=[]  
        for i in list(x.email):  
            if '@' in i:  
                lista.append(i)  
        if len(lista)>0:  
            return lista  
        else:  
            return '0' 
                             




def peirama3(x): 
    #k=list(x.email) 
    lista=[] 
    for i in x.email: 
        if ('.com' in i) or ('.org' in i) or ('.edu' in i) or ('.net' in i) or ('.me' in i) or ('.mil' in i) or ('.us' in i): 
            lista.append(i) 
    if len(lista)>0: 
        return lista 
    else: 
        return '0' 


def peirama4(x): 
    #k=list(x.email) 
    lista=[] 
    for i in x.email: 
        if ('font-face' not in i) and ('charset' not in i): 
            lista.append(i) 
    if len(lista)>0: 
        return lista 
    else: 
        return '0' 


def peirama5(x): 
    #k=list(x.email) 
    lista=[] 
    for i in x.email: 
        if len(i)<50: 
            lista.append(i) 
    if len(lista)>0: 
        return list(set(lista)) 
    else: 
        return '0' 
                                                                                                                                                                                                    


def peirama6(x): 
    k=x.email 
    lista=[] 
    for i in k: 
        try: 
            m=i.split(':')[1] 
            lista.append(m) 
        except: 
            lista.append(i) 
    if len(lista)>0: 
        return list(set(lista)) 
    else: 
        return '0' 
                           


def peirama7(x): 
    #k=list(x.email) 
    lista=[] 
    for i in x.email: 
        ii=i.strip() 
        lista.append(ii) 
    if len(lista)>0: 
        return list(set(lista)) 
    else: 
        return '0' 

def peirama8(x): 
    #k=list(x.email.split(' ')) 
    lista=[] 
    for i in x.email:#k: 
        m=i.split(' ') 
        lista2=[] 
        if len(m)>1: 
            for ii in m: 
                if '@' in ii: 
                    lista2.append(ii) 
        else: 
            lista2.append(m) 
        if len(lista2)>0: 
            lista.append(lista2)  
    if len(lista)>0: 
        return lista 
    else: 
        return '0'



def peirama9(x): 
    lista=[] 
    for i in x.email: 
        for j in i: 
            for w in j: 
                if '@' in w: 
                    lista.append(w) 
    if len(lista)>0: 
        return lista 
    else: 
        return '0' 
                                                           

def peirama10(x):  
    xx=x.email.replace('[','').replace(']','').replace('"','').split(', ')  
    return list(set(xx)) 

def peirama11(x):
    lista=[]
    xx=x.email.replace('[','').replace(']','').replace('"','').split(', ')
    for i in xx:
        if i == '@':
            lista.append('0')
        else:
            lista.append(i.replace('}','').replace('{','').replace('/','').replace('\\',''))
    return list(set(lista))

main()