# unchained_editor/widgets.py
import jwt
from django.conf import settings
from django import forms
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string
from datetime import datetime

PUBLIC_KEY = """
-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAnL33GSLBG295MRI/D0Dp
47x0ZFgnupGw0j6h/4LMoA46yc41n9BVnT+4aLpryb8+QKwOlMoH6nXJHG8zkSLZ
cekieq/oMX+K1NrtYED70nMRNCzrbHtfDLy5UMAEQaBKDtc93ZB7GNWGNAKAF5OR
2G8VqDbIfIN56U79yZP8RsAr/fZ7yTZSH3uRmiKe1MuGUyMA6v46g0k81JdZITHn
45UCYoH7eSZgtH0uvJ6d9ShJk+4rfFPo/iith4QfrAb2yZGW6fZNf2oUFquwT9HF
V0CxlnNgPoiyulAH2Xsw50a/6rGnwKztpvaa84Sj77opbXyZzB/SjOAsYZRNu860
TwIDAQAB
-----END PUBLIC KEY-----
"""

class CustomWYSIWYGWidget(forms.Widget):
    """
    Custom Widget for rendering the WYSIWYG editor.
    """
    template_name = 'unchained_editor/editor.html'

    class Media:
        css = {
            'all': ('unchained_editor/css/styles.css',)
        }
        js = ('unchained_editor/js/script.js',)

    def __init__(self, attrs=None, license_key=None):
        default_attrs = {'class': 'custom-wysiwyg'}
        if attrs:
            default_attrs.update(attrs)
        super().__init__(attrs=default_attrs)

        # If license_key is not passed in, fall back to Django settings
        if license_key is None:
            license_key = getattr(settings, 'UNCHAINED_EDITOR_LICENSE_KEY', None)

        self.license_key = license_key
        self.license_valid = self.verify_license(self.license_key) if self.license_key else False

    def render(self, name, value, attrs=None, renderer=None):
        license_valid = self.license_valid
        # Render the hidden textarea to store the content
        textarea_html = forms.Textarea(
            attrs={'name': name, 'id': f'id_{name}', 'style': 'display:none;'}
        ).render(name, value, attrs, renderer)
        
        # Render the WYSIWYG editor HTML once
        editor_html = render_to_string(self.template_name, {
            'name': name,
            'value': value,
            'license_valid': license_valid,
        })
        
        # Combine both with synchronization script
        combined_html = f"""
            {textarea_html}
            {editor_html}
            <script>
                initializeCustomWYSIWYG('{name}');
            </script>
        """
        return mark_safe(combined_html)

    def verify_license(self, license_key):
        if not license_key:
            return False

        try:
            payload = jwt.decode(license_key, PUBLIC_KEY, algorithms=['RS256'])
            
            return True
        
        except jwt.ExpiredSignatureError:
            return False
        except jwt.InvalidTokenError as e:
            return False


    def get_context(self, name, value, attrs):
        """
        Pass license validity to the template so you can display an error or
        disable the editor if the license is invalid.
        """
        context = super().get_context(name, value, attrs)
        context['widget']['license_valid'] = self.license_valid
        return context
