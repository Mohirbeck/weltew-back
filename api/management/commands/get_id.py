from django.core.management.base import BaseCommand
import requests
from requests.auth import HTTPBasicAuth
from api.models import ProductModel, ProductImagesModel, ProductCategoryModel, CollectionModel
from django.core.files.base import ContentFile
import re


def has_cyrillic(text):
    return bool(re.search('[а-яА-Я]', text))


class Command(BaseCommand):
    help = "Get product id 659 in total"

    def handle(self, *args, **options):
        urls = [
            "https://online.moysklad.ru/api/remap/1.2/entity/assortment",
            "https://online.moysklad.ru/api/remap/1.2/entity/assortment?offset=1000",
            "https://online.moysklad.ru/api/remap/1.2/entity/assortment?offset=2000",
        ]
        for url in urls:

            response = requests.get(
                url,
                auth=HTTPBasicAuth("sklad@nikitkakodenko", "usmon0078914"),
            )
            data = response.json()
            count = 0
            for product in data["rows"]:
                if 'pathName' in product.keys():
                    if "WELTEW" in product["pathName"]:
                        if 'code' in product.keys():
                            pr, c = ProductModel.objects.get_or_create(
                                code=product['code'])
                            pr.sklad_collection = product['pathName'].split(
                                '/')[-1]
                            if 'attributes' in product.keys():
                                attributes = {
                                    attribute["name"]: attribute["value"] for attribute in product["attributes"]}
                                if 'Комплектация' in attributes.keys():
                                    cat = attributes['Комплектация'].split('|')
                                    for c in cat:
                                        if has_cyrillic(c):
                                            pr.sklad_cat = c
                                            break
                                if 'Категория' in attributes.keys():
                                    cat = attributes['Категория'].split('|')
                                    for c in cat:
                                        if has_cyrillic(c):
                                            pr.sklad_cat_2 = c
                                            break
                            if c:
                                imgs_url = product["images"]["meta"]["href"]
                                imgs_response = requests.get(
                                    imgs_url,
                                    auth=HTTPBasicAuth(
                                        "sklad@nikitkakodenko", "usmon0078914"),
                                )
                                imgs_data = imgs_response.json()
                                for img in imgs_data['rows']:
                                    i, cr = ProductImagesModel.objects.get_or_create(
                                        url=img['meta']['downloadHref'])
                                    if cr:
                                        img_response = requests.get(
                                            img['meta']['downloadHref'],
                                            auth=HTTPBasicAuth(
                                                "sklad@nikitkakodenko", "usmon0078914"),
                                        )
                                        i.image.save(img['filename'], ContentFile(
                                            img_response.content))
                                    i.product = pr
                                    i.save()

                                pr.name = product['name']

                            pr.url = product['meta']['href']
                            pr.price = int(
                                product['salePrices'][0]['value']) / 100
                            if "stock" in product.keys():
                                if product['stock'] > 0:
                                    pr.availibility = True
                                else:
                                    pr.availibility = False
                            else:
                                pr.availibility = False
                            pr.save()
