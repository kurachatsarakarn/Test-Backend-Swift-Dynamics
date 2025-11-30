"""
เขียบนโปรแกรมแปลงตัวเลยเป็นคำอ่านภาษาไทย

[Input]
number: positive number rang from 0 to 10_000_000

[Output]
num_text: string of thai number call

[Example 1]
input = 101
output = หนึ่งร้อยเอ็ด

[Example 2]
input = -1
output = number can not less than 0
"""


class Solution:

    def number_to_thai(self, number: int) -> str:
        # Error
        if number < 0:
            return "number can not less than 0"
        if number > 10_000_000:
            return "number over range"
        if number == 0:
            return "ศูนย์"

        # หน่วยหลักภาษาไทย
        th_num = ["", "หนึ่ง", "สอง", "สาม", "สี่", "ห้า", "หก", "เจ็ด", "แปด", "เก้า"]
        th_unit = ["", "สิบ", "ร้อย", "พัน", "หมื่น", "แสน", "ล้าน"]

        def read_under_million(n: int) -> str:
            """อ่านเลขไม่เกิน 6 หลัก (0 - 999,999)"""
            result = ""
            digits = list(map(int, str(n)))
            length = len(digits)

            for i, d in enumerate(digits):
                pos = length - i - 1 

                if d == 0:
                    continue

                if pos == 1:
                    if d == 1:
                        result += "สิบ"
                    elif d == 2:
                        result += "ยี่สิบ"
                    else:
                        result += th_num[d] + "สิบ"

                elif pos == 0:
                    if d == 1 and length > 1:
                        result += "เอ็ด"
                    else:
                        result += th_num[d]

                else:
                    result += th_num[d] + th_unit[pos]

            return result

        if number >= 1_000_000:
            million = number // 1_000_000
            rest = number % 1_000_000
            if rest == 0:
                return read_under_million(million) + "ล้าน"
            else:
                return read_under_million(million) + "ล้าน" + read_under_million(rest)

        return read_under_million(number)
    
