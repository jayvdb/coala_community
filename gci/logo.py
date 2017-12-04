import os
import requests


def get_logo():
    # Obtain the org name from the Travis environment variables
    org_name = os.environ['TRAVIS_REPO_SLUG'].split('/')[0]

    image_url_short_max_res = 'http://github.com/%s.png' % (org_name)

    # Follow the redirect to the page containing the image and
    # store it in the response variable
    response_max_res = requests.get(image_url_short_max_res)

    # Write the image to a file and save
    image = open('images/org_logo.png', 'wb')
    image.write(response_max_res.content)
    image.close()

    # Run the same code again but download a 16x16 version for favicon
    image_url_short_favicon = 'http://github.com/%s.png?size=16' % (org_name)

    response_favicon = requests.get(image_url_short_favicon)

    image = open('favicon.png', 'wb')
    image.write(response_favicon.content)
    image.close()
