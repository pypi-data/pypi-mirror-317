import os

import pandas as pd
import glob
from fpdf import FPDF
from pathlib import Path


def generate(invoices_path, pdfs_path, image_path,
             product_id, product_name, amount_purchased,
             price_per_unit, total_price):

    """
    This function converts Excel files into pdf invoices
    :param invoices_path:
    :param pdfs_path:
    :param image_path:
    :param product_id:
    :param product_name:
    :param amount_purchased:
    :param price_per_unit:
    :param total_price:
    :return:
    """

    invoices_folder = glob.glob(f"{invoices_path}/*.xlsx")

    for invoice_file in invoices_folder:
        invoice_df = pd.read_excel(invoice_file, sheet_name="Sheet 1")
        filename = Path(invoice_file).stem
        invoice_number, invoice_date = filename.split("-")

        pdf = FPDF(orientation="P", unit="mm", format="letter")
        pdf.add_page()
        pdf.set_font(family="Arial", style="B", size=16)
        pdf.cell(w=0, h=8, txt=f"Invoice Number: {invoice_number}", align="L", ln=1, border=0)
        pdf.cell(w=0, h=8, txt=f"Date: {invoice_date}", align="L", ln=1, border=0)

        # add a bit of space before table
        pdf.ln(10)

        # set header
        columns = invoice_df.columns
        columns = [item.replace("_", " ").title() for item in columns]

        pdf.set_font(family="Arial", style="B", size=12)
        pdf.cell(w=30, h=8, txt=columns[0], align="L", border=1)
        pdf.cell(w=70, h=8, txt=columns[1], align="L", border=1)
        pdf.cell(w=42, h=8, txt=columns[2], align="C", border=1)
        pdf.cell(w=32, h=8, txt=columns[3], align="C", border=1)
        pdf.cell(w=25, h=8, txt=columns[4], align="C", ln=1, border=1)

        # set table content style
        pdf.set_font(family="Arial", size=12)

        total_amount = 0
        # print table contents from file
        for index, row in invoice_df.iterrows():
            pdf.cell(w=30, h=6, txt=f"{row[product_id]}", align="L", border=1)
            pdf.cell(w=70, h=6, txt=f"{row[product_name]}", align="L", border=1)
            pdf.cell(w=42, h=6, txt=f"{row[amount_purchased]}", align="R", border=1)
            pdf.cell(w=32, h=6, txt=f"$ {row[price_per_unit]:.2f}", align="R", border=1)
            pdf.cell(w=25, h=6, txt=f"$ {row[total_price]:.2f}", align="R", ln=1, border=1)

        # add total to the bottom of the table
        total_amount = invoice_df["total_price"].sum()
        pdf.cell(w=30, h=6, txt="", align="L", border=1)
        pdf.cell(w=70, h=6, txt="", align="L", border=1)
        pdf.cell(w=42, h=6, txt="", align="R", border=1)
        pdf.cell(w=32, h=6, txt="", align="R", border=1)
        pdf.cell(w=25, h=6, txt=f"$ {total_amount:.2f}", align="R", ln=1, border=1)

        # add a line after the table with the total amount
        pdf.ln(10)
        pdf.cell(w=0, h=8, txt=f"The total amount is: ${total_amount:.2f} CAD", align="L", ln=1, border=0)

        # add the image
        pdf.set_font(family="Arial", size=14, style="B")
        pdf.cell(w=0, h=12, txt="Company", align="L", border=0)
        pdf.image(name=image_path, x=38, y=None, w=12)

        # generate the individual invoice pdf
        if not os.path.exists(pdfs_path):
            os.makedirs(pdfs_path)
        pdf.output(f"{pdfs_path}/invoice_{invoice_number}.pdf")