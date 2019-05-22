import numpy as np
import os, fcntl
from django.http import HttpResponse
from django.shortcuts import render
from projects.models import Scatter


def index(request):
    return render(request, 'projects/index.html')


def put_order(order, path='./'):
    p = path + "/order/"
    po = p + 'order.txt'
    pt = p + 'todo.txt'
    if not os.path.exists(p):
        os.makedirs(p)
    old_order = set()
    if os.path.exists(po):
        with open(p + 'order.txt') as f:
            for line in f:
                old_order.add(line[:-1])
    if os.path.exists(pt):
        with open(p + 'todo.txt') as f:
            for line in f:
                old_order.add(line[:-1])
    print(old_order)
    with open(po, 'a') as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        for i in order:
            if not i in old_order:
                f.write(i + '\n')
        fcntl.flock(f, fcntl.LOCK_UN)


def first(request):
    cc = ['#e6194b', '#3cb44b', '#ffe119', '#4363d8', '#f58231', '#911eb4', '#46f0f0', '#f032e6', '#bcf60c', '#fabebe',
          '#008080', '#e6beff', '#9a6324', '#fffac8', '#800000', '#aaffc3', '#808000', '#ffd8b1', '#000075', '#808080']
    category = {'cup': 7, 'ant': 3, 'human': 2, 'airplane': 6, 'armdino': 1, 'teddy': 9, 'glasses': 10,
                'fish': 12, 'fourleg': 14, 'octopus': 8, 'bird': 11, 'plier': 13, 'chair': 15, 'hand': 5, 'table': 4}

    color = dict()
    for k in category:
        color[k] = cc[category[k]]
    feature = ['Top20combinations', 'agd', 'area', 'cf', 'geobase', 'mytanhgaussian', 'normalsangle', 'sdfval']
    aim = ['UMAP', "TSNE"]
    version = 0
    path = "/home/first/code/data/seg_bench/results/"
    message1 = ""
    message2 = ""
    pictures = []
    check = False
    if request.POST:
        check = True
        if not request.POST.__contains__('category'):
            message1 = "at lest choose one"
            check = False
        if not request.POST.__contains__('feature'):
            message2 = "at lest choose one"
            check = False
    q = dict(request.POST.lists())
    print(q, check)
    if check:
        id = 0
        for c in q['category']:
            id += 1 << (category[c] - 1)
        order = []
        str = id.__str__()
        if (feature[0] in q['feature']):
            str += "_" + feature[0]
            name = str
            destination = dict()
            dest_ready = False
            try:
                result = Scatter.objects.get(name=name, version=version, path=path)
            except (KeyError, Scatter.DoesNotExist):
                p = path + name + "_TOP" + '.txt'
                if os.path.exists(p):
                    f = open(p)
                    destination = eval(f.read())
                    f.close()
                    dest_ready = True
                    scat = Scatter(name=name, version=version, path=path, dict=destination.__str__())
                    scat.save()
                else:
                    order.append(path + " " + name + " " + "TOP")
            else:
                destination = eval(result.dict)
                dest_ready = True
            if dest_ready:
                for i in range(20):
                    pic_key = "UMAP_{}".format(i)
                    if pic_key in destination:
                        p = destination[pic_key][:-4] + ".npz"
                        temp_data = np.load(p)
                        temp_data.title_data = "data:" + ",".join(q['category'])
                        temp_data.title_features = "feature:" + ','.join(temp_data['comb'])
                        temp_data.title_nh = "NH:{}".format(temp_data['nh'].mean())
                        temp_data.title_method = "{}".format("UMAP")
                        pictures.append(temp_data)
                        pic_key = "TSNE_{}".format(i)
                        p = destination[pic_key][:-4] + ".npz"
                        temp_data = np.load(p)
                        temp_data.title_data = "data:" + ",".join(q['category'])
                        temp_data.title_features = "feature:" + ','.join(temp_data['comb'])
                        temp_data.title_nh = "NH:{}".format(temp_data['nh'].mean())
                        temp_data.title_method = "{}".format("TSNE")
                        pictures.append(temp_data)
                    else:
                        break

        else:
            for s in q['feature']:
                str += "_" + s
            name = str
            try:
                result = Scatter.objects.get(name=name, version=version, path=path)
            except (KeyError, Scatter.DoesNotExist):
                destination = dict()
                noone = True
                for a in aim:
                    p = path + name + "_" + a + '.'+ 'npz'
                    if os.path.exists(p):
                        noone = False
                        temp_data = np.load(p)
                        temp_data.title_data = "DATA: " + ",".join(q['category'])
                        temp_data.title_features = "FEATURES: " + ','.join(temp_data['comb'])
                        temp_data.title_nh = "NH: {}".format(temp_data['nh'].mean())
                        temp_data.title_method = "{}".format(a)
                        pictures.append(temp_data)
                        destination[a] = p
                    else:
                        order.append(path + " " + name + " " + a)
                if not noone:
                    scat = Scatter(name=name, version=version, path=path, dict=destination.__str__())
                    scat.save()
            else:
                destination = eval(result.dict)
                update = False
                for a in aim:
                    if a in destination:
                        p = destination[a][:-4] + '.npz'
                    else:
                        p = path + name + "_" + a + '.'+ 'npz'
                        if os.path.exists(p):
                            update = True
                    if os.path.exists(p):
                        temp_data = np.load(p)
                        temp_data.title_data = "data:" + ",".join(q['category'])
                        temp_data.title_features = "feature:" + ','.join(temp_data['comb'])
                        temp_data.title_nh = "NH:{}".format(temp_data['nh'].mean())
                        temp_data.title_method = "{}".format(a)
                        pictures.append(temp_data)
                        destination[a] = p
                    else:
                        order.append(path + " " + name + " " + a)
                if update:
                    result.dict=destination.__str__()
                    result.save()
        if len(order):
            put_order(order, path)
    for pic in pictures:
        pic.width = 400
        pic.height = 400
        x_min = pic['x'].min()
        x_max = pic['x'].max()
        x_width = x_max - x_min

        y_min = pic['y'].min()
        y_max = pic['y'].max()
        y_height = y_max - y_min
        pic.point = []
        for i in range(len(pic['x'])):
            px = (pic['x'][i] - x_min) / x_width * pic.width * 0.9 + pic.width * 0.05
            py = (pic['y'][i] - y_min) / y_height * pic.height * 0.9 + pic.height * 0.05
            pic.point.append((px, py, pic['c'][i], pic['nhc'][i]))

    return render(request, 'projects/first.html', locals())

