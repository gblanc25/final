My project has two design components: the front end website and the back-end algorithm. Altogether, they make up a Flask framework that is run similar to Finance, albeit with major structural changes as detailed below. 

I'll discuss them separately here!

FRONT-END WEBSITE

I started out with some HTML / CSS integration to build the main body of my website. I knew I wanted to embed an image with some accessible text, include a header up top, and include opportunities for user uploading and customization. That took the form of an upload button of type "file" that opens a user's file library and, via the accept attribute, specifically presents only .txt and .pdf options. That button, along with three textboxes and an input text box (with a placeholder to inform about comma usage), comprised all one form that could be submitted at once via a submit button. Doing so allows me to easily reference all submitted contents under the same form id in my Python code. Of note - the file upload is required, but none of the checkboxes are; if none are selected, the user would receive a blank page. 

I also used CSS attributes to add background colors, align all text to the center, resize my image (and ensure it's compatible on mobile devices too), and select a specific font (Tahoma) to be used for most of the content on my website. 

From there, I knew I wanted some dynamic elements on my website to appear. For instance, once a user submitted the form, I wanted the word "processing" to appear while my program ran, since especially with larger files the runtime could be longer. I implemented that via JavaScript code that listens for a submission of the form and subsequently removes the "hidden" attribute from that line of text. 

I also wanted the "download file" button to only occur after the form was submitted, so I decided to create a separate page (success.html) that the user would be redirected to ONLY via "post" methods, aka after submitting the form (for security purposes - we wouldn't want users to be able to download the previous contents of the text file that's stored in the system). There, I used a simple link traced to my output.txt file in my static folder, making it easy for the user to download their output file. I employed a similar method with an "Error" page (error.html), where if a user uploads a file that is not a PDF or a text file, they would be redirected to a page with an error message up top. 

Even for the Error and Success pages, I still wanted the form to submit a file to be accessible, so I used Jinja methods to create a default layout in layout.html and then extend that to all other pages, with certain main blocks inserted to allow for changes like the error or download messages. 

BACK-END ALGORITHM

Most of my new learning related to this final project took place with learning methods of reading and modifying files in Python (similar but more complicated than we had done in C), and then also working to correct errors that occurred during reading, such that via postprocessing I could make the text file I'm working with as close as possible to the original. Here, I'll walk through each major step of my main code, found in app.py. 

1) Present User With Appropriate Template

If a user is visiting the page for the first time, or if they refresh while on the Success page, they'll see the homepage html template via the "/" route, which will allow them to upload a file as usual. If they then submit an invalid file like a jpeg (via a file name that does not include the string '.pdf' or '.txt'), they'll be prompted by an error.html page with an error message but they'd still have the ability to submit the form on the same page. If they submit a valid file, they'll be prompted with a success.html page with a download link traced to the output.txt file discussed later, and they'll also still have the same form available to them to resubmit. 

2A) If a PDF is Uploaded

If the user uploads a PDF, I'll first save that PDF to my final project folder, which will allow me to directly reference it when reading from it later on. Then, I've added a third-party piece of code designed to draw upon the io and pdfminer libraries and read text from a pdf into a text string. As discussed in my README file, programs like these are not perfect, but since they rely on outside libraries some of those issues are largely out of my control - I just work to fix them later on in my code. 

The "convert" function encompasses that program: when a PDF file is passed into it, it returns one long text string (still broken by paragraphs), which is very useful for me since I can later read through that string all at once later on. 

2B) If a TXT File is Uploaded

This is what I started with when I was originally writing my code. TXT files are much easier and much more consistent to work with, and I only added PDF readability afterwards since most assigned reading would come in PDF form. Here, we simply save the file as in 2A and then use the read() function in Python to extract the text into a text string (by the same name as if it were a PDF).

At that point, no matter what type of file was uploaded, I had one text string by the same variable name to work with, so all of my following code could remain the same for either file type. Similarly, I was able to open an output.txt file in writing mode that would accept input from either file type too. 

3) Break Apart Text and Fix Annoying Errors

Every paragraph in a text file is followed by two newlines ('\n\n'), so since so much of my project focuses on working paragraph by paragraph, I used the split function to read the text into a dictionary broken apart after every two newlines, where each index in the dictionary is a different paragraph. 

Then, I used one overarching For loop to work through the text paragraph by paragraph. As I mentioned earlier, PDF readers can do some weird things, so I tried correcting as many of those errors as possible: for instance, I used a replace function to take any single lines that were split in two and join them together. I then also used replace functions to accommodate words and phrases that needed to have a period in them and that were not, of course, the end of a sentence. Since the rest of my algorithm depended on splitting each paragraph into individual sentences by periods, these steps helped prevent unecessary splits. I also replaced other punctuation marks, like ! or ? with periods so that they *would* be split there. 

One other issue I was encountering was that when a multi-page PDF was being read, there would be excessive breaks between text on one page and another, which would lead my program to treat them as two separate paragraphs. I fixed this by adding the keyword "donotsplithere!!!" in the initial PDF->text stage and then replacing any space between a new line and that keyword using a regular expression and a replace function.  This was necessary ONLY within a paragraph, not between multiple, which is why it's under the For loop. This may not always work, though, so it's possible large breaks may occur, unfortunately. 

4) Depending on User Input, Write to Output File

If the user checked the box to include the first sentence in each paragraph (checked via a request.form.get function), I would print the first index in each paragraph's dictionary. Later on, if the user checked the box to include the last sentence in each paragraph, I would print the last index in each paragraph's dictionary, SO LONG as the last line wasn't also the first line (which I found using a len(list) function, list being a dictionary holding individual sentences) UNLESS the first line wasn't printed. 

Then came the tricky part: I allowed users to input multiple keywords in the text box in the homepage, so long as they were separated by commas. I then split that text input into a dictionary where each index held one keyword, using a split function with a comma as its argument. After that, for each keyword, I checked if it was present (case-insensitive) in each sentence in the paragraph. 

If it was, I printed the sentence it was found in ONLY if:
-> It was in the first line AND the user didn't want all first lines printed 
-> It was in the last line AND the user didn't want all last lines printed
-> It was between the first and last lines AND that line hadn't already been printed due to the presence of another keyword

I kept track of that last bullet via a counter variable within the nested For loops that checked for each sentence; after a sentence with a keyword was printed, its counter increased by 1; if the second For loop ran a second time due to more keywords and another keyword was found in that same sentence, that sentence wouldn't print because the counter was no longer 0. The counter resets for each new sentence. 

5) Present User With Output File

At this point, the output file contains all necessary content, as was added in Step 4! So we can close it using a close function, and then also remove the original PDF or TXT file from the system via an os.remove function so that we don't have a bunch of files taking up storage. 

Then, as mentioned above, the user would be presented with the Success page and have the ability to download the completed output.txt file!





