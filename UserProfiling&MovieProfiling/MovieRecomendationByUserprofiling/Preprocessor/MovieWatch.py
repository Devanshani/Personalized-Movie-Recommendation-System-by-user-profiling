import re
import pypyodbc
from nltk.tokenize import word_tokenize,TweetTokenizer
import Preprocessor.emojiDictionary as emoji
import Preprocessor.emoticonDictionary as emot
import Preprocessor.acronymDictionary as acrn
from nltk.corpus import stopwords
from nltk.corpus import words

from nltk import WordNetLemmatizer

if __name__ == "__main__":
    con = pypyodbc.connect(Trusted_Connection='yes', driver='{SQL Server}', server='DESKTOP-7PTBIGN\DEVANSHANI',
                               database='MovieRecomendationDatabase', Uid='sa', Pwd='1234')
    cursor = con.cursor()
    # cursor.execute("UPDATE tbl_movie SET IsPreprocessed='FALSE'")
    cursor.execute("SELECT moviePlot,ID FROM MovieWatched")

    filtered_sentence = []
    for row in cursor.fetchall():
        # print(row[0])
        # print(row[1])
        tweet=str(row[0])
        id=str(row[1])
        print(id,"gggggggggggggggg")
        #remove unnecessary white spaces
        whitespace_less_tweet = re.sub('[\s]+', ' ',tweet)

        hash_tag_less_tweet = re.sub(r'#([^\s]+)', r'\1)',whitespace_less_tweet)
        # Remove additional white spaces
        additional_white_less_tweet = re.sub('[\s]+', ' ',hash_tag_less_tweet)
        # remove urls
        url_less_tweet = re.sub(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*', '',additional_white_less_tweet)
        # print(url_less_tweet)
        # Remove http
        http_less_tweet = re.sub(r"http\S+", "", url_less_tweet)
        # remove email
        email_less_tweet = re.sub(r'\w+@[a-zA-Z_]+?\.[a-zA-Z]{2,3}$', '', http_less_tweet)
        # print(email_less_tweet)
        # remove repeated characters
        repeate_char_less_tweet = re.sub(r'(.)\1{3,}', r'\1\1', email_less_tweet, flags=re.DOTALL)
        # print(repeate_char_less_tweet)
        filtered_sentence = []
        words = TweetTokenizer(strip_handles=True, reduce_len=True).tokenize(repeate_char_less_tweet)
        print(words)
        # replace emoticon
        for w in words:
            try:
                filtered_sentence.append(emot.select_emoticon(w))

            except:
                filtered_sentence.append(w)
        # print(filtered_sentence)

        filtered_replace_emoji = []
        # replace emoji
        print(filtered_sentence)
        for w in filtered_sentence:
            try:
                filtered_replace_emoji.append(emoji.select_emoji(w))
            except:
                filtered_replace_emoji.append(w)

        filtered_replaced_acronym = []
        # replace acronym
        for w in filtered_replace_emoji:
            try:
                filtered_replaced_acronym.append(acrn.select_acronym(w.lower()))
            except:
                filtered_replaced_acronym.append(w)

        sen = ""
        for a in filtered_replaced_acronym:
            sen = sen + a + " "

        # remove non alphanueric characters
        nonalphanumeric_less_tweet = re.sub(r'[^A-Za-z\s]+', '', sen)

        stop_words = []
        word_tokens = (word_tokenize(nonalphanumeric_less_tweet))
        with open("E:\MovieRecomendationByUserProfiling\PreProcessor\stopwords.txt", encoding='utf-8', errors='ignore')as f:
            lines = f.readlines()
        for line in lines:
            # print("kk", line)
            stop_words.append(line.strip())
        print(stop_words)
        filtered_sentence_stopword = []
        for w in word_tokens:
            if w not in stop_words:
                filtered_sentence_stopword.append(w)
        sentence = ""
        for a in filtered_sentence_stopword:
            sentence = sentence + a + " "
        print(sentence,"hhhhhhhhhhhhhhhhhhh")
        wnl = WordNetLemmatizer()
        lemmatizesent=" ".join([wnl.lemmatize(i) for i in sentence.split()])
        print(" ".join([wnl.lemmatize(i) for i in sentence.split()]))
        # remove single characters
        remove_single = re.sub(r'\b[B-Zb-z]\b', '', lemmatizesent)
        preprocessed_final = ''.join(map(str, remove_single))

        print(preprocessed_final)
        cursor.execute("UPDATE MovieWatched SET PreprocessedPlot ='" + str(preprocessed_final) + "' WHERE ID =" + str(id))
        cursor.commit()
        print("Review Updated!")
    cursor.close()