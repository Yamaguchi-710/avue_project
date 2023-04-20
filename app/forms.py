from django import forms

Reach = (
    (100,"100cm"),
    (110,"110cm"),
    (120,"120cm"),
    (130,"130cm"),
    (140,"140cm"),
    (150,"150cm"),
    (160,"160cm"),
    (170,"170cm"),
    (180,"180cm"),
    (190,"190cm"),
    (200,"200cm")
)

Size = (
    (1,"Small"),
    (2,"Avarage"),
    (3,"Large"),
    (4,"Ignore")
)

Level = (
    (15,"Easy"),
    (30,"Normal"),
    (45,"Hard"),
    (60,"Harder"),
    (75,"Hardest"),
    (100,"Hell")
)

class CalcPlusForm(forms.Form):
    val1 = forms.ChoiceField(label="Your Reach", choices=Reach, initial=170)
    val2 = forms.ChoiceField(label="Size of Holds",choices=Size, initial=2)
    val3 = forms.ChoiceField(label="Level", choices=Level, initial=30)
    