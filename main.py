import requests
import csv
from PIL import Image
from collections import Counter
import requests
from io import BytesIO

def get_rgb_values(img):
    width, height = img.size
    img = img.convert("RGB")

    rgb_values = []

    for y in range(height):
        for x in range(width):
            rgb = img.getpixel((x, y))

            rgb_values.append(rgb)

    return rgb_values

def get_majority_color(image_url):

    response = requests.get(image_url)
    img = Image.open(BytesIO(response.content))
    


    img = img.resize((100, 100))

    raw_rgb_values = get_rgb_values(img)

    color_counter = Counter(raw_rgb_values)

    majority_color  = prune_raw_rgb(color_counter)


    return majority_color

def prune_raw_rgb(counter):
    # get 20 most common tuples of format (r,g,b)
    ct = counter.most_common(20)
    print(ct)
    n = 1
    # iterate thru top 10
    while n < len(ct):
        majority_color = ct[n][0]
        # skip if white or black
        if majority_color == (0,0,0) or majority_color == (255, 255, 255):
            n+=1
        elif sum(majority_color) > 600 or not get_max_diff(majority_color) or sum(majority_color) < 30:
            #skip if too close to white, black, or grey
            n+=1
        else:
            return majority_color


def get_max_diff(tup):
    r,g,b = tup
    if max(abs(r-g), abs(r-b)) > 30:
        return True
    return False


rgb_list = []

with open('ids_and_urls.csv', mode='r') as file:
    reader = csv.reader(file)  # Read the header row

    for row in reader:
        team_id, url = row
        print(f"Team ID: {team_id}, URL: {url}")
        majority_color = get_majority_color(url)
        print(majority_color)
        rgb_list.append([team_id, majority_color])
    
with open("ids_and_rgb.csv", mode='w') as wf:
    writer = csv.writer(wf)

    for item in rgb_list:
        print(item)
        id = item[0]
        rgb = item[1]
        writer.writerow([id, rgb])
