import requests, os, re, shutil

def save(book_url: str, start_num,path="pages"):
    if not os.path.exists(path):
        os.mkdir(path)
    with requests.Session() as s:
        headers = {
            "User-Agent":
                "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
        }

        s.headers.update(headers)
        x = 1
        while True:
            spread = s.get(
                f"{book_url}{start_num}/spread.js")
            if str(spread.status_code).startswith("2"):
                req = s.get("https://oauth.digiboek.be" + spread.json()["structure"]["spread"]["bg"]["hires"][0])
                with open(f"./pages/{x}.png", 'wb') as f:
                    f.write(req.content)
            else:
                print(f"Found {x} pages!")
                break
            if x == 1:
                x += 1
            else:
                x += 2
            start_num += 1

def convert_pdf(path="pages", fn="book.pdf", delete_img=True):
    images = []
    for f in sorted(os.listdir(path), key=lambda x: int(re.sub("\D", "", x))):
        img = Image.open(os.path.join(path, f))
        if img.mode == 'RGBA':
            img = img.convert('RGB')
        images.append(img)
    pdf = images[0]
    pdf.save(fn, "PDF", resolution=100.0, save_all=True, append_images=images[1:])
    if delete_img:
        shutil.rmtree(path)

book_url = input("Book url: ")
start_page = input("The start page number: ")

save(book_url, start_page)
print("Downloaded all pages!")
convert_pdf()
print("Converted into a PNG!")