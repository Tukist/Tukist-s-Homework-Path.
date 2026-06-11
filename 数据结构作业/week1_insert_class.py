class IterableDeleter:
    def __init__(self, iterable) -> None:
    #  store the original iterable; we work on a copy internally
        self.iterable = iterable

    def delete_at(self, index: int) :
        """Delete the element at ``index`` and shift remaining elements forward.

        :param index: the index of the element to delete (supports negative indices)
        :type index: int
        :return: the modified iterable after deletion
        :rtype: list
        """
        seq = list(self.iterable)
        # shift elements one by one towards the start
        for i in range(index, len(seq) - 1):
            seq[i] = seq[i + 1]
        # remove last element
        seq.pop()
        self.iterable = seq
        return seq
a=IterableDeleter([1, 2, 3, 4, 5])
a.delete_at(2)
print(a.iterable)