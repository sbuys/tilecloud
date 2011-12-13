import PIL.Image

from tilecloud import BoundingPyramid, Tile, TileCoord, TileStore


class MaskTileStore(TileStore):
    """A black and white image representing present and absent tiles"""

    def __init__(self, z, slices, file=None):
        self.z = z
        self.xbounds, self.ybounds = slices
        self.width = self.xbounds.stop - self.xbounds.start
        self.height = self.ybounds.stop - self.ybounds.start
        if file:
            self.image = PIL.Image.open(file)
            assert self.image.mode == '1'
            assert self.image.size == (self.width, self.height)
        else:
            self.image = PIL.Image.new('1', (self.width, self.height))
        self.pixels = self.image.load()

    def delete_one(self, tile):
        if tile.tilecoord.z == self.z:
            x = tile.tilecoord.x - self.xbounds.start
            y = self.ybounds.stop - tile.tilecoord.y - 1
            if 0 <= x < self.width and 0 <= y < self.height:
                self.pixels[x, y] = 0
        return tile

    def get_bounding_pyramid(self):
        return BoundingPyramid({self.z: (self.xbounds, self.ybounds)})

    def list(self):
        for x in xrange(0, self.width):
            for y in xrange(0, self.height):
                if self.pixels[x, y]:
                    yield Tile(TileCoord(self.z, self.xbounds.start + x, self.ybounds.stop - y - 1))

    def put_one(self, tile):
        x = tile.tilecoord.x - self.xbounds.start
        y = self.ybounds.stop - tile.tilecoord.y - 1
        if 0 <= x < self.width and 0 <= y < self.height:
            self.pixels[x, y] = 1
        return tile

    def save(self, file, format, **kwargs):
        self.image.save(file, format, **kwargs)