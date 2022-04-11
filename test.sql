SELECT *
FROM movies
ORDER BY Year DESC
LIMIT 4;
SELECT *
FROM movies
ORDER BY Title ASC
LIMIT 5;
SELECT City,
  Country
FROM north_american_cities
WHERE Country = "Canada";
SELECT City
FROM north_american_cities
WHERE Country = "United States"
ORDER BY Latitude ASC;
SELECT City
FROM north_american_cities
WHERE Longitude < -87.629798
ORDER BY Longitude DESC;
SELECT City
FROM north_american_cities
WHERE Country = "Mexico"
ORDER BY Population DESC
LIMIT 2;
SELECT City,
  Population
FROM north_american_cities
WHERE Country = "United States"
ORDER BY Population DESC
LIMIT 2 OFFSET 2;
SELECT Domestic_sales,
  International_sales
FROM Movies
  INNER JOIN Boxoffice ON Movies.id = Boxoffice.Movie_id;
SELECT Title,
  Domestic_sales,
  International_sales
FROM Movies
  INNER JOIN Boxoffice ON Movies.id = Boxoffice.Movie_id;
SELECT Title,
  Domestic_sales,
  International_sales
FROM Movies
  INNER JOIN Boxoffice ON Movies.id = Boxoffice.Movie_id
WHERE International_sales > Domestic_sales;
SELECT Title
FROM Movies
  INNER JOIN Boxoffice ON Movies.id = Boxoffice.Movie_id
ORDER BY Rating DESC;
SELECT DISTINCT building
FROM employees;
SELECT *
FROM Buildings;
SELECT DISTINCT Role,
  Building
FROM Employees;
SELECT Name,
  Role
FROM Employees
WHERE Building IS NULL;
SELECT DISTINCT Building_name
FROM Buildings
  LEFT JOIN Employees ON Buildings.Building_name = Employees.Building
WHERE Role IS NULL;
SELECT title,
  (domestic_sales + international_sales) / 1000000 AS gross_sales_millions
FROM movies
  INNER JOIN boxoffice ON movies.id = boxoffice.movie_id;
SELECT Title,
  (Rating * 10) AS Rating_percent
FROM Movies
  INNER JOIN Boxoffice ON Movies.Id = Boxoffice.Movie_id;
SELECT MAX(years_employed) as Max_years_employed
FROM employees;
SELECT Role,
  AVG(Years_employed) AS Avg_years_employed
FROM Employees
GROUP BY Role;
SELECT SUM(Years_employed) AS Total_years_employed,
  Building
FROM Employees
GROUP BY Building;
SELECT role,
  COUNT(*) as Number_of_artists
FROM employees
WHERE role = "Artist";
SELECT Role,
  COUNT(*) as Role_count
From Employees
GROUP BY Role;
SELECT SUM(Years_employed) AS Total_years
FROM Employees
WHERE Role = "Engineer";
SELECT DISTINCT column,
  AGG_FUNC(column_or_expression),
  …
FROM mytable
  JOIN another_table ON mytable.column = another_table.column
WHERE constraint_expression
GROUP BY column
HAVING constraint_expression
ORDER BY column ASC / DESC
LIMIT count OFFSET COUNT;
SELECT Director,
  COUNT(Director)
FROM Movies
GROUP BY Director;
SELECT Director,
  (SUM(Domestic_sales) + SUM(International_sales)) AS Total_sales
FROM Movies
  INNER JOIN Boxoffice ON Movies.id = Boxoffice.movie_id
GROUP BY Director;


INSERT INTO Movies
VALUES (4, "Toy Story 4", "John Lasseter", 1995, 81);

INSERT INTO Boxoffice
VALUES (4, 8.7, 340000000, 270000000);

UPDATE Movies
SET Director = "John Lasseter"
WHERE Title = "A Bug's Life";

UPDATE Movies
SET Year = 1999
WHERE Title = "Toy Story 2";

UPDATE Movies
SET Title = "Toy Story 3", 
    Director = "Lee Unkrich"
WHERE Title = "Toy Story 8";

CREATE TABLE Database (
  id INTEGER PRIMARY KEY,
  Name TEXT,
  Version INTEGER
)

ALTER TABLE Movies
ADD Aspect_ratio FLOAT;