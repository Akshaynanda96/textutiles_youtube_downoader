from django.shortcuts import render ,redirect
from django.contrib import messages
from pytube import YouTube
from pytube.exceptions import VideoUnavailable
import os
from django.http import FileResponse

def index(request):
    return render(request, 'index.html')

    # return HttpResponse("Home")

def analyze(request):
    text_varbel  = request.POST.get('text','defult')
    check_box = request.POST.get('removepunc','off')
    upper = request.POST.get('fullcaps','off')
    extraspace = request.POST.get('extraspaceremover', 'off')
    Lineremover = request.POST.get('newlineremover', 'off')
    carcount = request.POST.get('carcount', 'off')

    if check_box == "on":
        convtor = ""
        punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
        if check_box == "on":
            for i in text_varbel:
                if i not in punctuations:
                    convtor = convtor + i
        param = {"hedaline_name" :"Magic in Action","analyze_text" :convtor  }
        return render(request, 'analyze.html', param)
    
    elif upper == "on":
        convert_to_up = ""
        for i in text_varbel:
            convert_to_up = convert_to_up + i.upper()
        param = {"hedaline_name" :"Perpoase to capitize","analyze_text" :convert_to_up  }
        return render(request, 'analyze.html', param)
    
    elif extraspace == "on":
        convert_to_up = ""
        for index, i in  enumerate(text_varbel):
            if not (text_varbel[index] ==" " and text_varbel[index+1] == " "):
                convert_to_up = convert_to_up + i
        param = {"hedaline_name" :"Remove all extra Space","analyze_text" :convert_to_up  }
        return render(request, 'analyze.html', param)

    elif Lineremover == "on":
        convert_to_up = ""
        for i in  text_varbel:
            if  i != "\n" and i != "\r":
                convert_to_up = convert_to_up + i
        param = {"hedaline_name" :"Extra lines is remove","analyze_text" :convert_to_up  }
        return render(request, 'analyze.html', param)
    
    elif carcount == "on":
        convert_to_up = ""
        count = 0
        for i in  text_varbel:
            if i == " " :
                continue
            convert_to_up = convert_to_up + i
            count += 1
        param = {"hedaline_name" :"the final counting is","analyze_text" :count  }
        return render(request, 'analyze.html', param)
                        
    else:
        messages.error(request,'Please Select the Option')

        return render(request, 'index.html')




def yputube_url(request):

   return render(request , 'youtube.html' , )

def youtube_download(request):
     
    resolution = []
    url = request.GET.get('url')


    if url:
        try:
            yt = YouTube(url)
            streamall = yt.streams.filter(progressive=True, file_extension='mp4')
            for i in streamall:
                if i.resolution is not None:
                    resolution.append(i.resolution)
            resolution = list(dict.fromkeys(resolution))
            embed_link = yt.watch_url.replace('watch?v=', 'embed/')

        except VideoUnavailable:
            messages.error(request, "The video is unavailable. Please check the URL.")
            return render(request , 'youtube.html' , )
        
        except Exception as ex:
            messages.error(request, f"An error occurred: {str(ex)}")
            return render(request , 'youtube.html' , )

    else:
        messages.error(request, "Please give me a valide Youtube Link")
        return render(request , 'youtube.html' , )

    return render(request , 'youtube_download.html' , {'resolution':resolution,'embed_link':embed_link,'url': url })

def download_video(request):
    url = request.GET.get('url')
    res = request.GET.get('res')

    if url and res:
        try:
            yt = YouTube(url)
            stream = yt.streams.filter(res=res, progressive=True, file_extension='mp4').first()
            if stream:
               
                file_path = stream.download(output_path='C:/Downloads/')
                file_name = os.path.basename(file_path)
                
                # Provide the video as a downloadable response
                response = FileResponse(open(file_path, 'rb'), as_attachment=True, filename=file_name)
                return response
            else:
                messages.error(request, "Selected resolution not available.")
        except Exception as ex:
            messages.error(request, f"An error occurred: {str(ex)}")
    else:
        messages.error(request, "Invalid URL or resolution.")

    return redirect('youtube_download')

     
