# -*- coding: utf-8 -*-
import tkinter
from tkinter import ttk, StringVar, filedialog
import os

import yt_dlp



def download_youtube_video(url):
    URLS = [url]
    def format_selector(ctx):
        """ Select the best video and the best audio that won't result in an mkv.
        NOTE: This is just an example and does not handle all cases """

        # formats are already sorted worst to best
        formats = ctx.get('formats')[::-1]

        # acodec='none' means there is no audio
        best_video = next(f for f in formats
            if f['vcodec'] != 'none' and f['acodec'] == 'none')

        # find compatible audio extension
        audio_ext = {'mp4': 'm4a', 'webm': 'webm'}[best_video['ext']]
        # vcodec='none' means there is no video
        best_audio = next(f for f in formats if (
            f['acodec'] != 'none' and f['vcodec'] == 'none' and f['ext'] == audio_ext))

        # These are the minimum required fields for a merged format
        yield {
            'format_id': f'{best_video["format_id"]}+{best_audio["format_id"]}',
            'ext': best_video['ext'],
            'requested_formats': [best_video, best_audio],
            # Must be + separated list of protocols
            'protocol': f'{best_video["protocol"]}+{best_audio["protocol"]}'
        }


    ydl_opts = {
        'format': format_selector,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download(URLS)


class DesktopApp(tkinter.Frame):
    def __init__(self, window=None):
        super().__init__(window, width=380, height=290,borderwidth=1, relief="groove")
        self.window = window
        self.pack()
        self.pack_propagate(0)
        self.create_widgets()

    # ウィジェット作成
    def create_widgets(self):
        
        url_frame = ttk.Frame(self, padding=10)
        url_label = ttk.Label(url_frame, text="URL")
        textVariable = StringVar()
        self.youtube_url = StringVar()
        entry = ttk.Entry(url_frame, textvariable=self.youtube_url)
        url_frame.pack()
        url_label.pack(side="left")
        entry.pack(side="left")
        
        workspace_frame = ttk.Frame(self, padding=10)
        workspace_label = ttk.Label(workspace_frame, text="保存先")
        self.workspace_path = StringVar()
        workspace_entry = ttk.Entry(workspace_frame, textvariable=self.workspace_path)
        select_button = ttk.Button(workspace_frame, text="参照", command=self.select_dir)
        workspace_frame.pack()
        workspace_label.pack(side="left")
        workspace_entry.pack(side="left")
        select_button.pack(side="right")
        
        save_button = ttk.Button(self, text="保存", command=self.save)
        save_button.pack(side="bottom")
        
    # ボタンのクリックイベント
    def select_dir(self):
        # エクスプローラーを開いてフォルダを選択する
        dir_path = filedialog.askdirectory()
        if len(dir_path) > 0: 
            self.workspace_path.set(dir_path)
    
    def save(self):
        print("save")
        path: str = self.workspace_path.get()
        url_link: str = self.youtube_url.get()
        # パスが存在するか確認する(ディレクトリ)
        if os.path.isdir(path):
            print("path is dir")
            print(path)
            download_youtube_video(url_link)
            
        

# Tkinterオブジェクト
window = tkinter.Tk()
# アプリのタイトル
window.title("YouTube Downloader")
# 画面の大きさ
window.geometry("400x300")
# アプリケーションオブジェクト
App = DesktopApp(window=window)
App.mainloop()

option = {
    'outtmpl' : 'C:/Users/hoge/Videos/mov/%(title)s.%(ext)s',
    'format' : 'bestvideo+bestaudio/best'
}