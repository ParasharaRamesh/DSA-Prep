'''
This is a hack to convert recursive code into iterative code by using an explicit stack and a state number

General idea:
1. write the recursive code
2. before & after every recursive function call , give a state number
3. push each state into an explicit stack while maintaining the state's current number
4. If the recursive function returns anything and has a base case then we need to essentially include more things in a frame and keep popping from the stack while updating each of the popped frames which lead to its parent ( which is slightly trickier to implement)


'''

from collections import defaultdict
# Example 1. Inorder traversal
class Node:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


# Recursion: pay attention to the state numbers
def inorder_recursion(node):
    if node is None:
        return
    # state 0: before processing left subtree
    inorder_recursion(node.left)
    # state 1: process current node
    print(node.val, end=' ')
    # state 2: after processing node, process right subtree
    inorder_recursion(node.right)
    # state 3: done with node (implicit)


# Iteration: use the state numbers and convert it:
def inorder_iterative(root):
    state_progress = defaultdict(int) # state -> current state progress
    stack = [root]

    while stack:
        node = stack[-1]
        if node == None:
            stack.pop()
            continue

        if state_progress[node] == 0:
            # State 0: Before processing left, so push left subtree
            stack.append(node.left)
        elif state_progress[node] == 1:
            # State 1: Process the node itself
            print(node.val, end=' ')
        elif state_progress[node] == 2:
            # State 2: Process right subtree
            stack.append(node.right)
        else:
            # State 3: All done with this node, pop from the stack
            stack.pop()

        # for each state increment the progress counter
        state_progress[node] += 1

# Example 2:
def fib_recursive(n):
    if n < 2:
        return n
    # return fib_recursive(n-1) + fib_recursive(n-2) # splitting this into multiple lines so that hack can work

    # state 0
    x = fib_recursive(n - 1)
    # state 1
    y = fib_recursive(n - 2)
    # state 2
    return x + y


def fib_iterative_with_parent(n):
    """
    Compute the nth Fibonacci number by emulating recursion with an explicit stack.

    Each frame is represented as a dictionary with:
      - 'state': the parameter (n) for this recursive call.
      - 'call_index': an integer indicating how many subcalls have finished.
                      For Fibonacci:
                        0 means no recursive subcall is done,
                        1 means the first subcall (fib(n-1)) is done,
                        2 means both subcalls are completed.
      - 'parent': a reference to the parent frame (or None for the root frame).
      - 'frame_result': stores the computed result for this frame; for Fibonacci, once
                        fib(n-1) returns, it is stored here; when fib(n-2) returns, we update
                        frame_result with the sum of these two values.
    """
    # Create the initial (root) frame.
    root_frame = {
        'state': n,  # The input parameter for this call (fib(n)).
        'call_index': 0,  # No subcalls have finished.
        'parent': None,  # This is the root, so no parent.
        'frame_result': None  # Will hold the computed result for this frame.
    }
    # Our stack holds call frames.
    stack = [root_frame]

    final_result = None  # Will eventually hold the final computed Fibonacci number.

    # A helper function for bubbling up a computed result r.
    def bubble_up(r):
        nonlocal final_result
        # Continue to update parent frames as long as there is one.
        while stack:
            parent_frame = stack[-1]
            if parent_frame['call_index'] == 0:
                # Parent is waiting for its first subcall.
                parent_frame['frame_result'] = r
                parent_frame['call_index'] = 1
                # We've updated the parent; break out.
                break
            elif parent_frame['call_index'] == 1:
                # The parent's first subcall is done.
                # Now r is the result of the second subcall.
                # Update parent's frame_result by combining the stored result and r.
                parent_frame['frame_result'] += r
                parent_frame['call_index'] = 2  # This parent's computation is complete.
                r = parent_frame['frame_result']  # New r is the parent's combined result.
                # Pop the parent's frame, as its work is done.
                stack.pop()
            # Continue looping to bubble the result upward.
        # Outside the loop: if the stack is empty, no parent remains.
        if not stack:
            final_result = r

    # Main loop: continue until our stack is empty.
    while stack:
        current_frame = stack[-1]  # Peek at the top frame.
        curr_n = current_frame['state']
        curr_call = current_frame['call_index']

        # --- Base Case ---
        if curr_n < 2:
            # For n=0 or 1 the Fibonacci value is just n.
            r = curr_n
            # Pop the finished frame.
            stack.pop()
            # Bubble the result upward.
            bubble_up(r)
            continue  # Proceed with the next iteration.

        # --- Recursive Case ---
        if curr_call == 0:
            # We're ready to compute fib(n-1).
            new_frame = {
                'state': curr_n - 1,
                'call_index': 0,
                'parent': current_frame,  # Reference to the current frame.
                'frame_result': None
            }
            stack.append(new_frame)
        elif curr_call == 1:
            # First subcall is complete; now compute fib(n-2).
            new_frame = {
                'state': curr_n - 2,
                'call_index': 0,
                'parent': current_frame,
                'frame_result': None
            }
            stack.append(new_frame)
        # When call_index reaches 2, the bubble_up function will handle combining results.

    return final_result



if __name__ == '__main__':
    # Example 1
    root = Node(7)
    root.left = Node(3)
    root.right = Node(10)
    root.left.left = Node(2)
    root.left.right = Node(5)
    root.left.left.left = Node(1)
    root.right.left = Node(8)
    root.right.right = Node(12)

    print(" Example 1 ")
    print("Inorder traversal (recursion):")
    inorder_recursion(root)
    print()

    print("Inorder traversal (iterative):")
    inorder_iterative(root)
    print()

    # Example 2.
    print("\n Example 2 ")
    print(f"fib(19) - recursive => {fib_recursive(19)}")
    print(f"fib(19) - iterative => {fib_iterative_with_parent(19)}")
