# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class City(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    state = scrapy.Field()
    name = scrapy.Field()
    percentage_male = scrapy.Field()
    percentage_female = scrapy.Field()
    population = scrapy.Field()
    median_age = scrapy.Field()
    median_household_income = scrapy.Field()
    median_house_value = scrapy.Field()
    cost_of_living_index = scrapy.Field()
    unemployment_rate = scrapy.Field()
    high_school_degree_or_higher = scrapy.Field()
    bachelors_degree_or_higher = scrapy.Field()
    graduate_or_professional_degree = scrapy.Field()

    #median_per_capita_income = scrapy.Field()

    # races
    white_alone = scrapy.Field()
    hispanic = scrapy.Field()
    asian_alone = scrapy.Field()
    american_indian_alone = scrapy.Field()
    black_alone = scrapy.Field()

    pass
