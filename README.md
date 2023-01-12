This is a subcomponent for a Master's Thesis Project at the TU Berlin.

This projects contains two scrapers that collect data about functions provided by [pandas](https://pandas.pydata.org/docs/reference/index.html) and [scikit-learn](https://scikit-learn.org/stable/modules/classes.html) API references. 

The data is being scraped in a following format for each function: <br />
full function title, function description, link to the doc reference, function arguments

To start a scraper, go into the folder with the scripts:
~~~
cd ds_scraper/ds_scraper/spiders/
~~~

And start the respective scraper: 
~~~
python pandas_scraper.py
~~~
or 
~~~
python sklearn_scraper.py
~~~

In the same folder you can find the postprocessing script. Currently, it only appends an index column in front.
To start, cd into the same folder as for scrapers:
~~~
cd ds_scraper/ds_scraper/spiders/
~~~

And call the script with input and output files as arguments respectfully:
~~~
python postprocessing.py -i "input_file" -o "output_file"
~~~
