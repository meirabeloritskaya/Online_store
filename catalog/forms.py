from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    forbidden_words = [
        'казино', 'криптовалюта', 'крипта',
        'биржа', 'дешево', 'бесплатно',
        'обман', 'полиция', 'радар'
    ]

    class Meta:
        model = Product
        fields = ['name', 'description']

    def clean_name(self):
        name = self.cleaned_data['name']
        self.validate_forbidden_words(name)
        return name

    def clean_description(self):
        description = self.cleaned_data['description']
        self.validate_forbidden_words(description)
        return description

    def validate_forbidden_words(self, text):
        text_lower = text.lower()
        for word in self.forbidden_words:
            if word in text_lower:
                raise forms.ValidationError(f"Использование слова '{word}' запрещено.")

    def clean_price(self):
        price = self.cleaned_data.get('price')

        if price is not None and price < 0:
            raise forms.ValidationError("Цена не может быть отрицательной.")

        return price