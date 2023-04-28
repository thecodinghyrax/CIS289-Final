
# Python II CIS 289 – Final Project Proposal 
##### DREW CRAWFORD – SPRING 2023

## Program Scope
For my project, I will be creating a Django website that will be used to gather and track computer component prices from NewEgg. The site will allow the user to enter specific parts needed for a computer build (via a part link) and then scrape NewEgg to find current prices. The prices will be stored in a database and then retrieved to create visuals that will show the price changes over time. 
## Existing Problem
The price of PC components fluctuates often and finding the best prices can be tricky. I am currently planning my next computer build and will need to maximize my budget with good data.  It can be impossible to know what prices are fair without knowing what the highest, lowest and average prices are. This project seeks to overcome the pricing manipulation seen by major retailers by collecting, organizing and visualizing data. 
## Project Components
- Database integration
- Scraping
- Pandas
- Visualizations 
- Django
- Threading
- Factory Patterns
## Project Expectations
- Basic Django website to collect user defined, PC part data and display the scraped prices.
- A database to store parts lists, catagories and historic prices.
- Scraping component data from NewEff to retrieve current prices.
- Pandas data frames created from the database information and plotted to charts.
## Potential Functionality
- Users will be able to create/view parts lists.
- Users will be able to trigger a scrape of NewEgg's website for their products.
- Users will be able to view price details in graphs showing historic price changes.
- Users will be able to edit their parts lists to change their build configuration.
## Potential Issues
Scraping some websites for specific products may be problematic. Care will need to be taken to ensure the right prices are returned for the right products. 
## Project Requirement Criteria Files
- DB read/write: repository.py
- Scraping: newegg_scrape.py
- Pandas: repository.py
- Visualization: charts.py
- DB Integration: repository.py
- Django: CIS289_Final/
- Multi-threading: charts.py, views.py
- Factories: models.py
