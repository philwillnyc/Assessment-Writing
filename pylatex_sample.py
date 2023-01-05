from pylatex import Document



if __name__ == '__main__':
    # Basic document
    doc = Document('basic', documentclass = 'standalone',)
    #fill_document(doc)
    doc.append('text \\undefinedcontrol')
    doc.generate_pdf(clean_tex=False,)
    doc.generate_tex()

    