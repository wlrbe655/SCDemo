from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect


# 中间键知识点：控制 请求和响应
# 如何用代码获取到浏览器输入框的地址

# class M1(MiddlewareMixin):
#     def process_request(self, request):
#         print("我是M1，我进来了")
#
#
#
#     def process_response(self, request, response):
#         print("我是M1，我出去了")
#         return response
#
# class M2(MiddlewareMixin):
#     def process_request(self, request):
#         print("我是M1，我进来了")
#
#     def process_response(self, request, response):
#         print("我是M1，我出去了")
#         return response
#


# 如果用户在地址栏输入除登录以外的地址就进行拦截


#
# class AuthMiddleware(MiddlewareMixin):
#     def process_request(self, request):
#         # 1.排除那些不需要登录就能访问的页面
#         # request.path_info 获取当前用户在浏览器输入框的地址
#         if request.path_info in ["/login/","/image/code/","/register/"]:
#             return
#         if request.session.get("info"):
#             return
#         else:
#             return redirect('/login')