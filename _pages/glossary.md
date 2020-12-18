---
layout: page
title: Glossary
permalink: glossary
nav_order: 99
last_modified_date: Jan 20, 2020
---

# Glossary
There are many concepts related to data and it is worth describing them quickly to make explicit what we mean when we use such terms. We can describe data using terms that indicate how it is stored/organized and terms that indicate how much the data has been "processed". In addition there are terms for the entity that contains the data and for various processes involved in the collection, storage and processing of data. 

Data by levels of processing
: Data that has not been processed at all is termed "raw" data. Data that is computed from other data, for example summary data, is called "derived" data. For reproducible research we want to share raw data with data analysis code that allows others to recompute all the analyses within a research project from the raw data, rather than only sharing the derived data. 

Data by file format and structure
: Multiple different system may record data in a variety of forms (e.g., structured, unstructured) and file formats (e.g., ".csv", ".json", ".dat"); data in their "native" form are called "source data". "Tidy" data is data that is organized in tabular form where each row is an observational unit and each column is a variable or property of that unit.

Data storage paradigms
: A "data lake" refers to an unstructured collection of data, typically from many different sources. On the one hand, the data lake can be seen as maximally flexible (accepting all sorts of data) and holding the potential for limitless data analysis enterprises; on the other, the data lake can be seen as a chaotic data dump or data swamp. A "data warehouse" organizes the incoming data in a consistent way (schema) before storing it. Data from the data warehouse can (more) readily be used for data analysis; data from data lakes require significant background knowledge and work to be processed.

> Some people use the term data mart to refer to either a subset or a view of the data warehouse (https://martinfowler.com/bliki/DataLake.html; https://en.wikipedia.org/wiki/Data_mart).
{: .note }

Database
: A database usually refers to a collection of data that is under the control of a database management system (DBMS); database typically implies some form of interaction between the data and end users who read or write data from or into the database.
: See https://en.wikipedia.org/wiki/Database.


Dataset 
: A dataset also refers to a collection of data but while a database is a "living" entity, a dataset is typically a static resource which can be downloaded and shared as a whole (e.g., the PISA 2012 dataset). A dataset can be defined by a data collection campaign (e.g, all the data collected within a the research project) or a data analysis campaign (e.g, a dataset created from a larger medical database that focuses specifically on mental health issues during the COVD period).
: See https://en.wikipedia.org/wiki/Data_set

## Confusing terms

It is sometimes easy to confuse the terms described above. For example, source data is often called raw data even though the source data may in fact contain derived data (for example, the overall score a person achieved on a school test alongside all individual responses and their correctness). Source data is often messy but could in some cases be tidy.

Note also that it is not always clear what is meant by "processing" and what still counts as "raw data". In our opinion, data is no longer "raw" when the data has been processed in a way that reflects assumptions about the values and relationships between variables. For example, filtering out trials with response times shorter than 150 milliseconds because one believes that such short durations imply those responses are not valid, is a form of data processing which is "biased" and thus the resulting, filtered data cannot no longer be considered "raw". On the other hand, if for some reason, a system logs the same events multiple times, removing duplicates is a data processing step that is not biased and hence, the resulting, filtered data should still be considered "raw" data.

In general, we believe that the following operations may be performed on source data without compromising the "raw" status of the resulting data:
- selection of variables
- renaming variables and enum values
- changes of units (from example, converting milliseconds to seconds)
- reordering of columns and rows
- removing duplicates
- joining or separating tables



### Which data to store? Which data to share?

It is typically the case that more data is stored than is shared. For example, researchers may store participants contact information or specific parameters of the hardware being used. The question then arises of what information should be collected in the first place and what subset of that data should be shared and whether or not the source data should be sent along with the data extracted from that source data.

Regarding what data to store, the answer depends on the purpose of the study. In any case, participants need to be informed about what data is being collected and the data collection must follow relevant regulations. It is generally well advised to be parsimonious regarding which personal data to collect (https://martinfowler.com/bliki/Datensparsamkeit.html). 

In our opinion, source data should not be shared if one has the ability to extract and share better formatted data. There are three main reasons not to share source data:
1. source data is not useable: they can be messy, come in diverse, sometimes proprietary formats, and lack documentation.
2. source data may contain personal data the data sharer is not aware of (e.g., participants' full name, IP address); by defining what data is to be shared and extracting only that data it seems that such accidental privacy breaches could be avoided.
3. the extraction of data from the source data into usable data is outside the scope of responsibility of the data analyst.

This last point deserves further explaining. For research to be reproducible one may want to test all the steps from the data collection up to the final results. While all the steps might be tested, they are not necessarily tested by the same person. For instance, a software company may run tests to determine that the recorded timestamps are accurate and a lab technician may run tests to calibrate the monitor and other hardware equipment. The question of what data to share is related to what quality assurance (QA) requirements are expected to be fulfilled by the data analyst. If both the source data and data extracted from the source data are handed over to the data analyst it becomes the data analyst's responsibility to verify that both sets of data are in fact in agreement. If there is an error in the extraction code, the data analysis becomes responsible because he/she had access to that and could thus have spotted and corrected the error. In our opinion, the preparation of usable data from source data is not the responsibility of the data analyst; it is the responsibility of the data engineer and the entity that is sharing the data. It remains however that in any case tests must be conducted to verify the validity and accuracy of the process (we simply argue this is not the role of the person receiving the data). 

In short then, we say "don't share source data", instead share well documented, well formatted, tidy raw data.

### Organization of standalone single study data

There are different valid options to organize standalone single study data and there are certain rules that apply to all such organizational systems.In particular, any dataset must have 
a document that describes and gives background information about the dataset as a whole (e.g., README.md, licence);

a code book that describes the meaning of the variables and the values they can take. 
Ideally these documents should have a code (hash) that guarantees that they refer to a particular dataset. These elements will be described later.


