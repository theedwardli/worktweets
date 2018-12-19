from textgenrnn import textgenrnn
t = textgenrnn()
t.train_from_file('work_tweets_negative.txt', num_epochs = 5)