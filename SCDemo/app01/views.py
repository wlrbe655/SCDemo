import os
import string
import traceback
import uuid
from datetime import datetime, timezone
import random
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
import json
from pyexpat.errors import messages
from django.db import transaction
from .models import goods, Stu, admin, order, job
from .utils.bootstrapModelForm import bootstrapModelForm
from django import forms
from .utils.code import check_code
from io import BytesIO
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.core.cache import cache
# Create your views here.





def generate_random_id(length=6):
    """生成一个指定长度的随机数字字符串"""
    return ''.join(random.choices(string.digits, k=length))


class UploadlistModelForm(bootstrapModelForm):
    bootstrap_exclude_fields = ["img"]
    class Meta:
        model = goods
        fields = '__all__'



class registerModelForm(bootstrapModelForm):
    class Meta:
        model = Stu  # 你要使用哪个表生成输入框
        fields = ['id','name','tel','qsld','password']

    code = forms.CharField(
        label="验证码",
        widget=forms.TextInput(attrs={"class": "form-control"})
    )




class UpModelForm(bootstrapModelForm):
    bootstrap_exclude_fields = ["img"]
    class Meta:
        model = admin
        fields = '__all__'



class UpjobModelForm(bootstrapModelForm):
    class Meta:
        model = job
        fields = ['name','tel']


class addjobModelForm(bootstrapModelForm):
    class Meta:
        model = job
        fields = ['name', 'tel']


class orderModelForm(bootstrapModelForm):
    class Meta:
        model = order
        fields = '__all__'


class jobModelForm(bootstrapModelForm):
    class Meta:
        model = job
        fields = '__all__'




class LoginModelForm(bootstrapModelForm):
    # 向数据库中新加一个字段,但是并不会真的存在在数据库中
    code = forms.CharField(
        label="验证码",
        widget=forms.TextInput(attrs={"class": "form-control"})
    )

    class Meta:
        model = Stu
        fields = ['tel', 'password']







def xcc_list(request):
    search_query = request.GET.get('search', '')
    cache_key = f"xcc_list_{search_query}"
    xcc = cache.get(cache_key)
    if xcc is None:
        if search_query:
            xcc = list(goods.objects.filter(Q(name__icontains=search_query) | Q(category__icontains=search_query)))
        else:
            xcc = list(goods.objects.all())
        cache.set(cache_key, xcc, 60)
    return render(request, 'xcc_list.html', {'xcc': xcc})


def sc_list(request):
    cache_key = "sc_list_all"
    sc = cache.get(cache_key)
    if sc is None:
        sc = list(goods.objects.all())
        cache.set(cache_key, sc, 60)
    return render(request, "sc_list.html", {"sc": sc})



def sc_add(request):
    upload = goods.objects.all()
    if request.method == "GET":
        form = UploadlistModelForm()
        return render(request, "sc_add.html", {'form': form, 'upload': upload})
    else:
        form = UploadlistModelForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            cache.delete("sc_list_all")  # ✅ 清除缓存
            cache.delete("xcc_list_")
    return redirect("/sc/list")


def sc_edit(request):
    nid = request.GET.get("nid")
    update = goods.objects.filter(id=nid).first()
    if request.method == "GET":
        form = UploadlistModelForm(instance=update)
        return render(request, "sc_edit.html", {'form': form})
    else:
        # 保存旧图片路径，以便后续删除
        old_img_path = None
        if update and update.img:
            old_img_path = update.img.path

        form = UploadlistModelForm(request.POST, request.FILES, instance=update)
        if form.is_valid():
            # 如果上传了新图片，则删除旧图片
            if 'img' in request.FILES and old_img_path:
                import os
                if os.path.exists(old_img_path):
                    os.remove(old_img_path)
            # 如果用户选择清除图片但没有上传新图片
            elif 'img-clear' in request.POST and old_img_path:
                import os
                if os.path.exists(old_img_path):
                    os.remove(old_img_path)
                update.img = None

            # 保存表单数据（包括新图片）
            form.save()

            # 清除缓存
            cache.delete("sc_list_all")
            cache.delete("xcc_list")

            return redirect("/sc/list")
        else:
            return render(request, "sc_edit.html", {'form': form})



def sc_delete(request):
    nid = request.GET.get("nid")
    # 先获取商品对象以便访问图片路径
    good = goods.objects.filter(id=nid).first()
    if good and good.img:
        # 删除关联的图片文件
        import os
        if os.path.exists(good.img.path):
            os.remove(good.img.path)

    goods.objects.filter(id=nid).delete()
    cache.delete("sc_list_all")
    cache.delete("xcc_list")
    return redirect("/sc/list")





