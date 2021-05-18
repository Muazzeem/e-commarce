from io import BytesIO
from django.http import HttpResponse, Http404
from django.template.loader import get_template
from django.views import View
from num2words import num2words
from xhtml2pdf import pisa
from store.models import *


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


class GeneratePdf(View):
    def get(self, request, *args, **kwargs):
        order_number = self.kwargs['number']
        try:
            order = Order.objects.get(user=request.user, id=order_number)
        except Order.DoesNotExist:
            raise Http404
        context = {"order": order, "price": num2words(order.total)}
        pdf = render_to_pdf('invoice.html', context)
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "Invoice_%s.pdf" % order_number
        content = "inline; filename='%s'" % filename
        download = request.GET.get("download")
        if download:
            content = "attachment; filename='%s'" % filename
        response['Content-Disposition'] = content
        return response
