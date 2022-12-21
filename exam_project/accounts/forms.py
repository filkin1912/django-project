from django.contrib.auth import forms as auth_forms, get_user_model

UserModel = get_user_model()


class ProfileCreateForm(auth_forms.UserCreationForm):
    class Meta(auth_forms.UserCreationForm.Meta):
        model = UserModel
        fields = ('username', 'email')
        field_classes = {'username': auth_forms.UsernameField, }


class ProfileEditForm(auth_forms.UserChangeForm):
    class Meta:
        model = UserModel
        fields = '__all__'
        field_classes = {'username': auth_forms.UsernameField}
