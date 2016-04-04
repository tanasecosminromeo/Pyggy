from os import system
import warnings
import time
from keys import uk, aid
import speech_recognition as sr
from pb_py import main as API
import csv
import ngram
import random
from chatterbot import ChatBot
import ngram
import os.path

bot = ChatBot("One",
    storage_adapter="chatterbot.adapters.storage.MongoDatabaseAdapter",
    logic_adapters=[
        "chatterbot.adapters.logic.EvaluateMathematically",
        "chatterbot.adapters.logic.TimeLogicAdapter",
        # "chatterbot.adapters.logic.ClosestMeaningAdapter"
        "chatterbot.adapters.logic.ClosestMatchAdapter"
    ],
    io_adapters=[
        "chatterbot.adapters.io.JsonAdapter"
    ],
    database="database_movie_small_mongo")

# check if the database file exists
# if not, then train it
bot.train("chatterbot.corpus.english.movielines10000")
bot.train("chatterbot.corpus.english.conversations")
	
host = 'aiaas.pandorabots.com'
user_key = uk
app_id = aid
botname = 'pyggy2'

# lm = ngram.train_char_lm("pg.txt", order=8)

## Diagnostic information

#result = API.list_bots(user_key, app_id, host)
#print result

# for i in os.listdir('pyggy'):
# 	filename = 'pyggy/' + i
# 	result = API.upload_file(user_key, app_id, host, botname, filename)
# 	print result

# result = API.list_files(user_key, app_id, host, botname)
# print result

# result = API.compile_bot(user_key, app_id, host, botname)
# print result
# 
def speak_who(text, name):
	print(name + " said: " + text)
	if name == 'Fiona':
		system("say -v Tom -r 200 " + text) # should be Tom
	elif name == 'Pyggy':
		system("say -v Samantha -r 200 you said: " + text) # should be Samantha
	else:
		return


def speak_response(response, name):
	bot_response = response
	# Some basic data cleaning
	bot_response = bot_response.replace("'", "")
	bot_response = bot_response.replace("\n", "")
	bot_response = bot_response.replace("(", "")
	bot_response = bot_response.replace(")", "")
	bot_response = bot_response.replace(";", "")
	bot_response = bot_response.replace("-", "")
	speak_who(bot_response, name)

# obtain audio from the microphone	
warnings.filterwarnings("ignore")
r = sr.Recognizer()

timenow = time.time()
with open('logs/' + str(timenow) + '_log.csv', 'wb') as csvfile:
	with sr.Microphone() as source:
		r.adjust_for_ambient_noise(source)
		writer = csv.writer(csvfile)
		fieldnames = ['timestamp', 'input_text', 'response']
		writer.writerow(fieldnames)
		text1 = "Who are your friends?"
		botresponse1 = text1
		while True:
			
			# Fiona says something (chatterbot)
			speak_response(text1, 'Fiona')

			# human responds 
			# audio = r.listen(source)
			# try:
				# text2 = r.recognize_google(audio)
			# except:
				# text2 = 'Lets start again'

			text2 = str(raw_input())

			speak_response(text2, 'You')

			# Pyggy responds (pandorabot)
			# result = API.talk(user_key, app_id, host, botname, text1, session_id=True, recent=True)
			# pb_text2 = result['response']
			# botresponse2 = bot.get_response(botresponse1)
			# text2 = pb_text2 + ' ' + botresponse2
			# speak_response(text2, 'Pyggy')

			# Save the back and forth to the CSV log
			# writer.writerow([time.time(),text1,text2])
			# csvfile.flush()

			result = API.talk(user_key, app_id, host, botname, text2, session_id=True, recent=True)
			pb_text1 = result['response']
			# for talking with pyggy
			# botresponse1 = bot.get_response(botresponse2)
			botresponse1 = bot.get_response(text2)
			text1 = pb_text1 + ' ' + botresponse1

