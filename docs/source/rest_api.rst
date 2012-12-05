REST API
========

To get a good overview of what REST api means, consider reading `Web Api Design,
Crafting interface that Developers love <http://offers.apigee.com/api-design-ebook-rr/>`_.


Principles
----------

- The standard format for input is application/x-www-form-urlencoded and
  multipart/form-data. See `W3C recommendation <http://www.w3.org/TR/html401/interact/forms.html#h-17.13.4>`_
  for more info.
- The standard format for output is JSON.
- A successful ``POST`` (used to create a new resource) will return HTTP 201
  (created). The newly-created resource's URL is contained in the "Location"
  header of the HTTP response.
- A successful ``PUT`` (used to change an existing resource or create a resource
  which URL is known before creation) will return HTTP 200 (OK).
- A ``PUT`` call may not make any changes to a resource that would change its
  URL.
- Attempting to call a method on a type that doesn't support it regardless of
  authentication (e.g. ``PUT`` or ``POST`` on read-only resources) will raise
  HTTP error 405 (method not supported).
- Attempting to call a method on a resource that doesn't exist will raise HTTP
  error 404 (not found).
- Likewise, attempting to create a resource with a reference to something that
  doesn't exist will raise HTTP 404.
- Missing, or incorrectly-formatted, parameters (e.g. letters in numeric
  parameters, negative quantities where disallowed) will raise HTTP 400 (bad
  request).


Medium: /media
--------------

Medium is a photo/video associated to gps location. Example::

    {
        "links": {
            "content": "http://0.0.0.0:6543/media/50aab36b9978d001f3be41b6/content",
            "self": "http://0.0.0.0:6543/media/50aab36b9978d001f3be41b6"
        },
        "creation_datetime": "2012-11-19T22:32:11.375000+00:00",
        "id": "50aab36b9978d001f3be41b6",
        "mime_type": "image/jpeg",
        "location": {
            "latitude": 123,
            "longitude": 23
        }
    }


* To create a medium, issue an ``HTTP POST`` request on endpoint ``/media`` using
  ``multipart/form-data`` encoding.
* Required fields are:

    * latitude
    * longitude
    * content: an image file

* For test purpose, you can also use a basic form on ``/media/new`` which issues
  a valid creation ``HTTP POST`` request.
