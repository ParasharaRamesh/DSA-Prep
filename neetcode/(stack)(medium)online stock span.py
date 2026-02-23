'''
Design an algorithm that collects daily price quotes for some stock and returns the span of that stock's price for the current day.

The span of the stock's price in one day is the maximum number of consecutive days (starting from that day and going backward) for which the stock price was less than or equal to the price of that day.

For example, if the prices of the stock in the last four days is [7,2,1,2] and the price of the stock today is 2, then the span of today is 4 because starting from today, the price of the stock was less than or equal 2 for 4 consecutive days.
Also, if the prices of the stock in the last four days is [7,34,1,2] and the price of the stock today is 8, then the span of today is 3 because starting from today, the price of the stock was less than or equal 8 for 3 consecutive days.
Implement the StockSpanner class:

StockSpanner() Initializes the object of the class.
int next(int price) Returns the span of the stock's price given that today's price is price.
 

Example 1:

Input
["StockSpanner", "next", "next", "next", "next", "next", "next", "next"]
[[], [100], [80], [60], [70], [60], [75], [85]]
Output
[null, 1, 1, 1, 2, 1, 4, 6]

Explanation
StockSpanner stockSpanner = new StockSpanner();
stockSpanner.next(100); // return 1
stockSpanner.next(80);  // return 1
stockSpanner.next(60);  // return 1
stockSpanner.next(70);  // return 2
stockSpanner.next(60);  // return 1
stockSpanner.next(75);  // return 4, because the last 4 prices (including today's price of 75) were less than or equal to today's price.
stockSpanner.next(85);  // return 6
 

Constraints:

1 <= price <= 105
At most 104 calls will be made to next.
'''
'''
Thoughts:

. I went down the wrong way as I thought monotonic stack might not solve it because I didn't apply it in the reverse direction
. basically you care about what is increasing from a point till the last element just added 
. So instead of:

“Who is my previous greater?”

You flip it to:

“Which previous elements have I already proven to be useless?”

The stack is doing lazy compression of history.

'''
class StockSpanner:
    def __init__(self):
        # Use a monotonic stack to store pairs of (price, span)
        self.stack = []

    def next(self, price: int) -> int:
        # The span of the current price starts at 1
        span = 1
        
        # While the stack is not empty and the top element's price 
        # is less than or equal to the current price
        while self.stack and self.stack[-1][0] <= price:
            # Add the span of the previous element to the current span
            span += self.stack.pop()[1]
            
        # Push the current price and its calculated span onto the stack
        self.stack.append((price, span))
        
        return span