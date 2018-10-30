#!/usr/bin/env python
# -*- coding: utf-8 -*- 
file=open("recognitionsExpected.txt","w",errors="ignore")
with open('reyyan.test.txt','r',encoding='utf-8',errors="ignore") as f:
    for line in f:
        words=line.split();
        i=0
        length=len(words)
        while (i<length):
            if(words[i]=="[ORG"):
                j=i+2
                while(words[j] != "]"):
                    if(j<len(words)-1):
                        j=j+1
                    else:
                        j=j+1
                        break
                interval=(j-i)-1
                if(interval==1):
                    file.write("B-ORG\n")
                elif(interval==2):
                    file.write("B-ORG\n")
                    file.write("I-ORG\n")
                else:
                    interval=interval-2
                    file.write("B-ORG\n")
                    temp=1
                    while(temp<=interval):
                        file.write("I-ORG\n")
                        temp=temp+1
                    file.write("I-ORG\n")
                i=j+1
            elif(words[i] == "[LOC"):
                j=i+2
                while(words[j] != "]"):
                    if(j<len(words)-1):
                        j=j+1
                    else:
                        j=j+1
                        break
                interval=(j-i)-1
                if(interval==1):
                    file.write("B-LOC\n")
                elif(interval==2):
                    file.write("B-LOC\n")
                    file.write("I-LOC\n")
                else:
                    interval=interval-2
                    file.write("B-LOC\n")
                    temp=1
                    while(temp<=interval):
                        file.write("I-LOC\n")
                        temp=temp+1
                    file.write("I-LOC\n")
                i=j+1
            elif(words[i] == "[PER"):
                j=i+2
                while(words[j] != "]"):
                    if(j<len(words)-1):
                        j=j+1
                    else:
                        j=j+1
                        break
                interval=(j-i)-1
                if(interval==1):
                    file.write("B-PER\n")
                elif(interval==2):
                    file.write("B-PER\n")
                    file.write("I-PER\n")
                else:
                    interval=interval-2
                    file.write("B-PER\n")
                    temp=1
                    while(temp<=interval):
                        file.write("I-PER\n")
                        temp=temp+1
                    file.write("I-PER\n")
                i=j+1
            else:
                if(words[i]is not "[ORG" and words[i]is not "[LOC" and 
                         words[i] is not "[PER" and words[i] is not"]"):
                    file.write("O\n")
                i=i+1
f.close
file.close
                
                
        
            
            
            
            
            
            
            
            
            
            
            
          