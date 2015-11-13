import scrapy
import re

from crime_prediction.items import City

TEST_MODE = 1
NUMBER_TEST_STATES = 3
NUMBER_TEST_CITIES = 2


class CitySpider(scrapy.Spider):
    name = "city"
    # allowed_domains = ["dmoz.org"]
    start_urls = [
        "http://www.city-data.com/",
    ]

    all_states_links = []
    all_states_initials = []
    all_cities_links = []

    finished_states = 0

    def parse(self, response):
        
        ### Extract links to states
        columns = response.xpath('//*[@id="home1"]/ul')

        # first 4 columns have useful links
        for column_index in range (0, 4):
            column = columns[column_index]
            
            # extract state initials
            state_initials = column.xpath('li/a').xpath('text()').extract();
            self.all_states_initials = self.all_states_initials + state_initials

            # extract links to data for each states
            state_links = column.xpath('li/a/@href').extract();
            self.all_states_links = self.all_states_links + state_links

        ### extracted links to states


        ### Extract links to cities
        ### big cities (excluded small cities)
        if (TEST_MODE == 1):
            for ind in range (0, NUMBER_TEST_STATES):
                yield scrapy.Request(self.all_states_links[ind], callback=self.get_city_links)
        else:
            for ind in range (0, len(self.all_states_links) - 1):
                yield scrapy.Request(self.all_states_links[ind], callback=self.get_city_links)

        ### small cities
        ### yield scrapy.Request(self.all_states_links[len(self.all_states_links) - 1], callback=self.get_city_links)


    def get_city_links(self, response):

        cities_links = response.xpath('//*[@class="rB"]//a/@href').extract()

        # for ind in range (0, len(cities_links)):
        for ind in range (0, len(cities_links)):
            cities_links[ind] = 'http://www.city-data.com/city/' + cities_links[ind]

        if (TEST_MODE == 1):
            for ind in range (0, NUMBER_TEST_CITIES):
                yield scrapy.Request(cities_links[ind], callback=self.parse_data_from_city)
        else:
            for ind in range (0, len(cities_links)):
                yield scrapy.Request(cities_links[ind], callback=self.parse_data_from_city)

        # self.all_cities_links = self.all_cities_links + cities_links

        """
        self.finished_states += 1;

        if (TEST_MODE == 1):
            # if self.finished_states == len(self.all_states_links) - 1:
            if self.finished_states == 1:
                for ind in range (0, TEST_CITIES):
                    yield scrapy.Request(self.all_cities_links[ind], callback=self.parse_data_from_city)
        else:
            # if self.finished_states == len(self.all_states_links) - 1:
            if self.finished_states == len(self.all_states_links) - 1:
                for ind in range (0, len(self.all_cities_links)):
                    yield scrapy.Request(self.all_cities_links[ind], callback=self.parse_data_from_city)
        """

    def parse_data_from_city(self, response):
        name = response.xpath('//*[@class="city"]/span/text()').extract()

        # state and city name
        item = City()
        item['name'] = name[0].split(",")[0]
        item['state'] = name[0].split(",")[1][1:]

        race_names = response.xpath('//*[@id="races-graph"]/ul/li[2]/ul/li/b/text()').extract()
        race_percentages = response.xpath('//*[@id="races-graph"]/ul/li[2]/ul/li/span[2]/text()').extract()


        item['white_alone'] = 0
        item['hispanic'] = 0
        item['asian_alone'] = 0
        item['american_indian_alone'] = 0
        item['black_alone'] = 0

        for ind in range (0, len(race_names)):
            if race_names[ind] == 'White alone':
               item['white_alone'] = race_percentages[ind][:-1]
            elif race_names[ind] == 'Hispanic':
               item['hispanic'] = race_percentages[ind][:-1]  
            elif race_names[ind] == 'Asian alone':
               item['asian_alone'] = race_percentages[ind][:-1]   
            elif race_names[ind] == 'American Indian alone':
               item['american_indian_alone'] = race_percentages[ind][:-1] 
            elif race_names[ind] == 'Black alone':
               item['black_alone'] = race_percentages[ind][:-1] 

        # gender percentage
        genders = response.xpath('//*[@id="population-by-sex"]/div/table/tr')
        item['percentage_male'] = genders[0].xpath('td[2]/text()').extract()[0].encode('utf-8')[3:][:-2]
        item['percentage_female'] = genders[1].xpath('td[2]/text()').extract()[0].encode('utf-8')[3:][:-2]
        
        # population

        male_population = genders[0].xpath('td[1]/text()').extract()[0].encode('utf-8')[1:][:-2]
        female_population = genders[1].xpath('td[1]/text()').extract()[0].encode('utf-8')[1:][:-2]

        item['population'] = 0 + int (male_population.replace(",", "")) + int(female_population.replace(",", ""))

        # median age

        item['median_age'] = response.xpath('//*[@id="median-age"]/div/table/tr[1]/td[2]/text()')[0].extract().encode('utf-8')[2:][:-6]
        
        # median household income 
        item['median_household_income'] = response.xpath('//*[@id="median-income"]/div[1]/table/tr[1]/td[2]/text()')[0].extract().encode('utf-8')[1:].replace(",", "")

        # median per capita income
        # item['median_per_capita_income'] = response.xpath('//*[@id="median-income"]/text()')[5].extract()

        # estimated median house value

        item['median_house_value'] = response.xpath('//*[@id="median-income"]/div[2]/table/tr[1]/td[2]/text()')[0].extract()[1:].replace(",", "")

        # cost of living index
        item['cost_of_living_index'] = response.xpath('//*[@id="cost-of-living-index"]/text()')[0].extract()[1:][:-1].replace(",", "")

        # unemployment_rate
        item['unemployment_rate'] = response.xpath('//*[@id="unemployment"]/div/table/tr[1]/td[2]/text()')[0].extract()[:-1]

        # High school or higher
        item['high_school_degree_or_higher'] = response.xpath('//*[@id="education-info"]/ul/li[1]/text()')[0].extract()[1:][:-1]

        # Bachelor's degree or higher
        item['bachelors_degree_or_higher'] = response.xpath('//*[@id="education-info"]/ul/li[2]/text()')[0].extract()[1:][:-1]

        # Graduate or professional degree
        item['graduate_or_professional_degree'] = response.xpath('//*[@id="education-info"]/ul/li[3]/text()')[0].extract()[1:][:-1]

        yield item

        

        





















        


