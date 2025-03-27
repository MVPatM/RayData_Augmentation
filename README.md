![Image](https://github.com/user-attachments/assets/0caed200-2c62-4d20-aabb-25b19ff85f2d)

사용자가 ai model에 training을 위해 데이터를 전달하는 과정인 input data pipeline에 대해 최적화를 진행했다. 
ImageNet-1k image dataset을 이용해서 최적화의 정도를 판단했다. 
Input data pipeline을 구축하기 위해서 ray framework를 사용했고 그 중에서 ray data library를 사용해서 구현했다. 
Aws환경에서 여러 개의 node들로 구성된 ray cluster를 구축해서 optimization rule을 적용한 경우와 적용하지 않은 경우에 대해 연산속도를 비교했다.
추가적으로 ray cluster에 사용된 node의 개수에 따라 연산속도가 어떻게 달라지는 지를 비교했다. Node가 1개, 4개, 8개인 경우를 각각 비교했다. 

Input data pipeline은 SimCLR의 input data pipeline을 참고해서 구성했다. 
![simclr](https://github.com/user-attachments/assets/e94174a8-00d9-4eb7-8dab-7adecb91d67a)



Ray Data의 내부와 Albumentations library의 내부 모두 최적화를 진행했다. 

<Albumentations library 내부>
1. Operation Reordering function 추가
   연산의 양을 줄여주는 crop, 등의 연산을 먼저 수행하도록 operation순서를 변경해주는 기능이다. 
  
2. Pushing down Float conversion function 추가
   Float type으로 연산을 진행할 필요가 있을 때까지 float연산을 뒤로 미루는 기능이다. 

<Ray Data 내부>

test_rule이라는 optimization rule을 ray data내부에 추가, 이 rule에서는 입력받은 UDF을 확인하고 operation reordering과 pushdown float최적화 방식을 수행한다.
