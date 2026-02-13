import rclpy
from rclpy.node import Node 
from std_msgs.msg import Int32

# node 1
class NumberPublisher (Node):
    # initialize node 
    def __init__(self):
        super().__init__('Number_Publisher')
        self.publisher = self.create_publisher (Int32 , 'count' 
        , 10)
        self.i = 0 
        self.timer = self.create_timer(0.5, self.timer_callback)

    def timer_callback (self):
        msg = Int32()
        msg.data = self.i 

        # Publish the message
        self.publisher.publish(msg)

        # Print to console (Optional, just to see it working)
        # Note: Usually publisher says "Publishing", subscriber says "Received
        self.get_logger().info('Publishing: %d' %msg.data)
        self.i += 1 


def main (args = None):
    rclpy.init(args = args )
    Number_Publisher = NumberPublisher()
     # 3. Keep the node alive and listening
    rclpy.spin(Number_Publisher)
    # 4. Clean up when we stop (Ctrl+C)
    Number_Publisher.destroy_node()
    rclpy.shutdown()




if __name__ == '__main__' :
    main()