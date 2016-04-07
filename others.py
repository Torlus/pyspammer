import csv
import sys
import re
from fpdf import FPDF

repc = re.compile('\\d{5}')
emails = []

pdffile = re.sub('csv$', 'pdf', sys.argv[1])
txtfile = re.sub('csv$', 'txt', sys.argv[1])

pdf = FPDF('P', 'mm', 'A4')

# Borders, for debug
b = 0

with open(sys.argv[1], encoding='Windows-1252') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=';')
    for row in csvreader:
        catg = row[0].strip()
        name = row[1].strip()
        moar = row[2].strip()
        addr = row[3].strip()
        mail = row[4].strip()
        if len(catg) == 1 and catg[0] == '#':
            continue
        if len(name) == 0:
            continue
        if len(addr) + len(mail) == 0:
            print('Discarding [' + (';'.join(row)) + ']: neither e-mail nor snail-mail address', file=sys.stderr)
            continue
        if len(mail) > 0 and '@' not in mail:
            print('Discarding [' + (';'.join(row)) + ']: incorrect e-mail', file=sys.stderr)
            continue
        if len(mail) > 0:
            emails.append(mail)
            continue
        if not repc.search(addr):
            print('Discarding [' + (';'.join(row)) + ']: incorrect postal code', file=sys.stderr)
            continue
        pdf.add_page()
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(190, 5, 'Association France Parkinson', b, 1)
        pdf.set_font('Arial', '', 12)
        pdf.cell(190, 5, 'Comité de Haute-Garonne', b, 1)
        pdf.set_font('Times', '', 11)

        pdf.cell(190, 25, '', b, 1)

        pdf.cell(90, 5, '', b, 0)
        pdf.cell(100, 5, name, b, 1)
        third = 45
        if len(moar) > 0:
            pdf.cell(90, 5, '', b, 0)
            pdf.cell(100, 5, moar, b, 1)
            third -= 5
        lines = addr.split('#')
        for ln in lines:
            pdf.cell(90, 5, '', b, 0)
            pdf.cell(100, 5, ln.strip(), b, 1)
            third -= 5
        while third > 0:
            pdf.cell(1, 5, '', b, 1)
            third -= 5
        pdf.cell(190, 0, '', 1, 1)
        pdf.cell(1, 10, '', b, 1)

        with open(txtfile, encoding='latin1') as text:
            for line in text.readlines():
                line = line.strip()
                if len(line) >= 1 and line[0] == ':':
                    pdf.set_font('Arial', 'B', 20)
                    pdf.cell(190, 10, line[1:], 0, 1, 'C')
                else:
                    pdf.set_font('Arial', '', 12)
                    pdf.cell(190, 5, line, 0, 1)

pdf.output(pdffile)

print(', '.join(emails), file=sys.stdout)
