import datetime
from fpdf import FPDF
from data_center.models import InvoiceProduct, QuotationProduct


class PdfHandler:
    def __init__(self, orientation='P', unit='pt', format='A4'):
        self.pdf_handler = FPDF(orientation=orientation, unit=unit, format=format)
    
    def _set_margins(self, left, top, right=-1):
        return self.pdf_handler.set_margins(left, top, right=right)

    def _set_title(self, title):
        return self.pdf_handler.set_title(title)

    def _set_subject(self, subject):
        return self.pdf_handler.set_subject(subject)

    def _set_author(self, author):
        return self.pdf_handler.set_author(author)

    def _set_keywords(self, keywords):
        return self.pdf_handler.set_keywords(keywords)

    def _set_creator(self, creator):
        return self.pdf_handler.set_creator(creator)

    def _add_page(self, orientation=''):
        return self.pdf_handler.add_page(orientation=orientation)

    def _set_draw_color(self, r, g=-1, b=-1):
        return self.pdf_handler.set_draw_color(r, g=g, b=b)

    def _set_fill_color(self, r, g=-1, b=-1):
        return self.pdf_handler.set_fill_color(g=g, b=b)

    def _set_text_color(self, r, g=-1, b=-1):
        return self.pdf_handler.set_text_color(r, g=-g, b=b)

    def _get_string_width(self, s):
        return self.pdf_handler.get_string_width(s)

    def _set_line_width(self, width):
        return self.pdf_handler.set_line_width(width)

    def _line(self, x1, y1, x2, y2):
        return self.pdf_handler.line(x1, y1, x2, y2)

    def _dashed_line(self, x1, y1, x2, y2, dash_length=1, space_length=1):
        return self.pdf_handler.dashed_line(x1, y1, x2, y2, dash_length=dash_length, space_length=space_length)

    def _rect(self, x, y, w, h, style=''):
        return self.pdf_handler.rect(x, y, w, h, style=style)

    def _ellipse(self, x, y, w, h, style=''):
        return self.pdf_handler.ellipse(x, y, w, h, style=style)

    def _set_font(self, family, style='', size=0):
        return self.pdf_handler.set_font(family, style=style, size=size)

    def _set_font_size(self, size):
        return self.pdf_handler.set_font_size(size)

    def _text(self, x, y, txt=''):
        return self.pdf_handler.text(x, y, txt=txt)

    def _multi_cell(self, w, h, txt='', border=0, align='J', fill=0, split_only=False):
        return self.pdf_handler.multi_cell(w, h, txt=txt, border=border, align=align, fill=fill, split_only=split_only)

    def _write(self, h, txt='', link=''):
        return self.pdf_handler.write(h, txt=txt, link=link)

    def _image(self, name, x=None, y=None, w=0, h=0, image_type='', link=''):
        return self.pdf_handler.image(name, x=x, y=y, w=w,h=h,type=image_type,link=link)

    def _normalize_text(self, txt):
        return self.pdf_handler.normalize_text(txt)

    def _output(self, name='', dest=''):
        return self.pdf_handler.output(name, dest)

    @staticmethod
    def generate_invoice_product_display_name(invoice_product):
        from_date = invoice_product.check_in
        to_date = invoice_product.check_out
        stay_length_concat = ''
        if to_date and from_date:
            display_from = datetime.date(from_date.year,from_date.month,from_date.day).strftime('%d/%m/%Y')
            display_to = datetime.date(to_date.year,to_date.month,to_date.day).strftime('%d/%m/%Y')
            stay_length_concat = f'({display_from} - {display_to})'
        return f'{invoice_product.product.product_name} {stay_length_concat}'

    @staticmethod
    def get_total(data):
        """ This function calculates a total amount due, for the passed data, to be written to the invoice """
        total = 0.0
        products = []
        if data.get("invoiceproduct_set"):
            products = data.get("invoiceproduct_set")
        elif data.get("quotationproduct_set"):
            products = data.get("quotationproduct_set")
        total = 0
        for product in products:
            days_of_service = 1
            if product.check_out and product.check_in:
                days_of_service = 1
                if product.check_out > product.check_in:
                    days_of_service = product.check_out - product.check_in
                    days_of_service = days_of_service.days
            product_quantity = product.product_quantity
            product_price = product.product.product_price
            product_total = days_of_service * float(product_price) * float(product_quantity)
            total = total + product_total

        return '%.2f' % total

    @staticmethod
    def calculate_number_of_pages(data):
        """ Uses the number of products to calculate the number of pages required in the invoice """
        products = data["products"]

        return int(len(products) / 15) + 1

