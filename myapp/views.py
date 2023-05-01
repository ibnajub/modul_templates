import string
from random import random

from django.shortcuts import render


def index(request):
    # my_num = 33
    # my_str = 'some string'
    # my_dict = {"some_key": "some_value"}
    # my_set = {'set_first_item', 'set_second_item', 'set_third_item'}
    # my_tuple = ('tuple_first_item', 'tuple_second_item', 'tuple_third_item')
    # my_class = MyClass('class string')
    # rand_list_article = [1, 2, 3, 4, 5]
    # # rand_list_article = 2
    # letters = string.ascii_letters
    # rand_article_slag = ''.join(random.choice(letters) for i in range(5)) + '-' \
    #                     + ''.join(random.choice(letters) for i in range(5))
    return render(request, 'index_demar v2.htm', {
        # 'rand_list_article': rand_list_article,
        # 'rand_list_article': rand_list_article,
        # 'rand_article_slag': rand_article_slag,
        
    })
