from enum import Enum


class Sorting(str, Enum):
    DESCENDING = "descending"
    ASCENDING = "ascending"


SORTING_TRANSLATE = {
    Sorting.ASCENDING: "正序",
    Sorting.DESCENDING: "倒序",
}
