Link to video: https://youtu.be/5Xjh2PQf3XY

SpeedReader is a program that extracts the most important information from a text (either in PDF or .txt form) based on user input and presents that information as a text file. Users can select which lines to be included in that output file, and can also specify if they want lines with certain keywords included as well. In this page, I'll go over exactly how to navigate and execute my program, and I'll also note some limitations in the backend of the design. 

First, my code uses an outside program to take an uploaded PDF and convert it to text. So, to be able to work with a PDF, you'll need to install some programs by typing the following in your terminal:

pip install pdfminer
pip install pdfminer.six

(You shouldn't need both, but just in case, it's good to have both as I've worked with both)

If all else fails: either contact me or comment out the imports related to pdfminer AND the entire "if 'pdf' in filename" section - the code should then still work with text files. 

From there, my program is designed around the Flask structure, so to launch my website, type 'Flask Run' into your terminal and click on the link you are presented with. Once the website is loaded, use the following steps to test my program:

1) Upload a PDF or Text File

Feel free to use the ones I provided you in the "DOWLOAD THESE FOR TESTING" folder, or use your own. Click on the "Choose File" button to select a file from your computer and upload that. Don't click submit yet! 

Of note: my program checks to see that '.pdf' or '.txt' are in the file name - though this is something that would be great to do in the future, it cannot *guarantee* that you are uploading a text or pdf file. In theory, you could upload a file named file.pdf.jpeg and the system would accept it - but don't do that. 

Also of note (VERY IMPORTANT): there are so many ways to create and encode a PDF - depending on the processor used to generate a PDF, there will be certain differences in formatting and back-end coding. This unfortunately affects how the program I imported reads the PDF, meaning some lines may appear out of order or with extra spaces, and these weird ways of reading occured with *every* outside program I tried. The important thing: my algorithm should work as intended either way, but because the initial file that it is working with might have some formatting issues, the results might be wonky unless you use a very simplified PDF like the one I provided. In any case, the focus of my project is my algorithm, and I just used an outside program to be able to accept PDFs as well. 

Finally: here's a good error to trigger! Upload a file without .pdf or .txt in its name (i.e. an image) and you'll be directed to an error page that will prompt you to reupload a file. This is intentional!

2) Select Which Lines to Include

Using the checkboxes beneath the Upload button, choose which lines from the original text you want included in the output file.

-> "Include First Line of Paragraphs" includes everything up to the first punctuation mark in each paragraph

-> "Include Last Line of Paragraphs" includes everything between the last two punctuation marks on each page. 

-> "Include the following keywords" includes any lines that include any of the keywords inputted in the box below, each separated by commas

3) Hit the "Submit" button

Note: the first time you run the Flask program, you'll see the word "processing" show up but the system may stall indefinitely. This doesn't mean the program isn't working, but usually I've found restarting the page or rebooting Flask tends to help. After this, you'll be redirected to a /success page with a button that says "Click here to download file!".

4) Click "Click here to download file!"

This will download a .txt file with all of your expected content to your device! When you open it up, see if your system offers an option like "Word Wrap" so that really long lines show up as multiple connected lines (as opposed to one line that extends beyond the page) for easier readability. 

5) You're all set! Compare your original file with the one my program provided you to check for accuracy. Certainly, there are certain things that won't work perfectly - I haven't accounted for all possible abbreviations, for instance, and it's possible my program will process certain text weirdly, but hopefully for the large part it will behave smoothly! 