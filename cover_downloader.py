import tkinter as tk
import requests
import json

def get_album_cover(artist, album):
    endpoint = "https://musicbrainz.org/ws/2/release-group?query=artist:" + artist + "%20AND%20release:" + album + "&fmt=json"

    response = requests.get(endpoint)

    if response.status_code == 200:
        data = json.loads(response.text)
        if data["release-groups"]:
            first_result = data["release-groups"][0]
            release_group_mbid = first_result["id"]
            cover_art_url = "https://coverartarchive.org/release-group/" + release_group_mbid
            response = requests.get(cover_art_url)
            if response.status_code == 200:
                data = json.loads(response.text)
                if data["images"]:
                    first_image = data["images"][0]
                    image_url = first_image["image"]
                    return image_url
                else:
                    return None
            else:
                return None
        else:
            return None
    else:
        return None

def download_image():
    artist = artist_entry.get()
    album = album_entry.get()
    album_cover_url = get_album_cover(artist, album)
    if album_cover_url:
        response = requests.get(album_cover_url)
        if response.status_code == 200:
            with open(album + ".jpg", "wb") as f:
                f.write(response.content)
            status_label.config(text="Cover successfully downloaded.", foreground="green")
        else:
            status_label.config(text="Unable to download the cover.", foreground="red")
    else:
        status_label.config(text="Cover not found.", foreground="red")

root = tk.Tk()
root.title("Cover Downloader by vuitsu")
root.geometry("400x200")
root.configure(bg='#F0F0F0')

artist_label = tk.Label(root, text="Artist :", bg='#F0F0F0')
artist_label.pack()
artist_label.place(relx=0.05, rely=0.1, anchor="w")

artist_entry = tk.Entry(root, font=("Arial", 12))
artist_entry.pack()
artist_entry.place(relx=0.3, rely=0.1, relwidth=0.6)

album_label = tk.Label(root, text="Album / Single :", bg='#F0F0F0')
album_label.pack()
album_label.place(relx=0.05, rely=0.3, anchor="w")

album_entry = tk.Entry(root, font=("Arial", 12))
album_entry.pack()
album_entry.place(relx=0.3, rely=0.3, relwidth=0.6)

download_button = tk.Button(root, text="Download", command=download_image)
download_button.pack()
download_button.place(relx=0.3, rely=0.5, relwidth=0.4)

status_label = tk.Label(root, text="", bg='#F0F0F0')
status_label.pack()
status_label.place(relx=0.05, rely=0.7, relwidth=0.9, anchor="w")

root.mainloop()
