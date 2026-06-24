---
title: "[Java Collection] 이더레이터 패턴"
date: 2023-06-02 07:36:25
url_slug: "Java-Collection-이더레이터-패턴"
---

![](https://velog.velcdn.com/images/trendsetter/post/9bcd372c-880b-461e-97b1-8bad3b6faa26/image.png)

Iterator는 자바의 컬렉션 프레임워크에서 컬렉션에 저장되어 있는 요소들을 읽어오는 방법을 표준화한 것이다. 

### About Java Collection...

`collection framwork`란 데이터를 저장하는 클래스들을 표준화한 설계이다.

collection framework는 위 그림과 같이 <span style=color:blue>데이터를 저장하는 구조</span>에 따라 <span style>**3가지 인터페이스**로 나뉜다. 

1. Set: 순서를 유지하지 않는 집합, 데이터 중복 허용 X, HashSet, TreeSet등이 있다.

2. List: 순서를 유지하는 데이터의 집합이다. 데이터의 중복이 허용 O, LinkedList, ArrayList등이 있다.

3. Map: `키`와 `값`으로 이루어진 데이터의 집합이다. 순서는 유지 되지 않으며, 키는 중복을 허락하지 않는다. TreeMap, HashTable,HashMap등이 있다. 

### Iterator 메소드

`Iterator`는 이런 집합체로부터 정보를 얻어낸다. 

집합체를 다룰 떄는 개별적인 클래스에 대해 데이터를 읽는법을 알아야 하므로 각 컬렉션에 접근이 힘들어진다. 

`Iterator`를 통해 어떤 컬렉션이라도 <span style="color:yellow">동일한 방식으로 접근 가능</span>하여 그 안에 있는 항목들에 접근할 수 있는 방법을 제공한다.

`Iterator`메소드로는 hasNext(), next(), remove()가 있다. 
> hasNext: 읽을 요소가 남아있는지 확인, 있으면 true, 없으면 false.
next(): 다음 데이터를 반환한다. 
remove(): next()로 읽어온 요로를 삭제한다. 

다음은 리스트에 들어있는 `일`,`월`,`수` 중 `수`라는 데이터를 삭제하는 예제이다.

```java
import java.util.ArrayList;
import java.util.Iterator;

public class Practice{
	public static void main(Stirngp[]args){
    	System.out.println("List생성");
        ArrayList list = new ArraryList();
        list.add("일");
        list.add("월");
        list.add("수");

		Iterator iter = list.iterator(); //객체 생성
        
        while(iter.hasNext()==true){	// hasNext()
        	String day = (String)iter.next();
            if(day=="수"){
            	iter.remove();
            }
            System.out.println("Day:" + day);
        }
        
        System.out.println("-------------");
        
        iter = list.iterator();
        
        while(iter.hasNext()==true){
        	String day = (String)iter.next();
            System.out.println("Day:" + day);
        }
    }
}


