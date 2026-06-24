---
title: "[javaDoc] Queue implementation"
date: 2024-07-23 03:27:39
url_slug: "javaDoc-Queue-implementation"
---

[reference to (javadoc) https://docs.oracle.com/javase/8/docs/api/java/util/Queue.html and chatgpt]
오늘은 자바 컬렉션에 내장되어 있는 프레임워크를 통해 큐와 스택을 구현하는 방법을 알아본다. 

## 큐 구현
"LinkedLest" 클래스를 통해 구현을 하며, 메소드를 포함한 예시 코드는 다음과 같다. 

```java
import java.util.LinkedList;
import java.util.Queue;

public class QueueExample{
	public static void main(String[]args){
    	Queue<Integer> queue = new LinkedList<>();
        
        //Adding elements
        queue.offer(1);
        queue.offer(2);
        
        //Removing elements from the queue and returns the head of the queue
        System.out.println(queue.poll());
        System.out.println(queue.poll());
        
        //Peeking
        queue.peek();
        
        //Checking if the queue contains an element
        System.out.println("Queue contains 3?: ", queue.contains(3));
        //Iterating
    }
}
```

### 삽입

- **offer와 add**가 있으며 둘의 **차이**는 만약 **큐에 요소 삽입 실패시** **예외를 던지느냐 아니냐의 차이**이다. 여느 다른 자료구조 인터페이스의 삽입 메소드와 마찬가지로 add는 IllegalStateException을 던지고 offer는 false를 반환한다. 

- **실제로 코딩테스트나 실무에서 예외처리가 중요한 경우 <span style= color:red>offer()</span>를 사용하는 것이** 실패시 예외 처리를 던지지 않고 false를 반환해 예외처리가 단순해지고 코드가 더 안정적으로 동작하는 측면에서 **안전하다**. 
    예외가 발생하지 않으면 코드의 복잡성이 줄어들고,  실행시간도 단축되기 때문. 아래 예시를 참고한다. 
    
    ```java 
    //using offer
    if(!queue.offer(1)){
    	System.out.println("Failed to add");
    }
    
    //using add
    try{
    	queue.add(2);
    }catch(IllegalStateException e){
    	System.out.println("Failed to add" + e.getMessage());
    }
    
    ```
    
    위와 같이 offer()는 예외 처리 블록이 필요없는 반면, add는 try-catch를 통해 예외 처리를 해주어야 한다. 
    
###     요소 삭제와 출력
![](https://velog.velcdn.com/images/trendsetter/post/bdfd4214-425d-46a4-a9d0-9b32aaf1b047/image.png)
javadoc을 참고한다. 차이는 예외를 던지느냐이다. 
[queue비어 있을때]
- remove(): **예외** 던짐
- poll(): **null 반환**

### 예외(Priority Queue) 및 주의점
1. 다만, 큐는 항상 FIFO방식으로 동작하지는 않는다. 
**예외중 하나는 우선순위 큐**이다. (Prioroty Queue) 

   우선순위 큐는 주어진 comparator나 요소의 자연적인 순서, 그리고 LIFO큐를 사용하여 요소를 정렬한다. 

 따라서 모든 큐 구현은 반드시 정렬 특성을 명시해야 하는것이 중요하겠다. 


2. 또, **<span style = color:red>큐는 null 요소 삽입을 불허</span>**하며, poll()의 반환형이 null일 수 있기에 주의를 기울여야 한다. 

 큐 구현은 일반적으로 메소드 equals와 hashcode의 요소기반 버젼을 정의하기 보단 **Object클래스로부터의 버전을 기반으로한 정체성을 상속받는다.**

 > 정리하자면, 큐의 equals와 hashcode 메소드는 일반적으로 요소기반이 아닌 'Object' 클래스의 기본 구현을 상속 받는다.
 
 즉, **두 큐가 동일한 요소를 갖고 있더라도 서로 가른 객체로 간주됨을 의미**한다. 

 이는 **요소-기반 동등성**이 항상 같은 요소가 있는 큐를 위해서 잘 정의 되어 있기 보다는 **다른 순서 속성을 가진 요소가 있는 큐를 위한 것**이기 때문이다. 


    
    
