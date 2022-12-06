#### 09-29-2022
## Project 02B - Missile Command (Part 1)

<center>
<img src="https://miro.medium.com/max/1400/1*6oQAh2tGYABlNJBmqNsaLA.webp" width="300">
</center>

## Overview

The goal of this project is to create an implementation of missile path randomly generated while incorporating our spatial db concepts. This is in regards to preparing to make a game in which we have
military bases to defend and missile randomly flying to attack it. To prepare for this, we create random
missile paths that are formed by establishing a box around the mainland United States. We then generate
a set even number of points on the border of this box and then pair together the points to create a 
coordinate system. Once each point has received its pair, and its counter point does not lie in the same
border edge, we then interpolate the two points to obtain a "line" connecting the coordinates together. 
This line represents the path that the given missile will take starting at one of the points and "moving"
to the other. Each path is stored in a postgreSQL table by its missile and also contains a set altitude, 
speed, degree, and id.

## Data 

We use two datasets: 
1. [military installations](https://www2.census.gov/geo/tiger/TIGER2021/MIL/tl_2021_us_mil.zip)
2. The randomly generated set of missile paths across the continental US.
