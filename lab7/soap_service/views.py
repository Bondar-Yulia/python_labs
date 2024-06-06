from spyne import Application, rpc, ServiceBase, Unicode
from spyne.protocol.soap import Soap11
from spyne.server.django import DjangoApplication
from django.views.decorators.csrf import csrf_exempt
from .models import Manufacturer, Brand

class SoapService(ServiceBase):
    @rpc(_returns=Unicode)
    def get_all_manufacturers(ctx):
        manufacturers = Manufacturer.objects.all()
        return ', '.join([m.name for m in manufacturers])

    @rpc(Unicode, _returns=Unicode)
    def get_brands_by_manufacturer(ctx, manufacturer_name):
        try:
            manufacturer = Manufacturer.objects.get(name=manufacturer_name)
            brands = Brand.objects.filter(manufacturer=manufacturer)
            return ', '.join([b.name for b in brands])
        except Manufacturer.DoesNotExist:
            return 'Manufacturer not found'

soap_app = Application([SoapService],
                       tns='soap_service',
                       in_protocol=Soap11(validator='lxml'),
                       out_protocol=Soap11())

django_soap_application = DjangoApplication(soap_app)
soap_service_view = csrf_exempt(django_soap_application)
