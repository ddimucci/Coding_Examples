"""
Prompt
Given an integer array nums,
return true if any value appears at least twice in the array,
and return false if every element is distinct.
"""

def contains_duplicates(nums):
    found_nums = {}
    for i in nums:
        if i in found_nums.keys():
            return True
        else:
            found_nums[i] = False
    return False

def contains_duplicates_sorted(nums):
    nums.sort()
    for i in range(len(nums)):
        if nums[i] == nums[i+1]:
            return True
    return False

def contains_duplicates_fast(nums):
    found_nums = {}
    for n in nums:
        if n in found_nums: return True
        else: found_nums[n] = 1
    return False

print("Case 1: nums = [1,2,3,1]")
nums1 = [1,2,3,1]
print(contains_duplicates(nums1))

print("Case 1: nums = [1,2,3,4]")
nums2 = [1,2,3,4]
print(contains_duplicates(nums2))

print("Case 1: nums3 = [1,1,1,3,3,4,3,2,4,2]")
nums3 = [1,1,1,3,3,4,3,2,4,2]
print(contains_duplicates(nums3))

# Comments
"""
Solutions submitted to: https://leetcode.com/problems/contains-duplicate/solutions/
contains_duplicates() is the solution I first came up with on my own. It passes the test cases for leetcode's challenge 
but it passes only 65/70 tests when submitted.

I then thought, if that's too slow, can I sort the list first and dynamically progress through it? This solution works.
In the distribution of solutions I saw my sorting answer was in the 79th percentile for speed and 88th for memory usage, and they share the answers in all the 
percentiles. This led to the third one.

I didn't come up with the third one contains_duplicates_fast() on my own, but I can see that it's the same idea
as my original one. The difference is that it sheds the unnecessary step of calling the .keys() method
That small change makes all the difference.  This solution is 100th percentile for speed and 80th for memory usage
"""
