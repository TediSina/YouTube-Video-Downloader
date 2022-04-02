from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from pytube import *
from pytube import YouTube
import os
import ffmpeg
import threading

def submitUrl():
    urlOutput.config(text="")
    global url
    url = urlEntryVar.get()
    print(f"Url: {url}")

    qualityTextLabel.grid_remove()

    qualityCombobox.grid_remove()

    qualitySubmitButton.grid_remove()

    qualityOutput.grid_remove()
    qualityOutput.config(text="")

    saveTextLabel.grid_remove()

    saveButton.grid_remove()

    saveOutput.grid_remove()
    saveOutput.config(text="")

    filenameTextLabel.grid_remove()

    filenameEntry.grid_remove()

    filenameSubmitButton.grid_remove()

    filenameOutput.grid_remove()
    filenameOutput.config(text="")

    downloadInfo.grid_remove()

    downloadButton.grid_remove()

    downloadProgressBar.grid_remove()

    downloadOutput.grid_remove()
    downloadOutput.config(text="")

    openLocation.savePath = None

    try:
        submitUrl.yt = YouTube(url)
        submitUrl.yt.register_on_progress_callback(on_progress)
        submitUrl.yt.streams.first()
    except exceptions.RegexMatchError as e:
        urlOutput.config(text="Please enter a valid YouTube video link.", font=("Arial", 10))
        print(e)
    except exceptions.VideoUnavailable as e:
        urlOutput.config(text="Please enter a valid YouTube video link.", font=("Arial", 10))
        print(e)
    except Exception as e:
        urlOutput.config(text="An error occured while submitting the URL. The link may not be valid or there are no streams available.", font=("Arial", 8))
        print(e)
    else:
        global qualityChoices
        highestQuality = submitUrl.yt.streams.filter(progressive=False).order_by("resolution").last()
        print(highestQuality)

        qualityTextLabel.grid(row=4, pady=5)

        if highestQuality.resolution == "4320p":
            qualityChoices = ["4320p", "2160p", "1440p", "1080p", "720p", "480p", "360p", "240p", "144p", "Audio only"]
        elif highestQuality.resolution == "2160p":
            qualityChoices = ["2160p", "1440p", "1080p", "720p", "480p", "360p", "240p", "144p", "Audio only"]
        elif highestQuality.resolution == "1440p":
            qualityChoices = ["1440p", "1080p", "720p", "480p", "360p", "240p", "144p", "Audio only"]
        elif highestQuality.resolution == "1080p":
            qualityChoices = ["1080p", "720p", "480p", "360p", "240p", "144p", "Audio only"]
        elif highestQuality.resolution == "720p":
            qualityChoices = ["720p", "480p", "360p", "240p", "144p", "Audio only"]
        elif highestQuality.resolution == "480p":
            qualityChoices = ["480p", "360p", "240p", "144p", "Audio only"]
        elif highestQuality.resolution == "360p":
            qualityChoices = ["360p", "240p", "144p", "Audio only"]
        elif highestQuality.resolution == "240p":
            qualityChoices = ["240p", "144p", "Audio only"]
        elif highestQuality.resolution == "144p":
            qualityChoices = ["144p", "Audio only"]

        qualityCombobox.config(values=qualityChoices)
        qualityCombobox.grid(row=5, pady=5)

        qualitySubmitButton.grid(row=6, pady=5)

        qualityOutput.grid(row=7, pady=5)

        saveTextLabel.grid(row=8, pady=5)

        saveButton.grid(row=9, pady=5)

        saveOutput.grid(row=10 , pady=5)

        filenameTextLabel.grid(row=11, pady=5)

        filenameEntry.grid(row=12, pady=5)

        filenameSubmitButton.grid(row=13, pady=5)

        filenameOutput.grid(row=14, pady=5)

        downloadInfo.grid(row=15, pady=5)

        downloadButton.grid(row=16, pady=5)

        downloadProgressBar.grid(row=17, pady=5)

        downloadOutput.grid(row=18, pady=5)

def submitQuality():
    qualityOutput.config(text="")
    if qualityVar.get() != "":
        print(qualityVar.get())
        if qualityVar.get() == "Audio only":
            submitQuality.selected_stream = submitUrl.yt.streams.filter(progressive=False, only_audio=True).first()
        else:
            submitQuality.selected_stream = submitUrl.yt.streams.filter(progressive=False, res=qualityVar.get()).first()
        print(submitQuality.selected_stream)
        qualityOutput.config(text=f"Quality setting submitted successfully: {qualityVar.get()}.", fg="green")
    else:
        qualityOutput.config(text="Please choose a quality setting.", fg="red")

