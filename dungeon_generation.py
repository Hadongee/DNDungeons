import tilemap
import random
import queue

# An arbitrary way to store data about a room
class RoomNode:
    def __init__ (self, index):
        # Index in the rooms array
        self.index = index
        # Has the room been pathed to yet?
        self.pathed = False
        # List of connected rooms
        self.paths = list()

        # In the future this will be replaced with a "roomtype" attribute which will hold info about the type of room.
        # Eg. Dining hall, entrance, storage room ect
        self.min_room_size = 2
        self.max_room_size = 10

# Generates an aritrary set of nodes which a dungeon can then be generated from
# TODO: This whole function should be rethought in the future, it does work but it's very messy
def generate_nodes (node_count, max_connections, max_trials):

    # Instantiate a list of room nodes
    nodes = list()
    for i in range(node_count):
        nodes.append(RoomNode(i))
    
    # Set the entrance room
    entrance = nodes[0]
    entrance.pathed = True

    # Initialize a queue with the entrance room
    nodes_to_path = queue.Queue(maxsize=node_count)
    nodes_to_path.put(entrance)

    # Continue iterating through the queue as long as it is not empty
    while not nodes_to_path.empty():
        # Grab the top node from the queue
        current_node = nodes_to_path.get()

        # Only add paths to the node if it has less paths than the maximum allowed amount
        if len(current_node.paths) < max_connections:

            # Create a random number of additional paths to the current node
            # The lower bound for the randint function is 2-len instead of 1-len to resolve an issue where
            # the entrance node would pick another node and then that node would generate 0 paths resulting 
            # in the end of the function with only 2 rooms connected
            new_path_count = random.randint(2-len(current_node.paths), max_connections - len(current_node.paths))

            if new_path_count > 0:
                for _ in range(0, new_path_count):

                    # Initialize a trial variable to determine when the upcoming while loop should exit
                    trial = 0

                    # The node we are pathing to
                    path_node = None

                    # This loops until the max trials has been reached, this prevents infinite loops where there is no possible path left
                    while trial < max_trials:
                        # Pick a random node to path to
                        path_node = random.choice(nodes)

                        # Check that the node we are pathing to is not ourselves, already part of our paths and has enough paths left
                        # The middle statement is actually very interesting with this statement, changing the amount of max connections creates
                        # a sort of average path amount for each node (Don't know how i just found this through testing)
                        if (path_node != current_node) and (len(path_node.paths) < max_connections/2) and (not (path_node in current_node.paths)):
                            break
                        else:
                            trial += 1
                    # If we exit the loop naturally that means we have run out of trials and we should just assume there are no possible paths
                    else:
                        break

                    # Since we have briken the while loop above that means we just add the path_node to our list of paths
                    current_node.paths.append(path_node)
                    # We also add the current_node to path_node's list of paths
                    path_node.paths.append(current_node)

                    # If the node we are pathing to has already been pathed we don't need to add it to the queue again and we just continue
                    # Otherwise we have to set it's pathing to true and add it to the queue
                    if not path_node.pathed:
                        path_node.pathed = True
                        nodes_to_path.put(path_node)

    # This is a safety mechanism to catch the stray rooms that have no connections and connect them.
    # TODO: This part especially needs reworking. Just messy and there is lots of similarity between the earlier function
    for node in nodes:
        if not node.pathed:
            while True:
                path_node = random.choice(nodes)
                if (path_node != node) and (len(path_node.paths) < max_connections) and (not (path_node in node.paths)):
                    node.pathed = True
                    node.paths.append(path_node)
                    path_node.paths.append(node)
                    break

    #Debug stuff for printing out nodes and their connected rooms
    for node in nodes:
        print("Node[" + str(node.index) + "]: ", end='')
        for path in node.paths:
            print("[" + str(path.index) + "] ", end='')
        print("")

    return nodes

generate_nodes(10, 3, 100)
