import sys, os, csv, time, requests, shutil
from utils import read_csv
from pprint import pprint
import bcolors

try:
    sys.argv[1]
    sys.argv[2]
except:
    raise Exception("Please provide an input csv and a output dir.")

csv_file = sys.argv[1]
output_dir = "output/" + sys.argv[2]

if not os.path.exists(output_dir):
    os.mkdir(output_dir)

rows = read_csv(csv_file)

products = []

for row in rows[1:]:
    new_product = True
    for p in products:
        if p['handle'] == row[0]:
            new_product = False
            p['images'].append(row[23])

    if new_product:
        product = {
            "title": row[1].replace(" ", "_").replace("/", "_").replace("\\", "_").replace("\"", "_").replace("\'", "_").replace(",", "_"),
            "sku": row[13].replace("'", ""),
            "images": [row[23]],
            "handle": row[0],
        }
        products.append(product)

sucessful_links = []
failed_links = []

for p in products:
    for index, link in enumerate(p['images']):
        if link:
            if p['sku']:
                sku = p['sku']
            else:
                sku = "xxxxx"
            filename = f"{sku}_{p['title']}_{index + 1}"
            r = requests.get(link, stream=True)

            if r.status_code == 200:
                r.raw.decode_content = True
                pprint(r.headers['Content-Type'])
                image_type = r.headers['Content-Type']
                if image_type == "image/png":
                    file_ext = '.png'
                elif image_type == "image/jpeg":
                    file_ext = '.jpg'
                elif image_type == "image/gif":
                    file_ext = '.gif'
                else:
                    print("Failed ext type:")
                    print(image_type)
                    exit()
                try:
                    print(f"{output_dir}/{filename}")
                    with open(f"{output_dir}/{filename}{file_ext}", 'wb') as f:
                        shutil.copyfileobj(r.raw, f)
                        pprint(f'Image sucessfuly downloaded: {filename}')
                        sucessful_links.append({
                        "link": link,
                        "filename": filename
                    })
                except Exception as e:
                    pprint(f"{filename} couldn't be downloaded.")
                    failed_links.append({
                        "link": link,
                        "filename": filename,
                        "error":e
                    })
            else:
                pprint(f"{filename} couldn't be downloaded.")
                failed_links.append({
                        "link": link,
                        "filename": filename
                    })
            time.sleep(0.3)


for f in failed_links:
    print(f['error'])
    print('\n\n')

print(f"Failed links: {len(failed_links)}")
print(f"Sucessful links: {len(sucessful_links)}")