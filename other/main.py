from random import random

from wordcloud import WordCloud
import matplotlib.pyplot as plt

text = "This is a sample text for generating word cloud."

def color_func(word, font_size, position, orientation, random_state=None, **kwargs):
    return "hsl(0, 0%, %d%%)" % random.randint(60, 100)

# 使用自定义 color_func
wordcloud = WordCloud(color_func=color_func).generate(text)

# 显示词云图像
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()
