from bs4 import BeautifulSoup
import requests
import re


def splitt(strr):
    new_str = strr.splitlines()
    return new_str


def regex(inputstr):
    res = re.sub(
        r'\d\d\d\d\d\d\d\d\d\d|\d\d\d\d\d\d\d\d\d\d\d\d\d|\d\d\d\d\d\d\d\d\d\w|\d\d\d\d\d\d\d\d\d\d\d\d\w|\d\d\d\d\d|\d\d\d\d|\d\d\w|\d\d\d|\d\d|\d-|-\d|,',
        "", inputstr)
    res = res.strip()
    return res


# gets the search query
query = input("Enter search query:")
query = query.replace(' ', '+')
print(query)
webpage = requests.get(f"https://libgen.li/index.php?req={query}&columns%5B%5D=t&objects%5B%5D=f&objects%5B%5D=e&objects%5B%5D=s&objects%5B%5D=a&objects%5B%5D=p&objects%5B%5D=w&topics%5B%5D=l&res=25&filesuns=all")


soup = BeautifulSoup(webpage.content, 'html.parser')
details = []
j = []
for trv in soup.find_all('tr'):
    details.append([trv.text])


for element in details:
    for val in element:
        value = splitt(val)
        j.append(value)
j.pop(0)
j.pop(0)

kil = j
libgen = []
for trv1 in soup.find_all('a', title="libgen"):
    libg = trv1.attrs['href']
    libgen.append(libg)


# to store link in the list itself as last entry
for num, ele in enumerate(libgen):
    kil[num].append(libgen[num])


for num, ele in enumerate(kil):
    kil[num][2] = regex(kil[num][2])
    print(f"{num}. Title: {kil[num][1]}, Publisher: {kil[num][6]}\n")


fileid1 = int(input("enter the serial number of file you want to download:"))
downlink = kil[fileid1][-1]
# print(downlink)

getLink = requests.get(downlink).text
soupy = BeautifulSoup(getLink, 'html.parser')

getsrc = soupy.body.table.tr
atag = getsrc.find('a')
href = atag.attrs['href']
# print(href)

res3 = requests.get(f'https://libgen.rocks/{href}')
with open('myfile.pdf', 'wb') as f:
    f.write(res3.content)
if res3.status_code == 200:
    print('It is a success')
