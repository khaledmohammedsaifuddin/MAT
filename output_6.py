# -*- coding: utf-8 -*-
"""
Created on Sat Jul 25 08:47:30 2020

@author: hamim
"""
import pandas as pd
import glob
import os
import collections
import textdistance
import regex as re

'''
Reading all files from this below folder
'''

path = r'E:/OSU/Research/Data_AU/after_filtering/Covid/Mat_drug_files/Old_data/All2/6_months_old/Association/Temp/'                     # use your path
all_files = glob.glob(os.path.join(path, "*.csv"))     # advisable to use os.path.join as this makes concatenation OS independent


'''
Putting the data into a pandas dataframe
'''
df_from_each_file = (pd.read_csv(f,low_memory=False) for f in all_files)
c   = pd.concat(df_from_each_file, ignore_index=True)

'''
Reading dictionary->Drug_streey_term
'''
file = open(r"E:\OSU\Research\Data_AU\after_filtering\Covid\Mat_drug_files\Bio_Dict\Drug_street_term.txt","r")
street_term=file.read().splitlines()
street_term=[x.lower() for x in street_term]
file.close()

'''
Reading dictionary->Illicit_drug
'''
file2 = open(r"E:\OSU\Research\Data_AU\after_filtering\Covid\Mat_drug_files\Bio_Dict\Illicit_drug.txt","r")
illicit_term=file2.read().splitlines()
illicit_term=[x.lower() for x in illicit_term]
file2.close()

'''
Reading dictionary->not_mat
'''
file3 = open(r"E:\OSU\Research\Data_AU\after_filtering\Covid\Mat_drug_files\Bio_Dict\nMAT.txt","r")
nMAT_term=file3.read().splitlines()
nMAT_term=[x.lower() for x in nMAT_term]
file3.close()

'''
Reading other files
'''
file4 = open(r"E:\OSU\Research\Data_AU\after_filtering\Covid\Mat_drug_files\Bio_Dict\delete.txt","r")
pres_term=file4.read().splitlines()
pres_term=[x.lower() for x in pres_term]
file4.close()

'''
Necessary lists
'''
disease=[]
drug=[]
drug0=[]
MAT_drug_only_with_all_possible_name=[]
term=[]
term0=[]
term1=[]
a_d=[]
a_d0=[]
a_d1=[]
nMAT0=[]
nMAT=[]
nMAT1=[]
street=[]
illicit=[]
heroin=[]
cocaine=[]
alcohol=[]
marijuana=[]
prescription=[]

'''
Extracting the Use/abuse terms from tweets in the presence of drugs
'''
for i in range (len(c['Drugs'])):
    if  c['Drugs'][i]!='[]':
        if c['Use/Abuse Terms'][i] !='[]' :
            term0.append(c['Use/Abuse Terms'][i])
            a=c['Use/Abuse Terms'][i]
            a=a.strip("[]")
            r1=re.findall(r',',a)
            if len(r1)!=0:
                a=a.split(',')
                for i in a:
                    term.append(i)
            else:
                term.append(a)
for i in term:
    a=str(i)
    a=a.strip('"')
    a=a.strip(' ')
    term1.append(a)
term1_counter=collections.Counter(term1)
term0_counter=collections.Counter(term0)

'''
Extracting the drug terms from tweets
'''
MAT=['suboxone','naloxone','naltrexone','revia','vivitro','depade','buprenorphine','bupes', 'sobos', 'bup', 'bupe','methadone','methadose','dollies','meth','metho','jungle juice','amidone']

sub_term=['suboxone']
sub=[]
bup_term=['buprenorphine','bupes', 'sobos', 'bup', 'bupe']
bup=[]
nalo_term=['naloxone']
nalo=[]
nalt_term=['naltrexone','revia','vivitro']
nalt=[]
meth_term=['methadone','methadose','dollies','meth','metho','jungle juice','amidone']
meth=[]

for i in range (len(c['Drugs'])):
    if c['Drugs'][i]!='[]' :
        a=c['Drugs'][i]
        a=a.strip("[]")
        r4=re.findall(r',',a)
        if len(r4)!=0:
            a=a.split(',')
            for i in a:
                b=str(i)
                b=b.strip('"')
                b=b.strip(' ')
                b=re.findall(r"\w+",b)
                b = ''.join(b)
                drug0.append(b)
        else:
            b=str(a)
            b=b.strip('"')
            b=b.strip(' ')
            b=re.findall(r"\w+",b)
            b = ''.join(b)
            drug0.append(b)
for i in range (len(drug0)):
    for x in MAT:
        if  textdistance.jaro_winkler.normalized_similarity( x.lower(),drug0[i].lower())>=0.95:
            MAT_drug_only_with_all_possible_name.append(drug0[i])
            break
    for x in nMAT_term:
        if  textdistance.jaro_winkler.normalized_similarity( x.lower(),drug0[i].lower())>=0.95:
            nMAT1.append(drug0[i])
            break
MAT_drug_only_with_all_possible_name_counter=collections.Counter(MAT_drug_only_with_all_possible_name)
nMAT1_counter=collections.Counter(nMAT1)

print('withoutmat',len(nMAT1))