def image_code(request):
    """生成随机图片验证码"""
    img,code_string = check_code()
    request.session["image_code"] = code_string
    request.session.set_expiry(60)
    stream = BytesIO()
    img.save(stream, 'png')
    return HttpResponse(stream.getvalue())



def sc_login(request):
    if request.method == "GET":
        form = LoginModelForm()
        return render(request, "login.html", {'form': form})
    else:
        form = LoginModelForm(request.POST)
        if form.is_valid():
            tel = form.cleaned_data.get("tel")
            password = form.cleaned_data.get("password")
            user_input_code = form.cleaned_data.pop("code")
            code = request.session.get("image_code")

            # 验证码验证
            if code.upper() != user_input_code.upper():
                form.add_error("code", "验证码错误")
                return render(request, "login.html", {"form": form})

            # 查询普通用户
            stu_row_data = Stu.objects.filter(tel=tel, password=password).first()

            # 查询管理员用户
            admin_row_data = admin.objects.filter(tel=tel, password=password).first()

            if stu_row_data:
                # 普通用户登录成功
                request.session["info"] = {'id': stu_row_data.id, 'name': stu_row_data.name, 'role': 'user'}
                request.session.set_expiry(60 * 60 * 24 * 7)
                request.session.modified = True  # 添加这行，标记会话已修改
                return redirect("/xcc/list")  # 重定向到普通用户页面
            elif admin_row_data:
                # 管理员登录成功
                request.session["info"] = {'id': admin_row_data.id, 'name': admin_row_data.username, 'role': 'admin'}
                request.session.set_expiry(60 * 60 * 24 * 7)
                request.session.modified = True  # 添加这行，标记会话已修改
                return redirect("/sc/list")  # 重定向到管理员页面
            else:
                # 登录失败
                form.add_error("password", "账号或密码错误")
                return render(request, "login.html", {'form': form})
        else:
            print(form.errors)
            return render(request, "login.html", {"form": form})

# def sc_login(request):
#     if request.method == "GET":
#         form = LoginModelForm()
#         return render(request, "login.html", {'form': form})
#     else:
#         form = LoginModelForm(request.POST)
#         if form.is_valid():
#             tel = form.cleaned_data.get("tel")
#             password = form.cleaned_data.get("password")
#             user_input_code = form.cleaned_data.pop("code")
#             code = request.session.get("image_code")
#
#             # 验证码验证
#             if code.upper() != user_input_code.upper():
#                 form.add_error("code", "验证码错误")
#                 return render(request, "login.html", {"form": form})
#
#             # 查询普通用户
#             stu_row_data = Stu.objects.filter(tel=tel, password=password).first()
#
#             # 查询管理员用户
#             admin_row_data = admin.objects.filter(tel=tel, password=password).first()
#
#             if stu_row_data:
#                 # 普通用户登录成功
#                 request.session["info"] = {'id': stu_row_data.id, 'name': stu_row_data.name, 'role': 'user'}
#                 request.session.set_expiry(60 * 60 * 24 * 7)
#                 return redirect("/xcc/list")  # 重定向到普通用户页面
#             elif admin_row_data:
#                 # 管理员登录成功
#                 request.session["info"] = {'id': admin_row_data.id, 'name': admin_row_data.username, 'role': 'admin'}
#                 request.session.set_expiry(60 * 60 * 24 * 7)
#                 return redirect("/sc/list")  # 重定向到管理员页面
#             else:
#                 # 登录失败
#                 form.add_error("password", "账号或密码错误")
#                 return render(request, "login.html", {'form': form})
#         else:
#             print(form.errors)
#             return render(request, "login.html", {"form": form})


def register(request):
    if request.method == "GET":
        form = registerModelForm()
        return render(request, "register.html", {'form': form})
    else:
        form = registerModelForm(request.POST)
        if form.is_valid():
            user_input_code = form.cleaned_data.pop("code")
            code = request.session.get("image_code")
            if code.upper() != user_input_code.upper():
                form.add_error("code", "验证码错误")
                return render(request, "register.html", {"form": form})
            id = form.cleaned_data['id']
            name = form.cleaned_data['name']
            tel = form.cleaned_data['tel']
            qsld = form.cleaned_data['qsld']
            password = form.cleaned_data['password']
            Stu.objects.create(id=form.cleaned_data['id'],
                               name=form.cleaned_data['name'],
                               tel=form.cleaned_data['tel'],
                               qsld=form.cleaned_data['qsld'],
                               password=form.cleaned_data['password'],
                               datetime=datetime.now().replace(microsecond=0),
                               )
            request.session["info"] = {'id': id, 'name': name, 'role': 'user'}
            request.session.set_expiry(60 * 60 * 24 * 7)  # 设置会话超时时间为7天
            return redirect("/xcc/list")
        else:
            return render(request, "register.html", {"form": form})





