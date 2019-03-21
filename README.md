# prooflisten
A python program which uses Google’s cloud speech-to-text software to convert text extracted from a .tex file into a series of audio clips. Originally built to assist in proof-reading my thesis. I found it very useful, and have a few more details and some comparison clips on my [blog](https://michaeledjones.tumblr.com/post/183380727169/proof-listening).

# Installation
To use the code you'll have to set yourself up with the google-cloud API. You can find an excellent quickstart guide [here](https://cloud.google.com/text-to-speech/docs/quickstart-client-libraries).

You can set the credential enviroment variables in an iPython console using `os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = <credentials file>`

You'll also need to install [opendetex](https://github.com/pkubowicz/opendetex). I found the default detex program found in the tex installation loses a lot of the content from a tex file - equations, captions etc. Opendetex is much better. Opendetex and detex both follow \include commands.

# Useage

`python prooflisten.py <folder with tex file in it> <tex file name>`
 
Google's cloud text-to-speech is [priced](https://cloud.google.com/text-to-speech/pricing) depending on the voice used. Higher quality voices are more expensive. You get a million characters (~160k words) a month for free and it's $16 per million characters after that.
