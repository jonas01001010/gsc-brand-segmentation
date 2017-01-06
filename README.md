# gsc-brand-segmentation
Script (python 3.5) to automate brand segmentation of traffic for each URL

Tools.
-	Python 3.5
-	Pip install: 
o	google-api-python-client
o	pandas

References:
-	https://developers.google.com/webmaster-tools/v3/how-tos/search_analytics
-	sample: https://github.com/google/google-api-python-client/tree/master/samples/searchconsole

Context:

Many online marketers have difficulties when it comes to evaluating the efficiency of their search traffic. Indeed traffic coming from organic search results could be due to branding, but could also be due to SEO. Over the past years it has become even more difficult to differentiate this traffic (issue known as non provided keywords by SEOs). But the differentiation of this traffic becomes increasingly important when brand campaigns are launched, or/and many efforts are made on SEO.

Indeed the costs of brand campaigns or the investment in SEO can take a lot of resources from marketing, and to optimize those costs it is necessary to differentiate the results from these campaigns. This is why we usually segment the organic search traffic in 2 categories: non brand organic traffic (SEO) and brand organic traffic. Brand traffic is due to the performance of the branding campaigns, with users looking for your brand on search engines. Non brand traffic represents the users that are looking for your service/products and land on your site. This usually is due, or at least maximized, with SEO efforts.

It is often a bigger challenge to do this segmentation for companies providing services. An e-commerce websites usually have a lot of landing pages. By optimizing those landing pages with different SEO queries, we can assume that most of the traffic from search on those pages is due to SEO efforts. For companies offering services (and more specifically a unique service) it is not so simple. Because most of the time the service is presented on the homepage. And SEO, to rank on the relevant most searched queries, optimize the homepage to maximize its traffic. A user searching for the brand on search engines also mainly lands on the homepage.  By doing both brand and SEO investments, the traffic on the homepage increases. Therefore the evaluation of the ROI or other KPIs (such as traffic, registrations, sales…) becomes also increasingly difficult.

Since the main search engines are protecting user data, it is not possible to know what the users are typing in to land on your website from organic search. The proposed solution offers an estimate of the share of those brand and non brand queries typed. By doing this segmentation, we can then estimate the share of SEO non brand traffic, and all other KPIs (from registration, to lead and revenues).

Several online tools offer the same data that will be provided by the script. The script extracts data from one of these tools (Google Search Console API) and automates the segmentation process. Some companies offer a similar service. Though they also use the same Google Search Console source for data, and their API does not allow extracting the segmentation data which doesn’t enable automating the process fully.


Process:

Using the Google Search Console API and a python script, we can extract the share of brand and non brand traffic per landing page. The process can be automated for any website (or property set) and for any timeframe.
The script is based on Python 3.5. Since I am a beginner at Python it has many things that could be done better in it. 
It has 3 main parts:
1-	Extracting queries types in Google to access your website (brand and non brand)
2-	Doing a VLOOKUP to match, for all your landing pages, the number of brand and non brand queries
3-	Calculating the share of brand and non brand traffic for each URL, and writing it in a csv file

One very important step is to first define your brand pattern. They are the queries that usually type in search engines to find you brand. You can find a lot of suggestions in the desktop version of Google Search Console. In instance a user looking for the brand “apple” could type “apple|apel |appe|…” while the non brand queries due to SEO could be “smartphone|phone|smrtphone|….”. 
Evidently there are far more non brand patterns than brand patterns. It will so be needed to define the brand pattern, and replace it in the code (XXXXXXX LINE 32 to 56).
The script can be customized for other needs, since based on the sample provided by Google (see below), almost all kind of data can be extracted.

Specs:

The first part of the code extracts:
-	For all pages: non brand clicks, non brand impressions and avg_position
-	For all pages : all clicks, impressions, and avg_position

The second part of the code prints 2 temporary csv file for the two requests (can be used for any possible request).
The third part of the code divides non brand clicks by all clicks, and create two columns (%brand and %non brand clicks for each page). A final CSV file is created.

Expected outcome:

The final csv file will have this format:

Page | NB impressions | NB clicks | NB avg_position | Brand clicks | %non brand | %brand

https://www.example.com/aaaa | 100 | 6 | 2.34 | 4 | 0.6 | 0.4

https://www.example.com/bbbb | 200 | 10 | 1.91 | 90 | 0.1 | 0.9

It can later be combined with internal company reports. For example for this report:

Page | Channel | Visits | REG | SALE | Revenues

https://www.example.com/aaaa  | SEO | 10 | 2 | 1 | 1000€

https://www.example.com/bbbb | SEO | 100 | 70 | 30 | 20000€

Can become this adjusted SEO report:

Page | Channel | Adj_Visits |Adj_ REG | Adj_SALE | Adj_Revenues

https://www.example.com/aaaa  | SEO | 10 | 1.2 | 0.6 | 600€

https://www.example.com/bbbb | SEO | 10 | 7 | 3 | 2000€


