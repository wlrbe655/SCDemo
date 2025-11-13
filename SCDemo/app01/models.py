from django.db import models

# Create your models here.


class Stu(models.Model):
    def __str__(self):
        return self.name


    id = models.CharField(verbose_name='学号', primary_key=True, max_length=10, error_messages={'unique': '该学号已存在，请使用其他学号。'})
    name = models.CharField(verbose_name='学生姓名', max_length=100)
    tel = models.CharField(verbose_name='手机号码', max_length=11)
    qsld = models.CharField(verbose_name='寝室号', max_length=32)
    password = models.CharField(verbose_name='密码', max_length=32)
    datetime = models.CharField(verbose_name='注册时间', max_length=32)



class admin(models.Model):
    def __str__(self):
        return self.username


    username = models.CharField(verbose_name='管理员', max_length=100)
    tel = models.CharField(verbose_name='手机号码', max_length=11)
    password = models.CharField(verbose_name='密码', max_length=100)




class job(models.Model):
    def __str__(self):
        return self.name


    name = models.CharField(verbose_name='兼职人员', max_length=100)
    tel = models.CharField(verbose_name='手机号', max_length=11)
    available_Time = (
        (1, "空闲"),
        (2, "配送中")
    )
    time = models.SmallIntegerField(verbose_name="状态", choices=available_Time, default=1)
    workload = models.CharField(verbose_name='工作量', max_length=100, default='0')



class order(models.Model):
    def __str__(self):
        return f"Order {self.id}"

    id = models.AutoField(verbose_name='订单ID', primary_key=True)
    stuID = models.ForeignKey('Stu', on_delete=models.CASCADE, related_name='orders')
    deliverId = models.ForeignKey('job', on_delete=models.CASCADE, related_name='orders', null=True, blank=True)
    goodsDetails = models.CharField(verbose_name='商品信息', max_length=100)
    money = models.CharField(verbose_name='费用', max_length=100)
    status_choices = (
        (1, "未发货"),
        (2, "配送中"),
        (3, "已送达")
    )
    status = models.SmallIntegerField(verbose_name="配送状态", choices=status_choices, default=1)
    createTime = models.CharField(verbose_name='创建时间', max_length=100)
    sendTime = models.CharField(verbose_name='配送时间', max_length=100, null=True, blank=True)
    completeTime = models.CharField(verbose_name='完成时间', max_length=100, null=True, blank=True)
    is_paid = models.BooleanField(verbose_name='支付状态',default=False)  # 添加支付状态字段


class goods(models.Model):
    def __str__(self):
        return self.name


    id = models.AutoField(verbose_name='商品ID', primary_key=True)
    name = models.CharField(verbose_name='商品名称', max_length=100)
    price = models.FloatField(verbose_name='商品价格')
    stock = models.IntegerField(verbose_name='商品库存')
    img = models.FileField(verbose_name="图片",upload_to="city/")
    category = models.CharField(verbose_name='商品分类', max_length=50)
    description = models.TextField(verbose_name='商品描述')


