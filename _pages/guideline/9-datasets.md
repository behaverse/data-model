---
title: Organizing datasets
parent: "Standards and conventions"
grand_parent: Guideline
layout: page
nav_order: 8
---

# Datasets


<hr />

## Table of content
{: .no_toc .text-delta }
- TOC
{:toc}

Datasets can be organized and stored in many different ways. This section focuses only on the organization of datasets that are destined to be archived on a specialized website and/or shared with other researchers who might want to reproduce results or process the data in novel ways. These data sets can be seen as static and encapsulated/standalone; they are not meant to be updated and augmented as new data comes in.

Data from research projects often fit naturally in that category because a study will typically define a data collection campaign with a clear scope and well defined start and end times (determined for example by the timeline and funding of a particular research project). However, this need not always be the case. A research group may for instance collect data on a particular task for a long period of time and use different subsets of that data for different studies. 


## Ordering tables

### Ordering of variables within a data table
The ordering of the columns within a table may facilitate the understanding of particular variables and can be useful when inspecting the data. Columns in a data table should be ordered according to the following rules:

first the primary key of the table, 
first the general, then the specific variables,
first the parameters/fixed variables, then the measurements,
group columns that are semantically related (e.g., columns describing the task, columns describing the response). 
if there's an implicit ordering, use that ordering (the stimulus was shown before the response was recorded, the stimulus columns should be to the left of the response columns);
order columns alphabetically.

Regarding the ordering of the suffixes within an entity (e.g., block) we use the following convention:

block_type > block_name > block_id > block_index

Rows should be ordered using the indexing rules described earlier; that is ordered by study, then subject, then session, then timeline, then episode, then task and finally trial. This will also be the ordering of the primary key of the table.

### Tidy tables
"Tidy data allows one to start analyzing the data right away"
Wickham, Hadley (20 February 2013). "Tidy Data" (PDF). Journal of Statistical Software.

Data should be in a tidy format. However, it is not always clear what that actually means. Take for example the case of survey data: should a row contain all the data for one participant (in which case each question has its own column) or should it contain the data for a single question (in which case there would be as many rows per participant as there were questions in the survey)?

When all the questions are of the same Type (say, "True/False" questions), one can have one row per question as the values within the same column would be of the same type (e.g., all responses are either "True" or "False"). But what if some questions ask about "True/False" and others ask for a rating from 1 to 5 and still others ask for a written text? In this case we can no longer have a row per question because the values would not be of the same type across rows; in this case, it seems to make more sense to have the questions be organized in columns rather than in rows. 


We currently do not have a satisfactory solution to deal with survey data using tabular data. All of our solutions have pros and cons and we finally decided for the following rules:
Firstly, survey data will be organized as a table per questionnaire where each row represents data from one subject and each question has its dedicated columns. We will use this "wide" format even when all questions and responses within a questionnaire are of the same "type" and a "long" data format would be possible. Second, data about the meaning of the variables (e.g., the exact wording of a particular question) will be stored in a separate table. Finally, variables in the survey data table should be given names that are indicative of the question (what does "q212" mean and how is it different from "q121"?) and need not be prefixed by the name of the questionnaire. Prefixing the questionnaire name might however be useful (to locate columns) or necessary (because the same column name is used for two different questions from different questionnaires) when combining data across multiple questionnaires. 

Note: it might be useful to use a hashing technique to guarantee various documentation files actually refer to specific dataset (by having the hash of the data (md5) in the documentation itself).

Note: some variables may have values that look as if they should/could be split into multiple, more tidy columns; it is OK to have such variable values to the extent that they are supposed to be used as is. For example, imagine there is a variable called timeline_name which takes values of the form `<instrument_name>_<number>`. It is in principle possible then to split this column in two columns that could be named `<instrument_name>` and `<timeline_number_in_instrument>`. However, the intention might be to have a variable to designate the construct "timeline" (which happens to be formatted in a principled way) rather than have two variables, one of which being rather useless on its own (i.e., `<timeline_number_in_instrument>`).
