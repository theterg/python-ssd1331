from PIL import Image, ImageChops, ImageDraw, ImageFont


class PILGFX:
    def __init__(self, display):
        self.d = display
        self.buff = Image.new("RGBA", (96, 64), (0, 0, 0, 255))
        self.last = self.buff.copy()
        self.font = ImageFont.load_default()

    def display(self):
        diff = ImageChops.difference(self.last, self.buff)
        bounds = diff.getbbox()
        if bounds is None:
            # buff is the same as last, nothing to do!
            return
        left, upper, right, lower = bounds
        #for y in range(self.buff.size[1]):
        for y in range(upper, lower):
            # TODO - if more than FOO pixels are all the same, use drawLine instead
            #for x in range(self.buff.size[0]):
            for x in range(left, right):
                # Only draw pixels that are different
                rd, gd, bd, ad = diff.getpixel((x,y))
                rb, gb, bb, ab = self.buff.getpixel((x,y))
                # If any of the pixels have changed, AND
                # The current buffer has opacity in this pixel
                if (rd != 0 or gd != 0 or bd != 0) and ab > 0:
                    r,g,b,a = self.buff.getpixel((x,y))
                    self.d.drawPixel(x, y, r, g, b)
        # Set all black pixels to transparent, so they don't need to be re-written
        # pixels = self.buff.load()
        # for x in range(self.buff.size[0]):
        #     for y in range(self.buff.size[1]):
        #         r,g,b,a = pixels[x,y]
        #         if r == 0 and g == 0 and b == 0:
        #             pixels[x,y] = (r, g, b, 0)
        self.last = self.buff.copy()

    def drawImageDiff(self, im):
        self.buff.paste(im, im)
        #diff = ImageChops.difference(im, self.bg)
        #left, upper, right, lower = im.getbbox()
        #for x in range(left, right):
        #    for y in range(upper, lower):
        #        # Only draw pixels that are different
        #        r,g,b = diff.getpixel((x,y))
        #        if r != 0 or g != 0 or b != 0:
        #            # draw original pixel values, not the diff
        #            r,g,b = im.getpixel((x,y))
        #            self.d.drawPixel(x, y, r, g, b)
        #            # Probably a more efficient way to do this,
        #            # but would like to avoid transparency atm
        #            self.bg.putpixel((x,y),(r,g,b))

    def drawText(self, xy, text, color=(255, 255, 255, 255)):
        if len(color) == 3:
            color = (color[0], color[1], color[2], 255)
        im = Image.new("RGBA", (96,64), (0, 0, 0, 0))
        draw = ImageDraw.Draw(im)
        font = ImageFont.load_default()
        draw.text(xy, text, color, font=font)
        self.drawImageDiff(im)
        return im

    def clearLines(self, y1, y2):
        im = self.buff.copy()
        draw = ImageDraw.Draw(im)
        draw.rectangle(((0,y1),(96,y2)), fill=(0, 0, 0, 255))
        self.buff.paste(im, self.buff)
        #for y in range(y1, y2):
        #    self.d.drawLine(0, 96, y, y, 0, 0, 0)

    def getblank(self):
        return Image.new("RGBA", (96,64), (0, 0, 0, 0))

    def getfont(self):
        return self.font

    def setfont(self, font):
        self.font = font

def testText():
    im = Image.new("RGBA", (96,64), (0, 0, 0, 0))
    draw = ImageDraw.Draw(im)
    font = ImageFont.load_default()
    draw.text((10, 0), "Testing", (255, 200, 100, 255), font=font)
    return im

#from SSD1331 import *
#s = SSD1331()
#g = PILGFX(s)
#im = testText()
