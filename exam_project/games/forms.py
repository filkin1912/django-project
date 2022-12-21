from django import forms
from exam_project.games.models import GameModel


class GameBaseForm(forms.ModelForm):
    class Meta:
        model = GameModel
        fields = '__all__'


class GameAddForm(GameBaseForm):
    class Meta:
        model = GameModel
        fields = '__all__'
        exclude = ('user',)
        labels = {
            'title': 'Title',
            'image_url': 'Link to Image',
        }
        widgets = {
            'title': forms.TextInput(
                attrs={
                    'placeholder': 'Write title'
                }
            ),
            'image_url': forms.URLInput(
                attrs={
                    'placeholder': 'Link to image',
                }
            ),
        }


class GameDetailsForm(GameBaseForm):
    pass


class GameEditForm(GameBaseForm):
    class Meta:
        model = GameModel
        fields = '__all__'
        exclude = ('user',)


class GameDeleteForm(GameBaseForm):
    class Meta:
        model = GameModel
        exclude = ('category', 'user',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__set_disabled_fields()

    def save(self, commit=True):
        if commit:
            self.instance.delete()
        return self.instance

    def __set_disabled_fields(self):
        for _, field in self.fields.items():
            field.widget.attrs['readonly'] = 'readonly'


class GameBuyForm(GameBaseForm):
    class Meta:
        model = GameModel
        fields = '__all__'
        exclude = ('user',)
