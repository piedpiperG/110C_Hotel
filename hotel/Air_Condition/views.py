from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

# def monitor_init(request):
#     return render(request, 'monitor.html')


from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.shortcuts import render
from Air_Condition.models import Scheduler, Room, StatisticController
import numpy as np
import datetime
from hotel.consumers import RoomsInfo, RoomBuffer

scheduler = Scheduler()  # 属于model模块
sc = StatisticController
room_b = RoomBuffer


# ============================管理员=============================
def init(request):
    return render(request, 'init.html')


def init_submit(request):
    request.encoding = 'utf-8'
    high = int(request.GET['high'])
    low = int(request.GET['low'])
    default = int(request.GET['default'])
    fee_h = float(request.GET['fee_h'])
    fee_m = float(request.GET['fee_m'])
    fee_l = float(request.GET['fee_l'])
    for i in range(1, 6):
        room_b.init_temp[i] = int(request.GET['r' + str(i)])

    print(room_b.init_temp)
    scheduler.set_para(high, low, default, fee_h, fee_l, fee_m)
    scheduler.power_on()
    scheduler.start_up()
    return HttpResponseRedirect('/monitor')


def monitor(request):
    rooms = scheduler.check_room_state()
    print(rooms)
    return render(request, 'monitor.html', RoomsInfo(rooms).dic)


def tst(request):
    dic = {
        "room_id": 1,
        "state": "挂起",
        "fan_speed": "高速",
        "current_temp": 28,
        "fee": 2,
        "target_temp": 25,
        "fee_rate": 0.5
    }
    return render(request, 'monitor.html')


# ===============================前台==============================
def reception_init(request):
    return render(request, 'reception.html')


def reception(request):
    request.encoding = 'utf-8'
    room_id = request.GET['room_id']
    begin_date = request.GET['begin_date']
    end_date = request.GET['end_date']
    type = request.GET['type']
    if type == "rdr":
        # 打印详单
        # sc.print_rdr(room_id, begin_date, end_date)
        # return HttpResponseRedirect('/reception_init/')
        # 首先先生成详单
        StatisticController.print_rdr(room_id, begin_date, end_date)

        # 获取详单，返回生成的文件
        from django.http import FileResponse
        file = open('./result/detailed_list.csv', 'rb')
        response = FileResponse(file)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="detailed_list.csv"'
        return response
    else:
        # # 打印账单
        # sc.print_bill(room_id, begin_date, end_date)
        # return HttpResponseRedirect('/reception_init/')
        """打印账单"""

        # 首先先生成账单
        StatisticController.print_bill(room_id, begin_date, end_date)

        # 获取账单，返回生成的文件
        from django.http import FileResponse
        file = open('./result/bill.csv', 'rb')
        response = FileResponse(file)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="bill.csv"'
        return response


# =========================经理==========================
def manager(request):
    return render(request, "report.html")


def manager_month(request):
    month = request.GET["month"]  # 字符串，格式2020-06
    year = month.split('-')[0]
    month = month.split('-')[1]
    # *****************打印月报表**********************
    # return HttpResponseRedirect('/manager/')

    """打印月报"""
    StatisticController.draw_report(-1, 1, year, month)

    # 获取月报，返回生成的文件
    from django.http import FileResponse
    file = open('./result/report.png', 'rb')
    response = FileResponse(file)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="month.png"'
    return response


def manager_week(request):
    week = request.GET["week"]  # 字符串，格式2020-W24
    #
    # # *****************打印周报表**********************
    # return HttpResponseRedirect('/manager/')
    """打印周报"""
    year = week.split('-')[0]
    week = week.split('W')[1]
    print(year)
    print(week)
    # 首先先生成周报
    StatisticController.draw_report(-1, 2, year, week)

    # 获取周报，返回生成的文件
    from django.http import FileResponse
    file = open('./result/report.png', 'rb')
    response = FileResponse(file)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="week.png"'
    return response


def report_printer(request):
    room_id = request.GET['room_id']
    year = request.GET['year']
    month = request.GET['month']
    week = request.GET['week']

    if request.GET['type'] == "月报":
        """打印月报"""

        # 首先先生成月报
        StatisticController.print_report(room_id, 1, year, month)

        # 获取月报，返回生成的文件
        from django.http import FileResponse
        file = open('./result/report.csv', 'rb')
        response = FileResponse(file)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="month_report.csv"'
        return response
    else:
        """打印周报"""

        # 首先先生成周报
        StatisticController.print_report(room_id, 2, year, week)

        # 获取周报，返回生成的文件
        from django.http import FileResponse
        file = open('./result/report.csv', 'rb')
        response = FileResponse(file)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="week_report.csv"'
        return response
