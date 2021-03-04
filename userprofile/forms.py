# 引入表单类
from django import forms
# 引入 User 模型
from django.contrib.auth.models import User
from .models import Profile

# 登录表单，继承了 forms.Form 类
class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()

# 注册表单
class UserRegisterForm(forms.ModelForm):
    # 对数据库进行操作的表单应该继承forms.ModelForm，
    # 可以自动生成模型中已有的字段。

    password = forms.CharField()
    password2 = forms.CharField()
    class Meta:
        model = User
        fields = ('username', 'email')

    # def clean_[字段] 这种写法Django会自动调用，来对单个字段的数据进行验证清洗。
    def clean_password2(self):
        date = self.cleaned_data
        if date.get('password') == date.get('password2'):
            # 这种取字典值得写法使得即使该字段为空 程序也不会跳出
            return date.get('password')
        else:
            raise forms.ValidationError('密码输入不一致,请重试。')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('phone', 'avatar', 'bio')


