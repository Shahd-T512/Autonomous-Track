import rclpy
from rclpy.node import Node 
from std_msgs.msg import Int32

# class node 
# node 2
class NumberCounter (Node):
    #initialize node 
    def __init__(self):
        super().__init__('Number_Counter')
        self.subscription = self.create_subscription (
            Int32 , 
            'count',
            self.listener_callback,
            10
        )
        self.subscription   #prevent unused variable warning
    
    def listener_callback(self,msg):
        self.get_logger().info('Recieved : %d'%msg.data)

def main (args = None):
    rclpy.init(args = args) # to be able to enter parameter if I want through terminal 
    # creating object from class 
    Number_Counter = NumberCounter()
    # to loop forever until stop manually
    rclpy.spin (Number_Counter)

    # destroy node after finishing
    Number_Counter.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()