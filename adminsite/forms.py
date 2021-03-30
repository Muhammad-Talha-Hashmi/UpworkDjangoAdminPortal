
#Don't Edit only use
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit
from django import forms

from adminsite.models import Users


class MangeUsersForm(forms.ModelForm):

    class Meta():
        model = Users
        fields = ['role']

    ROLE_CHOICES = (
        ('researcher', 'Researcher'),
        ('admin', 'Admin'),
    )

    role = forms.CharField(
        widget=forms.Select(choices=ROLE_CHOICES)
    )



    def _init_(self, *args, **kwargs):
        super(MangeUsersForm, self)._init_(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False

    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)