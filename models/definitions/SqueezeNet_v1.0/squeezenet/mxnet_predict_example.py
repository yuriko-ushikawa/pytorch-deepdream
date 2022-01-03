import sys, os, time
import subprocess
import threading
curr_path = os.path.dirname(os.path.abspath(os.path.expanduser(__file__)))
sys.path.append("~/mxnet/amalgamation/python/")
sys.path.append("~/mxnet/python/")

from mxnet_predict import Predictor, load_ndarray_file
import mxnet as mx
import logging
import numpy as np
from skimage import io, transform
# Load the pre-trained model
prefix = "./face-0"
num_round = 125
batch_size = 20
if len(sys.argv) >2:
    num_round = int(sys.argv[2])
symbol_file = "%s-symbol.json" % prefix
param_file = "%s-%s.params" % (prefix,str(num_round).zfill(4))
predictor = Predictor(open(symbol_file).read(), open(param_file).read(), {'data':(batch_size , 3, 224, 224)},'gpu',0)
mean_img = load_ndarray_file(open("./mean.bin").read())["mean_img"]

synset = [l.strip() for l in open('./labels.txt').readlines()]

def PreprocessImage(batchs, index, path, show_img=False):
    # load image
    img = io.imread(path)
    #print("Original Image Shape: ", img.shape)
    # we crop image from center
    short_egde = min(img.shape[:2])
    yy = int((img.shape[0] - short_egde) / 2)
    xx = int((img.shape[1] - short_egde) / 2)
    crop_img = img[yy : yy + short_egde, xx : xx + short_egde]
    # resize to 224, 224
    resized_img = transform.resize(crop_img, (224, 224))
    if show_img:
        io.imshow(resized_img)
    # convert to numpy.ndarray
    sample = np.asarray(resized_img) * 255
    # swap axes to make image from (224, 224, 3) to (3, 224, 224)
    sample = np.swapaxes(sample, 0, 2)
    sample = np.swapaxes(sample, 1, 2)

    # sub mean
    normed_img = sample - mean_img
    normed_img.resize(1, 3, 224, 224)
    
    batchs[index] = normed_img
    

if __name__=="__main__":
    imageList=[]
    if len(sys.argv) >1:
        folder=sys.argv[1]
        if os.path.isdir(folder):
            items= subprocess.check_output("tree -i -f %s|grep \.jpg"%folder,shell=True).strip().split("\n")
            imageList.extend(items)
        else:
            if os.path.exists(folder):
                # its a image actually
                imageList.append(folder)

    iters = len(imageList)/batch_size 
    if len(imageList)%batch_size >0:
        iters+=1
    for it in range(iters):

        # Get preprocessed batch (single image batch)
        batchs=np.ndarray(shape=[batch_size , 3, 224, 224])
        threads = []
        
        for index in range(batch_size):
            if it*batch_size+index <len(imageList):
                t = threading.Thread(target=PreprocessImage,args=(batchs, index, imageList[it*batch_size+index], False))
                t.start()
                threads.append(t)
        
        for t in threads:
            t.join()
        start = time.time()
        predictor.forward(data=batchs)
        prob = predictor.get_output(0)
        for item in range(batch_size):
            pred = np.argsort(prob[item])[::-1]
            # Get top1 label
            top1 = synset[pred[0]],prob[item][pred[0]]
            if it*batch_size+item <len(imageList):
                print  "top-1", imageList[it*batch_size+item], top1[0], top1[1] 
            # Get top5 label
            #top5 = [(synset[pred[i]],prob[item][pred[i]]) for i in range(5)]
            #for index,topx in enumerate(top5):
            #    print "top-%d"%index, imageList[it*batch_size+item], topx[0], topx[1]
        print "time elapsed: %f."%((time.time()-start)/batch_size)
        '''
        pred = np.argsort(prob)[::-1]
        # Get top1 label
        top1 = synset[pred[0]],prob[pred[0]]
        print image , top1[0], top1[1] , time.time()-start
        # Get top5 label
        #top5 = [(synset[pred[i]],prob[pred[i]]) for i in range(5)]
        #for index,topx in enumerate(top5):
        #    print index, topx[0], topx[1]
        '''