heroin_term=['heroin','brown sugar','china white','chiva dope','h','horse','skag','skunk','smack','white horse','big h','dope','hell dust','black tar heroin','happy pills','hillbilly heroin']
marijuana_term=['marijuana','join','tree','weed','pot','420','blunt','bud','doobie','dope','ganja','grass','green','herb','joint','mary jane','pot','reefer','sinsemilla','skunk','smoke','stinkweed','trees']
cocaine_term=['cocaine','blow','bump','c','candy','charlie','coke','crack','dust','flake','nose candy','rock','snow','sneeze','sniff','toot','white rock']
alcohol_term=['alcohol','alcoholic','liquor','beer','wine']
combaine_illegal=heroin_term+marijuana_term+alcohol_term+cocaine_term

import re
for x in nMAT1:
    for i in heroin_term:
        if textdistance.jaro_winkler.normalized_similarity( x.lower(),i.lower())>=0.95:
            heroin.append(x)
            break
for x in nMAT1:
    for i in marijuana_term:
        if textdistance.jaro_winkler.normalized_similarity( x.lower(),i.lower())>=0.95:
            marijuana.append(x)
            break
for x in nMAT1:
    for i in alcohol_term:
        if textdistance.jaro_winkler.normalized_similarity( x.lower(),i.lower())>=0.95:
            alcohol.append(x)
            break
for x in nMAT1:
    for i in cocaine_term:
        if textdistance.jaro_winkler.normalized_similarity( x.lower(),i.lower())>=0.95:
            cocaine.append(x)
            break
for x in nMAT1:
    for i in street_term:
        if textdistance.jaro_winkler.normalized_similarity( x.lower(),i.lower())>=0.95:
            street.append(x)
            break
for x in nMAT1:
    for  i in illicit_term:
        if textdistance.jaro_winkler.normalized_similarity( x.lower(),i.lower())>=0.95:
            illicit.append(x)
            break

for x in nMAT1:
    x=re.findall(r"\w+",x)
    x = ''.join(x)
    if x not in combaine_illegal:
        prescription.append(x)

'''
do it for, bup_term,meth_term etc.........
'''
for x in MAT_drug_only_with_all_possible_name:
    for  i in sub_term:
        if textdistance.jaro_winkler.normalized_similarity( x.lower(),i.lower())>=0.95:
            sub.append(x)
            break
print(len(sub))


streetname_counter=collections.Counter(street)
illicit_counter=collections.Counter(illicit)
prescription_counter=collections.Counter(prescription)

opioid=[]
for x in pres_term:
    for i in prescription:
        if textdistance.jaro_winkler.normalized_similarity( x.lower(),i.lower())>=0.95:
            opioid.append(x)
            break

print ("MAT=",len(MAT_drug_only_with_all_possible_name))
print ("illicit=",len(alcohol)+len(heroin)+len(marijuana)+len(cocaine))
print ("street=",len(street))
print("Heroine=",len(heroin))
print("Marijuana=",len(marijuana))
print("Cocaine=",len(cocaine))
print("Alcohol=",len(alcohol))
print("Other Opioid=",len(prescription))

k=1



l=[]
l1=[]
a='need'
#drug0.count("['naloxone', 'buprenorphine']")
### abuse term koto bar kore ase kon drug a
for i in range (len (c['Drugs'])):
    if c['Use/Abuse Terms'][i]!='[]':
        x=c['Use/Abuse Terms'][i]
        x=x.strip("")
        x=re.findall(r'\w+',x)
        x=x[0]
        if textdistance.jaro_winkler.normalized_similarity( x.lower(),a.lower())>=0.95:
            if (c['Drugs'][i])!='[]':
                b=c['Drugs'][i]
                b=b.strip("[]")
                b=str(b)
                r1=re.findall(r',',b)
                if len(r1)!=0:
                    b=b.split(',')
                    for i in b:
                        l.append(i)
                else:
                    l.append(b)
for i in l:
    f=str(i)
    f=f.strip('"')
    f=f.strip(' ')
    l1.append(f)
z=collections.Counter(l1)

al=0
# month wise analysis
for j in range (len(c['Drugs'])):
    drug_temp=[]
    if c['Drugs'][j]!='[]' :
        a=c['Drugs'][j]
        a=a.strip("[]")
        r4=re.findall(r',',a)
        if len(r4)!=0:
            a=a.split(',')
            for i in a:
                b=str(i)
                b=b.strip('"')
                b=b.strip(' ')
                b=re.findall(r"\w+",b)
                b = ''.join(b)
                drug_temp.append(b)
        else:
            b=str(a)
            b=b.strip('"')
            b=b.strip(' ')
            b=re.findall(r"\w+",b)
            b = ''.join(b)
            drug_temp.append(b)

        for x in drug_temp:
            for i in alcohol:
                if textdistance.jaro_winkler.normalized_similarity( x.lower(),i.lower())>=0.95:
                    al=al+1
                    a_d0.append(c['date'][j])
                    a=c['date'][j]
                    a=a.strip("[]")
                    r4=re.findall(r',',a)
                    if len(r4)!=0:
                        a=a.spliit(',')
                        for l in a:
                            a_d.append(l)
                    else:
                        a_d.append(a)
                    break
for i in a_d:
    a=str(i)
    a_d1.append(a)
a_d1_counter=collections.Counter(a_d1)
a_d0_counter=collections.Counter(a_d0)



'''
###Month wise analysis
for i in range (len(a_d1)):
    a=str(re.findall(r'(-03-)',a_d1[i]))
    if a!='[]':
        b.append(a)
'''
