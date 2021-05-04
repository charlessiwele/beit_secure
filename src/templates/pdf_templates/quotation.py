from fpdf import FPDF

from filerp.settings import ORGANISATION_LOGO, QUOTATION_ITEMS_PER_PAGE, QUOTATION_ITEMS_PER_PAGE


class QuotationTemplate:
    """ The model for the invoice resource """

    def __init__(self, data):
        """ Creates an invoice instance with the passed data and the FPDF library """
        self.pdf = FPDF()

        self.data = data
        self.pdf.set_title(f'{self.data.get("client_name")} | Quotation')
        self.pdf.set_font('Arial', 'B', 8)
        self.invoice_detail_current_line = 18
        self.invoice_detail_summary_line = 270
        self.margin_left = 15

        self.logo_width = 150
        self.logo_height = 35
        self.logo_start_y = 8
        self.title_text_y = self.logo_start_y + 50
        self.header_details_start_y = self.title_text_y + 10
        self.header_details_end_y = self.header_details_start_y
        self.product_table_y = 100

    def write_quotation_content(self, total, pages):
        """ The central function for writing invoice content based on invoice data in instance """
        all_products = self.data.get('products')
        if len(all_products) <= QUOTATION_ITEMS_PER_PAGE:
            last_page = True
            # 10 or less products posted to service, thus only one page required
            self.pdf.add_page()
            self.write_letterhead()
            self.write_document_title()
            self.write_header_details()
            self.write_content(total, all_products, last_page)
        else:
            # more than 10 products posted to service, 2 or more pages required
            for i in range(pages):
                if i == pages - 1:  # if current page we're writing to is the last page, then set flag to true
                    last_page = True
                else:
                    last_page = False

                first_index = 0 + i * QUOTATION_ITEMS_PER_PAGE
                second_index = QUOTATION_ITEMS_PER_PAGE + i * QUOTATION_ITEMS_PER_PAGE

                products = all_products[
                           first_index:
                           second_index]  # products on a given page will be a sublist of all products...
                # ...  based on page number so that a page always has 10 products
                self.pdf.add_page()
                self.write_letterhead()
                self.write_document_title()
                self.write_header_details()
                self.write_content(total, products, last_page, current_page_index=i, page_total=pages)

    def write_letterhead(self, header_title= 'Generic Invoice'):
        """ Draws the generic header content on the first page of the invoice """
        # image relative positioning, all other elements are relative to the logo positioning
        self.pdf.image(ORGANISATION_LOGO, self.margin_left, self.logo_start_y, self.logo_width, self.logo_height)
        self.pdf.set_font('Arial', size=22)

    def write_document_title(self, header_title= 'Generic Invoice'):
        """ Draws the generic header content on the first page of the invoice """
        # image relative positioning, all other elements are relative to the logo positioning

        # invoice
        self.pdf.set_font('Arial', size=30)
        self.write_text(self.margin_left, self.title_text_y, 'Quotation')

    def write_header_details(self, header_title= 'Generic Quotation'):
        """ Draws the generic header content on the first page of the invoice """
        # image relative positioning, all other elements are relative to the logo positioning

        # date, invoice number, and period
        self.pdf.set_font('Arial', size=12)
        header_details_y = self.header_details_start_y

        self.write_text(self.margin_left, header_details_y, f'Quotation No.: {self.data.get("quotation_number")}')

        header_details_y = header_details_y + 8
        self.write_text(self.margin_left, header_details_y, f'Quoted By: {self.data.get("user")}')

        header_details_y = header_details_y + 8
        self.write_text(self.margin_left, header_details_y, f'Date: {self.data.get("date")}')

        header_details_y = header_details_y + 8
        self.write_text(self.margin_left, header_details_y, f'Customer: {self.data.get("client_name")}')

        header_details_y = header_details_y + 8
        self.write_text(self.margin_left, header_details_y, f'Email: {self.data.get("client_email")}')
        self.header_details_end_y = header_details_y

    def write_content(self, total, products, last_page, current_page_index=0, page_total=1):
        """ Draws the cells for products and writes the products to the pages """
        # write titles and underline (line width 0.5mm, then reset to default)
        self.pdf.set_font('Arial', 'B', 12)
        product_table_y = self.header_details_end_y + 10

        self.pdf.set_line_width(0.5)
        self.pdf.line(15, product_table_y - 5, 195, product_table_y - 5)

        self.write_text(18, product_table_y, 'Product name:')
        self.write_text(105, product_table_y, 'SKU:')
        self.write_text(125, product_table_y, 'Qty:')
        self.write_text(140, product_table_y, 'Price:')
        self.write_text(165, product_table_y, 'Total:')

        product_table_y = product_table_y + 5
        self.pdf.set_line_width(0.5)
        self.pdf.line(15, product_table_y, 195, product_table_y)

        self.pdf.set_font('Arial', size=10)
        for product in products:
            title = product['title']
            sku = product['sku']
            quantity = product['quantity']
            price = product['price']
            product_total = '%.2f' % float(product['total'])

            if len(title) > 45:
                title = title[
                        0:40] + '...'  # truncating title and suffixing with dots, if product title longer than 30 chars

            product_table_y = product_table_y + 5
            self.write_text(18, product_table_y, title)
            self.write_text(105, product_table_y, str(sku))
            self.write_text(125, product_table_y, str(quantity))
            self.write_text(140, product_table_y, str(price))
            self.write_text(165, product_table_y, str('%.2f' % float(product_total)))
            self.pdf.set_line_width(0.3)

            product_table_y = product_table_y + 2
            self.pdf.line(15, product_table_y, 195, product_table_y)

        if last_page:  # if the the page we're currently writing to is the last page, then..
            # draw total amount cell
            self.pdf.set_xy(140, 260)
            self.pdf.cell(55, 15, '', border=1)

            # draw total amount value
            self.pdf.set_font('Arial', 'B', 22)
            self.write_text(145, self.invoice_detail_summary_line, 'R' + str('%.2f' % float(total)))

        self.pdf.set_font('Arial', 'B', 10)
        self.write_text(self.margin_left, self.invoice_detail_summary_line, f'Page {current_page_index + 1} of {page_total}')

    def write_notes(self):
        if len(self.data.get('notes')) > 0:
            """ Creates the last page and adds notes """
            self.pdf.add_page()

            self.pdf.set_font('Arial', 'B', 14)
            self.invoice_deatil_notes_line = 18
            self.write_text(self.margin_left, self.invoice_deatil_notes_line, 'Notes:')

            self.pdf.set_line_width(0.5)
            self.invoice_deatil_notes_line = self.invoice_deatil_notes_line + 2
            self.pdf.set_font('Arial', size=8)

            for note in self.data.get('notes'):
                self.pdf.set_xy(self.margin_left, self.invoice_deatil_notes_line)
                self.pdf.multi_cell(w=100, h=5, border=1, txt=note)

    def write_text(self, x, y, text):
        """ A function to write text to some coordinates on a page of the invoice """
        self.pdf.text(x, y, text)

    def output(self, filename):
        """ A function to save the file locally with the passed filename """
        self.pdf.output(filename, 'F')