import hashlib

import time
from django.shortcuts import render,HttpResponse
import json
from repository import models

from django.conf import settings

key_record = {
    # "3f090e8ea65e84297b4f724401c82b39|1545121938.720341" : 1545121948.720341
}

def decrypt(msg):
    from Crypto.Cipher import AES
    key = b'dfdsdfsasdfdsdfs'
    cipher = AES.new(key, AES.MODE_CBC, key)
    result = cipher.decrypt(msg) # result = b'\xe8\xa6\x81\xe5\x8a\xa0\xe5\xaf\x86\xe5\x8a\xa0\xe5\xaf\x86\xe5\x8a\xa0sdfsd\t\t\t\t\t\t\t\t\t'
    data = result[0:-result[-1]]
    return str(data,encoding='utf-8')

def asset(request):

    if request.method == 'GET':
        token = settings.TOKEN


        # 第三种方式：也是发送一个令牌，但是判断时间，并且把访问过的令牌放入到一个列表中
        client_key, client_ctime = request.META.get('HTTP_TOKEN').split('|')
        client_ctime = float(client_ctime)

        server_ctime = time.time()

        if server_ctime - client_ctime > 100000:
            return HttpResponse('【第一关】超时了')

        tmp = "%s|%s" % (token, client_ctime)
        m = hashlib.md5()
        m.update(bytes(tmp, encoding='utf-8'))
        server_key = m.hexdigest()

        if server_key != client_key:
            return HttpResponse('【第二关】动态令牌验证错误')

        for k in list(key_record.keys()):
            value = key_record[k]
            if server_ctime > value:
                del key_record[k]


        if client_key in key_record:
            return HttpResponse('[第三关] 该令牌已经被别人使用过了')
        else:
            key_record[client_key] = client_ctime + 100000

        return HttpResponse('非常重要的数据...')

    elif request.method == 'POST':

        info = decrypt(request.body)

        server_info = json.loads(info)


        hostname = server_info['basic']['data']['hostname']

        server_obj = models.Server.objects.filter(hostname=hostname).first()


        if not server_obj:
            return HttpResponse('当前主机名未录入')

        if not server_info['disk']['status']:
            models.ErrorLog.objects.create(asset_obj=server_obj.asset, content=server_info['disk']['data'],title="[%s]硬盘采集错误信息"%hostname)

        '''
        处理：
            新的资产：
                {'0': {'slot': '0', 'pd_type': 'SAS', 'capacity': '279.396', 'model': 'SEAGATE ST300MM0006     LS08S0K2B5NV'}, 
                '1': {'slot': '1', 'pd_type': 'SAS', 'capacity': '279.396', 'model': 'SEAGATE ST300MM0006     LS08S0K2B5AH'}, 
                '2': {'slot': '2', 'pd_type': 'SATA', 'capacity': '476.939', 'model': 'S1SZNSAFA01085L     Samsung SSD 850 PRO 512GB               EXM01B6Q'},
                '3': {'slot': '3', 'pd_type': 'SATA', 'capacity': '476.939', 'model': 'S1AXNSAF912433K     Samsung SSD 840 PRO Series              DXM06B0Q'}, 
                '4': {'slot': '4', 'pd_type': 'SATA', 'capacity': '476.939', 'model': 'S1AXNSAF303909M     Samsung SSD 840 PRO Series              DXM05B0Q'}, 
                '5': {'slot': '5', 'pd_type': 'SATA', 'capacity': '476.939', 'model': 'S1AXNSAFB00549A     Samsung SSD 840 PRO Series              DXM06B0Q'}}
                }
        '''
        new_disk_list = server_info['disk']['data']

        '''
            旧的资产：
                [
                    Disk('slot':5, 'pd_type':'SAS')
                    Disk('slot':3, 'pd_type':'SAS')
                ]
        '''
        old_disk_list = server_obj.disk.all()

        '''
            新老资产进行比较：
                新：{5,4,3} 
                老：[5,4,1]
        '''
        # 新的槽位列表
        new_slot_list = list(new_disk_list.keys())

        # 旧的槽位列表
        old_slot_list = []
        for item in old_disk_list:
            old_slot_list.append(item.slot)

        '''
            1. 删除（差集）：[1,]
            2. 增加 （差集）：[3,]
            3. 更新 （交集）：[5,4]
        '''

        # 1. 增加 (差集)
        add_list = set(new_slot_list).difference(old_slot_list)

        # 存入数据库表disk
        if add_list:
            disk_res = {}
            record_list = []
            for slot in add_list:
                disk_res = new_disk_list[slot]
                disk_res['server_obj'] = server_obj

                models.Disk.objects.create(**disk_res)

                tmp = "新增硬盘：槽位{slot} 容量{capacity} 型号{model} 类型{pd_type}".format(**disk_res)
                record_list.append(tmp)

            content = ",".join(record_list)
            models.AssetRecord.objects.create(asset_obj = server_obj.asset, content = content)


        # 2. 删除 （差集）
        del_list = set(old_slot_list).difference(new_slot_list)

        # 从表disk删除不存在的数据
        if del_list:
            models.Disk.objects.filter(slot__in=del_list, server_obj=server_obj).delete()
            # 记录日志
            models.AssetRecord.objects.create(asset_obj=server_obj.asset, content='删除硬盘:%s' % (",".join(del_list)))


        # 3. 更新（交集）
        update_list = set(old_slot_list).intersection(new_slot_list)
        print(update_list)

        record_list = []
        row_map = {'capacity':'容量', 'pd_type':'类型', 'model':'型号'}
        if update_list:

            for slot in update_list:
                # 新的数据，是一个字典
                new_disk_row = new_disk_list[slot]
                # 数据库中的数据
                old_disk_row = models.Disk.objects.filter(slot=slot, server_obj=server_obj).first()

                for k, new_v in new_disk_row.items():
                    # k: capacity;slot;pd_type;model
                    # v: '476.939''xxies              DXM05B0Q''SATA'
                    old_v = getattr(old_disk_row, k)

                    if new_v != old_v:
                        setattr(old_disk_row, k, new_v)
                        record_list.append("槽位%s, %s由%s变为%s" % (slot, row_map[k], old_v, new_v,))
                old_disk_row.save()

            if record_list:
                models.AssetRecord.objects.create(asset_obj = server_obj.asset, content=";".join(record_list))


    return HttpResponse('.....')