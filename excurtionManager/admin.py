from django.contrib import admin
from models import *
from django.contrib.gis.geos import Point
from django import forms
from tinymce.widgets import TinyMCE
from tursoft.settings import EMAIL_HOST_USER
from django.core.mail import send_mail
from django.core.mail.message import BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect

def send_email(modeladmin, request, queryset):
        ''' envia email a los participantes del evento. El email se compone de notas tecnicas, condiciones de contratacion y ficha medica '''
        ''' El usuario elije la/s nota/s tecnica/s. Si el producto es de alta montania deben mostrarse aquellas notas tecnicas pertinentes '''
        ''' El usuario recorre la lista de partipantes y envia email con datos a cada uno '''
        ''' Los datos deben ir como adjuntos en el email '''
        from_email = EMAIL_HOST_USER
                
        subject = modeladmin.excurtion.name
        message = '' 
        
        if subject and message and from_email:
            try:
                #each obj is a product
                for obj in queryset:
                    #each p is a competitor
                    for p in obj.competitors_set.all():
                        send_mail(subject, message, from_email, [p.email])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return HttpResponseRedirect(request)
        else:
            # In reality we'd use a form class
            # to get proper validation errors.
            return HttpResponse('Esta seguro que todos los campos estan correctos?')
send_email.short_description = "Enviar Email"

class TechnicNoteAdmin(admin.ModelAdmin):
    filter=['high_land']
    
    
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE(attrs={'cols': 100, 'rows': 100})},  
    }

class ExcurtionAdmin(admin.ModelAdmin):
    actions_on_top = True
    actions_on_bottom = True
    actions_selection_counter = True
    date_hierarchy = 'created'
    fields = (('name','study','min_amount','date_from','date_to'),'description',('include_services','not_include_services'),'activities',)
    list_filter = ('study__region','study__distrit','created')
    list_per_page = 25
    list_select_related = True
    
class StudyAdmin(admin.ModelAdmin):
    actions_on_top = True
    actions_on_bottom = True
    actions_selection_counter = True
    date_hierarchy = 'created'
    #fields = (('distrit','region'),('access','other_features','circuit'),('location','map'),('pay','amount_pay','vhf'),('available_from','available_to','high_land'),('contingency_plan','suppliers'))
    fields = (('distrit','region','available_from','available_to'),('pay','amount_pay','vhf','high_land'),'suppliers','access','other_features','contingency_plan')
    list_filter = ('pay','vhf','suppliers','created','region','distrit','high_land')
    filter = ('high_land',)
    filter_horizontal = ('suppliers',)
    list_per_page = 25
    list_select_related = True

class ProductAdmin(admin.ModelAdmin):
    actions_on_top = True
    actions_on_bottom = True
    actions_selection_counter = True
    date_hierarchy = 'created'
    list_per_page = 25
    list_select_related = True
    filter_horizontal = ('competitors','product_quotation','technics_note')
    fields = (('excurtion','price','percentage'),('competitors','product_quotation'),'technics_note')
    list_display = ('excurtion','precio_estimado','percentage','price','subtotal','subtotal_participantes','subtotal_organizacion','subtotal_comida_organizacion','subtotal_comida_participantes','costo_directo_grupal','costo_directo_individual','costo_indirecto_grupal','costo_indirecto_individual','costo_final_grupal','costo_final_individual','facturacion','utilidad','utilidad_por_participante')
    actions = [send_email] 

class SupplyAdmin(admin.ModelAdmin):
    actions_on_top = True
    actions_on_bottom = True
    actions_selection_counter = True
    date_hierarchy = 'created'
    list_filter = ('benefits','created')
    list_per_page = 25
    list_select_related = True
    filter_horizontal = ('benefits',)

class ClientAdmin(admin.ModelAdmin):
    actions_on_top = True
    actions_on_bottom = True
    actions_selection_counter = True
    date_hierarchy = 'created'
    list_filter = ('country','provenance','foreign')
    list_per_page = 25
    list_select_related = True
    list_display = ('last_name','name','phone','email','country','provenance')
    fieldsets = (
                 ('Datos Personales',{'fields':(('last_name','name'),('dni','birthday')),'classes': ['wide', 'extrapretty']}),
                 ('Datos de Contacto',{'fields':('email','phone','url'),'classes': ['wide', 'extrapretty']}),
                 ('Procedencia',{'fields':(('country','provenance','place'),'foreign'),'classes': ['collapse', 'extrapretty']}),
                )

class IssueAdmin(admin.ModelAdmin):
    actions_on_top = True
    actions_on_bottom = True
    actions_selection_counter = True
    date_hierarchy = 'created'
    list_filter = ('type')
    list_per_page = 25
    list_select_related = True
    list_display = ('name','type')

admin.site.register(Excurtion, ExcurtionAdmin)
admin.site.register(Study, StudyAdmin)
admin.site.register(Supply, SupplyAdmin)
admin.site.register(Benefit)
admin.site.register(Client, ClientAdmin)
admin.site.register(Country)
admin.site.register(Distrit)
admin.site.register(Region)
admin.site.register(Issue)
#admin.site.register(ProductQuotation)
#admin.site.register(Product,ProductAdmin)
admin.site.register(TechnicNote, TechnicNoteAdmin)
