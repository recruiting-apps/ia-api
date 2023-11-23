import sys
import os
import textdistance
import fitz
import re

skill_path = 'src/pdf/headers/skills.txt'
other_path = 'src/pdf/headers/others.txt'

def pdf2text(path):
    text=list()
    spans=list()
    doc = fitz.open(path)
    for page in doc:
        blocks = page.get_text("dict")["blocks"]
        for b in blocks:
            if b['type'] == 0:
                for l in b["lines"]:
                    for s in l["spans"]:
                        text.append(s['text'])
                        spans.append(s)
    return spans,text

def get_headers(spans):
    headers=list()
    for s in spans:
        if "Bold" in s['font'] or "Italic" in s['font'] or "Black" in s['font'] :
            text=re.sub("[^a-zA-Z ]","",s['text'])
            text=text.lower().lstrip().rstrip()
            if len(text.split())<=3 and text != "" :
                add=text
                headers.append(add)
    return headers

def read_pdf(path):
    filepath = os.path.join(path)
    spans,text=pdf2text(filepath)

    return get_headers(spans), text, spans

def get_pdfs(folderpath):
    final=list()
    wholespans=list()
    wholetext=list()

    if os.path.isdir(folderpath):
        nFiles = len(os.listdir(folderpath))
        for f in os.listdir(folderpath):
            filepath = os.path.join(folderpath, f)
            try:
                span_headers,text,spans=read_pdf(filepath)
                wholespans.append(spans)
                wholetext.append(text)
                final.append(span_headers)
            except:
                continue
    else:
        span_headers,text,spans=read_pdf(folderpath)
        wholespans.append(spans)
        wholetext.append(text)
        final.append(span_headers)

    print("No. of parsed files = ", len(wholetext))
    return final ,wholetext ,wholespans


def clean_data(text):
    text=re.sub("[^a-zA-Z0-9 ]","",text)
    text=text.lower().lstrip().rstrip()
    return text


def real_headers(header,skills,others):
    final=set()
    real=list()
    real2=list()
    for h in header:
        weight=list()
        weight2=list()

        ##for skills ##
        for i in range (len(skills)):
            weight.append((h,textdistance.ratcliff_obershelp(h,skills[i])))
            if i == len(skills)-1:
                weight.sort(key=lambda x: x[1],reverse = True)
                real.append(weight[0])

        ##for other headers ##
        for j in range (len(others)):
            weight2.append((h,textdistance.ratcliff_obershelp(h,others[j])))
            if j== len(others)-1:
                weight2.sort(key=lambda y: y[1],reverse = True)
                real2.append(weight2[0])

    real.sort(key=lambda x: x[1],reverse = True)
    real2.sort(key=lambda y: y[1],reverse = True)

    for s in real:
        if s[1]>0.8:
            final.add(s[0])

    for k in real2:
        if k[1]>0.6:
            final.add(k[0])
    return final

def indices(doc,headers):
    indexes=list()
    for h in headers:
        for i in range(len(doc)):
            if h in doc[i]['text'].lower():
                if "Bold" in doc[i]['font'] or "Italic" in doc[i]['font'] or "Black" in doc[i]['font'] :
                    indexes.append((h,i))
                    break
    indexes.sort(key=lambda y: y[1])
    return indexes

def extract_content(indexes,docx):
    content=list()
    for i in range(len(indexes)):
        if i==len(indexes)-1:
            content.append((indexes[i][0],clean_data(str(docx[indexes[i][1]+1:]))))
            break
        content.append((indexes[i][0],clean_data(str(docx[indexes[i][1]+1:indexes[i+1][1]]))))
    return content

def outoffile():
    f=open(skill_path,"r")
    result=f.read().splitlines()
    f1=open(other_path,"r")
    result1=f1.read().splitlines()
    return result,result1


def get_content(path):
    result,doc,spans = get_pdfs(path)
    all_skills, all_other_skills = outoffile()

    print(result)

    # Obtener sus cabeceras reales
    pdf_real_headers = real_headers(result[0],all_skills,all_other_skills)
    index=indices(spans[0], pdf_real_headers)

    # Extraer el contenido del cv
    pdf_content=extract_content(index,doc[0])

    return pdf_content