def user_logout(request):
    # 清除用户的登录状态
    logout(request)
    # 重定向到登录页面或其他页面
    return redirect('/xcc/list')


def user_list(request):
    cache_key = "user_list_all"
    user = cache.get(cache_key)
    if user is None:
        user = list(Stu.objects.all())
        cache.set(cache_key, user, 120)
    return render(request, "user_list.html", {"user": user})

def admin_list(request):
    cache_key = "admin_list_all"
    adm = cache.get(cache_key)
    if adm is None:
        adm = list(admin.objects.all())
        cache.set(cache_key, adm, 180)
    return render(request, 'admin_list.html', {"adm": adm})


def admin_add(request):
    upload = admin.objects.all()
    if request.method == "GET":
        form = UpModelForm()
        return render(request,"admin_add.html",{'form':form,'upload':upload})
    else:
        form = UpModelForm(data=request.POST,files=request.FILES)
        if form.is_valid():
            form.save()
    return redirect("/admin/list",{"form":form,"upload":upload})


def admin_edit(request):
    nid = request.GET.get("nid")
    update = admin.objects.filter(id=nid).first()
    if request.method == "GET":
        form = UpModelForm(instance=update)
        return render(request, "admin_edit.html", {'form':form,})
    else:
        form = UpModelForm(request.POST,instance=update)
        if form.is_valid():
            form.save()
            return redirect("/admin/list")
        else:
            return render(request, "admin_edit.html", {'form':form})



def admin_delete(request):
    nid = request.GET.get("nid")
    admin.objects.filter(id=nid).delete()
    return redirect("/admin/list")



def cart(request):
    if request.method == "GET":
        return render(request, "cart.html",)
    else:
        return redirect('/pay/')



def pay(request):
    if request.method == "GET":
        user_info = request.session.get("info")
        user_id = user_info.get('id')
        # 只获取当前登录用户的未支付订单
        form = order.objects.filter(stuID_id=user_id, is_paid=False)
        return render(request, "pay.html", {'form': form})
    else:
        return redirect('/pay/')



def pay_is(request):
    if request.method == "POST":
        user_info = request.session.get("info")
        if not user_info:
            return JsonResponse({'status': 'error', 'message': '用户未登录'})

        user_id = user_info.get('id')
        # 获取当前登录用户的未支付订单
        orders = order.objects.filter(stuID_id=user_id, is_paid=False)
        if not orders:
            return JsonResponse({'status': 'error', 'message': '没有未支付的订单'})

        # 更新订单状态为已支付
        for item in orders:
            item.is_paid = True
            item.save()

        return JsonResponse({'status': 'success', 'message': '支付成功'})
    else:
        return JsonResponse({'status': 'error', 'message': '无效的请求方法'})


@csrf_exempt
def checkout(request):
    if request.method == "POST":
        try:
            # 获取当前登录用户的信息
            user_info = request.session.get("info")
            if not user_info:
                return JsonResponse({'status': 'error', 'message': '用户未登录'})

            user_id = user_info.get('id')
            try:
                user = Stu.objects.get(id=user_id)
            except Stu.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': '用户不存在'})

            # 修复 JSON 解析
            # 从请求体中获取原始字节数据并解码为字符串
            body_data = request.body.decode('utf-8')
            cart_data = json.loads(body_data)

            # 计算总计金额
            total_money = sum(item['price'] * item['quantity'] for item in cart_data)

            # 创建订单
            with transaction.atomic():
                # 将购物车数据转换为商品信息字符串
                goods_details = ', '.join(
                    [f"{item['name']} x{item['quantity']}" for item in cart_data]
                )
                order_id = generate_random_id()
                # 创建订单
                orders = order.objects.create(
                    id = order_id,
                    stuID=user,
                    goodsDetails=goods_details,
                    money=str(total_money),
                    createTime=datetime.now().replace(microsecond=0),
                    status=1  # 默认状态为未发货
                )

            # 返回成功响应，包含订单信息
            return JsonResponse({
                'status': 'success',
                'message': '订单创建成功',
                'order_id': orders.id,
                'total_money': str(total_money),
                'goodsDetails': goods_details,
                'redirect_url': '/pay/'  # 添加重定向URL
            })

        except Exception as e:
            # 返回错误响应
            import traceback
            traceback.print_exc()  # 打印错误堆栈以便调试
            return JsonResponse({'status': 'error', 'message': str(e)})
    else:
        return JsonResponse({'status': 'error', 'message': '无效的请求方法'})




