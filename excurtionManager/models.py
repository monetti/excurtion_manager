from django.contrib.gis.db.models.manager import GeoManager
from django.core.mail import send_mail
from django.core.mail.message import BadHeaderError
from django.db import models
from django.http import HttpResponse, HttpResponseRedirect
from tursoft.settings import EMAIL_HOST_USER
import django.contrib.gis.db.models as gis_models

class Notification(models.Model):
    description = models.TextField("Descripcion")
    created = models.DateField(auto_now=True, editable=False)
    
    class Meta:
        ordering = ('-created',)

class TechnicNote(models.Model):
    name = models.CharField("Nombre",max_length=50)
    document = models.TextField("Descripcion")
    high_land = models.BooleanField("Alta Montania",blank=True)
    
    def __str__(self):
        return self.name
    
    def __unicode__(self):
        return self.name
    
class Equipment(models.Model):
    name = models.CharField("Nombre",max_length=50)
    high_land = models.BooleanField("Alta Montania",blank=True)
    
    def __str__(self):
        return self.name
        
class Issue(models.Model):
    name = models.CharField("Nombre",max_length=50)
    type = models.CharField(max_length=2,choices=(('CO','Comida'),('TR','Transporte'),('AR','Arancel'),('HO','Honorarios'),('SE','Seguro'),('PU', 'Publicidad')))
    created = models.DateField(auto_now=True, editable=False)
    
    def __str__(self):
        return self.name + '-' + self.type
    
    def __unicode__(self):
        return self.name + '-' + self.type
    
class ProductQuotation(models.Model):
    issue = models.ForeignKey('Issue',verbose_name='Rubro')
    amount = models.IntegerField("Cantidad",default=0)
    price = models.FloatField("Precio",default=0.0)
    organization = models.BooleanField("Organizacion",default=True)
    created = models.DateField(auto_now=True, editable=False)
    
    def __str__(self):
        return self.issue.name + " - " + str(self.amount) + " - " + str(self.price) + " - " + ("Participante", "Organizacion")[not self.organization] 
    
class Distrit(models.Model):
    name = models.CharField("Nombre",max_length=50)
    
    def __str__(self):
        return self.name
    
    def __unicode__(self):
        return self.name
    
class Benefit(models.Model):
    name = models.CharField("Nombre",max_length=50)
    
    def __str__(self):
        return self.name
    
    def __unicode__(self):
        return self.name
    
class Country(models.Model):
    name = models.CharField("Nombre",max_length=50)
    
    def __str__(self):
        return self.name
    
    def __unicode__(self):
        return self.name

class Client(models.Model):
    name = models.CharField("Nombre",max_length=50)
    last_name = models.CharField("Apellido",max_length=50)
    email = models.EmailField("Email")
    phone = models.CharField("Telefono",max_length=15,blank=True)
    country = models.ForeignKey('Country',verbose_name='Pais',blank=True,null=True)
    provenance = models.ForeignKey('Distrit',verbose_name='Provincia',blank=True,null=True)
    place = models.CharField("Localidad",max_length=100,blank=True)
    dni = models.CharField("DNI",max_length=15,blank=True)
    birthday = models.DateField("Fecha de Nacimiento",blank=True,null=True)
    url = models.URLField("Web",blank=True)
    foreign = models.BooleanField("Extranjero/a")
    created = models.DateField(auto_now=True,editable=False)
    
    def __str__(self):
        return self.name
    
    def __unicode__(self):
        return self.name
    
class Region(models.Model):
    name = models.CharField("Nombre",max_length=50)
    
    def __str__(self):
        return self.name
    
    def __unicode__(self):
        return self.name
        
class Excurtion(models.Model):
    name = models.CharField("Nombre",max_length=100)
    study = models.OneToOneField('Study',verbose_name='Relevamiento')
    description = models.TextField("Descripcion")
    include_services = models.TextField("Servicios que Incluye")
    not_include_services = models.TextField("Servicios que No Incluye")
    date_from = models.DateField("Fecha Inicio")
    date_to = models.DateField("Fecha Fin")
    min_amount = models.IntegerField("Cantidad Minima de Participantes")
    activities = models.TextField("Actividades")
    created = models.DateField(auto_now=True,editable=False)
    
    def __str__(self):
        return self.name
    
    def __unicode__(self):
        return self.name
    
