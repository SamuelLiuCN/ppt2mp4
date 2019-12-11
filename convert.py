# -*- coding: UTF-8 -*-
import win32com.client
import time
import os
import sys
import shutil

def ppt_to_mp4(ppt_path,mp4_target,resolution = 720,frames = 24,quality = 60,timeout = 120):
    # status:Convert result. 0:failed. -1: timeout. 1:success.
    status = 0
    if ppt_path == '' or mp4_target == '':
        return status
    # start_tm:Start time
    start_tm = time.time()

    # Create a folder that does not exist.
    sdir = mp4_target[:mp4_target.rfind('\\')]
    if not os.path.exists(sdir):
        os.makedirs(sdir)

    # Start converting
    ppt = win32com.client.Dispatch('PowerPoint.Application')
    presentation = ppt.Presentations.Open(ppt_path,WithWindow=False)
    # CreateVideo() function usage: https://docs.microsoft.com/en-us/office/vba/api/powerpoint.presentation.createvideo
    presentation.CreateVideo(mp4_target,-1,1,resolution,frames,quality)
    while True:
        try:
            time.sleep(0.1)
            if time.time() - start_tm > timeout:
                # Converting time out. Killing the PowerPoint process(An exception will be threw out).
                os.system("taskkill /f /im POWERPNT.EXE")
                status = -1
                break
            if os.path.exists(mp4_path) and os.path.getsize(mp4_target) == 0:
                # The filesize is 0 bytes when convert do not complete.
                continue
            status = 1
            break
        except Exception, e:
            print 'Error! Code: {c}, Message, {m}'.format(c = type(e).__name__, m = str(e))
            break
    print time.time()-start_tm
    if status != -1:
        ppt.Quit()

    return status
    
if __name__ == '__main__':

    # Require Windows system(Media Player was enabled) and Microsoft Office 2010 or higher.
    # Converting ppt into video relies on Windows Media Player. So you need to enable Desktop Experience feature.
    # More save types please visit: https://docs.microsoft.com/en-us/office/vba/api/powerpoint.ppsaveasfiletype

    # quality:0-100. The level of quality of the slide. The higher the number, the higher the quality.
    quality = 60
    # resolution:The resolution of the slide. 480,720,1080...
    resolution = 720
    # frames: The number of frames per second.
    frames = 24

    # ppt_path:The ppt/pptx/pptm file path.
    ppt_path = os.path.abspath('./test.pptx')
    # mp4_path:The mp4 video save path.
    mp4_path = os.path.abspath('./test.mp4')

    # ie_temp_dir:The convert cache file path.
    # The default path (hidden) is 'C:/Users/username/AppData/Local/Microsoft/Windows/Temporary Internet Files/Content.MSO/ppt'.
    # Or 'C:/Users/username/AppData/Local/Microsoft/Windows/INetCache/Content.MSO/ppt'
    # You can find the cache folde at IE setting.
    # If you don't want clear cache files,assign ie_temp_dir with empty string.
    #ie_temp_dir = 'C:/Users/username/AppData/Local/Microsoft/Windows/INetCache/Content.MSO/ppt'
    ie_temp_dir = ''

    # status:Converting result. 0:failed. -1: timeout. 1:success.
    status = 0
    # timeout: Seconds that converting time out.
    timeout = 4*60
    try:
        status = ppt_to_mp4(ppt_path,mp4_path,resolution,frames,quality,timeout)
        # Clear PowerPoint cache after convert completed. When you converted hundreds of files, the cache folder will be huge.
        if ie_temp_dir != '':
            shutil.rmtree(ie_temp_dir, ignore_errors=True)
    except Exception, e:
        print 'Error! Code: {c}, Message, {m}'.format(c = type(e).__name__, m = str(e))
        
    if status == -1:
        print 'Failed:timeout.'
    elif status == 1:
        print 'Success!'
    else:
        if os.path.exists(mp4_path):
            os.remove(mp4_path)
        print 'Failed:The ppt may have unknow elements. You can try to convert it manual.'
