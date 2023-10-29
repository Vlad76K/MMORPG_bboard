import random

from django.contrib.auth.models import User
from django.views.generic.edit import CreateView

from .forms import SignupForm
from .models import BaseRegisterForm

from django.shortcuts import redirect, render
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required

from .my_sign_func import insert_confirmation_code, select_confirmation_code, send_conf_code


class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = '/'
    signup_frm = SignupForm()
    cc_email = ''

    def post(self, request, *args, **kwargs):
        cc_code = request.POST['conf_code']
        form_su = SignupForm(request.POST)
        if cc_code == '':
            self.cc_email = self.request.POST['email']
            self.signup_frm = self.model.objects.all()

            cc_code = random.randint(1000, 9999)
            insert_confirmation_code(cc_code, 1, self.cc_email)
            send_conf_code(cc_code, self.cc_email)

            if request.method == 'POST':
                if form_su.is_valid():
                    user = form_su.save(commit=False)
                    user.is_active = False
                    user.save()
                else:
                    form_su = SignupForm()
                    # return HttpResponse('Ошибки в заполнении формы!')
            else:
               pass
            # self.form_class = self.signup_frm
        else:
            if request.method == 'POST':
                if request.POST['conf_code'] == select_confirmation_code(request.POST['conf_email']):
                    user = User.objects.get(email=request.POST['conf_email'])
                    user.is_active = 1
                    user.save()
                    return redirect('../../sign/login/')
            else:
                form_su = SignupForm()

        return render(request, 'sign/signup.html', {'form_su': form_su})

@login_required
def upgrade_me(request):
    user = request.user
    premium_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        premium_group.user_set.add(user)
    return redirect('/')
