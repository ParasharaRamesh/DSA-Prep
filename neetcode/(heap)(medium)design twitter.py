'''
Implement a simplified version of Twitter which allows users to post tweets, follow/unfollow each other, and view the 10 most recent tweets within their own news feed.

Users and tweets are uniquely identified by their IDs (integers).

Implement the following methods:

Twitter() Initializes the twitter object.
void postTweet(int userId, int tweetId) Publish a new tweet with ID tweetId by the user userId. You may assume that each tweetId is unique.
List<Integer> getNewsFeed(int userId) Fetches at most the 10 most recent tweet IDs in the user's news feed. Each item must be posted by users who the user is following or by the user themself. Tweets IDs should be ordered from most recent to least recent.
void follow(int followerId, int followeeId) The user with ID followerId follows the user with ID followeeId.
void unfollow(int followerId, int followeeId) The user with ID followerId unfollows the user with ID followeeId.
Example 1:

Input:
["Twitter", "postTweet", [1, 10], "postTweet", [2, 20], "getNewsFeed", [1], "getNewsFeed", [2], "follow", [1, 2], "getNewsFeed", [1], "getNewsFeed", [2], "unfollow", [1, 2], "getNewsFeed", [1]]

Output:
[null, null, null, [10], [20], null, [20, 10], [20], null, [10]]

Explanation:
Twitter twitter = new Twitter();
twitter.postTweet(1, 10); // User 1 posts a new tweet with id = 10.
twitter.postTweet(2, 20); // User 2 posts a new tweet with id = 20.
twitter.getNewsFeed(1);   // User 1's news feed should only contain their own tweets -> [10].
twitter.getNewsFeed(2);   // User 2's news feed should only contain their own tweets -> [20].
twitter.follow(1, 2);     // User 1 follows user 2.
twitter.getNewsFeed(1);   // User 1's news feed should contain both tweets from user 1 and user 2 -> [20, 10].
twitter.getNewsFeed(2);   // User 2's news feed should still only contain their own tweets -> [20].
twitter.unfollow(1, 2);   // User 1 follows user 2.
twitter.getNewsFeed(1);   // User 1's news feed should only contain their own tweets -> [10].
Constraints:

1 <= userId, followerId, followeeId <= 100
0 <= tweetId <= 1000

Insights:


'''
from heapq import *
from collections import defaultdict


class Twitter:
    def __init__(self):
        self.time = 0
        self.followers = defaultdict(set)
        self.user_tweets = defaultdict(list)  # user -> [(tweetid, global time)]

    def postTweet(self, userId: int, tweetId: int) -> None:
        t = self.time  # copy
        self.user_tweets[userId].append((tweetId, t))
        self.time += 1

    def getNewsFeed(self, userId: int) -> List[int]:
        userIds = [userId] + list(self.followers[userId])
        recent_heap = []
        feed = []

        for uid in userIds:
            for tweetId, time in self.user_tweets[uid]:
                heappush(recent_heap, (-time, tweetId))

        for _ in range(10):
            if not recent_heap:
                break

            _, tweetId = heappop(recent_heap)
            feed.append(tweetId)

        return feed

    def follow(self, followerId: int, followeeId: int) -> None:
        if followeeId != followerId:
            self.followers[followerId].add(followeeId)

    def unfollow(self, followerId: int, followeeId: int) -> None:
        if followerId in self.followers:
            self.followers[followerId].discard(followeeId)

