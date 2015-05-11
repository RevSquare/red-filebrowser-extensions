Red File Browser Extensions
==================

This library and its are being rewritten. It contans various fixes and new features:

* fixed jquery version conflict blocking the widget
* removing crop in the image library and put it directly in the original instance form field
* previous change allows to filter and contextualise better the available list of versions in the select which was way to big and confusing on projects using a large amount of versions
* added some filters to add in the FILEBROWSER_VERSIONS dictionnary in settings see below in 'settings'
* added a templatetag to easily trigger the version filepath plus the dimensions set in the settings. It allows to very easily combine this library with Sorl thumbnail for instance. This change was needed in order to make the library much more flexible. It has 2 major flaws: user had to manually crop the image or it would appear in its original dimensions, and if you need to change the dimension of the version because of a design change, you would have to recrop all the library, yuck!

Crop FileBrowser is an extension to FileBrowser <https://github.com/sehmaschine/django-filebrowser/>` that allows you to use JCrop <http://deepliquid.com/content/Jcrop.html> to create custom crops for your image versions:

Requirements
------------

* FileBrowser 3.4.3
* Django 1.3 (http://www.djangoproject.com)
* Grappelli 2.3.7 (https://github.com/sehmaschine/django-grappelli)
* PIL (http://www.pythonware.com/products/pil/)

Installation
------------

python setup.py install

Open settings.py and add crop_filebrowser to your INSTALLED_APPS if you want access to the filebrowser management commands you should include it as well:

    INSTALLED_APPS = (
        'grappelli',
        'crop_filebrowser',
        'filebrowser',
        'django.contrib.admin',
    )

In your url.py import the default CropFileBrowser site:

from crop_filebrowser.sites import site
and add the following URL-patterns (before any admin-urls):

urlpatterns = patterns('',
   url(r'^admin/filebrowser/', include(site.urls)),
)

Crop versions filter
--------------------

In order to contectualize the cropping options better you can restrict the list of available versions by using 2 news attributes in the FILEBROWSER_VERSIONS dictionnary in settings.

* 'filter_model': is a list or tuple of model names in lowercases (as it appears in the admin urls) to only display the version when its form is triggered from an object belonging to such model.
* 'filter_field': uses the class name of the form to only display the version when its form is triggered from a field named as such.

ie:

FILEBROWSER_VERSIONS = {
    'admin_thumbnail': {
        'verbose_name': 'Admin Thumbnail',
        'width': 100,
        'height': 75,
        'opts': 'crop',
        'filter_model': ('',)
    },
    'article_detail': {
        'verbose_name': 'Article detail page main image',
        'width': 600,
        'height': 400,
        'opts': 'crop',
        'filter_model': ('news',),
        'filter_field': ('image',)
    },
}

The exemple above will only be triggered if the crop form is opened from a form of a news object in the field named 'image'. 

For inlines, you can use the name of the fields prefixed before the id. On the following exemple, you would use 'news' because the name attribute 'news-0-image' has 'news' before the id / number of the inline: 

<input id="id_news-0-image" class="vFileBrowseField" type="text" value="my-image.jpg" name="news-0-image">

Templatetags
------------

A templatetag has been added to easily trigger the original dimensions set in for versions in settings. The template tag library is called *crop_filebrowser* and the tag *version_object_thumbnail* overwrites the original filebrowser version *version_object* tag. It adds a *version_dimensions* attribute to your generated version object.

An exemple might be more helpful!

{% load static thumbnail crop_filebrowser %}

{% version_object_thumbnail news.image 'news_homepage' as object_image %}  
{% thumbnail object_image object_image.version_dimensions crop="center" as im %}
    <img src="{{ im.url }}" alt="{{ news.title }}">
{% endthumbnail %}

Lantip Notes
------------
patched crop_filebrowser.sites to be able to work with filebrowser 3.5+
