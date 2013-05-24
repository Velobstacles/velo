
.. important::
   Deprecated

Medium: /media
--------------

Medium is a photo/video associated to gps location. Example::

    {
        "links": {
            "content": "http://0.0.0.0:6543/media/50aab36b9978d001f3be41b6/content",
            "self": "http://0.0.0.0:6543/media/50aab36b9978d001f3be41b6"
        },
        "_id": "50aab36b9978d001f3be41b6",
        "location": {
            "type": "Point",
            "coordinates": [-73.583885, 45.522706]
        }
    }


* To create a medium, issue an ``HTTP POST`` request on endpoint ``/media`` using
  ``multipart/form-data`` encoding.
* Required fields are:

    * longitude
    * latitude
    * content: an image file
