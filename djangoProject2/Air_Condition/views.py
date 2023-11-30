import json

from django.shortcuts import render
from django.http import JsonResponse


# Create your views here.

def guest_init(request):
    return render(request, 'customer.html')

def guest2_init(request):
    return render(request, 'customer_2.html')

def guest3_init(request):
    return render(request, 'customer_3.html')

def guest4_init(request):
    return render(request, 'customer_4.html')

def guest5_init(request):
    return render(request, 'customer_5.html')

def increase_temperature(request):
    # 在这里处理升温的逻辑
    # 您可以获取当前温度、增加温度，然后将新温度返回给前端
    current_temperature = 16  # 例如，这里是当前温度
    new_temperature = current_temperature + 1  # 增加温度
    response_data = {'new_temperature': new_temperature}
    return JsonResponse(response_data)


def click_data(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)


            # 在这里执行更新温度的操作，例如将数据写入文件
            with open('data_files/temperature_data.txt', 'w') as file:
                file.write(str(data))
            response_data = {'message': '温度已更新'}
            return JsonResponse(response_data)
        except json.JSONDecodeError:
            return JsonResponse({'error': '无效的JSON数据'}, status=400)

    return JsonResponse({'error': '仅支持POST请求'}, status=405)
