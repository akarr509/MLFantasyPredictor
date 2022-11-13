A script that uses BeautifulSoup and requests to scrape www.pro-football-reference.com to predict 2022-2023 fantasy production of NFL players

Goes through the top 400 players ranked by scrimmage yeards this season - checks to see if the player is not a rookie, and then proceeds to aggregate data
regarding all of their career season stats, as well as career averages leading up to each year - outputs this to a csv file to later be used as training data

Creates a testing data csv file with 2021 season performance as well as career averages up until that season - uses scikit learn to create a multivariate 
linear regression model to predict the performances of these players in the 2022-2023 season.
