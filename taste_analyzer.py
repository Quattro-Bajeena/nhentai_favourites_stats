import json
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import pandas as pd
from collections import Counter

with open("favourites_tags.json") as fp:
    tags_dict = json.load(fp)




TAG_CATEGORIES = ("parody", "character", "tag", "artist", "group", "language", "category", "pages")

tag_type = "parody"
global_frequency_threshold = 1
my_frequency_threshold = 2
realtive = False
use_stopwords = True

stopwords = set()
if use_stopwords:
    stopwords.add("sole male")
    stopwords.add("sole female")
    stopwords.add("mosaic censorship")
    # stopwords.add("original")
    # stopwords.add("nakadashi")


tag_list = [tag[1] for tag in tags_dict["tags"] if (tag[0] == tag_type and (tag[1] not in stopwords) and (tag_type == "pages" or tags_dict['tag_counts'][tag[1]] >= global_frequency_threshold))] 

word_could_dict = {x: count for x, count in Counter(tag_list).items() if count >= my_frequency_threshold}

if realtive:
    for (tag_name, tag_count) in word_could_dict.items():
        overall_count = tags_dict['tag_counts'][tag_name]
        word_could_dict[tag_name] = word_could_dict[tag_name] / overall_count


wordcloud = WordCloud(width = 900, height = 900,
        background_color ='white', stopwords = stopwords, 
        min_font_size = 10).generate_from_frequencies(word_could_dict)

# plot the WordCloud image                      
plt.figure(figsize = (8, 8), facecolor = None)
plt.imshow(wordcloud)
plt.axis("off")
plt.tight_layout(pad = 0)

plt.savefig(tag_type + ".png", bbox_inches='tight')
plt.show()

