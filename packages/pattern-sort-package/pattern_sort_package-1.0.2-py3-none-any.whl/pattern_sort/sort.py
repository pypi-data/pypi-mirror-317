class Sort:
    def bubble_sort(self, arr):
        """Sorts a list using bubble sort."""
        n = len(arr)
        for i in range(n):
            for j in range(0, n - i - 1):
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
        return arr

    def selection_sort(self, arr):
        """Sorts a list using selection sort."""
        for i in range(len(arr)):
            min_idx = i
            for j in range(i + 1, len(arr)):
                if arr[j] < arr[min_idx]:
                    min_idx = j
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
        return arr

    def insertion_sort(self, arr):
        """Sorts a list using insertion sort."""
        for i in range(1, len(arr)):
            key = arr[i]
            j = i - 1
            while j >= 0 and key < arr[j]:
                arr[j + 1] = arr[j]
                j -= 1
            arr[j + 1] = key
        return arr

    def merge_sort(self, arr):
        """Sorts a list using merge sort."""
        if len(arr) > 1:
            mid = len(arr) // 2
            left = arr[:mid]
            right = arr[mid:]

            self.merge_sort(left)
            self.merge_sort(right)

            i = j = k = 0
            while i < len(left) and j < len(right):
                if left[i] < right[j]:
                    arr[k] = left[i]
                    i += 1
                else:
                    arr[k] = right[j]
                    j += 1
                k += 1

            while i < len(left):
                arr[k] = left[i]
                i += 1
                k += 1

            while j < len(right):
                arr[k] = right[j]
                j += 1
                k += 1
        return arr

    def quick_sort(self, arr):
        """Sorts a list using quick sort."""
        if len(arr) <= 1:
            return arr
        pivot = arr[0]
        less = [x for x in arr[1:] if x <= pivot]
        greater = [x for x in arr[1:] if x > pivot]
        return self.quick_sort(less) + [pivot] + self.quick_sort(greater)

    def heap_sort(self, arr):
        """Sorts a list using heap sort."""
        def heapify(arr, n, i):
            largest = i
            left = 2 * i + 1
            right = 2 * i + 2

            if left < n and arr[i] < arr[left]:
                largest = left

            if right < n and arr[largest] < arr[right]:
                largest = right

            if largest != i:
                arr[i], arr[largest] = arr[largest], arr[i]
                heapify(arr, n, largest)

        n = len(arr)
        for i in range(n // 2 - 1, -1, -1):
            heapify(arr, n, i)

        for i in range(n - 1, 0, -1):
            arr[i], arr[0] = arr[0], arr[i]
            heapify(arr, i, 0)
        return arr

    def shell_sort(self, arr):
        """Sorts a list using shell sort."""
        n = len(arr)
        gap = n // 2

        while gap > 0:
            for i in range(gap, n):
                temp = arr[i]
                j = i
                while j >= gap and arr[j - gap] > temp:
                    arr[j] = arr[j - gap]
                    j -= gap
                arr[j] = temp
            gap //= 2
        return arr

    def counting_sort(self, arr):
        """Sorts a list using counting sort."""
        max_val = max(arr)
        count = [0] * (max_val + 1)

        for num in arr:
            count[num] += 1

        sorted_arr = []
        for i, c in enumerate(count):
            sorted_arr.extend([i] * c)
        return sorted_arr

    def radix_sort(self, arr):
        """Sorts a list using radix sort."""
        max_val = max(arr)
        exp = 1
        while max_val // exp > 0:
            self._counting_sort_by_digit(arr, exp)
            exp *= 10
        return arr

    def _counting_sort_by_digit(self, arr, exp):
        """Helper for radix sort."""
        n = len(arr)
        output = [0] * n
        count = [0] * 10

        for num in arr:
            index = (num // exp) % 10
            count[index] += 1

        for i in range(1, 10):
            count[i] += count[i - 1]

        i = n - 1
        while i >= 0:
            index = (arr[i] // exp) % 10
            output[count[index] - 1] = arr[i]
            count[index] -= 1
            i -= 1

        for i in range(n):
            arr[i] = output[i]

    def bucket_sort(self, arr):
        """Sorts a list using bucket sort."""
        if len(arr) == 0:
            return arr

        bucket_count = 10
        max_val = max(arr)
        size = max_val / bucket_count

        buckets = [[] for _ in range(bucket_count)]
        for num in arr:
            bucket_index = int(num / size)
            if bucket_index != bucket_count:
                buckets[bucket_index].append(num)
            else:
                buckets[bucket_count - 1].append(num)

        for bucket in buckets:
            bucket.sort()

        result = []
        for bucket in buckets:
            result.extend(bucket)
        return result