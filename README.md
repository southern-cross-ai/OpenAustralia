# OpenAustralia

## Overview

**Keywords**: Australian democracy; Parliamentary debates; Government transparency

[OpenAustralia](https://www.openaustralia.org.au) is an **independent**, **non-partisan** website dedicated to making Australian democracy more **accessible** and **transparent**. The platform allows citizens to easily access, explore, and understand the proceedings of the **Australian Parliament**. By providing searchable records of parliamentary debates (Hansard), users can follow what their representatives are saying and doing in Parliament.

## Data Source

The original data can be found at [OpenAustralia.org](https://www.openaustralia.org.au). For more details regarding their policy, Hansard or usage limitations, please seek information from [Help - OpenAustralia](https://www.openaustralia.org.au/help/).

## Data Structure

Under the directory `OpenAustralia`,

- **`recent_comments`** contains **1,117** [comments](https://www.openaustralia.org.au/comments/recent/) recorded from **2007 to 2020** (last time updated on 2024-08-22). 

  The comments are from both house debates and senate debates. We recorded comments with their main post at the same time.

  For example,  `debate_2014-02-26.92.10.html` is from a **house debate** posted on `2014-02-26, and `senate_2020-09-02.187.1.html` is from a **senate debate** posted on 2020-09-02.

- **`senate_debates`** contains **78,915** [senate debates](https://www.openaustralia.org.au/senate/#help) recorded from **2006 to 2024** (last time updated on 2024-08-22).

  Each file has the same naming convention `[date].[id].html`. For example, `2011-10-12.47.1.html` is from a **senate debate** posted on `2011-10-12`, and its ID `47.1` is used to identify its URL.

- **`house_debates`** contains **116,480** [house debates](https://www.openaustralia.org.au/debates/#help) recorded from **2006 to 2024** (last time updated on 2024-08-22).

  Each file has the same naming convention `[date].[id].html`. For example, `2012-03-21.143.1.html` is from a **house debate** posted on `2012-03-21`, and its ID `143.1` is used to identify its URL.

Notice that the first line of each `.html` file includes its original URL to OpenAustralia, e.g., `<!--https://www.openaustralia.org.au/debate/?id=2017-03-29.89.1-->`.

## Download

For downloading resources from OpenAustralia, we developed Python scripts under `utils` for you to understand how we build URLs, and you can modify the search time range for each debate database.

## License

This repo is licensed under [MIT](https://opensource.org/license/mit).

