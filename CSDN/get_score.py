import urllib.request
import json
import pandas as pd
from openpyxl import Workbook, load_workbook
from openpyxl.utils.dataframe import dataframe_to_rows


# 批量获取文章信息并保存到excel
class CSDNArticleExporter:
    def __init__(self, username, size, filename):
        self.username = username
        self.size = size
        self.filename = filename

    def get_articles(self):
        url = f"https://blog.csdn.net/community/home-api/v1/get-business-list?page=2&size={self.size}&businessType=blog&orderby=&noMore=false&year=&month=&username={self.username}"
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode())
        return data['data']['list']

    def export_to_excel(self):
        df = pd.DataFrame(self.get_articles())
        df = df[['title', 'url', 'postTime', 'viewCount', 'collectCount', 'diggCount', 'commentCount']]
        df.columns = ['文章标题', 'URL', '发布时间', '阅读量', '收藏量', '点赞量', '评论量']
        # df.to_excel(self.filename)
        # 下面的代码会让excel每列都是合适的列宽，如达到最佳阅读效果
        # 你只用上面的保存也是可以的
        # Create a new workbook and select the active sheet
        wb = Workbook()
        sheet = wb.active
        # Write DataFrame to sheet
        for r in dataframe_to_rows(df, index=False, header=True):
            sheet.append(r)
        # Iterate over the columns and set column width to the max length in each column
        for column in sheet.columns:
            max_length = 0
            column = [cell for cell in column]
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(cell.value)
                except:
                    pass
            adjusted_width = (max_length + 5)
            sheet.column_dimensions[column[0].column_letter].width = adjusted_width
        # Save the workbook
        wb.save(self.filename)


# 批量查询质量分
class ArticleScores:
    def __init__(self, filepath):
        self.filepath = filepath

    @staticmethod
    def get_article_score(article_url):
        url = "https://bizapi.csdn.net/trends/api/v1/get-article-score"
        headers = {
            "Accept": "application/json, text/plain, */*",
            "X-Ca-Key": "203930474",
            "X-Ca-Nonce": "f48fbdf5-f166-4f33-aad3-9178bdd7990a",
            "X-Ca-Signature": "Dm5IRgsgWZ+4juiGSEOpsenOfYgbr0MTdWc0k7Pg5bY=",
            "X-Ca-Signature-Headers": "x-ca-key,x-ca-nonce",
            "X-Ca-Signed-Content-Type": "multipart/form-data",
        }
        data = urllib.parse.urlencode({"url": article_url}).encode()
        req = urllib.request.Request(url, data=data, headers=headers)
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode())['data']['score']

    def get_scores_from_excel(self):
        # Read the Excel file
        df = pd.read_excel(self.filepath)
        # Get the 'URL' column
        urls = df['URL']
        # Get the score for each URL
        scores = [self.get_article_score(url) for url in urls]
        return scores

    def write_scores_to_excel(self):
        df = pd.read_excel(self.filepath)
        df['质量分'] = self.get_scores_from_excel()
        df.to_excel(self.filepath,index=False)


if __name__ == '__main__':
    # 获取文章信息
    exporter = CSDNArticleExporter("weixin_43764974", 194, 'score1.xlsx')  # Replace with your username
    exporter.export_to_excel()
    # 批量获取质量分
    score = ArticleScores('score1.xlsx')
    score.write_scores_to_excel()
