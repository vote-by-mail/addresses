# -*- coding: utf-8 -*-

'''
Generating list of churches for mail-my-ballot.
Generates a list of the scraped churches in the
target states and saves them out into a JSON file.

It was run in what is probably the wrong way (I'm a
scrapy noob) by making a new project and copying it into
the project's spider directory as described at
https://docs.scrapy.org/en/latest/intro/tutorial.html

'''

import scrapy

from states import states
import json

OUTPUT_FNAME = 'churches.json'

TARGET_STATES = [
  'fl', #  'Florida'
  'ga', #  'Georgia'
  'mn', #  'Minnesota'
  'ne', #  'Nebraska'
  'me', #  'Maine'
  'md', #  'Maryland'
  'va', #  'Virginia'
  'nv', #  'Nevada'
  'mi', #  'Michigan'
  'wi'  #  'Wisconsin'
]


class ChurchesSpider(scrapy.Spider):
  name = 'churches'
  allowed_domains = ['www.churchfinder.com']
  start_urls = [
    f'https://www.churchfinder.com/churches/{state.lower()}'
    for state in TARGET_STATES
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
        res = {
          'city_url': response.url,
          'url': church.css('.views-field-title a::attr(href)').extract_first(),
          'name': name,
          'address': church.css('.field-name-field-address .field-item::text').extract_first(),
          'denomination': church.css('.field-name-field-specific-denomination::text').extract_first(),
        }
      with open(OUTPUT_FNAME, 'a') as f:
        f.write(json.dumps(res)+'\n')
      yield res
