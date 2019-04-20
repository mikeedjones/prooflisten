

"""Prooflistening using Google Cloud Text-To-Speech API.

Example usage:
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = <credentials file> #first set your application credentials
    
    python prooflisten.py <folder with tex file in it> <tex file name>
"""

import time
import subprocess
import sys
import multiprocessing as mp
import os

#uses the opendetex (https://github.com/pkubowicz/opendetex) to extract the text from a tex file.
def extract_from_tex(folder,fname, save=False):
    if '.tex' in fname: fname=fname[:-4] #strips '.tex' from the input file name if present as it is not wanted by detex
    
    p=subprocess.run(["/usr/local/bin/detex",fname],cwd=folder,stdout=subprocess.PIPE,universal_newlines=True)
    text=p.stdout
    
    if save:
        fout=open(fname+".txt","w")
        fout.write(text)
    else:
        return text

#reads the text file and turns it into voice clips
def read_sections(text, outdir='audio'):
    sections=text.split('\n\n') #split text into paragraphs
    sections = list(filter(None, sections))
    
    #calculates the total length of all the text
    textlen=0
    for sec in sections: textlen+=len(sec)
    
    #creates the directory the audio files will be saved to 
    try:
        os.mkdir(outdir)
        print("Directory " , outdir ,  " Created ") 
    except FileExistsError:
        print("Directory " , outdir ,  " already exists")
    
    #group sections into ~140,000 character batches, one of which can be processed per minuite
    N=0
    i=0
    char_per_min=140000
    pr_per_min=150
    batches=[]  
    
    while N<textlen:
        n=0
        index_batch_start=i
        while n < char_per_min and i-index_batch_start < pr_per_min:
            n+=len(sections[i])
            i+=1
            if i >= len(sections): break
        index_batch_end=i-1
        batches.append(slice(index_batch_start,index_batch_end,1))
        N+=n
    
    #processes the text in batches. Running sequentially is much slower.
    for batch in batches:
        processes = [mp.Process(target=read_batch, args=(sections,sec)) for sec in sections[batch]]
        for p in processes: p.start()
        if batch != batches[-1]: time.sleep(60) #maximum 150,000 character per minuite limit API calls

def read_batch(sections, sec,outdir='audio'):
    p_index=sections.index(sec)
    if len(sec)<5000: #there is a 5000-character limit on each call to the text to speech API. 5000 chars is ~800 words.
        read_text(sec,outname=outdir+'/paragraph {0}'.format(p_index))
    else: print("This section ({0:}) is too long.".format(p_index))


def read_text(text,outname='output'):

    from google.cloud import texttospeech

    # Instantiates a client
    client = texttospeech.TextToSpeechClient()

    # Set the text input to be synthesized
    synthesis_input = texttospeech.types.SynthesisInput(text=text)

    # Build the voice request, select the language code ("en-GB")
    voice = texttospeech.types.VoiceSelectionParams(
        language_code='en-GB',
        name='en-GB-Wavenet-B')
    # Select the type of audio file you want returned
    audio_config = texttospeech.types.AudioConfig(
        audio_encoding=texttospeech.enums.AudioEncoding.MP3)

    # Perform the text-to-speech request on the text input with the selected
    # voice parameters and audio file type
    response = client.synthesize_speech(synthesis_input, voice, audio_config)

    # The response's audio_content is binary.
    with open(outname+'.mp3', 'wb') as out:
        # Write the response to the output file.
        out.write(response.audio_content)
        print('Audio content written to file "'+outname+'.mp3"')
    # [END tts_quickstart]

if __name__ == '__main__':
    folder=sys.argv[1]
    fname=sys.argv[2]
    read_sections(extract_from_tex(folder,fname))