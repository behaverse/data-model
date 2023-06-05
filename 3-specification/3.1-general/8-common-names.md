---
title: "Other common names"
parent: "Standards and conventions"
permalink: guideline/common-names
grand_parent: Guideline
layout: page
nav_order: 8
---

# Other common names

<hr />

## Table of content
{: .no_toc .text-delta }
- TOC
{:toc}

age [float]
: `age` is typically expressed in years. However, we don't recommend flooring "age" to get integer values, as flooring implies losing data. It is better to leave variables as floats (when they are floats) and let the analyst decide whether or not flooring this variable is necessary for their specific purpose.

accuracy [float]
: `accuracy` refers to a measure of performance; in many tasks, it reflects the percentage (0-100%) or fraction (0-1) of correct responses. We will always use `accuracy` to refer to a performance measure that is a float and bounded in the [0-1] range.

correct [boolean]
: `correct` is a boolean variable which indicates for a given trial or response whether it was correct or not. When no response was given when it should (i.e., timeout), correct evaluates to `FALSE` rather than `NA`. This is to avoid the case where people would be given a high performance score when in fact they avoided all difficult trials and responded correctly only to easy trials.

response_time [float]
: the meaning of `response_time` (and its units) is not consistent across studies. For us, `response_time` is the duration between the moment the participant fully completed their response on a given trial and the moment that the earliest possible correct response could have been completed by an AI agent with perfect knowledge of the task and ability to instantaneously execute the response.
: **Default unit:** seconds  

> Other measures of durations exist and may be useful to describe a person's response. If such additional measures are needed, they should be specified explicitly. For example
> - `response_onset`
> - `response_offset`
> - `response_duration`
{: .note }

> Units for response times are not consistent across papers and publicly available datasets and one can find them expressed in either seconds or milliseconds. We decided to use seconds as the default unit for response times because:
> - avoid "exception" by always using seconds as duration measure.
> - avoid computation by keeping the units as they currently are in our raw data and task specs.
> - avoid the temptation to round rt to integers when expressed in milliseconds.
> - take advantage of the fact that most packages to analyse rt seem to be using seconds as a default unit; be congruent with what seems to be the default unit in fMRI measurements. 
{: .note }

> It is tempting to abbreviate `response_time` as `rt`; however, there are several other variables prefixed `response_` which do not have abbreviations. Spelling the names out, while making the name longer, makes the overall data structure more consistent and explicit.
{: .note}

timed_out [boolean]
: indicates whether the participant failed to respond within the allocated time period. 

gender/sex [enum]
: gender and sex are not exactly the same. Sex refers to a biological sex while gender is a more complex construct. A person may have a male biological sex but identify as a women for example. Depending on the question asked, the variable should therefore be either `sex` or `gender`. *"What sex were you assigned at birth, such as on an original birth certificate?"* is clearly a question about biological sex and should be coded as `sex`.
: The values for `sex` should be an enum:
- `Female`
- `Male`
- `Other`
- `Prefer not to say`










## Standard variable name suffixes 

### Standard feature names
Variables may describe a feature or property of an entity, using the format <entity>_<feature>.  

length
: refers to the length in cm of a physical object. When possible use a more specific word (e.g., height, width, distance). Don't use length to mean count or size!

height, width
: refers to the height and width in cm of a physical object.

weight
: refers to the weight in kg a physical object.

~~size~~
: don't use "size" as this term is ambiguous. "size" could refer to 180cm, "Medium" or 230x230. Instead, use a more specific term.

count
: refers to the cardinality of the entity. If an observation/row has `car_count = 5` this means that this particular observation involves a total count of 5 cars; this 5 is unrelated to other rows in the table.

## Standard suffixes
All names below are not to be used alone but rather as suffixes (e.g., "block_type", "stimulus_description").

*_type [enum]
: is always an enum. The meaning of the particular enum needs to be explained in a codebook.
It can be tempting to use synonyms of "type", in particular when "type" is already taken; such synonyms include things like "category", "kind" or  "set". When those synonyms are not required (e.g., domain language) they should be avoided and replaced by "type". Not all enums however need to be suffixed with "type". 

*_description [string]
: is always a text (String) for human consumption. While it is not strictly necessary, a textual description can greatly facilitate the understanding and processing of the data by humans.


### Standard aggregation suffixes
We will use the following names as suffixes to refer to particular operations in variable names. For example the mean of a variable "age" would be called "age_mean" (and not for example age_avg or age_m). We typically use the same name as the aggregation function name in R or Python. More specialized terms require explicit descriptions.

mean
: average of the variable. Don't use `avg` or `average`.

median
: median of the variable. Don't use `med`. 

mode
: mode of a variable.

min, max
: minimum and maximum of a variable

sd
: standard deviation of a variable. there are many other abbreviations for the standard deviations for the standard deviation but https://en.wikipedia.org/wiki/Standard_deviation uses SD and SD is the most common according to https://www.abbreviations.com/abbreviation/Standard+Deviation. However we won't use sd in all caps.

var 
: variance of a variable.

sum
: the sum on a variable (e.g., `item_price_sum = sum(item_price)`). Don't use total to designate the result of a sum operation. 

count
: integer value, refers to the count of a particular entity (e.g., a variable named `page_count` indicates the number of pages). Note that "count" is different from "sum" (e.g., one can sum negative float values while count involves positive integers only) and from "index" (e.g., "this is the second" versus "there are two").
Note also that while the use "n" to refer to counts is much shorter and might be standard in some circles, "count" is more explicit and less error prone than "n" which may mean different things in other contexts (e.g., the length of the variable, an iterator).

