from urllib.request import Request,urlopen
from multiprocessing import Pool
import os
import re

url = 'https://123truyenvip.com/dao-gioi-thien-ha'
end_chap = 7323
novel_title = re.sub('https://123truyenvip.com/', '', url.replace('-', ''))

# Create directory for new book
if not os.path.isdir(novel_title):
    os.mkdir(novel_title)


def get_chapter(i):
    req = Request(
            url = url + '/chuong-' + str(i),
            headers = {'User-Agent': 'Mozilla/5.0'}
            )
    page = urlopen(req).read().decode('utf-8')

    # Find title
    pattern = "<title.*?>(.|\n)*?</title.*?>"
    match_results = re.search(pattern, page, re.IGNORECASE)
    title = match_results.group()
    title = re.sub('<.*?>', '', title)
    title = re.search(':(?!.*:).*', title, re.IGNORECASE).group().strip(':').strip()
    filename = novel_title + '/' + 'Chương ' + str(i) + ': ' + title + '.html'
    filepath = '/' + novel_title + '/' + filename
    if not os.path.isfile(filepath):
        
        # Create new file with title
        chapter = open(filename, 'w', encoding='utf-8')
        chapter.write('<title>' + title + '\n' + '</title>')
        
        # Add heading
        heading = '<h1>' + 'Chương ' + str(i) + ': ' + title + '</h1>'
        chapter.write(heading + '\n')
        chapter.close()

        # Find paragraphs
        chapter = open(filename, 'a', encoding='utf-8')
        pattern = '<div class="ccc chapter-content ccc".*?>(.|\n)*?<p style="font-size: 0.8em.*?>'
        match = re.search(pattern, page, re.IGNORECASE).group()

        # Clearance paragraphs
        match = re.sub("</p>", "\n", match)
        match = re.sub("<.*?>", "", match)
        lines = match.split('\n')
        for i in range(len(lines)):
            line = lines[i].strip()
            if i == 0:
                chapter.write('<title>' + line + '</title>')
                chapter.write('<h1>' + line + '</h1>')
            elif line != '':
                chapter.write('<p>' + line + '</p>')
        chapter.close()
        print(filename)

p = Pool()
p.map(get_chapter, range(1, end_chap + 1))
