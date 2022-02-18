

You've started a new movie-rating website, and you've been collecting data on reviewers' ratings of various movies. 
There's not much data yet, but you can still try out some interesting queries. Here's the schema: 

**Movie** ( mID, title, year, director ) 
English: There is a movie with ID number mID, a title, a release year, and a director. 

**Reviewer** ( rID, name ) 
English: The reviewer with ID number rID has a certain name. 

**Rating** ( rID, mID, stars, ratingDate ) 
English: The reviewer rID gave the movie mID a number of stars rating (1-5) on a certain ratingDate. 



#### Relational Queries

Write **Relational Algebraic Expression** AND **Calculus Formulae** AND **SQL Statement**, for the following queries.

1. Find the titles of all movies directed by *Steven Spielberg*. 
2. Find the names of all reviewers who rated *Gone with the Wind*.
3. Find all years that have a movie that received a rating of 4 or 5. 
4. Find the titles of all movies that have no ratings.
5. Find the titles of all movies not reviewed by *Chris Jackson*. 
6. Find the name of reviewers that rated every movie directed by *Steven Spielberg*.


#### [Optional] SQL Beyond Relational Queries

Write **SQL Statement** only for each of the following queries.

7. For each movie, return the title and the 'rating spread', that is, the difference between highest and lowest ratings given to that movie. Sort by rating spread from highest to lowest, then by movie title. 
8. For each director, return the director's name together with the title(s) of the movie(s) they directed that received the highest rating among all of their movies, and the value of that rating. Ignore movies whose director is NULL. 
9. For all movies that have an average rating of 4 stars or higher, add 25 to the release year. (Update the existing tuples; don't insert new tuples.)

1/ 
SELECT title FROM movie where director = 'Steven Spielberg';



2/ 
SELECT name
FROM Rating
JOIN Movie ON Movie.mid = Rating.mid
JOIN Reviewer ON Rating.rid = Reviewer.rid
where title='Gone with the Wind'

3/
SELECT DISTINCT year
FROM Rating
JOIN Movie ON Movie.mid = Rating.mid
JOIN Reviewer ON Rating.rid = Reviewer.rid
where stars > 3

4/
SELECT title from Movie where Movie.mid NOT in (
SELECT DISTINCT Movie.mid
FROM Movie
JOIN Rating ON Movie.mid = Rating.mid
)

5/
SELECT title from Movie where Movie.mid NOT in (
SELECT Movie.mid
FROM Rating
JOIN Movie ON Movie.mid = Rating.mid
JOIN Reviewer ON Rating.rid = Reviewer.rid
where name='Chris Jackson'
)

6/

select name from (
Select * from (
SELECT name, title, Movie.mid
FROM Rating
JOIN Movie ON Movie.mid = Rating.mid
JOIN Reviewer ON Rating.rid = Reviewer.rid
where director = 'Steven Spielberg'
  ) GROUP by name, title, mid
  ) Group by name having count(mid) >= (select count(*) from Movie where director = 'Steven Spielberg')