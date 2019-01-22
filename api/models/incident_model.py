from flask import json

redflag_table = []
intervention_table = []


class Incident():
    statuses = ['Pending', 'Under investigation', 'Resolved', 'Rejected']

    def __init__(self, **kwags):
        self._id = kwags.get('id', 0)
        self._title = kwags.get('title', '')
        self._created_on = kwags.get('created_on', '')
        self._comment = kwags.get('comment', '')
        self._created_by = kwags.get('created_by', '')
        self._location = kwags.get('location', '')
        self._status = kwags.get('status', '')
        self._incident_type = kwags.get('type', '')
        self._images = kwags.get('images', list())
        self._videos = kwags.get('videos', list())

    @property
    def id(self):
        return self._id

    @property
    def created_on(self):
        return self._created_on

    @property
    def created_by(self):
        return self._created_by

    @property
    def title(self):
        return self._title

    @property
    def comment(self):
        return self._comment

    @property
    def location(self):
        return self._location

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
    def incident_type(self):
        return self._incident_type

    @created_on.setter
    def created_on(self, created_on):
        self._created_on = created_on

    @title.setter
    def title(self, title):
        self._title = title

    @comment.setter
    def comment(self, comment):
        self._comment = comment

    @location.setter
    def location(self, location):
        self._location = location

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
                    created_on=self._created_on,
                    created_by=self._created_by,
                    title=self._title,
                    comment=self._comment,
                    location=self._location,
                    type=self._incident_type,
                    status=self._status,
                    images=self._images,
                    videos=self._videos
                    )

