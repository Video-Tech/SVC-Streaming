import os
import numpy as np

iters = [i for i in range(1, 11)]

dataset = 'vtl'
opath = '/home/mallesh/deepvideo/data/'+dataset+'/test/'
mv_dir = '/home/mallesh/deepvideo/data/'+dataset+'/test_mv'

def get_bmv_filenames(mv_dir, main_fn):

    fn = main_fn.split('/')[-1][:-4]

    return (os.path.join(mv_dir, fn + '_before_flow_x_0001.jpg'),
            os.path.join(mv_dir, fn + '_before_flow_y_0001.jpg'),
            os.path.join(mv_dir, fn + '_after_flow_x_0001.jpg'),
            os.path.join(mv_dir, fn + '_after_flow_y_0001.jpg'))

def get_flows_size(frame):
    flows = get_bmv_filenames(mv_dir, frame)
    size = 0
    for flow in flows:
        size += os.stat(flow).st_size
    return size

def get_code_size(frame, itr, gop):
    size = 0
    if gop == 0:
        size = os.stat('output_'+str(itr)+'/codes/'+frame+'.codes.npz').st_size
    else:
        size = os.stat('../../icodec/'+dataset+'/codes/'+frame+'.codes.npz').st_size
    return size

def get_number_of_pixels(dset):
    if dset == 'vtl':
        return 352*288.0
    elif dset == 'dhf1k':
        return 640*360.0
    else:
        return 1

for itr in iters:
    recframes = os.listdir('output_'+str(itr)+'/images')
    irecframes = os.listdir('../../icodec/'+dataset+'/images/')
    bpp_itr = []
    sizes = []
    print (itr)

    bits = {}

    for rframe in recframes:
        if rframe in irecframes:
            continue
        oframe = opath+rframe
        size = get_flows_size(rframe) + get_code_size(rframe, itr, 0)
        bpp = size*8/(get_number_of_pixels(dataset))

        #os.system('python ../metric.py -o '+oframe+' -c output_'+str(itr)+'/images/'+rframe+' >> rd/quality_'+rframe[6:-13]+'_itr'+str(itr)+'.txt')
        bits.setdefault(rframe[6:-13], []).append(str(bpp)+'\n')
        
    for irframe in irecframes:
        oframe = opath+irframe
        size = get_code_size(irframe, itr, 1)
        bpp = size*8/(get_number_of_pixels(dataset))

        #os.system('python ../metric.py -o '+oframe+' -c ../../icodec/'+dataset+'/images/'+irframe+' >> rd/quality_'+irframe[6:-13]+'_itr'+str(itr)+'.txt')
        bits.setdefault(irframe[6:-13], []).append(str(bpp)+'\n')

    for b in bits:
        tf = open('rd/bits_'+b+'_itr'+str(itr)+'.txt', 'w')
        tf.writelines(bits[b])
        tf.close()
