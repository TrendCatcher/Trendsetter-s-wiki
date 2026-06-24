---
title: "[자바- 우선순위 큐] PriorityQueue "
date: 2024-07-17 01:40:04
url_slug: "자바-우선순위-큐-PriorityQueue"
---

# Priority Queue

[reference by javadoc] https://docs.oracle.com/javase/8/docs/api/java/util/PriorityQueue.html

오늘은 자바의 우선순위 큐에 대해 이야기 해보자 한다. 

데이터를 저장할 때 우선순위에 따라 정렬하여 저장하는 자료구조이며,  이 자료구조를 구현하는 것은 Class PriorityQueue <E>, 즉, 클래스임을 알 수 있다. 
다음은 몇가지 특징들이다. 
  
## 1. 우선순위 큐 특징

  
- **우선순위 힙을 기반**으로한 **무제한** 우선순위 큐
  

  - 우선 순위 큐의 요소들은 그들의 자연적인 순서를 따르거나, 큐 생성시 제공된 Comparator에 따라 정렬된다.
  

  - null element는 불허한다. 

  - 비교가 불가능한 객체 삽입은 불가하다. 

  - **큐의 헤드**는 지정된 순서에서 **가장 작은 요소**
  
  - Time complexity(시간 복잡도): 
  	- 요소 삽입, 삭제 메소드 offer(), poll(), remove(): **O(log(n))**
  	- remove(object), contains(Object): **O(1)**, constant time
  	- 반환형 메소드 (peek,element): **O(n)**, linear time
  
  
  ## 2. 유용한 생성자들
  
  - 기본 생성자 **'PriorityQueue()'**
  	- 가장 기본적인 생성자이며, 기본 초기 용량이 11이며 자연 순서에 따라 정렬되는 우선순위 큐이다. 
  
  ```java
  import java.util.PriorityQueue;
  
  public class main{
  	public static void main(String[]args){
  		int nums[]={3,...4}//총 11개
  		PriorityQueue<Integer> priorityqueue = new PriorityQueue<>();
  
  		for(int num : nums){
  			priorityqueue.add(num)
  		}
  
  		// 최소값 출력
  		System.out.println("Minimun value: " + priority.poll());
  	}
  }
  
  ```

  - 초기 용량을 지정하는 생성자: **'PriorityQueue(int initialCapacity)'** 
  	- 데이터가 많은 경우 초기용량을 지정하여 공간의 효율성을 높이고 성능을 최적화 시킨다.
  ```java 
  
  PriorityQueue<Integer> priorityqueue = new PriorityQueue<>(1000);
  // 1000개의 요소를 큐에 추가
  for(int i=; i<1000; i++){
    priorityqueue.offer((int)(Math.random()* 1000));
                                                        }                                                
  ```
                                                                 
                                                                 - Comparator를 사용하는 생성자 'PriorityQueue(Comparator<? super E> comparator)'
```java
                                                                 
import java.util.Collections;
                                                                                                                         public class Main{
	public static void main(String[]args){
    	int nums= {3,1,.....};
        PriorityQueue<Integer> pq = new PriorityQueue<>(Collections.reverseOrder());		// 우선순위 큐 선언
  
  	for(int num:nums){
  		pq.offer(num);	// 우선순위 큐에 배열안의 수 값 넣고
  	}
  
  	System.out.println("Maximum value" + pq.poll());
  }
                                                                 }    
```
-초기용량과 Comparator를 지정하는 우선순위 큐
	- 이 생성자는 초기 용량과 사용자 정의 Comparator를 사용하여 우선순위 큐를 생성합니다. 
  >
  <예시: 특정 정렬 기준과 큰 데이터 세트 처리>
  
  ```java
  import java.util.Comparator;
  import java.util.PriorityQueue;
  
  public class Main{
  	public static void main(String[]args){
  		int nums[]=  new int [1000];
  		for(int i=0; i<1000;i++){
        	nums[i] =(int)(Math.random()*1000);              
    		}
    		Comparator<Integer> pq = new PriorityQueue<>(1000,customComparator);
  		for(int num: nums){
  			pq.add(num);
  		}
  //최댓값 출력
  	System.out.println("Maximum value: "+ pq.poll());
  	}
  }
  ```
  
  추가적으로 초기 용량을 굳이 조절하는 우선 순위의 생성자의 경우 그 효율성에 대해 정리한다. 
  #### 1. 공간 효율성 향상
  초기 용량을 지정하면 내부 배열의 크기를 미리 설정할 수 있으므로, 큐가 커질 때 마다 반복적으로 배열을 확장할 필요가 없다.
  
  #### 2. 성능 최적화
  초기 용량을 지정함으로써 배열 확정과 관련된 오버헤드를 줄일 수 있습니다. 배열 확장은 시간 복잡도가 O(n)이므로 초기 용량을 설정하면 이러한 작업 빈도를 낮출 수 있다. 
  - **삽입시간 단축**
  
                                                
                                                                 

