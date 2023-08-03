import requests
import pandas as pd
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows


# 批量获取文章信息并保存到excel
class CSDNArticleExporter:
    def __init__(self, username, size, filename):
        self.username = username
        self.size = size
        self.filename = filename

    def get_articles(self):
        url = f"https://blog.csdn.net/community/home-api/v1/get-business-list?page=1&size={self.size}&businessType=blog&orderby=&noMore=false&year=&month=&username={self.username}"
        try:
            response = requests.get(url)
            data = response.json()
            return data['data']['list']
        except Exception as e:
            print(f"Error occurred: {e}")
            return []

    def get_article_score(self, article_url):
        url = "https://bizapi.csdn.net/trends/api/v1/get-article-score"
        headers = {
            "Accept": "application/json, text/plain, */*",
            "X-Ca-Key": "203930474",
            "X-Ca-Nonce": "f48fbdf5-f166-4f33-aad3-9178bdd7990a",
            "X-Ca-Signature": "Dm5IRgsgWZ+4juiGSEOpsenOfYgbr0MTdWc0k7Pg5bY=",
            "X-Ca-Signature-Headers": "x-ca-key,x-ca-nonce",
            "X-Ca-Signed-Content-Type": "multipart/form-data",
        }
        data = {"url": article_url}
        try:
            response = requests.post(url, data=data, headers=headers)
            return response.json()['data']['score']
        except Exception as e:
            print(f"Error occurred: {e}")
            return None

    def export_to_excel(self):
        articles = self.get_articles()
        for article in articles:
            article['score'] = self.get_article_score(article['url'])
        df = pd.DataFrame(articles)
        df = df[['title', 'url', 'created_at', 'views', 'collects', 'likes', 'comments', 'score']]
        df.columns = ['文章标题', 'URL', '发布时间', '阅读量', '收藏量', '点赞量', '评论量', '质量分']
        self.save_to_excel(df, self.filename)

    @staticmethod
    def save_to_excel(df, filename):
        wb = Workbook()
        sheet = wb.active
        for r in dataframe_to_rows(df, index=False, header=True):
            sheet.append(r)
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
        wb.save(filename)


if __name__ == '__main__':
    exporter = CSDNArticleExporter("weixin_43764974", 20, 's.xlsx')
    exporter.export_to_excel()