from django.core.management.base import BaseCommand
import requests
from requests.auth import HTTPBasicAuth
from api.models import ProductModel, CollectionCategoryModel, CollectionModel, CollectionImagesModel
from django.core.files.base import ContentFile
import re
from bs4 import BeautifulSoup
from pages.models import Catalog

def has_cyrillic(text):
    return bool(re.search('[а-яА-Я]', text))


class Command(BaseCommand):

    def handle(self, *args, **options):
        resp = requests.get('https://www.weltew.com/en/e-catalog')
        soup = BeautifulSoup(resp.text, 'html.parser')
        catalogs = soup.select('.catalogPage .item')
        for catalog in catalogs:
            image = catalog.select_one('img')
            image_url = image.get('data-src')
            image_name = image_url.split('/')[-1]
            title = catalog.select_one('h2').text
            catalog, c = Catalog.objects.get_or_create(title=title)
            catalog.image.save(image_name, ContentFile(requests.get(image_url).content))
        #     file_url = catalog.select_one('a').get('href')
        #     file_name = file_url.split('/')[-1]
        #     file = requests.get(file_url)
        #     title = catalog.select_one('h2').text
        #     image_url = catalog.select_one('img').get('src')
        #     image_name = image_url.split('/')[-1]
        #     image = requests.get(image_url)
        #     catalog, c = Catalog.objects.get_or_create(title=title)
        #     if c:
        #         catalog.file.save(file_name, ContentFile(file.content))
        #         catalog.image.save(image_name, ContentFile(image.content))
        #         catalog.save()
        # collections = CollectionModel.objects.all()
        # for collection in collections:
        #     collection.name = collection.name.replace(collection.category.name, '')
        #     collection.save()

        # collections = CollectionModel.objects.all()
        # for collection in collections:
        #     resp = requests.get('https://www.weltew.com' + collection.url)
        #     soup = BeautifulSoup(resp.text, 'html.parser')

        #     images = soup.select('.big img')
        #     for image in images:
        #         img_url = image.get('data-src')
        #         if img_url:
        #             img, c = CollectionImagesModel.objects.get_or_create(
        #                 url=img_url)
        #             if c:
        #                 img.collection = collection
        #                 print(img_url.split('/')[-1])
        #                 img.image.save(img_url.split('/')[-1], ContentFile(requests.get(img_url).content))
        #                 img.save()

        #     desc = soup.select_one('.text-box')
        #     collection.description = desc.contents[0]
        #     print(desc.contents[0])

            # products = soup.select('.col-md-4 .item')
            # for product in products:
            #     name = product.select_one('.name').text
            #     url = product.select_one('a')['href']
            #     collection, c = CollectionModel.objects.get_or_create(url=url)
            #     collection.category = category
            #     collection.name = name
            #     collection.save()

        # resp = requests.get('https://www.weltew.com/en/sets/')
        # soup = BeautifulSoup(resp.text, 'html.parser')
        # cards = soup.select('.col-md-4 .item')
        # for card in cards:
        #     img = card.select_one('img')
        #     name = card.select_one('.name').text
        #     url = card.select_one('a')['href']
        #     cat, c = CollectionCategoryModel.objects.get_or_create(url=url)
        #     cat.name = name
        #     cat.image.save(f'{name}.jpg', ContentFile(requests.get(img['src']).content))
        #     cat.save()
        #     print(cat)

        # products = ProductModel.objects.all()
        # count = 0
        # collection = "ALACATI"
        # ps = []
        # for product in products:
        #     if (product.sklad_collection != collection):
        #         collection = product.sklad_collection
        #         count = 1
        #         ps = []
        #         ps.append(product)
        #     else:
        #         count += 1
        #         ps.append(product)
        #     if (count > 4):
        #         c = CollectionModel.objects.get(name=collection)
        #         print(c)
        #         for p in ps:
        #             c.products.add(p)

            # cat = ProductCategoryModel.objects.filter(name__contains=product.sklad_cat)
            # if len(cat):
            #     product.category = cat[0]
            #     product.save()
            # else:
            #     cat = ProductCategoryModel.objects.filter(name__contains=product.sklad_cat_2)
            #     if len(cat):
            #         product.category = cat[0]
            #         product.save()

            # ProductCategoryModel.objects.get_or_create(name=product.sklad_cat)
            #         category = ProductCategoryModel.objects.get(name=c)
            #         product.category = category
            #         product.save()
            #         break
            # if (product.sklad_cat == ""):
            #     print(product.id)
            # else:
            #     print(product.sklad_cat.replace(' ', ''))
