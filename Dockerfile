RUN apt update && apt upgrade 
RUN git clone https://github.com/audiminia/Tg-book-bot
RUN pip3 install -U -r requirements.txt 

CMD python3 bot.py
