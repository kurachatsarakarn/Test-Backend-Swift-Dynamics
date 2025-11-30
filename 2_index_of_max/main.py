"""
เขียบนโปรแกรมหา index ของตัวเลขที่มีค่ามากที่สุดใน list

[Input]
numbers: list of numbers

[Output]
index: index of maximum number in list

[Example 1]
input = [1,2,1,3,5,6,4]
output = 5

[Example 2]
input = []
output = list can not blank
"""


class Solution:

    def find_max_index(self, numbers: list) -> int | str:
        # ถ้า list ว่าง
        if not numbers:
            return "list can not blank"

        # เริ่มจาก index 0 เป็นค่ามากที่สุดก่อน
        max_index = 0

        # วนตั้งแต่ตัวที่ 1 ถึงตัวสุดท้าย
        for i in range(1, len(numbers)):
            # ถ้าเจอค่าที่มากกว่า index เดิม → อัปเดต
            if numbers[i] > numbers[max_index]:
                max_index = i

        return max_index
    