class Study(gis_models.Model):
    location = gis_models.PointField("Ubicacion",blank=True,null=True)
    distrit = models.ForeignKey("Distrit",verbose_name='Provincia',blank=True,null=True)
    access = models.TextField("Accceso", blank=True)
    map = gis_models.PolygonField("Mapa",blank=True,null=True)
    region = models.ForeignKey('Region',verbose_name='Region',blank=True,null=True)
    other_features = models.TextField("Otros Atractivos", blank=True)
    circuit =  gis_models.PolygonField("Circuito",blank=True,null=True)
    pay = models.BooleanField("Pago de Arancel", blank=True)
    amount_pay = models.IntegerField("Monto",default=0, blank=True)
    vhf = models.CharField("Frecuencia VHF",max_length=10,blank=True)
    available_from = models.DateField("Desde")
    available_to = models.DateField("Hasta")
    high_land = models.BooleanField("Alta Montania",blank=True)
    contingency_plan = models.TextField("Plan de Contingencia", blank=True)
    comments = models.TextField("Observaciones",blank=True)
    suppliers = models.ManyToManyField('Supply',verbose_name='Proveedores')
    created = models.DateField(auto_now=True,editable=False) 
    
    objetcs = GeoManager()
    
    def __str__(self):
        return self.region.name + " - " + self.distrit.name
    
class Supply(gis_models.Model):
    name = models.CharField("Nombre",max_length=50)
    address = models.CharField("Direccion",max_length=50)
    location = gis_models.PointField("Ubicacion",blank=True,null=True)
    url = models.URLField("Web",blank=True)
    tel = models.CharField("Nombre",max_length=50,blank=True)
    email = models.EmailField("Email",blank=True)
    benefits = models.ManyToManyField("Benefit")
    comments = models.TextField("Observaciones", blank=True)
    created = models.DateField(auto_now=True,editable=False)
    
    objetcs = GeoManager()
    
    def __str__(self):
        return self.name
    
    def __unicode__(self):
        return self.name
    
class Product(models.Model):
    excurtion = models.ForeignKey('Excurtion',verbose_name='Excursion')
    competitors = models.ManyToManyField('Client',verbose_name='Participantes')
    product_quotation = models.ManyToManyField('ProductQuotation',verbose_name='Cotizaciones')
    price = models.FloatField("Precio",default=0.0)
    percentage = models.IntegerField("Porcentaje de Ganancia",default=0)
    technics_note = models.ManyToManyField('TechnicNote',verbose_name='Notas Tecnicas')
    equipments = models.ManyToManyField('Notification',verbose_name='Equipamiento a Llevar')
    created = models.DateField(auto_now=True,editable=False)
    
    class Meta:
        ordering=('-created',)
    
    def __str__(self):
        return self.excurtion.name
    
    def get_honorarios(self):
        cotizaciones = self.product_quotation.values()
        total = 0.0
        for c in cotizaciones:
            if c.issue.type == 'Honorarios':
                    total += c['price'] * c['amount']
        return total
    
    def get_amount_competitors(self):
        return len(self.competitors.all())
    
    def precio_estimado(self):
        return self.subtotal() * ((self.percentage/100.0)+1)
    
    def subtotal(self):
        return self.subtotal_organizacion() + self.subtotal_participantes()
    
    def subtotal_organizacion(self):
        cotizaciones = self.product_quotation.values()
        total = 0.0
        for c in cotizaciones:
            if c['organization']:
                total += c['price'] * c['amount']
        return total
    
    def subtotal_participantes(self):
        cotizaciones = self.product_quotation.values()
        total = 0.0
        for c in cotizaciones:
            if not c['organization']:
                total += c['price'] * c['amount']
        return total
    
    def subtotal_comida_organizacion(self):
        cotizaciones = self.product_quotation.values()
        total = 0.0
        for c in cotizaciones:
            if c['organization']:
                if c.issue.type == 'Comida':
                    total += c['price'] * c['amount']
        return total
    
    def subtotal_comida_participantes(self):
        cotizaciones = self.product_quotation.values()
        total = 0.0
        for c in cotizaciones:
            if not c['organization']:
                if c.issue.type == 'Comida':
                    total += c['price'] * c['amount']
        return total
    
    def costo_directo_grupal(self):
        return self.subtotal_participantes()*self.get_amount_competitors()
    
    def costo_directo_individual(self):
        return self.subtotal_participantes()
    
    def costo_indirecto_grupal(self):
        return self.subtotal_organizacion()
    
    def costo_indirecto_individual(self):
        return float(self.costo_indirecto_grupal()/self.get_amount_competitors())
    
    def costo_final_grupal(self):
        return self.costo_final_individual()*self.get_amount_competitors()
    
    def costo_final_individual(self):
        return self.costo_directo_individual()+self.costo_indirecto_individual()
    
    def facturacion(self):
        return self.precio_estimado()*self.get_amount_competitors()
    
    def utilidad(self):
        return self.facturacion() -  self.gastos()
    
    def utilidad_por_participante(self):
        return self.utilidad() / self.get_amount_competitors()
    
    def utilidad_mas_guiada(self):
        return self.utilidad() + self.get_honorarios()
    
    def gastos(self):
        return self.subtotal_organizacion() + self.costo_directo_grupal()
         
    def send_evaluation_sheet(self):
        ''' La Ficha de Satisfaccion (evaluation sheet) es un formulario que el cliente rellena luego de realizarse la excursion. '''
        ''' Envia email a los participantes del evento con link a evaluation_sheet para cada uno '''
        pass
    

    

    
