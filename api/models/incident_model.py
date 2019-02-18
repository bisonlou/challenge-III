from flask import json


class Incident():
    statuses = ['Pending', 'Under investigation', 'Resolved', 'Rejected']

    def __init__(self, **kwags):
        self._id = kwags.get('id', 0)
        self._title = kwags.get('title', '')
        self._createdon = kwags.get('createdon', '')
        self._comment = kwags.get('comment', '')
        self._createdby = kwags.get('createdby', '')
        self._latitude = kwags.get('latitude', 0.0)
        self._longitude = kwags.get('longitude', 0.0)
        self._status = kwags.get('status', '')
        self._type = kwags.get('type', '')
        self._images = []
        self._videos = []

    def add_image(self, name):
        self._images.append(name)

    def add_video(self, name):
        self._videos.append(name)

    @property
    def id(self):
        return self._id

    @property
    def createdon(self):
        return self._createdon

    @property
    def createdby(self):
        return self._createdby

    @property
    def title(self):
        return self._title

    @property
    def comment(self):
        return self._comment

    @property
    def latitude(self):
        return self._latitude

    @property
    def longitude(self):
        return self._longitude

    @property
    def videos(self):
        return self._videos

    @property
    def images(self):
        return self._images

    @property
    def status(self):
        return self._status

    @property
    def type(self):
        return self._type

    @createdon.setter
    def created_on(self, created_on):
        self._createdon = created_on

    @title.setter
    def title(self, title):
        self._title = title

    @comment.setter
    def comment(self, comment):
        self._comment = comment

    @latitude.setter
    def latitude(self, latitude):
        self._latitude = latitude

    @longitude.setter
    def longitude(self, longitude):
        self._longitude = longitude

    @images.setter
    def images(self, images):
        self._images = images

    @videos.setter
    def videos(self, videos):
        self._videos = videos

    @status.setter
    def status(self, status):
        self._status = status

    def to_dict(self):
        return dict(id=self._id,
                    createdon=self._createdon,
                    createdby=self._createdby,
                    title=self._title,
                    comment=self._comment,
                    latitude=self._latitude,
                    longitude=self._longitude,
                    type=self._type,
                    status=self._status,
                    images=self._images,
                    videos=self._videos
                    )
