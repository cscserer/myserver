import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'try.settings'


import django

django.setup()
from polls.models import Question, Choice


import sys
sys.path.append("/home/first/code/py/HelloMesh")
from FeatureRepo import *

from projects.models import Mesh, Feature, Statistics

def load_from_path(path = ""):
    data = FeatureRepo()
    data.set_path(path)
    data.load_for_django_model()
    for m in data.meshes:
        f = Feature(agd=m.django_keys['agd'],
                    cf=m.django_keys['cf'],
                    mytanhgaussian=m.django_keys['mytanhgaussian'],
                    geobase=m.django_keys['geobase'],
                    normalsangle=m.django_keys['normalsangle'],
                    sdfval=m.django_keys['sdfval'],
                    area=m.django_keys['area'],
                    version=m.django_keys['f_version'])
        f.save()
        s = Statistics(total_vertices=m.django_keys['total_vertices'],
                    total_faces=m.django_keys['total_faces'],
                    total_area=m.django_keys['total_area'],
                    min_area=m.django_keys['min_area'],
                    max_area=m.django_keys['max_area'],
                    mean_area=m.django_keys['mean_area'],
                    std_area=m.django_keys['std_area'],
                    var_area=m.django_keys['var_area'],
                    version=m.django_keys['s_version'])
        s.save()
        m = Mesh(feature=f,
                 statistics=s,
                 path=m.id.path,
                 dir=m.id.dir,
                 kind=m.id.kind,
                 name=m.id.name,
                 suffix=m.id.suffix,
                 version=m.django_keys['m_version'])
        m.save()



if __name__ == '__main__':
    load_from_path('/home/first/code/data/seg_bench/')