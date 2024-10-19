![chart (2)](https://github.com/user-attachments/assets/1667cd08-80db-4cd7-aa4d-ad658e82510a)

사용자가 ai model에 training을 위해 이미지 데이터를 전달하는 과정인 input data pipeline에 대해 최적화를 진행해 보았다. 
최적화 방식은 총 2가지를 진행을 해 보았다. 

Input data pipeline은 SimCLR의 input data pipeline을 참고를 해서 구성을 하였다. 


하지만 resize연산을 추가함.

1. Operation Reordering


2. Pushing back Float conversion 
