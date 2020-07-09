R Notebook
================

COVID-19 Analysis

This is not an official analysis, this is for internal checking of the
data only.

``` r
# load libraries
knitr::opts_chunk$set(warning=FALSE, message=FALSE)
library(dplyr)
```

    ## Warning: package 'dplyr' was built under R version 3.6.3

    ## 
    ## Attaching package: 'dplyr'

    ## The following objects are masked from 'package:stats':
    ## 
    ##     filter, lag

    ## The following objects are masked from 'package:base':
    ## 
    ##     intersect, setdiff, setequal, union

``` r
library(DT)
```

    ## Warning: package 'DT' was built under R version 3.6.3

``` r
# read data, factor date
raw <- read.csv('tweets_US_states_counties.csv') %>% 
  mutate(
    date = as.Date(date, format= "%Y-%m-%d")
  )

raw %>% 
  head()
```

    ##     X user_id_str
    ## 1  12  1541832572
    ## 2 235   163674014
    ## 3 372   160564879
    ## 4 523   803459388
    ## 5 928    42273750
    ## 6 949    18220818
    ##                                                                                                                                                                                                                                                                                text
    ## 1                                                                                                                                                                                                    Having a mocha and avoiding coronavirus at the airport https://t.co/2ohvE3Pxb8
    ## 2                                                                                                                                                Sadly nothing will be done to help the people of China, because their communist government is untouchable. https://t.co/IVx7ztDzMG
    ## 3 The world is grieving for the Wuhan doctor who tried to warn colleagues about #coronavirus but only Democrats and a handful of Republicans  condemn @realDonaldTrump for firing the witnesses who told the truth about him. Foolish to expect anyone to stick their neck out now.
    ## 4                                                                                                                                                                            thereâ\200\231s a lot of asians with facemasks on, if i get this coronavirus, iâ\200\231m fucking lil ling ling up
    ## 5                                                                                                                                #COVIDãƒ¼19\n\nCovid - 19 Paranoia reaching extreme levels! \nI sneezed in front of my laptop and the antivirus immediately started scanning !ðŸ¤£
    ## 6                                                                                                                                                                                                                        I hope you are okay @GOPChairwoman https://t.co/li0zPGt7H1
    ##         date     time                        geometry proj_state proj_county
    ## 1 2020-02-10 07:03:44 POINT (-115.1351649 36.0609645)     Nevada       Clark
    ## 2 2020-02-10 07:44:00 POINT (-115.1351649 36.0609645)     Nevada       Clark
    ## 3 2020-02-09 02:08:51 POINT (-115.03833685 36.006256)     Nevada       Clark
    ## 4 2020-01-27 01:04:41 POINT (-115.1351649 36.0609645)     Nevada       Clark
    ## 5 2020-03-14 22:18:10 POINT (-115.03833685 36.006256)     Nevada       Clark
    ## 6 2020-03-14 22:19:05 POINT (-115.0611275 36.1847539)     Nevada       Clark

``` r
raw %>% 
  nrow()
```

    ## [1] 148831

The total sum of tweets

``` r
raw %>% 
  subset(select= date) %>% 
  group_by(date) %>% 
  summarise(
    count = n()
  ) %>% 
  mutate(
    total_sum = cumsum(count)
  ) %>% 
  arrange(date)
```

    ## # A tibble: 59 x 3
    ##    date       count total_sum
    ##    <date>     <int>     <int>
    ##  1 2020-01-22    80        80
    ##  2 2020-01-23   308       388
    ##  3 2020-01-24  1109      1497
    ##  4 2020-01-25  1266      2763
    ##  5 2020-01-26  1540      4303
    ##  6 2020-01-27  1309      5612
    ##  7 2020-01-28  1696      7308
    ##  8 2020-01-29  3669     10977
    ##  9 2020-01-30  3913     14890
    ## 10 2020-01-31  3339     18229
    ## # ... with 49 more rows

``` r
raw %>% 
  group_by(proj_state) %>% 
  summarise(
    count = n()
  ) %>% 
  arrange(-count)
```

    ## # A tibble: 52 x 2
    ##    proj_state   count
    ##    <fct>        <int>
    ##  1 California   25839
    ##  2 Texas        15195
    ##  3 New York     13020
    ##  4 Florida       8596
    ##  5 Pennsylvania  5080
    ##  6 Georgia       5077
    ##  7 Washington    4847
    ##  8 Illinois      4768
    ##  9 Virginia      4231
    ## 10 Ohio          4039
    ## # ... with 42 more rows
