from django import forms


class ProductCreateForm(forms.Form):
    image = forms.FileField(required=False)
    title = forms.CharField(max_length=36, min_length=3)
    description = forms.CharField(widget=forms.Textarea())
    price = forms.FloatField()


class CategoryCreateForm(forms.Form):
    title = forms.CharField(max_length=36, min_length=3)


# class CombinedForm(forms.Form):
#     def __init__(self, *args, **kwargs):
#         super(CombinedForm, self).__init__(*args, **kwargs)
#         self.fields.update(ProductCreateForm().fields)
#         self.fields.update(CategoryCreateForm().fields)
