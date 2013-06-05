.. important:: This document is a proposal.

=========
Resources
=========

To get a good overview of what REST api means, consider reading `Web Api Design,
Crafting interface that Developers love <http://offers.apigee.com/api-design-ebook-rr/>`_.

- :ref:`users` is the collection of registered users.

- :ref:`reports` is a collection of geolocalized reports submitted by users.

- :ref:`photos` is a collection of geolocalized photos.


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


.. note::
   Unless specified, all parameters are required and cannot be empty.

.. _users:

Users
*****

To be done

.. _reports:

Reports
*******

**GET** :file:`/reports?location={longitude},{latitude}&radius={radius}&page={index}&page_size={size}`
   Returns a paginated list of reports. If no parameter is provided, reports
   in antechronological order (newests first).

   Optionnal query parameters:

      :location: The longitude/latitude around which to retrieve information.
                 This must be specified as `longitude,latitude`.

      :radius: Defines the distance in meters within which to return results.
               Default to 50.
      :page: Page index of result set. Default to 0 (first page).
      :page_size: Number of reports returned by page, default to 20.

   Response format example for `/reports?location=-73.583885,45.522706&page_size=2&page=1`::

      {
         "reports":
            [
               {
                  "report":
                     {
                        "_id": "5183bef9e2a9c30005648611",
                        "author": "devon",
                        "description": "Water all over the street.",
                        "created": "2013-03-28T09:15:12+00:00",
                        "location":
                           {
                              "type": "Point",
                              "coordinates": [73.59432, 45.5233]
                           },
                        "tags": ["accident", "water"],
                        "report_photos":
                           {
                              "photos":
                                 [
                                    {
                                       "photo":
                                          {
                                             "_id": "5118fe5ab821d90005c1a24d",
                                             "author": "devon",
                                             "location":
                                                {
                                                   "type": "Point",
                                                   "coordinates": [-73.583885, 45.522706]
                                                }
                                          },
                                       "links":
                                          {
                                             "self": "http://api.velobstacles.com/photo/5118fe5ab821d90005c1a24d",
                                             "report": "http://api.velobstacles.com/report/5183bef9e2a9c30005648611",
                                             "author": "http://api.velobstacles.com/users/519f7c699978d00472bab9e7",
                                             "thumbnail": "http://cdn.velobstacles.com/d64c1cefeda4dadf695d3edd47ef1d85",
                                             "original_resolution": "http://cdn.velobstacles.com/3d5e2f6f37c8ab46ec7cb3a29bfb0bca",
                                             "low_resolution": "http://cdn.velobstacles.com/8cb4f88ffd80dac9c59859dcea8e2ae4"
                                          }
                                    }
                                 ],
                              "links":
                                 {
                                    "self": "http://api.velobstacles.com/reports/5183bef9e2a9c30005648611/photos",
                                    "report": "http://api.velobstacles.com/reports/5183bef9e2a9c30005648611"
                                 }
                           }
                     },
                  "links":
                     {
                        "self": "http://api.velobstacles.com/reports/5183bef9e2a9c30005648611",
                        "photos": "http://api.velobstacles.com/reports/5183bef9e2a9c30005648611/photos",
                        "author": "http://api.velobstacles.com/users/519f7c699978d00472bab9e7"
                     }
               },
               {
                  "report":
                     {
                        "_id": "5183c05ee2a9c30005648624",
                        "author": "rob_ford",
                        "description": "Big crack on road",
                        "created": "2013-03-28T09:15:12+00:00",
                        "location":
                           {
                              "type": "Point",
                              "coordinates": [73.5856, 45.5233]
                           },
                        "tags": ["working site"],
                        "report_photos": null
                     },
                  "links":
                     {
                        "self": "http://api.velobstacles.com/reports/5183c05ee2a9c30005648624"
                     }
               }
            ],
         "links":
            {
               "self": "http://api.velobstacles.com/reports?location=-73.583885,45.522706&radius=50&page=1&page_size=2",
               "previous": "http://api.velobstacles.com/reports?location=-73.583885,45.522706&radius=50&page=0&page_size=2",
               "next": "http://api.velobstacles.com/reports?location=-73.583885,45.522706&radius=50&page=2&page_size=2",
               "first": "http://api.velobstacles.com/reports?location=-73.583885,45.522706&radius=50&page=0&page_size=2",
               "last": "http://api.velobstacles.com/reports?location=-73.583885,45.522706&radius=50&page=11&page_size=2"
            }
      }