quantile25, quantile50
: quantiles are similar to percentiles; both refer to the value of a variable x that splits the data such that a given fraction of the data is smaller than x. Quantile expresses that fraction as a number between 0 and 1 while percentiles express it as a percentage (between 0 and 100). 

> We use quantiles rather than percentiles because they allow us to name the resulting variables in a simpler way. We use the following convention: 
> - `quantile(x, q = 0.23)` -> `quantile23`
> - `quantile(x, q = 0.145)` -> `quantile145`

{: .note }


There could be an ambiguity when using `quantile(x, q = 0.100)` versus `quantile(x, q = 1)`. However, note that `quantile(x, q = 1)` is in fact equivalent to `max(x)`; `quantile(x, q = 1)` is `median(x)` and `quantile(x, q = 0)` is `min(x)`. In these cases it is preferable to use the more direct name (`max(x)` rather than the `quantile(x, q = 1)`).
{: .note }


### Standard transformation suffixes
In general, use the function name that was used to do the transformation. 
For example the log of a variable `age` would be called `age_log` (and not for example `log_age` or `age_in_log`). We typically use the same name as the transformation function name in R or Python.  We will use the following names to refer to particular operations in variable names.

log, log10, log2
: natural log, log of base 10, log of base 2. Always specify the base when using the log except for the natural log (this seems standard in R and Python).

sqrt
: square root of a variable.

pow2, pow3, pow4, ...
: square or raised to the power of 3, 4, etc.

floor, ceil, round
: flooring, ceiling or rounding a variable. Rounding may require specifying additional parameters.

rank
: variables can be ranked (for example from the smallest to the largest values) and some values can be tied (in which case the rank will no longer be all integers). It might not be clear if the ranks are descending or ascending (e.g., `age_rank`). If such confusion arises it might be preferable to use a more direct name (e.g., `youngest_to_oldest` or `youngest_first_rank`).


### Standard referencing postfix terms
Several variables are used to filter, identify or locate particular rows in a table or across multiple tables. Below, we list and clarify the ones we use and how we use them.

> Note: some people start counting from 1 others from 0; here we follow the convention of always starting counting/indexing from 1.
{: .note }

*_id [string, integer]
: if a column name is postfix with `_id` (e.g., `participant_id`, `task_id`) it is expected that there exists a table which has the same name (i.e., "participant", "task), with a primary key named `id` such that a value of in the first (`particiapant_id = 215`) refers to an entry in the second (a row in the participant table where `id = 215`). It is expected that the values in a variable postfixed `_id` are unique within a "local scope" (e.g., a dataset); however, it is not expected that they are unique globally—for such purposes one should use the `_uuid`.
: If there is a column named `id` (i.e., without prefix) it is expected that there are other data tables or files that refer to this column; if such a link does not exist, use `index` instead.
Finally, the postfix `_id` does not imply a particular value format: both integers and strings are valid formats. 

*_name [string]
: Sometimes "name" is used in a way that is similar to id (e.g., `study_name` or `task_name`).
The difference between `_id` and `_name` is that `_name` is expected to be a readable string (e.g., `n-back` versus "f346-r23v"). As with `_id`, it is expected that name refers to other data tables and that names are unique within a certain context (contrary to `*_label`).

*_uuid [ISO/IEC 11578:1996; string] 
: Universally Unique Identifier (https://en.wikipedia.org/wiki/Universally_unique_identifier) is a 128-bit number that can be generated on the fly and will most likely be unique. uuid can be used to assign a row a unique id without having to ensure that that number is not yet used by some other table.
: _uuid are expected to be unique (globally); 
: _uuid are not expected to be human readable; 
: **Example**: `123e4567-e89b-12d3-a456-426614174000`

> There also exists a uid which we don't cover here.
{: .note }

*_hash
: sometimes it is useful to create a key by combining other keys. A hash is not strictly necessary as it can be recreated using other variables but it can be convenient for data processing.
https://en.wikipedia.org/wiki/Hash_function 
: There is not a single standard for hashing; rather there are multiple algorithms that can be used. We use both CRC32 (32 hexadecimal characters; e.g., "098f6bcd4621d373cade4e832627b4f6") and SHA256 (base64 characters, e.g., "d14a028c2a3a2bc9476102bb288234c415a2b01f828ea62ac5b3e42f"); depending on the probability of collision (i.e., two hashes being identical); when that probability is deemed high, we use SHA256.


*_index [integer]
: index should be favored when a variable is used for referencing and when order is important (often, but not always the chronological order).  For example, "stimulus_position_index" implies its value points to an entry in a list of possible stimulus_positions. Note that "index" typically implies a context within which the indexing occurs and that context must be made explicit. For example, trial_index may index trials within a block or a timeline.

*_repetition
: is used to count the number of times the same "thing" occurred (e.g., a participant completes the same test twice, the same stimulus appears multiple times). As with index, repetition assumes a context which must be clarified when ambiguous. 

> Repetition starts "counting" at 0 rather than 1; *_iteration instead of *_repetition would solve this issue but is less explicit and thus less preferred.
{: .note }

*_label [string]
: an text attached to a variable; expected to be human readable, but not unique. 

> We avoid the use of `*_number` because it is typically too general and thus confusing.
{: .note }









