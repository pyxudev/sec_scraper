import re
import csv
import json
import scrapy
from difflib import SequenceMatcher

class SecSpider(scrapy.Spider):
	name = 'sec'

	def start_requests(self):
		comp_names = []
		cik_target = []
		cik_list = open('C:/Users/Xu/Desktop/output/cik_list.csv', 'r', encoding='utf-8')
		cik_reader = csv.reader(cik_list, delimiter=',')

		for cik_line in cik_reader:
			if cik_line:
				comp_names.append(cik_line[0])
				cik_target.append(str(cik_line[1]))
		cik_list.close()

		for i in range(0, len(cik_target)):
			cik = cik_target[i]
			url = 'https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=' + str(cik) + '&owner=include&count=100'
			meta = {
				'comp_name': comp_names[i]
			}
			headers = {
				'Referer': 'https://www.sec.gov/'
			}
			yield scrapy.Request(url=url, meta=meta, headers=headers, callback=self.search_result)

	def search_result(self, response):
		name = response.meta['comp_name']
		meta = {
			'comp_name': name
		}
		headers = {
			'Referer': 'https://www.sec.gov/'
		}
		table = response.css('#seriesDiv > table.tableFile2 > tr').getall()
		for tr in table:
			if '10-K' in tr:
				link = tr.split('<a href="')[1].split('" id="documentsbutton">')[0]
				url =  'https://www.sec.gov' + link

				yield scrapy.Request(url=url, meta=meta, headers=headers, callback=self.filing_detail)
				break
	
	def filing_detail(self, response):
		name = response.meta['comp_name']
		table = response.css('#contentDiv > div:nth-child(3) > div:nth-child(1) > table:nth-child(2) > tr').getall()
		for tr in table:
			if '10-K' in tr:
				link = tr.split('<a href="/ix?doc=')[1].split('">')[0]
				url = 'https://www.sec.gov' + link
				res = open('C:/Users/Xu/Desktop/output/site_to_scrape.csv', 'a', newline='', encoding='utf-8')
				res_writer = csv.writer(res)
				res_writer.writerow([name, url])
				res.close()
				# print(url)
				break