def job_list(request):
    cache_key = "job_list_all"
    form = cache.get(cache_key)
    if form is None:
        form = list(job.objects.all())
        cache.set(cache_key, form, 180)
    return render(request, 'job_list.html', {'form': form})



def order_list(request):
    cache_key = "order_list_all"
    orders = cache.get(cache_key)
    if orders is None:
        orders = list(order.objects.all())
        cache.set(cache_key, orders, 180)
    delivery_persons = list(job.objects.all())
    return render(request, 'order_list.html', {'form': orders, 'jobs': delivery_persons})



def job_add(request):
    upload = job.objects.all()
    if request.method == "GET":
        form = addjobModelForm()
        return render(request, "job_add.html", {'form': form, 'upload': upload})
    else:
        form = addjobModelForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
    return redirect("/job/list", {"form": form, "upload": upload})




def job_edit(request):
    nid = request.GET.get("nid")
    update = job.objects.filter(id=nid).first()
    if request.method == "GET":
        form = UpjobModelForm(instance=update)
        return render(request, "job_edit.html", {'form':form,})
    else:
        form = UpjobModelForm(request.POST,instance=update)
        if form.is_valid():
            form.save()
            return redirect("/job/list")
        else:
            return render(request, "job_edit.html", {'form':form})




def job_delete(request):
    nid = request.GET.get("nid")
    job.objects.filter(id=nid).delete()
    return redirect("/job/list")



def assign_delivery(request, order_id):
    if request.method == "POST":
        user_info = request.session.get("info")
        if not user_info:
            return JsonResponse({'status': 'error', 'message': '用户未登录'})

        delivery_person_id = request.POST.get('delivery_person_id')
        print(f"Delivery Person ID: {delivery_person_id}")  # 调试信息

        if not delivery_person_id:
            return JsonResponse({'status': 'error', 'message': '请选择一个配送员'})

        try:
            delivery_person = job.objects.get(id=delivery_person_id)
            order_obj = order.objects.get(id=order_id)

            # 更新配送员的工作状态为“配送中”
            delivery_person.time = 2
            delivery_person.save()

            # 增加配送员的工作量
            workload_int = int(delivery_person.workload)  # 将 '1' 转换为 1
            workload_int += 1  # 1 + 1 = 2
            delivery_person.workload = str(workload_int)  # 将 2 转换为 '2'
            delivery_person.save()

            # 更新订单的配送员
            order_obj.delivery_person = delivery_person
            #更新配送时间
            order_obj.sendTime = datetime.now().replace(microsecond=0)
            order_obj.deliverId_id = delivery_person.id
            order_obj.status = 2
            order_obj.save()

            return JsonResponse({'status': 'success', 'message': '配送员分配成功'})
        except job.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': '配送员不存在'})
        except order.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': '订单不存在'})
    else:
        return JsonResponse({'status': 'error', 'message': '无效的请求方法'})




def user_order(request):
    if request.method == "GET":
        user_info = request.session.get("info")
        if not user_info:
            return JsonResponse({'status': 'error', 'message': '用户未登录'})
        user_id = user_info.get('id')
        cache_key = f"user_orders_{user_id}"
        orders = cache.get(cache_key)
        if orders is None:
            orders = list(order.objects.filter(stuID_id=user_id))
            cache.set(cache_key, orders, 120)
        return render(request, 'user_order.html', {'orders': orders})
    else:
        return JsonResponse({'status': 'error', 'message': '无效的请求方法'})



def complete_order(request, order_id):
    if request.method == "POST":
        user_info = request.session.get("info")
        if not user_info:
            return JsonResponse({'status': 'error', 'message': '用户未登录'})

        try:
            order_obj = order.objects.get(id=order_id)
            delivery_person = order_obj.deliverId

            if not delivery_person:
                return JsonResponse({'status': 'error', 'message': '订单没有分配配送员'})

            # 减少配送员的工作量
            workload_int = int(delivery_person.workload)  # 将 '1' 转换为 1
            workload_int -= 1  # 1 + 1 = 2
            delivery_person.workload = str(workload_int)  # 将 2 转换为 '2'
            delivery_person.save()

            # 如果工作量为0，将工作状态改为空闲
            if workload_int == 0:
                delivery_person.time = 1  # 1 表示空闲
                delivery_person.save()


            # 更新订单的完成时间
            order_obj.completeTime = datetime.now().replace(microsecond=0)
            order_obj.status = 3  # 设置订单状态为“完成”
            order_obj.save()

            return JsonResponse({'status': 'success', 'message': '订单完成'})
        except order.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': '订单不存在'})
    else:
        return JsonResponse({'status': 'error', 'message': '无效的请求方法'})