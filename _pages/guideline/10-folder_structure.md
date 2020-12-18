---
layout: page
title: "Folder structure"
permalink: guideline/folder-structure
parent: Guideline
nav_order: 3
---

# Folder structure

When data sets become large or involve many different kinds of tables it becomes necessary to organize the data into a folder structure. We will use the pattern described in The Brain Imaging Data Structure (BIDS, https://bids.neuroimaging.io). BIDS defines a clear standard for organizing and data in folders. We first describe the general principle before giving examples


Study/
├─ README.md
├─ description.json
├─ General/
├─ *Subject*/
│  ├─ General/
│  │  ├─ description.json
│  ├─ *Session*/
│  │  ├─ *DataType*/


The data is grouped first by study, then by subject and the data within each subject is further organized by session (when applicable) and finally data type. This organization makes sense in the context of brain imaging data because the data files per subject and session can be quite big and are processed at the individual level (e.g., preprocessing of fMRI data) and may lead to additional files that can then be stored in the same folder. It is typically only at later stages that data is aggregated across subjects and that data has been already heavily processed and summarized.

Most behavioral datasets do not follow the BIDS way of organizing data files and instead either have a table per task (including the data from all subjects in the same table) or a folder per task which contains a file per subject. Organizing data by task makes sense because a task defines a data schema that will be the same across subjects. Grouping subjects in a common table also makes sense because the data is usually small and typically processed all at once rather than on a subject-by-subject basis. However, as data sets become larger, there are several advantages to using the BIDS convention (in addition to consistency, this includes for example a greater ease to understand the scope of the indices or the ability to easily delete all the data from one particular subject who might request it). 


BIDS uses a hierarchy principle to avoid duplicating information across many folders: if some information applies to all the sessions of one subject, that information should be in the root folder of that subject's data. Information that is closest to the actual data file has priority over information presented at a higher level; this allows one to specify the general parameters at the root of the study folder and only include changes relative to those general parameters when they apply.  It is OK but not strictly necessary to follow this pattern.

The folder structure we will use is described below. Note that entities surrounded square brackets "[ ]" are optional and may be used only when applicable and entities marked with a "*" are replicated for each instance of the class (e.g., for each subject in the study).  

<study-name>/
├─ sub-<label>
├─── [ses-<label>]
├───── [beh/]
├───── [func/]
├───── [anat/]



...


Here's an example folder structure:

SDS_v2020.10/
	description.json
	*sub-<label>/
		*ses-<label>/





Defining terms like Session and Dataset; 
https://bids-specification.readthedocs.io/en/stable/02-common-principles.html




Naming data files and data folders

There are various good recommendations on how to name data files. In general, we will follow BIDS in using a specific naming pattern to name files, which takes the following form:


<key 1>-<value 1>_<key 2>-<value 2> … <.extension>

where the keys can only take a small set of possible values and must be entered in a specific order. For example, a valid BIDS filename might look like this:

sub-2475379_ses-1_task-rest_acq-TR2500_bold.nii

Note that we only use a subset of the BIDS keys as well as additional keys which are not used in BIDS (marked below with an * below): 
sub means subject (i.e., participant, person, animal), 
ses means session (index), 
task is the name of the activity performed by the participants (e.g., "nb", "bm", "ds"); 
*timeline|config is the name for the particular configuration used (e.g., "xcit_nb_01");
*rep "counts" repetition of completing a specific timeline;
desc means description and allows to manually tag particular data files; "desc" should only be used when strictly necessary;
*type indicates what type of data the file contains (e.g., "trial", "stimulus").


Hence a data filename within the Behaverse Data Model follows this pattern: 

sub-<label>[_ses-<label>]_task-<label>[_timeline-<label>][_rep-<index>]_type-<label>.csv

Note: one reason for using the BIDS file naming convention is that some file systems (e.g., FAT32) are case insensitive and CamelCase displayed in all lower case letters canbequitehardtoread, while the text-separated-by-dashes-is-not.

Note: the use of long filenames can sometimes be problematic (e.g., not recognized by software, relevant parts truncated in the file viewer) and is to some extent redundant with the folder structure and names. However, encoding information in the filename seems more robust than encoding it in the path and allows one to know what a file is about without having to open the file or open other files.











Naming Datasets
If a dataset B is derived from dataset A, it is expected that the derived dataset has the same root as dataset A but a specific postfix (e.g., "income_luxembourg_2020.csv"). 

A dataset may also have a version; in this case the filename should have a postfix expressing the version using semantic versioning (https://semver.org/); for example, "income_luxembourg_2020_v1.0.1") or calendar based versioning (calver.org ; for example "income_luxembourg_v2020.10."). For versioning datasets we recommend the use of calver.


Data file types

BIDS uses TSV rather than CSV for tabular data;
json for meta-data
https://library.stanford.edu/research/data-management-services/data-best-practices/best-practices-file-formats

There are two main file formats that seem most appropriate to store tabular data: CSV (comma separated values) and TSV (tab separated values). CSV have the advantage of being more common and can be read by most software that uses tabular data. TSV is less common but is technically more efficient, less error prone and more human readable. TSV is in particular more appropriate than CSV in cases where the values in a cell can contain commas, which is obviously very common in text data, and where the commas within a cell must be distinguished from the commas that serve as separators (tabs are much less common in data values). While TSV is less common than CSV, all advanced data analysis tools are able to easily handle tsv files and people who can't handle tsv files can find tsv to csv conversion tools. 

It seems therefore, that TSV is a better option for behavioral data and we will export our data in that format. This has the added benefit that we'll be consistent with BIDS who also uses the tsv fileformat for their behavioral data.

https://en.wikipedia.org/wiki/Tab-separated_values 
https://odino.org/tsv-better-than-csv/
https://stackoverflow.com/questions/11130120/choosing-between-tsv-and-csv


Example


SDS_v2020.10/
sub-001/
		ses-01/
			sub-001_ses-01_task-nb_timeline-xcit_nb_01_type-trial.csv
sub-001_ses-01_task-nb_timeline-xcit_nb_01_type-stimulus.csv
sub-001_ses-01_task-nb_timeline-xcit_nb_01_type-option.csv
…
		ses-02/
			sub-001_ses-02_task-nb_timeline-xcit_nb_01_type-trial.csv
sub-001_ses-02_task-nb_timeline-xcit_nb_01_type-stimulus.csv
sub-001_ses-02_task-nb_timeline-xcit_nb_01_type-option.csv
…

sub-002/
		ses-01/
			sub-002_ses-01_task-nb_timeline-xcit_nb_01_type-trial.csv
sub-002_ses-01_task-nb_timeline-xcit_nb_01_type-stimulus.csv
sub-002_ses-01_task-nb_timeline-xcit_nb_01_type-option.csv
…
		ses-02/
			sub-002_ses-02_task-nb_timeline-xcit_nb_01_type-trial.csv
sub-002_ses-02_task-nb_timeline-xcit_nb_01_type-stimulus.csv
sub-002_ses-02_task-nb_timeline-xcit_nb_01_type-option.csv
…
	…




