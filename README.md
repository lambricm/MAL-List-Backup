## MAL List Backup

The code here is for backing up your MAL list.

## Usage

### XML Downloader

```
python xml_download.py -u <username> [-o <output file path>]
```
Where the output file path can either be a folder or a file. If no output file path is inculded, it will default to ./ as the folder and if no file name is included a default format of USERNAME_(ANIME/MANGA)_list_YEAR_MONTH_DAY_UNIQUE-IDENTIFIER.xml will be used.