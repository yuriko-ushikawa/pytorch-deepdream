#./run.sh /media/haria/data/data/vgg_face/ 28
export PYTHONPATH=$PYTHONPATH:~/mxnet/python:~/mxnet/amalgamation/python/
num_examples=`cat train.txt |wc -l`
num_classes=`cat labels.txt |wc -l`
epochs=200
batch_size=40

#python train.py --network squeezenet --num-examples $num_examples --num-classes $num_classes --model-prefix `pwd`/face  --data-dir `pwd`/ --batch-size $batch_size --load-epoch $epoch_first_stage --lr 0.01 --lr-factor 0.1 --lr-factor-epoch 25 --num-epoch $epochs
python train.py --network squeezenet --num-examples $num_examples --num-classes $num_classes --model-prefix `pwd`/face  --data-dir `pwd`/ --batch-size $batch_size --lr 0.1 --lr-factor 0.1 --lr-factor-epoch 50 --num-epoch $epochs
