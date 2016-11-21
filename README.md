# Install

You must install the pytrends library:

```
sudo pip install pytrends
```

Then find the `request.py` file installed on your computer (e.g., `/Library/Python/2.7/site-packages/pytrends/request.py`) and add the following function after the `trend` function:
```
    def geomap(self, payload, return_type=None):
        payload['cid'] = 'GEO_MAP_0_0'
        payload['export'] = 3
        req_url = "http://www.google.com/trends/fetchComponent"
        req = self.ses.get(req_url, params=payload)
        try:
            if self.google_rl in req.text:
                raise RateLimitError
            # strip off js function call 'google.visualization.Query.setResponse();
            text = req.text[62:-2]
            # replace series of commas ',,,,'
            text = re.sub(',+', ',', text)
            # replace js new Date(YYYY, M, 1) calls with ISO 8601 date as string
            pattern = re.compile(r'new Date\(\d{4},\d{1,2},\d{1,2}\)')
            for match in re.finditer(pattern, text):
                # slice off 'new Date(' and ')' and split by comma
                csv_date = match.group(0)[9:-1].split(',')
                year = csv_date[0]
                # js date function is 0 based... why...
                month = str(int(csv_date[1]) + 1).zfill(2)
                day = csv_date[2].zfill(2)
                # covert into "YYYY-MM-DD" including quotes
                str_dt = '"' + year + '-' + month + '-' + day + '"'
                text = text.replace(match.group(0), str_dt)
            self.results = json.loads(text)
        except ValueError:
            raise ResponseError(req.content)
        if return_type == 'json' or return_type is None:
            return self.results
        if return_type == 'dataframe':
            self._trend_dataframe()
            return self.results
```

# Running

Run the `getwords.py` as follows:
```
python getwords.py
```

Insert a username and password for a **logged in** Google Account (but
you probably want to avoid using an account you care about).

# Getting the results

The script will add results to the `results.csv` file.  Display them
by running the `display.R` R script.
