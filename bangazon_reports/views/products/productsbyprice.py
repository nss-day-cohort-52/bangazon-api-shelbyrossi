"""Module for generating games by user report"""
from django.shortcuts import render
from django.db import connection
from django.views import View

from bangazon_reports.views.helpers import dict_fetch_all


class ProductPriceList(View):
    def get(self, request):
        with connection.cursor() as db_cursor:

            # TODO: Write a query to get all games along with the gamer first name, last name, and id
            db_cursor.execute("""
            SELECT P.price, P.name ProductName, S.name StoreName
            FROM bangazon_api_product P
            JOIN bangazon_api_store S 
            ON P.store_id = S.id
            WHERE price > 500
            """)
            # Pass the db_cursor to the dict_fetch_all function to turn the fetch_all() response into a dictionary
            dataset = dict_fetch_all(db_cursor)
            
            products_over_1000 = []
            
            for row in dataset:
                product = {
                    "price": row['price'],
                    "product_name": row['ProductName'],
                    "store_name": row['StoreName']    
                }
                
                products_over_1000.append(product)
                
        template = 'product_expensive.html'
        
        # The context will be a dictionary that the template can access to show data
        context = {
            "product_list": products_over_1000
        }

        return render(request, template, context)