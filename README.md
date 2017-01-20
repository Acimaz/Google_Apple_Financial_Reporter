#	Google and iTunes Connect Reporter

## For what?
This script can be used to query Sales- and Financial Reports from both **Google** and **Apple**.
The google part uses the Google API client library with a OAuth2 authentication to request the wanted reports.
The Apple part uses a python script written by a Github user named "fedoco". I just changed a few lines for me to work with it.
The script bundles both parts and writes the following columns into a "financialReport.csv" file: **Date**,  **Platform**, 
**newSubscriptions**,  **cancelledSubscriptions** and **activeSubscriptions**.
The data is always downloaded for one single day and then this data is applied to the end of the csv file.
There is a limit (which you can change to whatever you want ofc) of 58 days (58 data rows plus 1 header row).

## Why?
As the user fedoco explains, there is a tool called "Reporter" and it sadly is based on Java (for whatever smart or not so smart reason..).
As for the google part... well there is no such tool to do exactly this: Download new subscribers, cancallations and actively paying users counts
in order to visualize it in some other tool, like Klipfolio for example.
We decided to write this tool and we wanted it to work on **Amazon Lambda (AWS Lambda)** and then save the reports on a **S3-Bucket** to retrieve 
fit rom there via API calls.
This tool provided here is not ready for that as it only works locally! But there is another repository im going to upload which is in some parts 
rewritten to work on **AWS Lambda**. You if you are looking for that, just change the repo :)
 
 ## What do i need to use this tool?
 Well, obviously this tool wont work as is. There are a bunch of variables you have to set inside the python scripts and you have to provide a valid 
 json file to the service account on google you are using to fetch the data through. You can download it when you created the service account.
 Because i know that this is a pain in the ass to find because the documentation is.. **Ok**. Here is a link where you can create service accounts for
 the specified project: https://console.cloud.google.com/iam-admin
 
 Here is a list of variables you need to change for sourself and corresponding python script names where you can find them:
 ```text
 client_email in **GoogleReports.py** - Example: 'testDev@somethingYouCanSeeOnYourServiceAccountOnly.iam.gserviceaccount.com'
 json_file  in **GoogleReports.py** - Example: 'theNameToYourPrivateJasonKeyOfYourServiceAccount.json' (you can download/create this key via the 3 dotted menu on your service account on the Service Accounts page. Just drop the file into the same folder as the other .py scripts)
 cloud_storage_bucket  in **GoogleReports.py** - Example: 'pubsite_prod_rev_YOURBUCKET_ID' (you can find this id when you go to your Google dev console and click on your app and then financials and then try to download something. On the next page there are URI's listed like "gs://pubsite_prod_rev"...)
 report_to_download in **GoogleReports.py** - Example 'financial-stats/subscriptions/NameOfFileYouWantToLoad_' (dont forget the underscore, the rest of the filename is added dynamically according to the date you want the reports from)
 vendorId in **AppleReporter** - Example: 41064164 (you can get this number in starting the ApplePythonReporter.py made by fedoco as standalone with the needed parameters. For more info on this check out his Github page on https://github.com/fedoco/itc-reporter)
 userId in **AppleReporter** -  Example: 'itunesconnect@awesome.com'
 password in **AppleReporter** -  Example: 'MyAwesomePassword'
 account in **AppleReporter** -  Example: '326591'		(you can get this number in starting the ApplePythonReporter.py made by fedoco as standalone with the needed parameters. For more info on this check out his Github page on https://github.com/fedoco/itc-reporter)
 ```
 
 I tried to provide you with the neededl ibraries inside the projects "lib" folder.
 
## Usage examples
 Well, this is pretty straight forward. The only thing you have to do if you want to load the reports for, say 2 days ago, is the following:
 ```sh
 Reporter.py -d 2
 ```
 and for help 
 ```
 Reporter.py -h
 ```
 There is not much of a help though beside this command.
 
## What you could do with it
 This depends on what you want to have, but i am using it for example to load daily reports and im using a scheduler to execute this script with -d 2 every day.

## Why 2 days before and not today for live data?
 Because unfortunetaley neither Apple nor Google are refreshing their report data fast enough for us to load live data.
 I found it pretty stable though for reports from 2 days ago.
 
 ## Obligatory disclaimer
 There is absolutely no warranty for this tool. I do not guarantee in any way that this tool works as intended. 
 At the time im writing this it works for me and maybe it will work for you too or at least helps you write your own tool!
 
## Information about me
 Im not a python developer. Im a C# and Unity3D Software Developer working at Kaasa health GmbH in Düsseldorf, Germany and we try to monitor our financial 
 stats in various ways. One of it is using this tool to load reports form apple/google.
 If there is something i can correct (even if its only visual for better looking code) are welcome! :)