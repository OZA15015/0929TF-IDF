import MeCab
import codecs
import re
import collections
import os
import glob

def text_arrange(text): #不要文字の排除関数
    text = re.sub(r'<doc(.+?)\>', '', text)
    text = re.sub(r'</doc>', '', text)
    text = re.sub(r'https?://[\w/:%#\$&\?\(\)~\.=\+\-…]+', "", text)
    text = re.sub(r'[!-/:-@[-`{-~]', "", text) #半角記号
    text = re.sub(u'[！”＃＄％＆’（）＊＋，－．／：；＜＞？＠［￥］＾＿｀｛｜｝?「」] 『』【】', "", text) #全角記号
    text = re.sub(r'[、・’！?：＜＞＿｜「」｛｝【】『』〈〉－“”○〔〕…――――◇]', "", text)
    text = re.sub(r'[0-9]+', "", text) #半角数字
    text = re.sub(r'[０-９]+', "", text) #全角数字
    text = re.sub('\n', " ", text)  # 改行文字
    return text

def create_stop_words(): #stopwordの除去関数
    stop_words = []
    f = open('/home/ozawa/keio/research/tf-idf/stop_word.txt', 'r')
    tmp = f.readline()
    while tmp:
        tmp = tmp.replace("\n", "")
        stop_words.append(tmp)
        tmp = f.readline()
    f.close()
    return stop_words

def word_class(corpus, tagger): #対象品詞の抽出関数
    txt_list = []
    stop_words = create_stop_words()
    for text in corpus:
        text = text_arrange(text)
        if(text != ""):
             tagger.parse("")
             node = tagger.parseToNode(text)
             while node:
                if node.surface not in stop_words:
                    #if node.feature.split(",")[0] == u"名詞":
                    #    txt_list.append(node.surface)
                    if node.feature.split(",")[0] == u"形容詞":
                        txt_list.append(node.surface)
                node = node.next
    return txt_list    

def word_count(txt_list, per): #単語出現回数取得関数, per:何パーセント取得するか
    ch = collections.Counter(txt_list)
    d_len = int(len(ch) * per)
    ch_list = []
    #print(ch.most_common()[::-1][0:d_len])#少ない順
    for word, cnt in ch.most_common()[0:d_len]: #上位per件の単語
        ch_list.append(word)
    return ch_list

def make_honList(txt_list, ch_list): #対象文書中においてword_countで取得した単語を含めば格納し返却
    hon_List = []
    for txt in txt_list:
        if txt in ch_list:
             hon_List.append(txt)
    return hon_List

def main():
    file_list = glob.glob("0927_wikiData/*.txt")
    tagger = MeCab.Tagger('usr/lib/x86_64-linux-gnu/mecab/dic/mecab-ipadic-neologd')
    for file_data in file_list:
        with codecs.open(file_data, "r", "utf-8") as f: #文書の読み込み
            corpus = f.read().splitlines()

        txt_list = word_class(corpus, tagger) #対象品詞を取得
        ch_list = word_count(txt_list, 0.2) #指定出現回数単語リスト取得
        honList = make_honList(txt_list, ch_list)
        with open ('0929_keiyou/' + file_data, 'a', encoding='utf8') as writer:
            for data in honList:
                writer.write(data + '\n')
        del corpus, txt_list, ch_list, honList #メモリ領域開放

if __name__ == "__main__":
    main() 
