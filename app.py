from flask import Flask, render_template, request, redirect
import os
import io
import re
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def upload():
    
    # Provide user with form to upload a file
    return render_template("homepage.html")
        
@app.route("/success", methods=["GET", "POST"])
def success():        
    
    # Avoid showing user download button if they haven't submitted form
    if request.method == "GET":
        return redirect("/")

    else:

        # Save user's file in system
        f = request.files['original']  
        f.save(f.filename)

        # If improper file uploaded, display error page
        if ('.pdf' not in f.filename) and ('.txt' not in f.filename):
            os.remove(f.filename)
            return render_template("error.html")

        # If a PDF is uploaded, convert it to text
        if '.pdf' in f.filename:

            # Convert uploaded PDF file to a text string
            def convert(fname, pages=None): 
                
                # Calculate number of pages in PDF
                if not pages:
                    pagenums = set()
                else:
                    pagenums = set(pages)

                # Define processors
                output = io.StringIO()
                manager = PDFResourceManager()
                converter = TextConverter(manager, output, laparams=LAParams())
                interpreter = PDFPageInterpreter(manager, converter)

                # Extract text from each PDF page
                infile = open(fname, 'rb')
                for page in PDFPage.get_pages(infile, pagenums):
                    interpreter.process_page(page)
                    output.write("endofpage")
                infile.close()
                converter.close()
                text = output.getvalue()
                output.close
                return text

                # Function courtesy of https://stackoverflow.com/questions/55220455/convert-from-pdf-to-text-lines-and-words-are-broken

            # Run conversion function and extract text string
            text = convert(f.filename)
            text_ = str(text)

            # Eliminate extra spaces from page breaks (may not work with certain types of pdfs)
            text_ = re.sub("\n\n(.*?)endofpage", "", text_)

        # If a txt file is uploaded, read it to a string
        if '.txt' in f.filename: 
            file = open(f.filename)
            text_ = file.read()
            file.close()

            # Code courtesy of https://www.kite.com/python/answers/how-to-read-a-text-file-into-a-string-in-python  

        # Create an output text file
        output = open("static/output.txt", "w")

        # Read user's file into a dictionary, paragraph by paragraph
        input_ = text_.split('\n\n')

        # Print certain lines from every paragraph into output file
        for i in range(len(input_)):
            
            # Check sentence by sentence
            text_ = input_[i]

            # Fix for when extra line breaks would show up
            text_ = text_.replace("\n"," ")

            # Replace punctuation marks that wouldn't work in algorithm
            text = text_.replace("!",".").replace("?",".").replace("Mr.", "Mr").replace("Mrs.", "Mrs").replace("Ms.", "Ms").replace("Dr.", "Dr").replace("Jr.", "Jr")
            
            # Split each paragraph sentence by sentence, ignoring periods that behave like decimal points
            text = re.sub(r'[.](?=[^\s])', 'donotsplithere!!!', text)
            list = text.lstrip().rstrip().split(".")
            for l in range(len(list)):
                list[l] = re.sub('donotsplithere!!!', '.', list[l])
                # Fix for extra spaces showing up
                list[l] = re.sub('  ', ' ', list[l])
            
            # If user checked corresponding HTML box, print first line in each paragraph
            if request.form.get("cb1"):
                output.write(str(list[0] + "\n\n").lstrip())
            
            # If user checked corresponding HTML box, print any lines with provided keywords
            if request.form.get("cb3"):
                for j in range(len(list)):
                    counter = 0
                    keywords = str(request.form.get("keywords"))
                    
                    # Create a dictionary with all keywords provided 
                    keyword = keywords.split(",")
                    
                    # Check if each keyword is in each sentence; if so, print that sentence only once
                    for k in range(len(keyword)):
                        if str(keyword[k]).lower().lstrip().rstrip() in str(list[j]).lower().lstrip().rstrip():
                            if (not ((int(j) == 0 and request.form.get("cb1")) or (int(j) == len(list) - 1 and request.form.get("cb2")))):
                                if counter == 0:
                                    output.write(str(list[j] + "\n\n").lstrip())
                                    counter += 1

            # If user checked corresponding HTML box, print last line in each paragraph (could be first line if only one line - no duplicates)
            if request.form.get("cb2"):
                if (not request.form.get("cb1")) or len(list) > 2:
                    output.write(str(list[len(list) - 2] + "\n\n").lstrip())
        
        # Remove original file from the system
        os.remove(f.filename)

        # Close output file
        output.close()
        
        # Present user with page that includes a 'download file' button
        return render_template("success.html")

@app.route("/error", methods=["GET"])
def error():

    # Present user with page that includes an error message and allows for resubmitting
    return render_template("error.html")

# Help Received: Vincent Boersch-Supan, Eric Shen (Tutorial), Lawrence Zhang (Tutorial)
# Other sources consulted include Stack Overflow, W3Schools, GeeksforGeeks, and CS50's websites

    
    