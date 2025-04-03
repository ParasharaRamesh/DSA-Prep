'''
Design a time-based key-value data structure that can store multiple values for the same key at different time stamps and retrieve the key's value at a certain timestamp.

Implement the TimeMap class:

TimeMap() Initializes the object of the data structure.
void set(String key, String value, int timestamp) Stores the key key with the value value at the given time timestamp.
String get(String key, int timestamp) Returns a value such that set was called previously, with timestamp_prev <= timestamp. If there are multiple such values, it returns the value associated with the largest timestamp_prev. If there are no values, it returns "".


Example 1:

Input
["TimeMap", "set", "get", "get", "set", "get", "get"]
[[], ["foo", "bar", 1], ["foo", 1], ["foo", 3], ["foo", "bar2", 4], ["foo", 4], ["foo", 5]]
Output
[null, null, "bar", "bar", null, "bar2", "bar2"]

Explanation
TimeMap timeMap = new TimeMap();
timeMap.set("foo", "bar", 1);  // store the key "foo" and value "bar" along with timestamp = 1.
timeMap.get("foo", 1);         // return "bar"
timeMap.get("foo", 3);         // return "bar", since there is no value corresponding to foo at timestamp 3 and timestamp 2, then the only value is at timestamp 1 is "bar".
timeMap.set("foo", "bar2", 4); // store the key "foo" and value "bar2" along with timestamp = 4.
timeMap.get("foo", 4);         // return "bar2"
timeMap.get("foo", 5);         // return "bar2"


Constraints:

1 <= key.length, value.length <= 100
key and value consist of lowercase English letters and digits.
1 <= timestamp <= 107
All the timestamps timestamp of set are strictly increasing.
At most 2 * 105 calls will be made to set and get.

'''

from bisect import bisect_left


class TimeMap:
    def __init__(self):
        self.map = dict()

    def set(self, key: str, value: str, timestamp: int) -> None:
        if key not in self.map:
            self.map[key] = [(timestamp, value)]
        else:
            # put it in the right place (but constraints say that it is strictly increasing so just append)
            self.map[key].append((timestamp, value))

    def get(self, key: str, timestamp: int) -> str:
        if key not in self.map:
            return ""

        time_values = self.map[key]

        # using classic hardcoded binary search
        return self.bs_left(time_values, timestamp)

        # using bisect
        # ind = bisect_left(time_values, timestamp, key= lambda tv: tv[0])

        # if ind == len(time_values):
        #     return time_values[ind-1][1]
        # elif time_values[ind][0] == timestamp:
        #     return time_values[ind][1]
        # elif ind > 0:
        #     return time_values[ind-1][1]
        # else:
        #     return ""

    def bs_left(self, time_values, timestamp):
        l = 0
        r = len(time_values) - 1

        while l <= r:
            m = (l + r) // 2

            if timestamp <= time_values[m][0]:
                r = m - 1
            else:
                l = m + 1

        if 0 <= l < len(time_values) and timestamp == time_values[l][0]:
            #if l in range then choose this
            return time_values[l][1]
        elif 0 <= r < len(time_values):
            # if r in range
            return time_values[r][1]
        else:
            return ""


# Your TimeMap object will be instantiated and called as such:
# obj = TimeMap()
# obj.set(key,value,timestamp)
# param_2 = obj.get(key,timestamp)