def openLocation():
    saveOutput.config(text="")
    openLocation.savePath = filedialog.askdirectory()
    saveOutput.config(text=openLocation.savePath, fg="green")

def submitFilename():
    filenameOutput.config(text="")
    submitFilename.chosenFilename = filenameEntryVar.get()
    filenameOutput.config(text="Filename submitted successfully!", fg="green")

def on_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining 
    percentage_of_completion = bytes_downloaded / total_size * 100

    if qualityVar.get() == "Audio only":
        downloadOutput.config(text=f"Downloading the audio... ({bytes_downloaded / 1024 / 1024} MB/{total_size / 1024 / 1024} MB, {percentage_of_completion}%)")
    else:
        downloadOutput.config(text=f"Downloading the video... ({bytes_downloaded / 1024 / 1024} MB/{total_size / 1024 / 1024} MB, {percentage_of_completion}%)")
    
    downloadProgressBar['value'] = percentage_of_completion
    downloadOutput.update_idletasks()
    downloadProgressBar.update_idletasks()

def on_progress_audio(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining 
    percentage_of_completion = bytes_downloaded / total_size * 100

    downloadOutput.config(text=f"Downloading the audio... ({bytes_downloaded / 1024 / 1024} MB/{total_size / 1024 / 1024} MB, {percentage_of_completion}%)")    
    downloadProgressBar['value'] = percentage_of_completion
    downloadOutput.update_idletasks()
    downloadProgressBar.update_idletasks()

def downloadVideo():
    if openLocation.savePath != None:
        if qualityVar.get() == "720p" or qualityVar.get() == "360p":
            try:
                downloadOutput.config(text="Downloading the video...", fg="red", font=("Arial", 10))
                submitQuality.selected_stream.download(openLocation.savePath, submitFilename.chosenFilename + ".mp4")
            except Exception as e:
                downloadOutput.config(text="An error occured while trying to download the video and audio. Please make sure that\nthe device is connected to the internet and to have selected a quality and\na valid path to save the video.", fg="red", font=("Arial", 10))
                print(e)
                downloadProgressBar.stop()
            else:
                downloadOutput.config(text="Download completed successfully.", fg="green", font=("Arial", 10))
                downloadProgressBar.stop()
        elif qualityVar.get() == "144p":
            try:
                downloadOutput.config(text="Downloading the video...", fg="red", font=("Arial", 10))
                submitQuality.selected_stream.download(openLocation.savePath, submitFilename.chosenFilename + ".3gpp")
            except Exception as e:
                downloadOutput.config(text="An error occured while trying to download the video and audio. Please make sure that\nthe device is connected to the internet and to have selected a quality and\na valid path to save the video.", fg="red", font=("Arial", 10))
                print(e)
                downloadProgressBar.stop()
            else:
                downloadOutput.config(text="Download completed successfully.", fg="green", font=("Arial", 10))
                downloadProgressBar.stop()
        elif qualityVar.get() == "Audio only":
            try:
                downloadOutput.config(text="Downloading the audio in mp4 format...", fg="red", font=("Arial", 10))
                submitQuality.selected_stream.download(openLocation.savePath, submitFilename.chosenFilename + "tempmp4AudFile.mp4")
            except Exception as e:
                downloadOutput.config(text="An error occured while trying to download the video and audio. Please make sure that\nthe device is connected to the internet and to have selected a quality and\na valid path to save the video.", fg="red", font=("Arial", 10))
                print(e)
                downloadProgressBar.stop()
            else:
                downloadProgressBar.stop()
                try:
                    mp4_file = openLocation.savePath + "/" + submitFilename.chosenFilename + "tempmp4AudFile.mp4"
                    mp3_file = openLocation.savePath + "/" + submitFilename.chosenFilename + ".mp3"
                    input_audio = ffmpeg.input(mp4_file)
                    stream = ffmpeg.output(input_audio, mp3_file, f="mp3")
                    downloadOutput.config(text="Converting the audio from mp4 to mp3...", fg="red", font=("Arial", 10))
                    ffmpeg.run(stream)
                except Exception as e:
                    downloadOutput.config(text="An error occured while trying to convert the audio from mp4 to mp3.", fg="red", font=("Arial", 10))
                    print(e)
                    downloadProgressBar.stop()
                else:
                    downloadOutput.config(text="Download completed successfully.", fg="green", font=("Arial", 10))
                    downloadProgressBar.stop()
                os.remove(mp4_file)
        else:
            try:
                downloadOutput.config(text="Downloading the video without audio...", fg="red", font=("Arial", 10))
                submitQuality.selected_stream.download(openLocation.savePath, submitFilename.chosenFilename + "tempVidFile.mp4")
                audio = YouTube(url)
                audio.register_on_progress_callback(on_progress_audio)
                download_audio = audio.streams.filter(progressive=False, only_audio=True).first()
                print(download_audio)
                downloadOutput.config(text="Downloading the audio...", fg="red", font=("Arial", 10))
                download_audio.download(openLocation.savePath, submitFilename.chosenFilename + "tempAudFileVid.mp4")
            except Exception as e:
                downloadOutput.config(text="An error occured while trying to download the video and audio. Please make sure that\nthe device is connected to the internet and to have selected a quality and\na valid path to save the video.", fg="red", font=("Arial", 10))
                print(e)
                downloadProgressBar.stop()
            else:
                try:
                    video_location = openLocation.savePath + "/" + submitFilename.chosenFilename + "tempVidFile.mp4"
                    audio_location = openLocation.savePath + "/" + submitFilename.chosenFilename + "tempAudFileVid.mp4"
                    input_video = ffmpeg.input(video_location)
                    input_audio = ffmpeg.input(audio_location)
                    stream = ffmpeg.concat(input_video, input_audio, v=1, a=1)
                    stream = ffmpeg.output(input_video, input_audio, openLocation.savePath + "/" + submitFilename.chosenFilename + ".mp4")
                    downloadOutput.config(text="Concatenating the video and audio...", fg="red", font=("Arial", 10))
                    ffmpeg.run(stream)
                except Exception as e:
                    downloadOutput.config(text="An error occured while trying to concatenate the video and audio.", font=("Arial", 10))
                    print(e)
                    downloadProgressBar.stop()
                else:
                    downloadOutput.config(text="Download completed successfully.", fg="green", font=("Arial", 10))
                    downloadProgressBar.stop()
                os.remove(video_location)
                os.remove(audio_location)
    else:
        downloadOutput.config(text="Please make sure to have selected a quality and a valid path to save the video.", fg="red", font=("Arial", 10))

root = Tk()
root.title("YouTube Video Downloader")
root.geometry("700x900")
root.columnconfigure(0, weight=1)

urlTextLabel = Label(root, text="Enter the URL of the YouTube video", font=("Arial", 15))
urlTextLabel.grid(row=0)

urlEntryVar = StringVar()
urlEntry = Entry(root, width=75, textvariable=urlEntryVar)
urlEntry.grid(row=1, pady=5)

urlSubmitButton = Button(root, text="Submit", width=10, bg="red", fg="white", command = lambda : threading.Thread(target=submitUrl).start())
urlSubmitButton.grid(row=2, pady=5)

urlOutput = Label(root, text="", fg="red", font=("Arial", 10))
urlOutput.grid(row=3, pady=5)

qualityTextLabel = Label(root, text="Select quality", font=("Arial", 15))

qualityVar = StringVar()
qualityChoices = []
qualityCombobox = ttk.Combobox(root, values=qualityChoices, textvariable=qualityVar)

qualitySubmitButton = Button(root, text="Submit", width=10, bg="red", fg="white", command = lambda : threading.Thread(target=submitQuality).start())

qualityOutput = Label(root, text="", font=("Arial", 15))

saveTextLabel = Label(root, text="Choose where to save the selected YouTube video.", font=("Arial", 15))

saveButton = Button(root, width=10, bg="red", fg="white", text="Choose path", command = lambda : threading.Thread(target=openLocation).start())

saveOutput = Label(root, text="", font=("Arial", 10))

filenameTextLabel = Label(root, text="""Enter the filename without the extension (A filename cannot contain \/:*?"<>|)""", font=("Arial", 15))

filenameEntryVar = StringVar()
filenameEntry = Entry(root, width=50, textvariable=filenameEntryVar)

filenameSubmitButton = Button(root, text="Submit", width=10, bg="red", fg="white", command = lambda : threading.Thread(target=submitFilename).start())

filenameOutput = Label(root, text="", font=("Arial", 15))

downloadInfo = Label(root, text="Audio Only files are downloaded in mp4, then converted to mp3.\n144p files are downloaded in 3gpp.\n720p and 360p files are downloaded in mp4.\nOther files are downloaded video only in mp4, then concatenated with an mp4 audio file\n(High CPU usage since it's encoding video).\nThe result is in mp4.", font=("Arial", 10))

downloadButton = Button(root, text="Download", width=10, bg="red", fg="white", command = lambda : threading.Thread(target=downloadVideo).start())

downloadProgressBar = ttk.Progressbar(root, orient="horizontal", mode="determinate", length=400)

downloadOutput = Label(root, text="", font=("Arial", 10))

root.mainloop()
