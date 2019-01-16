'''
Python 3.6 
Pytorch 0.3
This project is produced by Hongyu Wang in June 2018 at MSRA.
And really thanks to Dr. Jianshu Zhang from USTC for useful comments and suggestions.
'''
import numpy
import pickle as pkl
import sys
import torch


def dataIterator(feature_file,label_file,dictionary,batch_size,batch_Imagesize,maxlen,maxImagesize):
    
    fp=open(feature_file,'rb')
    features=pkl.load(fp)
    fp.close()

    fp2=open(label_file,'r')
    labels=fp2.readlines()
    fp2.close()

    targets={}
    # map word to int with dictionary
    for l in labels:
        tmp=l.strip().split()
        uid=tmp[0]
        w_list=[]
        for w in tmp[1:]:
            if w in dictionary:
                w_list.append(dictionary[w])
            else:
                print('a word not in the dictionary !! sentence ',uid,'word ', w)
                sys.exit()
        targets[uid]=w_list


    imageSize={}
    imagehigh={}
    imagewidth={}
    for uid,fea in features.items():
        imageSize[uid]=fea.shape[1]*fea.shape[2]
        imagehigh[uid]=fea.shape[1]
        imagewidth[uid]=fea.shape[2]

    imageSize= sorted(imageSize.items(), key=lambda d:d[1],reverse=True) # sorted by sentence length,  return a list with each triple element


    feature_batch=[]
    label_batch=[]
    feature_total=[]
    label_total=[]
    uidList=[]

    batch_image_size=0
    biggest_image_size=0
    i=0
    for uid,size in imageSize:
        if size>biggest_image_size:
            biggest_image_size=size
        fea=features[uid]
        lab=targets[uid]
        batch_image_size=biggest_image_size*(i+1)

        if len(lab)>maxlen:
            print('sentence', uid, 'length bigger than', maxlen, 'ignore')

        elif len(lab)< 7:
            print('sentence', uid, 'length bigger than', maxlen, 'ignore')

        elif size>maxImagesize:
            print('image', uid, 'size bigger than', maxImagesize, 'ignore')


        elif imagehigh[uid] > 90:
            print('11')

        elif imagewidth[uid] < 440:
            print('11')

        else:
            uidList.append(uid)
            if batch_image_size>batch_Imagesize or i==batch_size: # a batch is full

                if label_batch:
                    feature_total.append(feature_batch)
                    label_total.append(label_batch)

                i=0
                biggest_image_size=size
                feature_batch=[]
                label_batch=[]
                feature_batch.append(fea)
                label_batch.append(lab)
                batch_image_size=biggest_image_size*(i+1)
                i+=1
            else:
                feature_batch.append(fea)
                label_batch.append(lab)
                i+=1

    # last
    feature_total.append(feature_batch)
    label_total.append(label_batch)
    print('total ',len(feature_total), 'batch data loaded')


    return feature_total,label_total