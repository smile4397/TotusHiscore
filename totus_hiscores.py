from PIL import Image, ImageDraw, ImageFont
import re

rank_conversion_dict = {
    '8️⃣': "Brigadier",
    '7️⃣': "Colonel",
    '6️⃣': "Major",
    '5️⃣': "Captain",
    '4️⃣': "Lieutenant",
    '3️⃣': "Sergeant",
    '2️⃣': "Corporal",
    '1️⃣': "Recruit",
    }

BLACK = (0,0,0,0)
# Number of pixels that are padded
PADDING = 18
HEADING_PADDING = 5
ACHIEVE_DIARY_X = 115
COL_LENGTHS = [60,119,70, 70]
s = 0
CUM_COL_LEN = [(s:=s+item) for item in COL_LENGTHS]
print(CUM_COL_LEN)

def data_gen():
    '''
    This generator yields the text file data and converts each row into a usable list.
    '''
    with open("totus_data.txt", "r", encoding="utf-8") as f:
        text = f.read()

    lines = text.strip().split("\n")
    # Ignore the first 2 lines as they are just the names of the columns.
    data_lines = lines[2:]
    # rows = []

    for line in data_lines:
        match = re.match(r"\s*(\d+)\)\s+(.+?)\s+(\S+)\s+([\d,]+)\s+(\d+)\s+([\d\.K]+)\s*(⭐?)", line)
        if match:
            #rows.append(list(match.groups()))
            yield list(match.groups())

def vertical_merge(im1: Image.Image, im2: Image.Image) -> Image.Image:
    '''
    Merges the images vertically
    '''
    w = max(im1.size[0], im2.size[0])
    h = im1.size[1] + im2.size[1]
    im = Image.new("RGBA", (w, h))

    im.paste(im1)
    im.paste(im2, (0, im1.size[1]))
    return im

# Image Files as objects
scroll_top_image = Image.open("scroll_top.png").convert("RGBA")
scroll_middle_image = Image.open("scroll_middle.png").convert("RGBA")
scroll_bottom_image = Image.open("scroll_bottom.png").convert("RGBA")
achievement_diary_icon = Image.open("Achievement_Diaries_icon.png").convert("RGBA")

# Merge all the image files into 1 big image
image = vertical_merge(scroll_top_image, scroll_middle_image)
image = vertical_merge(image, scroll_middle_image)
image = vertical_merge(image, scroll_middle_image)
image = vertical_merge(image, scroll_bottom_image)

# Add the achievement diary icon on the image (yh i know, magic numbers, cba)
top_banner_width, top_banner_height = scroll_top_image.size
STARTING_Y = top_banner_height + HEADING_PADDING
image.paste(achievement_diary_icon, (ACHIEVE_DIARY_X, top_banner_height), achievement_diary_icon)

# Prints the dimensions of the image.
print(image.format, image.size, image.mode)
W,H = image.size

# Fonts for the program, found these in the fonts folder in windows, might be different on a seperate system.
try:
    font = ImageFont.truetype("arial.ttf", size=13)
    heading_font = ImageFont.truetype("arialbd.ttf", size=13)
except:
    font = ImageFont.load_default()
    heading_font = font
    print("Default font loaded, arial couldn't be found")

draw = ImageDraw.Draw(image)

# Creating the generator, so we can iterate through data from each row.
dg = data_gen()

### Drawing the headings
y = STARTING_Y

draw.text(((W)/2,y), "Totus Hiscores", font=heading_font, anchor="mt", fill=BLACK)
y += PADDING + (HEADING_PADDING*2)

draw.text((CUM_COL_LEN[0], y), "#", font=heading_font, align="right", anchor="rs", fill=BLACK)
draw.text((CUM_COL_LEN[0]+10, y), "Name", font=heading_font, align="left", anchor="ls", fill=BLACK)
draw.text((CUM_COL_LEN[2],y), "Rank", font=heading_font, align="right", anchor="rs", fill=BLACK)
draw.text((CUM_COL_LEN[3],y), "Points", font=heading_font, align="right", anchor="rs", fill=BLACK)

y += PADDING + HEADING_PADDING

# Iterate through the rows and draw the relavent data on the image.
i = 0
for row in dg:
    if i > 25:
        break
    leader_board_rank = row[0]
    member_name = row[1]
    totus_rank = rank_conversion_dict[row[2]]
    totus_points = row[3]
    
    draw.text((CUM_COL_LEN[0], y), leader_board_rank, font=font, align="right", anchor="rs", fill=BLACK)
    # Names are left aligned, so used the edge of the first value.
    draw.text((CUM_COL_LEN[0]+10, y), member_name, font=font, align="left", anchor="ls", fill=BLACK)
    draw.text((CUM_COL_LEN[1],y), totus_rank, font=font, align="right", anchor="ls", fill=BLACK)
    draw.text((CUM_COL_LEN[3],y), totus_points, font=font, align="right", anchor="rs", fill=BLACK)
    
    y += PADDING

    i += 1

image.show()
#image.save("totus_hiscore_image.png")
