

Report: /report
---------------

Report::

  {
    "timestamp": datetime,
    "location": {
      "longitude": long,
      "latitude": long,
      },
    "altitude": long,
    "tags": [],
    "media_list": [],
    "description": unicode,
    "temperature": long,
    "light/luminosity": unicode     #  from timestamp?

    "metadata": {
      "device": {
        "id": unicode,
        "resolution": {
          "width": int,
          "height": int,
        },
        "user-agent": unicode,
      },
      "locale": unicode,
    },
  }


Tag
---

Tag::

  {
    "name": unicode,
    "id": ,
  }
