from django.shortcuts import render, HttpResponse

# Create your views here.
from repository import models
from django.core import serializers
from datetime import datetime
from datetime import date
import json,time
from django.conf import settings,global_settings


class JsonCustomEncoder(json.JSONEncoder):

    def default(self, value):
        if isinstance(value, datetime):
            return value.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(value, date):
            return value.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, value)

def server(request):
    print(global_settings.EMAIL_HOST)
    print(global_settings.TEMPLATES)
    return render(request, 'server-bs.html')


def ajax_server(request):

    fields = get_config(request, 'servers', True)

    server_list = models.Server.objects.values(*fields)
    total = models.Server.objects.values(*fields).count()
    print(server_list)

    ret = {
        'total': total,
        'rows': list(server_list),
    }

    return HttpResponse(json.dumps(ret, cls=JsonCustomEncoder))



def asset(request):

    return render(request, 'asset.html')

def ajax_asset(request):
    print(request.POST)
    print(request.body)

    fields = get_config(request, 'asset', True)

    asset_list = models.Asset.objects.values(*fields)

    total = models.Asset.objects.values(*fields).count()
    # print(asset_list)

    ret = {
        'total': total,
        'rows': list(asset_list),
    }

    return HttpResponse(json.dumps(ret, cls=JsonCustomEncoder))


def modify(request):

    action = request.POST.get('action')
    table  = request.GET.get('table')

    if action == 'edit':
        data = request.POST.get('postdata')
        import json
        data = json.loads(data)
        print('update', data)

        if data.get('device_status_id'):
            device_status = models.Asset.device_status_choices
            print(device_status)
            for v in device_status:
                if v[1] == data['device_status_id'] :
                    data['device_status_id'] = v[0]
                    break

        if data.get('device_type_id'):
            device_type = models.Asset.device_type_choices
            print(device_type)

        if data.get('idc__name'):
            idc_info = get_idc(request, flag=True)
            print((idc_info))

            for v in idc_info:

                if v['name'] == data['idc__name']:
                    data['idc_id'] = v['id']
                    break

            del data['idc__name']

        print('更新的数据是：',data)


        # res = models.Server.objects.filter(id=data['id']).update(asset_id=2)
        return HttpResponse('ok')

    if action == 'del':
        ids = request.POST.getlist('ids')
        print('要删除的id是：',ids)
        # models.Server.objects.filter(id__in=ids).delete()

        return HttpResponse('ok')



def get_config(request, tablename=None, flag=False):

    config = \
        {
            "servers":[
                {"field": "id", "title": 'id'},
                {"field": "hostname", "title": '主机名', 'editable': True},
                {"field": "sn", "title": 'SN号', 'editable': True}
            ],
            "idc": [
                {"field": "id", "title": 'id'},
                {
                    "field": "name",
                    "title": '机房名',
                    'editable': {
                        "type": 'select',
                        "title": '机房名',
                        "source": [],
                    }
                },
                {"field": "floor", "title": '楼层', 'editable': True}
            ],
            "asset":[
                {"field": "id", "title": 'id'},
                {
                    "field": "device_type_id",
                    "title": '资产类型',
                    'editable': {
                        "type": 'select',
                        "title": '资产类型',
                        "source":[],
                    },
                    "formatter":"device_type",
                    "device_type": models.Asset.device_type_choices
                },
                {
                    "field": "device_status_id",
                    "title": '资产状态',
                    'editable': {
                        "type": 'select',
                        "title": '资产状态',
                        "source": [],
                    },
                    "formatter":'device_status',
                    "device_status": models.Asset.device_status_choices
                },
                {"field": "cabinet_num", "title": '机柜号', 'editable': True},
                {"field": "cabinet_order", "title": '机柜序号', 'editable': True},
                {
                    "field": "idc__name",
                    "title": 'idc机房',
                    'editable': {
                        "type": 'select',
                        "title": 'idc机房',
                        "source": None,
                    },
                },
                {
                    "field": None,
                    "asset_search": [
                        {"name": 'cabinet_num', 'text': '机柜号', 'search_type': 'input'},
                        {"name": 'device_type_id', 'text': '资产类型', 'search_type': 'select', 'global_name': 'device_type_lists'},
                        {"name": 'device_status_id', 'text': '资产状态', 'search_type': 'select','global_name': 'device_status_lists'},
                    ]
                }
            ],

        }

    fields = []

    if not flag:
        return HttpResponse(json.dumps(config[request.POST.get('tablename')]))
    else:
        for row in config[tablename]:
            if row.get('field'):
                fields.append(row['field'])
        return fields

def get_product_line(request):

    res = models.BusinessUnit.objects.values('id','name').all()
    print(list(res))

    data = json.dumps(list(res), cls=JsonCustomEncoder)
    return HttpResponse(data)

def get_idc(request, flag=False):

    res = models.IDC.objects.values('id','name','floor').all()

    if not flag:
        data = json.dumps(list(res), cls=JsonCustomEncoder)
        return HttpResponse(data)
    else:
        return list(res)

def idc(request):

    return render(request, 'idc.html')


