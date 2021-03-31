from typing import List
import html


class Cleaner:
    def clean(self, data) -> List:
        for i in range(len(data)):
            row = data[i]

            for index in range(0,len(row)):
                text = str(row[index])
                text = text.replace("’", "'")
                text = str(text.encode('utf-8', 'ignore').decode())
                text = html.unescape(text)
                row[index] = text

            data[i] = row

        return data
