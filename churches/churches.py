# -*- coding: utf-8 -*-
import scrapy

from states import states

class ChurchesSpider(scrapy.Spider):
  name = 'churches'
  allowed_domains = ['www.churchfinder.com']
  start_urls = [
    f'https://www.churchfinder.com/churches/{state.lower()}'
    for state in states.keys()
  ]

  def parse(self, response):
    links = response.css('.field-content > a::attr(href)').extract()
    for link in links:
      yield scrapy.Request(response.urljoin(link), self.parse_city)

  def parse_city(self, response):
    next_page = response.css('.pager-next > a::attr(href)').extract_first()
    if next_page:
      yield scrapy.Request(response.urljoin(next_page), self.parse_city)

    churches = response.css('#content .views-row')
    for church in churches:
      name = church.css('.views-field-title a::text').extract_first()
      if name:
        yield {
          'city_url': response.url,
          'url': church.css('.views-field-title a::attr(href)').extract_first(),
          'name': name,
          'address': church.css('.field-name-field-address .field-item::text').extract_first(),
          'denomination': church.css('.field-name-field-specific-denomination::text').extract_first(),
        }