**GET** :file:`/reports/{_id}`
   Returns a report.

   Response format example::

      {
         "report":
            {
               "_id": "5183bef9e2a9c30005648611",
               "author": "devon",
               "description": "Water all over the street.",
               "created": "2013-03-28T09:15:12+00:00",
               "location":
                  {
                     "type": "Point",
                     "coordinates": [73.59432, 45.5233]
                  },
               "tags": ["accident", "water"],
               "report_photos":
                  {
                     "photos":
                        [
                           {
                              "photo":
                                 {
                                    "_id": "5118fe5ab821d90005c1a24d",
                                    "author": "devon",
                                    "location":
                                       {
                                          "type": "Point",
                                          "coordinates": [-73.583885, 45.522706]
                                       }
                                 },
                              "links":
                                 {
                                    "self": "http://api.velobstacles.com/photo/5118fe5ab821d90005c1a24d",
                                    "report": "http://api.velobstacles.com/report/5183bef9e2a9c30005648611",
                                    "author": "http://api.velobstacles.com/users/519f7c699978d00472bab9e7",
                                    "thumbnail": "http://cdn.velobstacles.com/d64c1cefeda4dadf695d3edd47ef1d85",
                                    "original_resolution": "http://cdn.velobstacles.com/3d5e2f6f37c8ab46ec7cb3a29bfb0bca",
                                    "low_resolution": "http://cdn.velobstacles.com/8cb4f88ffd80dac9c59859dcea8e2ae4"
                                 }
                           }
                        ],
                     "links":
                        {
                           "self": "http://api.velobstacles.com/reports/5183bef9e2a9c30005648611/photos",
                           "report": "http://api.velobstacles.com/reports/5183bef9e2a9c30005648611"
                        }
                  }
            },
         "links":
            {
               "self": "http://api.velobstacles.com/reports/5183bef9e2a9c30005648611",
               "photos": "http://api.velobstacles.com/reports/5183bef9e2a9c30005648611/photos",
               "author": "http://api.velobstacles.com/users/519f7c699978d00472bab9e7"
            }
      }

**POST** :file:`/reports`
   Submit a report.

   Required parameters:

      :author: Author's username
      :description:
      :longitude:
      :latitude:
      :tags: A list of tags.

   HTTP response header example::

      HTTP/1.1 201 Created
      Connection: keep-alive
      Content-Length: 116
      Content-Type: application/json; charset=UTF-8
      Date: Tue, 21 May 2013 16:25:29 GMT
      Location: http://api.velobstacles.com/reports/5183bef9e2a9c30005648611

   Response format example::

      {
         "report":
            {
               "_id": "5183bef9e2a9c30005648611",
               "author": "devon",
               "description": "Water all over the street.",
               "created": "2013-03-28T09:15:12+00:00",
               "location":
                  {
                     "type": "Point",
                     "coordinates": [73.59432, 45.5233]
                  },
               "tags": ["accident", "water"]
            },
         "links":
            {
               "self": "http://api.velobstacles.com/reports/5183bef9e2a9c30005648611",
               "photos": "http://api.velobstacles.com/reports/5183bef9e2a9c30005648611/photos",
               "author": "http://api.velobstacles.com/users/519f7c699978d00472bab9e7"
            }
      }

**DELETE** :file:`/reports/{_id}`
   Delete a report.

.. _photos:

Photos
******

**GET** :file:`/photos?page={index}&page_size={size}`
   Get photo list.

   Optionnal query parameters:

      :radius: Defines the distance in meters within which to return results.
               Default to 50.
      :page: Page index of result set. Default to 0 (first page).
      :page_size: Number of photos returned by page, default to 20.

   Response format example for `/photos?page=1&page_size=2`::

      {
         "photos":
            [
               {
                  "photo":
                     {
                        "_id": "5118fe5ab821d90005c1a24d",
                        "author": "devon",
                        "location":
                           {
                              "type": "Point",
                              "coordinates": [-73.583885, 45.522706]
                           }
                     },
                  "links":
                     {
                        "self": "http://api.velobstacles.com/photo/5118fe5ab821d90005c1a24d",
                        "report": "http://api.velobstacles.com/report/5183bef9e2a9c30005648611",
                        "author": "http://api.velobstacles.com/users/519f7c699978d00472bab9e7",
                        "thumbnail": "http://cdn.velobstacles.com/d64c1cefeda4dadf695d3edd47ef1d85",
                        "original_resolution": "http://cdn.velobstacles.com/3d5e2f6f37c8ab46ec7cb3a29bfb0bca",
                        "low_resolution": "http://cdn.velobstacles.com/8cb4f88ffd80dac9c59859dcea8e2ae4"
                     }
               },
               {
                  "photo":
                     {
                        "_id": "51367fa288a8be000596e2a1",
                        "location":
                           {
                              "type": "Point",
                              "coordinates": [-73.583885, 45.522706]
                           }
                     },
                  "links":
                     {
                        "self": "http://api.velobstacles.com/photo/51367fa288a8be000596e2a1",
                        "report": "http://api.velobstacles.com/report/5183bef9e2a9c30005648611",
                        "thumbnail": "http://cdn.velobstacles.com/0da8c9479b837745ef625f875c3f0e1b",
                        "original_resolution": "http://cdn.velobstacles.com/a598b26963ec7f531aaabdd447f60c02",
                        "low_resolution": "http://cdn.velobstacles.com/8cb4f88ffd80dac9c59859dcea8e2ae4"
                     }
               }

            ],
         "links":
         {
            "self": "http://api.velobstacles.com/media?page=1&page_size=2",
            "previous": "http://api.velobstacles.com/media?page=0&page_size=2",
            "next": "http://api.velobstacles.com/media?page=2&page_size=2",
            "first": "http://api.velobstacles.com/media?page=0&page_size=2",
            "last": "http://api.velobstacles.com/media?page=5&page_size=2"
         }
      }


