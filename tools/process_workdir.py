import glob
import shutil
import os

workdir = r'/project/train/src_repo/yolov5/runs'
model_path = r'/project/train/models'
log_path = r'/project/train/log'
graph_path = r'/project/train/result-graphs'

for i in (model_path, log_path, graph_path):
    if not os.path.exists(i):
        os.makedirs(i)

exp = os.listdir(workdir)[0]
print('final exp: {}'.format(exp))

exp_path = os.path.join(workdir, exp)

for file in os.listdir(os.path.join(exp_path, 'weights')):
    if file.endswith('.pt'):
        model_name = file.split('.')[0]
        if model_name != 'last':
            if not os.path.exists(os.path.join(model_path, model_name)):
                os.makedirs(os.path.join(model_path, model_name))
            shutil.copy(os.path.join(exp_path, 'weights', file), os.path.join(model_path, model_name, file))
        else:
            if not os.path.exists(os.path.join(model_path, 'final')):
                os.makedirs(os.path.join(model_path, 'final'))
            shutil.copy(os.path.join(exp_path, 'weights', file), os.path.join(model_path, 'final', file))

for file in os.listdir(exp_path):
    if file.endswith('jpg') or file.endswith('png'):
        shutil.copy(os.path.join(exp_path, file), os.path.join(graph_path, file))
    elif file.endswith('txt'):
        shutil.copy(os.path.join(exp_path, file), os.path.join(log_path, 'log.txt'))
    elif file.endswith('yaml'):
        for d in os.listdir(model_path):
            shutil.copy(os.path.join(exp_path, file), os.path.join(model_path, d, file))
    else:
        pass
