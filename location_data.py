import csv
from typing import TypedDict, cast


# other unused columns in Location:
# "roomid", "area", "xy","plmtypename","state","roomname","alternateroomid"
class Location(TypedDict):
    fullitemname: str
    locids: list[int]
    plmtypeid: int
    plmparamhi: int
    plmparamlo: int
    hiddenness: str
    alternateroomlocids: list[int]
    alternateroomdifferenthiddenness: str
    inlogic: bool


def pullCSV() -> dict[str, Location]:
    csvdict: dict[str, Location] = {}

    def commentfilter(line: str) -> bool:
        return (line[0] != '#')

    with open('subversiondata12.csv', 'r') as csvfile:
        reader = csv.DictReader(filter(commentfilter, csvfile))
        for row in reader:
            # commas within fields -> array
            row['locids'] = row['locids'].split(',')
            row['alternateroomlocids'] = row['alternateroomlocids'].split(',')
            # hex fields we want to use -> int
            row['locids'] = [int(locstr, 16)
                             for locstr in row['locids'] if locstr != '']
            row['alternateroomlocids'] = [
                int(locstr, 16) for locstr in row['alternateroomlocids'] if locstr != '']
            row['plmtypeid'] = int(row['plmtypeid'], 16)
            row['plmparamhi'] = int(row['plmparamhi'], 16)
            row['plmparamlo'] = int(row['plmparamlo'], 16)
            # new key: 'inlogic'
            row['inlogic'] = False
            csvdict[row['fullitemname']] = cast(Location, row)
    return csvdict