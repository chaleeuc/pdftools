import os
from PyPDF2 import PdfFileReader, PdfFileWriter, PdfFileMerger

# author = 'Changho Lee'
# email  = 'chaleeuc@gmail.com'

def index(operation):
    if operation == 'export':
        export()
        return False

    if operation == 'split':
        split()
        return False

    elif operation == 'merge':
        merge()
        return False

    elif operation == 'quit':
        return True

def export():
    files_list()

    doc_name = get_doc()

    pdf = PdfFileReader(open(doc_name, 'rb'))

    num_pages = pdf.getNumPages()
    print('\n' + 'pdf file has %d page(s)\n' %num_pages)

    exports = get_pages(num_pages)

    pdf_writer = PdfFileWriter()
    for page in exports:
        pdf_writer.addPage(pdf.getPage(page-1))

    doc_out = doc_name[:len(doc_name)-4] + str(exports) + '.pdf'
    with open(doc_out, 'wb') as out:
        pdf_writer.write(out)

    return print(f'\ncreated %s file\n' %doc_out)

def split():
    files_list()

    doc_name = get_doc()

    pdf = PdfFileReader(open(doc_name, 'rb'))

    num_pages = pdf.getNumPages()
    print('\n' + 'pdf file has %d page(s)\n' %num_pages)

    for page in range(num_pages):
        pdf_writer = PdfFileWriter()
        pdf_writer.addPage(pdf.getPage(page))
        doc_out = doc_name[:len(doc_name)-4] + '_page_' + str(page + 1) + '.pdf'
        with open(doc_out, 'wb') as out:
            pdf_writer.write(out)

    return print(f'\ncreated %d file(s)\n' %num_pages)

def merge():
    files_list()

    num_files = int(input('enter number of files to be merged: '))
    files = get_files(num_files)

    pdf_merger = PdfFileMerger()

    for f in files:
        pdf = PdfFileReader(open(f, 'rb'))
        pdf_merger.append(pdf)

    doc_out = ''
    for file in files:
        doc_out += file[:len(f)-4] + '_'

    doc_out += '.pdf'

    with open(doc_out, 'wb') as out:
        pdf_merger.write(out)

    return print(f'\nmerged %d files\n' %num_files)

# quick checks to make sure all files exist
def get_files(num_files):

    files = []
    while len(files) < num_files:
        file = get_doc()    
        files.append(file)

    return files

def get_doc():
    # quick check if document exists
    valid_file = False
    while not valid_file:
        doc_name = input('enter a document: ') 
        if os.path.isfile(doc_name):
            valid_file = True
        else:
            print('the document does not exist')

    return doc_name

def get_pages(num_pages):
    # no input check, assumes user follows e.g.
    pages = input('enter page(s) to be exported\ne.g. 2-6, 9, 12-16: ')

    # parse user input
    exported_pages = []
    for page in pages.split(', '):
        if '-' in page:
            for p in range(int(page.split('-')[0]), int(page.split('-')[1]) + 1):
                exported_pages.append(p)

        else:
            exported_pages.append(int(page))

    return exported_pages

def files_list():
    pdf_files = []
    for file in os.listdir():
        if file.endswith(".pdf"):
            pdf_files.append(file)

    return print('pdf file(s) availble: ' + str(pdf_files) + '\n')


def main():
    print(
        "\nUSAGE:\texport: Exports user specified pages of a single pdf into another pdf file\n"
        "\tsplit:\tSplit single pdf file into multiple pdf files\n"
        "\tmerge:\tMerge multiple pdf file into single pdf file\n"
        "\tquit:\tQuit program\n"
        )

    quit = False
    while not quit:
        operation = input('choose operation: export, split, merge, quit\n')
        quit = index(operation)

main()