# #!/usr/bin/env python

# import rospy
# import actionlib
# from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal

# def move_to_goal(x_goal, y_goal):

#     client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
#     client.wait_for_server()

#     goal = MoveBaseGoal()
#     goal.target_pose.header.frame_id = "map"  
#     goal.target_pose.header.stamp = rospy.Time.now()

#     goal.target_pose.pose.position.x = x_goal
#     goal.target_pose.pose.position.y = y_goal

#     goal.target_pose.pose.orientation.w = 1.0

#     client.send_goal(goal)
#     wait = client.wait_for_result()

#     if not wait:
#         rospy.logerr("Action server not available!")
#         rospy.signal_shutdown("Action server not available!")
#     else:
#         return client.get_result()


# if __name__ == '__main__':
#     try:
#         rospy.init_node('move_to_goal_node', anonymous=True)

#         # Hedef konum (X, Y)
#         x_goal = -1.0
#         y_goal = 1.0

#         result = move_to_goal(x_goal, y_goal)

#         if result:
#             rospy.loginfo("Goal reached successfully!")

#     except rospy.ROSInterruptException:
#         rospy.loginfo("Navigation test finished.")




# import rospy
# from geometry_msgs.msg import Twist
# from nav_msgs.msg import Odometry
# import math

# class MoveToGoal:
#     def __init__(self):
#         rospy.init_node('move_to_goal', anonymous=True)
#         self.pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
#         self.sub = rospy.Subscriber('/ground_truth/state', Odometry, self.odometry_callback)

#         self.current_position = (0, 0, 0)
#         self.goal = (0, 0, 1)  # Hedef konum (x, y, z)
#         self.rate = rospy.Rate(10)  # Hz

#     def odometry_callback(self, msg):
#         self.current_position = (msg.pose.pose.position.x, msg.pose.pose.position.y, msg.pose.pose.position.z)

#     def takeoff(self):
#         takeoff_cmd = Twist()
#         takeoff_cmd.linear.z = 1.0  # Yukarı doğru hareket
#         for _ in range(5):  # 5 döngü boyunca yukarı hareket
#             self.pub.publish(takeoff_cmd)
#             self.rate.sleep()

#     def move_to_goal(self):
#         while not rospy.is_shutdown():
#             twist = Twist()
#             distance = math.sqrt((self.goal[0] - self.current_position[0])**2 +
#                                  (self.goal[1] - self.current_position[1])**2 +
#                                  (self.goal[2] - self.current_position[2])**2)

#             if distance > 0.1:  # 10 cm'lik bir tolerans
#                 angle_to_goal = math.atan2(self.goal[1] - self.current_position[1], self.goal[0] - self.current_position[0])
#                 twist.linear.x = 0.5  # İleri hareket hızı
#                 twist.angular.z = angle_to_goal  # Hedefe yönelmek için açı
#             else:
#                 twist.linear.x = 0
#                 twist.angular.z = 0
#                 rospy.loginfo("Hedefe ulaşıldı!")

#             self.pub.publish(twist)
#             self.rate.sleep()

# if __name__ == '__main__':
#     try:
#         mover = MoveToGoal()
#         mover.takeoff()  # Kalkış
#         mover.move_to_goal()  # Hedefe hareket
#     except rospy.ROSInterruptException:
#         pass

#!/usr/bin/env python

#!/usr/bin/env python

import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal

class TurtleBotNavigator:
    def __init__(self):
        self.client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
        rospy.loginfo("move_base action client başlatılıyor...")
        self.client.wait_for_server()
        rospy.loginfo("move_base action client hazır.")

    def move_to_goal(self, x, y):
        goal = MoveBaseGoal()
        goal.target_pose.header.frame_id = "map"
        goal.target_pose.header.stamp = rospy.Time.now()
        goal.target_pose.pose.position.x = x
        goal.target_pose.pose.position.y = y
        goal.target_pose.pose.orientation.w = 1.0  # Doğru yönlendirme

        rospy.loginfo(f"Hedefe gidiliyor: x={x}, y={y}")
        self.client.send_goal(goal)
        self.client.wait_for_result()  # Sonucu bekle

        if self.client.get_state() == actionlib.GoalStatus.SUCCEEDED:
            rospy.loginfo(f"Hedefe varıldı: x={x}, y={y}")
        else:
            rospy.logerr("Hedefe varılamadı!")

if __name__ == '__main__':
    try:
        rospy.init_node('turtlebot_navigator', anonymous=True)
        navigator = TurtleBotNavigator()

        # Hedef konumları
        goals = [(2.0, 3.0), (-2.0, 4.0), (1.5, -1.0)]
        for goal in goals:
            rospy.loginfo(f"{goal} konumuna gidiliyor...")
            navigator.move_to_goal(goal[0], goal[1])

    except rospy.ROSInterruptException:
        rospy.loginfo("Navigasyon sonlandırıldı.")

