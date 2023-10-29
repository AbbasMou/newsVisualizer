## Intro
this is a data visiulization project for data scraped from news sitemaps as al jazeera and al mayadeen 
### Whats in there ?
flask rest api that fetches data from mongo db 
A dashboard page that contains 3 differnet charts using Highcharts.js libarary 

### Code Functionality
1. sitemap.py : this file responsible for visiting sitemap and sub sitemaps , these sitemaps should be ready for extracting data from each one 
2. crawler.py : this file is responsible for extarcting data from al maydeen and al jazeera sitemaps , then saving these data on mongo db 
3. app.py : this file contains python flast rest api endpoints for extracting useful information from data saved in mongodb.
4. dasboard.html : this file contains html and js ; the js code is from  highcharts.js charts library , these charts used data fetched from the flask api and make 3 differnet charts 

## ScreenShots 
![screenshot 1 ](/images/sc1.png)

![screenshot 2 ](/images/sc2.png)

