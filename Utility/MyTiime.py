from datetime import datetime
import calendar


class MyTime:

    def __init__(self):
        pass

    #90642928 to 九零六四二九二八
    def numberToText(self, number):

        return str(number).replace("0", "零").replace("1", "一").replace("2", "二") \
            .replace("3", "三").replace("4", "四").replace("5", "五").replace("6", "六") \
            .replace("7", "七").replace("8", "八").replace("9", "九")

    # 2022 to 二零二二年
    def getYear(self, number):
        year = str(number).replace("0", "零").replace("1", "一").replace("2", "二") \
            .replace("3", "三").replace("4", "四").replace("5", "五").replace("6", "六") \
            .replace("7", "七").replace("8", "八").replace("9", "九")

        year += "年"
        return year

    # 03 to 三月
    def getMonth(self, number):
        month = ""
        mList1 = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
        mList2 = ["一月", "二月", "三月", "四月", "五月", "六月", "七月", "八月", "九月",
                  "十月", "十一月", "十二月"]
        for i in range(len(mList1)):
            if number == mList1[i]:
                month = mList2[i]
                break

        return month

    # 05 to 五號
    def getDay(self, number):
        day = ""
        dList1 = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10",
                  "11", "12", "13", "14", "15", "16", "17", "18", "19", "20",
                  "21", "22", "23", "24", "25", "26", "27", "28", "29", "30",
                  "31"]
        dList2 = ["一號", "二號", "三號", "四號", "五號", "六號", "七號", "八號",
                  "九號", "十號", "十一號", "十二號", "十三號", "十四號", "十五號",
                  "十六號", "十七號", "十八號", "十九號", "二十號", "二十一號", "二十二號",
                  "二十三號", "二十四號", "二十五號", "二十六號", "二十七號", "二十八號",
                  "二十九號", "三十號", "三十一號"]

        for i in range(len(dList1)):
            if number == dList1[i]:
                day = dList2[i]
                break

        return day

    # 04 to 四時
    def getHour(self, number):
        hour = ""
        hList1 = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10",
                  "11", "12", "13", "14", "15", "16", "17", "18", "19", "20",
                  "21", "22", "23"]
        hList2 = ["一時", "二時", "三時", "四時", "五時", "六時", "七時", "八時", "九時", "十時",
                  "十一時", "十二時", "十三時", "十四時", "十五時", "十六時", "十七時", "十八時",
                  "十九時", "二十時", "二十一時", "二十二時", "二十三時"]

        for i in range(len(hList1)):
            if number == hList1[i]:
                hour = hList2[i]
                break

        return hour

    # 05 to 五分
    def getMinute(self, number):
        minute = ""
        mList1 = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10",
                  "11", "12", "13", "14", "15", "16", "17", "18", "19", "20",
                  "21", "22", "23", "24", "25", "26", "27", "28", "29", "30",
                  "31", "32", "33", "34", "35", "36", "37", "38", "39", "40",
                  "41", "42", "43", "44", "45", "46", "47", "48", "49", "50",
                  "51", "52", "53", "54", "55", "56", "57", "58", "59"]

        mList2 = ["一分", "二分", "三分", "四分", "五分", "六分", "七分", "八分", "九分", "十分",
                  "十一分", "十二分", "十三分", "十四分", "十五分", "十六分", "十七分", "十八分", "十九分", "二十分",
                  "二十一分", "二十二分", "二十三分", "二十四分", "二十五分", "二十六分", "二十七分", "二十八分",
                  "二十九分", "三十分", "三十一分", "三十二分", "三十三分", "三十四分", "三十五分", "三十六分",
                  "三十七分", "三十八分", "三十九分", "四十分", "四十一分", "四十二分", "四十三分", "四十四分",
                  "四十五分", "四十六分", "四十七分", "四十八分", "四十九分", "五十分", "五十一分", "五十二分",
                  "五十三分", "五十四分", "五十五分", "五十六分", "五十七分", "五十八分", "五十九分"]

        for i in range(len(mList1)):
            if number == mList1[i]:
                minute = mList2[i]
                break

        return minute

    # 06 to 六秒
    def getSecond(self, number):
        second = ""
        sList1 = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10",
                  "11", "12", "13", "14", "15", "16", "17", "18", "19", "20",
                  "21", "22", "23", "24", "25", "26", "27", "28", "29", "30",
                  "31", "32", "33", "34", "35", "36", "37", "38", "39", "40",
                  "41", "42", "43", "44", "45", "46", "47", "48", "49", "50",
                  "51", "52", "53", "54", "55", "56", "57", "58", "59"]

        sList2 = ["一秒", "二秒", "三秒", "四秒", "五秒", "六秒", "七秒", "八秒", "九秒", "十秒",
                  "十一秒", "十二秒", "十三秒", "十四秒", "十五秒", "十六秒", "十七秒", "十八秒", "十九秒", "二十秒",
                  "二十一秒", "二十二秒", "二十三秒", "二十四秒", "二十五秒", "二十六秒", "二十七秒", "二十八秒",
                  "二十九秒", "三十秒", "三十一秒", "三十二秒", "三十三秒", "三十四秒", "三十五秒", "三十六秒",
                  "三十七秒", "三十八秒", "三十九秒", "四十秒", "四十一秒", "四十二秒", "四十三秒", "四十四秒",
                  "四十五秒", "四十六秒", "四十七秒", "四十八秒", "四十九秒", "五十秒", "五十一秒", "五十二秒",
                  "五十三秒", "五十四秒", "五十五秒", "五十六秒", "五十七秒", "五十八秒", "五十九秒"]

        for i in range(len(sList1)):
            if number == sList1[i]:
                second = sList2[i]
                break

        return second

    def getYearMonthDay(self, number, delimiter):
        year = ""
        month = ""
        day = ""

        number = str(number)

        slashCount = number.count(delimiter)
        if slashCount == 2:
            index = number.index(delimiter)
            year = number[:index]
            number = number[index + 1:]
            index = number.index(delimiter)
            month = number[:index]
            day = number[index + 1:]
        else:
            index = number.index(delimiter)
            month = number[:index]
            day = number[index + 1:]

        return (year, month, day)

    def getFullYMD(self, number, delimiter):
        (y, m, d) = self.getYearMonthDay(number, delimiter)
        if y != "":
            year = self.getYear(y)
            month = self.getMonth(m)
            day = self.getDay(d)
            ymd = f"{year}{month}{day}"
        else:
            month = self.getMonth(m)
            day = self.getDay(d)
            ymd = f"{month}{day}"

        return ymd

    def getHourMinuteSecond(self, number, delimiter):
        hour = ""
        minute = ""
        second = ""

        number = str(number)

        slashCount = number.count(delimiter)
        if slashCount == 2:
            index = number.index(delimiter)
            hour = number[:index]
            number = number[index + 1:]
            index = number.index(delimiter)
            minute = number[:index]
            second = number[index + 1:]
        else:
            index = number.index(delimiter)
            minute = number[:index]
            second = number[index + 1:]

        return (hour, minute, second)

    def getFullHMS(self, number, delimiter):
        (h, m, s) = self.getHourMinuteSecond(number, delimiter)
        if h != "":
            hour = self.getHour(h)
            minute = self.getMinute(m)
            seconds = self.getSecond(s)
            hms = f"{hour}{minute}{seconds}"
        else:
            minute = self.getMinute(m)
            seconds = self.getSecond(s)
            hms = f"{minute}{seconds}"

        return hms

    #1665622622.933262
    def getUnixTimeStamp(self):
        today = datetime.utcnow()
        unixTimeStamp = today.timestamp()
        unixDateTime = today.strftime("%Y-%m-%d %H:%M:%S")
        utc_ts = calendar.timegm(today.utctimetuple())
        localDateTime = datetime.fromtimestamp(utc_ts).strftime("%Y-%m-%d %H:%M:%S")
        return (unixTimeStamp, unixDateTime, localDateTime)