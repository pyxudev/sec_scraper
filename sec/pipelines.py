import re
import csv
from time import sleep
from itemadapter import ItemAdapter
from difflib import SequenceMatcher
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome import service as fs
from selenium.webdriver.chrome.options import Options

class SecPipeline:
	def open_spider(self, spider):
		print('start program')
		cik_target = []
		comp_names = []

		name_list = open('C:/Users/Xu/Desktop/output/check_list.csv', 'r', encoding='utf-8')
		name_reader = csv.reader(name_list)
		cik_list = open('C:/Users/Xu/Desktop/output/cik_list.csv', 'a', newline='', encoding='utf-8')
		out_writer = csv.writer(cik_list)

		for name_line in name_reader:
			if name_line[0] != None:
				print(name_line[0])
				cik_list = open('C:/Users/Xu/Desktop/sec_scraper/sec/sec/spiders/cik-lookup-data.csv', 'r', encoding='utf-8', errors='ignore')
				cik_reader = csv.reader(cik_list, delimiter=',')
				compare = []
				for cik_line in cik_reader:
					if cik_line[0] != None:
						str_a = name_line[1].casefold()
						if f'"' in str_a:
							str_a = re.sub(f'"', '', str_a)
						str_b = cik_line[0].casefold()
						if f'"' in str_b:
							str_b = re.sub(f'"', '', str_b)
						rate = SequenceMatcher(None, str_a, str_b).ratio()
						if rate > 0.7:
							compare.append([name_line[1], str(cik_line[1]), rate])
				bench = 0
				out_list = []
				for i in range(0, len(compare)):
					if compare[i][2] > bench:
						bench = compare[i][2]
						out = compare[i]
				
				cik_list.close()
				cik_target.append(out[1])
				out_writer.writerow([out[0], out[1]])
		cik_list.close()
		name_list.close()

		print('cik analyze is done')

	def close_spider(self, spider):
		options = Options()
		# options.add_argument('--headless')
		chrome_service = fs.Service(executable_path='C:/chromedriver.exe')
		driver = webdriver.Chrome(service=chrome_service, options=options)
		scrape_list = open('C:/Users/Xu/Desktop/output/site_to_scrape.csv', 'r', encoding='utf-8')
		list_reader = csv.reader(scrape_list, delimiter=',')

		target_list = []
		for data in list_reader:
			target_list.append(data)
		scrape_list.close()
		b_keywords = ['Human Capital', 'Employee', 'Employees', 'Talent', 'Talents', 'People', 'Workforce', 'Workforces']
		keywords = {
			'Equality' : ['Equality', 'Impartiality', 'Discrimination'],
			'Harrassment' : ['Harassment', 'Harassments'],
			'Diversity' : ['Diversity'],
			'Inclusion' : ['Inclusion'],
			'Gender' : ['Gender', 'Women', 'Woman', 'Female', 'LGBT', 'sex', 'sexual'],
			'Disability' : ['Disability', 'Disable'],
			'Race' : ['Race', 'Racial', 'Color', 'Colour'],
			'Nationality' : ['Nationality', 'National Origin', 'Place of Birth', 'Birthplace'],
			'Age' : ['Age', 'Ageism'],
			'Turnover Rate' : ['Turnover Rate', 'Retention Rate', 'Turnover'],
			'Training Hours': ['Training Hours', 'Hour of Training', 'Training Time', 'Training Hour', 'Training Times', 'Hours of Training', 'Development Hours', 'Hour of Development', 'Development Time', 'Development Hour', 'Development Times', 'Hours of Development'],
			'Training Cost' : ['Training Costs', 'Cost of Training', 'Training Cost', 'Training Cost', 'Costs of Training', 'Training Expenses', 'Training Expense', 'Expense of Training', 'Expenses of Training', 'Development Costs', 'Cost of Development', 'Development Cost', 'Development Cost', 'Costs of Development', 'Development Expenses', 'Development Expense', 'Expense of Development', 'Expenses of Development'],
			'Training' : ['Training', 'Class', 'Seminar', 'Skill', 'Program', 'Reskill', 'Education', 'Growth', 'Trainings', 'Developments', 'Classes', 'Seminars', 'Skills', 'Programs', 'Reskilling', 'Educate'],
			'Engagement' : ['Engagement', 'Commitment', 'Loyalty', 'Motivation', 'Retention'],
			'Engagement Survey' : ['Engagement Survey', 'Commitment Survey', 'Loyalty Survey'],
			'Wellbeing' : ['Wellbeing', 'Well-being', 'Happiness'],
			'Culture' : ['Culture', 'Cultures', 'Plactice', 'Plactices'],
			'Productivity' : ['Productivity', 'Effectiveness'],
			'Human Capital ROI' : ['Human Capital ROI', 'HCROI'],
			'Critical Position' : ['Critical Position', 'Critical Positions', 'Critical Post', 'Critical Posts', 'Key Position', 'Key Positions', 'Key Post', 'Key Posts'],
			'Succession Plan' : ['Succession Plan', 'Succession Planining', 'Plan of Succession', 'Plans of Succession', 'Succession Program', 'Succession Programs', 'Plan of Successors', 'Plans of Successors', 'Succession Strategy'],
			'Wage' : ['Wage', 'Wages', 'Salary', 'Salaries', 'Compensation', 'Compensations'],
			'Benefit' : ['Benefit', 'Benefits'],
			'Health' : ['Health', 'Fitness'],
			'Safety' : ['Safety']
		}
		result_csv = open('C:/Users/Xu/Desktop/output/result.csv', 'a', newline='', encoding='utf-8')
		result_writer = csv.writer(result_csv)
		result_writer.writerow(['企業名', '記載項目'] + list(keywords.keys()))

		for data in target_list:
			name = data[0]
			url = data[1]
			new_line = [name.replace(f'"', '')]

			driver.get(url)
			sleep(5)
			i = 0
			for key in b_keywords:
				check = driver.find_elements(by=By.XPATH, value=f"//*[contains(text(), '{key}')]")
				b_check = driver.find_elements(by=By.XPATH, value=f"//*[contains(text(), '{key.upper()}')]")
				if check or b_check:
					new_line.append('1')
					i = 1
					break
			if i == 0:
				new_line.append('')

			for key, values in keywords.items():
				j = 0
				for value in values:
					check = driver.find_elements(by=By.XPATH, value=f"//*[contains(text(), '{value}')]")
					b_check = driver.find_elements(by=By.XPATH, value=f"//*[contains(text(), '{value.lower()}')]")
					if check or b_check:
						new_line.append('1')
						j = 1
						break
				if j == 0:
					new_line.append('')
			
			result_writer.writerow(new_line)

			print(new_line)
			print(name + " done")
		
		result_csv.close()
		driver.quit()
		print('all done')
