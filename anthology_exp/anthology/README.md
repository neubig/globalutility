

You can use the `download_anth.py` to download the PDFs from the anthology, which are stored in the `pdfs` directory. 

The same script then calls `pdftotext` (which can be installed with pip) to convert the PDF to a txt file with the same name, stored under the `text` directory.

Also, a minimal example of converting a pdf to txt file is the `convert_pdf_to_text.py`, which can be run with `convert_pdf_to_text.py < input.pdf > output.txt`.