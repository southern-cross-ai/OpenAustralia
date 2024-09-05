# OpenAustralia

## Overview

**Keywords**: Australian democracy; Parliamentary debates; Government transparency

[OpenAustralia](https://www.openaustralia.org.au) is an **independent**, **non-partisan** website dedicated to making Australian democracy more **accessible** and **transparent**. The platform allows citizens to easily access, explore, and understand the proceedings of the **Australian Parliament**. By providing searchable records of parliamentary debates (Hansard), users can follow what their representatives are saying and doing in Parliament.

## Data Source

The original data can be found at [OpenAustralia.org](https://www.openaustralia.org.au). For more details regarding their policy, Hansard or usage limitations, please seek information from [Help - OpenAustralia](https://www.openaustralia.org.au/help/).

## Data Structure

Under the directory `OpenAustralia`,

- **`recent_comments`** contains **1,117** [comments](https://www.openaustralia.org.au/comments/recent/) recorded from **2007 to 2020**. 

  The comments are from both house debates and senate debates. We recorded comments with their main post at the same time.

  For example,  `debate_2014-02-26.92.10.html` is from a **house debate** posted on `2014-02-26, and `senate_2020-09-02.187.1.html` is from a **senate debate** posted on 2020-09-02.

- **`senate_debates`** contains **78,915** [senate debates](https://www.openaustralia.org.au/senate/#help) recorded from **2006 to 2024**.

  Each file has the same naming convention `[date].[id].html`. For example, `2011-10-12.47.1.html` is from a **senate debate** posted on `2011-10-12`, and its ID `47.1` is used to identify its URL.

- **`house_debates`** contains **116,480** [house debates](https://www.openaustralia.org.au/debates/#help) recorded from **2006 to 2024**.

  Each file has the same naming convention `[date].[id].html`. For example, `2012-03-21.143.1.html` is from a **house debate** posted on `2012-03-21`, and its ID `143.1` is used to identify its URL.

Notice that the **first line** of each `.html` file indicates its original URL, e.g., in `senate_debates/2006-02-07.3.1.html`, the first line `<!--https://www.openaustralia.org.au/senate/?id=2006-02-07.3.1-->` indicates it is crawled from `https://www.openaustralia.org.au/senate/?id=2006-02-07.3.1`.

(Last time updated on 22 August 2024)

## Download

To crawl resources from OpenAustralia, we developed Python scripts under `utils` for you to explore and understand how we build URLs and retrieve data.

In `utils/utils.py`, we defined a class `OpenAustralia` which includes the details of how we first collect date entries from a time range, how we build URLs for each date entry, and how we crawl the posts under each data entry.

An example to crawl house debates data from `2021-01-23` to `2023-03-21` and save it to `test` is as follows:g
```python
from utils import OpenAustralia

if __name__ == '__main__':
    oa = OpenAustralia(start_date='2021-01-23',
                       end_date='2023-03-21',
                       data_type='house',
                       save_path='test')
    oa.retrieve_data()
```

## License

This repo is licensed under [MIT](https://opensource.org/license/mit).

