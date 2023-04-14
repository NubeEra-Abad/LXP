from django.shortcuts import render
from django.contrib.auth import get_user_model
def activate(request, uidb64, token):
    utype = '2'
    User = get_user_model()
    #try:
    user = User.objects.get(pk=uidb64)
    usertoken = User.objects.raw('SELECT user_id as id, activation_token FROM auth_userprofile WHERE user_id = ' + str(uidb64))
    for x in usertoken:
        usertoken = x.activation_token
    
    if user is not None and usertoken is not None and usertoken == token:
        user.is_active = True
        user.save()
        usertoken = User.objects.raw('UPDATE social_auth_usersocialauth SET utype = ' + utype + ' WHERE user_id = ' + str(uidb64))
        return render(request, 'lxpapp/users/activation_success.html',{'User':user})
    
    else:
        # Display an error page
        return render(request, 'lxpapp/users/activation_error.html')
