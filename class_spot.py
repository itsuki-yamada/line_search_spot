class AreaCode(object):
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def get_info(self):
        return f'{self.name}'


class Restaurant(object):
    def __init__(self, id, name, ac, address, mobile_url=None, access=None, lat=0.0, lon=0.0, image=None):
        self.id = id
        self.name = name
        self.ac = ac
        self.address = address
        self.mobile_url = mobile_url
        self.access = access
        self.lat = lat
        self.lon = lon
        self.image = image

    def edit_mobile_url(self, mobile_url=None):
        self.mobile_url = mobile_url

    def edit_access(self, access=None):
        self.access = access

    def get_info(self):
        return f'{self.name}\n' \
               f'{self.access}\n' \
               f'{self.mobile_url}'

    def edit_image(self, image):
        self.image = image
