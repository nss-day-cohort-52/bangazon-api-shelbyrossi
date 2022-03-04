"""Module for generating games by user report"""
from django.shortcuts import render
from django.db import connection
from django.views import View

from bangazon_reports.views.helpers import dict_fetch_all


class FavoriteStores(View):
    def get(self, request):
        with connection.cursor() as db_cursor:

            
            db_cursor.execute("""
            
            select a.first_name, a.last_name, s.name, f.customer_id, s.id
            from bangazon_api_favorite f
            join bangazon_api_store s on s.id=f.store_id
            join auth_user a on a.id = f.customer_id
            
            """)
            # Pass the db_cursor to the dict_fetch_all function to turn the fetch_all() response into a dictionary
            dataset = dict_fetch_all(db_cursor)

            # Take the flat data from the dataset, and build the
            # following data structure for each gamer.
            # This will be the structure of the favorite_store:
            #
            # [
            #   {
            #     "id": 1,
            #     "full_name": "Admina Straytor",
            #     "games": [
            #       {
            #         "id": 1,
            #         "title": "Foo",
            #         "maker": "Bar Games",
            #         "skill_level": 3,
            #         "number_of_players": 4,
            #         "game_type_id": 2
            #       },
            #       {
            #         "id": 2,
            #         "title": "Foo 2",
            #         "maker": "Bar Games 2",
            #         "skill_level": 3,
            #         "number_of_players": 4,
            #         "game_type_id": 2
            #       }
            #     ]
            #   },
            # ]

        
            favorite_store = []

            for row in dataset:
                # TODO: Create a dictionary called game that includes 
                # the name, description, number_of_players, maker,
                # game_type_id, and skill_level from the row dictionary
                store = { 'id': row['id'],
                        'name': row['name']
                        
                }
                
            
                
                user_dict = next(
                    (
                        user for user in favorite_store
                        if user['customer_id'] == row['customer_id']
                    ),
                    None
                )
                
                if user_dict:
                    # If the user_dict is already in the games_by_user list, append the game to the games list
                    user_dict['store'].append(store)
                else:
                    # If the user is not on the favorite, create and add the user to the list
                   favorite_store.append({
                        "customer_id": row['customer_id'],
                        "first_name": row['first_name'],
                        "last_name": row['last_name'],
                        "name": row['name'],
                        "store": [store]
                    })
        
        # The template string must match the file name of the html template
        template = 'favorite_stores.html'
        
        # The context will be a dictionary that the template can access to show data
        context = {
            "favoritestore_list": favorite_store
        }

        return render(request, template, context)