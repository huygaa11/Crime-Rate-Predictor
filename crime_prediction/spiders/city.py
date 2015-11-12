import scrapy

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
        # for ind in range (0, len(self.all_states_links)):
        for ind in range (0, len(self.all_states_links) - 1):
            yield scrapy.Request(self.all_states_links[ind], callback=self.get_city_links)

        


    def get_city_links(self, response):

        cities_links = response.xpath('//*[@class="rB"]//a/@href').extract()

        for ind in range (0, len(cities_links)):
            cities_links[ind] = 'http://www.city-data.com/city/' + cities_links[ind]

        self.all_cities_links = self.all_cities_links + cities_links

        self.finished_states += 1;

        if self.finished_states == len(self.all_states_links) - 1:
            # print self.all_cities_links
            print self.all_states_links
            print len(self.all_cities_links)

        
        





















        


