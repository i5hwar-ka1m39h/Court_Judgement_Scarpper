import scrapy
from bs4 import BeautifulSoup
import re



#clean the text remove all the extra whitespaces and line
def clean_text(text):
    text = re.sub(r'\s+', ' ', text) # multiple spaces and newlines
    text = text.strip() # removing spaces at the end and start of line
    return text


# from give html extract the court judgement
def extract_judgement(judgement_html):
    soup = BeautifulSoup(judgement_html, 'html.parser')

    #storing the different parts of judgement in dictonary
    judgement = {
        'title':'',
        'court_name': '',
        'bench': '',
        'author': '',
        'content': []
    }

    title_ele = soup.find('h2', class_="doc_title")
    if title_ele:
        judgement['title']= clean_text(title_ele.text)

    court_name_html = soup.find('h2', class_="docsource_main")
    if court_name_html:
        judgement['court_name'] = clean_text(court_name_html.text)

    bench_ele = soup.find("h3", class_="doc_bench")
    if bench_ele:
        #remove the "bench :" from the text
        bench_text = bench_ele.text.replace('Bench: ', '').strip()
        judgement['bench'] = clean_text(bench_text)

    author_ele = soup.find("h3", class_="doc_author")
    if author_ele:
        #remove the "author: " from the text
        author_text = author_ele.text.replace('Author: ', '').strip()
        judgement['author'] = clean_text(author_text)

    judgement_div = soup.find("div", class_="judgments")
    if judgement_div:
        content_element = judgement_div.find_all(['p', 'blockquote', 'pre'])

        for element in content_element:
            if "hidden_text" in element.get('class',[]):
                continue

            text = clean_text(element.get_text())

            if text and not text.isspace() and not text.isnumeric():

                structure = element.get('data-structure','')

                if text:
                    judgement['content'].append({
                        'type':structure,
                        'text': text
                    })

    return judgement

def format_judgement_text(judgement):
    formatted_text = []

    # judgement = {
    #     'court_name': '',
    #     'bench': '',
    #     'author': '',
    #     'content': [],
    #     'title': '',
    # }


    if judgement["title"]:
        formatted_text.append(f"TITLE:\n{judgement['title']}\n")

    if judgement['bench']:
        formatted_text.append(f"BENCH:\n{judgement['bench']}\n")

    if judgement['author']:
        formatted_text.append(f"AUTHOR:\n{judgement['author']}\n")

    formatted_text.append("JUDGEMENT CONTENT")
    for item in judgement["content"]:
        if item["type"]:
            formatted_text.append(f"\n[{item['type']}]")
        formatted_text.append(item["text"])

    return "\n".join(formatted_text)


# small_judge.py
class SmallJudgeSpider(scrapy.Spider):
    name = "small_judge"
    allowed_domains = ["indiankanoon.org"]
    start_urls = ["https://indiankanoon.org/doc/95609026/",
                  "https://indiankanoon.org/doc/22323604/",
                  "https://indiankanoon.org/doc/174244987/",
                  "https://indiankanoon.org/doc/70913397/",
                  "https://indiankanoon.org/doc/187260364/",
                  "https://indiankanoon.org/doc/173575471/",
                  "https://indiankanoon.org/doc/64092156/",
                  "https://indiankanoon.org/doc/125767416/",
                  "https://indiankanoon.org/doc/196200292/",
                  "https://indiankanoon.org/doc/77746091/",
                  "https://indiankanoon.org/doc/90052727/",
                  "https://indiankanoon.org/doc/139870956/",
                  "https://indiankanoon.org/doc/191080286/",
                  "https://indiankanoon.org/doc/185437413/",
                  "https://indiankanoon.org/doc/10909725/",
                  "https://indiankanoon.org/doc/118777590/",
                  "https://indiankanoon.org/doc/124568699/",
                  "https://indiankanoon.org/doc/45242209/",
                  "https://indiankanoon.org/doc/44178519/",
                  "https://indiankanoon.org/doc/43162195/"]
    
    def parse(self, response):
        judgement_html = response.css('div.judgments').get()
        title = response.css("h2.doc_title::text").get()
        
        if judgement_html:
            judgement = extract_judgement(judgement_html)  # Pass judgement_html instead of result
            clear_result = format_judgement_text(judgement)  # Fixed variable name from clear_reult
            
            if clear_result:  # Fixed variable name
                yield {
                    "title": title,
                    "all_data": clear_result
                }
            else:
                yield {
                    'title': "",
                    "all_data": ""
                }