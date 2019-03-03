import sys
import ijson
import re
from datetime import datetime
from dateutil.parser import parse
from wordcloud import WordCloud

json_path = sys.argv[1]
output_path = sys.argv[2]
begin = parse("2019-01-01")
end = parse("2019-03-01")


def parse_time(t):
    try:
        return datetime.strptime(t, "%Y-%m-%dT%H:%M:%S.%fZ")
    except ValueError:
        return datetime.strptime(t, "%Y-%m-%dT%H:%M:%SZ")


def match_item(item: dict):
    return item["title"].startswith("検索結果:") and (begin <= parse_time(item["time"]) <= end)


def extract_keywords(title: str):
    return list(filter(None, re.split(r'[\W\u3000]', title.split("検索結果: ")[1])))


if __name__ == '__main__':
    keywords = []
    with open(json_path) as f:
        for kws in (extract_keywords(item["title"]) for item in ijson.items(f, "item") if match_item(item)):
            for kw in kws:
                keywords.append(kw)

    wc = WordCloud(font_path='fonts/NotoSansCJKjp-Regular.otf', width=1280, height=720, background_color="white")
    wc.generate("\n".join(keywords))
    wc.to_file(output_path)

