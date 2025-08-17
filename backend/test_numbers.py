from backend.main import number_to_chinese

def test_number_to_chinese():
    cases = {
        0: "零",
        5: "五",
        10: "十",
        11: "十一",
        20: "二十",
        101: "一百零一",
        110: "一百一十",
        1001: "一千零一",
        2020: "二千零二十",
        1200: "一千二百",
    }
    for num, expected in cases.items():
        assert number_to_chinese(num) == expected
