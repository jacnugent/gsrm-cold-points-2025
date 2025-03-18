"""
split_soundings.py

Code to split up a text file of many U.Wyoming soundings
into individual text files that can be read into python
with pandas. Cuts out the HTML headings (not the column headers)
and the metadata at the bottom of the file.

1. Go here: http://weather.uwyo.edu/upperair/sounding.html
Select "Text: List", date(s) & time(s), and click on the location

2. In command line, where url is the url of the text list:
curl “url” >> /path/to/output/all_sonds_STN.txt

3. Run this script, e.g.,
    import split_soundings as spl
    spl.split_soundings(in_file, out_path)
"""
import os


OUT_PATH = "/home/disk/eos15/jnug/uwyo_soundings/"


def split_soundings(in_file, out_path=OUT_PATH, curled=True):
    """ 
    Splits sounding file for one location into one text file
    for each launch date/time. Assumes the file naming conventions
    from the UWyo files (see above). `in_file` must include file path.
    Makes a subdirectory of the station ID (if it doesn't exist) and places
    all the sounding files there.
    
    curled=True if you used curl to download the file (default) vs. 
    copy/pasting the contents of the webpage into an empty file
    """
    # get station id from the first header (starts on line 4)
    with open(in_file,'r') as f:
        if curled:
            stn_id = f.readlines()[3][4:14]
        else:
            stn_id = f.readlines()[0][:10]
        stn_lab = stn_id.replace(" ", "_")
        
    # make the subdirectory for it to go in
    if out_path[-1] != "/":
        out_path += "/"
    if not os.path.exists(out_path + stn_id[:5]):
        os.mkdir(out_path + stn_id[:5])
    out_path += "{}/".format(stn_id[:5])

    # loop through lines 3 onwards to skip the HTML formatting lines if curled
    with open(in_file,'r') as f:
        if curled:
            for line in f.readlines()[3:]:
                # get the date/time from the header line
                if stn_id in line:
                    tm, dt, mo, yr = line[-21:-6].split()
                    date_lab = "{y}_{m}_{d}_{t}".format(y=yr, m=mo, d=dt, t=tm)
                    f_out = open(out_path + '{s}_{d}.txt'.format(s=stn_lab, d=date_lab), 'w')
                # skip the metadata at the end
                elif ":" in line or "PRE>" in line or "<" in line or ";" in line or "=" in line or "Questions" in line or "-->" in line or "Check" in line: 
                    pass  
                # only write to the file if it's actual data
                else:
                    f_out.write(line)
                    
        else: 
            for line in f.readlines():
                # get the date/time from the header line
                if stn_id in line:
                    tm, dt, mo, yr = line[-16:-1].split()
                    date_lab = "{y}_{m}_{d}_{t}".format(y=yr, m=mo, d=dt, t=tm)
                    f_out = open(out_path + '{s}_{d}.txt'.format(s=stn_lab, d=date_lab), 'w')         
                # skip the metadata at the end
                elif ":" in line or "PRE>" in line or "<" in line or ";" in line or "=" in line or "Questions" in line or "-->" in line or "Check" in line: 
                    pass          
                # only write to the file if it's actual data
                else:
                    f_out.write(line)

