#book downloader bot using libgen

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.types import Message,CallbackQuery

from bot import Bot

from bs4 import BeautifulSoup
from urllib.parse import urlencode
import re
import os
import json
import requests
import aiohttp
import aiofiles
import asyncio

import random

def getSearchResults(link, term): #to get all books from search result
    parmas = urlencode({'req': term})
    url=link+parmas
    response=requests.get(url).content
    if not response:
        return 0
    html = BeautifulSoup(response, features="html.parser")
    for s in html.find_all('script'):
        s.decompose()
    table = html.find('table', attrs={"rules":"rows"})
    ids=[]
    for tr in table.find_all('tr', attrs={"valign":"top"})[1:]:
        ids.append(tr.td.get_text())
    return ids

def get_book(payload:str) -> dict:
    url=f"http://libgen.is/json.php"
    url=url+payload
    print(url)
    response = requests.post(url, data=payload)
    if response.status_code==200:
        books=response.json()
        print(json.dumps(books, indent=4, sort_keys=True))
        return books

def get_download_link(md5):
    try:
        link="http://libgen.li/ads.php?md5="
        url=link+md5
        response=requests.get(url).content
        soup = BeautifulSoup(response, features="html.parser")
        tables=soup.find_all("table")[0]
        for a in tables.find_all("a"):
            print(a)
            if a.text == 'GET':
                book_url = a.attrs['href']
                book_url=book_url.replace('\\','/')
                book_url=f"https://cdn3.booksdl.org/{book_url}" 
                print("Book download link: ",book_url)
                return book_url
            else:
                continue
    except:
        return 0

def get_download_link1(md5):
    try:
        link="http://library.lol/main/"
        url=link+md5
        response=requests.get(url).content
        soup = BeautifulSoup(response, features="html.parser")
        tables=soup.find_all("table")[0]
        for a in tables.find_all("a"):
            print(a)
            if a.text == 'GET':
                book_url = a.attrs['href']
                print(book_url)
                book_url=book_url.replace('\\','/')
                print("Book download link: ",book_url)
                return book_url
            else:
                continue
    except:
        return 0 
            
@Bot.on_callback_query()
async def download(client: Client, query: CallbackQuery):
    data = query.data.split('.')
    print(data)
    if int(data[-1]) != query.from_user.id:
        return await query.answer("Not for you!",show_alert=True)
    bookID = data[1]
    payload=f"?ids={bookID}&fields=id,title,volumeinfo,series,periodical,author,year,edition,publisher,city,pages,language,topic,library,issue,dpi,color,orientation,paginated,scanned,searchable,filesize,extension,md5,coverurl,tags,descr,pagesinfile,toc,sha1,sha256,crc32,edonkey,aich,tth,ipfs_cid,btih,torrent"
    try:
        book=get_book(payload)
        result=book[0]
        
        id=result.get('id', 'N/A') 
        title = result.get('title', 'N/A') 
        author = result.get('author','N/A')
        publisher = result.get('publisher', 'N/A')
        year = result.get('year', 'N/A')
        lang = result.get('language', 'N/A')
        pages = result.get('pages','N/A')
        size = result.get('filesize', 'N/A')
        size=f"{int(size)/1024**2:.2f} MB"
        ext = result.get('extension', 'N/A')
        md5= result.get('md5', None)
        descr=result.get('descr', 'N/A')
        descr=(f"{descr[:300]}..." if type(descr) is str else "N/A")
            
        if result.get("coverurl"):
            cover = result.get("coverurl")
            image_url = f"http://libgen.is/covers/{cover}"
            print(image_url)
        else:
            image_url = f"https://telegra.ph/file/7ebc4746da9f8149fedb2.jpg"
            
        if data[0]=='book':
            cap = f"""
<b>📖 {title}</b>
<i>by {author}</i>

<b>Publisher :</b> `{publisher}`
<b>Year :</b> {year}
<b>Language :</b> {lang}
<b>Pages :</b> {pages}
<b>Size :</b> {size}
<b>Ext. :</b> {ext}
[­]({image_url})
<b>Description :</b> {descr}
                    """
            print(cap)
            button=[
                    [
                        InlineKeyboardButton("🔒 Download book", callback_data = f'download.{id}.{query.from_user.id}')
                    ]
                ]
            await query.edit_message_text(cap, disable_web_page_preview=False, reply_markup=InlineKeyboardMarkup(button))
        elif data[0]=='download':
            try:
                await query.edit_message_text("Please wait...", disable_web_page_preview=False)
                # Constructing the filename based on title and author
                fname = f'{title} by {author}'
                # Get the download link using the md5 hash
                dlink = get_download_link(md5)
                if not dlink:
                    dlink = get_download_link1(md5)
                # Process the filename (remove non-alphanumeric characters, replace spaces, and limit to 45 characters)
                fname = re.sub(r'[^a-zA-Z0-9\s]+', '', fname).replace(" ", "_")[:45] + f'.{ext}'
                # Download the PDF file
                async with aiohttp.ClientSession() as session:
                      async with session.get(dlink) as response:
                           if response.status == 200:
                              async with aiofiles.open(fname, "wb") as file:
                                  while True:
                                      chunk = await response.content.read(81920)
                                      await asyncio.sleep(0)
                                      if not chunk:
                                          break
                                      await file.write(chunk)
                              await query.edit_message_text(f"{ext} File found.. Please wait uploading..")
                              await query.message.reply_document(document=open(fname, "rb"), caption=f'<b>📖 {title}</b><i>\nby {author}</i>')
                              os.remove(fname)
                              await query.message.delete()
            except Exception as e:
                # Handle any exceptions that might occur during the process
                await query.edit_message_text("Failed to get the file.", disable_web_page_preview=False)
                print(e)
                # If the file was partially downloaded, remove it
                if os.path.exists(fname):
                    os.remove(fname)
        else:
            pass         
    except Exception as e:
        print(e)
        await query.edit_message_text("Sorry something went wrong...please try again.", disable_web_page_preview=False)

@Bot.on_message(filters.command("book"))
async def get_cmd(client: Client, message: Message):
    url=f"http://libgen.is/index.php?"
    if len(message.text.split()) <= 1:
        await message.reply("No name found, enter book name")
        return
    book = message.text.split(maxsplit=1)[1]
    ids = getSearchResults(url, book)
    if not ids:
        await message.reply("No book found")
        return
        
    id=','.join(map(str, ids))
    data = f"?ids={id}&fields=id,title"
    result= get_book(data)
    buttons = []
    for i in result:
        buttons.append([InlineKeyboardButton(
            text=i['title'],
            callback_data=f'book.{i["id"]}.{message.from_user.id}'
        )])
    await message.reply(f"Search result for **{book}**:", disable_web_page_preview=False, reply_markup=InlineKeyboardMarkup(buttons))