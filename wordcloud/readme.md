>Bilibili弹幕获取并生成词云

# chatGPT_based


#  一、摘要

获取视频的弹幕文件（xml），并生成如图所示的词云：

![在这里插入图片描述](https://img-blog.csdnimg.cn/b1a5991280e3493aa34e1b9a2e51bcc8.png#pic_center =550x300)
用到的技术有：

> 1. 使用requests模块请求弹幕的xml文件；
> 2. 使用xpath解析，获取xml文件中的字幕；
> 3. 使用jieba对弹幕内容进行分词；
> 4. 使用	wordcloud生成词云。

# 二、获取目标视频cid

这个网站的视频以前使用AV号来唯一标记一个视频，后来改为BV号（打开移动端APP在视频的详情处即可看到），通过这两种标识号码可以直接搜索到对应的视频。

此外，一个视频还可以用cid、aid、bvid等来标识，本文使用cid来构造HTTP请求。获取视频cid的方法之一是：

1. 打开视频播放页面，（F12）检查页面；
2. 选择network选项，并搜索cid；
3. 点击其中一个结果，即可在payload选项下看到cid信息。
   ![在这里插入图片描述](https://img-blog.csdnimg.cn/7790b444492a44d89d115b0a404adcd8.png#pic_center =700x350)

<hr>
当然也可以点击视频的统计信息，下载统计信息文件，然后搜索cid。或者在程序中实现通过URL获取cid，方式不唯一。



# 三、获取视频弹幕xml文件

请求弹幕文件的方法有两种（截止今天，我用到的）：

![在这里插入图片描述](https://img-blog.csdnimg.cn/e1efd5c42ac44d4f828da9a883017051.png)


其中将cid号换成目标视频的cid即可。

直接在地址栏输入上面的地址即可预览视频的xml文件，可见弹幕内容都在`<p>`标签下面
![在这里插入图片描述](https://img-blog.csdnimg.cn/bb6c2e5a3bf540b38713f700cd99fb73.png#pic_center =700x480)
本文使用requests模块来获取该文件，并以cid号命名保存。

```python
  # 下载视频弹幕的xml文件
    def dm_xml(self):
        url = 'https://comment.bilibili.com/' + self.cid+ '.xml'
        try:
            response = requests.get(url)
        except Exception as e:
            print('获取xml内容失败,%s' % e)
            return False
        else:
            if response.status_code == 200:
                with open(f'{self.cid}.xml','wb') as f:
                    f.write(response.content)
                    print('成功下载弹幕xml文件')
                    return True
            else:
                return False
```


# 四、处理弹幕文件

下载xml后，需要进行如下操作，得到wordcloud的标准输入（string）：

1. 对每个`<p>`标签内的内容进行解析，并将其拼接成字符串；
2. 在使用jieba进行分词，将弹幕切分为一个个词语；
3. 去掉停用词，比如`啊、尽管、就是、因为`这样的词语，它们大量出现，但却不能反映弹幕的真实情感。

```python
    # 将xml文件中的文本提取出来，去掉停用词，分词
    def get_dm_txt(self):
        # 读取停用词，可以根据结果添加停用词
        with open("ChineseStopWords.txt", "r", encoding="utf-8") as fp:
            stopwords = [s.rstrip() for s in fp.readlines()]
        self.dm_xml()
        time.sleep(5)
        html = etree.parse(f'{self.cid}.xml', etree.HTMLParser())
        # xpath解析，获取当前所有的d标签下的所有文本内容
        text = html.xpath('//d//text()')
        # 列表拼接成字符串
        text = ''.join(text)
        text = jieba.lcut(text)
        words = []
        for w in text:
            if w not in stopwords:
                words.append(w)
        # 注意此处有空格
        words = ' '.join(words)
        return words
```

# 五、生成词云

使用wordcloud的generate()函数即可生成词云，再使用matplotlib显示即可。

此处要注意的一些参数有：

1. collocations，此参数设置为False可以保证每个词云只出现一次；
2. scale，缩放比例，该值越大，图像越清晰，但不宜太大，会导致加载变慢。

```python
    # 生成词云
    def wd(self):
        # collocations用于去掉重复词语；scale值越大清晰度越高，但太大加载会变慢
        wd = WordCloud(font_path='simhei.ttf',colormap="spring",width=800,height=400,
                       collocations=False,scale=5).generate(self.get_dm_txt())
        # 保存图片
        wd.to_file(f'{self.cid}.PNG')
        plt.imshow(wd, interpolation='bilinear')
        plt.axis("off")
        plt.show()
```





