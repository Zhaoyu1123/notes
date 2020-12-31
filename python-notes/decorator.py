# coding: utf-8
# 装饰器 
# 在编写装饰器时，在实现前加入 @functools.wraps(func) 可以保证装饰器不会对被装饰函数造成影响。比如，在 Flask 中，我们要自己重写 login_required 装饰器，但不想影响被装饰器装饰的方法，则 login_required 装饰器本身可以写成下面的样子
from functools import warps

def outer(*args, **kwargs):
    def login_required_(func):
        @wraps(func)
        def decorated_view(*args, **kwargs):
            if current_app.login_manager._login_disabled:
                return func(*args, **kwargs)
            elif not current_user.is_authenticated:
                # return current_app.login_manager.unauthorized()
                return redirect(url_for("login.loginPage", next=request.url))
            return func(*args, **kwargs)
    
        return decorated_view
    return login_required_   
     

    

