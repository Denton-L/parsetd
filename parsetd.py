#!/usr/bin/env python3

import csv
import re

class TDParser:
    ENTRY_REGEX = re.compile(r'''<tr class='(?:(?:odd)|(?:even))'>
<td class="first"><a class="expand icon" href="#">\+</a></td>
<td class="date">\d{2}/\d{2}/\d{4}</td>
<td class="description">(?P<Description>[^<]+)
<div class="details">
<div class="item">
Country Code:
<span> [A-Z]{2} - [^<]+
</span>
</div>
<div class="item">
Original Account Number:
<span>\*{8}(?P<Account>\d{4})</span>
</div>
<div class="item">
Currency:
<span>US Dollar \(USD\)</span>
</div>
<div class="item">
Merchant:
<span>[^<]+</span>
</div>
<div class="item">
Merchant Information:
<span class="merchant-value">[^<]+<br/>
[^<]+
</span>
</div>
<div class="item">
Transaction Date:
<span>(?P<Date>\d{2}/\d{2}/\d{4})</span>
</div>
<div class="item">
Posted Date:
<span>\d{2}/\d{2}/\d{4}</span>
</div>
<div class="item">
Transaction Type:
<span>Purchase</span>
</div>
<!--Only display if the Currency codes are different -->
(?:<div class="item">
Source Amount: <span>\$(?P<CAD>\d+\.\d{2})</span>
</div>
<div class="item">
Source Currency: <span>Canadian Dollar \(CAD\)</span>
</div>
<div class="item">
Conversion Rate: <span>\d+\.\d+</span>
</div>)?
<!--End Dif-->
<div class="item">
Reference Number:
<span>\d+</span>
</div>
</div></td>
<td class="amount nowrap">
<span class="nowrap ">(?P<Negative>-?)\$(?P<USD>\d+\.\d{2})</span>
</td>
</tr>'''.replace('\n', ''))

    CURRENCIES = ('CAD', 'USD')
    FIELDS = ('Description', 'Date', 'Account', *CURRENCIES)
    NEGATIVE = 'Negative'

    def main(self, infile, outfile):
        read_lines = ''.join(line.strip() for line in infile if line.strip())

        csv_writer = csv.writer(outfile)

        csv_writer.writerow(self.FIELDS)
        for match in self.ENTRY_REGEX.finditer(read_lines):
            row_list = [match.group(key) for key in self.FIELDS]
            if match.group(self.NEGATIVE):
                for field in self.CURRENCIES:
                    row_list[self.FIELDS.index(field)] = -float(row_list[self.FIELDS.index(field)])
            csv_writer.writerow(row_list)

if __name__ == '__main__':
    import sys

    parser = TDParser()
    parser.main(sys.stdin, sys.stdout)
