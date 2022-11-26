from bs4 import BeautifulSoup
import requests
import pandas as pd
import csv 
    
# csv field names 
fields = ['movie_name', 'release_year', 'imdb', 'meta','votes']
    
# Writing to csv file 
with open('movies.csv', 'w') as csvfile:
	writer = csv.DictWriter(csvfile, fieldnames = fields)
	writer.writeheader()

year_list=[2010,2011,2012,2013,2014,2015,2016,2017,2018,2019,2020]

for year in year_list:

	page_number=1

	while page_number < 5050:
		html_text=requests.get('https://www.imdb.com/search/title/?title_type=feature&year='+str(year)+'-01-01,'+str(year)+'-12-31&start='+str(page_number)+'&ref_=adv_nxt').text
		
		imdb=BeautifulSoup(html_text,'lxml')
		
		movie=imdb.find_all('div',class_='lister-item')

		film_name=[]
		release_year=[]
		imdb_score=[]
		meta_score=[]
		votes_value=[]

		for mov in movie:
			h3_tag=mov.find('h3',class_='lister-item-header')

			meta_rating=mov.find('span',class_="metascore")
			nv = mov.find_all('span', attrs = {'name':'nv'})
			film=mov.find('h3',class_='lister-item-header').a.text
			year_tag=h3_tag.find('span',class_='lister-item-year').text	

			votes = nv[0].text if nv else 0

			try:
				imdb_rating=mov.find('div',class_="ratings-imdb-rating").attrs['data-value']
			except:
				imdb_rating=0	

			try:
				final_meta=meta_rating.text
			except:
				final_meta=0		
			
			film_name.append(film)
			release_year.append(year)
			imdb_score.append(imdb_rating)
			meta_score.append(final_meta)
			votes_value.append(votes)

		movie_dictionary={'movie_name':film_name,'release_year':release_year,'imdb':imdb_score,'meta':meta_score,'votes':votes_value}
		df=pd.DataFrame(movie_dictionary)
		csv_save=df.to_csv('movies.csv',mode='a',index=False,header=False)
		page_number += 50