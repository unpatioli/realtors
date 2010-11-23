from django import forms

from usermessages.models import Usermessage

class UsermessageForm(forms.ModelForm):
    class Meta:
        model = Usermessage
        fields = ('subject', 'text', 'is_draft')
        widgets = {
            'is_draft': forms.HiddenInput,
        }
    
    def clean_is_draft(self):
        if 'save_to_drafts' in self.data:
            return True
        return False
    

